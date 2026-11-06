"""Prospective memory: a scheduler the harness owns, outside the model and outside every memory store.

Each record answers the module's five questions:
  action    - what should happen ("case_status_followup" or "customer_reminder")
  trigger   - when (`trigger_at`, compared with the harness clock)
  resume    - what the woken-up agent needs to pick the task up cold (ids, not facts)
  done flag - `status`, set to done by the harness on evidence, never on the model's word
  approval  - who must sign off before it runs ("none" or "ops_reviewer")

The agent's interface is narrow: a tool writes a record. `fire_due_followups`
wakes a fresh agent session when a record falls due; the record outlives the
conversation that created it.
"""

import inspect
import json
import sqlite3
import uuid
from collections.abc import Callable
from contextlib import closing
from pathlib import Path

from cardcare import world

MAX_ATTEMPTS = 3

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
  last_error TEXT
);
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


def schedule_followup(db_path: Path, user_id: str, action: str, trigger_at: str, resume: dict, approval: str, now: str) -> dict:
    followup_id = f"F-{uuid.uuid4().hex[:8]}"
    with closing(_connect(db_path)) as conn, conn:
        conn.execute(
            "INSERT INTO followups (followup_id, user_id, action, trigger_at, resume_json, approval, status, created_at)"
            " VALUES (?, ?, ?, ?, ?, ?, 'pending', ?)",
            (followup_id, user_id, action, trigger_at, json.dumps(resume), approval, now),
        )
        row = conn.execute("SELECT * FROM followups WHERE followup_id = ?", (followup_id,)).fetchone()
    return _record_view(row)


def list_followups(db_path: Path) -> list[dict]:
    with closing(_connect(db_path)) as conn:
        rows = conn.execute("SELECT * FROM followups ORDER BY created_at, followup_id").fetchall()
    return [_record_view(row) for row in rows]


def approve_followup(db_path: Path, followup_id: str, reviewer: str) -> dict:
    """A human signs off a record that was parked for approval; it fires on the next run."""
    with closing(_connect(db_path)) as conn, conn:
        conn.execute(
            "UPDATE followups SET approved_by = ?, status = 'pending'"
            " WHERE followup_id = ? AND status = 'awaiting_approval'",
            (reviewer, followup_id),
        )
        row = conn.execute("SELECT * FROM followups WHERE followup_id = ?", (followup_id,)).fetchone()
    return _record_view(row)


def _due_records(db_path: Path, now: str) -> list[dict]:
    with closing(_connect(db_path)) as conn:
        rows = conn.execute(
            "SELECT * FROM followups WHERE status = 'pending' AND trigger_at <= ? ORDER BY trigger_at", (now,)
        ).fetchall()
    return [_record_view(row) for row in rows]


def _set_status(db_path: Path, followup_id: str, from_status: str, to_status: str, **fields) -> bool:
    """Compare-and-set transition, so two workers can never both fire one record."""
    assignments = ", ".join([f"{name} = ?" for name in fields] + ["status = ?"])
    with closing(_connect(db_path)) as conn, conn:
        cursor = conn.execute(
            f"UPDATE followups SET {assignments} WHERE followup_id = ? AND status = ?",
            [*fields.values(), to_status, followup_id, from_status],
        )
    return cursor.rowcount == 1


async def fire_due_followups(
    scheduler_db: Path,
    bank_db: Path,
    now: str,
    run_followup_session: Callable[[dict, str], object],
) -> list[dict]:
    """Wake the agent for every due record, then decide `done` from the outbound-message log.

    `run_followup_session(record, now)` is the framework's resume callback (sync or async).

    Returns one outcome row per due record: fired_done, retry, failed, or awaiting_approval.
    """
    outcomes = []
    for record in _due_records(scheduler_db, now):
        followup_id = record["followup_id"]
        if record["approval"] != "none" and not record["approved_by"]:
            _set_status(scheduler_db, followup_id, "pending", "awaiting_approval")
            outcomes.append({"followup_id": followup_id, "user_id": record["user_id"], "outcome": "awaiting_approval"})
            continue
        if not _set_status(scheduler_db, followup_id, "pending", "running", fired_at=now, attempts=record["attempts"] + 1):
            continue
        error = None
        try:
            result = run_followup_session(record, now)
            if inspect.isawaitable(result):
                await result
        except Exception as exc:  # the record must survive any agent failure
            error = f"{type(exc).__name__}: {exc}"
        delivered = any(m["followup_id"] == followup_id for m in world.outbound_messages(bank_db))
        if delivered:
            _set_status(scheduler_db, followup_id, "running", "done", done_at=now, last_error=None)
            outcome = "fired_done"
        else:
            exhausted = record["attempts"] + 1 >= MAX_ATTEMPTS
            _set_status(
                scheduler_db, followup_id, "running", "failed" if exhausted else "pending",
                last_error=error or "agent finished without sending the customer a message",
            )
            outcome = "failed" if exhausted else "retry"
        outcomes.append({"followup_id": followup_id, "user_id": record["user_id"], "outcome": outcome, "error": error})
    return outcomes


def followup_trigger_message(record: dict) -> str:
    """The message that resumes a fresh agent session when a record fires."""
    return (
        f"[scheduled follow-up {record['followup_id']}] action={record['action']} "
        f"resume={json.dumps(record['resume'])}. The customer is not in this conversation. "
        "Carry out the action using your tools, then send the customer exactly one message with notify_customer."
    )
