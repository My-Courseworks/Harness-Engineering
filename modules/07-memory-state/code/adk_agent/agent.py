"""Kestrel card-care assistant on Google ADK: where each of the module's seven memory types lives.

  working / in-context  Session events (DatabaseSessionService on SQLite), re-sent every turn up to a
                        window of WORKING_WINDOW_TURNS customer turns, plus State:
                          identity_verified_at, identity_failed_attempts, followup_id, last_active_at,
                          reflected_turns, episodes_written, erasure_requested_at   this conversation only
                          user:contact_channel, user:travel_notice   this customer, every session
                          app:dispute_review_days, app:large_dispute_threshold_cents   every customer
                          temp:now   the harness clock for this invocation; never persisted
  semantic              the user: keys above: a closed schema, timestamped, overwritten by key,
                        preloaded into the instruction every turn (small and always relevant)
  episodic              EpisodeMemoryService: reflections on finished (or windowed-out) turns, recalled
                        on demand with ADK's load_memory tool (large and mostly irrelevant)
  procedural            the versioned instruction (cardcare/procedure_versions + the registry in var/)
  external / retrieval  tools: exact SQL lookups for transactions and cases; search_policy (embeddings)
  parametric            the DeepSeek weights; nothing here manages them, which is the point
  prospective           cardcare/scheduler.py: file_dispute and schedule_reminder write records, the
                        customer can list and cancel their own, the harness fires them (`tick`)

Run `python -m adk_agent.agent chat --user priya` from modules/07-memory-state/code.
"""

import argparse
import asyncio
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
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.adk.tools import ToolContext, load_memory
from google.genai import types

from cardcare import desk, procedures, scheduler, world
from cardcare.clock import wall_clock_now
from cardcare.episodes import build_episode, case_outcomes, group_by_customer_turn, own_case_ids, parse_reflection, reflection_prompt
from cardcare.memory_policy import (
    FACT_KEYS,
    FACT_KEYS_NEEDING_VERIFICATION,
    MAX_VERIFICATION_ATTEMPTS,
    TRANSCRIPT_RETENTION_DAYS,
    WORKING_KEEP_TURNS,
    WORKING_WINDOW_TURNS,
    build_fact,
    episode_is_expired,
    fact_is_expired,
    redact_card_secrets,
    render_profile,
    session_is_idle,
    transcript_is_expired,
    verification_gate_error,
)
from cardcare.model_config import DEEPSEEK_MODEL, deepseek_api_key
from cardcare.retrieval import embed_texts, search_policy as search_policy_documents, top_matches

APP_NAME = "kestrel_card_care"
AGENT_NAME = "card_care"
APP_SETTINGS = {"app:dispute_review_days": 10, "app:large_dispute_threshold_cents": 20000}
OPS_USER = "ops"
CODE_DIR = Path(__file__).resolve().parent.parent


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
            conn.executemany("INSERT OR REPLACE INTO episodes VALUES (?, ?, ?, ?, ?, ?, ?)", rows)

    async def search_memory(self, *, app_name: str, user_id: str, query: str) -> SearchMemoryResponse:
        # Scope first, similarity second: another customer's episodes are never even scored.
        with closing(sqlite3.connect(self.db_path)) as conn:
            rows = conn.execute(
                "SELECT memory_id, at, text, embedding FROM episodes WHERE app_name = ? AND user_id = ?", (app_name, user_id)
            ).fetchall()
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


async def open_harness(var_dir: Path) -> Harness:
    """Create (or reopen) every local store under var_dir and seed the bank and the app-wide settings."""
    var_dir.mkdir(parents=True, exist_ok=True)
    world.seed_bank(var_dir / "bank.db")
    scheduler.create_scheduler(var_dir / "scheduler.db")
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
    event = Event(invocation_id=f"harness-{uuid.uuid4().hex[:8]}", author="harness", actions=EventActions(state_delta=delta))
    await h.session_service.append_event(session, event)


def compact_sqlite(path: Path) -> None:
    """Deleted rows linger in free pages and in the WAL until the file is rewritten; erasure has to reach those too.

    VACUUM first (in WAL mode it writes the rebuilt pages to the WAL), then checkpoint them into the main file
    and truncate the WAL, so neither file still holds the deleted bytes.
    """
    with closing(sqlite3.connect(path)) as conn:
        conn.execute("VACUUM")
        conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")


