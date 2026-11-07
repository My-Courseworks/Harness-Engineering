"""Prospective memory: a scheduler the harness owns, outside the model and outside every memory store.

Each record answers the module's five questions:
  action    - what should happen ("case_status_followup" or "customer_reminder")
  trigger   - when (`trigger_at`, a normalised UTC instant compared as a time, never as a string)
  resume    - what the woken-up agent needs to pick the task up cold (ids, not facts)
  done flag - `status`: pending, running, awaiting_approval, done, cancelled or failed; set by the
              harness on evidence (a sent message), never on the model's word
  approval  - who signs off before anything reaches the customer ("none" or "ops_reviewer"). The
              reviewer approves the drafted message itself, after the agent has written it, and a
              draft that carries a masking token cannot be approved at all (`message_review_problems`).

The agent's interface is narrow: tools write a record, read the customer's own records, and cancel a
customer reminder. `fire_due_followups` wakes a fresh agent session when a record falls due; the record
outlives the conversation that created it. A record stuck in `running` (the process died mid-fire) is
recovered on the next run: done if its message was already sent, pending otherwise.
"""

import inspect
import json
import re
import sqlite3
import uuid
from collections.abc import Callable
from contextlib import closing
from datetime import timedelta
from pathlib import Path

from cardcare import world
from cardcare.clock import format_instant, parse_instant

MAX_ATTEMPTS = 3
RUNNING_LEASE_MINUTES = 10

SCHEMA = """
CREATE TABLE IF NOT EXISTS followups (
  followup_id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  action TEXT NOT NULL,
  trigger_at TEXT NOT NULL,
  resume_json TEXT NOT NULL,
  approval TEXT NOT NULL,
  status TEXT NOT NULL,
  attempts INTEGER NOT NULL DEFAULT 0,
  approved_by TEXT,
  created_at TEXT NOT NULL,
  fired_at TEXT,
  done_at TEXT,
  cancelled_at TEXT,
  last_error TEXT
);
-- One pending reminder per customer per day: a "send me three reminders" request, however it is phrased and
-- however many parallel tool calls it becomes, cannot create three records.
CREATE UNIQUE INDEX IF NOT EXISTS one_reminder_per_day
  ON followups(user_id, substr(trigger_at, 1, 10)) WHERE action = 'customer_reminder' AND status = 'pending';
"""


