"""The reviewer's desk: promote or retract procedural rules, and approve or reject held follow-up messages.

    python review.py candidates      --framework adk --var-dir var/adk/interactive          # evidence + a model draft
    python review.py promote         --framework adk --var-dir ... --code NO_CANCELLATION_PROOF \\
                                     --text "the rule as you edited it" --by "Jane Doe" --role ops_lead
    python review.py retract         --framework adk --var-dir ... --to v1 --by "Jane Doe" --reason "..."
    python review.py held-messages   --var-dir ...
    python review.py approve-message --var-dir ... --followup F-1234abcd --by "Jane Doe"
    python review.py reject-message  --var-dir ... --followup F-1234abcd --by "Jane Doe" --note "too blunt"

The same functions the scripted scenario calls (cardcare/procedures.py, cardcare/scheduler.py), behind a
command line, so promotion and approval are a product path rather than a test-driver call. A rule whose text
would refuse a customer is rejected unless one of the approvers has the role disputes_policy_owner.
"""

import argparse
import asyncio
import importlib
import inspect
import json
from pathlib import Path

from cardcare import procedures, scheduler, world
from cardcare.clock import wall_clock_now

FRAMEWORK_MODULES = {"adk": "adk_agent.agent", "langgraph": "langgraph_agent.agent"}
USERS = [customer[0] for customer in world.CUSTOMERS]


async def _resolved(value):
    return await value if inspect.isawaitable(value) else value


async def _episodes(framework: str, var_dir: Path) -> tuple[object, list[dict]]:
    fw = importlib.import_module(FRAMEWORK_MODULES[framework])
    h = await _resolved(fw.open_harness(var_dir))
    return fw, (await _resolved(fw.snapshot(h, USERS)))["episodes"]


async def main_async(args) -> dict:
    now = args.now or wall_clock_now()
    if args.command == "candidates":
        fw, episodes = await _episodes(args.framework, args.var_dir)
        candidates = procedures.promotion_candidates(episodes, procedures.load_registry(args.var_dir))
        for candidate in candidates:
            candidate["model_draft"] = (await _resolved(fw.complete_text(procedures.rule_drafting_prompt(candidate)))).strip()
            candidate["draft_problems_for_ops_lead"] = procedures.rule_review_problems(candidate["model_draft"], [{"role": "ops_lead"}])
        return {"candidates": candidates}
    if args.command == "promote":
        _, episodes = await _episodes(args.framework, args.var_dir)
        candidate = next(c for c in procedures.promotion_candidates(episodes, procedures.load_registry(args.var_dir))
                         if c["resolution_code"] == args.code)
        approvals = [{"name": args.by, "role": args.role}]
        return {"version": procedures.promote(args.var_dir, candidate, args.draft or "", args.text, approvals, now)}
    if args.command == "retract":
        retracted = procedures.load_registry(args.var_dir)["active"]
        _, episodes = await _episodes(args.framework, args.var_dir)
        procedures.retract(args.var_dir, args.to, args.by, args.reason, now)
        return {"active": args.to, "review_these_conversations": procedures.conversations_under_version(episodes, retracted)}
    bank_db, scheduler_db = args.var_dir / "bank.db", args.var_dir / "scheduler.db"
    if args.command == "held-messages":
        return {"held": [m for m in world.outbound_messages(bank_db) if m["status"] == "held"]}
    if args.command == "approve-message":
        return {"followup": scheduler.approve_followup(scheduler_db, bank_db, args.followup, args.by, now)}
    return {"followup": scheduler.reject_followup(scheduler_db, bank_db, args.followup, args.by, args.note or "", now)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("command", choices=["candidates", "promote", "retract", "held-messages", "approve-message", "reject-message"])
    parser.add_argument("--framework", choices=list(FRAMEWORK_MODULES), default="adk")
    parser.add_argument("--var-dir", type=Path, required=True)
    parser.add_argument("--code", help="promote: the resolution code of the candidate")
    parser.add_argument("--text", help="promote: the rule text as the reviewer edited it")
    parser.add_argument("--draft", help="promote: the model draft it was edited from, for the audit record")
    parser.add_argument("--to", help="retract: the version to make active again")
    parser.add_argument("--followup", help="approve-message / reject-message: the follow-up id")
    parser.add_argument("--by", help="the reviewer's name")
    parser.add_argument("--role", default="ops_lead", help="promote: the reviewer's role (disputes_policy_owner for refusal rules)")
    parser.add_argument("--reason", help="retract: why")
    parser.add_argument("--note", help="reject-message: what to change")
    parser.add_argument("--now", help="override the clock (ISO-8601)")
    print(json.dumps(asyncio.run(main_async(parser.parse_args())), indent=2, default=str))


if __name__ == "__main__":
    main()