# --------------------------------------------------------------------------- tools


def build_tools(h: Harness) -> list[Callable]:
    """Tool functions over this harness's stores. The customer is always tool_context.user_id, never a model argument."""

    def verify_identity(card_last4: str, postal_code: str, tool_context: ToolContext) -> dict:
        """Verify the logged-in customer with their card's last 4 digits and billing ZIP, as the customer typed them.
        Valid for 15 minutes. Locks after 3 failed attempts in a conversation."""
        failed = tool_context.state.get("identity_failed_attempts", 0)
        if failed >= MAX_VERIFICATION_ATTEMPTS:
            return {"verified": False, "error": "verification is locked for this conversation after 3 failed attempts; "
                                                "the customer must call Kestrel"}
        if not world.identity_matches(h.bank_db, tool_context.user_id, card_last4, postal_code):
            tool_context.state["identity_failed_attempts"] = failed + 1
            return {"verified": False, "error": "those details do not match this customer",
                    "attempts_left": MAX_VERIFICATION_ATTEMPTS - failed - 1}
        tool_context.state["identity_verified_at"] = tool_context.state["temp:now"]
        return {"verified": True, "valid_for_minutes": 15}

    def find_transactions(tool_context: ToolContext, merchant: str | None = None) -> dict:
        """List the customer's posted transactions, optionally only those whose merchant name contains `merchant`."""
        return {"transactions": world.find_transactions(h.bank_db, tool_context.user_id, merchant, tool_context.state["temp:now"])}

    def file_dispute(transaction_id: str, reason: str, tool_context: ToolContext, evidence_note: str | None = None) -> dict:
        """File a dispute for one transaction. reason: cancelled_subscription, not_recognized, duplicate,
        goods_not_received or incorrect_amount. evidence_note: anything the customer supplied (e.g. a cancellation
        reference). Requires a verify_identity in the last 15 minutes. Schedules the case follow-up automatically."""
        error = verification_gate_error(tool_context.state.get("identity_verified_at"), tool_context.state["temp:now"], "filing a dispute")
        if error:
            return {"error": error}
        return desk.file_dispute_with_followup(
            h.bank_db, h.scheduler_db, tool_context.user_id, transaction_id, reason, evidence_note,
            tool_context.state["temp:now"], tool_context.state["app:dispute_review_days"],
            tool_context.state["app:large_dispute_threshold_cents"],
        )

    def add_case_evidence(case_id: str, evidence_note: str, tool_context: ToolContext) -> dict:
        """Attach more evidence (e.g. a cancellation reference the customer found later) to one of their open cases."""
        return world.add_case_evidence(h.bank_db, tool_context.user_id, case_id, redact_card_secrets(evidence_note), tool_context.state["temp:now"])

    def get_case_status(tool_context: ToolContext, case_id: str | None = None) -> dict:
        """Current status of one dispute case, or of all this customer's cases when case_id is omitted."""
        return {"cases": world.list_cases(h.bank_db, tool_context.user_id, case_id)}

    def search_policy(question: str) -> dict:
        """Search Kestrel's policy documents (fees, dispute rules, travel notices, contact channels)."""
        return {"documents": search_policy_documents(question)}

    def remember_customer_fact(key: str, value: str, tool_context: ToolContext, valid_until: str | None = None) -> dict:
        """Store a fact the customer stated. key: contact_channel (value email, sms or secure_message) or
        travel_notice (value = destination, valid_until = return date YYYY-MM-DD). Replaces any earlier value."""
        if key in FACT_KEYS_NEEDING_VERIFICATION:
            error = verification_gate_error(tool_context.state.get("identity_verified_at"), tool_context.state["temp:now"], f"changing {key}")
            if error:
                return {"error": error}
        try:
            fact = build_fact(key, value, valid_until, tool_context.state["temp:now"])
        except ValueError as exc:
            return {"error": str(exc)}
        previous = tool_context.state.get(f"user:{key}")
        tool_context.state[f"user:{key}"] = fact  # keyed overwrite: the new value replaces the old, never joins it
        return {"stored": {key: fact}, "replaced": previous["value"] if previous else None}

    def forget_customer_fact(key: str, tool_context: ToolContext) -> dict:
        """Delete a stored customer fact (contact_channel or travel_notice) at the customer's request."""
        if key not in FACT_KEYS:
            return {"error": f"unknown fact {key}"}
        had_value = bool(tool_context.state.get(f"user:{key}"))
        tool_context.state[f"user:{key}"] = None
        return {"forgotten": key, "had_value": had_value,
                "note": f"deleted from memory now; conversation transcripts are deleted after {TRANSCRIPT_RETENTION_DAYS} days, "
                        "or at once if the customer asks to erase everything"}

    def schedule_reminder(note: str, remind_on: str, tool_context: ToolContext) -> dict:
        """Schedule a reminder message to the customer on a future date (YYYY-MM-DD). Only when the customer asks for one."""
        return desk.schedule_customer_reminder(h.scheduler_db, tool_context.user_id, note, remind_on, tool_context.state["temp:now"])

    def list_my_followups(tool_context: ToolContext) -> dict:
        """What is scheduled for this customer (reminders and case follow-ups), when, and on which channel it will arrive."""
        channel = (tool_context.state.get("user:contact_channel") or {}).get("value", "secure_message")
        records = [r for r in scheduler.user_followups(h.scheduler_db, tool_context.user_id) if r["status"] in ("pending", "awaiting_approval")]
        return {"scheduled": [scheduler.customer_view(r, channel) for r in records]}

    def cancel_reminder(followup_id: str, tool_context: ToolContext) -> dict:
        """Cancel one of the customer's own reminders before it is sent (ids come from list_my_followups)."""
        record = scheduler.get_followup(h.scheduler_db, followup_id)
        if not record or record["user_id"] != tool_context.user_id or record["action"] != "customer_reminder":
            return {"error": f"{followup_id} is not one of this customer's reminders"}
        cancelled = scheduler.cancel_followup(h.scheduler_db, followup_id, tool_context.user_id, tool_context.state["temp:now"])
        return {"cancelled": followup_id} if cancelled else {"error": f"{followup_id} has already been sent or cancelled"}

    def request_memory_erasure(tool_context: ToolContext) -> dict:
        """The customer asks to delete everything remembered about them. Runs when this conversation ends."""
        tool_context.state["erasure_requested_at"] = tool_context.state["temp:now"]
        return {"scheduled": "when this conversation ends, every remembered fact, every past-conversation summary and every "
                             "conversation transcript, including this one, will be erased",
                "kept": "dispute cases, transactions and messages already sent are bank records with their own legal retention"}

    def notify_customer(message: str, tool_context: ToolContext) -> dict:
        """Send the customer one message on their contact channel. Only for scheduled follow-ups; one per follow-up."""
        followup_id = tool_context.state.get("followup_id")
        if not followup_id:
            return {"error": "notify_customer is only for scheduled follow-ups; in a live conversation, just reply"}
        if any(m["followup_id"] == followup_id and m["status"] != "rejected" for m in world.outbound_messages(h.bank_db)):
            return {"error": "this follow-up has already produced its one message"}
        record = scheduler.get_followup(h.scheduler_db, followup_id)
        channel = (tool_context.state.get("user:contact_channel") or {}).get("value", "secure_message")
        held = record["approval"] != "none"
        sent = world.record_outbound_message(h.bank_db, tool_context.user_id, channel, redact_card_secrets(message), followup_id,
                                             held, tool_context.state["temp:now"])
        return {"channel": channel, "message_id": sent["message_id"],
                "status": "held for a Kestrel reviewer to approve before it is sent" if held else "sent"}

    return [verify_identity, find_transactions, file_dispute, add_case_evidence, get_case_status, search_policy,
            remember_customer_fact, forget_customer_fact, schedule_reminder, list_my_followups, cancel_reminder,
            request_memory_erasure, notify_customer]


