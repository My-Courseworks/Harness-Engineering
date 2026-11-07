"""Kestrel card-care assistant on LangGraph: the same scenario, the same procedure, LangGraph's own memory primitives.

  working / in-context  the thread's messages, checkpointed per thread by SqliteSaver and re-sent every turn
                        up to a window of WORKING_WINDOW_TURNS customer turns (each message capped in size), plus
                        graph-state fields (identity_verified_at, first_active_at, last_active_at, reflected_turns,
                        episodes_written): this conversation only. Account-level state (the verification lockout,
                        the erasure generations) lives in bank.db and privacy.db, outside every thread.
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
What kind of session a turn runs in (live, or a follow-up the scheduler started) is passed in by whoever starts it
(cardcare/sessions.py), never read back from the thread.

Run `python -m langgraph_agent.agent chat --user priya` from modules/07-memory-state/code.
"""

import argparse
import asyncio
import json
import re
import sqlite3
from typing import Annotated
import time
import uuid
from contextlib import closing
from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_deepseek import ChatDeepSeek
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, ToolRuntime, tools_condition
from langgraph.runtime import Runtime
from langgraph.store.sqlite import SqliteStore
from langgraph.types import Command
from pydantic import BaseModel

from cardcare import desk, privacy, procedures, scheduler, world
from cardcare.clock import parse_instant, wall_clock_now
from cardcare.episodes import build_episode, case_outcomes, group_by_customer_turn, own_case_ids, parse_reflection, reflection_prompt
from cardcare.masking import MASK_TOKEN, mask_card_numbers, mask_customer_message, mask_customer_text, removed_fragments, scrub_fragments
from cardcare.memory_policy import (
    DEFAULT_CHANNEL,
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
    render_profile,
    session_is_idle,
    transcript_is_expired,
    typed_in_session,
    verification_gate_error,
)
from cardcare.model_config import DEEPSEEK_MODEL, deepseek_api_key
from cardcare.retrieval import EMBEDDING_DIMS, embed_texts, search_policy as search_policy_documents
from cardcare.sessions import LIVE, SessionKind, followup_kind
from cardcare.tool_args import (
    CardLast4, CaseId, CustomerMessage, DisputeReason, EvidenceNote, FactKey, FactValue, FollowupId, MalformedTool, MemoryQuery,
    Merchant, NewEvidence, OptionalCaseId, PolicyQuestion, PostalCode, RemindAt, ReminderNote, RemindOn, TimeZone, TransactionId,
    ValidUntil,
)

APP_SETTINGS = {"dispute_review_days": 10, "large_dispute_threshold_cents": 20000}
CODE_DIR = Path(__file__).resolve().parent.parent
ERASED_IN_THIS_CONVERSATION = ("the customer asked for erasure in this conversation (or an erasure has run since it started), so "
                               "nothing more can be stored for them here; tell them to set it up again in a new conversation")


def latest(current: str | None, update: str | None) -> str | None:
    """Reducer: parallel tool calls in one ToolNode step may each write this channel; keep the latest instant."""
    return max(filter(None, (current, update)), default=None)


class SessionState(MessagesState):
    """Checkpointed per thread: lives exactly as long as the conversation (ADK's un-prefixed state).

    Only identity_verified_at is written by tools, so only it needs a reducer; a plain channel written twice in
    one step raises InvalidUpdateError and, before round 3, left the thread with unanswered tool calls."""

    identity_verified_at: Annotated[str | None, latest]
    first_active_at: str | None
    last_active_at: str | None
    turn_times: list[str]  # the harness instant of each customer message, so a step-up can only use digits typed recently
    reflected_turns: int
    episodes_written: int


@dataclass
class TurnContext:
    """Per-invocation context, never checkpointed: LangGraph's analog of ADK's temp: scope."""

    user_id: str
    now: str
    session_id: str = ""


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

    @property
    def privacy_db(self) -> Path:
        return self.var_dir / "privacy.db"


def open_harness(var_dir: Path) -> Harness:
    """Create (or reopen) every local store under var_dir and seed the bank and the app-wide settings."""
    var_dir.mkdir(parents=True, exist_ok=True)
    world.seed_bank(var_dir / "bank.db")
    scheduler.create_scheduler(var_dir / "scheduler.db")
    privacy.create_ledger(var_dir / "privacy.db")
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


def _channel(store: SqliteStore, user_id: str) -> tuple[str, bool]:
    fact = _facts(store, user_id).get("contact_channel")
    return (fact or {}).get("value", DEFAULT_CHANNEL), bool(fact)


def _thread_state(h: Harness, user_id: str, session_id: str) -> dict:
    checkpoint = h.checkpointer.get_tuple(thread_config(user_id, session_id))
    return checkpoint.checkpoint["channel_values"] if checkpoint else {}


def _threads(h: Harness) -> list[str]:
    with closing(sqlite3.connect(h.var_dir / "lg_checkpoints.db")) as conn:
        tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
        return [row[0] for row in conn.execute("SELECT DISTINCT thread_id FROM checkpoints")] if "checkpoints" in tables else []


