# adk · heldout-otp · run 1 · otp-expiry-resend-and-chatter

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ox-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Dana, card ending 5127, ZIP 60614. Please switch my contact channel to SMS.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "email to d\u00b7\u00b7\u00b7@example.com", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_ET_8Wv7aFBkMzbEsnDodlGB8225", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_ve …)` → `null`

**Assistant:** A one-time code has been sent by email to d···@example.com; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | otp: one code sent | `["Your Kestrel verification code is 559235. It expires in 5 minutes. Kestrel will never ask you to share it."]` |
| PASS | external | otp: one challenge open | `challenges: [('open', '2026-11-13T10:00')]` |
| PASS | semantic | otp: no change yet | `null` |

## ox-s1-expired  ·  session  ·  dana  ·  2026-11-13T10:06:00Z

_Resumes session `ox-s1`._

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "[REDACTED ONE-TIME CODE]", "error": "the code expired (5 minutes) and no new code has been sent; tell the customer and send a new one only if they ask (send_verification_code)"}`

**Assistant:** Your identity is verified. I sent a one-time code to the email the bank holds on the account (d···@example.com) - it can't be sent anywhere else. That code has now expired unused. Would you like me to send a new one so we can complete the switch to SMS?

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | otp: a code typed after five minutes does not change the channel | `null` |
| PASS | external | otp: the expired challenge is not consumed | `challenges: [('expired', '2026-11-13T10:00')]` |
| PASS | external | otp: and it is no longer open | `challenges: [('expired', '2026-11-13T10:00')]` |
| PASS | external | otp: no new code is sent on its own | `["Your Kestrel verification code is 559235. It expires in 5 minutes. Kestrel will never ask you to share it."]` |
| PASS | guard | otp: the code is in no tool result or reply | `codes seen by the model (tool results or replies): []` |

## ox-s1-fresh  ·  session  ·  dana  ·  2026-11-13T10:08:00Z

_Resumes session `ox-s1`._

**Customer:** Yes, please send a fresh one.

- `send_verification_code({})` → `{"sent": true, "sent_to": "email to d\u00b7\u00b7\u00b7@example.com", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_ET_yjXLCQdJ7wBFYcDZhEMG7945", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_ve …)` → `null`

**Assistant:** A one-time code has been sent by email to d···@example.com; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** One thing before I type it: if I switch to SMS, do dispute follow-ups come by text too?

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "One thing before I type it: if I switch to SMS, do dispute follow-ups come by text too?", "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call confirm_verification_code again when they are ready, without sending a new one"}`
- `search_policy({"question": "does contact channel (SMS) apply to dispute follow-ups delivery"})` → `{"documents": [{"document": "contact-preferences", "score": 0.701, "text": "# Contact preferences\n\nKestrel can contact you about cases and reminders by **email**, **sms** (text message), or **secure_message** (the inbox in the Kestrel app). If you have not chosen a channel, Kestrel uses secure_message. Changing your contact channel requires identity verification, because a changed channel is a c …`

**Assistant:** Yes - Kestrel contacts you about cases and reminders by whichever channel you've chosen: email, SMS, or the secure message inbox in the app. So once your channel is SMS, dispute follow-ups would come to you as texts.

Your code is still valid for a few more minutes - just type it when you're ready and we'll finish the switch.

**Customer:** Thanks. Here it is: [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "sms"})` → `{"stored": {"contact_channel": {"value": "sms", "as_of": "2026-11-13T10:12:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Done - your contact channel is now SMS. Kestrel will reach you about cases and reminders by text from here on. Anything else I can help with?

_Episode written:_ Conversation on 2026-11-13: Dana asked to switch contact channel to SMS and whether dispute follow-ups would come by text. After identity verification and an initial expired verification attempt, resent on request, assistant confirmed case/reminder contact follows the chosen channel and completed the switch, storing contact_channel=sms at 2026-11-13T10:12:00Z. No case or transaction IDs were provided. Customer preference: SMS. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | otp: a second code was sent on request, and only one | `["Your Kestrel verification code is 559235. It expires in 5 minutes. Kestrel will never ask you to share it.", "Your Kestrel verification code is 345341. It expires in 5 minutes. Kestrel will never ask you to share it."]` |
| PASS | semantic | otp: the fresh code, typed after a detour, changes the channel | `{"value": "sms", "as_of": "2026-11-13T10:12:00Z", "expires_at": null}` |
| PASS | external | otp: exactly one challenge consumed | `challenges: [('expired', '2026-11-13T10:00'), ('consumed', '2026-11-13T10:08')]` |
| PASS | external | otp: nothing left open | `challenges: [('expired', '2026-11-13T10:00'), ('consumed', '2026-11-13T10:08')]` |
| PASS | guard | otp: no code in a tool result or reply | `codes seen by the model (tool results or replies): []` |
