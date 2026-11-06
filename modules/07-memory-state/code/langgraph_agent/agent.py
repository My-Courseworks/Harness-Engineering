"""Kestrel card-care assistant on LangGraph: the same scenario, the same procedure, LangGraph's own memory primitives.

  working / in-context  the thread's messages, checkpointed per thread by SqliteSaver and re-sent every
                        turn, plus graph-state fields (identity_verified_at, followup_id): this
                        conversation only. Threads carry no user, so the harness names them "<user>:<session>".
                        The temp: analog is the per-invocation context (TurnContext.now): never checkpointed.
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
import json
import sqlite3
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
from cardcare.retrieval import EMBEDDING_DIMS, embed_texts, search_policy as search_policy_documents

APP_SETTINGS = {"dispute_review_days": 10, "large_dispute_threshold_cents": 20000}
CODE_DIR = Path(__file__).resolve().parent.parent


class SessionState(MessagesState):
    """Checkpointed per thread: lives exactly as long as the conversation (ADK's un-prefixed state)."""

    identity_verified_at: str | None
    followup_id: str | None


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


# --------------------------------------------------------------------------- tools


def build_tools(h: Harness) -> list:
    """Tools over this harness's stores. The customer is always runtime.context.user_id, never a model argument."""

    @tool
    def verify_identity(card_last4: str, postal_code: str, runtime: ToolRuntime[TurnContext]) -> Command:
        """Verify the logged-in customer with their card's last 4 digits and billing ZIP. Lasts for this conversation only."""
        if not world.identity_matches(h.bank_db, runtime.context.user_id, card_last4, postal_code):
            result, update = {"verified": False, "error": "those details do not match this customer"}, {}
        else:
            result, update = {"verified": True}, {"identity_verified_at": runtime.context.now}
        return Command(update={**update, "messages": [ToolMessage(json.dumps(result), tool_call_id=runtime.tool_call_id)]})

    @tool
    def find_transactions(runtime: ToolRuntime[TurnContext], merchant: str | None = None) -> str:
        """List the customer's posted transactions, optionally only those whose merchant name contains `merchant`."""
        return json.dumps({"transactions": world.find_transactions(h.bank_db, runtime.context.user_id, merchant, runtime.context.now)})

    @tool
    def file_dispute(transaction_id: str, reason: str, runtime: ToolRuntime[TurnContext], evidence_note: str | None = None) -> str:
        """File a dispute for one transaction. reason: cancelled_subscription, not_recognized, duplicate,
        goods_not_received or incorrect_amount. evidence_note: anything the customer supplied (e.g. a cancellation
        reference). Requires verify_identity in this conversation. Schedules the case follow-up automatically."""
        if not runtime.state.get("identity_verified_at"):
            return json.dumps({"error": "identity not verified in this conversation; call verify_identity first"})
        settings = runtime.store.get(("app",), "settings").value
        result = desk.file_dispute_with_followup(
            h.bank_db, h.scheduler_db, runtime.context.user_id, transaction_id, reason, evidence_note,
            runtime.context.now, settings["dispute_review_days"], settings["large_dispute_threshold_cents"],
        )
        if "followup" in result:
            result["followup"]["channel"] = _contact_channel(runtime.store, runtime.context.user_id)
        return json.dumps(result)

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
        if key in FACT_KEYS_NEEDING_VERIFICATION and not runtime.state.get("identity_verified_at"):
            return json.dumps({"error": f"changing {key} requires verify_identity in this conversation"})
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
        return json.dumps({"forgotten": key, "had_value": had_value})

    @tool
    def schedule_reminder(note: str, remind_on: str, runtime: ToolRuntime[TurnContext]) -> str:
        """Schedule a reminder message to the customer on a future date (YYYY-MM-DD), sent on their contact channel."""
        return json.dumps(desk.schedule_customer_reminder(h.scheduler_db, runtime.context.user_id, note, remind_on, runtime.context.now))

    @tool
    def notify_customer(message: str, runtime: ToolRuntime[TurnContext]) -> str:
        """Send the customer one message on their contact channel. Only for scheduled follow-ups."""
        followup_id = runtime.state.get("followup_id")
        if not followup_id:
            return json.dumps({"error": "notify_customer is only for scheduled follow-ups; in a live conversation, just reply"})
        channel = _contact_channel(runtime.store, runtime.context.user_id)
        sent = world.record_outbound_message(
            h.bank_db, runtime.context.user_id, channel, redact_card_secrets(message), followup_id, runtime.context.now
        )
        return json.dumps({"sent": True, "channel": channel, "message_id": sent["message_id"]})

    @tool
    def load_memory(query: str, runtime: ToolRuntime[TurnContext]) -> str:
        """Search reflections on this customer's past conversations. Use when they refer to an earlier conversation."""
        items = runtime.store.search(("episodes", runtime.context.user_id), query=query, limit=3)
        return json.dumps({"memories": [{"at": item.value["at"], "text": item.value["text"], "similarity": round(item.score or 0, 3)} for item in items]})

    return [verify_identity, find_transactions, file_dispute, get_case_status, search_policy,
            remember_customer_fact, forget_customer_fact, schedule_reminder, notify_customer, load_memory]


# --------------------------------------------------------------------------- graph


def _model() -> ChatDeepSeek:
    return ChatDeepSeek(model=DEEPSEEK_MODEL, api_key=deepseek_api_key())


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
        return {"messages": [model.invoke([SystemMessage(system), *state["messages"]])]}

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


def run_turn(h: Harness, user_id: str, session_id: str, text: str, now: str, disabled_tools: tuple[str, ...] = ()) -> dict:
    """One customer message through the graph. Returns what was sent, every tool call with its result, and the reply."""
    graph = build_graph(h, disabled_tools)
    config = thread_config(user_id, session_id)
    already = len(graph.get_state(config).values.get("messages", []))
    sent = redact_card_secrets(text)  # card numbers never enter the thread, let alone memory
    result = graph.invoke({"messages": [HumanMessage(sent)]}, config, context=TurnContext(user_id=user_id, now=now))
    return _turn_record(result["messages"][already:], sent)


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


def complete_text(prompt: str) -> str:
    return _model().invoke(prompt).content


def end_session(h: Harness, user_id: str, session_id: str, now: str) -> dict:
    """Session concluded: reflect on it and write one episode to the store."""
    messages = h.checkpointer.get_tuple(thread_config(user_id, session_id)).checkpoint["channel_values"]["messages"]
    turns = _transcript_turns(messages)
    reflection = parse_reflection(complete_text(reflection_prompt(turns)))
    episode = build_episode(user_id, session_id, now, reflection, case_outcomes(h.bank_db, user_id, turns),
                            procedures.active_procedure(h.var_dir)[0])
    h.store.put(("episodes", user_id), episode["episode_id"], episode)  # indexed on "text" for semantic recall
    return episode


def list_episodes(store: SqliteStore) -> list[dict]:
    episodes = []
    for namespace in store.list_namespaces(prefix=("episodes",)):
        episodes += [item.value for item in store.search(namespace, limit=1000)]
    return sorted(episodes, key=lambda e: e["at"])


def purge_expired_episodes(h: Harness, now: str) -> list[str]:
    """The retention job: forgetting on purpose."""
    expired = [e for e in list_episodes(h.store) if episode_is_expired(e, now)]
    for episode in expired:
        h.store.delete(("episodes", episode["user_id"]), episode["episode_id"])
    return [episode["episode_id"] for episode in expired]


def run_followup_session(h: Harness, record: dict, now: str) -> dict:
    """The scheduler's resume callback: a fresh thread for the customer, seeded with which follow-up it serves."""
    session_id = f"followup-{record['followup_id']}-{record['attempts'] + 1}"
    build_graph(h).update_state(thread_config(record["user_id"], session_id), {"followup_id": record["followup_id"]})
    turn = run_turn(h, record["user_id"], session_id, scheduler.followup_trigger_message(record), now)
    episode = end_session(h, record["user_id"], session_id, now)
    return {"session_id": session_id, "turn": turn, "episode": episode}


def snapshot(h: Harness, user_ids: list[str]) -> dict:
    """Read-only view of every store, for evidence."""
    with closing(sqlite3.connect(h.var_dir / "lg_checkpoints.db")) as conn:
        threads = [row[0] for row in conn.execute("SELECT DISTINCT thread_id FROM checkpoints")]
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
    }


