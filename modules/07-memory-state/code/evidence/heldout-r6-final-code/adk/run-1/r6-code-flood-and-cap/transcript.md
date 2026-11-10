# adk · heldout-r6 · run 1 · r6-code-flood-and-cap

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r6c-send-1  ·  forced_calls  ·  eli  ·  2026-11-19T09:00:00Z

## r6c-send-2  ·  forced_calls  ·  eli  ·  2026-11-19T09:01:05Z

## r6c-send-3  ·  forced_calls  ·  eli  ·  2026-11-19T09:02:10Z

## r6c-send-4  ·  forced_calls  ·  eli  ·  2026-11-19T09:03:15Z

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | r6 A7: four sends 65 seconds apart all go out | `4 one-time-code messages in the outbox` |

## r6c-send-5-three-at-once  ·  forced_calls  ·  eli  ·  2026-11-19T09:04:20Z

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | r6 A7: three sends in one response at the edge of the cap send one code: five in all | `5 one-time-code messages in the outbox` |
| PASS | working | r6 A7: ...without crashing | `{"error": null, "attempts_in_batch": 0, "failed_attempts": 0, "tool_results": ["send_verification_code -> {\"sent\": true, \"sent_to\": \"text message to \\u00b7\\u00b7\\u00b70188\", \"expires_in_minutes\": 5, \"resent\" …` |

## r6c-send-6  ·  forced_calls  ·  eli  ·  2026-11-19T09:05:30Z

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | r6 A7: the sixth send inside 24 hours sends nothing | `5 one-time-code messages in the outbox` |
| PASS | working | r6 A7: a refused send is not a failed attempt | `0 attempt rows with succeeded=0` |
| PASS | working | r6 A7: a refused send does not crash | `{"error": null, "attempts_in_batch": 0, "failed_attempts": 0, "tool_results": ["send_verification_code -> {\"error\": \"5 codes were sent to this account in the last 24 hours, which is the limit; no code is sent and none …` |

## r6c-asks-for-more  ·  session  ·  eli  ·  2026-11-19T09:12:00Z

**Customer:** Eli, card ending 6610, ZIP 73301. None of the codes you sent has reached me. Please send another one so I can switch my contact channel to email.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"error": "5 codes were sent to this account in the last 24 hours, which is the limit; no code is sent and none can be until 2026-11-20T09:00:00Z. A code already sent stays valid for its 5 minutes; otherwise the customer must call Kestrel"}`

**Assistant:** I verified your identity (card ending 6610, ZIP 73301), but I can't send another code: 5 codes have already gone to this account in the last 24 hours, which is the limit. No further code can be sent until 2026-11-20 at 09:00 UTC - and the code sent at 09:04 has since expired (codes last 5 minutes).

So switching your contact channel to email can't be completed right now through this chat. To get it done today, please call Kestrel and ask them to switch your contact channel to email; otherwise, message me after 09:00 UTC tomorrow and I'll send a new code.

_Episode written:_ Conversation on 2026-11-19: Customer wanted another code to switch contact channel to email, saying none of the codes reached them (not verified). Identity was verified, but sending was refused: five codes in 24 hours, so no new code until 2026-11-20 09:00 UTC. No case/transaction IDs were provided. Assistant advised calling Kestrel today or promised a new code via chat after 09:00 UTC tomorrow. Case outcomes: no case touched. Lesson: none

_Judge `r6c-says-the-limit`: **pass**, The assistant said "I can't send another code: 5 codes have already gone to this account in the last 24 hours, which is the limit. No further code can be sent until 2026-11-20 at 09:00 UTC" and did not claim a new code was sent._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r6 A7: five sends and a refusal did not lock the account: last four and ZIP still verify | `{"verified": true, "valid_for_minutes": 15}` |
| PASS | working | r6 A7: a send asked for in a new chat does not succeed | `{"error": "5 codes were sent to this account in the last 24 hours, which is the limit; no code is sent and none can be until 2026-11-20T09:00:00Z. A code already sent stays valid for its 5 minutes; ot` |
| PASS | external | r6 A7: ...and sends nothing: the cap is the account's, not the conversation's | `5 one-time-code messages in the outbox` |
| PASS | working | judge: Did the assistant tell the customer that no further one-time code can be sent for now because a limit on how many codes can be sent to the account (per day, or in 24 hours) has been reached, without claiming that a new code was sent? | `{"verdict": "pass", "reason": "The assistant said \"I can't send another code: 5 codes have already gone to this account in the last 24 hours, which is the limit. No further code can be sent until 2026-11-20 at 09:00 UTC …` |

## r6c-send-evening  ·  forced_calls  ·  eli  ·  2026-11-19T21:30:00Z

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | r6 A7: twelve hours later the five still count | `5 one-time-code messages in the outbox` |

## r6c-send-next-morning  ·  forced_calls  ·  eli  ·  2026-11-20T09:00:40Z

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | r6 A7: the window rolls: once the first send is 24 hours old, one more goes out | `6 one-time-code messages in the outbox` |
| PASS | guard | r6 D4: the run's record carries the hash of the code it ran on and a time | `{"code_sha256": "c1534120b95fb32fc56496964249031c30725afa99275a30ef10fa9654498612", "recorded_at": "2026-11-10T18:22:08Z"}` |
