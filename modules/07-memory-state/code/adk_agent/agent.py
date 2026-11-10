"""Kestrel card-care assistant on Google ADK: where each of the module's seven memory types lives.

  working / in-context  Session events (DatabaseSessionService on SQLite), re-sent every turn up to a
                        window of WORKING_WINDOW_TURNS customer turns (each message capped in size), plus State:
                          identity_verified_at, first_active_at, last_active_at, reflected_turns,
                          episodes_written   this conversation only
                          user:contact_channel, user:travel_notice   this customer, every session
                          app:dispute_review_days, app:large_dispute_threshold_cents   every customer
                          temp:now   the harness clock for this invocation; never persisted
  semantic              the user: keys above: a closed schema with a value grammar, timestamped, overwritten by
                        key, preloaded into the instruction every turn (small and always relevant)
  episodic              EpisodeMemoryService: reflections on finished (or windowed-out) turns, recalled
                        on demand with ADK's load_memory tool (large and mostly irrelevant)
  procedural            the versioned instruction (cardcare/procedure_versions + the registry in var/)
  external / retrieval  tools: exact SQL lookups for transactions and cases; search_policy (embeddings)
  parametric            the DeepSeek weights; nothing here manages them, which is the point
  prospective           cardcare/scheduler.py: file_dispute and schedule_reminder write records, the
                        customer can list and cancel their own, the harness fires them (`tick`) into
                        sessions that get only read tools and notify_customer
Account-level state (the verification lockout, the erasure generations) lives outside every session, in bank.db
and privacy.db, so no conversation boundary resets it. What kind of session a turn runs in (live, or a follow-up
the scheduler started) is passed in by whoever starts it (cardcare/sessions.py) and never read back from state.

Run `python -m adk_agent.agent chat --user priya` from modules/07-memory-state/code.
"""

import argparse
import asyncio
import contextvars
import json
import re
import sqlite3
import time
import uuid
from collections.abc import Callable
from contextlib import closing
from pathlib import Path
from typing import NamedTuple

import litellm
from google.adk.agents.callback_context import CallbackContext
from google.adk.agents.llm_agent import Agent
from google.adk.agents.readonly_context import ReadonlyContext
from google.adk.events import Event, EventActions
from google.adk.memory import BaseMemoryService
from google.adk.memory.base_memory_service import SearchMemoryResponse
from google.adk.memory.memory_entry import MemoryEntry
from google.adk.models import LiteLlm
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService, InMemorySessionService
from google.adk.tools import FunctionTool, ToolContext, load_memory
from google.genai import types

from cardcare import desk, privacy, procedures, scheduler, world
from cardcare.clock import parse_instant, wall_clock_now
from cardcare.episodes import build_episode, case_outcomes, group_by_customer_turn, own_case_ids, parse_reflection, reflection_prompt
from cardcare.masking import MASK_TOKEN, mask_card_numbers, mask_customer_message, mask_customer_text, removed_fragments, scrub_fragments
from cardcare.memory_policy import (
    DEFAULT_CHANNEL,
    VERIFICATION_TTL_MINUTES,
    FACT_KEYS,
    FACT_KEYS_NEEDING_VERIFICATION,
    MAX_CUSTOMER_MESSAGE_CHARS,
    MAX_VERIFICATION_ATTEMPTS,
    TRANSCRIPT_RETENTION_DAYS,
    VERIFICATION_LOCK_HOURS,
    WORKING_KEEP_TURNS,
    WORKING_WINDOW_TURNS,
    build_fact,
    episode_is_expired,
    fact_is_expired,
    possession_gate_error,
    render_profile,
    render_stepup_status,
    session_is_idle,
    transcript_is_expired,
    typed_in_session,
    verification_gate_error,
)
from cardcare.model_config import DEEPSEEK_MODEL, deepseek_api_key
from cardcare.retrieval import embed_texts, search_policy as search_policy_documents, top_matches
from cardcare.sessions import LIVE, SessionKind, followup_kind
from cardcare.tool_args import (
    CardLast4, CaseId, CustomerMessage, DisputeReason, EnteredCode, EvidenceNote, FactKey, FactValue, FollowupId, MalformedTool, MemoryQuery,
    Merchant, NewEvidence, OptionalCaseId, PolicyQuestion, PostalCode, RemindAt, ReminderNote, RemindOn, TimeZone, TransactionId,
    ValidUntil,
)

APP_NAME = "kestrel_card_care"
AGENT_NAME = "card_care"
APP_SETTINGS = {"app:dispute_review_days": 10, "app:large_dispute_threshold_cents": 20000}
OPS_USER = "ops"
CODE_DIR = Path(__file__).resolve().parent.parent
# The harness clock for the running turn, so a memory read (load_memory) can leave out what has expired even if
# maintenance has not run yet. A context variable: concurrent turns do not see each other's clock.
CLOCK: contextvars.ContextVar[str | None] = contextvars.ContextVar("cardcare_now", default=None)
_HELPER_SESSION = re.compile(r"^(facts|erasure)-[0-9a-f]{8}$")


# --------------------------------------------------------------------------- episodic memory


class EpisodeMemoryService(BaseMemoryService):
    """ADK long-term episodic memory: reflections on a customer's conversations, scoped by (app, user).

    ADK 2.13 ships a SqliteMemoryService, but it indexes raw session events with keyword
    (FTS5) search and has no delete_memory. The module's write path needs reflections in,
    paraphrase-tolerant recall out, and a way to forget, so this implements the same
    BaseMemoryService interface on SQLite with local embeddings.
    """

    def __init__(self, db_path: Path):
        self.db_path = db_path
        db_path.parent.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(db_path)) as conn, conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS episodes (memory_id TEXT PRIMARY KEY, app_name TEXT NOT NULL,"
                " user_id TEXT NOT NULL, at TEXT NOT NULL, text TEXT NOT NULL, embedding TEXT NOT NULL,"
                " episode_json TEXT NOT NULL)"
            )

    async def add_session_to_memory(self, session) -> None:
        raise NotImplementedError(
            "Raw sessions are never copied into long-term memory; the harness writes reflections with add_memory()."
        )

    async def add_memory(self, *, app_name: str, user_id: str, memories, custom_metadata=None) -> None:
        rows = []
        for memory in memories:
            text = "".join(part.text or "" for part in memory.content.parts)
            rows.append((memory.id, app_name, user_id, memory.timestamp, text, json.dumps(embed_texts([text])[0]),
                         json.dumps(memory.custom_metadata["episode"])))
        with closing(sqlite3.connect(self.db_path)) as conn, conn:
            conn.executemany("INSERT INTO episodes VALUES (?, ?, ?, ?, ?, ?, ?)", rows)  # an id is never reused or replaced

    async def search_memory(self, *, app_name: str, user_id: str, query: str) -> SearchMemoryResponse:
        # Scope first, expiry second, similarity third: another customer's episodes, and expired ones, are never scored.
        now = CLOCK.get()
        with closing(sqlite3.connect(self.db_path)) as conn:
            rows = [row for row in conn.execute(
                "SELECT memory_id, at, text, embedding, episode_json FROM episodes WHERE app_name = ? AND user_id = ?", (app_name, user_id))
                if not (now and episode_is_expired(json.loads(row[4]), now))]
        matches = top_matches(query, [json.loads(row[3]) for row in rows], limit=3)
        return SearchMemoryResponse(memories=[
            MemoryEntry(
                id=rows[index][0], author="reflection", timestamp=rows[index][1],
                content=types.Content(role="user", parts=[types.Part(text=rows[index][2])]),
                custom_metadata={"similarity": score},
            )
            for index, score in matches
        ])

    async def delete_memory(self, *, app_name: str, user_id: str, memory_id: str | None = None) -> None:
        with closing(sqlite3.connect(self.db_path)) as conn, conn:
            conn.execute("DELETE FROM episodes WHERE app_name = ? AND user_id = ? AND memory_id = ?", (app_name, user_id, memory_id))

    def list_episodes(self, app_name: str) -> list[dict]:
        with closing(sqlite3.connect(self.db_path)) as conn:
            rows = conn.execute("SELECT episode_json FROM episodes WHERE app_name = ? ORDER BY at", (app_name,)).fetchall()
        return [json.loads(row[0]) for row in rows]

    def rewrite_user_texts(self, app_name: str, user_id: str, fix: Callable[[str], str]) -> int:
        """Apply `fix` to every stored episode of this customer (a card number completed later is scrubbed here too)."""
        changed = 0
        with closing(sqlite3.connect(self.db_path)) as conn, conn:
            for memory_id, text, episode_json in conn.execute(
                    "SELECT memory_id, text, episode_json FROM episodes WHERE app_name = ? AND user_id = ?", (app_name, user_id)).fetchall():
                new_text, new_json = fix(text), json.dumps(_map_strings(json.loads(episode_json), fix))
                if new_text != text or new_json != episode_json:
                    conn.execute("UPDATE episodes SET text = ?, episode_json = ?, embedding = ? WHERE memory_id = ?",
                                 (new_text, new_json, json.dumps(embed_texts([new_text])[0]), memory_id))
                    changed += 1
        return changed


