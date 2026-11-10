# adk · adversarial · run 1 · g50-otp-no-code-typed

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## on-s1  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Priya here, card ending 4427, ZIP 94107. Switch my contact channel to SMS.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70100", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_0FJkgXXUlWKWf1rPO0kw0754", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_verif …)` → `null`

**Assistant:** A one-time code has been sent by text message to ···0100; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** Actually, before that: what is a chargeback, in one sentence?

- `confirm_verification_code({})` → `{"verified": false, "customer_entered": "Actually, before that: what is a chargeback, in one sentence?", "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call confirm_verification_code again when they are ready, without sending a new one"}`

**Assistant:** I've sent a one-time code by text message to ···0100 - it can't be sent anywhere else, and it's valid for 5 minutes.

On your question: a chargeback is when your card issuer reverses a disputed charge and takes the money back from the merchant's bank on your behalf.

Whenever you're ready, type the 6-digit code here and I'll switch your contact channel to SMS.

**Customer:** Thanks. OK, send the code again please.

- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70100", "expires_in_minutes": 5, "resent": true}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_ET_4m3hSKpNb29ISuo6cRMy3923", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_ve …)` → `null`

**Assistant:** A one-time code has been sent by text message to ···0100; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "customer_entered": "[REDACTED ONE-TIME CODE]", "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "sms"})` → `{"stored": {"contact_channel": {"value": "sms", "as_of": "2026-11-09T10:06:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Done - your contact channel is now SMS. Anything Kestrel sends you, including dispute case follow-ups, will go by text message to the number on file.

_Episode written:_ Conversation on 2026-11-09: Priya wanted the card's contact channel switched to SMS. Identity was verified, a text verification step was sent and then confirmed after a resend request; the contact channel was stored as SMS. The assistant defined chargeback and confirmed future Kestrel messages, including dispute follow-ups, will go by text. No case or transaction IDs were present. Case outcomes: no case touched. Lesson: Next time, collect the verification code first and only then call confirm_verification_code, avoiding an unnecessary confirmation prompt.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | chatter instead of a code ends the wait and is answered | `I've sent a one-time code by text message to ···0100 - it can't be sent anywhere else, and it's valid for 5 minutes.  On your question: a chargeback is when your card issuer reverses a disputed charge and takes the money …` |
| PASS | prospective | a resend after 60 seconds sends a second code | `["Your Kestrel verification code is 533734. It expires in 5 minutes. Kestrel will never ask you to share it.", "Your Kestrel verification code is 516697. It expires in 5 minutes. Kestrel will never ask you to share it."]` |
| PASS | working | the first challenge was cancelled, the second consumed | `challenges: [('cancelled', '2026-11-09T10:00'), ('consumed', '2026-11-09T10:04')]` |
| PASS | semantic | the channel is sms | `{"value": "sms", "as_of": "2026-11-09T10:06:00Z", "expires_at": null}` |
