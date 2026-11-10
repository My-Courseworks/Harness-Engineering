# adk · heldout-r6 · run 1 · r6-third-wrong-entry-and-two-waits

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r6d-ask  ·  session  ·  dana  ·  2026-11-20T15:00:00Z

**Customer:** Dana, card ending 5127, ZIP 60614. Please switch my contact channel to text messages.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "email to d\u00b7\u00b7\u00b7@example.com", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_ET_ZZP8dq2XKmwIpIC8Gek60052", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_ve …)` → `null`

**Assistant:** A one-time code has been sent by email to d···@example.com; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

## r6d-wrong  ·  session  ·  dana  ·  2026-11-20T15:00:30Z

_Resumes session `r6d-ask`._

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "[REDACTED ONE-TIME CODE]", "error": "that code is not right", "entries_left_for_this_code": 2}`

**Assistant:** I've verified your identity, and I sent a one-time code to the email we hold on file (d···@example.com). It can only go there, not to another address or number.

The code you entered wasn't right, I'm afraid - you have 2 attempts left on this code (it's valid for about 5 minutes). Would you like me to send you a new code instead?

**Customer:** Sorry, fat fingers. It's [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "error": "that code is not right", "entries_left_for_this_code": 1}`

**Assistant:** That one wasn't right either, I'm afraid - only 1 attempt left on this code. I'd suggest I send you a fresh code rather than risk using up the last try. Shall I send a new one to d···@example.com?

**Customer:** Third time lucky: [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "error": "that code is not right, and it was failed attempt 3 of 3: verification is now locked on this account for 24 hours. No new code can be sent and nothing that needs verification can be done; the customer must call Kestrel. Do not offer to send a new code"}`

**Assistant:** That code wasn't right either, and that was the third failed attempt - verification is now locked on your account for 24 hours. I can't send another code or make any change that needs verification (including the switch to text messages) until then. Please call Kestrel to get this sorted; they can help you with the contact channel change.

Your contact channel is still unchanged (no channel set, so follow-ups go by secure message in the Kestrel app). Sorry for the hassle.

_Judge `r6d-no-new-code-offered`: **pass**, The assistant said "verification is now locked on your account for 24 hours" and "Please call Kestrel to get this sorted", and did not offer a new code._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r6 A3: three wrong entries are three failed attempts | `3 attempt rows with succeeded=0` |
| PASS | working | r6 A8: the third wrong entry's result says verification is now locked | `{"verified": false, "error": "that code is not right, and it was failed attempt 3 of 3: verification is now locked on this account for 24 hours. No new code can be sent and nothing that needs verifica` |
| PASS | working | r6 A8: ...for 24 hours | `{"verified": false, "error": "that code is not right, and it was failed attempt 3 of 3: verification is now locked on this account for 24 hours. No new code can be sent and nothing that needs verifica` |
| PASS | guard | r6 A2: a wrong entry typed with a space is replaced like any other | `Sorry, fat fingers. It's [REDACTED ONE-TIME CODE]` |
| PASS | working | judge: After the customer's third wrong code, did the assistant tell the customer that verification on the account is now locked (for 24 hours, or that they must call Kestrel), and avoid offering to send a new or fresh code? | `{"verdict": "pass", "reason": "The assistant said \"verification is now locked on your account for 24 hours\" and \"Please call Kestrel to get this sorted\", and did not offer a new code.", "samples": ["pass", "pass", "p …` |

## r6d-after  ·  session  ·  dana  ·  2026-11-20T15:06:30Z

_Resumes session `r6d-ask`._

**Customer:** Okay, then just send me a fresh code, please.

**Assistant:** I'm sorry - I can't send a new code. Verification on your account is locked for 24 hours after the three failed attempts, so no code can be sent and no verification-required change can go through until then. You'll need to call Kestrel to get the contact channel switched to text messages.

_Episode written:_ Conversation on 2026-11-20: Dana wanted the contact channel switched to text messages. Identity was verified; a code was sent to the email on file. The customer entered wrong codes three times, so verification locked for 24 hours. No case/transaction IDs were provided. The assistant could not send a new code or make the change and advised calling Kestrel. The channel remains unchanged. The customer said the errors were due to 'fat fingers' (not verified). Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | r6 A8: no code is sent to a locked account | `1 one-time-code messages in the outbox` |
| PASS | working | r6 A8: a send, if tried, is refused | `not called` |
| PASS | semantic | r6 A8: nothing changed | `null` |

## r6d-two-waits  ·  forced_calls  ·  marco  ·  2026-11-20T16:00:00Z

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r6 A9: a response that opens two waits does not crash | `{"error": null, "attempts_in_batch": 0, "failed_attempts": 0, "tool_results": ["send_verification_code -> {\"sent\": true, \"sent_to\": \"text message to \\u00b7\\u00b7\\u00b70133\", \"expires_in_minutes\": 5, \"resent\" …` |
| PASS | external | r6 A9: ...and sends one code | `1 one-time-code messages in the outbox` |

## r6d-two-waits-go-on  ·  session  ·  marco  ·  2026-11-20T16:01:00Z

_Resumes session `forced-r6d-two-waits`._

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "customer_wrote": "[REDACTED ONE-TIME CODE]", "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "customer_wrote": "[REDACTED ONE-TIME CODE]", "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-20T16:01:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Done - your contact channel is now set to **email**. (A one-time code went to the mobile number ending ···0133 and was confirmed, so the change is complete.)

Anything else, Marco - a travel notice, or a question about a charge?

**Customer:** Thanks. So is email my contact channel now?

**Assistant:** Yes - email is your contact channel now.

_Episode written:_ Conversation on 2026-11-20: Marco asked to change his contact channel to email. A one-time code was sent to his mobile ending 0133 and verified. The contact channel was stored as email as of 2026-11-20T16:01:00Z, and the assistant confirmed the change was complete. No promises were made, and no case or transaction IDs were provided. Preference: email contact. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r6 A9: the conversation keeps working: no turn errors | `"no errors"` |
| PASS | semantic | r6 A1: the code typed one digit at a time is accepted and the channel changes | `{"value": "email", "as_of": "2026-11-20T16:01:00Z", "expires_at": null}` |
| PASS | working | r6 A9: one wait was left, so the next message was a message: no failed attempt | `0 attempt rows with succeeded=0` |
| PASS | semantic | r6 A9: ...and it is answered | `Yes - email is your contact channel now.` |
| PASS | guard | r6 A6: the six separate digits are in no session store | `store files holding a sent code: []` |

## r6d-guesses-as-arguments  ·  forced_calls  ·  eli  ·  2026-11-20T17:00:00Z

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r6 A5: a guess passed as an argument is not an entry: none is evaluated | `{"error": null, "attempts_in_batch": 0, "failed_attempts": 0, "tool_results": ["send_verification_code -> {\"sent\": true, \"sent_to\": \"text message to \\u00b7\\u00b7\\u00b70188\", \"expires_in_minutes\": 5, \"resent\" …` |
| PASS | working | r6 A5: ...so the model cannot spend the customer's attempts | `0 attempt rows with succeeded=0` |