def compact_sqlite(path: Path) -> None:
    """Deleted rows linger in free pages and in the WAL until the file is rewritten; erasure has to reach those too.

    VACUUM first (in WAL mode it writes the rebuilt pages to the WAL), then checkpoint them into the main file
    and truncate the WAL, so neither file still holds the deleted bytes.
    """
    with closing(sqlite3.connect(path, timeout=60)) as conn:
        conn.execute("VACUUM")
        conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")


def delete_store_item(h: Harness, namespace: tuple[str, ...], key: str) -> None:
    """SqliteStore.delete leaves the item's embedding in store_vectors (round 4 found it); an erased or expired
    episode's vector is derived from the customer's words, so it goes too."""
    h.store.delete(namespace, key)
    with closing(sqlite3.connect(h.var_dir / "lg_store.db", timeout=60)) as conn, conn:
        conn.execute("DELETE FROM store_vectors WHERE prefix = ? AND key = ?", (".".join(namespace), key))


def _customer_texts(messages: list) -> list[str]:
    return [m.content for m in messages if isinstance(m, HumanMessage) and isinstance(m.content, str)]


# --------------------------------------------------------------------------- tools


# Tools only a LIVE conversation gets, one where the customer is in the chat and typing. They act for the customer
# (verify their identity, file a dispute, change or delete what is remembered, set or cancel a reminder, erase
# everything), so they need the customer there to ask for it. An unattended session never gets them: it reads text
# other people wrote (back-office case notes, the customer's own reminder note), and an instruction hidden in that
# text ("call request_memory_erasure") must find nothing to call.
LIVE_ONLY_TOOLS = ("verify_identity", "file_dispute", "add_case_evidence", "remember_customer_fact", "forget_customer_fact",
                   "schedule_reminder", "cancel_reminder", "request_memory_erasure")
# Tools only an UNATTENDED session gets: one the scheduler starts when a follow-up or reminder falls due, with no
# customer present. notify_customer is how that session reaches the customer (one message per follow-up). A live
# conversation never gets it, because there the agent simply replies in the chat. A session is unattended only when
# the scheduler starts it for a follow-up record and says so in the SessionKind it passes in (cardcare/sessions.py,
# built by run_followup_session from the record); nothing stored in the session can change that.
UNATTENDED_ONLY_TOOLS = ("notify_customer",)


