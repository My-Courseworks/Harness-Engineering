"""Kestrel card-care assistant on Google ADK: where each of the module's seven memory types lives.

  working / in-context  Session events (DatabaseSessionService on SQLite) re-sent every turn, plus State:
                          identity_verified_at, followup_id   un-prefixed: this conversation only
                          user:contact_channel, user:travel_notice   this customer, every session
                          app:dispute_review_days, app:large_dispute_threshold_cents   every customer
                          temp:now   the harness clock for this invocation; never persisted
  semantic              the user: keys above: a closed schema, timestamped, overwritten by key,
                        preloaded into the instruction every turn (small and always relevant)
  episodic              EpisodeMemoryService: one reflection per finished session, recalled on
                        demand with ADK's load_memory tool (large and mostly irrelevant)
  procedural            the versioned instruction (cardcare/procedure_versions + the registry in var/)
  external / retrieval  tools: exact SQL lookups for transactions and cases; search_policy (embeddings)
  parametric            the DeepSeek weights; nothing here manages them, which is the point
  prospective           cardcare/scheduler.py: file_dispute and schedule_reminder write records,
                        the harness fires them into fresh sessions (`followups` command)

Run `python -m adk_agent.agent chat --user priya` from modules/07-memory-state/code.
"""

import argparse
import asyncio
import json
import re
import sqlite3
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
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.adk.tools import ToolContext, load_memory
from google.genai import types

from cardcare import desk, procedures, scheduler, world
from cardcare.clock import wall_clock_now
from cardcare.episodes import build_episode, case_outcomes, parse_reflection, reflection_prompt
from cardcare.memory_policy import (
    FACT_KEYS,
    FACT_KEYS_NEEDING_VERIFICATION,
    build_fact,
    episode_is_expired,
    fact_is_expired,
    redact_card_secrets,
    render_profile,
)
from cardcare.model_config import DEEPSEEK_MODEL, deepseek_api_key
from cardcare.retrieval import embed_texts, search_policy as search_policy_documents, top_matches

APP_NAME = "kestrel_card_care"
AGENT_NAME = "card_care"
APP_SETTINGS = {"app:dispute_review_days": 10, "app:large_dispute_threshold_cents": 20000}
CODE_DIR = Path(__file__).resolve().parent.parent


# --------------------------------------------------------------------------- episodic memory


class EpisodeMemoryService(BaseMemoryService):
    """ADK long-term episodic memory: one reflection per finished session, scoped by (app, user).

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
            "Raw sessions are never copied into long-term memory; the harness writes one reflection per session with add_memory()."
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


async def purge_expired_episodes(h: Harness, now: str) -> list[str]:
    """The retention job: forgetting on purpose, through the memory service's delete path."""
    expired = [e for e in h.memory_service.list_episodes(APP_NAME) if episode_is_expired(e, now)]
    for episode in expired:
        await h.memory_service.delete_memory(app_name=APP_NAME, user_id=episode["user_id"], memory_id=episode["episode_id"])
    return [episode["episode_id"] for episode in expired]


async def seed_app_settings(h: Harness) -> None:
    """app: state can only change through an event, so ops writes it as an EventActions.state_delta."""
    ops_session = await h.session_service.get_session(app_name=APP_NAME, user_id="ops", session_id="ops-settings")
    if ops_session and all(key in ops_session.state for key in APP_SETTINGS):
        return
    ops_session = ops_session or await h.session_service.create_session(app_name=APP_NAME, user_id="ops", session_id="ops-settings")
    event = Event(invocation_id=f"ops-{uuid.uuid4().hex[:8]}", author="ops", actions=EventActions(state_delta=dict(APP_SETTINGS)))
    await h.session_service.append_event(ops_session, event)


# --------------------------------------------------------------------------- tools


