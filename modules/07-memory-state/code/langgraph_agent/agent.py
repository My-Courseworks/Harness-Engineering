"""Kestrel card-care assistant on LangGraph: the same scenario, the same procedure, LangGraph's own memory primitives.

  working / in-context  the thread's messages, checkpointed per thread by SqliteSaver and re-sent every turn
                        up to a window of WORKING_WINDOW_TURNS customer turns, plus graph-state fields
                        (identity_verified_at, identity_failed_attempts, followup_id, last_active_at,
                        reflected_turns, episodes_written, erasure_requested_at): this conversation only.
                        Threads carry no user, so the harness names them "<user>:<session>". The temp: analog
                        is the per-invocation context (TurnContext.now): never checkpointed.
  semantic              SqliteStore namespace ("facts", <user>), key = fact name: put() overwrites by key;
                        preloaded into the system prompt every turn
  episodic              SqliteStore namespace ("episodes", <user>) with a sqlite-vec index on the
                        reflection text, recalled on demand by the load_memory tool (named after ADK's)
  procedural            the same versioned instruction file the ADK agent reads
  external / retrieval  tools: exact SQL lookups for transactions and cases; search_policy (embeddings)
  parametric            the DeepSeek weights, unmanaged
  prospective           the same harness-owned scheduler as the ADK agent

Run `python -m langgraph_agent.agent chat --user priya` from modules/07-memory-state/code.
"""

import argparse
import asyncio
import json
import sqlite3
import time
import uuid
from contextlib import closing
from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_deepseek import ChatDeepSeek
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, ToolRuntime, tools_condition
from langgraph.runtime import Runtime
from langgraph.store.sqlite import SqliteStore
from langgraph.types import Command

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
from cardcare.retrieval import EMBEDDING_DIMS, embed_texts, search_policy as search_policy_documents

APP_SETTINGS = {"dispute_review_days": 10, "large_dispute_threshold_cents": 20000}
CODE_DIR = Path(__file__).resolve().parent.parent


class SessionState(MessagesState):
    """Checkpointed per thread: lives exactly as long as the conversation (ADK's un-prefixed state)."""

    identity_verified_at: str | None
    identity_failed_attempts: int
    followup_id: str | None
    last_active_at: str | None
    reflected_turns: int
    episodes_written: int
    erasure_requested_at: str | None


@dataclass
class TurnContext:
    """Per-invocation context, never checkpointed: LangGraph's analog of ADK's temp: scope."""

    user_id: str
    now: str


class Harness(NamedTuple):
    var_dir: Path
    checkpointer: SqliteSaver
    store: SqliteStore

    @property
    def bank_db(self) -> Path:
        return self.var_dir / "bank.db"

    @property
    def scheduler_db(self) -> Path:
        return self.var_dir / "scheduler.db"


def open_harness(var_dir: Path) -> Harness:
    """Create (or reopen) every local store under var_dir and seed the bank and the app-wide settings."""
    var_dir.mkdir(parents=True, exist_ok=True)
    world.seed_bank(var_dir / "bank.db")
    scheduler.create_scheduler(var_dir / "scheduler.db")
    checkpointer = SqliteSaver(sqlite3.connect(var_dir / "lg_checkpoints.db", check_same_thread=False))
    store = SqliteStore(
        sqlite3.connect(var_dir / "lg_store.db", check_same_thread=False, isolation_level=None),
        index={"dims": EMBEDDING_DIMS, "embed": embed_texts, "fields": ["text"]},
    )
    store.setup()
    if store.get(("app",), "settings") is None:
        store.put(("app",), "settings", APP_SETTINGS, index=False)
    return Harness(var_dir, checkpointer, store)


def thread_config(user_id: str, session_id: str) -> dict:
    return {"configurable": {"thread_id": f"{user_id}:{session_id}"}}


def _facts(store: SqliteStore, user_id: str) -> dict[str, dict]:
    return {item.key: item.value for item in store.search(("facts", user_id), limit=len(FACT_KEYS))}


