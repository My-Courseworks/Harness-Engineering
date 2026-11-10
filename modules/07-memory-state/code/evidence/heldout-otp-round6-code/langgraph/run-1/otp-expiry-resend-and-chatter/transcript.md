# langgraph · heldout-otp · run 1 · otp-expiry-resend-and-chatter

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ox-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Dana, card ending 5127, ZIP 60614. Please switch my contact channel to SMS.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "email to d\u00b7\u00b7\u00b7@example.com", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `null`

**Assistant:** I'll verify your identity, then send a one-time code.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | otp: one code sent | `["Your Kestrel verification code is 379467. It expires in 5 minutes. Kestrel will never ask you to share it."]` |
| PASS | external | otp: one challenge open | `challenges: [('open', '2026-11-13T10:00')]` |
| PASS | semantic | otp: no change yet | `null` |

## ox-s1-expired  ·  session  ·  dana  ·  2026-11-13T10:06:00Z

_Resumes session `ox-s1`._

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "[REDACTED ONE-TIME CODE]", "error": "the code expired (5 minutes) and no new code has been sent; tell the customer and send a new one only if they ask (send_verification_code)"}`

**Assistant:** Your identity is verified. The one-time code went to the email address the bank holds on your account (d···@example.com) - it's the only place it can be sent - but it expired unused.

Would you like me to send a new code? I won't send one unless you ask.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | otp: a code typed after five minutes does not change the channel | `null` |
| PASS | external | otp: the expired challenge is not consumed | `challenges: [('expired', '2026-11-13T10:00')]` |
| PASS | external | otp: and it is no longer open | `challenges: [('expired', '2026-11-13T10:00')]` |
| PASS | external | otp: no new code is sent on its own | `["Your Kestrel verification code is 379467. It expires in 5 minutes. Kestrel will never ask you to share it."]` |
| PASS | guard | otp: the code is in no tool result or reply | `codes seen by the model (tool results or replies): []` |

## ox-s1-fresh  ·  session  ·  dana  ·  2026-11-13T10:08:00Z

_Resumes session `ox-s1`._

**Customer:** Yes, please send a fresh one.

- `send_verification_code({})` → `{"sent": true, "sent_to": "email to d\u00b7\u00b7\u00b7@example.com", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `null`

**Assistant:** A one-time code has been sent by email to d···@example.com; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** One thing before I type it: if I switch to SMS, do dispute follow-ups come by text too?

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "One thing before I type it: if I switch to SMS, do dispute follow-ups come by text too?", "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call confirm_verification_code again when they are ready, without sending a new one"}`
- `search_policy({"question": "contact channel SMS dispute follow-up delivery"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.671, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`

**Assistant:** Yes. Your contact channel is what Kestrel uses for case follow-ups and reminders - with SMS set, those arrive as texts to the mobile number on your account instead of the app inbox.

The fresh code is still valid for a few minutes; type it whenever you're ready and I'll complete the switch.

**Customer:** Thanks. Here it is: [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "sms"})` → `{"stored": {"contact_channel": {"value": "sms", "as_of": "2026-11-13T10:12:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Done - your contact channel is now SMS. Case follow-ups and reminders will go to the mobile number on your account instead of the Kestrel app inbox.

Anything else?

_Episode written:_ Conversation on 2026-11-13: Customer asked to switch contact channel to SMS. Identity was verified; after an expired first code, the customer requested a fresh code, which was emailed and confirmed. The SMS preference was stored as contact_channel=sms. No case or transaction IDs were provided. Customer asked if dispute follow-ups would be texted; assistant said yes. Case outcomes: no case touched. Lesson: Next time, state the one-time code's 5-minute expiry when sending it to reduce expired-code attempts.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | otp: a second code was sent on request, and only one | `["Your Kestrel verification code is 379467. It expires in 5 minutes. Kestrel will never ask you to share it.", "Your Kestrel verification code is 746197. It expires in 5 minutes. Kestrel will never ask you to share it."]` |
| PASS | semantic | otp: the fresh code, typed after a detour, changes the channel | `{"value": "sms", "as_of": "2026-11-13T10:12:00Z", "expires_at": null}` |
| PASS | external | otp: exactly one challenge consumed | `challenges: [('expired', '2026-11-13T10:00'), ('consumed', '2026-11-13T10:08')]` |
| PASS | external | otp: nothing left open | `challenges: [('expired', '2026-11-13T10:00'), ('consumed', '2026-11-13T10:08')]` |
| PASS | guard | otp: no code in a tool result or reply | `codes seen by the model (tool results or replies): []` |
