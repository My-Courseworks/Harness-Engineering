"""The card desk's multi-step operations, framework-free.

Each function takes the scope values a framework has already resolved (who the
customer is, what time it is, the app-wide settings) as plain arguments, so the
ADK and LangGraph tools differ only in where they read those values from.
"""

from pathlib import Path

from cardcare import scheduler, world
from cardcare.clock import add_days, parse_instant
from cardcare.memory_policy import redact_card_secrets

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
    existing = world.open_case_for_transaction(bank_db, user_id, transaction_id)
    if existing:
        return {"error": f"case {existing['case_id']} is already open for {transaction_id}"}
    case = world.open_case(bank_db, user_id, transaction_id, reason, redact_card_secrets(evidence_note) if evidence_note else None, now)
    # Customer-facing outcomes on large disputes are reviewed by a person before they go out.
    approval = "ops_reviewer" if txn["amount_cents"] >= large_dispute_threshold_cents else "none"
    followup = scheduler.schedule_followup(
        scheduler_db, user_id, "case_status_followup", add_days(now, review_days),
        {"case_id": case["case_id"]}, approval, now,
    )
    return {
        "case_id": case["case_id"],
        "status": case["status"],
        "followup": {
            "followup_id": followup["followup_id"],
            "due": followup["trigger_at"][:10],
            "approval": "a Kestrel reviewer approves the message before it is sent" if approval != "none" else "none",
            "sent_on": "the contact channel on file when it is sent",
        },
    }


def schedule_customer_reminder(scheduler_db: Path, user_id: str, note: str, remind_on: str, now: str) -> dict:
    try:
        trigger_at = f"{parse_instant(remind_on).date().isoformat()}T09:00:00Z"
    except ValueError:
        return {"error": "remind_on must be a date, YYYY-MM-DD"}
    if parse_instant(trigger_at) <= parse_instant(now):
        return {"error": "remind_on must be in the future"}
    record = scheduler.schedule_followup(scheduler_db, user_id, "customer_reminder", trigger_at, {"note": redact_card_secrets(note)}, "none", now)
    return {"followup_id": record["followup_id"], "due": trigger_at[:10]}