def _contact_channel(store: SqliteStore, user_id: str) -> str:
    return _facts(store, user_id).get("contact_channel", {}).get("value", "secure_message")


def _thread_state(h: Harness, user_id: str, session_id: str) -> dict:
    checkpoint = h.checkpointer.get_tuple(thread_config(user_id, session_id))
    return checkpoint.checkpoint["channel_values"] if checkpoint else {}


def _threads(h: Harness) -> list[str]:
    with closing(sqlite3.connect(h.var_dir / "lg_checkpoints.db")) as conn:
        return [row[0] for row in conn.execute("SELECT DISTINCT thread_id FROM checkpoints")]


def compact_sqlite(path: Path) -> None:
    """Deleted rows linger in free pages and in the WAL until the file is rewritten; erasure has to reach those too.

    VACUUM first (in WAL mode it writes the rebuilt pages to the WAL), then checkpoint them into the main file
    and truncate the WAL, so neither file still holds the deleted bytes.
    """
    with closing(sqlite3.connect(path)) as conn:
        conn.execute("VACUUM")
        conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")


# --------------------------------------------------------------------------- tools


def build_tools(h: Harness) -> list:
    """Tools over this harness's stores. The customer is always runtime.context.user_id, never a model argument."""

    @tool
    def verify_identity(card_last4: str, postal_code: str, runtime: ToolRuntime[TurnContext]) -> Command:
        """Verify the logged-in customer with their card's last 4 digits and billing ZIP, as the customer typed them.
        Valid for 15 minutes. Locks after 3 failed attempts in a conversation."""
        failed = runtime.state.get("identity_failed_attempts") or 0
        if failed >= MAX_VERIFICATION_ATTEMPTS:
            result, update = {"verified": False, "error": "verification is locked for this conversation after 3 failed "
                                                          "attempts; the customer must call Kestrel"}, {}
        elif not world.identity_matches(h.bank_db, runtime.context.user_id, card_last4, postal_code):
            result = {"verified": False, "error": "those details do not match this customer", "attempts_left": MAX_VERIFICATION_ATTEMPTS - failed - 1}
            update = {"identity_failed_attempts": failed + 1}
        else:
            result, update = {"verified": True, "valid_for_minutes": 15}, {"identity_verified_at": runtime.context.now}
        return Command(update={**update, "messages": [ToolMessage(json.dumps(result), tool_call_id=runtime.tool_call_id)]})

    @tool
    def find_transactions(runtime: ToolRuntime[TurnContext], merchant: str | None = None) -> str:
        """List the customer's posted transactions, optionally only those whose merchant name contains `merchant`."""
        return json.dumps({"transactions": world.find_transactions(h.bank_db, runtime.context.user_id, merchant, runtime.context.now)})

    @tool
    def file_dispute(transaction_id: str, reason: str, runtime: ToolRuntime[TurnContext], evidence_note: str | None = None) -> str:
        """File a dispute for one transaction. reason: cancelled_subscription, not_recognized, duplicate,
        goods_not_received or incorrect_amount. evidence_note: anything the customer supplied (e.g. a cancellation
        reference). Requires a verify_identity in the last 15 minutes. Schedules the case follow-up automatically."""
        error = verification_gate_error(runtime.state.get("identity_verified_at"), runtime.context.now, "filing a dispute")
        if error:
            return json.dumps({"error": error})
        settings = runtime.store.get(("app",), "settings").value
        return json.dumps(desk.file_dispute_with_followup(
            h.bank_db, h.scheduler_db, runtime.context.user_id, transaction_id, reason, evidence_note,
            runtime.context.now, settings["dispute_review_days"], settings["large_dispute_threshold_cents"],
        ))

    @tool
    def add_case_evidence(case_id: str, evidence_note: str, runtime: ToolRuntime[TurnContext]) -> str:
        """Attach more evidence (e.g. a cancellation reference the customer found later) to one of their open cases."""
        return json.dumps(world.add_case_evidence(h.bank_db, runtime.context.user_id, case_id, redact_card_secrets(evidence_note), runtime.context.now))

    @tool
    def get_case_status(runtime: ToolRuntime[TurnContext], case_id: str | None = None) -> str:
        """Current status of one dispute case, or of all this customer's cases when case_id is omitted."""
        return json.dumps({"cases": world.list_cases(h.bank_db, runtime.context.user_id, case_id)})

    @tool
    def search_policy(question: str) -> str:
        """Search Kestrel's policy documents (fees, dispute rules, travel notices, contact channels)."""
        return json.dumps({"documents": search_policy_documents(question)})

    @tool
    def remember_customer_fact(key: str, value: str, runtime: ToolRuntime[TurnContext], valid_until: str | None = None) -> str:
        """Store a fact the customer stated. key: contact_channel (value email, sms or secure_message) or
        travel_notice (value = destination, valid_until = return date YYYY-MM-DD). Replaces any earlier value."""
        if key in FACT_KEYS_NEEDING_VERIFICATION:
            error = verification_gate_error(runtime.state.get("identity_verified_at"), runtime.context.now, f"changing {key}")
            if error:
                return json.dumps({"error": error})
        try:
            fact = build_fact(key, value, valid_until, runtime.context.now)
        except ValueError as exc:
            return json.dumps({"error": str(exc)})
        namespace = ("facts", runtime.context.user_id)
        previous = runtime.store.get(namespace, key)
        runtime.store.put(namespace, key, fact, index=False)  # keyed overwrite: the new value replaces the old
        return json.dumps({"stored": {key: fact}, "replaced": previous.value["value"] if previous else None})

    @tool
    def forget_customer_fact(key: str, runtime: ToolRuntime[TurnContext]) -> str:
        """Delete a stored customer fact (contact_channel or travel_notice) at the customer's request."""
        if key not in FACT_KEYS:
            return json.dumps({"error": f"unknown fact {key}"})
        namespace = ("facts", runtime.context.user_id)
        had_value = runtime.store.get(namespace, key) is not None
        runtime.store.delete(namespace, key)
        return json.dumps({"forgotten": key, "had_value": had_value,
                           "note": f"deleted from memory now; conversation transcripts are deleted after {TRANSCRIPT_RETENTION_DAYS} "
                                   "days, or at once if the customer asks to erase everything"})

    @tool
    def schedule_reminder(note: str, remind_on: str, runtime: ToolRuntime[TurnContext]) -> str:
        """Schedule a reminder message to the customer on a future date (YYYY-MM-DD). Only when the customer asks for one."""
        return json.dumps(desk.schedule_customer_reminder(h.scheduler_db, runtime.context.user_id, note, remind_on, runtime.context.now))

    @tool
    def list_my_followups(runtime: ToolRuntime[TurnContext]) -> str:
        """What is scheduled for this customer (reminders and case follow-ups), when, and on which channel it will arrive."""
        channel = _contact_channel(runtime.store, runtime.context.user_id)
        records = [r for r in scheduler.user_followups(h.scheduler_db, runtime.context.user_id) if r["status"] in ("pending", "awaiting_approval")]
        return json.dumps({"scheduled": [scheduler.customer_view(r, channel) for r in records]})

    @tool
    def cancel_reminder(followup_id: str, runtime: ToolRuntime[TurnContext]) -> str:
        """Cancel one of the customer's own reminders before it is sent (ids come from list_my_followups)."""
        record = scheduler.get_followup(h.scheduler_db, followup_id)
        if not record or record["user_id"] != runtime.context.user_id or record["action"] != "customer_reminder":
            return json.dumps({"error": f"{followup_id} is not one of this customer's reminders"})
        cancelled = scheduler.cancel_followup(h.scheduler_db, followup_id, runtime.context.user_id, runtime.context.now)
        return json.dumps({"cancelled": followup_id} if cancelled else {"error": f"{followup_id} has already been sent or cancelled"})

    @tool
    def request_memory_erasure(runtime: ToolRuntime[TurnContext]) -> Command:
        """The customer asks to delete everything remembered about them. Runs when this conversation ends."""
        result = {"scheduled": "when this conversation ends, every remembered fact, every past-conversation summary and every "
                               "conversation transcript, including this one, will be erased",
                  "kept": "dispute cases, transactions and messages already sent are bank records with their own legal retention"}
        return Command(update={"erasure_requested_at": runtime.context.now,
                               "messages": [ToolMessage(json.dumps(result), tool_call_id=runtime.tool_call_id)]})

    @tool
    def notify_customer(message: str, runtime: ToolRuntime[TurnContext]) -> str:
        """Send the customer one message on their contact channel. Only for scheduled follow-ups; one per follow-up."""
        followup_id = runtime.state.get("followup_id")
        if not followup_id:
            return json.dumps({"error": "notify_customer is only for scheduled follow-ups; in a live conversation, just reply"})
        if any(m["followup_id"] == followup_id and m["status"] != "rejected" for m in world.outbound_messages(h.bank_db)):
            return json.dumps({"error": "this follow-up has already produced its one message"})
        held = scheduler.get_followup(h.scheduler_db, followup_id)["approval"] != "none"
        channel = _contact_channel(runtime.store, runtime.context.user_id)
        sent = world.record_outbound_message(h.bank_db, runtime.context.user_id, channel, redact_card_secrets(message), followup_id,
                                             held, runtime.context.now)
        return json.dumps({"channel": channel, "message_id": sent["message_id"],
                           "status": "held for a Kestrel reviewer to approve before it is sent" if held else "sent"})

    @tool
    def load_memory(query: str, runtime: ToolRuntime[TurnContext]) -> str:
        """Search reflections on this customer's past conversations. Use when they refer to an earlier conversation."""
        items = runtime.store.search(("episodes", runtime.context.user_id), query=query, limit=3)
        return json.dumps({"memories": [{"at": item.value["at"], "text": item.value["text"], "similarity": round(item.score or 0, 3)} for item in items]})

    return [verify_identity, find_transactions, file_dispute, add_case_evidence, get_case_status, search_policy,
            remember_customer_fact, forget_customer_fact, schedule_reminder, list_my_followups, cancel_reminder,
            request_memory_erasure, notify_customer, load_memory]