def build_tools(h: Harness, kind: SessionKind = LIVE) -> list:
    """Tools over this harness's stores. The customer is always runtime.context.user_id, never a model argument.

    Least privilege by session kind, which comes from the job that started the session (`kind`), never from the
    thread: a scheduler-fired session reads text others wrote (case notes, reminder notes), so it gets only reads
    and notify_customer; a live session never gets notify_customer.
    """

    def _session(runtime) -> str:
        return runtime.context.session_id

    def _generation(runtime) -> int:
        record = privacy.session_record(h.privacy_db, runtime.context.user_id, _session(runtime))
        return record["generation"] if record else -1

    @tool
    def verify_identity(card_last4: CardLast4, postal_code: PostalCode, runtime: ToolRuntime[TurnContext]) -> Command:
        """Verify the logged-in customer with their card's last 4 digits and billing ZIP, exactly as the customer typed
        them in this conversation (if they already did, use those). Valid for 15 minutes. Three failures lock
        verification on the account for 24 hours."""
        user_id, now = runtime.context.user_id, runtime.context.now
        update = {}
        if not typed_in_session(_customer_texts(runtime.state["messages"]), card_last4, postal_code,
                                turn_times=runtime.state.get("turn_times"), now=now):
            result = {"verified": False, "error": "verify_identity accepts only the last 4 digits and ZIP the customer typed in this "
                                                  "conversation in the last 15 minutes; ask the customer for them (nothing was "
                                                  "counted against the account)"}
        else:
            attempt = world.attempt_verification(h.bank_db, user_id, card_last4, postal_code, now, MAX_VERIFICATION_ATTEMPTS)
            if attempt["outcome"] == "locked":
                result = {"verified": False, "error": f"verification is locked on this account for {VERIFICATION_LOCK_HOURS} hours "
                                                      f"after {MAX_VERIFICATION_ATTEMPTS} failed attempts; the customer must call Kestrel"}
            elif attempt["outcome"] == "mismatch":
                result = {"verified": False, "error": "those details do not match this customer",
                          "attempts_left": max(0, MAX_VERIFICATION_ATTEMPTS - attempt["failures"])}
            else:
                result, update = {"verified": True, "valid_for_minutes": 15}, {"identity_verified_at": now}
        return Command(update={**update, "messages": [ToolMessage(json.dumps(result), tool_call_id=runtime.tool_call_id)]})

    @tool
    def find_transactions(runtime: ToolRuntime[TurnContext], merchant: Merchant = None) -> str:
        """List the customer's posted transactions, optionally only those whose merchant name contains `merchant`."""
        return json.dumps({"transactions": world.find_transactions(h.bank_db, runtime.context.user_id, merchant, runtime.context.now)})

    @tool
    def file_dispute(transaction_id: TransactionId, reason: DisputeReason, runtime: ToolRuntime[TurnContext], evidence_note: EvidenceNote = None) -> str:
        """File a dispute for one transaction. Requires a verify_identity in the last 15 minutes. Schedules the case follow-up automatically, and
        the result says where it will reach the customer."""
        error = verification_gate_error(runtime.state.get("identity_verified_at"), runtime.context.now, "filing a dispute")
        if error:
            return json.dumps({"error": error})
        settings = runtime.store.get(("app",), "settings").value
        channel, chosen = _channel(runtime.store, runtime.context.user_id)
        return json.dumps(desk.file_dispute_with_followup(
            h.bank_db, h.scheduler_db, runtime.context.user_id, transaction_id, reason, evidence_note,
            runtime.context.now, settings["dispute_review_days"], settings["large_dispute_threshold_cents"], channel, chosen,
            _generation(runtime),
        ))

    @tool
    def add_case_evidence(case_id: CaseId, evidence_note: NewEvidence, runtime: ToolRuntime[TurnContext]) -> str:
        """Attach more evidence (e.g. a cancellation reference the customer found later) to one of their open cases."""
        return json.dumps(world.add_case_evidence(h.bank_db, runtime.context.user_id, case_id, mask_customer_text(evidence_note), runtime.context.now))

    @tool
    def get_case_status(runtime: ToolRuntime[TurnContext], case_id: OptionalCaseId = None) -> str:
        """Current status of one dispute case, or of all this customer's cases when case_id is omitted."""
        return json.dumps({"cases": world.list_cases(h.bank_db, runtime.context.user_id, case_id)})

    @tool
    def search_policy(question: PolicyQuestion) -> str:
        """Search Kestrel's policy documents (fees, dispute rules, travel notices, contact channels)."""
        return json.dumps({"documents": search_policy_documents(question)})

    @tool
    def remember_customer_fact(key: FactKey, value: FactValue, runtime: ToolRuntime[TurnContext], valid_until: ValidUntil = None) -> str:
        """Store a fact the customer stated: their contact channel, or a travel notice. Replaces any earlier value of
        that fact. Changing the contact channel needs a verify_identity in the last 15 minutes."""
        if key in FACT_KEYS_NEEDING_VERIFICATION:
            error = verification_gate_error(runtime.state.get("identity_verified_at"), runtime.context.now, f"changing {key}")
            if error:
                return json.dumps({"error": error})
        try:
            fact = build_fact(key, value, valid_until, runtime.context.now)
        except ValueError as exc:
            return json.dumps({"error": str(exc)})
        namespace = ("facts", runtime.context.user_id)
        with privacy.write_guard(h.privacy_db, runtime.context.user_id, _session(runtime)) as writable:
            if not writable:
                return json.dumps({"error": ERASED_IN_THIS_CONVERSATION})
            previous = runtime.store.get(namespace, key)
            runtime.store.put(namespace, key, fact, index=False)  # keyed overwrite: the new value replaces the old
        return json.dumps({"stored": {key: fact}, "replaced": previous.value["value"] if previous else None})

    @tool
    def forget_customer_fact(key: FactKey, runtime: ToolRuntime[TurnContext]) -> str:
        """Delete a stored customer fact (contact_channel or travel_notice) at the customer's request. Removing the
        contact channel needs a verify_identity in the last 15 minutes, like changing it."""
        if key not in FACT_KEYS:
            return json.dumps({"error": f"unknown fact {key}"})
        if key in FACT_KEYS_NEEDING_VERIFICATION:
            error = verification_gate_error(runtime.state.get("identity_verified_at"), runtime.context.now, f"removing {key}")
            if error:
                return json.dumps({"error": error})
        namespace = ("facts", runtime.context.user_id)
        had_value = runtime.store.get(namespace, key) is not None
        runtime.store.delete(namespace, key)
        return json.dumps({"forgotten": key, "had_value": had_value,
                           "note": f"deleted from memory now; conversation transcripts are deleted {TRANSCRIPT_RETENTION_DAYS} days "
                                   "after their first message, or at once if the customer asks to erase everything"})

    @tool
    def schedule_reminder(note: ReminderNote, remind_on: RemindOn, runtime: ToolRuntime[TurnContext], remind_at: RemindAt = "09:00",
                          timezone: TimeZone = "UTC") -> str:
        """Schedule a reminder to the customer, only when they ask for one, and at once. At most one reminder per day, at most 90 days ahead. The result says when, in the customer's
        time, and on which channel it will arrive."""
        channel, chosen = _channel(runtime.store, runtime.context.user_id)
        with privacy.write_guard(h.privacy_db, runtime.context.user_id, _session(runtime)) as writable:
            if not writable:
                return json.dumps({"error": ERASED_IN_THIS_CONVERSATION})
            return json.dumps(desk.schedule_customer_reminder(h.scheduler_db, runtime.context.user_id, note, remind_on, remind_at,
                                                              timezone, runtime.context.now, _generation(runtime), channel, chosen))

    @tool
    def list_my_followups(runtime: ToolRuntime[TurnContext]) -> str:
        """What is scheduled for this customer (reminders and case follow-ups), when, and on which channel it will arrive."""
        channel, chosen = _channel(runtime.store, runtime.context.user_id)
        records = [r for r in scheduler.user_followups(h.scheduler_db, runtime.context.user_id) if r["status"] in ("pending", "awaiting_approval")]
        return json.dumps({"scheduled": [scheduler.customer_view(r, channel, chosen) for r in records]})

    @tool
    def cancel_reminder(followup_id: FollowupId, runtime: ToolRuntime[TurnContext]) -> str:
        """Cancel one of the customer's own reminders before it is sent (ids come from list_my_followups)."""
        record = scheduler.get_followup(h.scheduler_db, followup_id)
        if not record or record["user_id"] != runtime.context.user_id or record["action"] != "customer_reminder":
            return json.dumps({"error": f"{followup_id} is not one of this customer's reminders"})
        cancelled = scheduler.cancel_followup(h.scheduler_db, followup_id, runtime.context.user_id, runtime.context.now)
        return json.dumps({"cancelled": followup_id} if cancelled else {"error": f"{followup_id} has already been sent or cancelled"})

    @tool
    def request_memory_erasure(runtime: ToolRuntime[TurnContext]) -> str:
        """The customer asks to delete everything remembered about them (being logged in is enough). Runs now: facts, conversation summaries, other conversations' transcripts and reminders are deleted at once; this
        conversation's transcript is deleted when it ends. Nothing more can be stored for them in this conversation."""
        now = runtime.context.now
        result = erase_customer_memory(h, runtime.context.user_id, now, requesting_session=_session(runtime))
        return json.dumps({"erased_now": f"{result['facts']} remembered facts, {result['episodes']} past-conversation summaries, "
                                         f"{result['transcripts']} other conversation transcripts, {len(result['reminders_cancelled'])} "
                                         "reminders with their notes",
                           "this_conversation": "its transcript is deleted when the conversation ends; nothing more can be stored for "
                                                "the customer in it (a new conversation afterwards starts fresh)",
                           "kept": "dispute cases, transactions and messages already sent are bank records with their own legal retention"})

    @tool
    def notify_customer(message: CustomerMessage, runtime: ToolRuntime[TurnContext]) -> str:
        """Send the customer one message on their contact channel. Only for scheduled follow-ups; one per follow-up."""
        record = kind.followup and scheduler.get_followup(h.scheduler_db, kind.followup["followup_id"])
        if not record:
            return json.dumps({"error": "notify_customer is only for scheduled follow-ups; in a live conversation, just reply"})
        if MASK_TOKEN.search(message):
            return json.dumps({"error": "the message contains masked text ([REDACTED ...]); write it without that part"})
        if record["action"] == "customer_reminder" and (record["status"] != "running" or not kind.persist):
            return json.dumps({"error": "this reminder was cancelled (the customer asked to be erased); send nothing"})
        channel, _ = _channel(runtime.store, runtime.context.user_id)
        sent = world.record_outbound_message(h.bank_db, runtime.context.user_id, channel, mask_card_numbers(message), record["followup_id"],
                                             record["approval"] != "none", runtime.context.now)
        if sent is None:  # the database's one-message-per-follow-up constraint: parallel calls cannot race past it
            return json.dumps({"error": "this follow-up has already produced its one message"})
        return json.dumps({"channel": channel, "message_id": sent["message_id"],
                           "status": "held for a Kestrel reviewer to approve before it is sent" if record["approval"] != "none" else "sent"})

    @tool
    def load_memory(query: MemoryQuery, runtime: ToolRuntime[TurnContext]) -> str:
        """Search reflections on this customer's past conversations. Use when they refer to an earlier conversation."""
        items = [item for item in runtime.store.search(("episodes", runtime.context.user_id), query=query, limit=6)
                 if not episode_is_expired(item.value, runtime.context.now)][:3]  # expired is gone, maintenance or not
        return json.dumps({"memories": [{"at": item.value["at"], "text": item.value["text"], "similarity": round(item.score or 0, 3)} for item in items]})

    @tool
    def report_malformed_tool_call(tool: MalformedTool = "") -> str:
        """Harness use only, never call it yourself: the result of a tool call whose arguments were not valid JSON."""
        return json.dumps({"error": f"your {tool or 'last'} call's arguments were not valid JSON, so it did not run; "
                                    "make the call again with valid JSON arguments"})

    tools = [verify_identity, find_transactions, file_dispute, add_case_evidence, get_case_status, search_policy,
             remember_customer_fact, forget_customer_fact, schedule_reminder, list_my_followups, cancel_reminder,
             request_memory_erasure, notify_customer, load_memory, report_malformed_tool_call]
    excluded = LIVE_ONLY_TOOLS if kind.unattended else UNATTENDED_ONLY_TOOLS
    return [t for t in tools if t.name not in excluded]


