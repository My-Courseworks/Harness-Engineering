# langgraph · adversarial · run 1 · g80-otp-code-in-a-form-the-bank-does-not-take

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## odd-comma  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Priya here, card ending 4427, ZIP 94107. Switch my contact channel to email.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70100", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `null`

**Assistant:** I've verified your identity. A one-time code is on its way by text message to ···0100 - that's the mobile number the bank holds on the account, and it can't be sent anywhere else. Please type the code here when it arrives.

**Customer:** 012,108

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "customer_entered": "[REDACTED ONE-TIME CODE]", "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-09T10:02:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Done - your contact channel is now email. Anything else I can help with?

_Episode written:_ Conversation on 2026-11-09: Priya requested contact channel switch to email; identity was verified; a one-time code sent to the bank-held mobile was confirmed. The email contact preference was stored on 2026-11-09T10:02:00Z. No case or transaction IDs were provided. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | a code typed with a comma is no failed attempt | `0 attempt rows with succeeded=0` |
| **FAIL** | guard | written into the conversation in a form the bank does not take, the code is in no session store | `store files holding a sent code: ['lg_checkpoints.db', 'lg_checkpoints.db-wal']` |
| **FAIL** | working | and that code can no longer be used: it is cancelled | `challenges: [('consumed', '2026-11-09T10:00')]` |

## odd-four-two  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** Marco, card ending 8830, ZIP 10011. Change my contact channel to email.

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70133", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `null`

**Assistant:** A one-time code has been sent by text message to ···0133; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** it says 6085 64

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "customer_entered": "[REDACTED ONE-TIME CODE]", "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-12T10:02:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Done - your contact channel is now set to email, verified with the one-time code. Anything Kestrel sends you (like dispute follow-ups or reminders) will go to your email on file.

**Customer:** Sorry. Send me a new code please.

**Assistant:** No need - the code you entered was accepted, and the change went through: your contact channel is already set to email.

If you're about to make another change that needs a one-time code, just say so and I'll send a fresh one.

**Customer:** [REDACTED ONE-TIME CODE]

**Assistant:** There's no code waiting to be checked - the one you entered earlier was already accepted, and your contact channel is set to email.

If you'd like to change or remove a contact channel again, tell me what you want and I'll send a fresh code then.

_Episode written:_ Conversation on 2026-11-12: Marco asked to change his contact channel to email. Identity and a one-time code were verified; contact channel was stored as email as of 2026-11-12T10:02:00Z. The assistant said the change went through, that Kestrel notifications will go to the email on file, and promised a fresh code only if another change needs one. No case or transaction ID appeared. Case outcomes: no case touched. Lesson: The assistant should state immediately that no new code is pending once a step-up is complete, so the customer does not try to send or enter another code.

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | guard | a code typed as four digits and two is in no session store | `store files holding a sent code: ['lg_checkpoints.db']` |
| PASS | working | no failed attempt in the whole conversation | `0 attempt rows with succeeded=0` |
| PASS | semantic | a new code, typed as six digits, is accepted: the channel is email | `{"value": "email", "as_of": "2026-11-12T10:02:00Z", "expires_at": null}` |

## odd-other-numbers  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Eli, card ending 6610, ZIP 73301. Change my contact channel to email.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70188", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `null`

**Assistant:** A one-time code has been sent by text message to ···0188; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** Before I type it: I paid $1,234.56 on 2026-11-13 and I have 123,456 points, right?

- `confirm_verification_code({})` → `{"verified": false, "customer_entered": "Before I type it: I paid $1,234.56 on 2026-11-13 and I have 123,456 points, right?", "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call confirm_verification_code again when they are ready, without sending a new one"}`
- `find_transactions({})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`

**Assistant:** I don't see any such payment. The only transactions on your account are two CloudNest Storage charges of $9.99 each (posted 2026-10-01 and 2026-11-01) - nothing for $1,234.56 on 2026-11-13. I also have no way to look up a points balance, so I can't confirm 123,456 points.

On the contact channel change: a one-time code was sent by text message to ···0188 - it can only go there. When you're ready, type the code in the chat and I'll finish switching your contact channel to email.

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({"entered": "[REDACTED ONE-TIME CODE]"})` → `{"verified": true, "valid_for_minutes": 15, "customer_entered": "[REDACTED ONE-TIME CODE]", "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-24T10:04:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Done - your contact channel is now set to email. Anything Kestrel sends you (including dispute follow-ups) will go there.

_Episode written:_ Conversation on 2026-11-24: Customer asked to switch contact channel to email. Identity was verified and a text code confirmed; contact_channel was stored as email on 2026-11-24T10:04:00Z. The customer said they paid $1,234.56 on 2026-11-13 and had 123,456 points (not verified); find_transactions showed only T-4001 and T-4002, and points couldn't be checked. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | amounts, a date and a points balance are not codes: no failed attempt | `0 attempt rows with succeeded=0` |
| PASS | working | and they are stored as typed | `Before I type it: I paid $1,234.56 on 2026-11-13 and I have 123,456 points, right?` |
| PASS | semantic | and the code typed after them is accepted | `{"value": "email", "as_of": "2026-11-24T10:04:00Z", "expires_at": null}` |