# --------------------------------------------------------------------------- graph


def _model() -> ChatDeepSeek:
    return ChatDeepSeek(model=DEEPSEEK_MODEL, api_key=deepseek_api_key())


def windowed_messages(messages: list, reflected_turns: int) -> list:
    """Re-send only the turns not yet reflected into long-term memory (cut at a customer turn, so tool pairs stay whole)."""
    starts = [i for i, message in enumerate(messages) if isinstance(message, HumanMessage)]
    return messages[starts[reflected_turns]:] if 0 < reflected_turns < len(starts) else messages


def build_graph(h: Harness, disabled_tools: tuple[str, ...] = ()):
    tools = [t for t in build_tools(h) if t.name not in disabled_tools]
    model = _model().bind_tools(tools)

    def forget_expired_facts(state: SessionState, runtime: Runtime[TurnContext]) -> dict:
        """Mirror of the ADK before_agent_callback: an expired travel notice is deleted, not merely hidden."""
        for key, fact in _facts(runtime.store, runtime.context.user_id).items():
            if fact_is_expired(fact, runtime.context.now):
                runtime.store.delete(("facts", runtime.context.user_id), key)
        return {}

    def call_model(state: SessionState, runtime: Runtime[TurnContext]) -> dict:
        version, text = procedures.active_procedure(h.var_dir)
        profile = render_profile(_facts(runtime.store, runtime.context.user_id), runtime.context.now)
        settings = runtime.store.get(("app",), "settings").value
        system = procedures.render_system_prompt(text, version, profile, settings["dispute_review_days"], runtime.context.now)
        context = windowed_messages(state["messages"], state.get("reflected_turns") or 0)
        response = model.invoke([SystemMessage(system), *context])
        if not response.tool_calls and not (isinstance(response.content, str) and response.content.strip()):
            response = model.invoke([SystemMessage(system), *context])  # one retry: an empty turn is a model stall, not an answer
        return {"messages": [response]}

    graph = StateGraph(SessionState, context_schema=TurnContext)
    graph.add_node("forget_expired_facts", forget_expired_facts)
    graph.add_node("agent", call_model)
    graph.add_node("tools", ToolNode(tools))
    graph.add_edge(START, "forget_expired_facts")
    graph.add_edge("forget_expired_facts", "agent")
    graph.add_conditional_edges("agent", tools_condition)
    graph.add_edge("tools", "agent")
    return graph.compile(checkpointer=h.checkpointer, store=h.store)


