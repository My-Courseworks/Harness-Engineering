"""Kestrel Card's systems of record: customers, the ledger, dispute cases, outbound messages.

Kestrel Card is a fictional card issuer. Nothing in this file is agent memory.
It is the ground truth the agent reaches through tools, by exact lookup scoped
to the logged-in customer (the module's "pricing is an exact lookup by SKU"
point, moved to transactions). A tool never takes a user id from the model;
the harness supplies it, so the model cannot name somebody else's account.

Anything that must hold when tool calls run in parallel (LangGraph's ToolNode runs them on a thread pool, and two
processes may share these files) is one SQL transaction, never a read in one call and a write in the next:
  - a verification attempt counts the failures, refuses or evaluates, and records itself under BEGIN IMMEDIATE;
  - a dispute checks for an open case on the transaction, numbers the new case and inserts it in one transaction,
    behind a unique index (one open case per transaction);
  - evidence is appended by one UPDATE, so parallel notes cannot overwrite each other;
  - one message per follow-up is a unique index.
"""

import sqlite3
from contextlib import closing
from datetime import timedelta
from pathlib import Path

from cardcare.clock import format_instant, parse_instant
from cardcare.memory_policy import VERIFICATION_LOCK_HOURS

SCHEMA = """
CREATE TABLE IF NOT EXISTS customers (
  user_id TEXT PRIMARY KEY,
  display_name TEXT NOT NULL,
  card_last4 TEXT NOT NULL,
  postal_code TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS transactions (
  txn_id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL REFERENCES customers(user_id),
  posted_on TEXT NOT NULL,
  merchant TEXT NOT NULL,
  description TEXT NOT NULL,
  amount_cents INTEGER NOT NULL,
  currency TEXT NOT NULL,
  category TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS cases (
  case_id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL REFERENCES customers(user_id),
  txn_id TEXT NOT NULL REFERENCES transactions(txn_id),
  reason TEXT NOT NULL,
  evidence_note TEXT,
  status TEXT NOT NULL,
  opened_at TEXT NOT NULL,
  resolution_code TEXT,
  resolution_note TEXT,
  resolved_at TEXT,
  decision_id TEXT               -- one back-office decision event; a batch shares one id
);
CREATE TABLE IF NOT EXISTS outbound_messages (
  message_id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id TEXT NOT NULL REFERENCES customers(user_id),
  channel TEXT NOT NULL,
  body TEXT NOT NULL,
  followup_id TEXT,
  status TEXT NOT NULL,          -- sent, held (drafted, awaiting a reviewer), or rejected
  drafted_at TEXT NOT NULL,
  sent_at TEXT,
  reviewed_by TEXT
);
-- "One message per follow-up" is a constraint, not a read-then-insert: parallel tool calls cannot race past it.
CREATE UNIQUE INDEX IF NOT EXISTS one_message_per_followup
  ON outbound_messages(followup_id) WHERE followup_id IS NOT NULL AND status != 'rejected';
-- Step-up attempts are counted on the account, so a new conversation does not reset the lockout.
CREATE TABLE IF NOT EXISTS verification_attempts (
  user_id TEXT NOT NULL,
  at TEXT NOT NULL,
  succeeded INTEGER NOT NULL
);
"""
# One open case per transaction: parallel filings cannot open two.
CASE_INDEX = "CREATE UNIQUE INDEX IF NOT EXISTS one_open_case_per_transaction ON cases(user_id, txn_id) WHERE status = 'under_review'"

CUSTOMERS = [
    ("priya", "Priya", "4427", "94107"),
    ("marco", "Marco", "8830", "10011"),
    ("dana", "Dana", "5127", "60614"),
    ("eli", "Eli", "6610", "73301"),
]

