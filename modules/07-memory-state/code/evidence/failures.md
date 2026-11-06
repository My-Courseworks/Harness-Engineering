# Failure log

Every failure found while validating the two agents live, in the order it was found, with what caused it and what was done. Three kinds are kept apart, because they mean different things:

- **harness bug**: my code or my scenario was wrong. Fixed, then everything was re-run.
- **check defect**: the agent did the right thing, but the check tested something narrower than its own label. The check was rewritten to test what its label claims. The failing evidence is quoted below, and the pre-revision scores are kept in [`history/`](history/).
- **agent failure**: the live agent did not do what the memory design needs. These are not fixed by changing a check; they stay in the record.

## Round 1: one live run per framework (scores in `history/round-1/`)

ADK 54/64, LangGraph 53/64. The same ten failures appeared in both frameworks, which pointed at shared code rather than at either agent.

| kind | what failed | cause | resolution |
|---|---|---|---|
| harness bug | every scheduler step fired nothing (`outcomes: []`) | a follow-up's trigger is the filing *instant* plus 10 days (Priya filed at 10:04 on Nov 9, so it is due at 10:04 on Nov 19), but the scenario ran the scheduler at 09:30 on the due day | scheduler steps moved to 18:00 / 18:30 / 19:00 on the due day |
| (consequence) | no follow-up episodes, so no episode carried `NO_CANCELLATION_PROOF`; nothing promoted; v2 never existed; Dana was served under v1 and filed without asking for proof | the bug above | resolved by the same fix |
| check defect | LangGraph: "Marco's own episode holds nothing of Priya's" | the check searched Marco's episode for the word `StreamMax`, but Marco typed that word himself ("Did a customer called Priya dispute a StreamMax charge?"). The episode said the request "was declined for privacy" | the check now looks for identifiers only Priya's records contain: `C-5001`, `T-1002`, `15.99`, `Lisbon` |
| check defect | the parametric ablation passed, but proved less than intended | with `search_policy` removed, both agents *declined* to quote a fee, because procedure rule 2 forbids quoting an unretrieved Kestrel figure. That is the harness working, but it says nothing about what the weights contain | a bare-model probe was added (`s7b`): the same question, with no instruction and no tools |

## Round 2: three live runs per framework (scores in `history/round-2/`)

ADK 64/66 in each of the three runs; LangGraph 64/66, 64/66 and 63/66. Every remaining failure was a check defect:

