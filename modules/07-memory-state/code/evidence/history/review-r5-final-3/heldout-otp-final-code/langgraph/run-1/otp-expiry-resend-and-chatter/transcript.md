# langgraph · heldout-otp · run 1 · otp-expiry-resend-and-chatter

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ox-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Dana, card ending 5127, ZIP 60614. Please switch my contact channel to SMS.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "email to d\u00b7\u00b7\u00b7@example.com", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `null`

**Assistant:** A one-time code has been sent by email to d···@example.com; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | otp: one code sent | `["Your Kestrel verification code is 270742. It expires in 5 minutes. Kestrel will never ask you to share it."]` |
| PASS | external | otp: one challenge open | `challenges: [('open', '2026-11-13T10:00')]` |
| PASS | semantic | otp: no change yet | `null` |

## ox-s1-expired  ·  session  ·  dana  ·  2026-11-13T10:06:00Z

_Resumes session `ox-s1`._

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "error": "the code expired (5 minutes) and no new code has been sent; tell the customer and send a new one only if they ask (send_verification_code)", "customer_entered": "[REDACTED ONE-TIME CODE]"}`

**Assistant:** Your identity check passed, but the one-time code has expired, so the SMS switch isn't done yet. Would you like me to send a new code?

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | otp: a code typed after five minutes does not change the channel | `null` |
| PASS | external | otp: the expired challenge is not consumed | `challenges: [('expired', '2026-11-13T10:00')]` |
| PASS | external | otp: and it is no longer open | `challenges: [('expired', '2026-11-13T10:00')]` |
| PASS | external | otp: no new code is sent on its own | `["Your Kestrel verification code is 270742. It expires in 5 minutes. Kestrel will never ask you to share it."]` |
| PASS | guard | otp: the code is in no tool result or reply | `codes seen by the model (tool results or replies): []` |

## ox-s1-fresh  ·  session  ·  dana  ·  2026-11-13T10:08:00Z

_Resumes session `ox-s1`._

**Customer:** Yes, please send a fresh one.

- `send_verification_code({})` → `{"sent": true, "sent_to": "email to d\u00b7\u00b7\u00b7@example.com", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `null`

**Assistant:** A one-time code has been sent by email to d···@example.com; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** One thing before I type it: if I switch to SMS, do dispute follow-ups come by text too?

- `confirm_verification_code({})` → `{"verified": false, "customer_entered": "One thing before I type it: if I switch to SMS, do dispute follow-ups come by text too?", "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call confirm_verification_code again when they are ready, without sending a new one"}`
- `search_policy({"question": "where dispute follow-ups are sent, contact channel SMS"})` → `{"documents": [{"document": "contact-preferences", "score": 0.684, "text": "# Contact preferences\n\nKestrel can contact you about cases and reminders by **email**, **sms** (text message), or **secure_message** (the inbox in the Kestrel app). If you have not chosen a channel, Kestrel uses secure_message. Changing your contact channel requires identity verification, because a changed channel is a c …`

**Assistant:** Yes - dispute follow-ups and reminders go to whatever channel you've chosen, so once SMS is set they'd come by text. (With no channel chosen, they go by secure message in the app.)

The code is still valid for a couple more minutes - type it whenever you're ready and I'll finish the switch.

**Customer:** Thanks. Here it is: [REDACTED ONE-TIME CODE]

- `confirm_verification_code({"entered": "[REDACTED ONE-TIME CODE]"})` → `{"verified": true, "valid_for_minutes": 15, "customer_entered": "[REDACTED ONE-TIME CODE]", "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "sms"})` → `{"stored": {"contact_channel": {"value": "sms", "as_of": "2026-11-13T10:12:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Done - your contact channel is now set to SMS, so case follow-ups and reminders will reach you by text.

_Episode written:_ Conversation on 2026-11-13: The customer said she was Dana (not verified). She wanted contact channel switched to SMS and asked whether dispute follow-ups would arrive by text. Identity was verified; after one expired code and a resend, verification succeeded and the channel was stored as SMS as of 2026-11-13T10:12:00Z. Assistant confirmed dispute follow-ups/reminders go to chosen channel. No case/transaction IDs. Case outcomes: no case touched. Lesson: Next time, wait for the customer to supply the one-time code before calling confirm_verification_code; if they ask a question instead, answer it and avoid unnecessary resend attempts while the current code remains valid.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | otp: a second code was sent on request, and only one | `["Your Kestrel verification code is 270742. It expires in 5 minutes. Kestrel will never ask you to share it.", "Your Kestrel verification code is 198487. It expires in 5 minutes. Kestrel will never ask you to share it."]` |
| PASS | semantic | otp: the fresh code, typed after a detour, changes the channel | `{"value": "sms", "as_of": "2026-11-13T10:12:00Z", "expires_at": null}` |
| PASS | external | otp: exactly one challenge consumed | `challenges: [('expired', '2026-11-13T10:00'), ('consumed', '2026-11-13T10:08')]` |
| PASS | external | otp: nothing left open | `challenges: [('expired', '2026-11-13T10:00'), ('consumed', '2026-11-13T10:08')]` |
| PASS | guard | otp: no code in a tool result or reply | `codes seen by the model (tool results or replies): []` |
