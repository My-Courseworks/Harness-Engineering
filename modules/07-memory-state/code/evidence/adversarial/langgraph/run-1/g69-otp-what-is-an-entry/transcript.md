# langgraph · adversarial · run 1 · g69-otp-what-is-an-entry

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## en-s1  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Priya here, card ending 4427, ZIP 94107. Switch my contact channel to email.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70100", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `null`

**Assistant:** A one-time code has been sent by text message to ···0100; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** It hasn't arrived. Is it going to the number ending 0100? I'm in 94

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "It hasn't arrived. Is it going to the number ending 0100? I'm in 94", "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call confirm_verification_code again when they are ready, without sending a new one"}`

**Assistant:** Yes - the code went by text message to the number ending ···0100, the one the bank holds on the account; it can't be sent anywhere else. It stays usable for about 5 minutes. Type it here when it arrives and I'll complete the switch to email. If it doesn't come through, say so and I can send a new one (the bank allows a resend after 60 seconds).

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-09T10:04:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Done - your contact channel is now email. Anything Kestrel sends you, including dispute follow-ups, will go to your email address on file.

_Episode written:_ Conversation on 2026-11-09: Priya wanted contact channel switched to email. Identity was verified; a code was texted to phone ending 0100. Customer said it hadn't arrived (not verified) and asked if it went there. Assistant said it lasts 5 minutes and resend after 60 seconds. After confirmation, email was stored; all Kestrel messages, including dispute follow-ups, promised to email. No case/transaction IDs provided. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | a message whose digits happen to total six is not a guess: no failed attempt | `0 attempt rows with succeeded=0` |
| PASS | semantic | the code typed after it is accepted | `{"value": "email", "as_of": "2026-11-09T10:04:00Z", "expires_at": null}` |

## en-other-chat  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

_Resumes session `en-wait`._

**Customer:** Marco, card ending 8830, ZIP 10011. Change my contact channel to email.

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70133", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `null`

**Assistant:** A one-time code has been sent by text message to ···0133; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

## en-other-chat-2  ·  session  ·  marco  ·  2026-11-12T10:01:00Z

_Resumes session `en-elsewhere`._

**Customer:** Different question while I wait: is [REDACTED ONE-TIME CODE] one of your reference numbers?

- `confirm_verification_code({})` → `{"verified": false, "note": "a code is open for this customer, but it was sent from another conversation: a six-digit number typed here is removed and not checked. To verify in this conversation, send a new code (send_verification_code)"}`

**Assistant:** No - my reference numbers look like **T-1002** for a transaction or **C-5001** for a case, not six digits. Also, that number was removed before your message reached me, so I don't see it at all.

On verification: the code open on your account was sent from a different conversation of yours, so digits typed here aren't checked against it. If you want to go ahead with the contact-channel change, I can send a fresh code to ···0133 (text) - want me to?

_Episode written:_ Conversation on 2026-11-12: The customer asked if a six-digit one-time code was a reference number (not verified) and awaited a contact-channel change. The assistant said reference numbers are like [a transaction not on this account]/[a case not on this account], not six digits, explained the code was removed and came from another conversation, and offered a fresh text code to ···0133. No actual case/transaction IDs or preference stated. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | six digits typed in another conversation are not checked against the code: no attempt | `0 attempt rows with succeeded=0` |
| PASS | working | the code stays open for the conversation that asked for it | `challenges: [('open', '2026-11-12T10:00')]` |

## en-back  ·  session  ·  marco  ·  2026-11-12T10:02:00Z

_Resumes session `en-wait`._

**Customer:** [REDACTED ONE-TIME CODE] or maybe [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "[REDACTED ONE-TIME CODE] or maybe [REDACTED ONE-TIME CODE]", "note": "the message held more than one six-digit number: none was checked and nothing was counted. Ask the customer to type only the code, as their whole message"}`

**Assistant:** Thanks - identity verified, and I've sent a one-time code by text message to ···0133 (it can only go to the number the bank holds on your account).

Your last message contained more than one six-digit number, so the code wasn't checked. Please reply with just the code on its own, as your whole message, and I'll apply the change to email.

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-12T10:04:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** The code checked out - your contact channel is now set to email. Case follow-ups and other bank messages will go there.

_Episode written:_ Conversation on 2026-11-12: Customer wanted contact channel changed to email. Identity was verified, a one-time code was sent by text and confirmed after an initial submission containing multiple numbers; the contact channel was then stored as email (as of 2026-11-12T10:04:00Z). The assistant promised case follow-ups and other bank messages would go there. No case or transaction IDs were provided. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | two numbers in one message are not checked, either of them: still no failed attempt | `0 attempt rows with succeeded=0` |
| PASS | semantic | then the code alone is accepted | `{"value": "email", "as_of": "2026-11-12T10:04:00Z", "expires_at": null}` |
| PASS | guard | none of it is stored | `store files holding a sent code: []` |