def _map_strings(value, fix: Callable[[str], str]):
    if isinstance(value, str):
        return fix(value)
    if isinstance(value, list):
        return [_map_strings(v, fix) for v in value]
    if isinstance(value, dict):
        return {k: _map_strings(v, fix) for k, v in value.items()}
    return value


# --------------------------------------------------------------------------- harness


class Harness(NamedTuple):
    var_dir: Path
    session_service: DatabaseSessionService
    memory_service: EpisodeMemoryService

    @property
    def bank_db(self) -> Path:
        return self.var_dir / "bank.db"

    @property
    def scheduler_db(self) -> Path:
        return self.var_dir / "scheduler.db"

    @property
    def sessions_db(self) -> Path:
        return self.var_dir / "adk_sessions.db"

    @property
    def episodes_db(self) -> Path:
        return self.var_dir / "adk_episodes.db"

    @property
    def privacy_db(self) -> Path:
        return self.var_dir / "privacy.db"


async def open_harness(var_dir: Path) -> Harness:
    """Create (or reopen) every local store under var_dir and seed the bank and the app-wide settings."""
    var_dir.mkdir(parents=True, exist_ok=True)
    world.seed_bank(var_dir / "bank.db")
    scheduler.create_scheduler(var_dir / "scheduler.db")
    privacy.create_ledger(var_dir / "privacy.db")
    harness = Harness(
        var_dir,
        DatabaseSessionService(db_url=f"sqlite+aiosqlite:///{var_dir / 'adk_sessions.db'}"),
        EpisodeMemoryService(var_dir / "adk_episodes.db"),
    )
    await seed_app_settings(harness)
    return harness


async def seed_app_settings(h: Harness) -> None:
    """app: state can only change through an event, so ops writes it as an EventActions.state_delta."""
    ops_session = await h.session_service.get_session(app_name=APP_NAME, user_id=OPS_USER, session_id="ops-settings")
    if ops_session and all(key in ops_session.state for key in APP_SETTINGS):
        return
    ops_session = ops_session or await h.session_service.create_session(app_name=APP_NAME, user_id=OPS_USER, session_id="ops-settings")
    event = Event(invocation_id=f"ops-{uuid.uuid4().hex[:8]}", author=OPS_USER, actions=EventActions(state_delta=dict(APP_SETTINGS)))
    await h.session_service.append_event(ops_session, event)


async def write_session_state(h: Harness, user_id: str, session_id: str, delta: dict) -> None:
    """Harness-side state writes go through an event too (the documented manual path), never session.state[...]."""
    session = await h.session_service.get_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)
    if session is None:
        return
    event = Event(invocation_id=f"harness-{uuid.uuid4().hex[:8]}", author="harness", actions=EventActions(state_delta=delta))
    await h.session_service.append_event(session, event)


async def user_facts(h: Harness, user_id: str) -> dict:
    return {key: value for key, value in (await h.session_service.get_user_state(app_name=APP_NAME, user_id=user_id)).items() if value}


async def write_user_facts(h: Harness, user_id: str, delta: dict) -> None:
    """user: state changes from outside a running turn (erasure, maintenance): an event on a throwaway session, then deleted."""
    writer = await h.session_service.create_session(app_name=APP_NAME, user_id=user_id, session_id=f"facts-{uuid.uuid4().hex[:8]}")
    await h.session_service.append_event(writer, Event(invocation_id=f"facts-{uuid.uuid4().hex[:8]}", author="harness",
                                                       actions=EventActions(state_delta={f"user:{k}": v for k, v in delta.items()})))
    await h.session_service.delete_session(app_name=APP_NAME, user_id=user_id, session_id=writer.id)


def compact_sqlite(path: Path) -> None:
    """Deleted rows linger in free pages and in the WAL until the file is rewritten; erasure has to reach those too.

    VACUUM first (in WAL mode it writes the rebuilt pages to the WAL), then checkpoint them into the main file
    and truncate the WAL, so neither file still holds the deleted bytes.
    """
    with closing(sqlite3.connect(path, timeout=60)) as conn:
        conn.execute("VACUUM")
        conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")


def _customer_texts(events: list[Event]) -> list[str]:
    return [part.text for event in events if event.author == "user" for part in ((event.content.parts if event.content else None) or [])
            if part.text and not part.function_response]


# --------------------------------------------------------------------------- tools


# Tools only a LIVE conversation gets, one where the customer is in the chat and typing. They act for the customer
# (verify their identity, file a dispute, change or delete what is remembered, set or cancel a reminder, erase
# everything), so they need the customer there to ask for it. An unattended session never gets them: it reads text
# other people wrote (back-office case notes, the customer's own reminder note), and an instruction hidden in that
# text ("call request_memory_erasure") must find nothing to call.
# send_verification_code and confirm_verification_code are live-only too: they text a one-time code to the number the bank
# holds and then WAIT for the customer to type it, and nobody is there to type it in a scheduler session.
LIVE_ONLY_TOOLS = ("verify_identity", "file_dispute", "add_case_evidence", "remember_customer_fact", "forget_customer_fact",
                   "schedule_reminder", "cancel_reminder", "request_memory_erasure", "send_verification_code", "confirm_verification_code")
CONFIRMATION_CALL = "adk_request_confirmation"  # ADK's own function call that pauses a turn for the customer's input
ONE_TIME_CODE_MASK = "[REDACTED ONE-TIME CODE]"
# Tools only an UNATTENDED session gets: one the scheduler starts when a follow-up or reminder falls due, with no
# customer present. notify_customer is how that session reaches the customer (one message per follow-up). A live
# conversation never gets it, because there the agent simply replies in the chat. A session is unattended only when
# the scheduler starts it for a follow-up record and says so in the SessionKind it passes in (cardcare/sessions.py,
# built by run_followup_session from the record); nothing stored in the session can change that.
UNATTENDED_ONLY_TOOLS = ("notify_customer",)
ERASED_IN_THIS_CONVERSATION = ("the customer asked for erasure in this conversation (or an erasure has run since it started), so "
                               "nothing more can be stored for them here; tell them to set it up again in a new conversation")


