# M7 code: seven memory types, one card-care desk, two frameworks

A customer-support agent for **Kestrel Card**, a fictional card issuer, built twice: once on **Google ADK** and once on **LangGraph**. Both share the same scenario, the same versioned procedure, the same bank systems and the same scheduler. Each puts the module's seven memory types ([README](../README.md#the-memory-taxonomy-seven-types-two-axes-four-scopes)) where that framework's own primitives put them.

Every claim below is backed by live runs against DeepSeek, in two forms:
- **The scripted scenario:** a month in the life of the desk.
- **An adversarial and unscripted suite** built from an interviewer's attempts to break the design. It was run once against the round-1 code (to reproduce the breaks) and again after the fixes.

See [Evidence](#evidence-what-was-run-and-what-failed).

```
modules/07-memory-state/code/
├── adk_agent/agent.py          ADK: Session/State scopes, a BaseMemoryService, load_memory, callbacks
├── langgraph_agent/agent.py    LangGraph: checkpointer threads, graph state, Store namespaces, ToolRuntime
├── cardcare/                   framework-free: everything both agents share
│   ├── world.py                the bank's systems of record (customers, ledger, cases, outbound messages)
│   ├── scheduler.py            prospective memory: the harness-owned follow-up scheduler
│   ├── memory_policy.py        the write path as code: fact schema, card-data masking, TTLs, retention, windows
│   ├── episodes.py             reflection: turns become validated episodes, incrementally
│   ├── procedures.py           procedural memory: versions, guarded promotion, retraction
│   ├── procedure_versions/v1.md  the baseline instruction both agents run
│   ├── retrieval.py            local embeddings and the policy knowledge base
│   ├── policy_kb/*.md          Kestrel's policy documents (external retrieval corpus)
│   ├── desk.py                 multi-step operations (file a dispute + schedule its follow-up)
│   ├── scenario.py             the scripted scenario, and every check kind
│   └── adversarial.py          the adversarial and unscripted suite
├── run_scenario.py             drives a framework through a suite and writes evidence/
├── review.py                   the reviewer's desk: promote/retract rules, approve/reject held messages
├── eval_retrieval.py           measures retrieval (embeddings vs keyword) on labelled queries
└── evidence/                   transcripts, raw step records, per-check results, failure log
```

## The scenario

Kestrel's card-care desk serves four logged-in cardholders over one simulated month, plus a jump past the retention windows:

| when (simulated) | who | what happens | memory types exercised |
|---|---|---|---|
| Nov 9 | Priya | sets a travel notice (Lisbon, to Nov 30) and email as contact channel; disputes "the later" of two StreamMax charges; asks what a chargeback is; asks the FX fee | semantic, working, external, prospective, parametric, episodic |
| Nov 12 | Priya | new session: "what did we sort out last time?"; "is it resolved?"; "how will you contact me?"; switches to SMS (re-verifies) | episodic, external, semantic, working |
| Nov 12 | Marco | asks what is on file for him; asks about "a customer called Priya"; disputes a $240 gym renewal | semantic + episodic leakage, prospective approval |
| Nov 18, Nov 20 | back office | two separate decisions: each cancelled-subscription dispute is rejected for `NO_CANCELLATION_PROOF` | (system of record) |
| Nov 19 | scheduler | Priya's follow-up fires and texts her (the channel she chose *after* the record was written) | prospective, semantic |
| Nov 20 | Priya | "why was it rejected?"; asks for a reminder on Nov 29; asks for a recap across conversations | external, prospective, episodic |
| Nov 22 | scheduler + ops | Marco's follow-up fires; the agent's draft is held; a reviewer approves *that text*, which is then sent once | prospective |
| Nov 23 | Marco, then reviewer | Marco asks why he was rejected; the recurring outcome (two customers, two decisions) is promoted: model draft → reviewer edit → v2 | procedural |
| Nov 24 | Dana, then Eli | Dana's identical dispute under v2 (asks for the reference first); a retraction drill restores v1 and lists Dana's conversation for review; Eli's identical dispute under v1 as the control | procedural |
| Nov 29 | scheduler | Priya's reminder fires | prospective |
| Dec 3 | Priya | travel notice has expired; sets and then deletes a new one; pastes a full card number | semantic (staleness, deletion), guard |
| Dec 3 | Priya, then the bare model | asks Kestrel's late fee, which no document holds: the agent declines, the bare model invents one | parametric |
| Jun 15 2027 | maintenance, Priya | episodes (180 days) and transcripts (30 days) past retention are deleted; "what did we talk about last time?" | episodic, working (forgetting) |

The domain was picked because every memory type has a non-contrived job in it, and because its failure modes are the module's ones with real consequences. A stale travel notice causes wrong fraud decisions. Leaking another cardholder's case is a privacy breach. A follow-up that never fires, or fires after the customer cancelled it, is a broken promise. A stored card number is a PCI incident.

## Where each memory type lives

| type | the module's framing | ADK | LangGraph |
|---|---|---|---|
| **Working / in-context** | the session, re-sent every turn, plus a scoped scratchpad; bounded | `Session` events in `DatabaseSessionService` (SQLite), re-sent up to 8 customer turns (`window_working_memory`, a `before_model_callback`). Session state: `identity_verified_at`, `identity_failed_attempts`, `followup_id`, `last_active_at`, `reflected_turns`, `episodes_written`, `erasure_requested_at`; `user:*`; `app:*`; `temp:now` (trimmed before persistence) | thread messages in `SqliteSaver`, re-sent up to 8 customer turns (`windowed_messages` in the agent node); the same fields as graph-state channels; `TurnContext.now` as per-invocation `context`, never checkpointed (the `temp:` analog). Threads have no owner, so the harness names them `<user>:<session>` |
| **Semantic** | facts, verified, timestamped, scoped, overwritten not appended | `user:contact_channel`, `user:travel_notice` written through `tool_context.state`, preloaded into the instruction by an `InstructionProvider` | `SqliteStore` namespace `("facts", user)`, key = fact name, `put()` overwrites, preloaded into the system prompt by the agent node |
| **Episodic** | what happened, as validated reflections, searched on demand | `EpisodeMemoryService(BaseMemoryService)`: `add_memory` / `search_memory` / `delete_memory` on SQLite + local embeddings, recalled by ADK's built-in `load_memory` | `SqliteStore` namespace `("episodes", user)` with a sqlite-vec index, recalled by a `load_memory` tool |
| **Procedural** | the versioned instruction, not a store; promotion needs evidence, a reviewer and a retraction path | the `InstructionProvider` reads the active version each turn | the agent node reads the active version each turn |
| **External / retrieval** | the store + a retriever; exact lookup for specific facts, vector search for related text | tools: `find_transactions`, `get_case_status` (exact SQL, scoped by `tool_context.user_id`), `search_policy` (embeddings) | the same tools, scoped by `runtime.context.user_id` |
| **Parametric** | the unmanaged floor | the DeepSeek weights, via `LiteLlm` | the DeepSeek weights, via `ChatDeepSeek` |
| **Prospective** | a scheduler the harness owns, never the memory store; five fields; "until done or cancelled" | `cardcare/scheduler.py`. Written by `file_dispute` and `schedule_reminder`, read by `list_my_followups`, cancelled by `cancel_reminder`. Fired by `tick` into a fresh session; a held draft is approved by a person before it is sent | the same scheduler, fired into a fresh thread |

The procedure, the bank, the scheduler and the write-path rules are shared code. That is deliberate: procedural and prospective memory are framework-independent by the module's own definition. The differences between the two agents are therefore all about *where state lives*, which is the comparison worth making.

### The write path, end to end

1. **Masking.** A customer message is masked for card data before it enters the session (`memory_policy.redact_card_secrets`).
   - Any run of 12 or more digits, whatever separates them, is masked.
   - So is a fragment that completes a Luhn-valid number together with the previous messages.
   - In a card-security context, short codes and expiries are masked too.
   - The agent sees only `[REDACTED …]` tokens, and claims masking only when it sees one (procedure rule 10).
2. **Semantic writes** are a closed schema, timestamped, overwritten by key, and gated. A contact-channel change needs a step-up verification less than 15 minutes old, with 3 attempts per conversation, enforced in the tool.
3. **Reflection is incremental.** A session records how many turns are already reflected, so nothing is reflected twice and a resumed session cannot re-create forgotten content. A turn leaving the 8-turn working window is reflected mid-session, so it stays recallable. Each reflection is validated before storage:
   - card data is masked again;
   - other customers' names, ids and cases are scrubbed;
   - unverified claims are labelled;
   - the outcome comes from the case system, not the model.
4. **Forgetting.**
   - `tick` runs maintenance: it closes idle chats (30 minutes), purges episodes after 180 days, and deletes transcripts (ADK sessions and their events; LangGraph threads and all checkpoints) 30 days after their last activity, then `VACUUM`s and checkpoints the SQLite files so deleted bytes do not survive in free pages or the WAL.
   - `request_memory_erasure` deletes everything about a customer when the conversation ends, the conversation included.
   - Bank records (cases, ledger, sent messages) are not memory and stay.

### What each framework made easy or awkward

- **Scope is a key prefix in ADK and a namespace convention in LangGraph.** ADK sessions are keyed by `(app, user, session)` and `user:` state is joined in automatically. LangGraph checkpointer threads have no owner, so per-user isolation of threads and of store namespaces is the harness's job (`thread_config`, `("facts", user)`).
- **`temp:` has no LangGraph equivalent in state.** Every state channel is checkpointed, so the per-invocation clock rides in `context` instead. Both suites check that no clock value is ever persisted.
- **App-wide state is event-sourced in ADK.** `app:` keys can only change through an event, so ops seeds them with `EventActions.state_delta` (`seed_app_settings`), and the harness writes its own session marks the same way (`write_session_state`). In LangGraph these are `store.put(("app",), ...)` and `update_state`.
- **ADK's built-in local memory service did not fit the write path.** ADK 2.13 ships `SqliteMemoryService`, but it indexes raw session events with keyword search and has no `delete_memory`. So the ADK agent implements `BaseMemoryService` itself. Measured, embeddings beat keyword search clearly ([evidence/retrieval](evidence/retrieval/results.md)): recall@1 0.80 against 0.47 on the policy KB, and 0.92 against 0.67 on an episode history. Both session stores *do* have a delete (`delete_session`, `delete_thread`); what they lacked was a policy that calls it.
- **Bounding working memory** is a `before_model_callback` that rewrites `llm_request.contents` in ADK, and a slice of `state["messages"]` in the LangGraph agent node. Both cut at a customer turn, so tool-call pairs stay whole.
- **LangGraph checkpoints serialise the whole message list on every step.** One pasted message becomes many copies across a thread's checkpoints, so erasure has to delete the thread, not edit a message.
- **Session state inside a parallel tool batch behaves differently.** In ADK, `tool_context.state` writes through to the live session, so `remember_customer_fact` sees a `verify_identity` from the same model response. In LangGraph, every call in a `ToolNode` batch reads the pre-batch state, and `Command` updates merge afterwards. The gated write is refused once and the model retries. The gate fails closed in both. Read-your-own-write across parallel tool calls is not a given in LangGraph.

## Assumptions, each with a one-line defence

| # | assumption | defence |
|---|---|---|
| A1 | Kestrel Card, its customers, merchants and policy numbers (75-day window, 1.25% FX fee) are fictional | nothing here imitates a real issuer; the parametric evidence uses a figure the KB does not hold (a late fee), so it does not rest on the numbers being invented |
| A2 | the customer is already authenticated by the app; `user_id` comes from the harness, never from the model | that is how logged-in support chat works, and it makes cross-customer access impossible by construction rather than by instruction |
| A3 | filing a dispute and changing the contact channel need a step-up verification (last 4 + ZIP) less than 15 minutes old, at most 3 attempts per conversation | a changed contact channel is a standard account-takeover step; a step-up proves possession now, not seven months ago; in production the step-up would be an OTP, and this is the shape of the gate, not its strength |
| A4 | the harness owns the clock and the scenario injects simulated instants (normalised to UTC) | follow-ups, expiry and retention are time-driven; an injected clock is the standard way to test time (Temporal's time-skipping test server does the same) |
| A5 | semantic memory is a closed schema of two customer-stated facts | the customer is the authority on their own preferences; free-form keys are how contradictory duplicates and poisoned "facts" (a claimed VIP fee waiver) get in |
| A6 | retention per data class: transcripts 30 days after last activity, episodes 180 days, a travel notice until the day after the trip; bank records keep their own retention | the raw transcript is the riskiest class, so it lives shortest; the numbers are illustrative, not regulatory |
| A7 | episodes are model-written reflections, validated before storage, plus case outcomes read from the case system | the module's write path: extraction is a candidate; validation masks card data, removes other customers, labels unverified claims |
| A8 | the case follow-up is scheduled by `file_dispute` itself; customer reminders only when the customer asks, and they can be listed and cancelled | a follow-up that depends on the model remembering to schedule it is a silent drop; "until done or cancelled" needs a cancel |
| A9 | a follow-up is `done` only when its message is sent; one message per follow-up, enforced in the tool | the done flag must be set on evidence, not on the model's claim; the baseline showed a reminder note could make the agent send three messages |
| A10 | messages for disputes of $200 or more are drafted by the agent and held; a person approves or rejects the drafted text | approval has to see the content it approves; approving "firing" approves nothing |
| A11 | the back office's decisions are scripted, one decision per case | the merchant response is outside the agent's control in reality too; separate decisions make the promotion evidence independent |
| A12 | the knowledge base does not mention cancellation proof | customer-facing documents lag operational reality; the gap is what promotion closes |
| A13 | promotion needs the same outcome in conversations with at least two different customers and from at least two separate decisions; scheduler-only sessions do not count | one episode, or one batch, would turn bad luck into policy (the module's warning) |
| A14 | promoted versions are written under `var/`, not committed; `review.py` is the product path | a re-run must start from v1; in production the write is a reviewed pull request against `procedure_versions/` |
| A15 | embeddings are local: fastembed `BAAI/bge-small-en-v1.5` (384-d, ONNX, CPU, ~64 MB) | DeepSeek has no embeddings endpoint; customer text stays on the machine; measured to beat keyword search on paraphrase (`eval_retrieval.py`) |
| A16 | transactions and cases are exact SQL lookups, never vector search | a specific fact needs an exact lookup, or a neighbouring record can stand in for it; `file_dispute` takes only an exact transaction id |
| A17 | card data is masked in free text at the harness boundary | the production design is a tokenising card-entry widget so free text never carries card data; the free-text mask is the backstop and assumes hostile formatting |
| A18 | the scripted scenario front-loads verification details; the adversarial and unscripted suite does not | a script must not stall on a clarifying question; the dialogue bugs that front-loading hides are what the second suite is for |
| A19 | one model for everything (`deepseek-v4-flash`), default sampling, no retries except one retry of an empty LangGraph turn | failures are recorded as they happened; the single retry closes a stall seen once in 240 LangGraph turns |
| A20 | the card number pasted in the scenarios is the published Mastercard test number `5555 5555 5555 4444` | a realistic-looking random number could collide with a real card |
| A21 | the reviewer in the runs is scripted and approves an edited rule, not the model's draft | the run must be unattended; the draft and the edit are both recorded, and a draft that refuses customers could not have shipped with ops approval alone |

## Running it

```bash
cd modules/07-memory-state/code
python3.13 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export DEEPSEEK_API_KEY=...        # or put it in a gitignored code/.env; module 01's .env is also read
```

Chat with either agent (sessions and memory persist under `var/<framework>/interactive/`):

```bash
python -m adk_agent.agent chat --user priya                 # 'exit' or end-of-input ends the session
python -m langgraph_agent.agent chat --user marco
python -m adk_agent.agent chat --user priya --session chat-1a2b3c4d          # continue a session
python -m adk_agent.agent chat --user priya --now 2026-12-03T10:00:00Z       # pretend it is later
python -m adk_agent.agent tick --now 2026-11-19T10:00:00Z    # fire what is due, then run memory maintenance
python -m adk_agent.agent tick --loop 60                     # the same on the wall clock, every minute
python review.py candidates --framework adk --var-dir var/adk/interactive    # promotion evidence + a model draft
python review.py held-messages --var-dir var/adk/interactive                 # drafts waiting for approval
```

Nothing fires by itself in chat mode; `tick` is the harness's background job. In production it would run under cron or a durable scheduler.

Replay the suites and regenerate the evidence:

```bash
python run_scenario.py --suite scripted --framework adk --run 1
python run_scenario.py --suite adversarial --framework langgraph --run 1
python run_scenario.py --rescore        # re-score recorded runs after a check changes (pure function of steps.json)
python run_scenario.py --summarize
python eval_retrieval.py
```

Run the harness itself, not `adk web`. The harness owns the clock, the card-data masking, reflection and maintenance, and `adk web` would bypass all of them.

## Evidence: what was run and what failed

**How it was validated.** No mocks and no unit tests. Every conversation below went to the real agent and the real model, from empty stores. Checks read only what a run produced (tool calls and results, replies, every store's contents, including raw file bytes), and each one is tagged with the memory type it proves. Open-ended replies are scored by an LLM judge whose verdict is recorded in the run's `steps.json`, so every check is a pure function of the record and `--rescore` never re-runs anything.

| suite | what it is | runs per framework | ADK | LangGraph |
|---|---|---|---|---|
| [scripted](evidence/scripted/summary.md) | the 22-step scenario above: 27 customer turns, 3 scheduler-fired sessions, reflections, a reviewed promotion, a retraction, a retention sweep; 70 checks | 3 | **210/210** | **210/210** |
| [adversarial + unscripted](evidence/adversarial/summary.md) | the round-1 interviewer's probes (card data in every format, other customers' names in rule text, a seven-month-old step-up, resumed expired sessions, cancel/readback/approval, refusals, lockout, erasure, overflow, a closed tab), plus five simulated customers who write each next line live; 67 checks | 2 | **134/134** | **133/134** |
| [adversarial, against the round-1 code](evidence/adversarial-baseline/summary.md) | the same suite before any fix, to reproduce the interviewer's findings | 1 | 40/66 | 37/66 |

| memory type | the claim, in one probe each (all live, both frameworks) |
|---|---|
| working | a step-up lasts 15 minutes and locks after 3 attempts (`g1/p1-s2-resumed-2027`, `g6-lockout`); the model sees at most 8 customer turns, and older ones are compacted into a recallable episode (`g8-overflow`: a detail from turn 1 is recalled at turn 14); `temp:now` / `TurnContext.now` never persist |
| semantic | last-stated value wins inside a session; "VIP fee waiver" is not stored; the profile, not recall, answers "how will you contact me"; an expired notice is deleted before the turn; another customer's facts never appear |
| episodic | recall across sessions on paraphrase; no other customer's case reaches Marco, Dana or a "husband" (`v2-marco-se`, `sim-fishing`); a resumed expired session recreates nothing (`g1/p1-s3-resumed-2027`); erasure leaves no fact, episode, transcript or byte (`g7-erasure`) |
| procedural | promotion needs two customers and two decisions; the rule every customer sees names nobody; a draft that refuses customers cannot ship with ops approval alone; under v2 a fraud dispute and an insisting customer's dispute are both filed; retraction lists the conversations held under v2 |
| external | exact ledger and case lookups; fresh case status even when the customer says "no need to look it up"; policy figures only from retrieval |
| parametric | asked Kestrel's late fee (in no document), the agent states no figure, while the bare model invents one (`s7`/`s7b`, `g4/p7`); no unattended message promises "we'll add it to your case" |
| prospective | records fire once, on time, on the channel on file at send time; a cancelled reminder never sends; "what is scheduled" comes from the scheduler; a held draft is sent only after a person approves its text; a reminder note cannot make the agent send three messages |
| guard | no card number, code or expiry reaches any store, in any format (dotted, slashed, double-spaced, split across turns, keyword-less "the three digits on the back are 737", or improvised by a simulated customer) |

Per run, under `evidence/<suite>/<framework>/run-<n>[/<group>]/`:
- `transcript.md`: every turn, tool call, reply, judge verdict and check;
- `steps.json`: the raw record the checks are computed from;
- `final-stores.json`: every store's contents at the end;
- `procedure-v2.md` where a rule was promoted.

`evidence/retrieval/results.md` measures embeddings against keyword search on labelled queries. `evidence/history/` keeps the scores of every earlier round. No file under `evidence/` holds a key or a store file. The only card number anywhere is the published test number, and it appears raw only in the round-1 baseline, where the bug was reproduced.

**What failed** (every round, with quotes: [evidence/failures.md](evidence/failures.md)):
- **Round 1:** the interviewer broke card-data masking, procedural scope, step-up expiry, retention, deletion, and prospective cancel / readback / approval, plus the promotion review. All of it reproduced in the baseline.
- **Round 2, found live:**
  - an unscripted customer slipped a run-together "number / expiry / code" past the masker;
  - deleted checkpoint bytes survived in LangGraph's WAL;
  - LangGraph stalled once on an empty turn.

  All three are fixed, and the suites were re-run.
- **Final round:** one judged failure. LangGraph filed an insisting customer's dispute, but its first reply listed the cancellation confirmation next to a real prerequisite, and the judge read that as implying it was required.
- **Still open:** fragmented card numbers typed across four messages; a reviewer who is scripted; a leak rate that is bounded, not measured.
