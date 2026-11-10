"""The card desk's multi-step operations, framework-free.

Each function takes the scope values a framework has already resolved (who the
customer is, what time it is, the app-wide settings) as plain arguments, so the
ADK and LangGraph tools differ only in where they read those values from.
"""

from pathlib import Path

from cardcare import scheduler, world
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from cardcare.clock import add_days, format_instant, parse_instant
from cardcare.masking import mask_customer_text
from cardcare.memory_policy import REMINDER_HORIZON_DAYS

DISPUTE_WINDOW_DAYS = 75  # mirrors policy_kb/dispute-window.md; the system of record enforces it


def file_dispute_with_followup(
    bank_db: Path,
    scheduler_db: Path,
    user_id: str,
    transaction_id: str,
    reason: str,
    evidence_note: str | None,
    now: str,
    review_days: int,
    large_dispute_threshold_cents: int,
    channel: str = "secure_message",
    channel_chosen: bool = False,
    generation: int = 0,
) -> dict:
    """Open a case and, in the same step, write its prospective follow-up record.

    The follow-up is scheduled here, deterministically, rather than left to the model:
    a future task that depends on the model remembering to schedule it is a silent drop
    waiting to happen.
    """
    if reason not in world.DISPUTE_REASONS:
        return {"error": f"reason must be one of {', '.join(world.DISPUTE_REASONS)}"}
    txn = world.get_transaction(bank_db, user_id, transaction_id)
    if not txn:
        return {"error": f"{transaction_id} is not a transaction on this customer's account"}
    if parse_instant(txn["posted_on"]) > parse_instant(now):
        return {"error": f"{transaction_id} has not posted yet"}
    age_days = (parse_instant(now) - parse_instant(txn["posted_on"])).days
    if age_days > DISPUTE_WINDOW_DAYS:
        return {"error": f"{transaction_id} posted {age_days} days ago, outside the {DISPUTE_WINDOW_DAYS}-day dispute window"}
    # Checking for an open case and opening one is a single transaction (world.open_case): three parallel filings
    # of one transaction open one case, and only the call that opened it schedules the follow-up.
    case, created = world.open_case(bank_db, user_id, transaction_id, reason,
                                    mask_customer_text(evidence_note) if evidence_note else None, now)
    # Customer-facing outcomes on large disputes are reviewed by a person before they go out.
    approval = "ops_reviewer" if txn["amount_cents"] >= large_dispute_threshold_cents else "none"
    existing = [f for f in scheduler.user_followups(scheduler_db, user_id)
                if f["action"] == "case_status_followup" and f["resume"].get("case_id") == case["case_id"] and f["status"] not in ("cancelled", "failed")]
    if not created and existing:
        return {"error": f"case {case['case_id']} is already open for {transaction_id}", "case_id": case["case_id"], "status": case["status"],
                "followup": {"followup_id": existing[0]["followup_id"], "due": existing[0]["trigger_at"][:10]}}
    # the case exists but its follow-up does not: the step that opens the case and the one that schedules the follow-up are
    # two databases, so a process that died between them (round 5's lost-result probe) left a dispute nobody would revisit;
    # a repeated filing completes it instead of refusing it
    followup = existing[0] if existing else scheduler.schedule_followup(
        scheduler_db, user_id, "case_status_followup", add_days(now, review_days),
        {"case_id": case["case_id"]}, approval, now, generation=generation,
    )
    return {
        "case_id": case["case_id"],
        "status": case["status"],
        **({} if created else {"note": "this dispute was already filed (a call whose result was lost); nothing was filed twice"}),
        "followup": {
            "followup_id": followup["followup_id"],
            "due": followup["trigger_at"][:10],
            "approval": "a Kestrel reviewer approves the message before it is sent" if approval != "none" else "none",
            "sent_on": f"{scheduler.channel_description(channel, channel_chosen)}; if the customer changes their contact "
                       "channel before then, the follow-up uses the new one",
        },
    }


def ensure_case_followups(bank_db: Path, scheduler_db: Path, now: str, review_days: int, large_dispute_threshold_cents: int,
                          user_id: str | None = None, generation_of=lambda user_id: 0) -> list[str]:
    """Every case under review has a follow-up record: the invariant `file_dispute_with_followup` establishes in two
    databases, which a process that dies between the two steps breaks (round 5's lost-result probe). Called at the
    start of a customer's turn (their cases) and by maintenance (every customer's), it writes the missing records,
    due `review_days` after the case was opened, reviewed when the dispute is large. Returns the case ids repaired."""
    existing = {f["resume"].get("case_id") for f in scheduler.list_followups(scheduler_db)
                if f["action"] == "case_status_followup" and f["status"] not in ("cancelled", "failed")}
    repaired = []
    for case in world.all_cases(bank_db):
        if case["status"] != "under_review" or case["case_id"] in existing or (user_id and case["user_id"] != user_id):
            continue
        txn = world.get_transaction(bank_db, case["user_id"], case["txn_id"])
        approval = "ops_reviewer" if txn and txn["amount_cents"] >= large_dispute_threshold_cents else "none"
        scheduler.schedule_followup(scheduler_db, case["user_id"], "case_status_followup", add_days(case["opened_at"], review_days),
                                    {"case_id": case["case_id"]}, approval, now, generation=generation_of(case["user_id"]))
        repaired.append(case["case_id"])
    return repaired


def schedule_customer_reminder(scheduler_db: Path, user_id: str, note: str, remind_on: str, remind_at: str, timezone: str, now: str,
                               generation: int = 0, channel: str = "secure_message", channel_chosen: bool = False) -> dict:
    """A reminder at a local date and time. The record stores the UTC instant and the customer's local day; one live
    reminder per local day is a unique index. The readback is computed back from the stored instant, so what the
    customer is told is what will happen (a time skipped by a daylight-saving change reads as the time it becomes)."""
    try:
        zone = ZoneInfo(timezone)
        local = datetime.fromisoformat(f"{remind_on[:10]}T{remind_at}").replace(tzinfo=zone)
    except (ValueError, ZoneInfoNotFoundError, KeyError):
        return {"error": "remind_on must be YYYY-MM-DD, remind_at HH:MM, timezone an IANA name such as America/Los_Angeles"}
    trigger_at = format_instant(local)
    if parse_instant(trigger_at) <= parse_instant(now):
        return {"error": "the reminder time must be in the future"}
    if parse_instant(trigger_at) > parse_instant(add_days(now, REMINDER_HORIZON_DAYS)):
        return {"error": f"a reminder can be set at most {REMINDER_HORIZON_DAYS} days ahead; it holds the customer's own words until it fires"}
    actual = parse_instant(trigger_at).astimezone(zone)
    record = scheduler.schedule_followup(scheduler_db, user_id, "customer_reminder", trigger_at, {"note": mask_customer_text(note)}, "none",
                                         now, generation=generation, local_day=actual.date().isoformat())
    if record is None:
        return {"error": f"a reminder is already scheduled for {actual.date().isoformat()} ({timezone}); one reminder per day, so put "
                         "everything for that day in that one"}
    return {"followup_id": record["followup_id"], "due_utc": trigger_at,
            "local_time": f"{actual.strftime('%A %Y-%m-%d %H:%M')} {actual.tzname()} ({timezone})",
            "sent_on": f"{scheduler.channel_description(channel, channel_chosen)}, the contact channel on file when it is sent"}