def build_tools(h: Harness, kind: SessionKind = LIVE) -> list[Callable]:
    """Tool functions over this harness's stores. The customer is always tool_context.user_id, never a model argument.

    Least privilege by session kind, which comes from the job that started the session (`kind`), never from state:
    a scheduler-fired session reads text others wrote (case notes, reminder notes), so it gets only reads and
    notify_customer; a live session never gets notify_customer.
    """

    def verify_identity(card_last4: CardLast4, postal_code: PostalCode, tool_context: ToolContext) -> dict:
        """Verify the logged-in customer with their card's last 4 digits and billing ZIP, exactly as the customer typed
        them in this conversation (if they already did, use those). Valid for 15 minutes. Three failures lock
        verification on the account for 24 hours."""
        now = tool_context.state["temp:now"]
        if not typed_in_session(_customer_texts(tool_context.session.events), card_last4, postal_code,
                                turn_times=tool_context.state.get("turn_times"), now=now):
            return {"verified": False, "error": "verify_identity accepts only the last 4 digits and ZIP the customer typed in this "
                                                "conversation in the last 15 minutes; ask the customer for them (nothing was counted "
                                                "against the account)"}
        attempt = world.attempt_verification(h.bank_db, tool_context.user_id, card_last4, postal_code, now, MAX_VERIFICATION_ATTEMPTS,
                                             session_id=tool_context.session.id,
                                             repeat_of_lost_call=world.lost_result_is_recent(tool_context.state.get("lost_result_at"), now))
        if attempt["outcome"] == "locked":
            return {"verified": False, "error": f"verification is locked on this account for {VERIFICATION_LOCK_HOURS} hours after "
                                                f"{MAX_VERIFICATION_ATTEMPTS} failed attempts; the customer must call Kestrel"}
        if attempt["outcome"] == "mismatch":
            return {"verified": False, "error": "those details do not match this customer",
                    "attempts_left": max(0, MAX_VERIFICATION_ATTEMPTS - attempt["failures"])}
        tool_context.state["identity_verified_at"] = now
        return {"verified": True, "valid_for_minutes": 15}

    def find_transactions(tool_context: ToolContext, merchant: Merchant = None) -> dict:
        """List the customer's posted transactions, optionally only those whose merchant name contains `merchant`."""
        return {"transactions": world.find_transactions(h.bank_db, tool_context.user_id, merchant, tool_context.state["temp:now"])}

    def _channel(tool_context: ToolContext) -> tuple[str, bool]:
        fact = tool_context.state.get("user:contact_channel") or {}
        return fact.get("value", DEFAULT_CHANNEL), bool(fact)

    def _generation(tool_context: ToolContext) -> int:
        record = privacy.session_record(h.privacy_db, tool_context.user_id, tool_context.session.id)
        return record["generation"] if record else -1

    def _lock_error(tool_context: ToolContext) -> str | None:
        """The account's lock, asked at every action that needs a verification: a verification obtained in the same model
        response as the lock (the right guess first in a parallel batch) is worth nothing once the lock is on."""
        if world.verification_locked(h.bank_db, tool_context.user_id, tool_context.state["temp:now"]):
            return (f"verification is locked on this account for {VERIFICATION_LOCK_HOURS} hours after {MAX_VERIFICATION_ATTEMPTS} failed "
                    "attempts: nothing that needs verification can be done, in any conversation, until then; the customer must call Kestrel")
        return None

    def file_dispute(transaction_id: TransactionId, reason: DisputeReason, tool_context: ToolContext, evidence_note: EvidenceNote = None) -> dict:
        """File a dispute for one transaction. Requires a verify_identity in the last 15 minutes. Schedules the case follow-up automatically, and
        the result says where it will reach the customer."""
        error = _lock_error(tool_context) or verification_gate_error(tool_context.state.get("identity_verified_at"), tool_context.state["temp:now"],
                                                                     "filing a dispute")
        if error:
            return {"error": error}
        channel, chosen = _channel(tool_context)
        return desk.file_dispute_with_followup(
            h.bank_db, h.scheduler_db, tool_context.user_id, transaction_id, reason, evidence_note,
            tool_context.state["temp:now"], tool_context.state["app:dispute_review_days"],
            tool_context.state["app:large_dispute_threshold_cents"], channel, chosen, _generation(tool_context),
        )

    def add_case_evidence(case_id: CaseId, evidence_note: NewEvidence, tool_context: ToolContext) -> dict:
        """Attach more evidence (e.g. a cancellation reference the customer found later) to one of their open cases."""
        return world.add_case_evidence(h.bank_db, tool_context.user_id, case_id, mask_customer_text(evidence_note), tool_context.state["temp:now"])

    def get_case_status(tool_context: ToolContext, case_id: OptionalCaseId = None) -> dict:
        """Current status of one dispute case, or of all this customer's cases when case_id is omitted."""
        return {"cases": world.list_cases(h.bank_db, tool_context.user_id, case_id)}

    def search_policy(question: PolicyQuestion) -> dict:
        """Search Kestrel's policy documents (fees, dispute rules, travel notices, contact channels)."""
        return {"documents": search_policy_documents(question)}

    def remember_customer_fact(key: FactKey, value: FactValue, tool_context: ToolContext, valid_until: ValidUntil = None) -> dict:
        """Store a fact the customer stated: their contact channel, or a travel notice. Replaces any earlier value of
        that fact. Changing the contact channel needs a verify_identity in the last 15 minutes."""
        if key in FACT_KEYS_NEEDING_VERIFICATION:  # knowledge (last four + ZIP) and possession (the one-time code), both fresh
            error = _lock_error(tool_context) or possession_gate_error(tool_context.state.get("identity_verified_at"),
                                                                       tool_context.state.get("possession_verified_at"),
                                                                       tool_context.state["temp:now"], f"changing {key}")
            if error:
                return {"error": error}
        try:
            fact = build_fact(key, value, valid_until, tool_context.state["temp:now"])
        except ValueError as exc:
            return {"error": str(exc)}
        with privacy.write_guard(h.privacy_db, tool_context.user_id, tool_context.session.id) as writable:
            if not writable:
                return {"error": ERASED_IN_THIS_CONVERSATION}
            previous = tool_context.state.get(f"user:{key}")
            tool_context.state[f"user:{key}"] = fact  # keyed overwrite: the new value replaces the old, never joins it
        return {"stored": {key: fact}, "replaced": previous["value"] if previous else None}

    def forget_customer_fact(key: FactKey, tool_context: ToolContext) -> dict:
        """Delete a stored customer fact (contact_channel or travel_notice) at the customer's request. Removing the
        contact channel needs a verify_identity in the last 15 minutes, like changing it."""
        if key not in FACT_KEYS:
            return {"error": f"unknown fact {key}"}
        if key in FACT_KEYS_NEEDING_VERIFICATION:
            error = _lock_error(tool_context) or possession_gate_error(tool_context.state.get("identity_verified_at"),
                                                                       tool_context.state.get("possession_verified_at"),
                                                                       tool_context.state["temp:now"], f"removing {key}")
            if error:
                return {"error": error}
        had_value = bool(tool_context.state.get(f"user:{key}"))
        tool_context.state[f"user:{key}"] = None
        return {"forgotten": key, "had_value": had_value,
                "note": f"deleted from memory now; conversation transcripts are deleted {TRANSCRIPT_RETENTION_DAYS} days after their "
                        "first message, or at once if the customer asks to erase everything"}

    def schedule_reminder(note: ReminderNote, remind_on: RemindOn, tool_context: ToolContext, remind_at: RemindAt = "09:00",
                          timezone: TimeZone = "UTC") -> dict:
        """Schedule a reminder to the customer, only when they ask for one, and at once. At most one reminder per day, at most 90 days ahead. The result says when, in the customer's
        time, and on which channel it will arrive."""
        channel, chosen = _channel(tool_context)
        with privacy.write_guard(h.privacy_db, tool_context.user_id, tool_context.session.id) as writable:
            if not writable:
                return {"error": ERASED_IN_THIS_CONVERSATION}
            return desk.schedule_customer_reminder(h.scheduler_db, tool_context.user_id, note, remind_on, remind_at, timezone,
                                                   tool_context.state["temp:now"], _generation(tool_context), channel, chosen)

    def list_my_followups(tool_context: ToolContext) -> dict:
        """What is scheduled for this customer (reminders and case follow-ups), when, and on which channel it will arrive."""
        channel, chosen = _channel(tool_context)
        records = [r for r in scheduler.user_followups(h.scheduler_db, tool_context.user_id) if r["status"] in ("pending", "awaiting_approval")]
        return {"scheduled": [scheduler.customer_view(r, channel, chosen) for r in records]}

    def cancel_reminder(followup_id: FollowupId, tool_context: ToolContext) -> dict:
        """Cancel one of the customer's own reminders before it is sent (ids come from list_my_followups)."""
        record = scheduler.get_followup(h.scheduler_db, followup_id)
        if not record or record["user_id"] != tool_context.user_id or record["action"] != "customer_reminder":
            return {"error": f"{followup_id} is not one of this customer's reminders"}
        cancelled = scheduler.cancel_followup(h.scheduler_db, followup_id, tool_context.user_id, tool_context.state["temp:now"])
        return {"cancelled": followup_id} if cancelled else {"error": f"{followup_id} has already been sent or cancelled"}

    async def request_memory_erasure(tool_context: ToolContext) -> dict:
        """The customer asks to delete everything remembered about them (being logged in is enough). Runs now: facts, conversation summaries, other conversations' transcripts and reminders are deleted at once; this
        conversation's transcript is deleted when it ends. Nothing more can be stored for them in this conversation."""
        now = tool_context.state["temp:now"]
        result = await erase_customer_memory(h, tool_context.user_id, now, requesting_session=tool_context.session.id)
        for key in FACT_KEYS:
            tool_context.state[f"user:{key}"] = None  # this invocation's copy, too
        return {"erased_now": f"{result['facts']} remembered facts, {result['episodes']} past-conversation summaries, "
                              f"{result['transcripts']} other conversation transcripts, {len(result['reminders_cancelled'])} reminders with "
                              "their notes",
                "this_conversation": "its transcript is deleted when the conversation ends, or once it has been idle for 30 minutes if "
                                     "the customer just closes the chat; nothing more can be stored for the customer in it (a new "
                                     "conversation afterwards starts fresh)",
                "kept": "dispute cases, transactions and messages already sent are bank records with their own legal retention"}

    def send_verification_code(tool_context: ToolContext) -> dict:
        """Send a one-time code to the mobile number or email the bank holds on this account, the second step before changing
        or removing the contact channel. Needs a verify_identity in the last 15 minutes first. The result says where the code
        went (never the code). Then call confirm_verification_code, which waits for the customer to type it."""
        now = tool_context.state["temp:now"]
        error = _lock_error(tool_context) or verification_gate_error(tool_context.state.get("identity_verified_at"), now, "sending a one-time code")
        if error:
            return {"error": error}
        return world.issue_code(h.bank_db, tool_context.user_id, tool_context.session.id, now, MAX_VERIFICATION_ATTEMPTS)

    def confirm_verification_code(tool_context: ToolContext, entered: EnteredCode = None) -> dict:
        """Check the one-time code that was just sent. If the customer already typed it in their latest message, pass it as
        `entered`. Otherwise call it with no argument: the conversation pauses until the customer's next message, which is
        taken as their entry. Never ask the customer to read the code to you and never repeat it."""
        now = tool_context.state["temp:now"]
        confirmation = tool_context.tool_confirmation
        typed = entered or str(((confirmation.payload if confirmation else None) or {}).get("entered", ""))
        proved = world.possession_proved_at(h.bank_db, tool_context.user_id, tool_context.session.id, now)
        if proved:  # this conversation already entered the right code (its result was lost to a crash): the bank record is the result
            tool_context.state["possession_verified_at"] = proved
            is_code = typed.strip().isdigit() and len(typed.strip()) == 6
            return {"verified": True, "valid_for_minutes": VERIFICATION_TTL_MINUTES, "customer_entered": ONE_TIME_CODE_MASK if is_code else typed,
                    "note": "the code was entered correctly before the process stopped; this result is rebuilt from the bank's record of it, so carry out the change or removal the customer asked for before the code was sent" + ("" if is_code else "; the customer's latest message was not a code: answer it too")}
        attempt = world.attempt_code(h.bank_db, tool_context.user_id, typed, now, MAX_VERIFICATION_ATTEMPTS, session_id=tool_context.session.id,
                                     repeat_of_lost_call=world.lost_result_is_recent(tool_context.state.get("lost_result_at"), now))
        return _code_result(tool_context.state, attempt, typed, now)

    def notify_customer(message: CustomerMessage, tool_context: ToolContext) -> dict:
        """Send the customer one message on their contact channel. Only for scheduled follow-ups; one per follow-up."""
        record = kind.followup and scheduler.get_followup(h.scheduler_db, kind.followup["followup_id"])
        if not record:
            return {"error": "notify_customer is only for scheduled follow-ups; in a live conversation, just reply"}
        if MASK_TOKEN.search(message):
            return {"error": "the message contains masked text ([REDACTED ...]); write it without that part"}
        if record["action"] == "customer_reminder" and (record["status"] != "running" or not kind.persist):
            return {"error": "this reminder was cancelled (the customer asked to be erased); send nothing"}
        channel, _ = _channel(tool_context)
        held = record["approval"] != "none"
        sent = world.record_outbound_message(h.bank_db, tool_context.user_id, channel, mask_card_numbers(message), record["followup_id"],
                                             held, tool_context.state["temp:now"])
        if sent is None:  # the database's one-message-per-follow-up constraint
            return {"error": "this follow-up has already produced its one message"}
        return {"channel": channel, "message_id": sent["message_id"],
                "status": "held for a Kestrel reviewer to approve before it is sent" if held else "sent"}

    tools = [verify_identity, find_transactions, file_dispute, add_case_evidence, get_case_status, search_policy,
             remember_customer_fact, forget_customer_fact, schedule_reminder, list_my_followups, cancel_reminder,
             request_memory_erasure, send_verification_code, confirm_verification_code, notify_customer]
    excluded = LIVE_ONLY_TOOLS if kind.unattended else UNATTENDED_ONLY_TOOLS
    # confirm_verification_code is ADK's confirmation flow: called without the code it pauses the turn (adk_request_confirmation)
    # and the customer's next message resumes it with their entry as the payload, which the tool then checks (run_turn routes
    # it); called with the code the customer already typed, it checks at once. No pause either when the bank already holds
    # this conversation's proof (a code consumed just before a crash): the tool runs and returns the recorded result
    def needs_the_customers_entry(tool_context: ToolContext, entered: str | None = None) -> bool:
        return not entered and not world.possession_proved_at(h.bank_db, tool_context.user_id, tool_context.session.id,
                                                              tool_context.state["temp:now"])

    return [FunctionTool(tool, require_confirmation=needs_the_customers_entry) if tool.__name__ == "confirm_verification_code" else tool
            for tool in tools if tool.__name__ not in excluded]