# --------------------------------------------------------------------------- turns, sessions, follow-ups


def _turn_record(messages: list, customer_text: str) -> dict:
    tool_calls, reply = [], []
    for message in messages:
        if isinstance(message, AIMessage):
            tool_calls += [{"name": c["name"], "args": c["args"], "result": None, "id": c["id"]} for c in message.tool_calls]
            if isinstance(message.content, str) and message.content.strip():
                reply.append(message.content)
        elif isinstance(message, ToolMessage):
            for call in tool_calls:
                if call["id"] == message.tool_call_id:
                    try:
                        call["result"] = json.loads(message.content)
                    except (TypeError, json.JSONDecodeError):
                        call["result"] = message.content
    for call in tool_calls:
        call.pop("id")
    return {"customer": customer_text, "tool_calls": tool_calls, "reply": "\n".join(reply).strip()}


def _transcript_turns(messages: list) -> list[dict]:
    turns = []
    for message in messages:
        if isinstance(message, HumanMessage):
            turns.append({"role": "customer", "text": message.content})
        elif isinstance(message, AIMessage):
            turns += [{"role": "tool", "text": f"called {c['name']}({json.dumps(c['args'])})"} for c in message.tool_calls]
            if isinstance(message.content, str) and message.content.strip():
                turns.append({"role": "assistant", "text": message.content})
        elif isinstance(message, ToolMessage):
            turns.append({"role": "tool", "text": f"{message.name} -> {str(message.content)[:600]}"})
    return turns


