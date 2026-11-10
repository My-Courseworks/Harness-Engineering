# adk · adversarial · run 1 · g50-otp-no-code-typed

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## on-s1  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Priya here, card ending 4427, ZIP 94107. Switch my contact channel to SMS.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `remember_customer_fact({"key": "contact_channel", "value": "sms"})` → `{"stored": {"contact_channel": {"value": "sms", "as_of": "2026-11-09T10:00:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Your contact channel is now set to SMS, Priya. Anything Kestrel sends you - reminders and case follow-ups - will go by text from now on.

**Customer:** Actually, before that: what is a chargeback, in one sentence?

**Assistant:** A chargeback is a process where your card issuer reverses a disputed charge and takes the money back from the merchant's bank, which then has a chance to contest it.

**Customer:** Thanks. OK, send the code again please.

- **error:** `ServiceUnavailableError: litellm.ServiceUnavailableError: ServiceUnavailableError: DeepseekException - {"error":{"message":"Service is too busy. We advise users to temporarily switch to alternative LLM API service providers. (request_id: be059630-a51b-482c-8e82-b335e2f79915)","type":"service_unavailable_error","param":null,"code":"service_unavailable_error"}}`

**Assistant:** (no reply)

**Customer:** (no code arrived)

**Assistant:** I don't have a way to send a code - there's no code-sending tool on my side, and identity checks here are done with your card's last 4 digits and billing ZIP, which you've already given and which verified fine.

If you're waiting on a verification code for the app or a phone login, that comes from Kestrel's systems, not this chat - call the number on the back of your card. What were you trying to do?

_Episode written:_ Conversation on 2026-11-09: Priya asked to switch her contact channel to SMS. Identity verified; the tool stored contact_channel=sms as of 2026-11-09T10:00:00Z. No case/transaction IDs. She then asked what a chargeback is (explained) and said no code arrived (not verified); the assistant said no code-sending tool exists and advised calling the card's number. Preference: SMS contact. Case outcomes: no case touched. Lesson: Next time, clarify early whether the customer needs a code for this chat or for another Kestrel system, since this chat cannot send verification codes.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | chatter instead of a code ends the wait and is answered | `A chargeback is a process where your card issuer reverses a disputed charge and takes the money back from the merchant's bank, which then has a chance to contest it.` |
| **FAIL** | prospective | a resend after 60 seconds sends a second code | `[]` |
| **FAIL** | working | the first challenge was cancelled, the second consumed | `not in snapshot` |
| PASS | semantic | the channel is sms | `{"value": "sms", "as_of": "2026-11-09T10:00:00Z", "expires_at": null}` |