def _tool_name(tool) -> str:
    return getattr(tool, "__name__", None) or tool.name


def _code_result(state, attempt: dict, entered: str, now: str) -> dict:
    """What the model is told after a code entry; the code itself is never in it."""
    outcome = attempt["outcome"]
    if outcome == "matched":
        state["possession_verified_at"] = now
        return {"verified": True, "valid_for_minutes": VERIFICATION_TTL_MINUTES, "customer_entered": ONE_TIME_CODE_MASK,
                "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, "
                        "without asking them to repeat it"}
    if outcome == "locked":
        return {"verified": False, "error": f"verification is locked on this account for {VERIFICATION_LOCK_HOURS} hours after "
                                            f"{MAX_VERIFICATION_ATTEMPTS} failed attempts; the customer must call Kestrel"}
    if outcome == "mismatch":
        return {"verified": False, "error": "that code is not right", "entries_left_for_this_code": attempt["entries_left"],
                "customer_entered": ONE_TIME_CODE_MASK}
    if outcome == "expired":
        return {"verified": False, "error": "the code expired (5 minutes) and no new code has been sent; tell the customer and send a new one only if they ask (send_verification_code)",
                "customer_entered": ONE_TIME_CODE_MASK if entered.strip().isdigit() else entered}
    if outcome == "no_open_code":
        return {"verified": False, "error": "no code is open for this customer; call send_verification_code first", "customer_entered": entered}
    return {"verified": False, "customer_entered": entered,
            "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call "
                    "confirm_verification_code again when they are ready, without sending a new one"}


# --------------------------------------------------------------------------- agent


def build_instruction(h: Harness) -> Callable[[ReadonlyContext], str]:
    def instruction(ctx: ReadonlyContext) -> str:
        version, text = procedures.active_procedure(h.var_dir)
        now = ctx.state["temp:now"]
        facts = {key: ctx.state.get(f"user:{key}") for key in FACT_KEYS}
        profile = render_profile({key: fact for key, fact in facts.items() if fact}, now)
        return procedures.render_system_prompt(text, version, profile, ctx.state["app:dispute_review_days"], now,
                                               render_stepup_status(ctx.state.get("identity_verified_at"), ctx.state.get("possession_verified_at"), now,
                                                                    world.open_code_status(h.bank_db, ctx.user_id, now)))

    return instruction


def forget_expired_facts(callback_context: CallbackContext) -> None:
    """before_agent_callback: an expired travel notice is deleted, not merely hidden."""
    now = callback_context.state["temp:now"]
    for key in FACT_KEYS:
        fact = callback_context.state.get(f"user:{key}")
        if fact and fact_is_expired(fact, now):
            callback_context.state[f"user:{key}"] = None


def _is_customer_turn(content: types.Content) -> bool:
    parts = content.parts or []
    return content.role == "user" and any(p.text for p in parts) and not any(p.function_response for p in parts)


def window_working_memory(callback_context: CallbackContext, llm_request: LlmRequest) -> None:
    """before_model_callback: re-send the turns not yet reflected into long-term memory, and never fewer than the last
    WORKING_KEEP_TURNS customer turns (a conversation resumed after its end has every turn reflected; before round 5 the
    model then saw none of them and, with a one-time code waiting, could not tell what the code had been sent for)."""
    reflected = callback_context.state.get("reflected_turns", 0)
    starts = [i for i, content in enumerate(llm_request.contents) if _is_customer_turn(content)]
    start = min(reflected, max(0, len(starts) - WORKING_KEEP_TURNS))
    if 0 < start < len(starts):
        llm_request.contents = llm_request.contents[starts[start]:]


def mask_model_output(llm_response: LlmResponse) -> None:
    """Before anything is persisted: card numbers are masked in every reply part, and the model's reasoning (thought
    parts, which ADK stores in the session's events) gets the full customer-input rules, security codes and expiries
    included, since nobody reads it and over-masking it costs nothing."""
    for part in (llm_response.content.parts if llm_response.content else None) or []:
        if part.text:
            part.text = mask_customer_text(part.text) if part.thought else mask_card_numbers(part.text)


def report_malformed_tool_call(tool: MalformedTool = "") -> dict:
    """Harness use only, never call it yourself: the result of a tool call whose arguments were not valid JSON."""
    return {"error": f"your {tool or 'last'} call's arguments were not valid JSON, so it did not run; "
                     "make the call again with valid JSON arguments"}


def after_model(callback_context: CallbackContext, llm_response: LlmResponse) -> LlmResponse | None:
    """after_model_callback: mask, then turn a malformed tool call into a tool round trip. ADK ends the turn on
    MALFORMED_FUNCTION_CALL, so the customer would get no reply and the action (a dispute) would silently not happen;
    once per turn, the response is replaced by a call to report_malformed_tool_call, whose error result lets the
    model make the call again, the same contract as any other tool error (the LangGraph agent does the same in
    route_malformed_calls)."""
    mask_model_output(llm_response)
    if llm_response.error_code != "MALFORMED_FUNCTION_CALL" or callback_context.state.get("temp:malformed_call_retried"):
        return None
    callback_context.state["temp:malformed_call_retried"] = True
    thoughts = [part for part in ((llm_response.content.parts if llm_response.content else None) or []) if part.thought]
    call = types.FunctionCall(id=f"malformed-{uuid.uuid4().hex[:8]}", name="report_malformed_tool_call", args={})
    return LlmResponse(content=types.Content(role="model", parts=[*thoughts, types.Part(function_call=call)]))


