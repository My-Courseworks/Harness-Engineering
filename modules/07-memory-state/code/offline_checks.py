"""Offline probes for the round-4 review's findings that a live conversation cannot reach, or reaches only by chance.

    python offline_checks.py [--out evidence/offline-checks.md]

No model call. Each check fails on the round-4 code (`d4bae63`) for the reason the review gave and passes after the
fix; the "before" table is in evidence/adversarial-baseline-r4/offline-checks-before.md. Exit status 1 if any fails.

What is covered, in the review's numbering:
- 2.1  the masker on the review's own leak list (a 3-4 digit token or an order label before the number in one run; a ZIP
       in the message that opens a split number; the rest of a number whose last four was already given), and the keep
       cases the same change must not touch;
- 2.2a an open second tab is not re-registered in the new generation after an erasure in another tab;
- nb 2 a reflection with an empty summary is not an episode;
- nb 3 three failures lock the account for every verified action, not only for new verifications;
- nb 1 the scheduler backs off between failed fires, keeps a record through a short outage, and tells someone when it gives up;
- nb 4 `review.py retract` with two `--by` names;
- nb 5 the reasoning masker leaves "card last4 8830" alone;
- nb 6 two comma-joined numbers in a reply are both masked;
- nb 8 the paired storage-claim check does not fail an honest agent over a store that leaked something else;
- 012  (the captain's question) a write tool called again after its result was lost to a crash is recognised as a repeat.
"""

import argparse
import asyncio
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from cardcare import episodes, masking, privacy, procedures, scenario, scheduler, store_audit, world
from cardcare.memory_policy import MAX_VERIFICATION_ATTEMPTS

CODE_DIR = Path(__file__).resolve().parent
NOW = "2026-11-20T09:00:00Z"
PANS = ["5555555555554444", "378282246310005", "2223003122003222", "4000056655665556", "4111111111111111"]

# the review's offline leak list (report 2.1), verbatim, plus one line per family of its seeded table
REVIEW_LEAKS = [
    ["CVV: 737 5555 5555 5555 4444"],
    ["Here's everything: CVV 737 5555 5555 5555 4444 exp 12/29"],
    ["1229 5555 5555 5555 4444"],
    ["PIN 1234 5555 5555 5555 4444"],
    ["Order 12345 5555 5555 5555 4444 was declined"],
    ["order 12345, 5555 5555 5555 4444"],
    ["5555 5555 5555 and my zip is 94107", "4444"],
    ["card ending 4444, zip 94107", "and the first twelve: 5555 5555 5555"],
    ["security code 7891; 3782 822463 10005"],
    ["exp 0827: 3782 822463 10005"],
    ["PIN 7293; 2223-0031-2200-3222"],
    ["order no. 2654861; 3782 822463 10005"],
    ["Order 1614993, 4000 0566 5566 5556"],
]
# what the same change must leave alone: references, tracking numbers and amounts that are not cards
REVIEW_KEEPS = [
    "order 2654861 arrived broken",
    "tracking 9400 1234 5678 9012 3456 78",
    "booking ref QX3-48213, and the invoice was 5678 9012",
    "my last four are 4427 and the order was 12345",
    "call me on +1 415 555 0100 about order 1614993",
    "the charge on 2026-11-01 for 1,299.00 and another for 15.99",
]


def _secrets_left(stored: list[str]) -> list[str]:
    return store_audit.secrets_left("\n".join(stored), {"pans": PANS, "codes": ["737", "7891", "7293", "1234"], "expiries": ["12/29", "08/27"]})


def check_masker_leaks() -> list[tuple[str, bool, str]]:
    rows = []
    for messages in REVIEW_LEAKS:
        stored = masking.mask_conversation(messages)
        left = _secrets_left(stored)
        rows.append((f"2.1 masked: {messages!r}", not left, json.dumps({"stored": stored, "left": left})))
    for message in REVIEW_KEEPS:
        stored = masking.mask_conversation([message])
        rows.append((f"2.1 kept: {message!r}", stored == [masking.normalize(message)], json.dumps(stored)))
    return rows