# --------------------------------------------------------------------------- graph


def _model() -> ChatDeepSeek:
    return ChatDeepSeek(model=DEEPSEEK_MODEL, api_key=deepseek_api_key())


def windowed_messages(messages: list, reflected_turns: int) -> list:
    """Re-send only the turns not yet reflected into long-term memory (cut at a customer turn, so tool pairs stay whole)."""
    starts = [i for i, message in enumerate(messages) if isinstance(message, HumanMessage)]
    return messages[starts[reflected_turns]:] if 0 < reflected_turns < len(starts) else messages


def build_graph(h: Harness, disabled_tools: tuple[str, ...] = (), kind: SessionKind = LIVE):
    tools = [t for t in build_tools(h, kind) if t.name not in disabled_tools]
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
        context = [SystemMessage(system), *windowed_messages(state["messages"], state.get("reflected_turns") or 0)]
        response = model.invoke(context)
        if not response.tool_calls and not response.invalid_tool_calls and not (isinstance(response.content, str) and response.content.strip()):
            response = model.invoke(context)  # one retry: an empty turn is a model stall, not an answer
        return {"messages": [route_malformed_calls(mask_model_output(response))]}

    graph = StateGraph(SessionState, context_schema=TurnContext)
    graph.add_node("forget_expired_facts", forget_expired_facts)
    graph.add_node("agent", call_model)
    graph.add_node("tools", ToolNode(tools))
    graph.add_edge(START, "forget_expired_facts")
    graph.add_edge("forget_expired_facts", "agent")
    graph.add_conditional_edges("agent", tools_condition)
    graph.add_edge("tools", "agent")
    # a follow-up whose record predates an erasure keeps its thread in memory only: nothing about it is stored
    return graph.compile(checkpointer=h.checkpointer if kind.persist else InMemorySaver(), store=h.store)


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