def _connect(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def _record_view(row: sqlite3.Row) -> dict:
    record = dict(row)
    record["resume"] = json.loads(record.pop("resume_json"))
    return record


def create_scheduler(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with closing(_connect(db_path)) as conn, conn:
        conn.executescript(SCHEMA)


def schedule_followup(db_path: Path, user_id: str, action: str, trigger_at: str, resume: dict, approval: str, now: str) -> dict | None:
    """Write a record. None if the customer already has a pending reminder that day."""
    followup_id = f"F-{uuid.uuid4().hex[:8]}"
    try:
        with closing(_connect(db_path)) as conn, conn:
            conn.execute(
                "INSERT INTO followups (followup_id, user_id, action, trigger_at, resume_json, approval, status, created_at)"
                " VALUES (?, ?, ?, ?, ?, ?, 'pending', ?)",
                (followup_id, user_id, action, format_instant(parse_instant(trigger_at)), json.dumps(resume), approval,
                 format_instant(parse_instant(now))),
            )
            row = conn.execute("SELECT * FROM followups WHERE followup_id = ?", (followup_id,)).fetchone()
    except sqlite3.IntegrityError:
        return None
    return _record_view(row)


def erase_customer_reminders(db_path: Path, user_id: str, now: str) -> list[str]:
    """Erasure: the customer's pending reminders are cancelled, and the note of every reminder record they ever had,
    whatever its status (pending, cancelled, done, failed), is purged, because the note is their words. Returns
    the ids that were still pending. Case follow-ups carry only a case id and stay with the case."""
    with closing(_connect(db_path)) as conn, conn:
        ids = [row[0] for row in conn.execute(
            "SELECT followup_id FROM followups WHERE user_id = ? AND action = 'customer_reminder' AND status IN ('pending', 'awaiting_approval')",
            (user_id,))]
        conn.execute(
            "UPDATE followups SET status = 'cancelled', cancelled_at = ?, last_error = 'erased at the customer''s request'"
            " WHERE user_id = ? AND action = 'customer_reminder' AND status IN ('pending', 'awaiting_approval')",
            (format_instant(parse_instant(now)), user_id))
        conn.execute("UPDATE followups SET resume_json = '{}' WHERE user_id = ? AND action = 'customer_reminder'", (user_id,))
    return ids


def list_followups(db_path: Path) -> list[dict]:
    with closing(_connect(db_path)) as conn:
        rows = conn.execute("SELECT * FROM followups ORDER BY created_at, followup_id").fetchall()
    return [_record_view(row) for row in rows]


def get_followup(db_path: Path, followup_id: str) -> dict | None:
    with closing(_connect(db_path)) as conn:
        row = conn.execute("SELECT * FROM followups WHERE followup_id = ?", (followup_id,)).fetchone()
    return _record_view(row) if row else None


def user_followups(db_path: Path, user_id: str) -> list[dict]:
    return [f for f in list_followups(db_path) if f["user_id"] == user_id]


def cancel_followup(db_path: Path, followup_id: str, user_id: str, now: str) -> dict | None:
    """Cancel a record that has not fired yet. Returns the record, or None if it was not cancellable."""
    with closing(_connect(db_path)) as conn, conn:
        cursor = conn.execute(
            "UPDATE followups SET status = 'cancelled', cancelled_at = ?"
            " WHERE followup_id = ? AND user_id = ? AND status IN ('pending', 'awaiting_approval')",
            (format_instant(parse_instant(now)), followup_id, user_id),
        )
        row = conn.execute("SELECT * FROM followups WHERE followup_id = ?", (followup_id,)).fetchone()
    return _record_view(row) if cursor.rowcount == 1 else None


def message_review_problems(body: str) -> list[str]:
    """What no approval can override: a customer-facing message never carries a masking token."""
    return [f"the draft contains masked text: {token}" for token in re.findall(r"\S*\[REDACTED[^\]]*\]\S*", body)]


def approve_followup(db_path: Path, bank_db: Path, followup_id: str, reviewer: str, now: str) -> dict:
    """A person signs off the drafted message itself: it is released to the customer and the record is done.
    Raises ValueError if there is no draft, or if the draft fails `message_review_problems` (reject it instead)."""
    held = [m for m in world.outbound_messages(bank_db) if m["followup_id"] == followup_id and m["status"] == "held"]
    if not held:
        raise ValueError(f"{followup_id} has no drafted message awaiting approval")
    problems = message_review_problems(held[-1]["body"])
    if problems:
        raise ValueError("; ".join(problems))
    world.release_message(bank_db, held[-1]["message_id"], reviewer, now)
    _set_status(db_path, followup_id, "awaiting_approval", "done", approved_by=reviewer, done_at=now)
    return get_followup(db_path, followup_id)


def reject_followup(db_path: Path, bank_db: Path, followup_id: str, reviewer: str, note: str, now: str) -> dict:
    """The reviewer rejects the draft: nothing is sent, and the record goes back to pending with their note."""
    for message in world.outbound_messages(bank_db):
        if message["followup_id"] == followup_id and message["status"] == "held":
            world.reject_message(bank_db, message["message_id"], reviewer, now)
    record = get_followup(db_path, followup_id)
    with closing(_connect(db_path)) as conn, conn:
        conn.execute(
            "UPDATE followups SET status = 'pending', resume_json = ?, last_error = ? WHERE followup_id = ? AND status = 'awaiting_approval'",
            (json.dumps({**record["resume"], "reviewer_note": note}), f"draft rejected by {reviewer}", followup_id),
        )
    return get_followup(db_path, followup_id)


def _due_records(db_path: Path, now: str) -> list[dict]:
    instant = parse_instant(now)
    pending = [r for r in list_followups(db_path) if r["status"] == "pending"]
    return sorted((r for r in pending if parse_instant(r["trigger_at"]) <= instant), key=lambda r: parse_instant(r["trigger_at"]))


def _set_status(db_path: Path, followup_id: str, from_status: str, to_status: str, **fields) -> bool:
    """Compare-and-set transition, so two workers can never both fire one record."""
    assignments = ", ".join([f"{name} = ?" for name in fields] + ["status = ?"])
    with closing(_connect(db_path)) as conn, conn:
        cursor = conn.execute(
            f"UPDATE followups SET {assignments} WHERE followup_id = ? AND status = ?",
            [*fields.values(), to_status, followup_id, from_status],
        )
    return cursor.rowcount == 1


def _messages_for(bank_db: Path, followup_id: str, status: str) -> list[dict]:
    return [m for m in world.outbound_messages(bank_db) if m["followup_id"] == followup_id and m["status"] == status]


def recover_stale_running(db_path: Path, bank_db: Path, now: str) -> list[dict]:
    """After a crash between `running` and `done`: done if the message went out, pending otherwise."""
    recovered = []
    for record in list_followups(db_path):
        if record["status"] != "running" or not record["fired_at"]:
            continue
        if parse_instant(record["fired_at"]) + timedelta(minutes=RUNNING_LEASE_MINUTES) > parse_instant(now):
            continue
        sent = _messages_for(bank_db, record["followup_id"], "sent")
        target = "done" if sent else "pending"
        if _set_status(db_path, record["followup_id"], "running", target, last_error="recovered after an interrupted run"):
            recovered.append({"followup_id": record["followup_id"], "user_id": record["user_id"], "outcome": f"recovered_{target}"})
    return recovered


async def fire_due_followups(
    scheduler_db: Path,
    bank_db: Path,
    now: str,
    run_followup_session: Callable[[dict, str], object],
) -> list[dict]:
    """Wake the agent for every due record, then set its status from the outbound-message log.

    `run_followup_session(record, now)` is the framework's resume callback (sync or async).
    Returns one outcome row per record touched: fired_done, awaiting_approval, retry, failed, or recovered_*.
    """
    now = format_instant(parse_instant(now))
    outcomes = recover_stale_running(scheduler_db, bank_db, now)
    for record in _due_records(scheduler_db, now):
        followup_id = record["followup_id"]
        if not _set_status(scheduler_db, followup_id, "pending", "running", fired_at=now, attempts=record["attempts"] + 1):
            continue
        error = None
        try:
            result = run_followup_session(record, now)
            if inspect.isawaitable(result):
                await result
        except Exception as exc:  # the record must survive any agent failure
            error = f"{type(exc).__name__}: {exc}"
        if _messages_for(bank_db, followup_id, "sent"):
            _set_status(scheduler_db, followup_id, "running", "done", done_at=now, last_error=None)
            outcome = "fired_done"
        elif _messages_for(bank_db, followup_id, "held"):
            _set_status(scheduler_db, followup_id, "running", "awaiting_approval", last_error=None)
            outcome = "awaiting_approval"
        else:
            exhausted = record["attempts"] + 1 >= MAX_ATTEMPTS
            _set_status(
                scheduler_db, followup_id, "running", "failed" if exhausted else "pending",
                last_error=error or "agent finished without drafting a customer message",
            )
            outcome = "failed" if exhausted else "retry"
        outcomes.append({"followup_id": followup_id, "user_id": record["user_id"], "outcome": outcome, "error": error})
    return outcomes


def followup_trigger_message(record: dict) -> str:
    """The message that resumes a fresh agent session when a record fires."""
    return (
        f"[scheduled follow-up {record['followup_id']}] action={record['action']} "
        f"resume={json.dumps(record['resume'])}. The customer is not in this conversation and cannot reply to the "
        "message you send. Carry out the action using your tools, then send the customer exactly one message with "
        "notify_customer."
    )


def customer_view(record: dict, channel_now: str) -> dict:
    """What a customer may see of their own record."""
    view = {"followup_id": record["followup_id"], "action": record["action"], "due": record["trigger_at"],
            "status": record["status"], "sent_on": f"the contact channel on file when it is sent (currently {channel_now})"}
    view.update({k: v for k, v in record["resume"].items() if k in ("case_id", "note")})
    if record["approval"] != "none":
        view["approval"] = "a Kestrel reviewer approves the message before it is sent"
    return view