def build_agent(h: Harness, disabled_tools: tuple[str, ...] = (), kind: SessionKind = LIVE) -> Agent:
    tools = [tool for tool in build_tools(h, kind) if _tool_name(tool) not in disabled_tools]
    if "load_memory" not in disabled_tools:
        tools.append(load_memory)
    tools.append(report_malformed_tool_call)
    return Agent(
        model=LiteLlm(model=f"deepseek/{DEEPSEEK_MODEL}", api_key=deepseek_api_key()),
        name=AGENT_NAME,
        description="Kestrel card-care assistant",
        instruction=build_instruction(h),
        tools=tools,
        before_agent_callback=forget_expired_facts,
        before_model_callback=window_working_memory,
        after_model_callback=after_model,
    )


# --------------------------------------------------------------------------- turns, sessions, follow-ups


def _turn_record(events: list[Event], customer_text: str) -> dict:
    tool_calls, reply = [], []
    for event in events:
        for part in (event.content.parts if event.content else None) or []:
            if part.function_call:
                tool_calls.append({"name": part.function_call.name, "args": dict(part.function_call.args or {}),
                                   "result": None, "id": part.function_call.id})
            elif part.function_response:
                matched = [call for call in tool_calls if call["id"] == part.function_response.id]
                for call in matched:
                    call["result"] = part.function_response.response
                if not matched and part.function_response.name != CONFIRMATION_CALL:
                    # the result of a call made in an earlier turn (a paused confirm_verification_code resumed by this one)
                    tool_calls.append({"name": part.function_response.name, "args": {}, "result": part.function_response.response, "id": None})
            elif part.text and not part.thought and event.author == AGENT_NAME:
                reply.append(part.text)
    for call in tool_calls:
        call.pop("id")
    return {"customer": customer_text, "tool_calls": tool_calls, "reply": "\n".join(reply).strip()}


def _transcript_turns(events: list[Event]) -> list[dict]:
    turns = []
    for event in events:
        for part in (event.content.parts if event.content else None) or []:
            if part.function_call:
                if part.function_call.name == CONFIRMATION_CALL:
                    continue  # ADK's pause; the customer's entry is rendered from its response below
                turns.append({"role": "tool", "text": f"called {part.function_call.name}({json.dumps(dict(part.function_call.args or {}))})"})
            elif part.function_response:
                if part.function_response.name == CONFIRMATION_CALL:
                    entered = ((part.function_response.response or {}).get("payload") or {}).get("entered")
                    if entered is not None:
                        turns.append({"role": "customer", "text": str(entered)})
                    continue
                turns.append({"role": "tool", "text": f"{part.function_response.name} -> {json.dumps(part.function_response.response, default=str)[:600]}"})
            elif part.text and not part.thought:
                turns.append({"role": "customer" if event.author == "user" else "assistant", "text": part.text})
    return turns


def _paused_call_id(confirmation_call: types.FunctionCall) -> str | None:
    """The id of the tool call an adk_request_confirmation call paused."""
    return ((confirmation_call.args or {}).get("originalFunctionCall") or {}).get("id")


def _pending_confirmation(session) -> types.FunctionCall | None:
    """ADK's pause for the one-time code: the latest adk_request_confirmation call whose paused tool has not recorded
    its result. Not yet answered is the ordinary wait. Answered with no tool result after the answer is a wait a crash
    reopened: the Runner stores the customer's entry before it re-runs the tool, so a process that dies inside the tool
    leaves the entry and no result, and the next message must resume the tool again (ADK's own request processor
    treats a confirmation as consumed only once the tool's result follows the answer)."""
    if not session:
        return None
    waiting: dict[str, types.FunctionCall] = {}
    answered: set[str] = set()
    for event in session.events:
        for part in (event.content.parts if event.content else None) or []:
            call, response = part.function_call, part.function_response
            if call and call.name == CONFIRMATION_CALL:
                waiting[call.id] = call
            elif response and response.id in waiting:
                answered.add(response.id)  # the customer's entry; the paused tool runs next
            elif response:
                for confirmation_id in [cid for cid in answered if cid in waiting and _paused_call_id(waiting[cid]) == response.id]:
                    del waiting[confirmation_id]  # the paused tool's result, recorded after the entry: the wait is over
    return list(waiting.values())[-1] if waiting else None


LOST_RESULT = "the result of this call was lost: the process stopped after the call was made and before its result was recorded, so the call may or may not have taken effect. Every tool is safe to call again with the same arguments (a repeat is recognised and nothing happens twice): make the same call again, or check the current state with a read tool first (get_case_status, list_my_followups), and do not tell the customer anything happened unless the repeated call or the read confirms it"


async def repair_interrupted_tool_calls(h: Harness, user_id: str, session_id: str, now: str | None = None) -> int:
    """A function call with no response (the process died mid-tool) would make every later model call fail; answer it.
    Round 4 answered "this call was interrupted and did not run", a guess: the process may have died after the tool's
    effect and before its result was recorded. Round 5 says the result was lost and that a repeat is safe, which is true
    of every write tool (cardcare/world.py, desk.py: a repeat is recognised by a constraint, a key overwrite or the
    guess itself). The repair also records when it said so (`lost_result_at`): only in the two minutes after that is
    the same verification guess made again taken for the lost call repeated, not for a new attempt. The one-time-code
    confirmation call is not a dangling call: it waits for the customer."""
    session = await h.session_service.get_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)
    if not session:
        return 0
    answered = {p.function_response.id for e in session.events for p in ((e.content.parts if e.content else None) or []) if p.function_response}
    dangling = [p.function_call for e in session.events for p in ((e.content.parts if e.content else None) or [])
                if p.function_call and p.function_call.id not in answered and p.function_call.name != CONFIRMATION_CALL]
    # a confirm_verification_code whose code the bank recorded as entered correctly by this conversation (the process died
    # after the code was consumed, before its result and, when the payload event was lost too, the customer's entry were
    # recorded): answered from the record, and the wait for the entry closed with it, so the next message is a message
    proved = world.possession_proved_at(h.bank_db, user_id, session_id, now) if now else None
    if dangling:
        matched = {"verified": True, "valid_for_minutes": VERIFICATION_TTL_MINUTES, "customer_entered": ONE_TIME_CODE_MASK, "note": "the code was entered correctly before the process stopped; this result is rebuilt from the bank's record of it, so carry out the change or removal the customer asked for before the code was sent"}
        parts = [types.Part(function_response=types.FunctionResponse(
            id=call.id, name=call.name,
            response=matched if proved and call.name == "confirm_verification_code" else {"error": LOST_RESULT}))
                 for call in dangling]
        await h.session_service.append_event(session, Event(invocation_id=f"repair-{uuid.uuid4().hex[:8]}", author=AGENT_NAME,
                                                            content=types.Content(role="user", parts=parts),
                                                            actions=EventActions(state_delta={"lost_result_at": now} if now else {})))
    return len(dangling)


def _cap(text: str) -> str:
    if len(text) <= MAX_CUSTOMER_MESSAGE_CHARS:
        return text
    return text[:MAX_CUSTOMER_MESSAGE_CHARS] + f" [message cut here: the other {len(text) - MAX_CUSTOMER_MESSAGE_CHARS} characters were not kept]"


CONTEXT_HOURS = 24  # earlier messages in the customer's other chats this recent are context for the masker too


async def recent_customer_messages(h: Harness, user_id: str, session_id: str, own: list[str], now: str) -> list[tuple[str, str]]:
    """(session id, stored text) of the customer's earlier messages, oldest first: this session's, after the last few of
    their other chats active in the past CONTEXT_HOURS (so a number split across two chats is caught too)."""
    others = []
    for listed in (await h.session_service.list_sessions(app_name=APP_NAME, user_id=user_id)).sessions:
        last = listed.state.get("last_active_at")
        if listed.id == session_id or _HELPER_SESSION.match(listed.id) or not last \
                or (parse_instant(now) - parse_instant(last)).total_seconds() > CONTEXT_HOURS * 3600:
            continue
        session = await h.session_service.get_session(app_name=APP_NAME, user_id=user_id, session_id=listed.id)
        others += [(last, listed.id, text) for text in _customer_texts(session.events)[-3:]]
    return [(sid, text) for _, sid, text in sorted(others, key=lambda item: item[0])] + [(session_id, text) for text in own]


