# M7 code: seven memory types, one card-care desk, two frameworks

A customer-support agent for **Kestrel Card**, a fictional card issuer, built twice: once on **Google ADK** and once on **LangGraph**. Both share the same scenario, the same versioned procedure, the same bank systems and the same scheduler. Each puts the module's seven memory types ([README](../README.md#the-memory-taxonomy-seven-types-two-axes-four-scopes)) where that framework's own primitives put them.

Every claim below is backed by live runs against DeepSeek, in three forms:
- **The scripted scenario:** a month in the life of the desk.
- **An adversarial and unscripted suite** built from two rounds of an interviewer's attempts to break the design, plus fresh variants written before each round's fixes. Each round's new groups were first run against the previous round's code, to reproduce the breaks.
- **A held-out suite**, written before the round-3 fixes and run once, never tuned against.

Two offline measurements back the parts a live run cannot sample densely: the card-data masker (recall and precision on a tuning corpus, a held-out corpus and a seeded fuzzer) and the LLM judge (agreement with labelled transcripts).

See [Evidence](#evidence-what-was-run-and-what-failed).

```
modules/07-memory-state/code/
├── adk_agent/agent.py          ADK: Session/State scopes, a BaseMemoryService, load_memory, callbacks
├── langgraph_agent/agent.py    LangGraph: checkpointer threads, graph state, Store namespaces, ToolRuntime
├── cardcare/                   framework-free: everything both agents share
│   ├── world.py                the bank's systems of record (customers, ledger, cases, outbound messages)
│   ├── scheduler.py            prospective memory: the harness-owned follow-up scheduler
│   ├── memory_policy.py        the write path as code: fact schema, TTLs, lockout, retention, windows
│   ├── masking.py              card-data masking by normalisation, tokens and Luhn (customer text, model output, reasoning)
│   ├── privacy.py              the erasure ledger: requests, execution, tombstones
│   ├── episodes.py             reflection: turns become validated episodes, incrementally
│   ├── procedures.py           procedural memory: versions, guarded promotion, retraction
│   ├── procedure_versions/v1.md  the baseline instruction both agents run
│   ├── procedure_versions/reviewers.json  who may approve rules, and in which role
│   ├── retrieval.py            local embeddings and the policy knowledge base
│   ├── policy_kb/*.md          Kestrel's policy documents (external retrieval corpus)
│   ├── desk.py                 multi-step operations (file a dispute + schedule its follow-up)
│   ├── scenario.py             the scripted scenario, and every check kind
│   ├── adversarial.py          the adversarial and unscripted suite (tuning)
│   ├── heldout.py              the held-out live groups and masker corpus (never tuned against)
│   └── redaction_cases.py      the masker's tuning corpus
├── run_scenario.py             drives a framework through a suite and writes evidence/
├── review.py                   the reviewer's desk: promote/retract rules, approve/reject held messages
├── eval_retrieval.py           measures retrieval (embeddings vs keyword) on labelled queries
├── eval_redaction.py           measures the masker: recall and precision on tuning, held-out and fuzz corpora
├── eval_judge.py               measures the LLM judge against labelled transcripts
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
| **Working / in-context** | the session, re-sent every turn, plus a scoped scratchpad; bounded | `Session` events in `DatabaseSessionService` (SQLite), re-sent up to 8 customer turns (`window_working_memory`, a `before_model_callback`). Session state: `identity_verified_at`, `followup_id`, `followup_created_at`, `first_active_at`, `last_active_at`, `reflected_turns`, `episodes_written`; `user:*`; `app:*`; `temp:now` (trimmed before persistence). Failed verifications are not session state: they are counted on the account, in the bank | thread messages in `SqliteSaver`, re-sent up to 8 customer turns (`windowed_messages` in the agent node); the same fields as graph-state channels, `identity_verified_at` with a reducer so parallel calls cannot crash the step; `TurnContext.now` as per-invocation `context`, never checkpointed (the `temp:` analog). Threads have no owner, so the harness names them `<user>:<session>` |
| **Semantic** | facts, verified, timestamped, scoped, overwritten not appended | `user:contact_channel`, `user:travel_notice` written through `tool_context.state`, preloaded into the instruction by an `InstructionProvider` | `SqliteStore` namespace `("facts", user)`, key = fact name, `put()` overwrites, preloaded into the system prompt by the agent node |
| **Episodic** | what happened, as validated reflections, searched on demand | `EpisodeMemoryService(BaseMemoryService)`: `add_memory` / `search_memory` / `delete_memory` on SQLite + local embeddings, recalled by ADK's built-in `load_memory` | `SqliteStore` namespace `("episodes", user)` with a sqlite-vec index, recalled by a `load_memory` tool |
| **Procedural** | the versioned instruction, not a store; promotion needs evidence, a reviewer and a retraction path | the `InstructionProvider` reads the active version each turn | the agent node reads the active version each turn |
| **External / retrieval** | the store + a retriever; exact lookup for specific facts, vector search for related text | tools: `find_transactions`, `get_case_status` (exact SQL, scoped by `tool_context.user_id`), `search_policy` (embeddings) | the same tools, scoped by `runtime.context.user_id` |
| **Parametric** | the unmanaged floor | the DeepSeek weights, via `LiteLlm` | the DeepSeek weights, via `ChatDeepSeek` |
| **Prospective** | a scheduler the harness owns, never the memory store; five fields; "until done or cancelled" | `cardcare/scheduler.py`. Written by `file_dispute` and `schedule_reminder` (a local time and an IANA zone; one reminder per customer per day, a unique index), read by `list_my_followups`, cancelled by `cancel_reminder`. Fired by `tick` into a fresh session that has only read tools and `notify_customer`; one message per follow-up is a unique index on the outbox; a held draft is approved by a person, and a draft carrying a masking token cannot be approved | the same scheduler, fired into a fresh thread with the same reduced tool set |

The procedure, the bank, the scheduler and the write-path rules are shared code. That is deliberate: procedural and prospective memory are framework-independent by the module's own definition. The differences between the two agents are therefore all about *where state lives*, which is the comparison worth making.

### The write path, end to end

1. **Masking** (`cardcare/masking.py`). Card data is found by normalising and tokenising, not by listing formats.
   - The text is NFKC-normalised: every Unicode space and dash is mapped, zero-width characters are dropped, and number words ("seven", "oh") become digits.
   - Digit tokens that are identifiers (`C-5001`, `CN-77812`), amounts (`$240`, `39 euros`), clock times and real dates (`2026-11-03`, `Dec 2029`) never join a card candidate.
   - The rest are chained across separators and up to two words. A card number is 12+ digits joined by separators only, or a 13–19 digit Luhn-valid run, words between groups included, as long as it looks read out in sequence. A fragment that completes a Luhn-valid number with any of the previous three messages is masked too.
   - A 3-digit run is a security code, and in a message that carries card data so is any bare 3-digit number. A 4-digit run counts as one only next to a cue ("cvv", "back", "reverse"…), because last-fours, years and cancellation codes look the same. Expiries (`12/29`, `12-2029`, `Dec 2029`) are masked only when the message carries card data or says "expiry".
   - The same module masks the model's replies (card numbers only, so case ids and amounts survive) and its stored reasoning (every rule, since nobody reads it).
   - The agent sees `[REDACTED …]` tokens. It claims masking only when it sees one, never says data "was not stored", and never coaches a way around the mask (procedure rule 10).
   - Measured offline in [evidence/redaction](evidence/redaction/). The limits are stated in A17.
2. **Semantic writes** are a closed schema, timestamped, overwritten by key, and gated. A contact-channel change needs a step-up verification less than 15 minutes old, enforced in the tool. Three failed attempts lock verification **on the account** for 24 hours, in every conversation (`world.verification_attempts`).
3. **Reflection is incremental.** A session records how many turns are already reflected, so nothing is reflected twice and a resumed session cannot re-create forgotten content. A turn leaving the 8-turn working window is reflected mid-session, so it stays recallable. Each reflection is validated before storage:
   - card numbers are masked again;
   - other customers' names, case and transaction ids, last-fours and ZIPs are scrubbed;
   - unverified claims are labelled;
   - the outcome comes from the case system, not the model.
4. **Forgetting.**
   - `tick` runs maintenance. It closes idle chats (30 minutes) and purges episodes after 180 days. It deletes a transcript (ADK session and events; LangGraph thread and every checkpoint) 30 days after its **first** turn, so a session in constant use cannot keep day-0 text past its episode. Then it `VACUUM`s and checkpoints the SQLite files so deleted bytes do not survive in free pages or the WAL.
   - `request_memory_erasure` writes a durable request to the erasure ledger (`cardcare/privacy.py`). Every path runs pending requests: the end of the session, the maintenance run that eventually closes a closed tab, and the start of the customer's next turn anywhere.
   - Erasure deletes facts, episodes and transcripts. It cancels pending reminders and purges the note of every reminder record the customer had, then leaves a tombstone. A case follow-up that must still reach the customer after erasure sends its message but writes no transcript and no episode.
   - Bank records (cases, ledger, sent messages) are not memory and stay.

### What each framework made easy or awkward

- **Scope is a key prefix in ADK and a namespace convention in LangGraph.** ADK sessions are keyed by `(app, user, session)` and `user:` state is joined in automatically. LangGraph checkpointer threads have no owner, so per-user isolation of threads and of store namespaces is the harness's job (`thread_config`, `("facts", user)`).
- **`temp:` has no LangGraph equivalent in state.** Every state channel is checkpointed, so the per-invocation clock rides in `context` instead. Both suites check that no clock value is ever persisted.
- **App-wide state is event-sourced in ADK.** `app:` keys can only change through an event, so ops seeds them with `EventActions.state_delta` (`seed_app_settings`), and the harness writes its own session marks the same way (`write_session_state`). In LangGraph these are `store.put(("app",), ...)` and `update_state`.
- **ADK's built-in local memory service did not fit the write path.** ADK 2.13 ships `SqliteMemoryService`, but it indexes raw session events with keyword search and has no `delete_memory`. So the ADK agent implements `BaseMemoryService` itself. Measured, embeddings beat keyword search clearly ([evidence/retrieval](evidence/retrieval/results.md)): recall@1 0.80 against 0.47 on the policy KB, and 0.92 against 0.67 on an episode history. Both session stores *do* have a delete (`delete_session`, `delete_thread`); what they lacked was a policy that calls it.
- **Bounding working memory** is a `before_model_callback` that rewrites `llm_request.contents` in ADK, and a slice of `state["messages"]` in the LangGraph agent node. Both cut at a customer turn, so tool-call pairs stay whole.
- **LangGraph checkpoints serialise the whole message list on every step.** One pasted message becomes many copies across a thread's checkpoints, so erasure has to delete the thread, not edit a message.
- **Parallel tool calls are a different execution model.**
  - ADK 2.13 runs sync tools one at a time on the event loop, and `tool_context.state` writes through, so `remember_customer_fact` sees a `verify_identity` from the same model response.
  - LangGraph's `ToolNode` runs sync tools on a thread pool. Every call in a batch reads the pre-batch state, and `Command` updates merge afterwards. A plain channel written by two calls in one step raises `InvalidUpdateError`, and the crash leaves a dangling tool call that turns every later request into an HTTP 400.
  - So nothing that must hold under concurrency lives in the tools' read-then-write: "one message per follow-up" and "one reminder per day" are unique indexes, the failed-attempt count is rows in the bank, and `identity_verified_at` has a reducer.
  - Each turn first repairs interrupted tool calls, and the chat loop reports a failed turn instead of exiting. The forced-parallel probe (`g17`) drives both frameworks with three parallel calls in one model response.
- **A malformed tool call fails differently.** DeepSeek sometimes emits a call whose JSON arguments do not parse.
  - ADK ends the turn on `MALFORMED_FUNCTION_CALL`. The customer gets no reply and the dispute is silently not filed, but the session stays usable.
  - LangGraph puts the call in `invalid_tool_calls`, which ToolNode never runs. The turn ends with no reply, and the call stays in every later request with no result, so every later turn is an HTTP 400.
  - Both agents now answer it like any failing tool: it becomes a call to `report_malformed_tool_call` under the same id, and that tool returns the parse error, so the model makes the call again. ADK does this in `after_model_callback`, LangGraph in `route_malformed_calls`. The probe that forces it is `g19`.

## Assumptions, each with a one-line defence

| # | assumption | defence |
|---|---|---|
| A1 | Kestrel Card, its customers, merchants and policy numbers (75-day window, 1.25% FX fee) are fictional | nothing here imitates a real issuer; the parametric evidence uses a figure the KB does not hold (a late fee), so it does not rest on the numbers being invented |
| A2 | the customer is already authenticated by the app; `user_id` comes from the harness, never from the model | that is how logged-in support chat works, and it makes cross-customer access impossible by construction rather than by instruction |
| A3 | filing a dispute and changing the contact channel need a step-up verification (last 4 + ZIP) less than 15 minutes old; 3 failed attempts lock verification on the account for 24 hours, across conversations | a changed contact channel is a standard account-takeover step; a step-up proves possession now, not seven months ago; with the lock on the account, an attacker holding the unlocked phone gets 3 guesses a day, not 3 per new chat; in production the step-up would be an OTP plus an alert, and this is the shape of the gate, not its strength |
| A4 | the harness owns the clock and the scenario injects simulated instants (normalised to UTC) | follow-ups, expiry and retention are time-driven; an injected clock is the standard way to test time (Temporal's time-skipping test server does the same) |
| A5 | semantic memory is a closed schema of two customer-stated facts | the customer is the authority on their own preferences; free-form keys are how contradictory duplicates and poisoned "facts" (a claimed VIP fee waiver) get in |
| A6 | retention per data class: a transcript lives 30 days from its session's first turn (a session cannot be resumed past that), episodes 180 days, a travel notice until the day after the trip; bank records keep their own retention | the raw transcript is the riskiest class, so it lives shortest; capping the session's life, rather than counting from last activity, is what makes "no message older than 30 days" true per message; the numbers are illustrative, not regulatory |
| A7 | episodes are model-written reflections, validated before storage, plus case outcomes read from the case system | the module's write path: extraction is a candidate; validation masks card data, removes other customers, labels unverified claims |
| A8 | the case follow-up is scheduled by `file_dispute` itself; customer reminders only when the customer asks, and they can be listed and cancelled | a follow-up that depends on the model remembering to schedule it is a silent drop; "until done or cancelled" needs a cancel |
| A9 | a follow-up is `done` only when its message is sent; one message per follow-up and one reminder per customer per day, both unique indexes | the done flag must be set on evidence, not on the model's claim; a check in the tool is a race under LangGraph's thread pool (round 2: three messages for one follow-up), a constraint is not |
| A10 | messages for disputes of $200 or more are drafted by the agent and held; a person approves or rejects the drafted text | approval has to see the content it approves; approving "firing" approves nothing |
| A11 | the back office's decisions are scripted; each carries a `decision_id`, and a batch shares one | the merchant response is outside the agent's control in reality too; the id is what lets promotion count decisions, not cases |
| A12 | the knowledge base does not mention cancellation proof | customer-facing documents lag operational reality; the gap is what promotion closes |
| A13 | promotion needs the same outcome in conversations with at least two different customers and from at least two distinct `decision_id`s; scheduler-only sessions do not count | one episode, or one batch, would turn bad luck into policy (the module's warning); two cases closed in one batch count as one decision |
| A14 | promoted versions are written under `var/`, not committed; `review.py` is the product path | a re-run must start from v1; in production the write is a reviewed pull request against `procedure_versions/` |
| A15 | embeddings are local: fastembed `BAAI/bge-small-en-v1.5` (384-d, ONNX, CPU, ~64 MB) | DeepSeek has no embeddings endpoint; customer text stays on the machine; measured to beat keyword search on paraphrase (`eval_retrieval.py`) |
| A16 | transactions and cases are exact SQL lookups, never vector search | a specific fact needs an exact lookup, or a neighbouring record can stand in for it; `file_dispute` takes only an exact transaction id |
| A17 | card data is masked in free text at the harness boundary, by normalisation and Luhn; what it does **not** catch is stated, not hidden: numbers spelled as tens ("fifty-five fifty-five…") and spelled expiries ("twelve twenty-nine"); the first piece of a number sent in two halves when neither its message nor the one before it holds card data ("first half: 5555 5555" as the opening line), which cannot be told from an order number (the second piece is masked when it completes the number); a 4-digit security code with no cue. It also over-masks by design: any bare 3-digit number, and, about once in a thousand fuzzed messages, several unrelated numbers that happen to form a card-shaped Luhn run | the production design is a tokenising card-entry widget so free text never carries card data; the free-text mask is the backstop. Its recall and precision are measured, on a held-out corpus too ([evidence/redaction](evidence/redaction/)) |
| A18 | the scripted scenario front-loads verification details; the adversarial and unscripted suite does not | a script must not stall on a clarifying question; the dialogue bugs that front-loading hides are what the second suite is for |
| A19 | the agent and the simulated customers are `deepseek-v4-flash`; the judge is `deepseek-v4-pro`, sampled 3 times with a majority vote; default sampling, no retries except one retry of an empty LangGraph turn, and a malformed tool call answered with its parse error (both agents) so the model can make it again | the agent is not graded by itself; one judge sample was shown to flip at the margin; the judge's agreement with labelled transcripts is measured ([evidence/judge](evidence/judge/results.md)); a claim about the stores is never left to the judge, but paired with a scan of the store files |
| A20 | the card number pasted in the scenarios is the published Mastercard test number `5555 5555 5555 4444` | a realistic-looking random number could collide with a real card |
| A21 | the reviewer in the runs is scripted and approves an edited rule, not the model's draft; every rule learned from dispute outcomes needs an ops lead **and** the disputes policy owner, whatever its wording, and roles come from a registry (`reviewers.json`), not from the approver | routing by source cannot be paraphrased around, as a wording filter was (7 of 8 paraphrases shipped in round 2); the draft, the edit and the diff are recorded, and a promotion without its draft is refused; in production the registry is the identity provider, and this is the shape of the control |
| A22 | unattended sessions (a fired follow-up) have only read tools and `notify_customer` | they read text other people wrote (resolution notes, reminder notes), so least privilege is structural: an injected "call request_memory_erasure" has nothing to call |
| A23 | the held-out live groups and masker corpus (`cardcare/heldout.py`) were written before the round-3 fixes and run once; failures they exposed were fixed afterwards, with new tuning cases, and the held-out results stay as first recorded | a suite you tune against measures your tuning; a held-out set is the only honest estimate of the next unseen input, and it is spent once it has been looked at |

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
python review.py promote --framework adk --var-dir var/adk/interactive --code NO_CANCELLATION_PROOF \
    --draft "<the model draft>" --text "<your edited rule>" \
    --by "ops-lead (scripted reviewer)" --by "disputes-policy-owner (scripted reviewer)"
python review.py held-messages --var-dir var/adk/interactive                 # drafts waiting for approval
```

Nothing fires by itself in chat mode; `tick` is the harness's background job. In production it would run under cron or a durable scheduler.

Replay the suites and regenerate the evidence:

```bash
python run_scenario.py --suite scripted --framework adk --run 1
python run_scenario.py --suite adversarial --framework langgraph --run 1
python run_scenario.py --suite heldout --framework adk --run 1     # spent: see A23
python run_scenario.py --rescore        # re-score recorded runs after a check changes (pure function of steps.json)
python run_scenario.py --summarize
python eval_retrieval.py
python eval_redaction.py tuning         # also: heldout, fuzz (no model calls)
python eval_judge.py                    # the judge against labelled transcripts
```

Run the harness itself, not `adk web`. The harness owns the clock, the card-data masking, reflection and maintenance, and `adk web` would bypass all of them.

## Evidence: what was run and what failed

**How it was validated.** No mocks and no unit tests. Every conversation below went to the real agent and the real model, from empty stores.
- Checks read only what a run produced: tool calls and results, replies, and every store's contents, raw file bytes included. Each check is tagged with the memory type it proves.
- Open-ended replies are scored by an LLM judge (A19) whose verdicts are recorded in the run's `steps.json`. Every check is a pure function of that record, so `--rescore` never re-runs anything.
- Two probes force a model response instead of asking for one: `g17` forces parallel calls, and `g19` corrupts a tool call's arguments. Everything after the forced response is the real framework and the real model.

| suite | what it is | runs per framework | ADK | LangGraph |
|---|---|---|---|---|
| [scripted](evidence/scripted/summary.md) | the 22-step scenario above: 27 customer turns, 3 scheduler-fired sessions, reflections, a reviewed promotion, a retraction, a retention sweep | 3 | 202/213 | 213/213 |
| [adversarial + unscripted](evidence/adversarial/summary.md) | two review rounds of probes plus fresh variants (`g1`–`g19`): card data in every format, over-redaction, erasure from a closed tab, rolling retention, lockout across chats, parallel and malformed tool calls, injected notes, plus simulated customers who write each next line live | 2 | 194/196 | 195/196 |
| [held-out, blind](evidence/heldout/summary.md) | 3 groups written before the round-3 fixes and run once (A23) | 1 | 5/7 | 7/7 |
| [held-out, final code](evidence/heldout-final/summary.md) | the same groups on the committed code: no longer blind | 1 | 7/7 | 7/7 |
| [round-2 code vs round-3 variants](evidence/adversarial-baseline-r2/summary.md) | `g10`–`g18` run before any round-3 fix, to reproduce the round-2 review | 1 | 20/37 | 18/37 |
| [round-1 code](evidence/adversarial-baseline/summary.md) | the round-1 suite before any round-2 fix | 1 | 40/66 | 37/66 |

| offline measurement | result |
|---|---|
| [masker, tuning corpus](evidence/redaction/tuning.md) | recall 35/35, precision 28/28 |
| [masker, held-out corpus, blind](evidence/redaction/heldout-run-1.md) | recall **11/13**, precision 12/12: spelled tens and a spelled expiry are missed (A17) |
| [masker, seeded fuzzer](evidence/redaction/fuzz.md) | recall 1250/1250, precision 1249/1250 (the miss: a Luhn coincidence across three numbers) |
| [judge vs labelled transcripts](evidence/judge/results.md) | 14/14 majority verdicts, 41/42 single samples |
| [retrieval](evidence/retrieval/results.md) | embeddings recall@1 0.80 [0.55, 0.93] on the policy KB against keyword 0.47; with 8 near-miss distractors, 11/12 against 5/12 |

| memory type | the claim, in one probe each (all live, both frameworks) |
|---|---|
| working | a step-up lasts 15 minutes; 3 failures lock the account for 24 hours across chats (`g15`); the model sees at most 8 customer turns, and older ones are compacted into a recallable episode (`g8-overflow`); parallel and malformed tool calls never crash a turn or break the thread (`g17`, `g19`); `temp:now` / `TurnContext.now` never persist |
| semantic | last-stated value wins inside a session; "VIP fee waiver" is not stored; the profile, not recall, answers "how will you contact me"; an expired notice is deleted before the turn; the last four as typed still verifies (`g12`) |
| episodic | recall across sessions on paraphrase; no other customer's name, last four, case or transaction reaches another's reply or reflection (`v2-marco-se`, `sim-fishing`); erasure leaves no fact, episode, transcript, reminder note or byte, from a closed tab too, and nothing is recreated afterwards (`g7`, `g13`) |
| procedural | promotion needs two customers and two decisions; every dispute-derived rule needs the ops lead and the policy owner, so no paraphrase ships on ops alone (`ops_only_refused`); the rule names nobody; under v2 a fraud dispute and an insisting customer's dispute are both filed; retraction lists the conversations held under v2 |
| external | exact ledger and case lookups; fresh case status even when the customer says "no need to look it up"; policy figures only from retrieval; a numeric cancellation code reaches the case as evidence (`g12`) |
| parametric | asked Kestrel's late fee (in no document), the agent states no figure, while the bare model invents one (`s7`/`s7b`, `g4/p7`); no unattended message invites a reply |
| prospective | records fire once, on time, on the channel on file at send time; one message per follow-up and one reminder per day hold under parallel calls (`g16`, `g17`); a cancelled reminder never sends; "what is scheduled" comes from the scheduler; a held draft is sent only after a person approves its text, and a draft carrying a masking token cannot be approved; unattended sessions cannot reach erasure or forget tools (`g18`) |
| guard | no card number, code or expiry reaches any store in the formats tested (en-dash, NBSP, words between groups, split across turns, "on the reverse", improvised by simulated customers), checked by a scanner that decodes JSON escapes and number words; a claim that data was removed or not stored is checked against the store bytes. What it does not catch is listed in A17 |

Per run, under `evidence/<suite>/<framework>/run-<n>[/<group>]/`:
- `transcript.md`: every turn, tool call, reply, judge verdict and check;
- `steps.json`: the raw record the checks are computed from;
- `final-stores.json`: every store's contents at the end;
- `procedure-v2.md` where a rule was promoted.

`evidence/history/` keeps the scores of earlier rounds. No file under `evidence/` holds a key or a store file. The only card number anywhere is the published test number. It appears raw only in the baselines, where the bugs were reproduced, and in the masker corpora.

**What failed** (every round, with quotes: [evidence/failures.md](evidence/failures.md)):
- **Round 1:** the interviewer broke card-data masking, procedural scope, step-up expiry, retention, deletion, and prospective cancel / readback / approval, plus the promotion review. All of it reproduced in the baseline.
- **Round 2:** an unscripted customer slipped a run-together number past the masker; deleted bytes survived in the WAL; LangGraph stalled once. All fixed.
- **Round 3:** the second review got past the round-2 fixes with formats and paths the suite never sent. Fresh variants reproduced all of it on the round-2 code. Then the held-out run, the fuzzer and two more live passes found more:
  - span shadowing;
  - a reminder note surviving erasure;
  - security codes chained to ZIPs;
  - number words read as identifiers;
  - a cross-message Luhn coincidence that masked a last four;
  - malformed tool calls that silently dropped a dispute (ADK) or broke the thread (LangGraph);
  - a procedure regression of my own.

  All are fixed and re-run.
- **Final pass:** scripted ADK 202/213 and LangGraph 213/213; adversarial ADK 194/196 and LangGraph 195/196. One ADK scripted run asked again for already-typed verification details and never filed, and the 10 checks that depend on that case fell with it. One ADK judged reply called the confirmation "the required proof" (after filing at once). One false failure of the blunt "reply" check ("Reply here isn't possible on this message"). In one LangGraph `g15` run the agent held back the third wrong attempt, so the lock was never reached. All are quoted, with why each stays, in the failure log.
- **Still open:** the masker limits in A17; fired reminders keep their notes on the scheduler record until erasure (no age-based sweep yet); an ADK dialogue failure that asks again for already-typed details (fails closed); a reviewer who is scripted; a leak rate that is bounded, not measured.
