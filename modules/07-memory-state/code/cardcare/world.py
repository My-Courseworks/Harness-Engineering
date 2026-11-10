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
  - one message per follow-up is a unique index;
  - a one-time code is issued and checked in one transaction each (one open code per customer is a unique index).

The one-time code (round 4): `customers.otp_channel` and `customers.otp_destination` are the issuer's registered mobile
number or email, set when the account was opened and changeable only out of band. No chat tool writes them, and no
memory fact copies them: the follow-up channel the customer picks in chat is memory; the number the bank texts is not.
A code is 6 digits, stored as a salted hash, single-use, dead after CODE_TTL_MINUTES or CODE_MAX_ENTRIES wrong entries;
every wrong entry is a failed attempt on the account's shared lock. The sent message is a row in the outbox, which is
the bank's record of what it sent, with the full destination (an SMS gateway log has it too); the code itself never
goes into a tool result.
"""

import hashlib
import re
import secrets
import sqlite3
import uuid
from contextlib import closing
from datetime import timedelta
from pathlib import Path

from cardcare.clock import format_instant, parse_instant
from cardcare.masking import ONE_TIME_CODE_MASK
from cardcare.memory_policy import (CODE_MAX_ENTRIES, CODE_RESEND_SECONDS, CODE_TTL_MINUTES, MAX_CODES_PER_DAY, MAX_VERIFICATION_ATTEMPTS,
                                    VERIFICATION_LOCK_HOURS,
                                    VERIFICATION_TTL_MINUTES)

SCHEMA = """
CREATE TABLE IF NOT EXISTS customers (
  user_id TEXT PRIMARY KEY,
  display_name TEXT NOT NULL,
  card_last4 TEXT NOT NULL,
  postal_code TEXT NOT NULL,
  otp_channel TEXT NOT NULL DEFAULT 'sms',       -- where the issuer sends one-time codes: the registered mobile or email
  otp_destination TEXT NOT NULL DEFAULT ''       -- set out of band, never by a chat tool, never copied into memory
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
  reviewed_by TEXT,
  destination TEXT,              -- the address it went to (one-time codes: the registered number or email)
  purpose TEXT NOT NULL DEFAULT 'follow_up'   -- follow_up or one_time_code
);
-- One-time codes: issued, checked and retired in the bank, never in memory.
CREATE TABLE IF NOT EXISTS verification_challenges (
  challenge_id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL REFERENCES customers(user_id),
  session_id TEXT,
  code_hash TEXT NOT NULL,
  salt TEXT NOT NULL,
  channel TEXT NOT NULL,
  destination TEXT NOT NULL,
  sent_at TEXT NOT NULL,
  expires_at TEXT NOT NULL,
  attempts INTEGER NOT NULL DEFAULT 0,
  status TEXT NOT NULL,          -- open, consumed, expired, failed, cancelled
  closed_at TEXT,
  consumed_in TEXT                 -- round 5: the conversation that entered the matching code (a repeat from it is the same proof)
);
CREATE UNIQUE INDEX IF NOT EXISTS one_open_code_per_customer ON verification_challenges(user_id) WHERE status = 'open';
-- "One message per follow-up" is a constraint, not a read-then-insert: parallel tool calls cannot race past it.
CREATE UNIQUE INDEX IF NOT EXISTS one_message_per_followup
  ON outbound_messages(followup_id) WHERE followup_id IS NOT NULL AND status != 'rejected';
