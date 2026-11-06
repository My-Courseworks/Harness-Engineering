"""Drive the shared scenario through the real ADK or LangGraph agent and write the evidence.

    python run_scenario.py --framework adk --run 1
    python run_scenario.py --framework langgraph --run 1
    python run_scenario.py --summarize

Every session step is a live conversation against DeepSeek. Each run starts from
empty stores under --var-root/<framework>/run-<n> and writes, under
evidence/<framework>/run-<n>/, a transcript, the per-check results, and the
final contents of every store. No store file is ever written into evidence/.
"""

import argparse
import asyncio
import importlib
import inspect
import json
import shutil
import traceback
from pathlib import Path

from cardcare import procedures, scheduler, world
from cardcare.clock import add_minutes
from cardcare.scenario import MEMORY_TYPES, SCENARIO, evaluate, pan_locations

CODE_DIR = Path(__file__).resolve().parent
USERS = [customer[0] for customer in world.CUSTOMERS]
FRAMEWORK_MODULES = {"adk": "adk_agent.agent", "langgraph": "langgraph_agent.agent"}


async def resolved(value):
    """The ADK harness is async and the LangGraph one is sync; the runner awaits whichever it gets."""
    return await value if inspect.isawaitable(value) else value


async def run_session(fw, h, step: dict) -> dict:
    turns = []
    for index, text in enumerate(step["turns"]):
        now = add_minutes(step["at"], index * 2)
        try:
            turns.append(await resolved(fw.run_turn(h, step["user"], step["id"], text, now, tuple(step.get("disabled_tools", ())))))
        except Exception as exc:  # a failed turn is evidence, not a reason to stop the run
            turns.append({"customer": text, "tool_calls": [], "reply": "", "error": f"{type(exc).__name__}: {exc}",
                          "traceback": traceback.format_exc(limit=3)})
    episode = await resolved(fw.end_session(h, step["user"], step["id"], add_minutes(step["at"], len(turns) * 2)))
    stores = [path for path in h.var_dir.rglob("*") if path.is_file()]
    return {"turns": turns, "episode": episode, "pan_found_in": pan_locations(stores)}


async def run_followups(fw, h, step: dict) -> dict:
    sessions = []

    async def resume(record: dict, now: str):
        sessions.append(await resolved(fw.run_followup_session(h, record, now)))

    outcomes = await scheduler.fire_due_followups(h.scheduler_db, h.bank_db, step["at"], resume)
    return {"outcomes": outcomes, "followup_sessions": sessions}


async def run_promotion(fw, h, step: dict) -> dict:
    snapshot = await resolved(fw.snapshot(h, USERS))
    candidates = procedures.promotion_candidates(snapshot["episodes"], procedures.load_registry(h.var_dir))
    if not candidates:
        return {"promoted": None, "candidates": []}
    candidate = candidates[0]
    rule_text = await resolved(fw.complete_text(procedures.rule_drafting_prompt(candidate)))
    version = procedures.promote(h.var_dir, candidate, rule_text, step["reviewer"], step["at"])
    return {"promoted": {**candidate, "rule_text": rule_text.strip(), "version": version}, "candidates": candidates,
            "procedure_text": procedures.procedure_text(h.var_dir, version)}


async def run_step(fw, h, step: dict) -> dict:
    kind = step["kind"]
    if kind == "session":
        return await run_session(fw, h, step)
    if kind == "fire_followups":
        return await run_followups(fw, h, step)
    if kind == "resolve_cases":
        return {"resolved": world.resolve_open_cases(h.bank_db, step["reason"], step["status"], step["code"], step["note"], step["at"])}
    if kind == "approve_followups":
        parked = [f for f in scheduler.list_followups(h.scheduler_db) if f["user_id"] == step["user"] and f["status"] == "awaiting_approval"]
        return {"approved": [scheduler.approve_followup(h.scheduler_db, f["followup_id"], step["reviewer"]) for f in parked]}
    if kind == "promote":
        return await run_promotion(fw, h, step)
    if kind == "retract":
        return {"registry": procedures.retract(h.var_dir, step["to"], step["reviewer"], step["reason"], step["at"])}
    if kind == "retention_sweep":
        return {"purged": await resolved(fw.purge_expired_episodes(h, step["at"]))}
    raise ValueError(f"unknown step kind {kind}")


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
    if step.get("disabled_tools"):
        lines += [f"_Tools removed for this session: {', '.join(step['disabled_tools'])}_", ""]
    for turn in result.get("turns", []):
        lines += _turn_markdown(turn)
    for session in result.get("followup_sessions", []):
        lines += [f"### follow-up session `{session['session_id']}`", ""] + _turn_markdown(session["turn"], "Scheduler")
        lines += [f"_Episode written:_ {session['episode']['text']}", ""]
    if result.get("episode"):
        lines += [f"_Episode written:_ {result['episode']['text']}", ""]
    for key in ("outcomes", "resolved", "approved", "purged"):
        if key in result:
            lines += [f"_{key}:_ `{_clip(result[key], 600)}`", ""]
    if result.get("promoted"):
        promoted = result["promoted"]
        lines += [f"_Promoted to {promoted['version']}:_ {promoted['rule_text']}", "",
                  f"_Evidence:_ episodes {promoted['episodes']} from customers {promoted['users']}", ""]
    if "registry" in result:
        lines += [f"_Registry history:_ `{_clip(result['registry']['history'], 800)}`", ""]
    if checks:
        lines += ["| | memory type | check | evidence |", "|---|---|---|---|"]
        for c in checks:
            evidence = _clip(c["evidence"], 220).replace("|", "\\|").replace("\n", " ")
            lines.append(f"| {'PASS' if c['passed'] else '**FAIL**'} | {c['type']} | {c['label']} | `{evidence}` |")
        lines.append("")
    return lines


