# adk · adversarial · run 1 · g80-otp-code-in-a-form-the-bank-does-not-take

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## odd-comma  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Priya here, card ending 4427, ZIP 94107. Switch my contact channel to email.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70100", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_ET_KFZp72bzaeTesAWtTsZz9540", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_ve …)` → `null`

**Assistant:** A one-time code has been sent by text message to ···0100; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** 163,298

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "customer_entered": "[REDACTED ONE-TIME CODE]", "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-09T10:02:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Done, Priya - your contact channel is now email (the address Kestrel holds on your account), effective from now. The one-time code went to the text message number ending 0100, and it checked out.

Anything else you'd like to change?

_Episode written:_ Conversation on 2026-11-09: The customer asked to switch her contact channel to email. Identity was verified; a one-time code was sent to the phone ending 0100 and confirmed. The assistant stored contact_channel as email effective from now and told her it was done. No case or transaction IDs appeared. Customer preference: email. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | a code typed with a comma is no failed attempt | `0 attempt rows with succeeded=0` |
| **FAIL** | guard | written into the conversation in a form the bank does not take, the code is in no session store | `store files holding a sent code: ['adk_sessions.db']` |
| **FAIL** | working | and that code can no longer be used: it is cancelled | `challenges: [('consumed', '2026-11-09T10:00')]` |

## odd-four-two  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** Marco, card ending 8830, ZIP 10011. Change my contact channel to email.

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70133", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_7x4iVPxIEDQ3WORWYvaa6655", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_verif …)` → `null`

**Assistant:** I'll verify your identity first.

**Customer:** it says 6391 90

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "customer_entered": "[REDACTED ONE-TIME CODE]", "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-12T10:02:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Done - your contact channel is now set to email. The one-time code went to the mobile number on file (ending ···0133) and checked out, so no further steps are needed. Future card-care messages will reach you by email.

**Customer:** Sorry. Send me a new code please.

**Assistant:** No new code is needed - the code you entered checked out, and your contact channel is already changed to email.

If you're planning another change that needs a code (like changing the channel again or removing it), tell me which one and I'll send a fresh code.

**Customer:** [REDACTED ONE-TIME CODE]

**Assistant:** There's no code pending on my side - the earlier one already checked out and your contact channel is set to email, so nothing is waiting for entry.

If you want to make another change that needs a code, tell me what it is and I'll send a fresh one to the mobile number on file.

_Episode written:_ Conversation on 2026-11-12: Marco (ZIP [verification detail]) asked to change contact channel to email. Identity was verified by one-time code, and contact_channel was stored as email, as of 2026-11-12. No case or transaction IDs were provided. When the customer later asked for a new code, the assistant said none was needed because the change was already complete. Case outcomes: no case touched. Lesson: When a customer asks for another verification code after a completed step-up, clearly confirm the prior request is already finished and ask whether they intend a different change.

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | guard | a code typed as four digits and two is in no session store | `store files holding a sent code: ['adk_sessions.db']` |
| PASS | working | no failed attempt in the whole conversation | `0 attempt rows with succeeded=0` |
| PASS | semantic | a new code, typed as six digits, is accepted: the channel is email | `{"value": "email", "as_of": "2026-11-12T10:02:00Z", "expires_at": null}` |

## odd-other-numbers  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Eli, card ending 6610, ZIP 73301. Change my contact channel to email.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70188", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_iVnnNTGSPkTszvZuFAVa5749", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_verif …)` → `null`

**Assistant:** A one-time code has been sent by text message to ···0188; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** Before I type it: I paid $1,234.56 on 2026-11-13 and I have 123,456 points, right?

- `confirm_verification_code({})` → `{"verified": false, "customer_entered": "Before I type it: I paid $1,234.56 on 2026-11-13 and I have 123,456 points, right?", "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call confirm_verification_code again when they are ready, without sending a new one"}`
- `find_transactions({})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`

**Assistant:** I checked rather than guess, and I can't confirm either figure:

- **Transactions:** I see no $1,234.56 payment on 2026-11-13. The only charges on your account are two CloudNest Storage subscriptions of $9.99 each (2026-10-01 and 2026-11-01).
- **Points:** I have no way to look up a points balance, so I can't confirm 123,456 - please check the app's rewards section.

On the contact-channel change: a one-time code is on its way by **text message to ···0188** (it can only go to the number the bank holds, nowhere else). It's valid for 5 minutes - type it here when you're ready and I'll switch your contact channel to email.

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({"entered": "[REDACTED ONE-TIME CODE]"})` → `{"verified": true, "valid_for_minutes": 15, "customer_entered": "[REDACTED ONE-TIME CODE]", "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-24T10:04:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Done - your contact channel is now **email**. Kestrel will use your email on file for case follow-ups and reminders.

_Episode written:_ Conversation on 2026-11-24: Customer asked to change contact channel to email. Assistant verified identity, sent a one-time code valid 5 minutes, and stored contact_channel email as of 2026-11-24T10:04:00Z. Transactions found were T-4001 and T-4002, $9.99 CloudNest each. The customer said they paid $1,234.56 on 2026-11-13 and have 123,456 points (not verified). Assistant said Kestrel will use email for case follow-ups/reminders. Case outcomes: no case touched. Lesson: Next time, wait for the customer to provide the one-time code before calling confirm_verification_code; if a question intervenes, answer it and reuse the still-valid code.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | amounts, a date and a points balance are not codes: no failed attempt | `0 attempt rows with succeeded=0` |
| PASS | working | and they are stored as typed | `Before I type it: I paid $1,234.56 on 2026-11-13 and I have 123,456 points, right?` |
| PASS | semantic | and the code typed after them is accepted | `{"value": "email", "as_of": "2026-11-24T10:04:00Z", "expires_at": null}` |