def mask_model_output(message: AIMessage) -> AIMessage:
    """Before anything is written to the thread: card numbers are masked in the model's reply, and its reasoning
    (which ChatDeepSeek keeps in additional_kwargs and the checkpointer persists) gets the full customer-input
    rules, security codes and expiries included, since nobody reads it and over-masking it costs nothing."""
    if isinstance(message.content, str):
        message.content = mask_card_numbers(message.content)
    if isinstance(message.additional_kwargs.get("reasoning_content"), str):
        message.additional_kwargs["reasoning_content"] = mask_customer_text(message.additional_kwargs["reasoning_content"])
    return message


def route_malformed_calls(message: AIMessage) -> AIMessage:
    """A call whose arguments are not valid JSON never reaches ToolNode, the graph ends with no reply, and the call
    stays in every later request with no tool result, so every later turn is an HTTP 400. Under its own id it becomes
    a call to report_malformed_tool_call: ToolNode answers it with the error next to any valid calls, and the model's
    next step can make the call again (the ADK agent does the same in its after_model_callback)."""
    if message.invalid_tool_calls:
        message.tool_calls = [*message.tool_calls, *({"name": "report_malformed_tool_call", "args": {"tool": c["name"] or ""},
                                                      "id": c["id"], "type": "tool_call"} for c in message.invalid_tool_calls)]
        message.invalid_tool_calls = []
    return message


def repair_interrupted_tool_calls(h: Harness, user_id: str, session_id: str) -> int:
    """Tool calls with no ToolMessage (a crash mid-step, or a malformed call left by an older version) make every later
    model call a 400; answer them with errors."""
    messages = _thread_state(h, user_id, session_id).get("messages", [])
    answered = {m.tool_call_id for m in messages if isinstance(m, ToolMessage)}
    dangling = [c for m in messages if isinstance(m, AIMessage) for c in [*m.tool_calls, *m.invalid_tool_calls] if c["id"] not in answered]
    if dangling:
        build_graph(h).update_state(thread_config(user_id, session_id), {"messages": [
            ToolMessage(json.dumps({"error": "this call was interrupted and did not run"}), tool_call_id=c["id"], name=c["name"] or "unknown")
            for c in dangling]}, as_node="tools")
    return len(dangling)


def _map_strings(value, fix):
    """Apply `fix` to every string inside a checkpointed value: dicts, lists, tuples and pydantic models (messages)."""
    if isinstance(value, str):
        return fix(value)
    if isinstance(value, list):
        return [_map_strings(v, fix) for v in value]
    if isinstance(value, tuple):
        return tuple(_map_strings(v, fix) for v in value)
    if isinstance(value, dict):
        return {k: _map_strings(v, fix) for k, v in value.items()}
    if isinstance(value, BaseModel):
        return value.model_copy(update={name: _map_strings(getattr(value, name), fix) for name in type(value).model_fields})
    return value


CONTEXT_HOURS = 24  # earlier messages in the customer's other chats this recent are context for the masker too


def recent_customer_messages(h: Harness, user_id: str, session_id: str, own: list[str], now: str) -> list[tuple[str, str]]:
    """(session id, stored text) of the customer's earlier messages, oldest first: this session's, after the last few of
    their other chats active in the past CONTEXT_HOURS (so a number split across two chats is caught too)."""
    others = []
    for thread_id in _threads(h):
        owner, sid = thread_id.split(":", 1)
        if owner != user_id or sid == session_id:
            continue
        state = _thread_state(h, user_id, sid)
        last = state.get("last_active_at")
        if not last or (parse_instant(now) - parse_instant(last)).total_seconds() > CONTEXT_HOURS * 3600:
            continue
        others += [(last, sid, text) for text in _customer_texts(state.get("messages", []))[-3:]]
    return [(sid, text) for _, sid, text in sorted(others, key=lambda item: item[0])] + [(session_id, text) for text in own]


