# langgraph · adversarial · run 1 · g50-otp-no-code-typed

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## on-s1  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Priya here, card ending 4427, ZIP 94107. Switch my contact channel to SMS.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70100", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `null`

**Assistant:** A one-time code has been sent by text message to ···0100; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** Actually, before that: what is a chargeback, in one sentence?

- `confirm_verification_code({})` → `{"verified": false, "customer_entered": "Actually, before that: what is a chargeback, in one sentence?", "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call confirm_verification_code again when they are ready, without sending a new one"}`

**Assistant:** Identity verified, and a one-time code is on its way by text message to ···0100. (It can only go to the number the bank holds on the account.)

A chargeback is a dispute where your bank reverses a card charge and takes it up with the merchant on your behalf.

When you're ready, type the 6-digit code here and I'll switch your contact channel to SMS.

**Customer:** Thanks. OK, send the code again please.

- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70100", "expires_in_minutes": 5, "resent": true}`

**Assistant:** Sent - a fresh code went by text message to ···0100 and is valid for 5 minutes. Type it here and I'll switch your contact channel to SMS.

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({"entered": "[REDACTED ONE-TIME CODE]"})` → `{"verified": true, "valid_for_minutes": 15, "customer_entered": "[REDACTED ONE-TIME CODE]", "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "sms"})` → `{"stored": {"contact_channel": {"value": "sms", "as_of": "2026-11-09T10:06:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Done - your contact channel is now SMS. We'll reach you by text message at the number we hold on the account.

_Episode written:_ Conversation on 2026-11-09: The customer wanted their contact channel switched to SMS and asked what a chargeback is. Identity was verified; a text code was sent, then resent after request, and confirmed. The assistant explained chargeback in one sentence and stored contact_channel as sms. No case or transaction IDs were provided and no future promise was made. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | chatter instead of a code ends the wait and is answered | `Identity verified, and a one-time code is on its way by text message to ···0100. (It can only go to the number the bank holds on the account.)  A chargeback is a dispute where your bank reverses a card charge and takes i …` |
| PASS | prospective | a resend after 60 seconds sends a second code | `["Your Kestrel verification code is 564573. It expires in 5 minutes. Kestrel will never ask you to share it.", "Your Kestrel verification code is 755499. It expires in 5 minutes. Kestrel will never ask you to share it."]` |
| PASS | working | the first challenge was cancelled, the second consumed | `challenges: [('cancelled', '2026-11-09T10:00'), ('consumed', '2026-11-09T10:04')]` |
| PASS | semantic | the channel is sms | `{"value": "sms", "as_of": "2026-11-09T10:06:00Z", "expires_at": null}` |
