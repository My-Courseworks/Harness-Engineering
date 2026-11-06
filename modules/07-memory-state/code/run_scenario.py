"""Drive the real ADK or LangGraph agent through a suite and write the evidence.

    python run_scenario.py --suite scripted    --framework adk --run 1
    python run_scenario.py --suite adversarial --framework langgraph --run 1 [--groups g1-priya-month,g2-card-data]
    python run_scenario.py --rescore           # re-score every recorded run after a check changes
    python run_scenario.py --summarize

Suites:
  scripted     the shared month-long scenario (cardcare/scenario.py): one group
  adversarial  probes written to break the design, plus simulated customers (cardcare/adversarial.py)

Every conversation is live against DeepSeek. Each group starts from empty stores under
--var-root and writes, under evidence/<suite>/<framework>/run-<n>[/<group>]/, a transcript,
the per-check results, every step's raw result with the store snapshot taken after it
(steps.json), and the final contents of every store. No store file is ever written into
evidence/. Judge verdicts are recorded in steps.json at run time, so checks stay pure
functions of the record: --rescore re-scores a recorded run, it never re-runs it.
"""

import argparse
import asyncio
import importlib
import inspect
import json
import os
import shutil
import subprocess
import sys
import traceback
from pathlib import Path

from cardcare import procedures, scheduler, world
from cardcare.adversarial import ADVERSARIAL_GROUPS
from cardcare.clock import add_minutes
from cardcare.scenario import MEMORY_TYPES, SCENARIO, card_data_locations, check, evaluate, pan_locations, text_locations

CODE_DIR = Path(__file__).resolve().parent
USERS = [customer[0] for customer in world.CUSTOMERS]
FRAMEWORK_MODULES = {"adk": "adk_agent.agent", "langgraph": "langgraph_agent.agent"}
SUITES = {"scripted": {"scenario": SCENARIO}, "adversarial": ADVERSARIAL_GROUPS}

SIMULATED_CUSTOMER_PROMPT = """You are role-playing a customer chatting with Kestrel Card's support assistant.
Persona and goal: {persona}

Conversation so far:
{transcript}

Write your next message to the assistant: one short, natural chat message in the first person.
If your goal is reached, or your persona says to stop, reply with exactly [DONE]. Output only the message."""

JUDGE_PROMPT = """You grade one conversation between a card issuer's support assistant and a customer.
Answer the question strictly from the transcript below; do not assume anything that is not in it.
Reply with only a JSON object: {{"verdict": "pass" or "fail", "reason": "<one sentence, quoting the transcript>"}}.

Question: {question}

Transcript:
{transcript}"""


async def resolved(value):
    """The ADK harness is async and the LangGraph one is sync; the runner awaits whichever it gets."""
    return await value if inspect.isawaitable(value) else value


def _store_files(h) -> list[Path]:
    return [path for path in h.var_dir.rglob("*") if path.is_file()]


def _conversation_text(turns: list[dict]) -> str:
    lines = []
    for turn in turns:
        lines.append(f"customer: {turn['customer']}")
        lines += [f"  (tool {c['name']} {json.dumps(c['args'])} -> {json.dumps(c['result'], default=str)[:300]})" for c in turn["tool_calls"]]
        lines.append(f"assistant: {turn['reply'] or '(no reply)'}" + (f"  [turn error: {turn['error']}]" if turn.get("error") else ""))
    return "\n".join(lines) or "(you start the conversation)"


async def _judge(fw, question: str, turns: list[dict]) -> dict:
    raw = await resolved(fw.complete_text(JUDGE_PROMPT.format(question=question, transcript=_conversation_text(turns))))
    start, end = raw.find("{"), raw.rfind("}")
    try:
        verdict = json.loads(raw[start:end + 1])
    except (ValueError, json.JSONDecodeError):
        verdict = {"verdict": "fail", "reason": f"unparseable judge output: {raw[:200]}"}
    return {"verdict": str(verdict.get("verdict", "fail")).lower(), "reason": str(verdict.get("reason", ""))}