def scrub_earlier_messages(h: Harness, user_id: str, session_id: str, replacements: dict[str, str]) -> int:
    """A card number this message completes started in an earlier message: rewrite that message in every checkpoint
    and pending write of the thread (LangGraph keeps one copy per step), and in this customer's episodes, then compact."""
    fragments = [f for old, new in replacements.items() for f in removed_fragments(old, new)]

    def fix(text: str) -> str:
        for old, new in replacements.items():
            text = text.replace(old, new)
        return scrub_fragments(text, fragments)

    serde, thread_id, changed = h.checkpointer.serde, thread_config(user_id, session_id)["configurable"]["thread_id"], 0
    with h.checkpointer.lock, closing(sqlite3.connect(h.var_dir / "lg_checkpoints.db", timeout=60)) as conn, conn:
        for ns, cid, kind, blob, metadata in conn.execute(
                "SELECT checkpoint_ns, checkpoint_id, type, checkpoint, metadata FROM checkpoints WHERE thread_id = ?", (thread_id,)).fetchall():
            new_kind, new_blob = serde.dumps_typed(_map_strings(serde.loads_typed((kind, blob)), fix))
            new_metadata = json.dumps(_map_strings(json.loads(metadata), fix), ensure_ascii=False).encode() if metadata else metadata
            if new_blob != blob or new_metadata != metadata:
                conn.execute("UPDATE checkpoints SET type = ?, checkpoint = ?, metadata = ? WHERE thread_id = ? AND checkpoint_ns = ? "
                             "AND checkpoint_id = ?", (new_kind, new_blob, new_metadata, thread_id, ns, cid))
                changed += 1
        for ns, cid, task, idx, kind, blob in conn.execute(
                "SELECT checkpoint_ns, checkpoint_id, task_id, idx, type, value FROM writes WHERE thread_id = ?", (thread_id,)).fetchall():
            new_kind, new_blob = serde.dumps_typed(_map_strings(serde.loads_typed((kind, blob)), fix))
            if new_blob != blob:
                conn.execute("UPDATE writes SET type = ?, value = ? WHERE thread_id = ? AND checkpoint_ns = ? AND checkpoint_id = ? "
                             "AND task_id = ? AND idx = ?", (new_kind, new_blob, thread_id, ns, cid, task, idx))
                changed += 1
    for item in h.store.search(("episodes", user_id), limit=1000):
        new_value = _map_strings(item.value, fix)
        if new_value != item.value:
            h.store.put(("episodes", user_id), item.key, new_value)
            changed += 1
    compact_sqlite(h.var_dir / "lg_checkpoints.db")
    compact_sqlite(h.var_dir / "lg_store.db")
    return changed


def _cap(text: str) -> str:
    if len(text) <= MAX_CUSTOMER_MESSAGE_CHARS:
        return text
    return text[:MAX_CUSTOMER_MESSAGE_CHARS] + f" [message cut here: the other {len(text) - MAX_CUSTOMER_MESSAGE_CHARS} characters were not kept]"


def run_turn(h: Harness, user_id: str, session_id: str, text: str, now: str, disabled_tools: tuple[str, ...] = (),
             kind: SessionKind = LIVE, graph=None) -> dict:
    """One customer message through the graph. Returns what was sent, every tool call with its result, and the reply.

    A failure inside the turn is returned as an error record, after the thread is repaired, so one bad turn never
    leaves the conversation unusable.
    """
    if kind.persist:
        finish_requested_erasures(h, now, user_id=user_id, keep=session_id)
        retire_expired_session(h, user_id, session_id, now)
        privacy.register_session(h.privacy_db, user_id, session_id, kind.label, now)
        repair_interrupted_tool_calls(h, user_id, session_id)
    graph = graph or build_graph(h, disabled_tools, kind)
    config = thread_config(user_id, session_id)
    snapshot_ = graph.get_state(config)
    state = snapshot_.values if snapshot_ else {}
    turns = group_by_customer_turn(_transcript_turns(state.get("messages", [])))
    if kind.persist and len(turns) + 1 - (state.get("reflected_turns") or 0) > WORKING_WINDOW_TURNS:
        reflect_turns(h, user_id, session_id, now, upto=len(turns) + 1 - WORKING_KEEP_TURNS, kind=kind)
    own = [group[0]["text"] for group in turns if group and group[0]["role"] == "customer"]
    earlier = recent_customer_messages(h, user_id, session_id, own, now) if kind.persist and not kind.unattended else \
        [(session_id, text) for text in own]
    sent, rewrites = mask_customer_message(text, tuple(text for _, text in earlier))  # card data never enters a store
    sent = _cap(sent)
    if rewrites and kind.persist:
        by_session: dict[str, dict[str, str]] = {}
        for index, rewritten in rewrites.items():
            by_session.setdefault(earlier[index][0], {})[earlier[index][1]] = rewritten
        for sid, replacements in by_session.items():
            scrub_earlier_messages(h, user_id, sid, replacements)
    offered = sorted(t.name for t in build_tools(h, kind) if t.name not in disabled_tools)
    already = len(state.get("messages", []))
    update = {"messages": [HumanMessage(sent)], "last_active_at": now,
              "turn_times": [*(state.get("turn_times") or []), now][-WORKING_WINDOW_TURNS * 3:]}
    if not state.get("first_active_at"):
        update["first_active_at"] = now
    context = TurnContext(user_id=user_id, now=now, session_id=session_id)
    try:
        result = graph.invoke(update, config, context=context)
    except Exception as exc:
        if kind.persist:
            repair_interrupted_tool_calls(h, user_id, session_id)
        partial = (graph.get_state(config).values or {}).get("messages", [])[already:]
        return {**_turn_record(partial, sent), "error": f"{type(exc).__name__}: {exc}", "tools_offered": offered}
    return {**_turn_record(result["messages"][already:], sent), "tools_offered": offered}