-- Step-up attempts are counted on the account, so a new conversation does not reset the lockout.
CREATE TABLE IF NOT EXISTS verification_attempts (
  user_id TEXT NOT NULL,
  at TEXT NOT NULL,
  succeeded INTEGER NOT NULL,
  kind TEXT NOT NULL DEFAULT 'digits',  -- digits (last four + ZIP) or code (the one-time code)
  session_id TEXT,                      -- round 5: after a tool result was lost to a crash, the same guess made again in the same
  guess_hash TEXT                       -- conversation within REPEAT_WINDOW_SECONDS is the same attempt, not a new one
);
"""
REPEAT_WINDOW_SECONDS = 120
# One open case per transaction: parallel filings cannot open two.
CASE_INDEX = "CREATE UNIQUE INDEX IF NOT EXISTS one_open_case_per_transaction ON cases(user_id, txn_id) WHERE status = 'under_review'"

CUSTOMERS = [
    ("priya", "Priya", "4427", "94107"),
    ("marco", "Marco", "8830", "10011"),
    ("dana", "Dana", "5127", "60614"),
    ("eli", "Eli", "6610", "73301"),
]
# The registered one-time-code destination per customer: fictional numbers from the reserved 555-01xx block, and one
# fictional email, so both channel kinds appear. These are bank records, seeded, never written by any tool.
OTP_DESTINATIONS = {
    "priya": ("sms", "+1 415 555 0100"),
    "marco": ("sms", "+1 212 555 0133"),
    "dana": ("email", "dana.k@example.com"),
    "eli": ("sms", "+1 512 555 0188"),
}

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
        for table, column, ddl in (("customers", "otp_channel", "TEXT NOT NULL DEFAULT 'sms'"), ("customers", "otp_destination", "TEXT NOT NULL DEFAULT ''"),
                                   ("outbound_messages", "destination", "TEXT"), ("outbound_messages", "purpose", "TEXT NOT NULL DEFAULT 'follow_up'"),
                                   ("verification_attempts", "kind", "TEXT NOT NULL DEFAULT 'digits'"),
                                   ("verification_attempts", "session_id", "TEXT"), ("verification_attempts", "guess_hash", "TEXT"),
                                   ("verification_challenges", "consumed_in", "TEXT")):
            if table in {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")} \
                    and column not in {r[1] for r in conn.execute(f"PRAGMA table_info({table})")}:
                conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {ddl}")  # a store written by an earlier version
        conn.executescript(SCHEMA)
        try:
            conn.execute(CASE_INDEX)
        except sqlite3.IntegrityError:  # a store written by an earlier version already holds duplicate open cases
            pass
        conn.executemany("INSERT OR IGNORE INTO customers (user_id, display_name, card_last4, postal_code) VALUES (?, ?, ?, ?)", CUSTOMERS)
        for user_id, (channel, destination) in OTP_DESTINATIONS.items():
            conn.execute("UPDATE customers SET otp_channel = ?, otp_destination = ? WHERE user_id = ? AND otp_destination = ''",
                         (channel, destination, user_id))
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


def with_next_step(case: dict) -> dict:
    """A case as the agent reads it: a decided case also says what can still be done with it. add_case_evidence refuses
    a decided case and says to file a new dispute; a model that only read "rejected" told customers their proof could be
    "added to the case" (round 5's second final pass, LangGraph, both runs). The record now says it before anyone asks."""
    if case["status"] == "under_review":
        return case
    return {**case, "next_step": "This case is decided and closed: nothing can be added to it. With new proof (for example the "
                                 "merchant's cancellation confirmation) the customer can ask in the card-care chat for a new dispute "
                                 "of the same charge."}


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


def record_outbound_message(db_path: Path, user_id: str, channel: str, body: str, followup_id: str | None, held: bool, now: str,
                            destination: str | None = None, purpose: str = "follow_up") -> dict | None:
    """Send a message now, or hold the draft for a reviewer when `held`. None if this follow-up already has its message."""
    try:
        with closing(_connect(db_path)) as conn, conn:
            cursor = conn.execute(
                "INSERT INTO outbound_messages (user_id, channel, body, followup_id, status, drafted_at, sent_at, destination, purpose)"
                " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (user_id, channel, body, followup_id, "held" if held else "sent", now, None if held else now, destination, purpose),
            )
            row = conn.execute("SELECT * FROM outbound_messages WHERE message_id = ?", (cursor.lastrowid,)).fetchone()
    except sqlite3.IntegrityError:
        return None
    return dict(row)


def _failures(conn: sqlite3.Connection, user_id: str, now: str) -> int:
    """Failed attempts of either kind in the lock window since the account's last completed step-up. Only a correct
    one-time code resets the count: a correct last four and ZIP does not, or someone who knows the digits could
    re-verify between code guesses and get three fresh guesses each time."""
    since = format_instant(parse_instant(now) - timedelta(hours=VERIFICATION_LOCK_HOURS))  # instants are stored normalised
    last_ok = conn.execute("SELECT MAX(rowid) FROM verification_attempts WHERE user_id = ? AND succeeded = 1 AND kind = 'code'",
                           (user_id,)).fetchone()[0]
    return conn.execute("SELECT COUNT(*) FROM verification_attempts WHERE user_id = ? AND succeeded = 0 AND at > ? AND rowid > ?",
                        (user_id, since, last_ok or 0)).fetchone()[0]


def failed_verifications(db_path: Path, user_id: str, now: str) -> int:
    """Failed step-up attempts in the lock window, since the account's last success."""
    with closing(_connect(db_path)) as conn:
        return _failures(conn, user_id, now)


def verification_locked(db_path: Path, user_id: str, now: str) -> bool:
    """Whether the account's lock is on: three failures in the window. The lock is asked at every action that needs a
    verification, not only at new guesses, so a verification obtained in the same breath as the lock (the right guess
    first in a parallel batch, the round-4 review's non-blocking 3) buys nothing: locked means locked everywhere."""
    with closing(_connect(db_path)) as conn:
        return _failures(conn, user_id, now) >= MAX_VERIFICATION_ATTEMPTS


def _guess_hash(*parts: str) -> str:
    return hashlib.sha256(":".join(parts).encode()).hexdigest()


def lost_result_is_recent(lost_result_at: str | None, now: str) -> bool:
    """Whether the harness told this conversation, within REPEAT_WINDOW_SECONDS, that a tool call's result was lost. Only
    then may the same guess made again be the lost call repeated; without it every entry is a new attempt, so a customer
    who types the same wrong code twice has made two attempts."""
    return bool(lost_result_at) and 0 <= (parse_instant(now) - parse_instant(lost_result_at)).total_seconds() <= REPEAT_WINDOW_SECONDS


def _repeat_of(conn: sqlite3.Connection, user_id: str, kind: str, guess_hash: str, session_id: str | None, now: str):
    """The account's latest attempt, if it is this very guess made again in the same conversation within
    REPEAT_WINDOW_SECONDS: what a tool call repeated after its result was lost (the process died after the row was
    written and before the framework recorded the result) looks like. A repeat is not a new attempt: it is answered
    from the row and counted once. A different guess, another conversation, or the same guess later is new. Callers
    ask only when the conversation was told of a lost result (`repeat_of_lost_call`)."""
    if not session_id:
        return None
    row = conn.execute("SELECT * FROM verification_attempts WHERE user_id = ? ORDER BY rowid DESC LIMIT 1", (user_id,)).fetchone()
    if row and row["kind"] == kind and row["guess_hash"] == guess_hash and row["session_id"] == session_id \
            and 0 <= (parse_instant(now) - parse_instant(row["at"])).total_seconds() <= REPEAT_WINDOW_SECONDS:
        return row
    return None


def attempt_verification(db_path: Path, user_id: str, card_last4: str, postal_code: str, now: str, max_failures: int,
                         session_id: str | None = None, repeat_of_lost_call: bool = False) -> dict:
    """One step-up attempt, atomically: count the failures since the last success, refuse without evaluating once
    `max_failures` stand, otherwise evaluate and record the attempt, all inside one BEGIN IMMEDIATE transaction. Six
    parallel guesses are six transactions in a row, so no guess is ever evaluated past the limit. With
    `repeat_of_lost_call` (the conversation was just told a result was lost), the same guess made again in the same
    conversation within REPEAT_WINDOW_SECONDS is answered from its row, not counted again."""
    guess = _guess_hash(user_id, str(card_last4).strip(), str(postal_code).strip())
    with closing(_connect(db_path, autocommit=True)) as conn:
        conn.execute("BEGIN IMMEDIATE")
        try:
            repeat = _repeat_of(conn, user_id, "digits", guess, session_id, now) if repeat_of_lost_call else None
            if repeat is not None:
                return {"outcome": "matched" if repeat["succeeded"] else "mismatch", "failures": _failures(conn, user_id, now), "repeat": True}
            failures = _failures(conn, user_id, now)
            if failures >= max_failures:
                return {"outcome": "locked", "failures": failures}
            row = conn.execute("SELECT card_last4, postal_code FROM customers WHERE user_id = ?", (user_id,)).fetchone()
            matched = bool(row) and row["card_last4"] == str(card_last4).strip() and row["postal_code"] == str(postal_code).strip()
            conn.execute("INSERT INTO verification_attempts (user_id, at, succeeded, kind, session_id, guess_hash) VALUES (?, ?, ?, 'digits', ?, ?)",
                         (user_id, format_instant(parse_instant(now)), int(matched), session_id, guess))
            return {"outcome": "matched" if matched else "mismatch", "failures": failures if matched else failures + 1}
        finally:
            conn.execute("COMMIT")


def record_verification(db_path: Path, user_id: str, succeeded: bool, now: str) -> None:
    with closing(_connect(db_path)) as conn, conn:
        conn.execute("INSERT INTO verification_attempts (user_id, at, succeeded, kind) VALUES (?, ?, ?, 'digits')",
                     (user_id, format_instant(parse_instant(now)), int(succeeded)))


# --------------------------------------------------------------------------- one-time codes


def masked_destination(channel: str, destination: str) -> str:
    """What a customer may be told: "text message to ···0100", "email to d···@example.com"."""
    if channel == "email" and "@" in destination:
        local, domain = destination.split("@", 1)
        return f"email to {local[:1]}···@{domain}"
    digits = re.sub(r"\D", "", destination)
    return f"text message to ···{digits[-4:]}"


def otp_destination(db_path: Path, user_id: str) -> tuple[str, str]:
    with closing(_connect(db_path)) as conn:
        row = conn.execute("SELECT otp_channel, otp_destination FROM customers WHERE user_id = ?", (user_id,)).fetchone()
    return (row["otp_channel"], row["otp_destination"]) if row else ("sms", "")


def _code_hash(code: str, salt: str) -> str:
    return hashlib.sha256(f"{salt}:{code}".encode()).hexdigest()


def issue_code(db_path: Path, user_id: str, session_id: str, now: str, max_failures: int) -> dict:
    """Issue a one-time code to the customer's registered destination, in one transaction: refuse while the account is
    locked; refuse a resend within CODE_RESEND_SECONDS of a still-valid code; otherwise cancel any open code, store the
    new one hashed, and write the message the gateway sends to the outbox. Parallel calls meet the one-open-code index
    and all but one get the "already sent" answer. The code is returned only so the caller can log the message; it is
    never put in a tool result."""
    instant = format_instant(parse_instant(now))
    with closing(_connect(db_path, autocommit=True)) as conn:
        conn.execute("BEGIN IMMEDIATE")
        try:
            if _failures(conn, user_id, now) >= max_failures:
                return {"error": f"verification is locked on this account for {VERIFICATION_LOCK_HOURS} hours after {max_failures} failed "
                                 "attempts; no code is sent; the customer must call Kestrel"}
            open_code = conn.execute("SELECT * FROM verification_challenges WHERE user_id = ? AND status = 'open'", (user_id,)).fetchone()
            if open_code:
                age = (parse_instant(instant) - parse_instant(open_code["sent_at"])).total_seconds()
                if parse_instant(instant) < parse_instant(open_code["expires_at"]) and age < CODE_RESEND_SECONDS:
                    return {"error": f"a code was sent {int(age)} seconds ago and is still valid; ask the customer to enter it "
                                     f"(a new one can be sent {CODE_RESEND_SECONDS} seconds after the last)",
                            "sent_to": masked_destination(open_code["channel"], open_code["destination"])}
            day_ago = format_instant(parse_instant(instant) - timedelta(hours=24))
            recent = [row["sent_at"] for row in conn.execute("SELECT sent_at FROM verification_challenges WHERE user_id = ? AND sent_at > ? "
                                                             "ORDER BY sent_at", (user_id, day_ago))]
            if len(recent) >= MAX_CODES_PER_DAY:  # refused before the open code is touched: it stays usable
                again = format_instant(parse_instant(recent[0]) + timedelta(hours=24))
                return {"error": f"{MAX_CODES_PER_DAY} codes were sent to this account in the last 24 hours, which is the limit; no code is sent "
                                 f"and none can be until {again}. A code already sent stays valid for its {CODE_TTL_MINUTES} minutes; "
                                 "otherwise the customer must call Kestrel"}
            if open_code:
                conn.execute("UPDATE verification_challenges SET status = 'cancelled', closed_at = ? WHERE challenge_id = ?",
                             (instant, open_code["challenge_id"]))
            channel, destination = conn.execute("SELECT otp_channel, otp_destination FROM customers WHERE user_id = ?", (user_id,)).fetchone()
            # six digits that never start with zero: a code is then the same six digits wherever it is handled as a number
            # (a model's JSON argument, a msgpack integer), where "039074" would be 39074 and no reader would know it
            code, salt = str(100_000 + secrets.randbelow(900_000)), secrets.token_hex(8)
            expires_at = format_instant(parse_instant(instant) + timedelta(minutes=CODE_TTL_MINUTES))
            try:
                conn.execute("INSERT INTO verification_challenges (challenge_id, user_id, session_id, code_hash, salt, channel, destination,"
                             " sent_at, expires_at, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'open')",
                             (f"V-{uuid.uuid4().hex[:8]}", user_id, session_id, _code_hash(code, salt), salt, channel, destination, instant, expires_at))
            except sqlite3.IntegrityError:
                return {"error": "a code was just sent; ask the customer to enter it", "sent_to": masked_destination(channel, destination)}
            body = (f"Your Kestrel verification code is {code}. It expires in {CODE_TTL_MINUTES} minutes. Kestrel will never ask you to share it.")
            conn.execute("INSERT INTO outbound_messages (user_id, channel, body, followup_id, status, drafted_at, sent_at, destination, purpose)"
                         " VALUES (?, ?, ?, NULL, 'sent', ?, ?, ?, 'one_time_code')", (user_id, channel, body, instant, instant, destination))
            return {"sent": True, "sent_to": masked_destination(channel, destination), "expires_in_minutes": CODE_TTL_MINUTES, "resent": bool(open_code)}
        finally:
            conn.execute("COMMIT")


def attempt_code(db_path: Path, user_id: str, entered: str, now: str, max_failures: int, session_id: str | None = None,
                 repeat_of_lost_call: bool = False) -> dict:
    """Check an entered code, in one transaction: refuse while locked; no open code, or an expired one, is not a guess;
    a wrong code is a failed attempt on the account and on the code; a match consumes the code and records a success.
    With `repeat_of_lost_call` (the conversation was just told a result was lost, and the call is made again): the code
    this conversation consumed within the last VERIFICATION_TTL_MINUTES is the same proof and matches again; the same
    wrong code within REPEAT_WINDOW_SECONDS is the same mistake and is not counted again. Without it a code is
    single-use and every wrong entry counts."""
    instant = format_instant(parse_instant(now))
    digits = re.sub(r"\D", "", entered or "")
    with closing(_connect(db_path, autocommit=True)) as conn:
        conn.execute("BEGIN IMMEDIATE")
        try:
            latest = conn.execute("SELECT * FROM verification_challenges WHERE user_id = ? ORDER BY sent_at DESC, challenge_id DESC LIMIT 1",
                                  (user_id,)).fetchone()
            if repeat_of_lost_call and latest is not None and len(digits) == 6 and session_id:
                if latest["status"] == "consumed" and latest["consumed_in"] == session_id and latest["closed_at"] \
                        and (parse_instant(now) - parse_instant(latest["closed_at"])).total_seconds() <= VERIFICATION_TTL_MINUTES * 60 \
                        and _code_hash(digits, latest["salt"]) == latest["code_hash"]:
                    return {"outcome": "matched", "code": digits, "repeat": True}
                repeat = _repeat_of(conn, user_id, "code", _guess_hash(latest["challenge_id"], digits), session_id, now)
                if repeat is not None and not repeat["succeeded"]:
                    return {"outcome": "mismatch", "failures": _failures(conn, user_id, now), "repeat": True,
                            "entries_left": max(0, CODE_MAX_ENTRIES - latest["attempts"]), "code_dead": latest["status"] == "failed"}
            failures = _failures(conn, user_id, now)
            if failures >= max_failures:
                return {"outcome": "locked", "failures": failures}
            open_code = conn.execute("SELECT * FROM verification_challenges WHERE user_id = ? AND status = 'open'", (user_id,)).fetchone()
            if not open_code:
                return {"outcome": "no_open_code"}
            if parse_instant(instant) >= parse_instant(open_code["expires_at"]):
                conn.execute("UPDATE verification_challenges SET status = 'expired', closed_at = ? WHERE challenge_id = ?", (instant, open_code["challenge_id"]))
                return {"outcome": "expired", "sent_to": masked_destination(open_code["channel"], open_code["destination"])}
            if len(digits) != 6:
                return {"outcome": "no_code_entered"}
            if _code_hash(digits, open_code["salt"]) == open_code["code_hash"]:
                conn.execute("UPDATE verification_challenges SET status = 'consumed', closed_at = ?, attempts = attempts + 1, consumed_in = ? "
                             "WHERE challenge_id = ?", (instant, session_id, open_code["challenge_id"]))
                conn.execute("INSERT INTO verification_attempts (user_id, at, succeeded, kind, session_id, guess_hash) VALUES (?, ?, 1, 'code', ?, ?)",
                             (user_id, instant, session_id, _guess_hash(open_code["challenge_id"], digits)))
                return {"outcome": "matched", "code": digits}
            attempts = open_code["attempts"] + 1
            dead = attempts >= CODE_MAX_ENTRIES
            conn.execute("UPDATE verification_challenges SET attempts = ?, status = ?, closed_at = ? WHERE challenge_id = ?",
                         (attempts, "failed" if dead else "open", instant if dead else None, open_code["challenge_id"]))
            conn.execute("INSERT INTO verification_attempts (user_id, at, succeeded, kind, session_id, guess_hash) VALUES (?, ?, 0, 'code', ?, ?)",
                         (user_id, instant, session_id, _guess_hash(open_code["challenge_id"], digits)))
            return {"outcome": "mismatch", "failures": failures + 1, "entries_left": 0 if dead else CODE_MAX_ENTRIES - attempts, "code_dead": dead,
                    "account_locked": failures + 1 >= max_failures}
        finally:
            conn.execute("COMMIT")


def cancel_open_codes(db_path: Path, user_id: str, now: str) -> int:
    with closing(_connect(db_path)) as conn, conn:
        return conn.execute("UPDATE verification_challenges SET status = 'cancelled', closed_at = ? WHERE user_id = ? AND status = 'open'",
                            (format_instant(parse_instant(now)), user_id)).rowcount


def retire_code_messages(db_path: Path, now: str) -> int:
    """Maintenance: the outbox keeps a code's text only while the code can be used; afterwards the body says the code expired."""
    cutoff = format_instant(parse_instant(now) - timedelta(minutes=CODE_TTL_MINUTES))
    with closing(_connect(db_path)) as conn, conn:
        return conn.execute("UPDATE outbound_messages SET body = 'Your Kestrel verification code [expired]. Kestrel will never ask you to share it.'"
                            " WHERE purpose = 'one_time_code' AND drafted_at <= ? AND body NOT LIKE '%[expired]%'", (cutoff,)).rowcount


def open_code_status(db_path: Path, user_id: str, now: str) -> dict | None:
    """The customer's latest one-time code as the bank sees it, for the system prompt: when it was sent, where, whether
    it can still be entered. The model is told this from the record, not from its own memory of the conversation (a
    round-5 dev run had the agent deny, seven minutes later, that it had sent a code its own history showed)."""
    with closing(_connect(db_path)) as conn:
        if "verification_challenges" not in {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}:
            return None
        row = conn.execute("SELECT channel, destination, sent_at, expires_at, status, closed_at, consumed_in FROM verification_challenges "
                           "WHERE user_id = ? ORDER BY sent_at DESC, challenge_id DESC LIMIT 1", (user_id,)).fetchone()
    if not row:
        return None
    status = row["status"]
    if status == "open" and parse_instant(row["expires_at"]) <= parse_instant(now):
        status = "expired"
    return {"sent_at": row["sent_at"], "expires_at": row["expires_at"], "sent_to": masked_destination(row["channel"], row["destination"]),
            "status": status, "closed_at": row["closed_at"], "consumed_in": row["consumed_in"]}


def possession_proved_at(db_path: Path, user_id: str, session_id: str, now: str) -> str | None:
    """When this conversation entered the right code, if it did within the last VERIFICATION_TTL_MINUTES: the bank's
    record of the possession proof. The session keeps a copy (`possession_verified_at`); a process that died after the
    code was consumed and before the tool's result was recorded (the round-5 lost-result probe) loses the copy, and
    the next turn rebuilds it from here."""
    code = open_code_status(db_path, user_id, now)
    if not code or code["status"] != "consumed" or code["consumed_in"] != session_id or not code["closed_at"]:
        return None
    if (parse_instant(now) - parse_instant(code["closed_at"])).total_seconds() > VERIFICATION_TTL_MINUTES * 60:
        return None
    return code["closed_at"]


_CODE_SEPARATOR = r"[ \u00a0.\-]"
_NUMBER_WORDS = {"zero": "0", "oh": "0", "one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8",
                 "nine": "9"}
# six digits the way a code is typed: together, as two threes, as three pairs, or one at a time, one separator between
# groups; never part of a longer run of digits ("+1 415 555 0100", "5555 5555 5555 4444" and "1,234,567" hold none)
_CODE_SPAN = re.compile(
    rf"(?<!\d)(?<!\d{_CODE_SEPARATOR})(?:\d{{6}}|\d{{3}}{_CODE_SEPARATOR}\d{{3}}|\d{{2}}{_CODE_SEPARATOR}\d{{2}}{_CODE_SEPARATOR}\d{{2}}"
    rf"|\d(?:{_CODE_SEPARATOR}\d){{5}})(?!\d)(?!{_CODE_SEPARATOR}\d)")
_SPOKEN_DIGITS = re.compile(r"\b(?:" + "|".join(_NUMBER_WORDS) + r")\b(?:[\s,\-]+(?:" + "|".join(_NUMBER_WORDS) + r")\b)*", re.IGNORECASE)


def code_spans(text: str) -> list[tuple[int, int, str]]:
    """Every place in `text` where a one-time code may have been typed, as (start, end, its six digits). This is the one
    definition of "a typed code": the bank checks what it finds, the harness removes what it finds, and nothing else is
    ever compared with a code. Round 5 had two definitions (the check stripped every non-digit, the redaction looked for
    six contiguous digits), so "481 975" was accepted and kept."""
    spans = [(m.start(), m.end(), re.sub(r"\D", "", m.group())) for m in _CODE_SPAN.finditer(text)]
    for m in _SPOKEN_DIGITS.finditer(text):
        words = re.findall(r"[A-Za-z]+", m.group())
        if len(words) == 6:
            spans.append((m.start(), m.end(), "".join(_NUMBER_WORDS[w.lower()] for w in words)))
    return sorted(spans)


def _without(text: str, spans: list[tuple[int, int, str]]) -> str:
    for start, end, _ in sorted(spans, reverse=True):
        text = text[:start] + ONE_TIME_CODE_MASK + text[end:]
    return text


def take_code_entry(db_path: Path, user_id: str, session_id: str, text: str, now: str, max_failures: int,
                    repeat_of_lost_call: bool = False) -> dict:
    """The door every customer message passes before the model reads it or anything stores it. Returns the text to keep
    and what the bank made of it: {"text", "entry"}.

    While the bank holds an open code for this customer, every code-shaped span is replaced by the marker, in any of
    their conversations, match or not: what the customer can read never tells the code from another six-digit number.
    Round 5 replaced a span only when it hash-matched an issued code and did so in the reply, which made the marker a
    yes/no test of "is this the code" outside the attempt counter (the round-5 review's list echo: 300 candidates a
    message, no failure recorded). The only comparison is the entry: in the conversation the code was sent from, a
    message with exactly one span is checked once by attempt_code, counted like any attempt. No span is not an entry.
    Two or more are not compared at all.

    With no code open, six digits are just six digits, except the customer's own dead codes, which are removed by salted
    hash (a dead code is worth nothing, so saying which number it was gives nothing away). The same hash search runs
    over what the shape rule leaves: a code of theirs written in a form the bank does not take is removed, and if it is
    the open code, that code is cancelled first (outcome "written_unusably")."""
    spans = code_spans(text)
    with closing(_connect(db_path)) as conn:
        if "verification_challenges" not in {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}:
            return {"text": text, "entry": None}
        open_code = conn.execute("SELECT session_id, expires_at FROM verification_challenges WHERE user_id = ? AND status = 'open'",
                                 (user_id,)).fetchone()
        issued = conn.execute("SELECT code_hash, salt FROM verification_challenges WHERE user_id = ?", (user_id,)).fetchall()
    usable = open_code is not None and parse_instant(now) < parse_instant(open_code["expires_at"])
    if open_code is None or (not usable and open_code["session_id"] != session_id):
        # Nothing can be entered: six digits are six digits again, five minutes after the send at the latest. A code past
        # its five minutes that nobody has typed since is still marked open; it is as dead as a used one.
        return {"text": _marked(text, codes_exposed_in(db_path, user_id, text, now)), "entry": None}
    kept = _without(text, spans)  # by shape: every form the bank takes, whether or not it is the code
    # By hash, in what is left: one of the customer's own codes in a form the bank does not take ("481,975", "4819 75").
    # It is not an entry and not something to keep. If it is the open code, that code is cancelled before anything is
    # said: it has been written into a conversation, and a match is never an answer about a code that can still be used.
    kept = _marked(kept, codes_exposed_in(db_path, user_id, kept, now))
    if not _has_open_code(db_path, user_id):
        return {"text": kept, "entry": {"outcome": "written_unusably"}}
    if open_code["session_id"] != session_id:
        return {"text": kept, "entry": {"outcome": "other_conversation"} if spans else None}
    if not usable and len(spans) != 1:
        # This conversation's code has run out and the message is not an entry for it: the code is closed here, so that
        # nothing waits for it and the model is told it expired. (A single span still goes to attempt_code, which answers
        # "expired" and closes it.) Before, the tool result said "the code already sent stays valid"; asked for a new code
        # six minutes after the send, LangGraph sent none and said one had gone out (round 6's second final pass).
        with closing(_connect(db_path)) as conn, conn:
            conn.execute("UPDATE verification_challenges SET status = 'expired', closed_at = ? WHERE user_id = ? AND status = 'open'",
                         (format_instant(parse_instant(now)), user_id))
        return {"text": kept, "entry": {"outcome": "several_numbers" if spans else "no_code_entered", "code_expired": True}}
    if not spans:
        return {"text": kept, "entry": {"outcome": "no_code_entered"}}
    if len(spans) > 1:
        return {"text": kept, "entry": {"outcome": "several_numbers"}}
    attempt = attempt_code(db_path, user_id, spans[0][2], now, max_failures, session_id=session_id, repeat_of_lost_call=repeat_of_lost_call)
    return {"text": kept, "entry": {key: value for key, value in attempt.items() if key != "code"}}


def _marked(text: str, renderings: list[str]) -> str:
    for rendering in sorted(renderings, key=len, reverse=True):
        text = text.replace(rendering, ONE_TIME_CODE_MASK)
    return text


def _has_open_code(db_path: Path, user_id: str) -> bool:
    with closing(_connect(db_path)) as conn:
        return conn.execute("SELECT 1 FROM verification_challenges WHERE user_id = ? AND status = 'open'", (user_id,)).fetchone() is not None


def open_code_sent_at(db_path: Path, user_id: str, session_id: str) -> str | None:
    """When the customer's open code was sent, if it was sent from this conversation: only then is there anything to
    wait for here (None otherwise)."""
    with closing(_connect(db_path)) as conn:
        row = conn.execute("SELECT session_id, sent_at FROM verification_challenges WHERE user_id = ? AND status = 'open'", (user_id,)).fetchone()
    return row["sent_at"] if row and row["session_id"] == session_id else None


def waits_for_an_entry(db_path: Path, user_id: str, session_id: str, entry: dict | None, now: str) -> bool:
    """Whether confirm_verification_code should pause for the customer's next message: a code sent from this conversation
    is open, and this turn's message was not an entry for it (it held no code, or the code was sent during this turn,
    after the message was read: "that one expired, send another" is answered with a new code and a new wait)."""
    sent_at = open_code_sent_at(db_path, user_id, session_id)
    return sent_at is not None and ((entry or {}).get("outcome") in (None, "no_code_entered") or parse_instant(sent_at) >= parse_instant(now))


def attempt_went_unanswered(db_path: Path, user_id: str, session_id: str, recorded_through: str | None) -> bool:
    """Whether the bank holds a code attempt from this conversation that is newer than anything the conversation itself
    recorded: the door checked an entry and the process stopped before the turn was stored, so the customer never saw
    an answer. Only then is the same entry typed again the lost one repeated (attempt_code's `repeat_of_lost_call`)."""
    with closing(_connect(db_path)) as conn:
        row = conn.execute("SELECT at FROM verification_attempts WHERE user_id = ? AND session_id = ? AND kind = 'code' ORDER BY rowid DESC LIMIT 1",
                           (user_id, session_id)).fetchone()
    return bool(row) and (recorded_through is None or parse_instant(row["at"]) > parse_instant(recorded_through))


# Six digits in order with up to two characters that are neither digits nor letters between any two of them, not
# touching a digit or a letter: every way a code can sit in text, the forms the door takes and the ones it does not
# ("481,975", "4819 75"). Dates, clock times and ids are blanked first: they are never a code.
_SIX_DIGITS_ANYHOW = re.compile(r"(?<![0-9A-Za-z])(?=(\d(?:[^0-9A-Za-z]{0,2}\d){5})(?![0-9A-Za-z]))")
_DATE_TIME_OR_ID = re.compile(r"\d{4}-\d{2}-\d{2}(?:[T ]\d{2}:\d{2}(?::\d{2}(?:\.\d+)?)?)?(?:Z|[+-]\d{2}:\d{2})?"
                              r"|[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")


def codes_exposed_in(db_path: Path, user_id: str, text: str, now: str) -> list[str]:
    """Defence in depth for what did not come through the door as an entry: a code the customer wrote in a form the bank
    does not take ("481,975"), and a model's own output (a reply, a tool-call argument, as text or as a number). `text`
    is searched for this customer's codes, by salted hash, in every rendering the evidence check can read. If it holds
    one, the open code is cancelled on the spot: it has been written into a conversation, so it is burnt, and saying
    which number it was is then worth nothing (a match is never an answer about a code that can still be used). Every
    matching rendering is returned for the caller to rewrite."""
    readable = _DATE_TIME_OR_ID.sub(lambda m: "#" * len(m.group()), text)
    candidates = {m.group(1): re.sub(r"\D", "", m.group(1)) for m in _SIX_DIGITS_ANYHOW.finditer(readable)}
    candidates.update({text[start:end]: digits for start, end, digits in code_spans(text)})  # number words too
    if not candidates:
        return []
    with closing(_connect(db_path)) as conn, conn:
        if "verification_challenges" not in {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}:
            return []
        rows = conn.execute("SELECT challenge_id, code_hash, salt, status FROM verification_challenges WHERE user_id = ?", (user_id,)).fetchall()
        found = []
        for rendering, digits in candidates.items():
            matches = [row for row in rows if _code_hash(digits, row["salt"]) == row["code_hash"]]
            if matches:
                found.append(rendering)
                for row in matches:
                    if row["status"] == "open":
                        conn.execute("UPDATE verification_challenges SET status = 'cancelled', closed_at = ? WHERE challenge_id = ?",
                                     (format_instant(parse_instant(now)), row["challenge_id"]))
    return found


def list_challenges(db_path: Path) -> list[dict]:
    with closing(_connect(db_path)) as conn:
        if "verification_challenges" not in {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}:
            return []
        return [{k: row[k] for k in row.keys() if k not in ("code_hash", "salt")} for row in
                conn.execute("SELECT * FROM verification_challenges ORDER BY sent_at, challenge_id")]


def verification_attempt_rows(db_path: Path) -> list[dict]:
    with closing(_connect(db_path)) as conn:
        return [dict(row) for row in conn.execute("SELECT rowid AS id, user_id, at, succeeded, kind FROM verification_attempts ORDER BY rowid")]


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
    overwrite each other's notes. The same line attached again (a call repeated after its result was lost) is already
    there and is not appended twice."""
    line = f"[{now[:10]}] {evidence_note}"
    with closing(_connect(db_path)) as conn, conn:
        current = conn.execute("SELECT * FROM cases WHERE case_id = ? AND user_id = ?", (case_id, user_id)).fetchone()
        if current and current["status"] == "under_review" and line in (current["evidence_note"] or "").split("\n"):
            return {**_case_view(current), "already_attached": True}
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