# --------------------------------------------------------------------------- agent


def build_instruction(h: Harness) -> Callable[[ReadonlyContext], str]:
    def instruction(ctx: ReadonlyContext) -> str:
        version, text = procedures.active_procedure(h.var_dir)
        now = ctx.state["temp:now"]
        facts = {key: ctx.state.get(f"user:{key}") for key in FACT_KEYS}
        profile = render_profile({key: fact for key, fact in facts.items() if fact}, now)
        return procedures.render_system_prompt(text, version, profile, ctx.state["app:dispute_review_days"], now)

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
    """before_model_callback: re-send only the turns not yet reflected into long-term memory."""
    reflected = callback_context.state.get("reflected_turns", 0)
    starts = [i for i, content in enumerate(llm_request.contents) if _is_customer_turn(content)]
    if 0 < reflected < len(starts):
        llm_request.contents = llm_request.contents[starts[reflected]:]


def build_agent(h: Harness, disabled_tools: tuple[str, ...] = ()) -> Agent:
    tools = [tool for tool in build_tools(h) if tool.__name__ not in disabled_tools]
    if "load_memory" not in disabled_tools:
        tools.append(load_memory)
    return Agent(
        model=LiteLlm(model=f"deepseek/{DEEPSEEK_MODEL}", api_key=deepseek_api_key()),
        name=AGENT_NAME,
        description="Kestrel card-care assistant",
        instruction=build_instruction(h),
        tools=tools,
        before_agent_callback=forget_expired_facts,
        before_model_callback=window_working_memory,
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
                for call in tool_calls:
                    if call["id"] == part.function_response.id:
                        call["result"] = part.function_response.response
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
                turns.append({"role": "tool", "text": f"called {part.function_call.name}({json.dumps(dict(part.function_call.args or {}))})"})
            elif part.function_response:
                turns.append({"role": "tool", "text": f"{part.function_response.name} -> {json.dumps(part.function_response.response, default=str)[:600]}"})
            elif part.text and not part.thought:
                turns.append({"role": "customer" if event.author == "user" else "assistant", "text": part.text})
    return turns


async def run_turn(h: Harness, user_id: str, session_id: str, text: str, now: str, disabled_tools: tuple[str, ...] = ()) -> dict:
    """One customer message through the agent. Returns what was sent, every tool call with its result, and the reply."""
    session = await h.session_service.get_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)
    turns = group_by_customer_turn(_transcript_turns(session.events)) if session else []
    if session and len(turns) + 1 - session.state.get("reflected_turns", 0) > WORKING_WINDOW_TURNS:
        await reflect_turns(h, user_id, session_id, now, upto=len(turns) + 1 - WORKING_KEEP_TURNS)
    previous = tuple(group[0]["text"] for group in turns[-3:] if group and group[0]["role"] == "customer")
    sent = redact_card_secrets(text, previous)  # card data never enters the session, let alone memory
    runner = Runner(app_name=APP_NAME, agent=build_agent(h, disabled_tools), session_service=h.session_service,
                    memory_service=h.memory_service, auto_create_session=True)
    message = types.Content(role="user", parts=[types.Part(text=sent)])
    events = [event async for event in runner.run_async(
        user_id=user_id, session_id=session_id, new_message=message, state_delta={"temp:now": now, "last_active_at": now}
    )]
    return _turn_record(events, sent)