def run_turn(h: Harness, user_id: str, session_id: str, text: str, now: str, disabled_tools: tuple[str, ...] = ()) -> dict:
    """One customer message through the graph. Returns what was sent, every tool call with its result, and the reply."""
    state = _thread_state(h, user_id, session_id)
    turns = group_by_customer_turn(_transcript_turns(state.get("messages", [])))
    if len(turns) + 1 - (state.get("reflected_turns") or 0) > WORKING_WINDOW_TURNS:
        reflect_turns(h, user_id, session_id, now, upto=len(turns) + 1 - WORKING_KEEP_TURNS)
    previous = tuple(group[0]["text"] for group in turns[-3:] if group and group[0]["role"] == "customer")
    sent = redact_card_secrets(text, previous)  # card data never enters the thread, let alone memory
    graph = build_graph(h, disabled_tools)
    already = len(state.get("messages", []))
    result = graph.invoke({"messages": [HumanMessage(sent)], "last_active_at": now}, thread_config(user_id, session_id),
                          context=TurnContext(user_id=user_id, now=now))
    return _turn_record(result["messages"][already:], sent)


def complete_text(prompt: str) -> str:
    return _model().invoke(prompt).content


def reflect_turns(h: Harness, user_id: str, session_id: str, now: str, upto: int | None = None) -> dict | None:
    """Reflect the customer turns after the thread's reflected mark, up to `upto` (default: all), into one episode."""
    state = _thread_state(h, user_id, session_id)
    groups = group_by_customer_turn(_transcript_turns(state.get("messages", [])))
    reflected = state.get("reflected_turns") or 0
    upto = len(groups) if upto is None else upto
    turns = [turn for group in groups[reflected:upto] for turn in group]
    if not turns:
        return None
    reflection = parse_reflection(complete_text(reflection_prompt(turns)), user_id, own_case_ids(h.bank_db, user_id))
    sequence = (state.get("episodes_written") or 0) + 1
    episode = build_episode(user_id, session_id, sequence, now, reflection, case_outcomes(h.bank_db, user_id, turns),
                            procedures.active_procedure(h.var_dir)[0], customer_present=not state.get("followup_id"))
    h.store.put(("episodes", user_id), episode["episode_id"], episode)  # indexed on "text" for semantic recall
    build_graph(h).update_state(thread_config(user_id, session_id), {"reflected_turns": upto, "episodes_written": sequence})
    return episode