TRANSACTIONS = [
    ("T-1001", "priya", "2026-09-28", "StreamMax", "StreamMax Premium monthly", 1599, "USD", "subscription"),
    ("T-1002", "priya", "2026-10-28", "StreamMax", "StreamMax Premium monthly", 1599, "USD", "subscription"),
    ("T-1003", "priya", "2026-10-30", "Bluebottle Coffee", "Coffee", 650, "USD", "dining"),
    ("T-1004", "priya", "2026-11-08", "Pastelaria Lisboa", "Bakery, Lisbon", 420, "EUR", "dining"),
    ("T-1005", "priya", "2026-12-01", "Livraria Porto", "Bookshop, Porto", 2200, "EUR", "retail"),
    ("T-2001", "marco", "2025-11-03", "FitPulse Gym", "FitPulse annual membership", 24000, "USD", "fitness"),
    ("T-2002", "marco", "2026-11-03", "FitPulse Gym", "FitPulse annual membership renewal", 24000, "USD", "fitness"),
    ("T-2003", "marco", "2026-11-05", "Corner Deli", "Deli", 1240, "USD", "dining"),
    ("T-3001", "dana", "2026-10-01", "CloudNest Storage", "CloudNest 2TB monthly", 999, "USD", "subscription"),
    ("T-3002", "dana", "2026-11-01", "CloudNest Storage", "CloudNest 2TB monthly", 999, "USD", "subscription"),
    ("T-4001", "eli", "2026-10-01", "CloudNest Storage", "CloudNest 2TB monthly", 999, "USD", "subscription"),
    ("T-4002", "eli", "2026-11-01", "CloudNest Storage", "CloudNest 2TB monthly", 999, "USD", "subscription"),
]

DISPUTE_REASONS = ("cancelled_subscription", "not_recognized", "duplicate", "goods_not_received", "incorrect_amount")


def _connect(db_path: Path, autocommit: bool = False) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path, timeout=60, isolation_level=None if autocommit else "")
    conn.row_factory = sqlite3.Row
    return conn


def _format_amount(amount_cents: int, currency: str) -> str:
    symbol = {"USD": "$", "EUR": "€"}.get(currency, currency + " ")
    return f"{symbol}{amount_cents / 100:.2f}"


def _transaction_view(row: sqlite3.Row) -> dict:
    return {
        "transaction_id": row["txn_id"],
        "posted_on": row["posted_on"],
        "merchant": row["merchant"],
        "description": row["description"],
        "amount": _format_amount(row["amount_cents"], row["currency"]),
        "currency": row["currency"],
        "category": row["category"],
    }


def _case_view(row: sqlite3.Row) -> dict:
    return {key: row[key] for key in row.keys()}


def seed_bank(db_path: Path) -> None:
    """Create the bank tables and load the fixed seed customers and transactions."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with closing(_connect(db_path)) as conn, conn:
        conn.executescript(SCHEMA)
        try:
            conn.execute(CASE_INDEX)
        except sqlite3.IntegrityError:  # a store written by an earlier version already holds duplicate open cases
            pass
        conn.executemany("INSERT OR IGNORE INTO customers VALUES (?, ?, ?, ?)", CUSTOMERS)
        conn.executemany("INSERT OR IGNORE INTO transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?)", TRANSACTIONS)


def identity_matches(db_path: Path, user_id: str, card_last4: str, postal_code: str) -> bool:
    with closing(_connect(db_path)) as conn:
        row = conn.execute("SELECT card_last4, postal_code FROM customers WHERE user_id = ?", (user_id,)).fetchone()
    return bool(row) and row["card_last4"] == card_last4.strip() and row["postal_code"] == postal_code.strip()


def find_transactions(db_path: Path, user_id: str, merchant: str | None, now: str) -> list[dict]:
    """The customer's posted transactions up to `now`, optionally filtered by merchant substring."""
    query = "SELECT * FROM transactions WHERE user_id = ? AND posted_on <= ?"
    params: list = [user_id, now[:10]]
    if merchant:
        query += " AND merchant LIKE ?"
        params.append(f"%{merchant}%")
    with closing(_connect(db_path)) as conn:
        rows = conn.execute(query + " ORDER BY posted_on", params).fetchall()
    return [_transaction_view(row) for row in rows]


def get_transaction(db_path: Path, user_id: str, txn_id: str) -> dict | None:
    with closing(_connect(db_path)) as conn:
        row = conn.execute("SELECT * FROM transactions WHERE user_id = ? AND txn_id = ?", (user_id, txn_id)).fetchone()
    return dict(row) if row else None