async def complete_text(prompt: str) -> str:
    response = await litellm.acompletion(
        model=f"deepseek/{DEEPSEEK_MODEL}", api_key=deepseek_api_key(), messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content or ""


async def reflect_turns(h: Harness, user_id: str, session_id: str, now: str, upto: int | None = None) -> dict | None:
    """Reflect the customer turns after the session's reflected mark, up to `upto` (default: all), into one episode."""
    session = await h.session_service.get_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)
    groups = group_by_customer_turn(_transcript_turns(session.events))
    reflected = session.state.get("reflected_turns", 0)
    upto = len(groups) if upto is None else upto
    turns = [turn for group in groups[reflected:upto] for turn in group]
    if not turns:
        return None
    reflection = parse_reflection(await complete_text(reflection_prompt(turns)), user_id, own_case_ids(h.bank_db, user_id))
    sequence = session.state.get("episodes_written", 0) + 1
    episode = build_episode(user_id, session_id, sequence, now, reflection, case_outcomes(h.bank_db, user_id, turns),
                            procedures.active_procedure(h.var_dir)[0], customer_present=not session.state.get("followup_id"))
    await h.memory_service.add_memory(app_name=APP_NAME, user_id=user_id, memories=[MemoryEntry(
        id=episode["episode_id"], author="reflection", timestamp=now,
        content=types.Content(role="user", parts=[types.Part(text=episode["text"])]),
        custom_metadata={"episode": episode},
    )])
    await write_session_state(h, user_id, session_id, {"reflected_turns": upto, "episodes_written": sequence})
    return episode


async def end_session(h: Harness, user_id: str, session_id: str, now: str) -> dict | None:
    """Session concluded: reflect what is not yet reflected, or carry out an erasure the customer asked for."""
    session = await h.session_service.get_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)
    if not session:
        return None
    if session.state.get("erasure_requested_at"):
        await erase_customer_memory(h, user_id)
        return None
    return await reflect_turns(h, user_id, session_id, now)


