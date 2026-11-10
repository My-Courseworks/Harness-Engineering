# adk · adversarial · run 2 · g50-otp-no-code-typed

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## on-s1  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Priya here, card ending 4427, ZIP 94107. Switch my contact channel to SMS.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70100", "expires_in_minutes": 5, "resent": false}`

**Assistant:** I've verified you. A one-time code is on its way by text message to ···0100 - that's the number the bank holds on the account, and it can't be sent anywhere else. Please type the 6-digit code here to confirm the switch to SMS.

**Customer:** Actually, before that: what is a chargeback, in one sentence?

**Assistant:** A chargeback is a reversal of a card payment, where the card issuer takes the money back from the merchant's bank and credits it to you, typically after you dispute a charge for reasons like a cancelled subscription, a duplicate, or goods never received.

The code sent to ···0100 is still valid for a few more minutes - just type it here whenever you're ready and I'll switch your contact channel to SMS.

**Customer:** Thanks. OK, send the code again please.

- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70100", "expires_in_minutes": 5, "resent": true}`

**Assistant:** Sent again - a new code went by text message to ···0100. Please type the 6-digit code here and I'll complete the switch to SMS.

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({"entered": "[REDACTED ONE-TIME CODE]"})` → `{"verified": true, "valid_for_minutes": 15, "customer_entered": "[REDACTED ONE-TIME CODE]", "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "sms"})` → `{"stored": {"contact_channel": {"value": "sms", "as_of": "2026-11-09T10:06:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Done - your contact channel is now set to SMS. Anything else?

_Episode written:_ Conversation on 2026-11-09: Priya asked to switch her contact channel to SMS. Identity was verified, a one-time code was sent and resent to the bank-held number, then confirmed; the contact channel was stored as SMS on 2026-11-09. She also asked what a chargeback is and received a one-sentence explanation. No case/transaction IDs or promises were recorded. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | chatter instead of a code ends the wait and is answered | `A chargeback is a reversal of a card payment, where the card issuer takes the money back from the merchant's bank and credits it to you, typically after you dispute a charge for reasons like a cancelled subscription, a d …` |
| PASS | prospective | a resend after 60 seconds sends a second code | `["Your Kestrel verification code is 352439. It expires in 5 minutes. Kestrel will never ask you to share it.", "Your Kestrel verification code is 273973. It expires in 5 minutes. Kestrel will never ask you to share it."]` |
| PASS | working | the first challenge was cancelled, the second consumed | `challenges: [('cancelled', '2026-11-09T10:00'), ('consumed', '2026-11-09T10:04')]` |
| PASS | semantic | the channel is sms | `{"value": "sms", "as_of": "2026-11-09T10:06:00Z", "expires_at": null}` |