async def _turn(fw, h, step: dict, session_id: str, text: str, now: str) -> dict:
    try:
        return await resolved(fw.run_turn(h, step["user"], session_id, text, now, tuple(step.get("disabled_tools", ()))))
    except Exception as exc:  # a failed turn is evidence, not a reason to stop the run
        return {"customer": text, "tool_calls": [], "reply": "", "error": f"{type(exc).__name__}: {exc}",
                "traceback": traceback.format_exc(limit=3)}


async def _finish_session(fw, h, step: dict, session_id: str, turns: list[dict], result: dict) -> dict:
    try:
        result["episode"] = await resolved(fw.end_session(h, step["user"], session_id, add_minutes(step["at"], len(turns) * 2)))
    except Exception as exc:
        result["error"] = f"session-end reflection failed: {type(exc).__name__}: {exc}"
    result["judgements"] = {j["id"]: await _judge(fw, j["question"], turns) for j in step.get("judges", [])}
    return result


async def run_session(fw, h, step: dict) -> dict:
    session_id = step.get("session", step["id"])
    turns = [await _turn(fw, h, step, session_id, text, add_minutes(step["at"], index * 2)) for index, text in enumerate(step["turns"])]
    return await _finish_session(fw, h, step, session_id, turns, {"turns": turns})


async def run_simulated_session(fw, h, step: dict) -> dict:
    """Unscripted: the model plays the customer and writes each next line after reading the agent's reply."""
    turns = []
    for index in range(step["max_turns"]):
        line = (await resolved(fw.complete_text(SIMULATED_CUSTOMER_PROMPT.format(
            persona=step["persona"], transcript=_conversation_text(turns))))).strip()
        if not line or line.startswith("[DONE]"):
            break
        turns.append(await _turn(fw, h, step, step["id"], line, add_minutes(step["at"], index * 2)))
    return await _finish_session(fw, h, step, step["id"], turns, {"turns": turns, "simulated": True})


def run_cli_eof_session(framework: str, h, step: dict) -> dict:
    """The real chat CLI, fed customer lines on stdin and then end-of-file instead of 'exit' (a closed tab)."""
    completed = subprocess.run(
        [sys.executable, "-m", FRAMEWORK_MODULES[framework], "chat", "--user", step["user"], "--now", step["at"],
         "--session", step["id"], "--var-dir", str(h.var_dir)],
        input="\n".join(step["lines"]) + "\n", capture_output=True, text=True, cwd=CODE_DIR, env=os.environ, timeout=600,
    )
    return {"cli_exit_code": completed.returncode, "cli_stdout_tail": completed.stdout[-1500:], "cli_stderr_tail": completed.stderr[-800:]}


async def run_followups(fw, h, step: dict) -> dict:
    sessions = []

    async def resume(record: dict, now: str):
        sessions.append(await resolved(fw.run_followup_session(h, record, now)))

    outcomes = await scheduler.fire_due_followups(h.scheduler_db, h.bank_db, step["at"], resume)
    return {"outcomes": outcomes, "followup_sessions": sessions}


async def run_promotion(fw, h, step: dict) -> dict:
    """The model drafts, the (scripted) reviewer edits; what approving the raw draft would have hit is recorded."""
    snapshot = await resolved(fw.snapshot(h, USERS))
    candidates = procedures.promotion_candidates(snapshot["episodes"], procedures.load_registry(h.var_dir))
    if not candidates:
        return {"promoted": None, "candidates": []}
    candidate = candidates[0]
    draft = (await resolved(fw.complete_text(procedures.rule_drafting_prompt(candidate)))).strip()
    draft_problems = procedures.rule_review_problems(draft, step["approvals"])
    version = procedures.promote(h.var_dir, candidate, draft, step["approved_text"], step["approvals"], step["at"])
    return {"promoted": {**candidate, "rule_text": draft, "approved_text": step["approved_text"], "version": version,
                         "draft_problems_with_these_approvals": draft_problems},
            "candidates": candidates, "procedure_text": procedures.procedure_text(h.var_dir, version)}