async def erase_customer_memory(h: Harness, user_id: str) -> dict:
    """Right to erasure: every fact, episode and transcript of this customer. Bank records are not memory and stay."""
    eraser = await h.session_service.create_session(app_name=APP_NAME, user_id=user_id, session_id=f"erasure-{uuid.uuid4().hex[:8]}")
    await h.session_service.append_event(eraser, Event(invocation_id=f"erasure-{uuid.uuid4().hex[:8]}", author="harness",
                                                       actions=EventActions(state_delta={f"user:{key}": None for key in FACT_KEYS})))
    episodes = [e for e in h.memory_service.list_episodes(APP_NAME) if e["user_id"] == user_id]
    for episode in episodes:
        await h.memory_service.delete_memory(app_name=APP_NAME, user_id=user_id, memory_id=episode["episode_id"])
    sessions = (await h.session_service.list_sessions(app_name=APP_NAME, user_id=user_id)).sessions
    for session in sessions:
        await h.session_service.delete_session(app_name=APP_NAME, user_id=user_id, session_id=session.id)
    compact_sqlite(h.sessions_db)
    compact_sqlite(h.episodes_db)
    return {"user_id": user_id, "episodes": len(episodes), "transcripts": len(sessions) - 1}


async def run_maintenance(h: Harness, now: str) -> dict:
    """The harness's memory job: close idle chats, purge expired episodes, delete expired transcripts."""
    closed, deleted = [], []
    for listed in (await h.session_service.list_sessions(app_name=APP_NAME)).sessions:
        last_active = listed.state.get("last_active_at")
        if listed.user_id == OPS_USER:
            continue
        if session_is_idle(last_active, now) and await reflect_turns(h, listed.user_id, listed.id, last_active):
            closed.append(listed.id)
        if transcript_is_expired(last_active, now):
            await h.session_service.delete_session(app_name=APP_NAME, user_id=listed.user_id, session_id=listed.id)
            deleted.append(listed.id)
    expired = [e for e in h.memory_service.list_episodes(APP_NAME) if episode_is_expired(e, now)]
    for episode in expired:
        await h.memory_service.delete_memory(app_name=APP_NAME, user_id=episode["user_id"], memory_id=episode["episode_id"])
    if deleted or expired:
        compact_sqlite(h.sessions_db)
        compact_sqlite(h.episodes_db)
    return {"closed_idle_sessions": closed, "purged_episodes": [e["episode_id"] for e in expired], "deleted_transcripts": deleted}


async def run_followup_session(h: Harness, record: dict, now: str) -> dict:
    """The scheduler's resume callback: a fresh session for the customer, seeded with which follow-up it serves."""
    session_id = f"followup-{record['followup_id']}-{record['attempts'] + 1}"
    await h.session_service.create_session(
        app_name=APP_NAME, user_id=record["user_id"], session_id=session_id,
        state={"followup_id": record["followup_id"], "last_active_at": now},
    )
    turn = await run_turn(h, record["user_id"], session_id, scheduler.followup_trigger_message(record), now)
    episode = await end_session(h, record["user_id"], session_id, now)
    return {"session_id": session_id, "turn": turn, "episode": episode}


async def snapshot(h: Harness, user_ids: list[str]) -> dict:
    """Read-only view of every store, for evidence. Reads state; never writes it."""
    facts, transcripts = {}, {}
    for user_id in user_ids:
        user_state = await h.session_service.get_user_state(app_name=APP_NAME, user_id=user_id)
        facts[user_id] = {key: value for key, value in user_state.items() if value}
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
            print(f"\n[assistant]: {turn['reply']}")
    episode = await end_session(h, user_id, session_id, now or wall_clock_now())
    if episode:
        print(f"\n[memory] episode {episode['episode_id']}: {episode['text']}")


async def tick(var_dir: Path, now: str | None) -> dict:
    """One pass of the harness's background work: fire what is due, then run the memory maintenance job."""
    h = await open_harness(var_dir)
    at = now or wall_clock_now()
    fired = await scheduler.fire_due_followups(h.scheduler_db, h.bank_db, at, lambda record, t: run_followup_session(h, record, t))
    return {"now": at, "followups": fired, "maintenance": await run_maintenance(h, at)}


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