def build_tools(h: Harness) -> list[Callable]:
    """Tool functions over this harness's stores. The customer is always tool_context.user_id, never a model argument."""

    def verify_identity(card_last4: str, postal_code: str, tool_context: ToolContext) -> dict:
        """Verify the logged-in customer with their card's last 4 digits and billing ZIP. Lasts for this conversation only."""
        if not world.identity_matches(h.bank_db, tool_context.user_id, card_last4, postal_code):
            return {"verified": False, "error": "those details do not match this customer"}
        tool_context.state["identity_verified_at"] = tool_context.state["temp:now"]
        return {"verified": True}

    def find_transactions(tool_context: ToolContext, merchant: str | None = None) -> dict:
        """List the customer's posted transactions, optionally only those whose merchant name contains `merchant`."""
        return {"transactions": world.find_transactions(h.bank_db, tool_context.user_id, merchant, tool_context.state["temp:now"])}

    def file_dispute(transaction_id: str, reason: str, tool_context: ToolContext, evidence_note: str | None = None) -> dict:
        """File a dispute for one transaction. reason: cancelled_subscription, not_recognized, duplicate,
        goods_not_received or incorrect_amount. evidence_note: anything the customer supplied (e.g. a cancellation
        reference). Requires verify_identity in this conversation. Schedules the case follow-up automatically."""
        if not tool_context.state.get("identity_verified_at"):
            return {"error": "identity not verified in this conversation; call verify_identity first"}
        result = desk.file_dispute_with_followup(
            h.bank_db, h.scheduler_db, tool_context.user_id, transaction_id, reason, evidence_note,
            tool_context.state["temp:now"], tool_context.state["app:dispute_review_days"],
            tool_context.state["app:large_dispute_threshold_cents"],
        )
        if "followup" in result:
            channel = (tool_context.state.get("user:contact_channel") or {}).get("value", "secure_message")
            result["followup"]["channel"] = channel
        return result

    def get_case_status(tool_context: ToolContext, case_id: str | None = None) -> dict:
        """Current status of one dispute case, or of all this customer's cases when case_id is omitted."""
        return {"cases": world.list_cases(h.bank_db, tool_context.user_id, case_id)}

    def search_policy(question: str) -> dict:
        """Search Kestrel's policy documents (fees, dispute rules, travel notices, contact channels)."""
        return {"documents": search_policy_documents(question)}

    def remember_customer_fact(key: str, value: str, tool_context: ToolContext, valid_until: str | None = None) -> dict:
        """Store a fact the customer stated. key: contact_channel (value email, sms or secure_message) or
        travel_notice (value = destination, valid_until = return date YYYY-MM-DD). Replaces any earlier value."""
        if key in FACT_KEYS_NEEDING_VERIFICATION and not tool_context.state.get("identity_verified_at"):
            return {"error": f"changing {key} requires verify_identity in this conversation"}
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
        return {"forgotten": key, "had_value": had_value}

    def schedule_reminder(note: str, remind_on: str, tool_context: ToolContext) -> dict:
        """Schedule a reminder message to the customer on a future date (YYYY-MM-DD), sent on their contact channel."""
        return desk.schedule_customer_reminder(h.scheduler_db, tool_context.user_id, note, remind_on, tool_context.state["temp:now"])

    def notify_customer(message: str, tool_context: ToolContext) -> dict:
        """Send the customer one message on their contact channel. Only for scheduled follow-ups."""
        followup_id = tool_context.state.get("followup_id")
        if not followup_id:
            return {"error": "notify_customer is only for scheduled follow-ups; in a live conversation, just reply"}
        channel = (tool_context.state.get("user:contact_channel") or {}).get("value", "secure_message")
        sent = world.record_outbound_message(
            h.bank_db, tool_context.user_id, channel, redact_card_secrets(message), followup_id, tool_context.state["temp:now"]
        )
        return {"sent": True, "channel": channel, "message_id": sent["message_id"]}

    return [verify_identity, find_transactions, file_dispute, get_case_status, search_policy,
            remember_customer_fact, forget_customer_fact, schedule_reminder, notify_customer]


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


async def run_turn(h: Harness, user_id: str, session_id: str, text: str, now: str, disabled_tools: tuple[str, ...] = ()) -> dict:
    """One customer message through the agent. Returns what was sent, every tool call with its result, and the reply."""
    runner = Runner(app_name=APP_NAME, agent=build_agent(h, disabled_tools), session_service=h.session_service,
                    memory_service=h.memory_service, auto_create_session=True)
    sent = redact_card_secrets(text)  # card numbers never enter the session, let alone memory
    message = types.Content(role="user", parts=[types.Part(text=sent)])
    events = [event async for event in runner.run_async(
        user_id=user_id, session_id=session_id, new_message=message, state_delta={"temp:now": now}
    )]
    return _turn_record(events, sent)


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