def open_case(db_path: Path, user_id: str, txn_id: str, reason: str, evidence_note: str | None, now: str) -> tuple[dict, bool]:
    """Open a case, or return the one already open on this transaction. (case, created) in one transaction."""
    with closing(_connect(db_path, autocommit=True)) as conn:
        conn.execute("BEGIN IMMEDIATE")
        try:
            existing = conn.execute("SELECT * FROM cases WHERE user_id = ? AND txn_id = ? AND status = 'under_review'",
                                    (user_id, txn_id)).fetchone()
            if existing:
                return _case_view(existing), False
            count = conn.execute("SELECT COUNT(*) FROM cases").fetchone()[0]
            case_id = f"C-{5001 + count}"
            conn.execute(
                "INSERT INTO cases (case_id, user_id, txn_id, reason, evidence_note, status, opened_at)"
                " VALUES (?, ?, ?, ?, ?, 'under_review', ?)",
                (case_id, user_id, txn_id, reason, evidence_note, now),
            )
            return _case_view(conn.execute("SELECT * FROM cases WHERE case_id = ?", (case_id,)).fetchone()), True
        finally:
            conn.execute("COMMIT")


def open_case_for_transaction(db_path: Path, user_id: str, txn_id: str) -> dict | None:
    with closing(_connect(db_path)) as conn:
        row = conn.execute(
            "SELECT * FROM cases WHERE user_id = ? AND txn_id = ? AND status = 'under_review'", (user_id, txn_id)
        ).fetchone()
    return _case_view(row) if row else None


def list_cases(db_path: Path, user_id: str, case_id: str | None) -> list[dict]:
    query, params = "SELECT * FROM cases WHERE user_id = ?", [user_id]
    if case_id:
        query += " AND case_id = ?"
        params.append(case_id)
    with closing(_connect(db_path)) as conn:
        rows = conn.execute(query + " ORDER BY opened_at", params).fetchall()
    return [_case_view(row) for row in rows]


def cases_by_id(db_path: Path, case_ids: list[str]) -> list[dict]:
    if not case_ids:
        return []
    marks = ",".join("?" for _ in case_ids)
    with closing(_connect(db_path)) as conn:
        rows = conn.execute(f"SELECT * FROM cases WHERE case_id IN ({marks}) ORDER BY case_id", case_ids).fetchall()
    return [_case_view(row) for row in rows]


def resolve_case(db_path: Path, case_id: str, status: str, resolution_code: str, note: str, now: str, decision_id: str) -> dict:
    """Back-office step: a decision on one case. Cases decided in one batch share a decision_id."""
    with closing(_connect(db_path)) as conn, conn:
        conn.execute(
            "UPDATE cases SET status = ?, resolution_code = ?, resolution_note = ?, resolved_at = ?, decision_id = ? WHERE case_id = ?",
            (status, resolution_code, note, now, decision_id, case_id),
        )
        row = conn.execute("SELECT * FROM cases WHERE case_id = ?", (case_id,)).fetchone()
    return _case_view(row) if row else {"error": f"no case {case_id}: the dispute it stands for was never filed"}


def record_outbound_message(db_path: Path, user_id: str, channel: str, body: str, followup_id: str | None, held: bool, now: str) -> dict | None:
    """Send a message now, or hold the draft for a reviewer when `held`. None if this follow-up already has its message."""
    try:
        with closing(_connect(db_path)) as conn, conn:
            cursor = conn.execute(
                "INSERT INTO outbound_messages (user_id, channel, body, followup_id, status, drafted_at, sent_at)"
                " VALUES (?, ?, ?, ?, ?, ?, ?)",
                (user_id, channel, body, followup_id, "held" if held else "sent", now, None if held else now),
            )
            row = conn.execute("SELECT * FROM outbound_messages WHERE message_id = ?", (cursor.lastrowid,)).fetchone()
    except sqlite3.IntegrityError:
        return None
    return dict(row)


def _failures(conn: sqlite3.Connection, user_id: str, now: str) -> int:
    since = format_instant(parse_instant(now) - timedelta(hours=VERIFICATION_LOCK_HOURS))  # instants are stored normalised
    last_ok = conn.execute("SELECT MAX(rowid) FROM verification_attempts WHERE user_id = ? AND succeeded = 1", (user_id,)).fetchone()[0]
    return conn.execute("SELECT COUNT(*) FROM verification_attempts WHERE user_id = ? AND succeeded = 0 AND at > ? AND rowid > ?",
                        (user_id, since, last_ok or 0)).fetchone()[0]


def failed_verifications(db_path: Path, user_id: str, now: str) -> int:
    """Failed step-up attempts in the lock window, since the account's last success."""
    with closing(_connect(db_path)) as conn:
        return _failures(conn, user_id, now)