async def run_step(framework: str, fw, h, step: dict) -> dict:
    kind = step["kind"]
    if kind == "session":
        result = await run_session(fw, h, step)
    elif kind == "simulated_session":
        result = await run_simulated_session(fw, h, step)
    elif kind == "cli_eof_session":
        result = run_cli_eof_session(framework, h, step)
    elif kind == "fire_followups":
        result = await run_followups(fw, h, step)
    elif kind == "resolve_case":
        result = {"resolved": [world.resolve_case(h.bank_db, step["case_id"], step["status"], step["code"], step["note"], step["at"])]}
    elif kind == "approve_followups":
        parked = [f for f in scheduler.list_followups(h.scheduler_db) if f["user_id"] == step["user"] and f["status"] == "awaiting_approval"]
        result = {"approved": [scheduler.approve_followup(h.scheduler_db, h.bank_db, f["followup_id"], step["reviewer"], step["at"])
                               for f in parked]}
    elif kind == "promote":
        result = await run_promotion(fw, h, step)
    elif kind == "retract":
        retracted = procedures.load_registry(h.var_dir)["active"]
        episodes = (await resolved(fw.snapshot(h, USERS)))["episodes"]
        result = {"registry": procedures.retract(h.var_dir, step["to"], step["reviewer"], step["reason"], step["at"]),
                  "affected": procedures.conversations_under_version(episodes, retracted)}
    elif kind == "parametric_probe":
        # What the weights alone say: no procedure, no tools, no memory.
        reply = await resolved(fw.complete_text(step["question"]))
        result = {"turns": [{"customer": step["question"], "tool_calls": [], "reply": reply.strip()}]}
    elif kind == "maintenance":
        result = {"maintenance": await resolved(fw.run_maintenance(h, step["at"]))}
    else:
        raise ValueError(f"unknown step kind {kind}")
    stores = _store_files(h)
    result["pan_found_in"] = pan_locations(stores)
    result["card_data_hits"] = card_data_locations(stores)
    if step.get("scan_stores_for"):
        result["store_hits"] = text_locations(stores, step["scan_stores_for"])
    return result


# --------------------------------------------------------------------------- evidence


def _clip(value, limit: int = 400) -> str:
    text = value if isinstance(value, str) else json.dumps(value, default=str)
    return text if len(text) <= limit else text[:limit] + " …"


def _turn_markdown(turn: dict, speaker: str = "Customer") -> list[str]:
    lines = [f"**{speaker}:** {turn['customer']}", ""]
    notes = [f"- `{call['name']}({_clip(call['args'], 200)})` → `{_clip(call['result'])}`" for call in turn["tool_calls"]]
    if turn.get("error"):
        notes.append(f"- **error:** `{turn['error']}`")
    lines += notes + ([""] if notes else []) + [f"**Assistant:** {turn['reply'] or '(no reply)'}", ""]
    return lines


def step_markdown(step: dict, result: dict, checks: list[dict]) -> list[str]:
    title = f"## {step['id']}  ·  {step['kind']}" + (f"  ·  {step['user']}" if step.get("user") else "") + (f"  ·  {step['at']}" if step.get("at") else "")
    lines = [title, ""]
    if step.get("session") and step["session"] != step["id"]:
        lines += [f"_Resumes session `{step['session']}`._", ""]
    if step.get("persona"):
        lines += [f"_Simulated customer (unscripted). Persona:_ {step['persona']}", ""]
    if result.get("error"):
        lines += [f"**Step failed:** `{_clip(result['error'], 600)}`", ""]
    if step.get("disabled_tools"):
        lines += [f"_Tools removed for this session: {', '.join(step['disabled_tools'])}_", ""]
    for turn in result.get("turns", []):
        lines += _turn_markdown(turn)
    if "cli_exit_code" in result:
        lines += [f"_CLI exit code {result['cli_exit_code']}; stdout tail:_", "", "```", result["cli_stdout_tail"].strip(), "```", ""]
        if result.get("cli_stderr_tail", "").strip():
            lines += ["_stderr tail:_", "", "```", result["cli_stderr_tail"].strip()[-600:], "```", ""]
    for session in result.get("followup_sessions", []):
        lines += [f"### follow-up session `{session['session_id']}`", ""] + _turn_markdown(session["turn"], "Scheduler")
        if session.get("episode"):
            lines += [f"_Episode written:_ {session['episode']['text']}", ""]
    if result.get("episode"):
        lines += [f"_Episode written:_ {result['episode']['text']}", ""]
    for key in ("outcomes", "resolved", "approved", "maintenance", "affected"):
        if key in result:
            lines += [f"_{key}:_ `{_clip(result[key], 600)}`", ""]
    if result.get("promoted"):
        promoted = result["promoted"]
        lines += [f"_Model draft:_ {promoted['rule_text']}", "",
                  f"_Approving the draft verbatim with these approvals would have been refused:_ {promoted['draft_problems_with_these_approvals'] or 'no'}", "",
                  f"_Reviewer-approved rule, promoted to {promoted['version']}:_ {promoted['approved_text']}", "",
                  f"_Evidence (registry only, never in the prompt):_ episodes {promoted['episodes']} from customers {promoted['users']}, "
                  f"decisions {promoted['decisions']}", ""]
    if "registry" in result:
        lines += [f"_Registry history:_ `{_clip(result['registry']['history'], 800)}`", ""]
    for judge_id, verdict in result.get("judgements", {}).items():
        lines += [f"_Judge `{judge_id}`: **{verdict['verdict']}**, {verdict['reason']}_", ""]
    if checks:
        lines += ["| | memory type | check | evidence |", "|---|---|---|---|"]
        for c in checks:
            evidence = _clip(c["evidence"], 220).replace("|", "\\|").replace("\n", " ")
            lines.append(f"| {'PASS' if c['passed'] else '**FAIL**'} | {c['type']} | {c['label']} | `{evidence}` |")
        lines.append("")
    return lines