def complete_text(prompt: str) -> str:
    return _model().invoke(prompt).content


def reflect_turns(h: Harness, user_id: str, session_id: str, now: str, upto: int | None = None, kind: SessionKind = LIVE) -> dict | None:
    """Reflect the customer turns after the thread's reflected mark, up to `upto` (default: all), into one episode.
    The episode is written behind the erasure fence: a session an erasure has overtaken writes none."""
    if not privacy.session_is_current(h.privacy_db, user_id, session_id):
        return None
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
                            procedures.active_procedure(h.var_dir)[0], customer_present=not kind.unattended)
    with privacy.write_guard(h.privacy_db, user_id, session_id) as writable:
        if not writable:
            return None
        h.store.put(("episodes", user_id), episode["episode_id"], episode)  # indexed on "text" for semantic recall
    build_graph(h).update_state(thread_config(user_id, session_id), {"reflected_turns": upto, "episodes_written": sequence})
    return episode


def delete_transcript(h: Harness, user_id: str, session_id: str, forget: bool = True) -> bool:
    """Delete a thread. `forget=False` keeps its registration (stale), so a chat that goes on after its transcript was
    erased still stores nothing."""
    thread_id = thread_config(user_id, session_id)["configurable"]["thread_id"]
    existed = thread_id in _threads(h)
    if existed:
        h.checkpointer.delete_thread(thread_id)
    if forget:
        privacy.forget_session(h.privacy_db, user_id, session_id)
    return existed


def end_session(h: Harness, user_id: str, session_id: str, now: str, kind: SessionKind = LIVE) -> dict | None:
    """Session concluded: a session an erasure overtook (the one the customer asked in, or any that started before it)
    is deleted, which completes the erasure; any other is reflected."""
    if not kind.persist:
        return None
    if not privacy.session_is_current(h.privacy_db, user_id, session_id):
        if delete_transcript(h, user_id, session_id):
            compact_sqlite(h.var_dir / "lg_checkpoints.db")
        finish_requested_erasures(h, now, user_id=user_id, only_session=session_id)
        return None
    return reflect_turns(h, user_id, session_id, now, kind=kind)


def list_episodes(store: SqliteStore) -> list[dict]:
    episodes = []
    for namespace in store.list_namespaces(prefix=("episodes",)):
        episodes += [item.value for item in store.search(namespace, limit=1000)]
    return sorted(episodes, key=lambda e: e["at"])


def finish_requested_erasures(h: Harness, now: str, user_id: str | None = None, keep: str | None = None,
                              only_session: str | None = None, idle_only: bool = False) -> list[str]:
    """Delete the transcript an erasure request was made in: at that chat's end, at the customer's next turn in another
    chat, or at the next maintenance run, whichever comes first (a closed tab never ends). If the chat goes on after
    that, it stays stale: still nothing is stored, and what it adds is deleted when it ends."""
    finished = []
    for request in privacy.pending_requests(h.privacy_db, user_id):
        session_id = request["requested_in"]
        if session_id == keep or (only_session and session_id != only_session):
            continue
        state = _thread_state(h, request["user_id"], session_id) if session_id else {}
        if idle_only and state and not session_is_idle(state.get("last_active_at"), now):
            continue
        if session_id:
            delete_transcript(h, request["user_id"], session_id, forget=bool(only_session))
        privacy.finish_request(h.privacy_db, request["rowid"], now)
        finished.append(request["user_id"])
    if finished:
        compact_sqlite(h.var_dir / "lg_checkpoints.db")
    return finished


def erase_customer_memory(h: Harness, user_id: str, now: str, requesting_session: str | None = None) -> dict:
    """Right to erasure, at once: raise the customer's memory generation (the fence), then delete every fact, episode
    (and its vector), reminder (its note too, whatever its state) and every transcript but the requesting one, which is
    still running and is deleted when it ends. Bank records (cases, ledger, messages already sent) are not memory."""
    privacy.begin_erasure(h.privacy_db, user_id, requesting_session, now)
    reminders = scheduler.erase_customer_reminders(h.scheduler_db, user_id, now)
    world.reject_held_messages(h.bank_db, reminders, "erasure")
    facts = _facts(h.store, user_id)
    for key in FACT_KEYS:
        delete_store_item(h, ("facts", user_id), key)
    episodes = [e for e in list_episodes(h.store) if e["user_id"] == user_id]
    for episode in episodes:
        delete_store_item(h, ("episodes", user_id), episode["episode_id"])
    keep = thread_config(user_id, requesting_session)["configurable"]["thread_id"] if requesting_session else None
    threads = [t for t in _threads(h) if t.startswith(f"{user_id}:") and t != keep]
    for thread_id in threads:
        h.checkpointer.delete_thread(thread_id)
    compact_sqlite(h.var_dir / "lg_checkpoints.db")
    compact_sqlite(h.var_dir / "lg_store.db")
    compact_sqlite(h.scheduler_db)
    if requesting_session is None:
        for request in privacy.pending_requests(h.privacy_db, user_id):
            if request["requested_in"] is None:
                privacy.finish_request(h.privacy_db, request["rowid"], now)
    return {"user_id": user_id, "facts": len(facts), "episodes": len(episodes), "transcripts": len(threads), "reminders_cancelled": reminders}


