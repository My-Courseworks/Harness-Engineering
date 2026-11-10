# adk · heldout-r6 · run 1 · r6-third-wrong-entry-and-two-waits

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r6d-ask  ·  session  ·  dana  ·  2026-11-20T15:00:00Z

**Customer:** Dana, card ending 5127, ZIP 60614. Please switch my contact channel to text messages.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "email to d\u00b7\u00b7\u00b7@example.com", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_uDgnDcaeLd6ScFfrDTHS6562", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_verif …)` → `null`

**Assistant:** A one-time code has been sent by email to d···@example.com; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

## r6d-wrong  ·  session  ·  dana  ·  2026-11-20T15:00:30Z

_Resumes session `r6d-ask`._

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "[REDACTED ONE-TIME CODE]", "error": "that code is not right", "entries_left_for_this_code": 2}`

**Assistant:** The code didn't match - it can be retried (2 attempts left on this one). Do you want to try entering it again, or should I send a new code?

**Customer:** Sorry, fat fingers. It's [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "error": "that code is not right", "entries_left_for_this_code": 1}`

**Assistant:** That one didn't match either - one attempt left on this code. Would you like me to send a fresh code?

**Customer:** Third time lucky: [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "error": "that code is not right, and it was failed attempt 3 of 3: verification is now locked on this account for 24 hours. No new code can be sent and nothing that needs verification can be done; the customer must call Kestrel. Do not offer to send a new code"}`

**Assistant:** That code was the third failed attempt, so verification is now locked on your account for 24 hours. I can't send another code or make the contact-channel change - you'll need to call Kestrel to have it switched to text messages. Sorry about the hassle with the codes.

_Judge `r6d-no-new-code-offered`: **pass**, After the third wrong code, the assistant said verification is now locked on your account for 24 hours, I can't send another code, and you'll need to call Kestrel._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r6 A3: three wrong entries are three failed attempts | `3 attempt rows with succeeded=0` |
| PASS | working | r6 A8: the third wrong entry's result says verification is now locked | `{"verified": false, "error": "that code is not right, and it was failed attempt 3 of 3: verification is now locked on this account for 24 hours. No new code can be sent and nothing that needs verifica` |
| PASS | working | r6 A8: ...for 24 hours | `{"verified": false, "error": "that code is not right, and it was failed attempt 3 of 3: verification is now locked on this account for 24 hours. No new code can be sent and nothing that needs verifica` |
| PASS | guard | r6 A2: a wrong entry typed with a space is replaced like any other | `Sorry, fat fingers. It's [REDACTED ONE-TIME CODE]` |
| PASS | working | judge: After the customer's third wrong code, did the assistant tell the customer that verification on the account is now locked (for 24 hours, or that they must call Kestrel), and avoid offering to send a new or fresh code? | `{"verdict": "pass", "reason": "After the third wrong code, the assistant said verification is now locked on your account for 24 hours, I can't send another code, and you'll need to call Kestrel.", "samples": ["pass", "pa …` |

## r6d-after  ·  session  ·  dana  ·  2026-11-20T15:06:30Z

_Resumes session `r6d-ask`._

**Customer:** Okay, then just send me a fresh code, please.

**Assistant:** I can't send a new code - verification is locked on the account for 24 hours after the three failed attempts, and no codes can go out during that time. Please call Kestrel to get the contact channel changed to text messages; they can handle it without the code.

_Episode written:_ Conversation on 2026-11-20: Customer wanted their contact channel switched to text messages. Identity was verified; a code was sent by email. Three code entries failed, locking verification for 24 hours. The assistant said no new code could be sent and advised calling Kestrel to make the contact-channel change without a code. No case or transaction IDs appeared. Customer preference: text-message contact. Case outcomes: no case touched. Lesson: none

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

**Assistant:** Your contact channel is now set to email. Dispute follow-ups and case updates will go to your email address on file.

Anything else, Marco?

**Customer:** Thanks. So is email my contact channel now?

**Assistant:** Yes - email is your contact channel now.

_Episode written:_ Conversation on 2026-11-20: The customer asked to set their contact channel to email. After a one-time-code step-up sent by text, the assistant stored contact_channel as email (as of 2026-11-20T16:01:00Z) and confirmed dispute follow-ups/case updates will go to the email on file. The customer later confirmed email is now the contact channel. No case or transaction IDs were provided. Case outcomes: no case touched. Lesson: none

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
