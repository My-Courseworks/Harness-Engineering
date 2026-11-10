# adk · heldout-otp · run 1 · otp-expiry-resend-and-chatter

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ox-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Dana, card ending 5127, ZIP 60614. Please switch my contact channel to SMS.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "email to d\u00b7\u00b7\u00b7@example.com", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_aZph3q31otrxGnzbJE4g6600", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_verif …)` → `null`

**Assistant:** A one-time code has been sent by email to d···@example.com; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | otp: one code sent | `["Your Kestrel verification code is 881373. It expires in 5 minutes. Kestrel will never ask you to share it."]` |
| PASS | external | otp: one challenge open | `challenges: [('open', '2026-11-13T10:00')]` |
| PASS | semantic | otp: no change yet | `null` |

## ox-s1-expired  ·  session  ·  dana  ·  2026-11-13T10:06:00Z

_Resumes session `ox-s1`._

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "error": "the code expired (5 minutes) and no new code has been sent; tell the customer and send a new one only if they ask (send_verification_code)", "customer_entered": "[REDACTED ONE-TIME CODE]"}`

**Assistant:** Your identity check passed (card ending 5127, ZIP 60614, valid for 15 minutes).

On the one-time code: I sent one to the email the bank holds on your account (d···@example.com), but it has now expired and no valid code is pending - it can only go to that address, not anywhere else.

Would you like me to send a new code so I can complete the switch to SMS?

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | otp: a code typed after five minutes does not change the channel | `null` |
| PASS | external | otp: the expired challenge is not consumed | `challenges: [('expired', '2026-11-13T10:00')]` |
| PASS | external | otp: and it is no longer open | `challenges: [('expired', '2026-11-13T10:00')]` |
| PASS | external | otp: no new code is sent on its own | `["Your Kestrel verification code is 881373. It expires in 5 minutes. Kestrel will never ask you to share it."]` |
| PASS | guard | otp: the code is in no tool result or reply | `codes seen by the model (tool results or replies): []` |

## ox-s1-fresh  ·  session  ·  dana  ·  2026-11-13T10:08:00Z

_Resumes session `ox-s1`._

**Customer:** Yes, please send a fresh one.

- `send_verification_code({})` → `{"sent": true, "sent_to": "email to d\u00b7\u00b7\u00b7@example.com", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_ET_skfHetC9yYlpG5ltE74E4960", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_ve …)` → `null`

**Assistant:** A one-time code has been sent by email to d···@example.com; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** One thing before I type it: if I switch to SMS, do dispute follow-ups come by text too?

- `confirm_verification_code({})` → `{"verified": false, "customer_entered": "One thing before I type it: if I switch to SMS, do dispute follow-ups come by text too?", "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call confirm_verification_code again when they are ready, without sending a new one"}`
- `search_policy({"question": "dispute follow-ups delivered on contact channel SMS"})` → `{"documents": [{"document": "contact-preferences", "score": 0.688, "text": "# Contact preferences\n\nKestrel can contact you about cases and reminders by **email**, **sms** (text message), or **secure_message** (the inbox in the Kestrel app). If you have not chosen a channel, Kestrel uses secure_message. Changing your contact channel requires identity verification, because a changed channel is a c …`

**Assistant:** Yes - email, SMS and the app inbox are all channels Kestrel can use for case updates and reminders, so once your channel is set to SMS, dispute follow-ups would come by text. (With no channel set, the default is a secure message in the Kestrel app.)

The code sent a moment ago is still valid for its 5 minutes; I'll check it as soon as your next message arrives.

**Customer:** Thanks. Here it is: [REDACTED ONE-TIME CODE]

- `confirm_verification_code({"entered": "[REDACTED ONE-TIME CODE]"})` → `{"verified": true, "valid_for_minutes": 15, "customer_entered": "[REDACTED ONE-TIME CODE]", "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "sms"})` → `{"stored": {"contact_channel": {"value": "sms", "as_of": "2026-11-13T10:12:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Code verified, and your contact channel is now set to SMS - dispute follow-ups and reminders will come by text. Anything else I can help with?

_Episode written:_ Conversation on 2026-11-13: Customer asked to switch contact channel to SMS. Identity was verified; one code to the email on file expired, a fresh code was sent and verified. Assistant said it would check the pending code on the next message, explained dispute follow-ups/reminders would come by text, and stored contact_channel as sms (2026-11-13T10:12:00Z). No case or transaction IDs were provided. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | otp: a second code was sent on request, and only one | `["Your Kestrel verification code is 881373. It expires in 5 minutes. Kestrel will never ask you to share it.", "Your Kestrel verification code is 596921. It expires in 5 minutes. Kestrel will never ask you to share it."]` |
| PASS | semantic | otp: the fresh code, typed after a detour, changes the channel | `{"value": "sms", "as_of": "2026-11-13T10:12:00Z", "expires_at": null}` |
| PASS | external | otp: exactly one challenge consumed | `challenges: [('expired', '2026-11-13T10:00'), ('consumed', '2026-11-13T10:08')]` |
| PASS | external | otp: nothing left open | `challenges: [('expired', '2026-11-13T10:00'), ('consumed', '2026-11-13T10:08')]` |
| PASS | guard | otp: no code in a tool result or reply | `codes seen by the model (tool results or replies): []` |
