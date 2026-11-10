# adk · adversarial · run 1 · g80-otp-code-in-a-form-the-bank-does-not-take

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

**This is not a run of the product.** The mutant `only-the-forms-the-bank-takes-are-looked-for` (probes/mutants/mutants.py) put one defect back before the run, to show the check written for it failing.

## odd-comma  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Priya here, card ending 4427, ZIP 94107. Switch my contact channel to email.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70100", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_ET_RjCRq5jGNoP0Kd4uQ3Hw7238", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_ve …)` → `null`

**Assistant:** A one-time code has been sent by text message to ···0100; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** 269,548

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "269,548", "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call confirm_verification_code again when they are ready, without sending a new one"}`

**Assistant:** Thanks, Priya - your identity is confirmed.

I've sent a one-time code by text message to the mobile number ending ···0100. It's valid for 5 minutes and can't be sent anywhere else. What came through last time wasn't a single code, so please type just the 6-digit code on its own in one message, and I'll finish switching your contact channel to email.

_Episode written:_ Conversation on 2026-11-09: The customer asked to switch her contact channel to email. Identity was verified. A one-time code was sent by text to the mobile ending 0100. The customer entered 269,548, which was not accepted as a code; the assistant asked her to type only the 6-digit code and said the email switch would be completed after that confirmation. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | a code typed with a comma is no failed attempt | `0 attempt rows with succeeded=0` |
| **FAIL** | guard | written into the conversation in a form the bank does not take, the code is in no session store | `store files holding a sent code: ['adk_sessions.db']` |
| **FAIL** | working | and that code can no longer be used: it is cancelled | `challenges: [('open', '2026-11-09T10:00')]` |

## odd-four-two  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** Marco, card ending 8830, ZIP 10011. Change my contact channel to email.

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70133", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_ET_QMQCMIPsCsNcjqPKkAzH9411", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_ve …)` → `null`

**Assistant:** A one-time code has been sent by text message to ···0133; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** it says 1180 67

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "it says 1180 67", "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call confirm_verification_code again when they are ready, without sending a new one"}`

**Assistant:** That message isn't the code - it looks like two separate numbers. The code is a single six-digit number in the text message the bank sent to ···0133. When you have it, type just that six-digit code here (no other numbers alongside it) and I'll check it.

**Customer:** Sorry. Send me a new code please.

- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70133", "expires_in_minutes": 5, "resent": true}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_ET_c5p8oGXCFRhniMJDE4Gk6042", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_ve …)` → `null`

**Assistant:** A one-time code has been sent by text message to ···0133; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "customer_wrote": "[REDACTED ONE-TIME CODE]", "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-12T10:06:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Done - your contact channel is now set to email.

_Episode written:_ Conversation on 2026-11-12: The customer asked to change their contact channel to email. Identity was verified via a texted one-time code, after one malformed entry and a successful resend, and the email preference was stored on 2026-11-12T10:06:00Z. No case or transaction IDs were provided; no promises were made. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | guard | a code typed as four digits and two is in no session store | `store files holding a sent code: ['adk_episodes.db', 'adk_sessions.db']` |
| PASS | working | no failed attempt in the whole conversation | `0 attempt rows with succeeded=0` |
| PASS | semantic | a new code, typed as six digits, is accepted: the channel is email | `{"value": "email", "as_of": "2026-11-12T10:06:00Z", "expires_at": null}` |

## odd-other-numbers  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Eli, card ending 6610, ZIP 73301. Change my contact channel to email.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70188", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_ET_p82KZAH4pPjxDmFQtOQy9997", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_ve …)` → `null`

**Assistant:** A one-time code has been sent by text message to ···0188; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** Before I type it: I paid $1,234.56 on 2026-11-13 and I have 123,456 points, right?

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "Before I type it: I paid $1,234.56 on 2026-11-13 and I have 123,456 points, right?", "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call confirm_verification_code again when they are ready, without sending a new one"}`
- `find_transactions({})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`

**Assistant:** I checked rather than going from memory: I don't see a $1,234.56 charge on 2026-11-13 on your card. The only transactions on the account are two CloudNest Storage charges of $9.99 each, posted 2026-10-01 and 2026-11-01. And I have no way to see a points balance - that isn't something my tools cover, so I can't confirm 123,456 points.

On the email change: the one-time code went by text message to ···0188 and is still valid for a few minutes. Type the six-digit code here and I'll finish switching your contact channel to email.

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-24T10:04:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Done - your contact channel is now email. Nothing else changed.

_Episode written:_ Conversation on 2026-11-24: Customer Eli requested contact channel changed to email. Identity was verified via text code to ···0188. The customer said a $1,234.56 charge on 2026-11-13 and 123,456 points (not verified). No case ID. Transactions show only CloudNest $9.99 charges T-4001 (2026-10-01) and T-4002 (2026-11-01); points unavailable. Contact channel was stored as email on 2026-11-24. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | amounts, a date and a points balance are not codes: no failed attempt | `0 attempt rows with succeeded=0` |
| PASS | working | and they are stored as typed | `Before I type it: I paid $1,234.56 on 2026-11-13 and I have 123,456 points, right?` |
| PASS | semantic | and the code typed after them is accepted | `{"value": "email", "as_of": "2026-11-24T10:04:00Z", "expires_at": null}` |
