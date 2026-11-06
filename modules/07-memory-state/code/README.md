# M7 code: seven memory types, one card-care desk, two frameworks

A customer-support agent for **Kestrel Card**, a fictional card issuer, built twice: once on **Google ADK** and once on **LangGraph**. Both share the same scenario, the same versioned procedure, the same bank systems and the same scheduler. Each puts the module's seven memory types ([README](../README.md#the-memory-taxonomy-seven-types-two-axes-four-scopes)) where that framework's own primitives put them. Every claim below is backed by a live, scripted multi-session run against DeepSeek: see [Evidence](#evidence-what-was-run-and-what-failed).

```
modules/07-memory-state/code/
├── adk_agent/agent.py          ADK: Session/State scopes, a BaseMemoryService, load_memory, callbacks
├── langgraph_agent/agent.py    LangGraph: checkpointer threads, graph state, Store namespaces, ToolRuntime
├── cardcare/                   framework-free: everything both agents share
│   ├── world.py                the bank's systems of record (customers, ledger, cases, outbound messages)
│   ├── scheduler.py            prospective memory: the harness-owned follow-up scheduler
│   ├── memory_policy.py        the write path as code: fact schema, expiry, card-number redaction, retention
│   ├── episodes.py             reflection: a finished session becomes one episode
│   ├── procedures.py           procedural memory: versions, promotion with threshold + reviewer, retraction
│   ├── procedure_versions/v1.md  the baseline instruction both agents run
│   ├── retrieval.py            local embeddings and the policy knowledge base
│   ├── policy_kb/*.md          Kestrel's policy documents (external retrieval corpus)
│   ├── desk.py                 multi-step operations (file a dispute + schedule its follow-up)
│   └── scenario.py             the scripted scenario and its live checks
├── run_scenario.py             drives a framework through the scenario and writes evidence/
└── evidence/                   transcripts, per-check results, final store contents, failure analysis
```

## The scenario

Kestrel's card-care desk serves four logged-in cardholders over one simulated month, plus a jump to the end of the episode-retention window:

| when (simulated) | who | what happens | memory types exercised |
|---|---|---|---|
| Nov 9 | Priya | sets a travel notice (Lisbon, to Nov 30) and email as contact channel; disputes "the later" of two StreamMax charges; asks what a chargeback is; asks the FX fee | semantic, working, external, prospective, parametric, episodic |
| Nov 12 | Priya | new session: "what did we sort out last time?"; "is it resolved?"; "how will you contact me?"; switches to SMS (re-verifies) | episodic, external, semantic, working |
| Nov 12 | Marco | asks what is on file for him; asks about "a customer called Priya"; disputes a $240 gym renewal | semantic + episodic leakage, prospective approval |
| Nov 18 | back office | merchants answer: both cancelled-subscription disputes are rejected for `NO_CANCELLATION_PROOF` | (system of record) |
| Nov 19 | scheduler | Priya's follow-up fires; it texts her (the channel she chose *after* the record was written) | prospective, semantic |
| Nov 20 | Priya | "why was it rejected?"; asks for a reminder on Nov 29; asks for a recap across conversations | external, prospective, episodic |
| Nov 22 | scheduler + ops | Marco's follow-up is parked for `ops_reviewer`, approved, fires once, then never again | prospective |
| Nov 23 | reviewer | the same rejection in two customers' episodes is promoted into procedure v2 | procedural |
| Nov 24 | Dana, then Eli | Dana's identical dispute under v2 (agent asks for the cancellation reference first); a retraction drill restores v1; Eli's identical dispute under v1 as the control | procedural |
| Nov 29 | scheduler | Priya's reminder fires | prospective |
| Dec 3 | Priya | travel notice has expired; sets and then deletes a new one; pastes a full card number | semantic (staleness, deletion), guard |
| Dec 3 | Priya | FX-fee question with retrieval removed (ablation) | parametric |
| Jun 15 2027 | retention job, Priya | episodes past 180 days are deleted; "what did we talk about last time?" | episodic (forgetting) |

The domain was picked because every memory type has a non-contrived job in it, and because its failure modes are the module's ones with real consequences. A stale travel notice causes wrong fraud decisions. Leaking another cardholder's case is a privacy breach. A follow-up that never fires is a broken promise to a customer, and a stored card number is a PCI incident.

## Where each memory type lives

| type | the module's framing | ADK | LangGraph |
|---|---|---|---|
| **Working / in-context** | the session, re-sent every turn, plus a scoped scratchpad | `Session` events in `DatabaseSessionService` (SQLite). State by prefix: `identity_verified_at`, `followup_id` (session), `user:*` (customer), `app:*` (all customers), `temp:now` (this invocation; trimmed before persistence) | thread messages in `SqliteSaver`; graph-state fields `identity_verified_at`, `followup_id` (session); `TurnContext.now` passed as per-invocation `context`, never checkpointed (the `temp:` analog). Threads have no owner, so the harness names them `<user>:<session>` |
| **Semantic** | facts, verified, timestamped, scoped, overwritten not appended | `user:contact_channel`, `user:travel_notice` written through `tool_context.state`, preloaded into the instruction by an `InstructionProvider` | `SqliteStore` namespace `("facts", user)`, key = fact name, `put()` overwrites, preloaded into the system prompt by the `agent` node |
| **Episodic** | what happened, as a distilled reflection, searched on demand | `EpisodeMemoryService(BaseMemoryService)`: `add_memory` / `search_memory` / `delete_memory` on SQLite + local embeddings, recalled by ADK's built-in `load_memory` tool | `SqliteStore` namespace `("episodes", user)` with a sqlite-vec index on the reflection text, recalled by a `load_memory` tool |
| **Procedural** | the versioned instruction, not a store; promotion needs a threshold, a reviewer and a retraction path | the `InstructionProvider` reads the active version each turn | the `agent` node reads the active version each turn |
| **External / retrieval** | the store + a retriever; exact lookup for specific facts, vector search for related text | tools: `find_transactions`, `get_case_status` (exact SQL, scoped by `tool_context.user_id`), `search_policy` (embeddings) | the same tools, scoped by `runtime.context.user_id` |
| **Parametric** | the unmanaged floor | the DeepSeek weights, via `LiteLlm` | the DeepSeek weights, via `ChatDeepSeek` |
| **Prospective** | a scheduler the harness owns, never the memory store; five fields | `cardcare/scheduler.py`: written by `file_dispute` / `schedule_reminder`, fired by the harness into a fresh session (`run_followup_session`) | the same scheduler; fired into a fresh thread |

The procedure, the bank, the scheduler and the write-path rules are shared code. That is deliberate: procedural and prospective memory are framework-independent by the module's own definition. The differences between the two agents are therefore all about *where state lives*, which is the comparison worth making.

### What each framework made easy or awkward

- **Scope is a key prefix in ADK and a namespace convention in LangGraph.** ADK sessions are keyed by `(app, user, session)` and `user:` state is joined in automatically. LangGraph checkpointer threads have no owner, so per-user isolation of threads and of store namespaces is the harness's job (`thread_config`, `("facts", user)`).
- **`temp:` has no LangGraph equivalent in state.** Every state channel is checkpointed, so the per-invocation clock rides in `context` instead. Both runs check that no clock value is ever persisted.
- **App-wide state is event-sourced in ADK.** `app:` keys can only change through an event, so ops seeds them with `EventActions.state_delta` (`seed_app_settings`). In LangGraph it is a plain `store.put(("app",), ...)`.
- **ADK's built-in local memory service did not fit the write path.** ADK 2.13 ships `SqliteMemoryService`, but it indexes raw session events with keyword search and has no `delete_memory`. The module asks for reflections in, paraphrase-tolerant recall out, and deletion. So the ADK agent implements `BaseMemoryService` itself (about 60 lines). LangGraph's `SqliteStore` already had vector search, overwrite-by-key and delete.
- **ADK's built-in `load_memory` returns a stringified `MemoryEntry` repr to the model**, not JSON. The LangGraph tool returns JSON. The scenario's "empty recall" check accepts both forms.
- **State written by a tool** is `tool_context.state[...] = ...` in ADK. LangGraph needs a `Command(update=...)` carrying the `ToolMessage`. Store writes, however, are direct in both.

## Assumptions, each with a one-line defence

| # | assumption | defence |
|---|---|---|
| A1 | Kestrel Card, its customers, merchants and policy numbers (75-day window, 1.25% FX fee) are fictional | the policy numbers are deliberately unlike common real-world defaults, so a parametric answer is detectably different from a retrieved one |
| A2 | the customer is already authenticated by the app; `user_id` comes from the harness, never from the model | that is how logged-in support chat works, and it makes cross-customer access impossible by construction rather than by instruction |
| A3 | filing a dispute and changing the contact channel need step-up verification (last 4 + ZIP) *in the current session* | a changed contact channel is a standard account-takeover step; session scope is the narrowest scope that does not re-ask every turn |
| A4 | the harness owns the clock and the scenario injects simulated instants | follow-ups, expiry and retention are time-driven; real waiting is impossible, and an injected clock is the standard way to test time (Temporal's time-skipping test server does the same) |
| A5 | semantic memory is a closed schema of two customer-stated facts | the customer is the authority on their own preferences, so stating it *is* verification; free-form model-chosen keys are how contradictory duplicates appear |
| A6 | a travel notice expires the day after the return date; episodes are retained 180 days | both are per-data-class retention choices the module asks for; the numbers are illustrative, not regulatory |
| A7 | episodes are model-written reflections plus case outcomes read from the case system | the module's write path: the summary is what retrieval surfaces; the outcome code must come from the system of record, not the model's paraphrase |
| A8 | the case follow-up is scheduled by `file_dispute` itself, not by the model | a follow-up that depends on the model remembering to schedule it is a silent drop; customer-requested reminders do go through a model-called tool |
| A9 | a follow-up is `done` only when an outbound message tied to it exists | the done flag must be set on evidence, not on the model's claim; otherwise it retries (max 3) |
| A10 | outcomes on disputes of $200 or more go out only after `ops_reviewer` sign-off | customer-facing decisions on larger amounts getting human review is common practice and gives the approval field a real job |
| A11 | the back office's response is scripted: both cancelled-subscription disputes are rejected for missing cancellation proof | the module's promotion loop needs a recurring outcome; the merchant response is outside the agent's control in reality too |
| A12 | the knowledge base does not mention cancellation proof | customer-facing documents lag operational reality; the gap is what promotion closes |
| A13 | promotion threshold = the same outcome code in episodes from at least two different customers, plus a human reviewer; the reviewer is scripted in the run | one episode would turn an unlucky case into policy (the module's warning); "different customers" makes the evidence independent |
| A14 | promoted versions are written under `var/`, not committed | a re-run must start from v1; in production the write is a reviewed pull request against `procedure_versions/` |
| A15 | embeddings are local: fastembed `BAAI/bge-small-en-v1.5` (384-d, ONNX, CPU, ~64 MB, downloaded once into `var/`) | DeepSeek has no embeddings endpoint; sending customer episodes to a second vendor only to index them is a data-processing decision this demo cannot justify; paraphrased recall ("that streaming thing") needs more than keywords |
| A16 | transactions and cases are exact SQL lookups, never vector search | the module's recall-failure fix: a specific fact needs an exact lookup, or a neighbouring record can substitute for it |
| A17 | a pasted card number is masked at the harness boundary before the message enters the session | "never store secrets" has to cover the event log too, and the only place that covers every store at once is before the first write |
| A18 | the scripted customer turns front-load what an agent would ask for (verification details) | fixed scripts must not stall on a clarifying question; the checks then test memory, not dialogue luck |
| A19 | one model for everything (`deepseek-v4-flash`), default sampling, no retries | the same pattern as module 01; failures are recorded as they happened instead of being retried away |

## Running it

```bash
cd modules/07-memory-state/code
python3.13 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export DEEPSEEK_API_KEY=...        # or put it in a gitignored code/.env; module 01's .env is also read
```

Chat with either agent (sessions and memory persist under `var/<framework>/interactive/`):

```bash
python -m adk_agent.agent chat --user priya                 # 'exit' ends the session and writes its episode
python -m langgraph_agent.agent chat --user marco
python -m adk_agent.agent chat --user priya --session chat-1a2b3c4d          # continue a session
python -m adk_agent.agent chat --user priya --now 2026-12-03T10:00:00Z       # pretend it is later
python -m adk_agent.agent followups --now 2026-11-19T10:00:00Z               # fire whatever is due
```

Replay the whole scenario and regenerate its evidence:

```bash
python run_scenario.py --framework adk --run 1
python run_scenario.py --framework langgraph --run 1
python run_scenario.py --summarize
```

Run the harness itself, not `adk web`. The harness owns the clock, the card-number redaction and the session-end reflection, and `adk web` would bypass all three.

## Evidence: what was run and what failed

_Filled in from the recorded live runs; see [evidence/summary.md](evidence/summary.md) and [evidence/failures.md](evidence/failures.md)._
