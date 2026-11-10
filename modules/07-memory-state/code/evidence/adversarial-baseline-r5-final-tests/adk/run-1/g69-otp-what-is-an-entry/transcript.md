# adk · adversarial · run 1 · g69-otp-what-is-an-entry

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## en-s1  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Priya here, card ending 4427, ZIP 94107. Switch my contact channel to email.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70100", "expires_in_minutes": 5, "resent": false}`

**Assistant:** I've verified you. A one-time code is on its way by text message to ···0100 - that's the number the bank holds, and it can't be sent anywhere else. Please type it here when it arrives.

**Customer:** It hasn't arrived. Is it going to the number ending 0100? I'm in 94

**Assistant:** Yes - it went by text to the number ending 0100, the one the bank holds on the account. It can't be sent to any other number or address. The code is valid for 5 minutes from when it was sent.

If it hasn't shown up, I can send a new code (the bank allows a resend after 60 seconds) - just say the word. Also, you mentioned "I'm in 94" - could you clarify what you meant by that?

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({"entered": "[REDACTED ONE-TIME CODE]"})` → `{"verified": true, "valid_for_minutes": 15, "customer_entered": "[REDACTED ONE-TIME CODE]", "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-09T10:04:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Code confirmed - your contact channel is now set to email. Anything Kestrel sends you will go to the email address on file instead of text message.

Was there anything else - for instance, what you meant by "I'm in 94"?

_Episode written:_ Conversation on 2026-11-09: Priya wanted contact channel switched to email. Verified; a code was sent by text to bank-held number ending 0100 (valid 5 minutes), and customer said it had not arrived (not verified). She entered confirmed code; email stored as preference, and Kestrel messages will go there. No case/transaction IDs appeared. Customer said I'm in 94 (not verified); clarification unresolved. Case outcomes: no case touched. Lesson: When a customer sends a truncated or unclear message, clarify it promptly rather than leaving ambiguity unresolved after completing the request.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | a message whose digits happen to total six is not a guess: no failed attempt | `0 attempt rows with succeeded=0` |
| PASS | semantic | the code typed after it is accepted | `{"value": "email", "as_of": "2026-11-09T10:04:00Z", "expires_at": null}` |

## en-other-chat  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

_Resumes session `en-wait`._

**Customer:** Marco, card ending 8830, ZIP 10011. Change my contact channel to email.

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70133", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_ET_3MAlNE0F9VOLuvViOk5o0235", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_ve …)` → `null`

**Assistant:** A one-time code has been sent by text message to ···0133; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

## en-other-chat-2  ·  session  ·  marco  ·  2026-11-12T10:01:00Z

_Resumes session `en-elsewhere`._

**Customer:** Different question while I wait: is [REDACTED ONE-TIME CODE] one of your reference numbers?

- `confirm_verification_code({"entered": "[REDACTED ONE-TIME CODE]"})` → `{"verified": false, "error": "that code is not right", "entries_left_for_this_code": 2, "customer_entered": "[REDACTED ONE-TIME CODE]"}`

**Assistant:** That wasn't a reference number - what you typed went in as the one-time code for the verification step, and it isn't the right one (two tries left on it).

Would you like me to send a new code?

_Episode written:_ Conversation on 2026-11-12: Customer asked whether a code they supplied was one of the issuer's reference numbers. It was submitted as a one-time verification code; the check returned that it was not right, with two attempts left. The assistant explained this and offered to send a new code; no case or transaction ID was provided, and no outcome was confirmed. Case outcomes: no case touched. Lesson: Next time, first clarify the purpose of a customer-provided code before submitting it for verification, to avoid using a verification attempt while answering a reference-number question.

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | six digits typed in another conversation are not checked against the code: no attempt | `1 attempt rows with succeeded=0` |
| PASS | working | the code stays open for the conversation that asked for it | `challenges: [('open', '2026-11-12T10:00')]` |

## en-back  ·  session  ·  marco  ·  2026-11-12T10:02:00Z

_Resumes session `en-wait`._

**Customer:** 475398 or maybe [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "customer_entered": "475398 or maybe 364287", "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call confirm_verification_code again when they are ready, without sending a new one"}`

**Assistant:** I got two possible codes there, so neither was checked - I can't guess between them.

Please type just the single 6-digit code from the text message sent to ···0133 into this chat. That code stays valid until about 10:05 UTC, so there's no need for a new one yet.

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({"entered": "[REDACTED ONE-TIME CODE]"})` → `{"verified": true, "valid_for_minutes": 15, "customer_entered": "[REDACTED ONE-TIME CODE]", "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-12T10:04:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Code confirmed - your contact channel is now set to **email**. That's where Kestrel will send you things like dispute follow-ups. Anything else I can help with?

_Episode written:_ Conversation on 2026-11-12: Customer asked to change their contact channel to email. Identity was verified; a text verification code was sent and confirmed after initial ambiguity. Contact channel was stored as email. The assistant said the code stayed valid until about 10:05 UTC. No case or transaction ID was given. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | two numbers in one message are not checked, either of them: still no failed attempt | `1 attempt rows with succeeded=0` |
| PASS | semantic | then the code alone is accepted | `{"value": "email", "as_of": "2026-11-12T10:04:00Z", "expires_at": null}` |
| PASS | guard | none of it is stored | `store files holding a sent code: []` |