async def scrub_earlier_messages(h: Harness, user_id: str, session_id: str, replacements: dict[str, str]) -> int:
    """A card number this message completes started in an earlier message: rewrite that message wherever it is stored
    (the session's events, the model's replies and reasoning that echoed it, this customer's episodes), then compact."""
    fragments = [f for old, new in replacements.items() for f in removed_fragments(old, new)]

    def fix(text: str) -> str:
        for old, new in replacements.items():
            text = text.replace(old, new)
        return scrub_fragments(text, fragments)

    changed = 0
    with closing(sqlite3.connect(h.sessions_db, timeout=60)) as conn, conn:
        for event_id, data in conn.execute("SELECT id, event_data FROM events WHERE app_name = ? AND user_id = ? AND session_id = ?",
                                           (APP_NAME, user_id, session_id)).fetchall():
            event = json.loads(data) if data else None
            if isinstance(event, dict) and "content" in event:  # only the conversation's content; ids and timestamps are never touched
                event["content"] = _map_strings(event["content"], fix)
            new = json.dumps(event) if data else data
            if new != data:
                conn.execute("UPDATE events SET event_data = ? WHERE id = ? AND app_name = ? AND user_id = ? AND session_id = ?",
                             (new, event_id, APP_NAME, user_id, session_id))
                changed += 1
    changed += h.memory_service.rewrite_user_texts(APP_NAME, user_id, fix)
    compact_sqlite(h.sessions_db)
    compact_sqlite(h.episodes_db)
    return changed


async def _undo_stale_fact_writes(h: Harness, user_id: str, session_id: str, events: list[Event]) -> None:
    """ADK applies a tool's state change when it appends the tool's event, after the tool has returned. If an erasure
    overtook this session in between (from another chat or process), a fact this turn wrote is deleted again."""
    if privacy.session_is_current(h.privacy_db, user_id, session_id):
        return
    written = {k[5:]: v for e in events for k, v in ((e.actions.state_delta if e.actions else None) or {}).items()
               if k.startswith("user:") and v}
    stored = await user_facts(h, user_id)
    stale = {key: None for key, value in written.items() if stored.get(key) == value}
    if stale:
        await write_user_facts(h, user_id, stale)


async def _ephemeral_session(h: Harness, user_id: str, session_id: str, now: str) -> InMemorySessionService:
    """A follow-up whose record predates an erasure: it runs in memory and nothing about it is stored."""
    service = InMemorySessionService()
    state = {**APP_SETTINGS, **{f"user:{k}": v for k, v in (await user_facts(h, user_id)).items()}, "first_active_at": now,
             "last_active_at": now}
    await service.create_session(app_name=APP_NAME, user_id=user_id, session_id=session_id, state=state)
    return service


async def run_turn(h: Harness, user_id: str, session_id: str, text: str, now: str, disabled_tools: tuple[str, ...] = (),
                   kind: SessionKind = LIVE, service=None) -> dict:
    """One customer message through the agent. Returns what was sent, every tool call with its result, and the reply.

    A failure inside the turn is returned as an error record, after the session is repaired, so one bad turn never
    leaves the conversation unusable.
    """
    clock = CLOCK.set(now)
    try:
        return await _run_turn(h, user_id, session_id, text, now, disabled_tools, kind, service)
    finally:
        CLOCK.reset(clock)


async def _run_turn(h, user_id, session_id, text, now, disabled_tools, kind, service) -> dict:
    if kind.persist:
        await finish_requested_erasures(h, now, user_id=user_id, keep=session_id)
        await retire_expired_session(h, user_id, session_id, now)
        privacy.register_session(h.privacy_db, user_id, session_id, kind.label, now)
        await repair_interrupted_tool_calls(h, user_id, session_id, now)
        desk.ensure_case_followups(h.bank_db, h.scheduler_db, now, APP_SETTINGS["app:dispute_review_days"],
                                   APP_SETTINGS["app:large_dispute_threshold_cents"], user_id=user_id,
                                   generation_of=lambda uid: privacy.current_generation(h.privacy_db, uid))
        service = h.session_service
    else:
        service = service or await _ephemeral_session(h, user_id, session_id, now)
    session = await service.get_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)
    turns = group_by_customer_turn(_transcript_turns(session.events)) if session else []
    if kind.persist and session and len(turns) + 1 - session.state.get("reflected_turns", 0) > WORKING_WINDOW_TURNS:
        await reflect_turns(h, user_id, session_id, now, upto=len(turns) + 1 - WORKING_KEEP_TURNS, kind=kind)
    own = [group[0]["text"] for group in turns if group and group[0]["role"] == "customer"]
    earlier = await recent_customer_messages(h, user_id, session_id, own, now) if kind.persist and not kind.unattended else \
        [(session_id, text) for text in own]
    sent, rewrites = mask_customer_message(text, tuple(text for _, text in earlier))  # card data never enters a store
    sent = _cap(sent)
    if rewrites and kind.persist:
        by_session: dict[str, dict[str, str]] = {}
        for index, rewritten in rewrites.items():
            by_session.setdefault(earlier[index][0], {})[earlier[index][1]] = rewritten
        for sid, replacements in by_session.items():
            await scrub_earlier_messages(h, user_id, sid, replacements)
    agent = build_agent(h, disabled_tools, kind)
    runner = Runner(app_name=APP_NAME, agent=agent, session_service=service, memory_service=h.memory_service, auto_create_session=True)
    pending = _pending_confirmation(session) if kind.persist else None
    if pending:  # the agent is waiting for the one-time code: this message is the customer's entry, and it resumes the paused tool
        message = types.Content(role="user", parts=[types.Part(function_response=types.FunctionResponse(
            id=pending.id, name=CONFIRMATION_CALL, response={"confirmed": True, "payload": {"entered": sent}}))])
    else:
        message = types.Content(role="user", parts=[types.Part(text=sent)])
    delta = {"temp:now": now, "last_active_at": now,
             "turn_times": [*((session.state.get("turn_times") or []) if session else []), now][-WORKING_WINDOW_TURNS * 3:]}
    if not (session and session.state.get("first_active_at")):
        delta["first_active_at"] = now
    if kind.persist and not (session and session.state.get("possession_verified_at")):
        proved = world.possession_proved_at(h.bank_db, user_id, session_id, now)  # the bank's record rebuilds a copy a crash lost
        if proved:
            delta["possession_verified_at"] = proved
    events = []
    try:
        async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=message, state_delta=delta):
            events.append(event)
    except Exception as exc:
        record = _turn_record(events, sent)
        if kind.persist:
            await repair_interrupted_tool_calls(h, user_id, session_id, now)
            record = await without_one_time_codes(h, user_id, session_id, sent, record)  # a failed turn keeps no code either
        return {**record, "error": f"{type(exc).__name__}: {exc}", "tools_offered": _tool_names(agent)}
    if kind.persist:
        await _undo_stale_fact_writes(h, user_id, session_id, events)
    record = _turn_record(events, sent)
    if not record["reply"].strip() and kind.persist and _pending_confirmation(
            await h.session_service.get_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)):
        record["reply"] = waiting_for_code_line(h.bank_db, user_id, now)  # the model paused without a word: the bank record speaks
    if kind.persist:
        record = await without_one_time_codes(h, user_id, session_id, sent, record)
    return {**record, "tools_offered": _tool_names(agent)}


async def without_one_time_codes(h: Harness, user_id: str, session_id: str, sent: str, record: dict) -> dict:
    """Redact one-time codes from the stored session and return the turn record without them. A code the tool took: every
    6-digit run in the message goes. A code no tool took (typed when nothing was pending, or left raw by a crash or a
    failed turn): the runs that are one of the bank's codes for this customer, by salted hash. Runs at the end of every
    turn, failed ones included, so a code the bank issued is never kept in a transcript."""
    taken = any(call["name"] == "confirm_verification_code" and (call.get("result") or {}).get("customer_entered") == ONE_TIME_CODE_MASK
                for call in record["tool_calls"])
    codes = set(re.findall(r"(?<!\d)\d{6}(?!\d)", sent)) if taken else set()
    codes |= set(world.codes_matching(h.bank_db, user_id, await _session_text(h, user_id, session_id)))
    if not codes:
        return record
    await scrub_earlier_messages(h, user_id, session_id, {code: ONE_TIME_CODE_MASK for code in codes})
    calls = [{**call, "args": {k: (_replace_codes(v, codes) if isinstance(v, str) else v) for k, v in call["args"].items()}}
             for call in record["tool_calls"]]
    return {**record, "customer": _replace_codes(sent, codes), "tool_calls": calls}


async def _session_text(h: Harness, user_id: str, session_id: str) -> str:
    """Every string the session's events hold (texts, tool arguments, tool results, confirmation payloads), for the
    hash check of one-time codes."""
    session = await h.session_service.get_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)
    return json.dumps([e.content.model_dump(mode="json") for e in (session.events if session else []) if e.content], default=str)


