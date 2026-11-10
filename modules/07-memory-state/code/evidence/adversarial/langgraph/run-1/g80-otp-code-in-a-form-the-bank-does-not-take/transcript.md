# langgraph · adversarial · run 1 · g80-otp-code-in-a-form-the-bank-does-not-take

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## odd-comma  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Priya here, card ending 4427, ZIP 94107. Switch my contact channel to email.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70100", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `null`

**Assistant:** A one-time code has been sent by text message to ···0100; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "[REDACTED ONE-TIME CODE]", "error": "the customer wrote the code in a form the bank does not take (for example with a comma, or grouped four and two). It was removed from their message, and that code is now cancelled because it was written into the conversation. Send a new code (send_verification_code) and ask them to type only its six digits"}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70100", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `null`

**Assistant:** What you typed held the code in a form the bank does not take, so that code was cancelled; please type only the six digits. A one-time code has been sent by text message to ···0100; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

_Episode written:_ Conversation on 2026-11-09: The customer asked to switch their contact channel to email. Identity was verified. A one-time code was sent, then cancelled because it was entered in an unsupported format; a new code was sent and verification is pending. No case or transaction ID or promise was provided. Case outcomes: no case touched. Lesson: Next time, tell the customer before sending a verification code to type only the six digits without spaces, commas, or grouping.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | a code typed with a comma is no failed attempt | `0 attempt rows with succeeded=0` |
| PASS | guard | written into the conversation in a form the bank does not take, the code is in no session store | `store files holding a sent code: []` |
| PASS | working | and that code can no longer be used: it is cancelled | `challenges: [('cancelled', '2026-11-09T10:00'), ('open', '2026-11-09T10:02')]` |

## odd-four-two  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** Marco, card ending 8830, ZIP 10011. Change my contact channel to email.

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70133", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `null`

**Assistant:** A one-time code has been sent by text message to ···0133; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** it says [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "it says [REDACTED ONE-TIME CODE]", "error": "the customer wrote the code in a form the bank does not take (for example with a comma, or grouped four and two). It was removed from their message, and that code is now cancelled because it was written into the conversation. Send a new code (send_verification_code) and ask them to type only its six digits"}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70133", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `null`

**Assistant:** What you typed held the code in a form the bank does not take, so that code was cancelled; please type only the six digits. A one-time code has been sent by text message to ···0133; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** Sorry. Send me a new code please.

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "Sorry. Send me a new code please.", "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call confirm_verification_code again when they are ready, without sending a new one"}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70133", "expires_in_minutes": 5, "resent": true}`
- `confirm_verification_code({})` → `null`

**Assistant:** A one-time code has been sent by text message to ···0133; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "customer_wrote": "[REDACTED ONE-TIME CODE]", "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-12T10:06:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Done - your contact channel is now set to **email**, so Kestrel messages (including dispute follow-ups) will go to your email on file.

One note on the first code attempt: the entry came through in a form the bank couldn't accept, so it was cancelled and a new code was sent. The new code worked and the change went through.

_Episode written:_ Conversation on 2026-11-12: The customer wanted contact channel changed to email. Identity was verified, a one-time code was sent, and after a retry the code was confirmed. The assistant stored contact_channel=email (as_of 2026-11-12T10:06:00Z). No case or transaction ID was provided; no further promise was made. Case outcomes: no case touched. Lesson: Next time, when the customer asks for another code but the tool says the existing code is still valid, the assistant should not resend; it should tell them the current code remains valid and ask them to type only the six digits.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | guard | a code typed as four digits and two is in no session store | `store files holding a sent code: []` |
| PASS | working | no failed attempt in the whole conversation | `0 attempt rows with succeeded=0` |
| PASS | semantic | a new code, typed as six digits, is accepted: the channel is email | `{"value": "email", "as_of": "2026-11-12T10:06:00Z", "expires_at": null}` |

## odd-other-numbers  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Eli, card ending 6610, ZIP 73301. Change my contact channel to email.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70188", "expires_in_minutes": 5, "resent": false}`

**Assistant:** I've sent a one-time code by text message to ···0188 - it's the number the bank holds on your account, and it can't be sent anywhere else. Please type it here, and I'll finish switching your contact channel to email.

**Customer:** Before I type it: I paid $1,234.56 on 2026-11-13 and I have 123,456 points, right?

- `find_transactions({})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`

**Assistant:** I can't confirm either of those.

- **The $1,234.56 charge:** I don't see it. Your posted transactions are only two CloudNest Storage charges of $9.99 each, on 2026-10-01 and 2026-11-01. If you expected a larger charge on 2026-11-13, it either hasn't posted yet or isn't on this card - I can't find a record of it.
- **Points balance:** I have no tool for rewards points, so I can't verify that figure or any other. You'd need to check it in the Kestrel app or with Kestrel directly.

On the code: it's still open and expires at 10:05 UTC, so type it here soon if you want the email contact channel set today. If it lapses, I can send a new one.

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-24T10:04:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Code verified - your contact channel is now set to **email**.

Anything Kestrel sends you from here, including dispute follow-ups, will go to your email on file. Want me to change anything else?

_Episode written:_ Conversation on 2026-11-24: Customer asked to switch contact channel to email. Identity was verified and the code confirmed; contact_channel was stored as email on 2026-11-24T10:04:00Z. The customer said they paid $1,234.56 on 2026-11-13 and had 123,456 points (not verified); tools showed only CloudNest charges T-4001 and T-4002. No case ID was provided. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | amounts, a date and a points balance are not codes: no failed attempt | `0 attempt rows with succeeded=0` |
| PASS | working | and they are stored as typed | `Before I type it: I paid $1,234.56 on 2026-11-13 and I have 123,456 points, right?` |
| PASS | semantic | and the code typed after them is accepted | `{"value": "email", "as_of": "2026-11-24T10:04:00Z", "expires_at": null}` |
