"""Erasure as a memory generation, and the fence every memory write passes.

Each customer has a memory generation, and every session is registered with the generation it started in.
`begin_erasure` raises the generation under a write lock on this database. From that moment:
  - every memory write (a fact, an episode, a reminder) is made inside `write_guard`, which holds the same lock and
    lets the write through only if the writing session's generation is current. A session that started before the
    erasure, including the one the customer asked in, can write nothing more, whatever runs concurrently;
  - the erasure then deletes facts, episodes, reminders and their notes, and every transcript except the one the
    request was made in, which is still running. That one is deleted when it ends (end of session, idle close by
    maintenance, or the customer's next turn in another session) and its request is then marked executed;
  - scheduled work created in an older generation can no longer write memory either: a reminder is cancelled with
    the rest, and a case follow-up, which must still reach the customer, runs without storing a session at all.
Bank records (cases, the ledger, messages already sent) are not memory and are not touched. This database keeps
only ids and timestamps: who asked, in which session, when, and each session's generation.
"""

import sqlite3
from contextlib import closing, contextmanager
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS erasure_requests (
  user_id TEXT NOT NULL,
  requested_at TEXT NOT NULL,
  executed_at TEXT
);
CREATE TABLE IF NOT EXISTS memory_generations (
  user_id TEXT PRIMARY KEY,
  generation INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS memory_sessions (
  user_id TEXT NOT NULL,
  session_id TEXT NOT NULL,
  generation INTEGER NOT NULL,
  kind TEXT NOT NULL,
  created_at TEXT NOT NULL,
  PRIMARY KEY (user_id, session_id)
);
"""


def _connect(db_path: Path) -> sqlite3.Connection:
    return sqlite3.connect(db_path, timeout=60, isolation_level=None)


def create_ledger(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with closing(_connect(db_path)) as conn:
        conn.executescript(SCHEMA)
        columns = {row[1] for row in conn.execute("PRAGMA table_info(erasure_requests)")}
        if "requested_in" not in columns:
            conn.execute("ALTER TABLE erasure_requests ADD COLUMN requested_in TEXT")


def _generation(conn: sqlite3.Connection, user_id: str) -> int:
    row = conn.execute("SELECT generation FROM memory_generations WHERE user_id = ?", (user_id,)).fetchone()
    return row[0] if row else 0


def current_generation(db_path: Path, user_id: str) -> int:
    with closing(_connect(db_path)) as conn:
        return _generation(conn, user_id)


def register_session(db_path: Path, user_id: str, session_id: str, kind: str, now: str) -> int:
    """Record the generation a session starts in (once); returns the session's generation."""
    with closing(_connect(db_path)) as conn:
        conn.execute("BEGIN IMMEDIATE")
        conn.execute("INSERT OR IGNORE INTO memory_sessions VALUES (?, ?, ?, ?, ?)",
                     (user_id, session_id, _generation(conn, user_id), kind, now))
        generation = conn.execute("SELECT generation FROM memory_sessions WHERE user_id = ? AND session_id = ?",
                                  (user_id, session_id)).fetchone()[0]
        conn.execute("COMMIT")
    return generation


def session_record(db_path: Path, user_id: str, session_id: str) -> dict | None:
    with closing(_connect(db_path)) as conn:
        row = conn.execute("SELECT generation, kind, created_at FROM memory_sessions WHERE user_id = ? AND session_id = ?",
                           (user_id, session_id)).fetchone()
    return {"generation": row[0], "kind": row[1], "created_at": row[2]} if row else None


def session_is_current(db_path: Path, user_id: str, session_id: str) -> bool:
    """A session may write memory only if it is registered in the customer's current generation."""
    with closing(_connect(db_path)) as conn:
        return _is_current(conn, user_id, session_id)


def _is_current(conn: sqlite3.Connection, user_id: str, session_id: str) -> bool:
    """Registered in the current generation. A session with no row (written before sessions were registered) counts
    as current only while the customer has never been erased; after an erasure, an unregistered session is stale."""
    row = conn.execute("SELECT generation FROM memory_sessions WHERE user_id = ? AND session_id = ?", (user_id, session_id)).fetchone()
    generation = _generation(conn, user_id)
    return row[0] == generation if row else generation == 0


@contextmanager
def write_guard(db_path: Path, user_id: str, session_id: str):
    """Hold the erasure lock while a memory write is made; yields whether the write may happen at all."""
    with closing(_connect(db_path)) as conn:
        conn.execute("BEGIN IMMEDIATE")
        try:
            yield _is_current(conn, user_id, session_id)
        finally:
            conn.execute("COMMIT")


def begin_erasure(db_path: Path, user_id: str, session_id: str | None, now: str) -> int:
    """Record the request and raise the customer's generation, atomically. Every session registered so far is stale
    from here on; the requesting session stays registered (stale) so that its own end can finish the erasure."""
    with closing(_connect(db_path)) as conn:
        conn.execute("BEGIN IMMEDIATE")
        generation = _generation(conn, user_id) + 1
        conn.execute("INSERT INTO memory_generations VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET generation = excluded.generation",
                     (user_id, generation))
        conn.execute("INSERT INTO erasure_requests (user_id, requested_at, requested_in) VALUES (?, ?, ?)", (user_id, now, session_id))
        conn.execute("DELETE FROM memory_sessions WHERE user_id = ? AND session_id IS NOT ?", (user_id, session_id))
        conn.execute("COMMIT")
    return generation


def pending_requests(db_path: Path, user_id: str | None = None) -> list[dict]:
    """Requests whose requesting session has not been deleted yet."""
    query, params = "SELECT rowid, user_id, requested_at, requested_in FROM erasure_requests WHERE executed_at IS NULL", []
    if user_id:
        query, params = query + " AND user_id = ?", [user_id]
    with closing(_connect(db_path)) as conn:
        return [{"rowid": r[0], "user_id": r[1], "requested_at": r[2], "requested_in": r[3]} for r in conn.execute(query, params)]


def finish_request(db_path: Path, rowid: int, now: str) -> None:
    with closing(_connect(db_path)) as conn:
        conn.execute("UPDATE erasure_requests SET executed_at = ? WHERE rowid = ?", (now, rowid))


def forget_session(db_path: Path, user_id: str, session_id: str) -> None:
    with closing(_connect(db_path)) as conn:
        conn.execute("DELETE FROM memory_sessions WHERE user_id = ? AND session_id = ?", (user_id, session_id))


def erased_at(db_path: Path, user_id: str) -> str | None:
    """The latest request of this customer, if any."""
    with closing(_connect(db_path)) as conn:
        row = conn.execute("SELECT MAX(requested_at) FROM erasure_requests WHERE user_id = ?", (user_id,)).fetchone()
    return row[0] if row else None