async def run_scenario(framework: str, run: int, var_root: Path, evidence_root: Path) -> list[dict]:
    fw = importlib.import_module(FRAMEWORK_MODULES[framework])
    var_dir = var_root / framework / f"run-{run}"
    shutil.rmtree(var_dir, ignore_errors=True)
    h = await resolved(fw.open_harness(var_dir))
    out_dir = evidence_root / framework / f"run-{run}"
    out_dir.mkdir(parents=True, exist_ok=True)
    transcript = [f"# {framework} · run {run}", "",
                  "Live run of the shared scenario against DeepSeek. Every customer turn below was sent to the real agent; "
                  "tool results are clipped for length.", ""]
    results = []
    for step in SCENARIO:
        print(f"[{framework} run {run}] {step['id']}", flush=True)
        result = await run_step(fw, h, step)
        snapshot = await resolved(fw.snapshot(h, USERS))
        checks = []
        for spec in step["checks"]:
            passed, evidence = evaluate(spec, result, snapshot)
            checks.append({"step": step["id"], "type": spec["type"], "label": spec["label"], "passed": passed, "evidence": evidence})
        results += checks
        transcript += step_markdown(step, result, checks)
        if result.get("procedure_text"):
            (out_dir / f"procedure-{result['promoted']['version']}.md").write_text(result["procedure_text"])
    final = await resolved(fw.snapshot(h, USERS))
    (out_dir / "transcript.md").write_text("\n".join(transcript))
    (out_dir / "results.json").write_text(json.dumps(results, indent=2))
    (out_dir / "final-stores.json").write_text(json.dumps(final, indent=2, default=str))
    passed = sum(c["passed"] for c in results)
    print(f"[{framework} run {run}] {passed}/{len(results)} checks passed -> {out_dir}")
    return results


def summarize(evidence_root: Path) -> str:
    """One table of pass counts per memory type per framework, across every recorded run, plus every failure."""
    runs = {fw: sorted((evidence_root / fw).glob("run-*/results.json")) for fw in FRAMEWORK_MODULES}
    lines = ["# Evidence summary", "", "Pass counts per memory type, summed over every recorded live run.", "",
             "| memory type | " + " | ".join(f"{fw} ({len(paths)} runs)" for fw, paths in runs.items()) + " |",
             "|---|" + "---|" * len(runs)]
    loaded = {fw: [json.loads(p.read_text()) for p in paths] for fw, paths in runs.items()}
    for memory_type in MEMORY_TYPES:
        cells = []
        for fw in runs:
            checks = [c for run in loaded[fw] for c in run if c["type"] == memory_type]
            cells.append(f"{sum(c['passed'] for c in checks)}/{len(checks)}" if checks else "-")
        lines.append(f"| {memory_type} | " + " | ".join(cells) + " |")
    lines += ["", "## Every failed check", "", "| framework | run | step | memory type | check | evidence |", "|---|---|---|---|---|---|"]
    for fw, paths in runs.items():
        for path, run in zip(paths, loaded[fw]):
            for c in run:
                if not c["passed"]:
                    evidence = _clip(c["evidence"], 200).replace("|", "\\|").replace("\n", " ")
                    lines.append(f"| {fw} | {path.parent.name} | {c['step']} | {c['type']} | {c['label']} | `{evidence}` |")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--framework", choices=list(FRAMEWORK_MODULES))
    parser.add_argument("--run", type=int, default=1)
    parser.add_argument("--var-root", type=Path, default=CODE_DIR / "var" / "scenario")
    parser.add_argument("--evidence-root", type=Path, default=CODE_DIR / "evidence")
    parser.add_argument("--summarize", action="store_true", help="rewrite evidence/summary.md from recorded runs")
    args = parser.parse_args()
    if args.summarize:
        (args.evidence_root / "summary.md").write_text(summarize(args.evidence_root))
        return
    if not args.framework:
        parser.error("--framework is required unless --summarize")
    asyncio.run(run_scenario(args.framework, args.run, args.var_root, args.evidence_root))


if __name__ == "__main__":
    main()