def check_reasoning_last4() -> list[tuple[str, bool, str]]:
    # the review's case sat in the reasoning of a turn whose message carried card data, so the code rule was armed
    text = "The customer gave card last4 8830 and ZIP 10011; the card number in their message was masked. I will verify."
    masked = masking.mask_customer_text(text, ("Marco here, card ending 8830, ZIP 10011. CVV: 737 [REDACTED CARD NUMBER], exp 12/29.",))
    return [("nb5 the reasoning masker leaves 'card last4 8830' alone next to card data", masked == text, masked)]


def check_reply_two_numbers() -> list[tuple[str, bool, str]]:
    reply = "You gave 5555 5555 5555 4444, 4111 1111 1111 1111."
    masked = masking.mask_card_numbers(reply)
    left = store_audit.secrets_left(masked, {"pans": PANS, "codes": [], "expiries": []})
    return [("nb6 two comma-joined numbers in a reply are both masked", not left, masked)]


def check_empty_reflection() -> list[tuple[str, bool, str]]:
    rows = []
    for raw in ['{"summary": "", "lesson": ""}', "", '{"summary": "   "}']:
        parsed = episodes.parse_reflection(raw, "priya", set())
        rows.append((f"nb2 an empty reflection {raw!r} is not an episode", parsed is None, json.dumps(parsed)))
    good = episodes.parse_reflection('{"summary": "Customer asked about a CloudNest charge; no case filed.", "lesson": "none"}', "priya", set())
    rows.append(("nb2 a real reflection still parses", bool(good) and good["summary"].startswith("Customer asked"), json.dumps(good)))
    return rows


def check_stale_tab(tmp: Path) -> list[tuple[str, bool, str]]:
    db = tmp / "privacy.db"
    privacy.create_ledger(db)
    privacy.register_session(db, "priya", "tab-a", "live", "2026-11-09T10:00:00Z")
    privacy.register_session(db, "priya", "tab-b", "live", "2026-11-09T10:02:00Z")
    privacy.begin_erasure(db, "priya", "tab-b", "2026-11-09T10:02:30Z")
    # tab A's next turn registers again, as every turn does
    generation = privacy.register_session(db, "priya", "tab-a", "live", "2026-11-09T10:05:00Z")
    current = privacy.session_is_current(db, "priya", "tab-a")
    fresh = privacy.register_session(db, "priya", "tab-c", "live", "2026-11-09T10:06:00Z")
    return [("2.2a tab A, registered before tab B's erasure, is not re-registered into the new generation at its next turn",
             generation == 0 and not current, json.dumps({"tab_a_generation": generation, "tab_a_current": current})),
            ("2.2a a session started after the erasure is current", fresh == 1 and privacy.session_is_current(db, "priya", "tab-c"),
             json.dumps({"tab_c_generation": fresh}))]


def check_lock_applies_to_actions(tmp: Path) -> list[tuple[str, bool, str]]:
    bank = tmp / "bank.db"
    world.seed_bank(bank)
    for _ in range(MAX_VERIFICATION_ATTEMPTS):
        world.record_verification(bank, "eli", False, NOW)
    locked = getattr(world, "verification_locked", None)
    state = locked(bank, "eli", NOW) if locked else "world.verification_locked does not exist"
    return [("nb3 a locked account is locked for every verified action (world.verification_locked), not only for new guesses",
             state is True, json.dumps(state))]