def waiting_for_code_line(bank_db: Path, user_id: str, now: str) -> str:
    """What the customer reads when the turn paused for the code and the model wrote nothing: composed from the bank's
    record of the code it just sent, never from the model."""
    code = world.open_code_status(bank_db, user_id, now)
    where = f" by {code['sent_to']}" if code else ""
    return (f"A one-time code has been sent{where}; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it "
            "arrives, and I will finish your request.")


def _replace_codes(text: str, codes: set[str]) -> str:
    for code in codes:
        text = text.replace(code, ONE_TIME_CODE_MASK)
    return text


def _tool_names(agent: Agent) -> list[str]:
    return sorted(_tool_name(tool) for tool in agent.tools)


async def complete_text(prompt: str) -> str:
    response = await litellm.acompletion(
        model=f"deepseek/{DEEPSEEK_MODEL}", api_key=deepseek_api_key(), messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content or ""


async def reflect_turns(h: Harness, user_id: str, session_id: str, now: str, upto: int | None = None,
                        kind: SessionKind = LIVE) -> dict | None:
    """Reflect the customer turns after the session's reflected mark, up to `upto` (default: all), into one episode.
    The episode is written behind the erasure fence: a session an erasure has overtaken writes none."""
    session = await h.session_service.get_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)
    if not session or not privacy.session_is_current(h.privacy_db, user_id, session_id):
        return None
    groups = group_by_customer_turn(_transcript_turns(session.events))
    reflected = session.state.get("reflected_turns", 0)
    upto = len(groups) if upto is None else upto
    turns = [turn for group in groups[reflected:upto] for turn in group]
    if not turns:
        return None
    reflection = parse_reflection(await complete_text(reflection_prompt(turns)), user_id, own_case_ids(h.bank_db, user_id))
    if reflection is None:  # nothing the model wrote: no episode, and the turns stay unreflected for the next opportunity
        return None
    sequence = session.state.get("episodes_written", 0) + 1
    episode = build_episode(user_id, session_id, sequence, now, reflection, case_outcomes(h.bank_db, user_id, turns),
                            procedures.active_procedure(h.var_dir)[0], customer_present=not kind.unattended)
    with privacy.write_guard(h.privacy_db, user_id, session_id) as writable:
        if not writable:
            return None
        await h.memory_service.add_memory(app_name=APP_NAME, user_id=user_id, memories=[MemoryEntry(
            id=episode["episode_id"], author="reflection", timestamp=now,
            content=types.Content(role="user", parts=[types.Part(text=episode["text"])]),
            custom_metadata={"episode": episode},
        )])
    await write_session_state(h, user_id, session_id, {"reflected_turns": upto, "episodes_written": sequence})
    return episode


async def delete_transcript(h: Harness, user_id: str, session_id: str, forget: bool = True) -> bool:
    """Delete a session. `forget=False` keeps its registration (stale), so a chat that goes on after its transcript was
    erased still stores nothing."""
    session = await h.session_service.get_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)
    if session:
        await h.session_service.delete_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)
    if forget:
        privacy.forget_session(h.privacy_db, user_id, session_id)
    return bool(session)


async def end_session(h: Harness, user_id: str, session_id: str, now: str, kind: SessionKind = LIVE) -> dict | None:
    """Session concluded: a session an erasure overtook (the one the customer asked in, or any that started before it)
    is deleted, which completes the erasure; any other is reflected."""
    if not kind.persist:
        return None
    if not privacy.session_is_current(h.privacy_db, user_id, session_id):
        if await delete_transcript(h, user_id, session_id):
            compact_sqlite(h.sessions_db)
        await finish_requested_erasures(h, now, user_id=user_id, only_session=session_id)
        return None
    return await reflect_turns(h, user_id, session_id, now, kind=kind)


async def finish_requested_erasures(h: Harness, now: str, user_id: str | None = None, keep: str | None = None,
                                    only_session: str | None = None, idle_only: bool = False) -> list[str]:
    """Delete the transcript an erasure request was made in: at that chat's end, at the customer's next turn in another
    chat, or when maintenance finds it idle (`idle_only`: 30 minutes without a turn, a closed tab), whichever comes
    first. A customer who asks to be erased and keeps typing keeps their open conversation until it ends. If the chat
    goes on after that, it stays stale: still nothing is stored, and what it adds is deleted when it ends."""
    finished = []
    for request in privacy.pending_requests(h.privacy_db, user_id):
        session_id = request["requested_in"]
        if session_id == keep or (only_session and session_id != only_session):
            continue
        session = session_id and await h.session_service.get_session(app_name=APP_NAME, user_id=request["user_id"], session_id=session_id)
        if idle_only and session and not session_is_idle(session.state.get("last_active_at"), now):
            continue
        if session_id:
            await delete_transcript(h, request["user_id"], session_id, forget=bool(only_session))
        privacy.finish_request(h.privacy_db, request["rowid"], now)
        finished.append(request["user_id"])
    if finished:
        compact_sqlite(h.sessions_db)
    return finished


async def erase_customer_memory(h: Harness, user_id: str, now: str, requesting_session: str | None = None) -> dict:
    """Right to erasure, at once: raise the customer's memory generation (the fence), then delete every fact, episode,
    reminder (its note too, whatever its state) and every transcript but the requesting one, which is still running and
    is deleted when it ends. Bank records (cases, ledger, messages already sent) are not memory and stay."""
    privacy.begin_erasure(h.privacy_db, user_id, requesting_session, now)
    world.cancel_open_codes(h.bank_db, user_id, now)  # a code waiting to be typed dies with the request
    reminders = scheduler.erase_customer_reminders(h.scheduler_db, user_id, now)
    world.reject_held_messages(h.bank_db, reminders, "erasure")
    facts = await user_facts(h, user_id)
    await write_user_facts(h, user_id, {key: None for key in FACT_KEYS})
    episodes = [e for e in h.memory_service.list_episodes(APP_NAME) if e["user_id"] == user_id]
    for episode in episodes:
        await h.memory_service.delete_memory(app_name=APP_NAME, user_id=user_id, memory_id=episode["episode_id"])
    sessions = [s for s in (await h.session_service.list_sessions(app_name=APP_NAME, user_id=user_id)).sessions if s.id != requesting_session]
    for session in sessions:
        await h.session_service.delete_session(app_name=APP_NAME, user_id=user_id, session_id=session.id)
    compact_sqlite(h.sessions_db)
    compact_sqlite(h.episodes_db)
    compact_sqlite(h.scheduler_db)
    if requesting_session is None:
        for request in privacy.pending_requests(h.privacy_db, user_id):
            if request["requested_in"] is None:
                privacy.finish_request(h.privacy_db, request["rowid"], now)
    return {"user_id": user_id, "facts": len(facts), "episodes": len(episodes), "transcripts": len(sessions), "reminders_cancelled": reminders}


async def retire_expired_session(h: Harness, user_id: str, session_id: str, now: str) -> bool:
    """A session lives 30 days from its first turn, whether or not maintenance has run: a turn on an older one first
    reflects what is not yet reflected, then deletes it, so the conversation continues as a new one."""
    session = await h.session_service.get_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)
    if not session or not transcript_is_expired(session.state.get("first_active_at") or session.state.get("last_active_at"), now):
        return False
    record = privacy.session_record(h.privacy_db, user_id, session_id)
    await reflect_turns(h, user_id, session_id, session.state.get("last_active_at") or now,
                        kind=SessionKind(unattended=bool(record and record["kind"] == "unattended")))
    await delete_transcript(h, user_id, session_id)
    compact_sqlite(h.sessions_db)
    compact_sqlite(h.episodes_db)
    return True


