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

**Assistant:** I tried, but I can't send another code: **5 codes have gone to this account in the last 24 hours, which is the limit**, so no new code can be sent until **2026-11-20 09:00 UTC**. A code can only ever go to the mobile number or email Kestrel already holds for you - it can't be redirected to a different address.

Since none of the codes has reached you, the quickest fix is to **call Kestrel** and have them check the contact details they hold for you; they can also switch your contact channel to email over the phone.

Your identity check (card ending 6610, ZIP 73301) is done and valid for 15 minutes, but without a one-time code I can't change the contact channel from here.

_Episode written:_ Conversation on 2026-11-19: The customer said no verification codes reached them (not verified) and wanted another to switch contact channel to email. Identity verification succeeded for 15 minutes. Code sending failed: 5 codes/24h limit, no new code until 2026-11-20T09:00:00Z. No case/transaction IDs provided. Assistant advised calling Kestrel to check contact details and change the channel. Case outcomes: no case touched. Lesson: none

_Judge `r6c-says-the-limit`: **pass**, The assistant said, "I can't send another code: 5 codes have gone to this account in the last 24 hours, which is the limit, so no new code can be sent until 2026-11-20 09:00 UTC," and did not claim a new code was sent._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r6 A7: five sends and a refusal did not lock the account: last four and ZIP still verify | `{"verified": true, "valid_for_minutes": 15}` |
| PASS | working | r6 A7: a send asked for in a new chat does not succeed | `{"error": "5 codes were sent to this account in the last 24 hours, which is the limit; no code is sent and none can be until 2026-11-20T09:00:00Z. A code already sent stays valid for its 5 minutes; ot` |
| PASS | external | r6 A7: ...and sends nothing: the cap is the account's, not the conversation's | `5 one-time-code messages in the outbox` |
| PASS | working | judge: Did the assistant tell the customer that no further one-time code can be sent for now because a limit on how many codes can be sent to the account (per day, or in 24 hours) has been reached, without claiming that a new code was sent? | `{"verdict": "pass", "reason": "The assistant said, \"I can't send another code: 5 codes have gone to this account in the last 24 hours, which is the limit, so no new code can be sent until 2026-11-20 09:00 UTC,\" and did …` |

## r6c-send-evening  ·  forced_calls  ·  eli  ·  2026-11-19T21:30:00Z

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | r6 A7: twelve hours later the five still count | `5 one-time-code messages in the outbox` |

## r6c-send-next-morning  ·  forced_calls  ·  eli  ·  2026-11-20T09:00:40Z

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | r6 A7: the window rolls: once the first send is 24 hours old, one more goes out | `6 one-time-code messages in the outbox` |
| PASS | guard | r6 D4: the run's record carries the hash of the code it ran on and a time | `{"code_sha256": "669b5fc87d9a8906480441d0e64ff271fc34ae06e5b3b99c182dbb9d0efca5f1", "recorded_at": "2026-11-10T17:05:53Z"}` |
