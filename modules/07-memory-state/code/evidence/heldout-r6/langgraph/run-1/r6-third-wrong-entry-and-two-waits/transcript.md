# langgraph · heldout-r6 · run 1 · r6-third-wrong-entry-and-two-waits

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r6d-ask  ·  session  ·  dana  ·  2026-11-20T15:00:00Z

**Customer:** Dana, card ending 5127, ZIP 60614. Please switch my contact channel to text messages.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "email to d\u00b7\u00b7\u00b7@example.com", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `null`

**Assistant:** I'll verify you first.

## r6d-wrong  ·  session  ·  dana  ·  2026-11-20T15:00:30Z

_Resumes session `r6d-ask`._

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "[REDACTED ONE-TIME CODE]", "error": "that code is not right", "entries_left_for_this_code": 2}`

**Assistant:** The one-time code didn't check out - I sent it to the email address the bank holds on your account, d···@example.com, and it can't be sent anywhere else. That code is still open for another couple of tries, and a new one would arrive by the same route.

Would you like me to send a fresh code, or would you rather try again with the one you have? Once it confirms, I'll switch your contact channel to text messages (SMS) right away.

**Customer:** Sorry, fat fingers. It's [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "error": "that code is not right", "entries_left_for_this_code": 1}`

**Assistant:** That one didn't match either. That code now has just one try left on it.

I can send you a fresh code to d···@example.com instead - just say the word and I'll send it. If the code expires or runs out of tries, we'll need a new one to finish the switch to text messages.

**Customer:** Third time lucky: [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "error": "that code is not right, and it was failed attempt 3 of 3: verification is now locked on this account for 24 hours. No new code can be sent and nothing that needs verification can be done; the customer must call Kestrel. Do not offer to send a new code"}`

**Assistant:** That code was the third miss, so verification is now locked on your account for 24 hours. No new code can be sent, and nothing that needs verification - including changing your contact channel to text messages - can be done until the lock clears.

Please call Kestrel to get this handled; they can take you through it directly. Sorry for the trouble.

_Judge `r6d-no-new-code-offered`: **pass**, The assistant said 'verification is now locked on your account for 24 hours. No new code can be sent' and 'Please call Kestrel to get this handled,' without offering a new code._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r6 A3: three wrong entries are three failed attempts | `3 attempt rows with succeeded=0` |
| PASS | working | r6 A8: the third wrong entry's result says verification is now locked | `{"verified": false, "error": "that code is not right, and it was failed attempt 3 of 3: verification is now locked on this account for 24 hours. No new code can be sent and nothing that needs verifica` |
| PASS | working | r6 A8: ...for 24 hours | `{"verified": false, "error": "that code is not right, and it was failed attempt 3 of 3: verification is now locked on this account for 24 hours. No new code can be sent and nothing that needs verifica` |
| PASS | guard | r6 A2: a wrong entry typed with a space is replaced like any other | `Sorry, fat fingers. It's [REDACTED ONE-TIME CODE]` |
| PASS | working | judge: After the customer's third wrong code, did the assistant tell the customer that verification on the account is now locked (for 24 hours, or that they must call Kestrel), and avoid offering to send a new or fresh code? | `{"verdict": "pass", "reason": "The assistant said 'verification is now locked on your account for 24 hours. No new code can be sent' and 'Please call Kestrel to get this handled,' without offering a new code.", "samples" …` |

## r6d-after  ·  session  ·  dana  ·  2026-11-20T15:06:30Z

_Resumes session `r6d-ask`._

**Customer:** Okay, then just send me a fresh code, please.

**Assistant:** I can't - the lock blocks any new code for 24 hours, so sending one now isn't possible. Nothing that needs verification can be done in the meantime, including the switch to text messages.

Please call Kestrel; they can take care of it directly.

_Episode written:_ Conversation on 2026-11-20: Customer wanted contact channel switched to text messages. Identity was verified, but three one-time code attempts failed, locking verification for 24 hours. No new code could be sent and verification-required actions, including the switch, were blocked. Assistant advised calling Kestrel. Customer later asked for a fresh code; assistant explained the lock prevented it. No switch was completed. Case outcomes: no case touched. Lesson: none

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

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-20T16:01:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Your contact channel is now set to email. The one-time code went to the mobile number the bank holds (···0133) and checked out.

Anything else I can help with?

**Customer:** Thanks. So is email my contact channel now?

**Assistant:** Yes - email is your contact channel on file now, as of a few minutes ago. Anything else?

_Episode written:_ Conversation on 2026-11-20: Customer asked to change their contact channel to email. After step-up verification, the assistant stored contact_channel=email (as_of 2026-11-20T16:01:00Z) and confirmed email is now on file. No case or transaction ID was provided; no promises were made. Customer preference: email contact. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r6 A9: the conversation keeps working: no turn errors | `"no errors"` |
| PASS | semantic | r6 A1: the code typed one digit at a time is accepted and the channel changes | `{"value": "email", "as_of": "2026-11-20T16:01:00Z", "expires_at": null}` |
| PASS | working | r6 A9: one wait was left, so the next message was a message: no failed attempt | `0 attempt rows with succeeded=0` |
| PASS | semantic | r6 A9: ...and it is answered | `Yes - email is your contact channel on file now, as of a few minutes ago. Anything else?` |
| PASS | guard | r6 A6: the six separate digits are in no session store | `store files holding a sent code: []` |

## r6d-guesses-as-arguments  ·  forced_calls  ·  eli  ·  2026-11-20T17:00:00Z

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r6 A5: a guess passed as an argument is not an entry: none is evaluated | `{"error": null, "attempts_in_batch": 0, "failed_attempts": 0, "tool_results": ["send_verification_code -> {\"sent\": true, \"sent_to\": \"text message to \\u00b7\\u00b7\\u00b70188\", \"expires_in_minutes\": 5, \"resent\" …` |
| PASS | working | r6 A5: ...so the model cannot spend the customer's attempts | `0 attempt rows with succeeded=0` |