def end_session(h: Harness, user_id: str, session_id: str, now: str) -> dict | None:
    """Session concluded: reflect what is not yet reflected, or carry out an erasure the customer asked for."""
    state = _thread_state(h, user_id, session_id)
    if not state:
        return None
    if state.get("erasure_requested_at"):
        erase_customer_memory(h, user_id)
        return None
    return reflect_turns(h, user_id, session_id, now)


def list_episodes(store: SqliteStore) -> list[dict]:
    episodes = []
    for namespace in store.list_namespaces(prefix=("episodes",)):
        episodes += [item.value for item in store.search(namespace, limit=1000)]
    return sorted(episodes, key=lambda e: e["at"])


def erase_customer_memory(h: Harness, user_id: str) -> dict:
    """Right to erasure: every fact, episode and transcript of this customer. Bank records are not memory and stay."""
    for key in FACT_KEYS:
        h.store.delete(("facts", user_id), key)
    episodes = [e for e in list_episodes(h.store) if e["user_id"] == user_id]
    for episode in episodes:
        h.store.delete(("episodes", user_id), episode["episode_id"])
    threads = [t for t in _threads(h) if t.startswith(f"{user_id}:")]
    for thread_id in threads:
        h.checkpointer.delete_thread(thread_id)
    compact_sqlite(h.var_dir / "lg_checkpoints.db")
    compact_sqlite(h.var_dir / "lg_store.db")
    return {"user_id": user_id, "episodes": len(episodes), "transcripts": len(threads)}


def run_maintenance(h: Harness, now: str) -> dict:
    """The harness's memory job: close idle chats, purge expired episodes, delete expired transcripts."""
    closed, deleted = [], []
    for thread_id in _threads(h):
        user_id, session_id = thread_id.split(":", 1)
        last_active = _thread_state(h, user_id, session_id).get("last_active_at")
        if session_is_idle(last_active, now) and reflect_turns(h, user_id, session_id, last_active):
            closed.append(session_id)
        if transcript_is_expired(last_active, now):
            h.checkpointer.delete_thread(thread_id)
            deleted.append(session_id)
    expired = [e for e in list_episodes(h.store) if episode_is_expired(e, now)]
    for episode in expired:
        h.store.delete(("episodes", episode["user_id"]), episode["episode_id"])
    if deleted or expired:
        compact_sqlite(h.var_dir / "lg_checkpoints.db")
        compact_sqlite(h.var_dir / "lg_store.db")
    return {"closed_idle_sessions": closed, "purged_episodes": [e["episode_id"] for e in expired], "deleted_transcripts": deleted}