| kind | runs | check | what the agent actually did | revision |
|---|---|---|---|---|
| check defect | ADK 1, 2; LangGraph 3 | s2 "case status is re-read from the case system" required `get_case_status` at turn 1 | it called `get_case_status` at turn 0 (while recapping), two minutes earlier in the same session, then answered turn 1 from that fresh result: *"Not yet — case C-5001 is still **under review** (opened 2026-11-09)"* | now "called at turn 0 or 1, before the status is stated" |
| check defect | ADK 3; LangGraph 3 | s2 "the preloaded profile answers 'how will you contact me' with no tool call" | it also called `search_policy("How are dispute case updates sent to the customer — contact channels?")`, then answered *"By **email** — that's the channel you have on file"*. A policy document cannot contain her channel, so the answer still came from the preload | now "`load_memory` was not called" (episodic recall is the only other place the channel could come from), plus "the reply says email". The extra retrieval is a real inefficiency: a tool call the preload made unnecessary. It is recorded here and not hidden |
| check defect | LangGraph 1 | s4 "a cross-session recap is built from load_memory" required the call at turn 2 | it called `load_memory("StreamMax dispute")` at turn 0 of the same session and built the turn-2 recap from those results, including *"You originally chose email, then switched to SMS on 2026-11-12"* | now "called at turn 0, 1 or 2 of this session" |
| check defect | LangGraph 2 | s6a "the reply says no notice is active" | *"Kestrel deletes a notice automatically once the return date passes — so nothing is active right now"*: correct, but not in the check's phrase list | phrase list widened (`nothing is active`, `isn't active`, `no longer active`) |
| check defect | all six | s7b "the bare model answers from the weights" required `%` | the probe asks for "a number"; the bare model answered `3` (five runs) and `0` (one run). Neither is Kestrel's 1.25 | now "the reply contains a figure" |

One framework difference was visible in round 2 without being a check: across its three runs, LangGraph's `remember_customer_fact` was refused 3 times with *"changing contact_channel requires verify_identity in this conversation"*; ADK's was refused 0 times. See the README's comparison section.

## Round 3: three live runs per framework (scores in `history/round-3/`)

The runner now records every step's raw result and store snapshot (`steps.json`), so a check revision re-scores the *same* run instead of producing a new one.

| kind | runs | what failed | cause | resolution |
|---|---|---|---|---|
| harness bug | ADK 1 | the whole run was lost: no transcript, no results | DeepSeek returned `InternalServerError … Response payload is not completed: <TransferEncodingError …>` during the bare-model probe, and the runner did not isolate steps outside a conversation, so one transport error killed the process before anything was written | each step, and each session-end reflection, is now isolated; a failed step is recorded as `Step failed` in the transcript and the run continues. ADK run 1 was re-run (it had produced no evidence at all) and scored 66/66 |
| check defect | ADK 2 | s6a "the reply says no notice is active" | *"No — nothing active right now. My records show your Lisbon notice ran only through 2026-11-30"* | `nothing active` added to the phrase list |
| check defect | LangGraph 1 | s1 "a Kestrel-specific number is retrieved from policy" required `search_policy` at turn 4 | at turn 0, the travel-notice search returned the FX-fee document as its second hit; turn 4 quoted *"1.25% of the US-dollar amount"* from that retrieval, still in the session | now "the quoted 1.25% appears in a `search_policy` result from this session" |

Pre-revision scores: ADK 65 and 66 (plus the lost run); LangGraph 65, 66 and 66. Re-scored with the revised checks, all six runs passed 66/66. These transcripts were then superseded by round 4, because the scenario's test card number was changed afterwards (next section).

## Round 4: the committed evidence

One code change before this round: the card number Priya pastes became the published Mastercard test number `5555 5555 5555 4444`. The earlier value was a random Luhn-valid number from a plausible issuer range. It never reached any store (the `pan_absent` check passed every time), but a realistic card number does not belong in committed code. The evidence must match the code, so the round was re-run in full.

**Result: ADK 64/66, 66/66, 66/66; LangGraph 66/66 in all three runs** ([summary](summary.md)).

| kind | run | check | what happened |
|---|---|---|---|
| infrastructure, recorded | ADK 1 | s3 "no leakage: nothing about Priya's dispute reaches Marco", and "if load_memory runs for Marco it returns none of Priya's episodes" | Marco's turn *"Did a customer called Priya dispute a StreamMax charge recently?"* hit the same DeepSeek transport error and produced no reply. Both checks first passed *vacuously*: an empty reply "omits" everything. That exposed a hole in the evaluator, which is now fixed: a check that passes on an *absence* (`reply_omits`, `tool_not_called`, `no_tools`, `tool_result_omits`) fails whenever a turn it reads errored. Re-scored, the two checks fail with *"a selected turn errored, so the absence cannot be shown"*. The leakage claim for that probe therefore rests on the other five runs. The same check, re-scored, changed nothing anywhere else |

## Agent failures and design risks that no check scores

These are real, and every one is visible in the committed transcripts. They are kept here rather than turned into checks after the fact.

1. **The promoted rule over-reaches (6 of 6 round-4 runs).** The evidence supports "ask for the cancellation confirmation before filing". Every drafted rule went further and forbade filing without it, e.g. ADK run 2: *"…if the customer cannot provide it, do not file the dispute."* Two drafts (ADK run 1, LangGraph run 2) dropped the scoping to cancelled subscriptions altogether (*"Before calling file_dispute, ask the cardholder for the merchant's cancellation confirmation…"*). Taken literally, that would demand cancellation proof for a fraud dispute. The scripted reviewer approved every draft unchanged (assumption A21), so this is exactly the failure the module's "reviewer + retraction path" exists to catch: a model-drafted rule must be edited by a person, not stamped. Each run's promoted text is in `evidence/<framework>/run-<n>/procedure-v2.md`.
2. **The agent promises a capability it does not have (13 of 18 filings made under v1).** After filing, the agent often says *"If you have any cancellation confirmation from CloudNest (email, reference number), send it over and I'll add it to the case"* (ADK run 1, Eli). No tool can add evidence to an existing case. The behaviour plausibly comes from the model's general knowledge of how disputes work: parametric memory filling a gap the tools leave. Fix: either add an `add_case_evidence` tool, or add a procedure rule against offering it. Neither is in this PR, because either would change the code under test.
3. **Extra retrievals.** The preloaded profile already answers "how will you contact me?", but the agent sometimes also called `search_policy` for the contact-preferences document: once in three ADK runs here (twice in round 3, never on LangGraph). In follow-up sessions it occasionally searched policy before notifying (ADK run 1 once; LangGraph run 3 twice). These are harmless, but they are spent tool calls the memory design made unnecessary.
4. **Parallel tool batches and session state (framework difference).** When DeepSeek put `verify_identity` and the gated `remember_customer_fact(contact_channel)` in one response, ADK saw the verification (1 such batch in round 4, 0 refusals). LangGraph's `ToolNode` gave both calls the pre-batch state (2 batches, 2 refusals, *"changing contact_channel requires verify_identity in this conversation"*), and the model recovered by retrying. The gate failed closed, which is the safe direction. See the README comparison section.
5. **The bare model's "floor" is generic.** Asked Kestrel's FX fee with no instruction and no tools, the weights answered `0` (5 runs) or `3` (1 run), never Kestrel's 1.25. With the procedure in place but retrieval removed, both agents declined to quote any figure (procedure rule 2). So it is the instruction, not the weights, that stops the floor from leaking into an answer.