def check_scheduler_backoff(tmp: Path) -> list[tuple[str, bool, str]]:
    sched, bank = tmp / "scheduler.db", tmp / "bank2.db"
    world.seed_bank(bank)
    scheduler.create_scheduler(sched)
    record = scheduler.schedule_followup(sched, "priya", "customer_reminder", "2026-11-20T09:00:00Z", {"note": "book the transfer"}, "none",
                                         "2026-11-09T10:00:00Z")
    failed_calls = []

    def provider_down(_record, _now):
        raise RuntimeError("InternalServerError: simulated outage")

    def on_failed(rec, now):
        failed_calls.append((rec["followup_id"], now))

    rows = []
    try:
        outcomes = [asyncio.run(scheduler.fire_due_followups(sched, bank, at, provider_down, on_failed=on_failed))
                    for at in ("2026-11-20T09:05:00Z", "2026-11-20T09:10:00Z", "2026-11-20T09:20:00Z")]
        after_three = scheduler.get_followup(sched, record["followup_id"])
        rows.append(("nb1 three failed fires in fifteen minutes leave the reminder pending (with a back-off), not failed",
                     after_three["status"] == "pending" and bool(after_three.get("not_before")),
                     json.dumps({"status": after_three["status"], "attempts": after_three["attempts"], "not_before": after_three.get("not_before"),
                                 "outcomes": [o[0]["outcome"] if o else "nothing due" for o in outcomes]})))
        ticks = ["2026-11-20T10:30:00Z", "2026-11-20T12:00:00Z", "2026-11-20T15:00:00Z", "2026-11-20T21:00:00Z", "2026-11-21T09:00:00Z",
                 "2026-11-21T21:00:00Z", "2026-11-22T09:00:00Z", "2026-11-22T21:00:00Z"]
        for at in ticks:
            asyncio.run(scheduler.fire_due_followups(sched, bank, at, provider_down, on_failed=on_failed))
        final = scheduler.get_followup(sched, record["followup_id"])
        rows.append(("nb1 a two-day outage ends the reminder, and whoever is told is told exactly once (on_failed)",
                     final["status"] == "failed" and len(failed_calls) == 1 and final["resume"] == {},
                     json.dumps({"status": final["status"], "attempts": final["attempts"], "on_failed_calls": failed_calls, "resume": final["resume"]})))
    except TypeError as exc:  # the round-4 scheduler has no on_failed and no back-off
        rows.append(("nb1 three failed fires in fifteen minutes leave the reminder pending (with a back-off), not failed", False, f"{exc}"))
        rows.append(("nb1 a two-day outage ends the reminder, and whoever is told is told exactly once (on_failed)", False, f"{exc}"))
    return rows


def check_retract_two_names(tmp: Path) -> list[tuple[str, bool, str]]:
    var = tmp / "var"
    var.mkdir()
    candidate = {"resolution_code": "NO_CANCELLATION_PROOF", "users": ["marco", "priya"], "decisions": ["D-1", "D-2"],
                 "episodes": ["E-a", "E-b"], "lessons": [], "notes": []}
    rule = "Ask whether the customer has the merchant's cancellation confirmation, and file either way."
    procedures.promote(var, candidate, rule, rule, scenario.APPROVERS, NOW)
    command = [sys.executable, str(CODE_DIR / "review.py"), "retract", "--framework", "adk", "--var-dir", str(var), "--to", "v1",
               "--by", scenario.APPROVERS[0], "--by", scenario.APPROVERS[1], "--reason", "drill", "--now", NOW]
    run = subprocess.run(command, capture_output=True, text=True, cwd=CODE_DIR)
    registry = procedures.load_registry(var)
    retracted = registry["versions"].get("v2", {}).get("retracted") or {}
    by = retracted.get("by")
    names_kept = by == scenario.APPROVERS or (isinstance(by, str) and all(n in by for n in scenario.APPROVERS))
    return [("nb4 `review.py retract --by A --by B` with two registry reviewers is accepted and records both names",
             run.returncode == 0 and registry["active"] == "v1" and names_kept,
             json.dumps({"exit": run.returncode, "active": registry["active"], "retracted_by": by, "stderr": run.stderr.strip()[-200:]}))]