def run_followup_session(h: Harness, record: dict, now: str) -> dict:
    """The scheduler's resume callback: a fresh thread for the customer, seeded with which follow-up it serves."""
    session_id = f"followup-{record['followup_id']}-{record['attempts'] + 1}"
    build_graph(h).update_state(thread_config(record["user_id"], session_id), {"followup_id": record["followup_id"], "last_active_at": now})
    turn = run_turn(h, record["user_id"], session_id, scheduler.followup_trigger_message(record), now)
    episode = end_session(h, record["user_id"], session_id, now)
    return {"session_id": session_id, "turn": turn, "episode": episode}


def snapshot(h: Harness, user_ids: list[str]) -> dict:
    """Read-only view of every store, for evidence."""
    threads = _threads(h)
    channels = set()
    for thread_id in threads:
        checkpoint = h.checkpointer.get_tuple({"configurable": {"thread_id": thread_id}})
        channels |= {name for name in checkpoint.checkpoint["channel_values"] if not name.startswith("branch:")}
    return {
        "facts": {user_id: _facts(h.store, user_id) for user_id in user_ids},
        "episodes": list_episodes(h.store),
        "persisted_state_keys": sorted(channels),
        "persisted_clock_keys": sorted(channels & {"now"}),
        "threads": sorted(threads),
        "followups": scheduler.list_followups(h.scheduler_db),
        "outbound_messages": world.outbound_messages(h.bank_db),
        "cases": world.all_cases(h.bank_db),
        "procedure": procedures.load_registry(h.var_dir),
        "procedure_text": procedures.active_procedure(h.var_dir)[1],
        "transcripts": {user_id: sorted(t.split(":", 1)[1] for t in threads if t.startswith(f"{user_id}:")) for user_id in user_ids},
    }


# --------------------------------------------------------------------------- interactive CLI


def chat(var_dir: Path, user_id: str, session_id: str | None, now: str | None) -> None:
    h = open_harness(var_dir)
    session_id = session_id or f"chat-{uuid.uuid4().hex[:8]}"
    print(f"Kestrel card-care (LangGraph) | customer={user_id} session={session_id} | 'exit' or end-of-input ends the session")
    while True:
        try:
            text = input("\n[you]: ").strip()
        except EOFError:  # the tab was closed: the session still ends properly
            break
        if text in ("exit", "quit"):
            break
        if text:
            turn = run_turn(h, user_id, session_id, text, now or wall_clock_now())
            for call in turn["tool_calls"]:
                print(f"  [tool] {call['name']}({json.dumps(call['args'])})")
            print(f"\n[assistant]: {turn['reply']}")
    episode = end_session(h, user_id, session_id, now or wall_clock_now())
    if episode:
        print(f"\n[memory] episode {episode['episode_id']}: {episode['text']}")


async def tick(var_dir: Path, now: str | None) -> dict:
    """One pass of the harness's background work: fire what is due, then run the memory maintenance job."""
    h = open_harness(var_dir)
    at = now or wall_clock_now()
    fired = await scheduler.fire_due_followups(h.scheduler_db, h.bank_db, at, lambda record, t: run_followup_session(h, record, t))
    return {"now": at, "followups": fired, "maintenance": run_maintenance(h, at)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("command", choices=["chat", "tick"])
    parser.add_argument("--user", default="priya", choices=[c[0] for c in world.CUSTOMERS])
    parser.add_argument("--session", help="continue an existing session id")
    parser.add_argument("--now", help="override the clock (ISO-8601), e.g. 2026-11-19T10:00:00Z")
    parser.add_argument("--loop", type=int, metavar="SECONDS", help="tick: repeat every SECONDS on the wall clock")
    parser.add_argument("--var-dir", type=Path, default=CODE_DIR / "var" / "langgraph" / "interactive")
    args = parser.parse_args()
    if args.command == "chat":
        chat(args.var_dir, args.user, args.session, args.now)
        return
    while True:
        print(json.dumps(asyncio.run(tick(args.var_dir, args.now)), indent=2))
        if not args.loop:
            break
        time.sleep(args.loop)


if __name__ == "__main__":
    main()
