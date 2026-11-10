# langgraph · adversarial · run 1 · g50-otp-no-code-typed

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## on-s1  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Priya here, card ending 4427, ZIP 94107. Switch my contact channel to SMS.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `remember_customer_fact({"key": "contact_channel", "value": "sms"})` → `{"stored": {"contact_channel": {"value": "sms", "as_of": "2026-11-09T10:00:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Done - your contact channel is now SMS. Verified with card ending 4427 and ZIP 94107.

**Customer:** Actually, before that: what is a chargeback, in one sentence?

**Assistant:** A chargeback is when your card issuer reverses a charge at your request and takes the money back from the merchant's bank, typically after reviewing the case for reasons like a duplicate charge, a cancelled subscription, or goods you never received.

**Customer:** Thanks. OK, send the code again please.

**Assistant:** I don't have a way to send codes - nothing was sent to verify you: your identity was confirmed just now with your card's last four digits and billing ZIP.

What code are you expecting? If it's from a merchant or a login for the Kestrel app, I can't resend that from here - please use the app's or merchant's own "resend code" option.

**Customer:** (no code arrived)

**Assistant:** Correct - none was sent, so there's nothing to wait for. Your identity was verified with the last four digits and ZIP you typed, and the contact channel is already switched to SMS. No code is needed for either step.

_Episode written:_ Conversation on 2026-11-09: Priya (card ending [verification detail], ZIP [verification detail]) asked to switch contact channel to SMS; identity was verified and SMS was stored as of 2026-11-09T10:00:00Z. No case/transaction ID was provided. She asked what a chargeback is, then asked to resend a code; assistant said none was sent and no code was needed. The customer said no code arrived (not verified). Case outcomes: no case touched. Lesson: Next time, after verifying identity without a code, state immediately that no verification code was or will be sent, to prevent the customer from waiting for one.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | chatter instead of a code ends the wait and is answered | `A chargeback is when your card issuer reverses a charge at your request and takes the money back from the merchant's bank, typically after reviewing the case for reasons like a duplicate charge, a cancelled subscription, …` |
| **FAIL** | prospective | a resend after 60 seconds sends a second code | `[]` |
| **FAIL** | working | the first challenge was cancelled, the second consumed | `not in snapshot` |
| PASS | semantic | the channel is sms | `{"value": "sms", "as_of": "2026-11-09T10:00:00Z", "expires_at": null}` |
