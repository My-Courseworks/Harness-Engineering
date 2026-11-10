# langgraph · heldout-r6 · run 1 · r6-third-wrong-entry-and-two-waits

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r6d-ask  ·  session  ·  dana  ·  2026-11-20T15:00:00Z

**Customer:** Dana, card ending 5127, ZIP 60614. Please switch my contact channel to text messages.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "email to d\u00b7\u00b7\u00b7@example.com", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `null`

**Assistant:** A one-time code has been sent by email to d···@example.com; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

## r6d-wrong  ·  session  ·  dana  ·  2026-11-20T15:00:30Z

_Resumes session `r6d-ask`._

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "[REDACTED ONE-TIME CODE]", "error": "that code is not right", "entries_left_for_this_code": 2}`

**Assistant:** The code didn't check out - it wasn't the right one. There are 2 attempts left on it, and it stays valid for a few more minutes (it expires at 15:05 UTC).

Would you like me to send a new code, or try again with the current one? Note the existing code goes to the email address the bank holds (d···@example.com) - a new one would go to the same place; codes can't be sent anywhere else.

**Customer:** Sorry, fat fingers. It's [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "error": "that code is not right", "entries_left_for_this_code": 1}`

**Assistant:** Still not right, I'm afraid - 1 attempt left on this code before it expires at 15:05 UTC.

Want me to send a fresh code (can be resent now, since more than 60 seconds have passed), or would you like one more try with the current one?

**Customer:** Third time lucky: [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "error": "that code is not right, and it was failed attempt 3 of 3: verification is now locked on this account for 24 hours. No new code can be sent and nothing that needs verification can be done; the customer must call Kestrel. Do not offer to send a new code"}`

**Assistant:** That was the third failed attempt, so verification is now locked on your account for 24 hours - no new code can be sent, and I can't complete the switch to text messages right now.

You'll need to call Kestrel to get this sorted; they can help with the contact channel change (or unlock verification) from there. Sorry for the hassle - once verification is available again, it's a quick change.

_Judge `r6d-no-new-code-offered`: **pass**, The assistant said, 'That was the third failed attempt, so verification is now locked on your account for 24 hours - no new code can be sent,' and 'You'll need to call Kestrel,' and did not offer a new code._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r6 A3: three wrong entries are three failed attempts | `3 attempt rows with succeeded=0` |
| PASS | working | r6 A8: the third wrong entry's result says verification is now locked | `{"verified": false, "error": "that code is not right, and it was failed attempt 3 of 3: verification is now locked on this account for 24 hours. No new code can be sent and nothing that needs verifica` |
| PASS | working | r6 A8: ...for 24 hours | `{"verified": false, "error": "that code is not right, and it was failed attempt 3 of 3: verification is now locked on this account for 24 hours. No new code can be sent and nothing that needs verifica` |
| PASS | guard | r6 A2: a wrong entry typed with a space is replaced like any other | `Sorry, fat fingers. It's [REDACTED ONE-TIME CODE]` |
| PASS | working | judge: After the customer's third wrong code, did the assistant tell the customer that verification on the account is now locked (for 24 hours, or that they must call Kestrel), and avoid offering to send a new or fresh code? | `{"verdict": "pass", "reason": "The assistant said, 'That was the third failed attempt, so verification is now locked on your account for 24 hours - no new code can be sent,' and 'You'll need to call Kestrel,' and did not …` |

## r6d-after  ·  session  ·  dana  ·  2026-11-20T15:06:30Z

_Resumes session `r6d-ask`._

**Customer:** Okay, then just send me a fresh code, please.

**Assistant:** I can't send one - verification is locked on the account for 24 hours after the three failed attempts, so no code can go out, fresh or otherwise.

Please call Kestrel; they can unlock it and set your contact channel to text messages.

_Episode written:_ Conversation on 2026-11-20: Customer Dana asked to switch contact channel to text messages. Identity was verified, but three one-time-code attempts failed; verification locked for 24 hours and no new code can be sent. The customer said the first error was 'fat fingers' (not verified). Assistant directed the customer to call Kestrel to unlock and change the channel. No case or transaction IDs provided. Case outcomes: no case touched. Lesson: After two failed code entries, recommend sending a fresh code instead of offering another attempt on the same code, to reduce the risk of a 24-hour verification lock.

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

**Assistant:** Your contact channel is now set to email. There was no previous preference on file, so nothing else changed.

You can switch it again or remove it any time; either needs the same identity check plus a one-time code.

**Customer:** Thanks. So is email my contact channel now?

**Assistant:** Yes - your contact channel is set to email, as of just now. That's where Kestrel will send account messages, including dispute follow-ups, unless you change it.

_Episode written:_ Conversation on 2026-11-20: The customer asked to set contact channel to email. After one-time-code verification, the assistant stored contact_channel=email (as_of 2026-11-20T16:01:00Z) and confirmed it; no prior preference existed. The assistant said future account messages, including dispute follow-ups, would go to email unless changed, and changing/removing later requires identity verification plus a one-time code. No case or transaction IDs mentioned. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r6 A9: the conversation keeps working: no turn errors | `"no errors"` |
| PASS | semantic | r6 A1: the code typed one digit at a time is accepted and the channel changes | `{"value": "email", "as_of": "2026-11-20T16:01:00Z", "expires_at": null}` |
| PASS | working | r6 A9: one wait was left, so the next message was a message: no failed attempt | `0 attempt rows with succeeded=0` |
| PASS | semantic | r6 A9: ...and it is answered | `Yes - your contact channel is set to email, as of just now. That's where Kestrel will send account messages, including dispute follow-ups, unless you change it.` |
| PASS | guard | r6 A6: the six separate digits are in no session store | `store files holding a sent code: []` |

## r6d-guesses-as-arguments  ·  forced_calls  ·  eli  ·  2026-11-20T17:00:00Z

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r6 A5: a guess passed as an argument is not an entry: none is evaluated | `{"error": null, "attempts_in_batch": 0, "failed_attempts": 0, "tool_results": ["send_verification_code -> {\"sent\": true, \"sent_to\": \"text message to \\u00b7\\u00b7\\u00b70188\", \"expires_in_minutes\": 5, \"resent\" …` |
| PASS | working | r6 A5: ...so the model cannot spend the customer's attempts | `0 attempt rows with succeeded=0` |