async def run_maintenance(h: Harness, now: str) -> dict:
    """The harness's memory job: finish erasures whose conversation is over, delete expired facts of every customer,
    close idle chats (deleting the ones an erasure overtook), purge expired episodes and delete transcripts 30 days
    after their first turn."""
    CLOCK.set(now)
    erased = await finish_requested_erasures(h, now, idle_only=True)
    world.retire_code_messages(h.bank_db, now)  # the outbox keeps a code's text only while the code can be used
    repaired_cases = desk.ensure_case_followups(h.bank_db, h.scheduler_db, now, APP_SETTINGS["app:dispute_review_days"],
                                                APP_SETTINGS["app:large_dispute_threshold_cents"],
                                                generation_of=lambda uid: privacy.current_generation(h.privacy_db, uid))
    expired_facts = []
    for user_id in [customer[0] for customer in world.CUSTOMERS]:
        stale = {key: None for key, fact in (await user_facts(h, user_id)).items() if key in FACT_KEYS and fact_is_expired(fact, now)}
        if stale:
            await write_user_facts(h, user_id, stale)
            expired_facts += [f"{user_id}:{key}" for key in stale]
    closed, deleted = [], []
    for listed in (await h.session_service.list_sessions(app_name=APP_NAME)).sessions:
        if listed.user_id == OPS_USER:
            continue
        last_active = listed.state.get("last_active_at")
        current = privacy.session_is_current(h.privacy_db, listed.user_id, listed.id)
        record = privacy.session_record(h.privacy_db, listed.user_id, listed.id)
        kind = SessionKind(unattended=bool(record and record["kind"] == "unattended"))
        if not current and (session_is_idle(last_active, now) or _HELPER_SESSION.match(listed.id) or not last_active):
            await delete_transcript(h, listed.user_id, listed.id)
            deleted.append(listed.id)
            continue
        if session_is_idle(last_active, now) and await reflect_turns(h, listed.user_id, listed.id, last_active, kind=kind):
            closed.append(listed.id)
        if transcript_is_expired(listed.state.get("first_active_at") or last_active, now):
            await delete_transcript(h, listed.user_id, listed.id)
            deleted.append(listed.id)
    expired = [e for e in h.memory_service.list_episodes(APP_NAME) if episode_is_expired(e, now)]
    for episode in expired:
        await h.memory_service.delete_memory(app_name=APP_NAME, user_id=episode["user_id"], memory_id=episode["episode_id"])
    if deleted or expired or expired_facts:
        compact_sqlite(h.sessions_db)
        compact_sqlite(h.episodes_db)
    return {"erased_customers": erased, "expired_facts": expired_facts, "closed_idle_sessions": closed,
            "purged_episodes": [e["episode_id"] for e in expired], "deleted_transcripts": deleted, "case_followups_repaired": repaired_cases}


async def run_followup_session(h: Harness, record: dict, now: str) -> dict:
    """The scheduler's resume callback. The session's kind is built from the record and passed in; nothing it stores
    can change it. A record written before the customer's latest erasure runs in memory and leaves nothing behind."""
    # whoever fires a follow-up, a pending erasure of that customer is finished first (its requesting chat's transcript
    # deleted), so nothing scheduled can run while part of an erasure is still waiting
    await finish_requested_erasures(h, now, user_id=record["user_id"])
    persist = record.get("generation", 0) == privacy.current_generation(h.privacy_db, record["user_id"])
    kind = followup_kind(record, persist)
    session_id = f"followup-{record['followup_id']}-{record['attempts'] + 1}"
    if persist:
        await h.session_service.create_session(app_name=APP_NAME, user_id=record["user_id"], session_id=session_id,
                                               state={"last_active_at": now, "first_active_at": now})
    turn = await run_turn(h, record["user_id"], session_id, scheduler.followup_trigger_message(record), now, kind=kind)
    episode = await end_session(h, record["user_id"], session_id, now, kind=kind)
    return {"session_id": session_id, "persisted": persist, "turn": turn, "episode": episode}


async def snapshot(h: Harness, user_ids: list[str]) -> dict:
    """Read-only view of every store, for evidence. Reads state; never writes it."""
    facts, transcripts = {}, {}
    for user_id in user_ids:
        facts[user_id] = await user_facts(h, user_id)
        sessions = await h.session_service.list_sessions(app_name=APP_NAME, user_id=user_id)
        transcripts[user_id] = sorted(session.id for session in sessions.sessions)
    with closing(sqlite3.connect(h.sessions_db)) as conn:
        session_keys = {key for (state,) in conn.execute("SELECT state FROM sessions") for key in json.loads(state or "{}")}
        stored_text = " ".join(text or "" for (text,) in conn.execute("SELECT state FROM sessions UNION ALL SELECT event_data FROM events"))
    return {
        "facts": facts,
        "episodes": h.memory_service.list_episodes(APP_NAME),
        "persisted_state_keys": sorted(session_keys),
        "persisted_clock_keys": sorted(set(re.findall(r'"(temp:[A-Za-z_]+)"', stored_text))),
        "followups": scheduler.list_followups(h.scheduler_db),
        "outbound_messages": world.outbound_messages(h.bank_db),
        "verification_attempts": world.verification_attempt_rows(h.bank_db),
        "challenges": world.list_challenges(h.bank_db),
        "cases": world.all_cases(h.bank_db),
        "procedure": procedures.load_registry(h.var_dir),
        "procedure_text": procedures.active_procedure(h.var_dir)[1],
        "transcripts": transcripts,
    }


# --------------------------------------------------------------------------- interactive CLI


async def chat(var_dir: Path, user_id: str, session_id: str | None, now: str | None) -> None:
    h = await open_harness(var_dir)
    session_id = session_id or f"chat-{uuid.uuid4().hex[:8]}"
    print(f"Kestrel card-care (ADK) | customer={user_id} session={session_id} | 'exit' or end-of-input ends the session")
    shown = max((m["message_id"] for m in world.outbound_messages(h.bank_db)), default=0)
    while True:
        try:
            text = (await asyncio.to_thread(input, "\n[you]: ")).strip()
        except EOFError:  # the tab was closed: the session still ends properly
            break
        if text in ("exit", "quit"):
            break
        if text:
            turn = await run_turn(h, user_id, session_id, text, now or wall_clock_now())
            for call in turn["tool_calls"]:
                print(f"  [tool] {call['name']}({json.dumps(call['args'])})")
            print(f"\n[assistant]: {turn['reply'] or '(no reply: ' + turn.get('error', 'empty turn') + '; you can keep chatting)'}")
            for line in device_lines(h.bank_db, user_id, shown):  # what the customer's phone shows, not part of the reply
                print(line)
            shown = max((m["message_id"] for m in world.outbound_messages(h.bank_db)), default=shown)
    episode = await end_session(h, user_id, session_id, now or wall_clock_now())
    if episode:
        print(f"\n[memory] episode {episode['episode_id']}: {episode['text']}")


async def fire_followups(h: Harness, now: str, on_session: Callable[[dict], None] | None = None) -> list[dict]:
    """The scheduler's job: finish every pending erasure first (the requesting chat's transcript goes, whether or not a
    record of that customer is due), then fire what is due. `on_session` sees each follow-up session's record."""
    await finish_requested_erasures(h, now)

    async def resume(record: dict, at: str) -> dict:
        session = await run_followup_session(h, record, at)
        if on_session:
            on_session(session)
        return session

    return await scheduler.fire_due_followups(h.scheduler_db, h.bank_db, now, resume, on_failed=lambda record, at: notify_delivery_failure(h, record, at))


async def notify_delivery_failure(h: Harness, record: dict, now: str) -> None:
    """A record the scheduler gave up on (MAX_ATTEMPTS fires without a message): the customer is told by a bank message
    on the channel on file, with no model involved, that carries the date and nothing of the reminder's note."""
    facts = await user_facts(h, record["user_id"])
    channel = (facts.get("contact_channel") or {}).get("value", DEFAULT_CHANNEL)
    world.record_outbound_message(h.bank_db, record["user_id"], channel, scheduler.delivery_failure_notice(record), record["followup_id"],
                                  False, now, purpose="delivery_failure")


def device_lines(bank_db: Path, user_id: str, after_message_id: int) -> list[str]:
    """One-time codes the bank sent this customer since `after_message_id`, as the customer's own device would show them.
    The agent never sees these lines; the person at the keyboard does, and types the code back."""
    return [f"\n[your phone, {m['channel']} to {m['destination']}]: {m['body']}" for m in world.outbound_messages(bank_db)
            if m["user_id"] == user_id and m.get("purpose") == "one_time_code" and m["message_id"] > after_message_id]


async def tick(var_dir: Path, now: str | None) -> dict:
    """One pass of the harness's background work: memory maintenance, then the scheduler (which finishes any pending
    erasure before it fires anything)."""
    h = await open_harness(var_dir)
    at = now or wall_clock_now()
    maintenance = await run_maintenance(h, at)
    return {"now": at, "maintenance": maintenance, "followups": await fire_followups(h, at)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("command", choices=["chat", "tick"])
    parser.add_argument("--user", default="priya", choices=[c[0] for c in world.CUSTOMERS])
    parser.add_argument("--session", help="continue an existing session id")
    parser.add_argument("--now", help="override the clock (ISO-8601), e.g. 2026-11-19T10:00:00Z")
    parser.add_argument("--loop", type=int, metavar="SECONDS", help="tick: repeat every SECONDS on the wall clock")
    parser.add_argument("--var-dir", type=Path, default=CODE_DIR / "var" / "adk" / "interactive")
    args = parser.parse_args()
    if args.command == "chat":
        asyncio.run(chat(args.var_dir, args.user, args.session, args.now))
        return
    while True:
        print(json.dumps(asyncio.run(tick(args.var_dir, args.now)), indent=2))
        if not args.loop:
            break
        time.sleep(args.loop)


if __name__ == "__main__":
    main()