# --------------------------------------------------------------------------- interactive CLI


def chat(var_dir: Path, user_id: str, session_id: str | None, now: str | None) -> None:
    h = open_harness(var_dir)
    session_id = session_id or f"chat-{uuid.uuid4().hex[:8]}"
    print(f"Kestrel card-care (LangGraph) | customer={user_id} session={session_id} | 'exit' ends the session and writes its episode")
    took_turn = False
    while True:
        text = input("\n[you]: ").strip()
        if text in ("exit", "quit"):
            break
        if text:
            turn = run_turn(h, user_id, session_id, text, now or wall_clock_now())
            took_turn = True
            for call in turn["tool_calls"]:
                print(f"  [tool] {call['name']}({json.dumps(call['args'])})")
            print(f"\n[assistant]: {turn['reply']}")
    if took_turn:
        episode = end_session(h, user_id, session_id, now or wall_clock_now())
        print(f"\n[memory] episode {episode['episode_id']}: {episode['text']}")


async def fire_followups(var_dir: Path, now: str | None) -> list[dict]:
    h = open_harness(var_dir)
    return await scheduler.fire_due_followups(
        h.scheduler_db, h.bank_db, now or wall_clock_now(), lambda record, at: run_followup_session(h, record, at)
    )


def main() -> None:
    import asyncio

    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("command", choices=["chat", "followups"])
    parser.add_argument("--user", default="priya", choices=[c[0] for c in world.CUSTOMERS])
    parser.add_argument("--session", help="continue an existing session id")
    parser.add_argument("--now", help="override the clock (ISO-8601), e.g. 2026-11-19T10:00:00Z")
    parser.add_argument("--var-dir", type=Path, default=CODE_DIR / "var" / "langgraph" / "interactive")
    args = parser.parse_args()
    if args.command == "chat":
        chat(args.var_dir, args.user, args.session, args.now)
    else:
        outcomes = asyncio.run(fire_followups(args.var_dir, args.now))
        print(json.dumps(outcomes, indent=2) if outcomes else "nothing due")


if __name__ == "__main__":
    main()