def attempt_verification(db_path: Path, user_id: str, card_last4: str, postal_code: str, now: str, max_failures: int) -> dict:
    """One step-up attempt, atomically: count the failures since the last success, refuse without evaluating once
    `max_failures` stand, otherwise evaluate and record the attempt, all inside one BEGIN IMMEDIATE transaction. Six
    parallel guesses are six transactions in a row, so no guess is ever evaluated past the limit."""
    with closing(_connect(db_path, autocommit=True)) as conn:
        conn.execute("BEGIN IMMEDIATE")
        try:
            failures = _failures(conn, user_id, now)
            if failures >= max_failures:
                return {"outcome": "locked", "failures": failures}
            row = conn.execute("SELECT card_last4, postal_code FROM customers WHERE user_id = ?", (user_id,)).fetchone()
            matched = bool(row) and row["card_last4"] == str(card_last4).strip() and row["postal_code"] == str(postal_code).strip()
            conn.execute("INSERT INTO verification_attempts VALUES (?, ?, ?)", (user_id, format_instant(parse_instant(now)), int(matched)))
            return {"outcome": "matched" if matched else "mismatch", "failures": 0 if matched else failures + 1}
        finally:
            conn.execute("COMMIT")


def record_verification(db_path: Path, user_id: str, succeeded: bool, now: str) -> None:
    with closing(_connect(db_path)) as conn, conn:
        conn.execute("INSERT INTO verification_attempts VALUES (?, ?, ?)", (user_id, format_instant(parse_instant(now)), int(succeeded)))


def release_message(db_path: Path, message_id: int, reviewer: str, now: str) -> None:
    with closing(_connect(db_path)) as conn, conn:
        conn.execute("UPDATE outbound_messages SET status = 'sent', sent_at = ?, reviewed_by = ? WHERE message_id = ? AND status = 'held'",
                     (now, reviewer, message_id))


def reject_message(db_path: Path, message_id: int, reviewer: str, now: str) -> None:
    with closing(_connect(db_path)) as conn, conn:
        conn.execute("UPDATE outbound_messages SET status = 'rejected', reviewed_by = ? WHERE message_id = ? AND status = 'held'",
                     (reviewer, message_id))


def add_case_evidence(db_path: Path, user_id: str, case_id: str, evidence_note: str, now: str) -> dict:
    """Attach more evidence to one of the customer's open cases: one UPDATE that appends, so parallel calls never
    overwrite each other's notes."""
    line = f"[{now[:10]}] {evidence_note}"
    with closing(_connect(db_path)) as conn, conn:
        cursor = conn.execute(
            "UPDATE cases SET evidence_note = CASE WHEN evidence_note IS NULL OR evidence_note = '' THEN ? "
            "ELSE evidence_note || char(10) || ? END WHERE case_id = ? AND user_id = ? AND status = 'under_review'",
            (line, line, case_id, user_id))
        row = conn.execute("SELECT * FROM cases WHERE case_id = ? AND user_id = ?", (case_id, user_id)).fetchone()
    if cursor.rowcount == 1:
        return _case_view(row)
    if not row:
        return {"error": f"{case_id} is not a case on this customer's account"}
    return {"error": f"{case_id} is already decided ({row['status']}); file a new dispute with the evidence instead"}


def reject_held_messages(db_path: Path, followup_ids: list[str], reviewer: str) -> None:
    """Held drafts of follow-ups that were cancelled (an erasure) are never released."""
    if not followup_ids:
        return
    marks = ",".join("?" for _ in followup_ids)
    with closing(_connect(db_path)) as conn, conn:
        conn.execute(f"UPDATE outbound_messages SET status = 'rejected', reviewed_by = ? WHERE status = 'held' AND followup_id IN ({marks})",
                     (reviewer, *followup_ids))


def outbound_messages(db_path: Path) -> list[dict]:
    with closing(_connect(db_path)) as conn:
        rows = conn.execute("SELECT * FROM outbound_messages ORDER BY message_id").fetchall()
    return [dict(row) for row in rows]


def all_cases(db_path: Path) -> list[dict]:
    with closing(_connect(db_path)) as conn:
        rows = conn.execute("SELECT * FROM cases ORDER BY case_id").fetchall()
    return [_case_view(row) for row in rows]