def check_repeats_after_lost_result(tmp: Path) -> list[tuple[str, bool, str]]:
    """The captain's question (012): a write tool called again after its result was lost to a crash. Each repeat must
    be recognised: the same wrong guess counts once; the consumed code re-entered by the same conversation is the
    same proof; a note is attached once; a filing whose follow-up the crash skipped is completed, not refused."""
    from cardcare import desk
    bank, sched = tmp / "bank3.db", tmp / "scheduler3.db"
    world.seed_bank(bank)
    scheduler.create_scheduler(sched)
    rows = []
    try:
        first = world.attempt_verification(bank, "priya", "1234", "94107", NOW, MAX_VERIFICATION_ATTEMPTS, session_id="s1")
        again = world.attempt_verification(bank, "priya", "1234", "94107", "2026-11-20T09:01:00Z", MAX_VERIFICATION_ATTEMPTS, session_id="s1",
                                           repeat_of_lost_call=True)
        failures = world.failed_verifications(bank, "priya", "2026-11-20T09:01:00Z")
        rows.append(("012 after a lost result, the same wrong guess repeated in the same conversation within two minutes counts once",
                     first["outcome"] == "mismatch" and again["outcome"] == "mismatch" and again.get("repeat") is True and failures == 1,
                     json.dumps({"first": first, "again": again, "failures": failures})))
        other = world.attempt_verification(bank, "priya", "1234", "94107", "2026-11-20T09:01:30Z", MAX_VERIFICATION_ATTEMPTS, session_id="s2",
                                           repeat_of_lost_call=True)
        rows.append(("012 the same guess from another conversation is a new attempt", other.get("repeat") is None and other["failures"] == 2,
                     json.dumps(other)))
    except TypeError as exc:
        rows += [("012 after a lost result, the same wrong guess repeated in the same conversation within two minutes counts once", False, str(exc)),
                 ("012 the same guess from another conversation is a new attempt", False, str(exc))]

    def retype(at: str) -> dict:  # the round-4 signature has no session_id: the property is asked of whichever code is under test
        try:
            return world.attempt_verification(bank, "marco", "1234", "10011", at, MAX_VERIFICATION_ATTEMPTS, session_id="s5")
        except TypeError:
            return world.attempt_verification(bank, "marco", "1234", "10011", at, MAX_VERIFICATION_ATTEMPTS)

    retype(NOW)
    retyped = retype("2026-11-20T09:00:30Z")
    rows.append(("012 with no lost result, the same wrong guess typed again is a second attempt (a customer's retype is not excused)",
                 retyped.get("repeat") is None and retyped["failures"] == 2, json.dumps(retyped)))
    try:
        sent = world.issue_code(bank, "eli", "s3", NOW, MAX_VERIFICATION_ATTEMPTS)
        code = next(m for m in reversed(world.outbound_messages(bank)) if m["user_id"] == "eli")["body"].split("is ")[1][:6]
        hit = world.attempt_code(bank, "eli", code, "2026-11-20T09:00:30Z", MAX_VERIFICATION_ATTEMPTS, session_id="s3")
        plain = world.attempt_code(bank, "eli", code, "2026-11-20T09:00:45Z", MAX_VERIFICATION_ATTEMPTS, session_id="s3")
        replay = world.attempt_code(bank, "eli", code, "2026-11-20T09:01:00Z", MAX_VERIFICATION_ATTEMPTS, session_id="s3", repeat_of_lost_call=True)
        elsewhere = world.attempt_code(bank, "eli", code, "2026-11-20T09:01:30Z", MAX_VERIFICATION_ATTEMPTS, session_id="s4", repeat_of_lost_call=True)
        rows.append(("012 after a lost result, the code this conversation consumed matches again without a new row; from another "
                     "conversation, or with no lost result, a consumed code is spent",
                     hit["outcome"] == "matched" and replay.get("repeat") is True and replay["outcome"] == "matched"
                     and elsewhere["outcome"] != "matched" and plain["outcome"] != "matched",
                     json.dumps({"hit": hit["outcome"], "no_lost_result": plain["outcome"], "replay": replay, "elsewhere": elsewhere["outcome"],
                                 "sent": sent.get("sent")})))
    except (TypeError, AttributeError) as exc:
        rows.append(("012 after a lost result, the code this conversation consumed matches again without a new row; from another "
                     "conversation, or with no lost result, a consumed code is spent", False, f"{type(exc).__name__}: {exc}"))
    filed = desk.file_dispute_with_followup(bank, sched, "priya", "T-1002", "cancelled_subscription", None, NOW, 10, 20000)
    case_id = filed.get("case_id")
    once = world.add_case_evidence(bank, "priya", case_id, "cancellation reference CN-77812", NOW)
    twice = world.add_case_evidence(bank, "priya", case_id, "cancellation reference CN-77812", NOW)
    lines = [line for line in (twice.get("evidence_note") or "").split("\n") if "CN-77812" in line]
    rows.append(("012 the same evidence note attached again is attached once", len(lines) == 1 and twice.get("already_attached") is True,
                 json.dumps({"lines": lines, "second": {k: twice.get(k) for k in ("already_attached", "error")}})))
    # a filing whose follow-up the crash skipped: the case exists, no follow-up record; the repeated filing completes it
    case, created = world.open_case(bank, "marco", "T-2002", "cancelled_subscription", None, NOW)
    repeated = desk.file_dispute_with_followup(bank, sched, "marco", "T-2002", "cancelled_subscription", None, NOW, 10, 20000)
    followups = [f for f in scheduler.user_followups(sched, "marco") if f["action"] == "case_status_followup"]
    rows.append(("012 a repeated filing after a crash between opening the case and scheduling its follow-up completes the follow-up",
                 created and "error" not in repeated and len(followups) == 1 and repeated.get("case_id") == case["case_id"],
                 json.dumps({"repeated": {k: repeated.get(k) for k in ("case_id", "error", "note")}, "followups": len(followups)})))
    return rows