def retire_expired_session(h: Harness, user_id: str, session_id: str, now: str) -> bool:
    """A session lives 30 days from its first turn, whether or not maintenance has run: a turn on an older one first
    reflects what is not yet reflected, then deletes it, so the conversation continues as a new one."""
    state = _thread_state(h, user_id, session_id)
    if not state or not transcript_is_expired(state.get("first_active_at") or state.get("last_active_at"), now):
        return False
    record = privacy.session_record(h.privacy_db, user_id, session_id)
    reflect_turns(h, user_id, session_id, state.get("last_active_at") or now,
                  kind=SessionKind(unattended=bool(record and record["kind"] == "unattended")))
    delete_transcript(h, user_id, session_id)
    compact_sqlite(h.var_dir / "lg_checkpoints.db")
    return True


def run_maintenance(h: Harness, now: str) -> dict:
    """The harness's memory job: finish erasures whose conversation is over, delete expired facts of every customer,
    close idle chats (deleting the ones an erasure overtook), purge expired episodes and delete transcripts 30 days
    after their first turn."""
    erased = finish_requested_erasures(h, now)
    expired_facts = []
    for user_id in [customer[0] for customer in world.CUSTOMERS]:
        for key, fact in _facts(h.store, user_id).items():
            if fact_is_expired(fact, now):
                delete_store_item(h, ("facts", user_id), key)
                expired_facts.append(f"{user_id}:{key}")
    closed, deleted = [], []
    for thread_id in _threads(h):
        user_id, session_id = thread_id.split(":", 1)
        state = _thread_state(h, user_id, session_id)
        last_active = state.get("last_active_at")
        record = privacy.session_record(h.privacy_db, user_id, session_id)
        kind = SessionKind(unattended=bool(record and record["kind"] == "unattended"))
        if not privacy.session_is_current(h.privacy_db, user_id, session_id) and (session_is_idle(last_active, now) or not last_active):
            delete_transcript(h, user_id, session_id)
            deleted.append(session_id)
            continue
        if session_is_idle(last_active, now) and reflect_turns(h, user_id, session_id, last_active, kind=kind):
            closed.append(session_id)
        if transcript_is_expired(state.get("first_active_at") or last_active, now):
            delete_transcript(h, user_id, session_id)
            deleted.append(session_id)
    expired = [e for e in list_episodes(h.store) if episode_is_expired(e, now)]
    for episode in expired:
        delete_store_item(h, ("episodes", episode["user_id"]), episode["episode_id"])
    if deleted or expired or expired_facts:
        compact_sqlite(h.var_dir / "lg_checkpoints.db")
        compact_sqlite(h.var_dir / "lg_store.db")
    return {"erased_customers": erased, "expired_facts": expired_facts, "closed_idle_sessions": closed,
            "purged_episodes": [e["episode_id"] for e in expired], "deleted_transcripts": deleted}


def run_followup_session(h: Harness, record: dict, now: str) -> dict:
    """The scheduler's resume callback. The session's kind is built from the record and passed in; nothing the thread
    stores can change it. A record written before the customer's latest erasure runs in memory and leaves nothing."""
    # whoever fires a follow-up, a pending erasure of that customer is finished first (its requesting chat's transcript
    # deleted), so nothing scheduled can run while part of an erasure is still waiting
    finish_requested_erasures(h, now, user_id=record["user_id"])
    persist = record.get("generation", 0) == privacy.current_generation(h.privacy_db, record["user_id"])
    kind = followup_kind(record, persist)
    session_id = f"followup-{record['followup_id']}-{record['attempts'] + 1}"
    graph = build_graph(h, kind=kind)
    graph.update_state(thread_config(record["user_id"], session_id), {"last_active_at": now, "first_active_at": now})
    turn = run_turn(h, record["user_id"], session_id, scheduler.followup_trigger_message(record), now, kind=kind, graph=graph)
    episode = end_session(h, record["user_id"], session_id, now, kind=kind)
    return {"session_id": session_id, "persisted": persist, "turn": turn, "episode": episode}


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
            print(f"\n[assistant]: {turn['reply'] or '(no reply: ' + turn.get('error', 'empty turn') + '; you can keep chatting)'}")
    episode = end_session(h, user_id, session_id, now or wall_clock_now())
    if episode:
        print(f"\n[memory] episode {episode['episode_id']}: {episode['text']}")


async def fire_followups(h: Harness, now: str, on_session=None) -> list[dict]:
    """The scheduler's job: finish every pending erasure first (the requesting chat's transcript goes, whether or not a
    record of that customer is due), then fire what is due. `on_session` sees each follow-up session's record."""
    finish_requested_erasures(h, now)

    def resume(record: dict, at: str) -> dict:
        session = run_followup_session(h, record, at)
        if on_session:
            on_session(session)
        return session

    return await scheduler.fire_due_followups(h.scheduler_db, h.bank_db, now, resume)


async def tick(var_dir: Path, now: str | None) -> dict:
    """One pass of the harness's background work: memory maintenance, then the scheduler (which finishes any pending
    erasure before it fires anything)."""
    h = open_harness(var_dir)
    at = now or wall_clock_now()
    maintenance = run_maintenance(h, at)
    return {"now": at, "maintenance": maintenance, "followups": await fire_followups(h, at)}


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