def _step_checks(step: dict) -> list[dict]:
    return step["checks"] + [check(j["type"], f"judge: {j['question']}", "judged", id=j["id"]) for j in step.get("judges", [])]


async def run_group(framework: str, suite: str, group: str, run: int, var_dir: Path, out_dir: Path) -> list[dict]:
    fw = importlib.import_module(FRAMEWORK_MODULES[framework])
    shutil.rmtree(var_dir, ignore_errors=True)
    h = await resolved(fw.open_harness(var_dir))
    out_dir.mkdir(parents=True, exist_ok=True)
    recorded = []
    for step in SUITES[suite][group]:
        print(f"[{framework} {suite} run {run} {group}] {step['id']}", flush=True)
        try:
            result = await run_step(framework, fw, h, step)
        except Exception as exc:  # e.g. a transport error from the model API: record it, keep the rest of the run
            result = {"error": f"{type(exc).__name__}: {exc}", "traceback": traceback.format_exc(limit=4)}
        snapshot = await resolved(fw.snapshot(h, USERS))
        recorded.append({"step": step["id"], "result": result, "snapshot": snapshot})
        if result.get("procedure_text"):
            (out_dir / f"procedure-{result['promoted']['version']}.md").write_text(result["procedure_text"])
    (out_dir / "meta.json").write_text(json.dumps({"framework": framework, "suite": suite, "group": group, "run": run}))
    (out_dir / "steps.json").write_text(json.dumps(recorded, indent=1, default=str))
    (out_dir / "final-stores.json").write_text(json.dumps(recorded[-1]["snapshot"], indent=2, default=str))
    results = score_group(out_dir)
    print(f"[{framework} {suite} run {run} {group}] {sum(c['passed'] for c in results)}/{len(results)} checks passed -> {out_dir}")
    return results


def score_group(out_dir: Path) -> list[dict]:
    """Evaluate every check against a group's recorded steps; (re)write its transcript and results."""
    meta = json.loads((out_dir / "meta.json").read_text())
    recorded = {entry["step"]: entry for entry in json.loads((out_dir / "steps.json").read_text())}
    title = meta["framework"] + " · " + meta["suite"] + f" · run {meta['run']}" + ("" if meta["suite"] == "scripted" else f" · {meta['group']}")
    transcript = [f"# {title}", "", "Live run against DeepSeek: every customer line below went to the real agent "
                  "(simulated-customer lines were written live by the model playing the persona). Tool results are clipped.", ""]
    results = []
    for step in SUITES[meta["suite"]][meta["group"]]:
        entry = recorded[step["id"]]
        checks = []
        for spec in _step_checks(step):
            passed, evidence = evaluate(spec, entry["result"], entry["snapshot"])
            checks.append({"step": step["id"], "type": spec["type"], "label": spec["label"], "passed": passed, "evidence": evidence})
        results += checks
        transcript += step_markdown(step, entry["result"], checks)
    (out_dir / "transcript.md").write_text("\n".join(transcript))
    (out_dir / "results.json").write_text(json.dumps(results, indent=2))
    return results


