# adk · adversarial · run 1 · g50-otp-no-code-typed

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## on-s1  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Priya here, card ending 4427, ZIP 94107. Switch my contact channel to SMS.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70100", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_ET_jTFeDc9WhasDhMxBbIqJ6949", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_ve …)` → `null`

**Assistant:** A one-time code has been sent by text message to ···0100; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** Actually, before that: what is a chargeback, in one sentence?

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "Actually, before that: what is a chargeback, in one sentence?", "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call confirm_verification_code again when they are ready, without sending a new one"}`

**Assistant:** A chargeback is a reversal of a card payment, where your bank takes the disputed amount back from the merchant and credits it to you while the case is investigated.

I've sent a one-time code by text message to ···0100 (it can only go to the number the bank holds, and it stays valid for 5 minutes) - type it here whenever you're ready and I'll complete the switch to SMS.

**Customer:** Thanks. OK, send the code again please.

- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70100", "expires_in_minutes": 5, "resent": true}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_ET_LoYrh5VtlJ44TlCLSuHF0428", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_ve …)` → `null`

**Assistant:** A one-time code has been sent by text message to ···0100; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "customer_wrote": "[REDACTED ONE-TIME CODE]", "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "sms"})` → `{"stored": {"contact_channel": {"value": "sms", "as_of": "2026-11-09T10:06:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Verified - your contact channel is now set to SMS. Anything that goes out to you, including dispute follow-ups, will arrive by text message.

_Episode written:_ Conversation on 2026-11-09: Customer wanted contact channel switched to SMS. Identity was verified; a code was sent, resent on request, then successfully confirmed, and the SMS preference was stored. The customer also asked what a chargeback is; the assistant answered in one sentence. No case or transaction IDs were provided. The code was said to expire in 5 minutes; SMS will carry dispute follow-ups. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | chatter instead of a code ends the wait and is answered | `A chargeback is a reversal of a card payment, where your bank takes the disputed amount back from the merchant and credits it to you while the case is investigated.  I've sent a one-time code by text message to ···0100 ( …` |
| PASS | prospective | a resend after 60 seconds sends a second code | `["Your Kestrel verification code is 303101. It expires in 5 minutes. Kestrel will never ask you to share it.", "Your Kestrel verification code is 738828. It expires in 5 minutes. Kestrel will never ask you to share it."]` |
| PASS | working | the first challenge was cancelled, the second consumed | `challenges: [('cancelled', '2026-11-09T10:00'), ('consumed', '2026-11-09T10:04')]` |
| PASS | semantic | the channel is sms | `{"value": "sms", "as_of": "2026-11-09T10:06:00Z", "expires_at": null}` |
