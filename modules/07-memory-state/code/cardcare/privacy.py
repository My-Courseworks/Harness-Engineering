"""The erasure ledger: a right-to-erasure request is a durable record, not a flag on one conversation.

`request_erasure` writes the request the moment the customer asks. Every path that can end a conversation
or run background work executes pending requests: the end of a session, the maintenance tick (which is what
eventually runs for a closed tab), and the start of the customer's next turn in any session. A request is
executed once, and leaves a tombstone (`erased_at`) so that work scheduled before the erasure, such as a case
follow-up that still has to reach the customer, cannot write new memory about them.
"""

import sqlite3
from contextlib import closing
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS erasure_requests (
  user_id TEXT NOT NULL,
  requested_at TEXT NOT NULL,
  executed_at TEXT
);
"""


def create_ledger(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(db_path)) as conn, conn:
        conn.executescript(SCHEMA)


def request_erasure(db_path: Path, user_id: str, now: str) -> None:
    with closing(sqlite3.connect(db_path)) as conn, conn:
        conn.execute("INSERT INTO erasure_requests (user_id, requested_at) VALUES (?, ?)", (user_id, now))


def pending_erasures(db_path: Path) -> list[str]:
    with closing(sqlite3.connect(db_path)) as conn:
        return [row[0] for row in conn.execute("SELECT DISTINCT user_id FROM erasure_requests WHERE executed_at IS NULL")]


def mark_erased(db_path: Path, user_id: str, now: str) -> None:
    with closing(sqlite3.connect(db_path)) as conn, conn:
        conn.execute("UPDATE erasure_requests SET executed_at = ? WHERE user_id = ? AND executed_at IS NULL", (now, user_id))


def erased_at(db_path: Path, user_id: str) -> str | None:
    """The latest executed erasure of this customer, if any: the tombstone."""
    with closing(sqlite3.connect(db_path)) as conn:
        row = conn.execute("SELECT MAX(executed_at) FROM erasure_requests WHERE user_id = ?", (user_id,)).fetchone()
    return row[0] if row else None