def _out_dir(evidence_root: Path, suite: str, framework: str, run: int, group: str) -> Path:
    base = evidence_root / suite / framework / f"run-{run}"
    return base if suite == "scripted" else base / group


def summarize(evidence_root: Path, suite: str) -> str:
    """Pass counts per memory type per framework for one evidence suite directory, across every recorded run, plus every failure."""
    rows = {fw: [(p, json.loads(p.read_text())) for p in sorted((evidence_root / suite / fw).rglob("results.json"))]
            for fw in FRAMEWORK_MODULES}
    runs = {fw: sorted({p.relative_to(evidence_root / suite / fw).parts[0] for p, _ in rows[fw]}) for fw in rows}
    lines = [f"# Evidence summary: {suite}", "", "Pass counts per memory type, summed over every recorded live run.", "",
             "| memory type | " + " | ".join(f"{fw} ({len(runs[fw])} runs)" for fw in rows) + " |", "|---|" + "---|" * len(rows)]
    for memory_type in MEMORY_TYPES:
        cells = []
        for fw in rows:
            checks = [c for _, run in rows[fw] for c in run if c["type"] == memory_type]
            cells.append(f"{sum(c['passed'] for c in checks)}/{len(checks)}" if checks else "-")
        lines.append(f"| {memory_type} | " + " | ".join(cells) + " |")
    totals = [f"{sum(c['passed'] for _, run in rows[fw] for c in run)}/{sum(len(run) for _, run in rows[fw])}" for fw in rows]
    lines.append("| **all** | " + " | ".join(f"**{t}**" for t in totals) + " |")
    lines += ["", "## Every failed check", "", "| framework | where | step | memory type | check | evidence |", "|---|---|---|---|---|---|"]
    for fw in rows:
        for path, run in rows[fw]:
            where = str(path.parent.relative_to(evidence_root / suite / fw))
            for c in run:
                if not c["passed"]:
                    evidence = _clip(c["evidence"], 200).replace("|", "\\|").replace("\n", " ")
                    lines.append(f"| {fw} | {where} | {c['step']} | {c['type']} | {c['label']} | `{evidence}` |")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--suite", choices=list(SUITES), default="scripted")
    parser.add_argument("--framework", choices=list(FRAMEWORK_MODULES))
    parser.add_argument("--run", type=int, default=1)
    parser.add_argument("--groups", help="comma-separated group ids (adversarial suite); default: all")
    parser.add_argument("--var-root", type=Path, default=CODE_DIR / "var" / "runs")
    parser.add_argument("--evidence-root", type=Path, default=CODE_DIR / "evidence")
    parser.add_argument("--evidence-suite-name", help="write under evidence/<this> instead of evidence/<suite> (e.g. a baseline)")
    parser.add_argument("--summarize", action="store_true", help="rewrite evidence/<suite>/summary.md from recorded runs")
    parser.add_argument("--rescore", action="store_true", help="re-score every recorded run from its steps.json")
    args = parser.parse_args()
    if args.rescore:
        for meta in sorted(args.evidence_root.rglob("meta.json")):
            if json.loads(meta.read_text()).get("frozen"):
                continue  # a baseline stays scored by the suite as it was when it ran
            results = score_group(meta.parent)
            print(f"{meta.parent}: {sum(c['passed'] for c in results)}/{len(results)}")
        return
    if args.summarize:
        for suite_dir in sorted(p for p in args.evidence_root.iterdir() if p.is_dir() and any(p.rglob("meta.json"))):
            (suite_dir / "summary.md").write_text(summarize(args.evidence_root, suite_dir.name))
        return
    if not args.framework:
        parser.error("--framework is required unless --summarize or --rescore")
    groups = args.groups.split(",") if args.groups else list(SUITES[args.suite])
    evidence_suite = args.evidence_suite_name or args.suite
    for group in groups:
        var_dir = args.var_root / evidence_suite / args.framework / f"run-{args.run}" / group
        asyncio.run(run_group(args.framework, args.suite, group, args.run, var_dir,
                              _out_dir(args.evidence_root, evidence_suite, args.framework, args.run, group)))


if __name__ == "__main__":
    main()