async def complete_text(prompt: str) -> str:
    response = await litellm.acompletion(
        model=f"deepseek/{DEEPSEEK_MODEL}", api_key=deepseek_api_key(), messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content or ""


async def end_session(h: Harness, user_id: str, session_id: str, now: str) -> dict:
    """Session concluded: reflect on it and write one episode to long-term memory."""
    session = await h.session_service.get_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)
    turns = _transcript_turns(session.events)
    reflection = parse_reflection(await complete_text(reflection_prompt(turns)))
    episode = build_episode(user_id, session_id, now, reflection, case_outcomes(h.bank_db, user_id, turns),
                            procedures.active_procedure(h.var_dir)[0])
    await h.memory_service.add_memory(app_name=APP_NAME, user_id=user_id, memories=[MemoryEntry(
        id=episode["episode_id"], author="reflection", timestamp=now,
        content=types.Content(role="user", parts=[types.Part(text=episode["text"])]),
        custom_metadata={"episode": episode},
    )])
    return episode


async def run_followup_session(h: Harness, record: dict, now: str) -> dict:
    """The scheduler's resume callback: a fresh session for the customer, seeded with which follow-up it serves."""
    session_id = f"followup-{record['followup_id']}-{record['attempts'] + 1}"
    await h.session_service.create_session(
        app_name=APP_NAME, user_id=record["user_id"], session_id=session_id, state={"followup_id": record["followup_id"]}
    )
    turn = await run_turn(h, record["user_id"], session_id, scheduler.followup_trigger_message(record), now)
    episode = await end_session(h, record["user_id"], session_id, now)
    return {"session_id": session_id, "turn": turn, "episode": episode}


async def snapshot(h: Harness, user_ids: list[str]) -> dict:
    """Read-only view of every store, for evidence. Reads state; never writes it."""
    facts = {}
    for user_id in user_ids:
        user_state = await h.session_service.get_user_state(app_name=APP_NAME, user_id=user_id)
        facts[user_id] = {key: value for key, value in user_state.items() if value}
    with closing(sqlite3.connect(h.var_dir / "adk_sessions.db")) as conn:
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
    }


# --------------------------------------------------------------------------- interactive CLI


async def chat(var_dir: Path, user_id: str, session_id: str | None, now: str | None) -> None:
    h = await open_harness(var_dir)
    session_id = session_id or f"chat-{uuid.uuid4().hex[:8]}"
    print(f"Kestrel card-care (ADK) | customer={user_id} session={session_id} | 'exit' ends the session and writes its episode")
    took_turn = False
    while True:
        text = (await asyncio.to_thread(input, "\n[you]: ")).strip()
        if text in ("exit", "quit"):
            break
        if text:
            turn = await run_turn(h, user_id, session_id, text, now or wall_clock_now())
            took_turn = True
            for call in turn["tool_calls"]:
                print(f"  [tool] {call['name']}({json.dumps(call['args'])})")
            print(f"\n[assistant]: {turn['reply']}")
    if took_turn:
        episode = await end_session(h, user_id, session_id, now or wall_clock_now())
        print(f"\n[memory] episode {episode['episode_id']}: {episode['text']}")


async def fire_followups(var_dir: Path, now: str | None) -> None:
    h = await open_harness(var_dir)
    outcomes = await scheduler.fire_due_followups(
        h.scheduler_db, h.bank_db, now or wall_clock_now(), lambda record, at: run_followup_session(h, record, at)
    )
    print(json.dumps(outcomes, indent=2) if outcomes else "nothing due")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("command", choices=["chat", "followups"])
    parser.add_argument("--user", default="priya", choices=[c[0] for c in world.CUSTOMERS])
    parser.add_argument("--session", help="continue an existing session id")
    parser.add_argument("--now", help="override the clock (ISO-8601), e.g. 2026-11-19T10:00:00Z")
    parser.add_argument("--var-dir", type=Path, default=CODE_DIR / "var" / "adk" / "interactive")
    args = parser.parse_args()
    if args.command == "chat":
        asyncio.run(chat(args.var_dir, args.user, args.session, args.now))
    else:
        asyncio.run(fire_followups(args.var_dir, args.now))


if __name__ == "__main__":
    main()