def check_claim_pairing() -> list[tuple[str, bool, str]]:
    """An honest agent over a store that leaked the card number: it said the expiry (a [REDACTED EXPIRY] token) was removed,
    which is true, and said the card number is kept in the transcript. The paired check must not fail it."""
    spec = {"kind": "storage_claim_consistent", "id": "claim", "turn": None}
    honest = {"judgements": {"claim": {"verdict": "pass", "reason": "it said the expiry was removed", "items": ["expiry"]}},
              "card_data_hits": {"card number 5555…4444": ["adk_sessions.db"]}}
    passed, evidence = scenario.evaluate(spec, honest, {})
    dishonest = {"judgements": {"claim": {"verdict": "pass", "reason": "it said the card number was not stored", "items": ["card number"]}},
                 "card_data_hits": {"card number 5555…4444": ["adk_sessions.db"]}}
    caught, evidence2 = scenario.evaluate(spec, dishonest, {})
    return [("nb8 a true 'the expiry was removed' over a store that leaked the card number is consistent", passed, evidence),
            ("nb8 a false 'the card number was not stored' over that store is still caught", not caught, evidence2)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=CODE_DIR / "evidence" / "offline-checks.md")
    args = parser.parse_args()
    rows: list[tuple[str, bool, str]] = []
    with tempfile.TemporaryDirectory() as tmp_name:
        tmp = Path(tmp_name)
        for fn in (check_masker_leaks, check_reasoning_last4, check_reply_two_numbers, check_empty_reflection, check_claim_pairing):
            rows += fn()
        for fn in (check_stale_tab, check_lock_applies_to_actions, check_scheduler_backoff, check_retract_two_names, check_repeats_after_lost_result):
            try:
                rows += fn(tmp)
            except Exception as exc:  # a missing function on old code is a failed check, not a crash
                rows.append((fn.__name__, False, f"{type(exc).__name__}: {exc}"))
    passed = sum(ok for _, ok, _ in rows)
    lines = [f"# Offline checks: {passed}/{len(rows)} passed", "", "`python offline_checks.py`, run from the code directory; no model call.", "",
             "| | check | evidence |", "|---|---|---|"]
    lines += [f"| {'PASS' if ok else '**FAIL**'} | {label.replace('|', '\\|')} | `{evidence[:300].replace('|', '\\|').replace(chr(10), ' ')}` |"
              for label, ok, evidence in rows]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0 if passed == len(rows) else 1


if __name__ == "__main__":
    sys.exit(main())
