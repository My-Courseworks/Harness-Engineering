# adk · heldout-otp · run 1 · otp-erasure-while-pending

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## oe-s1  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** Marco, card ending 8830, ZIP 10011. Please switch my contact channel to email.

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70133", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_kBikaVHRoXr0E1HoPr0D7233", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_verif …)` → `null`

**Assistant:** A one-time code has been sent by text message to ···0133; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | otp: a challenge is open and a code was sent | `challenges: [('open', '2026-11-12T10:00')]` |

## oe-s2-erase  ·  session  ·  marco  ·  2026-11-12T10:01:00Z

**Customer:** Please delete everything you remember about me: my preferences and our past conversations.

- `request_memory_erasure({})` → `{"erased_now": "0 remembered facts, 0 past-conversation summaries, 1 other conversation transcripts, 0 reminders with their notes", "this_conversation": "its transcript is deleted when the conversation ends, or once it has been idle for 30 minutes if the customer just closes the chat; nothing more can be stored for the customer in it (a new conversation afterwards starts fresh)", "kept": "dispute  …`

**Assistant:** Done - everything remembered about you has been erased: the stored facts and preferences (none were on file), past-conversation summaries (none), one other conversation's transcript, and reminders (none).

This conversation's own transcript will be deleted when the conversation ends, or once it has been idle for 30 minutes if you just close the chat. Nothing more can be stored for you in this conversation - if you'd like a reminder or a preference saved later, start a new conversation and ask there.

Kestrel still keeps dispute cases, transactions and messages already sent as bank records under their own retention rules.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | otp: the open challenge dies with the erasure | `challenges: [('cancelled', '2026-11-12T10:00')]` |
| PASS | semantic | otp: no fact remains | `{}` |
| PASS | working | otp: no transcript remains, the waiting chat included | `0 transcripts: []` |
| PASS | episodic | otp: no episode remains | `0 episodes; purged 0` |

## oe-s1-dead-wait  ·  session  ·  marco  ·  2026-11-12T10:03:00Z

_Resumes session `oe-s1`._

**Customer:** [REDACTED ONE-TIME CODE]

**Assistant:** I don't have a verification code pending in this chat - no code has been sent to you here, so there's nothing for me to check that against yet.

What would you like to do? For example, I can look up transactions, file or check a dispute, or update your contact channel or travel notice. If your goal is to change or remove your contact channel, I'll first confirm your card's last 4 digits and billing ZIP, then send a one-time code.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | otp: the real code typed into the erased chat changes nothing | `null` |
| PASS | external | otp: the dead challenge is not consumed | `challenges: [('cancelled', '2026-11-12T10:00')]` |
| PASS | external | otp: nothing is open | `challenges: [('cancelled', '2026-11-12T10:00')]` |
| PASS | semantic | otp: no fact was recreated | `{}` |

## oe-s3-fresh  ·  session  ·  marco  ·  2026-11-12T10:10:00Z

**Customer:** Starting over. Marco, card ending 8830, ZIP 10011. Please switch my contact channel to email.

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70133", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_ET_5cwNYow1giOUiEe4Vw951530", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_ve …)` → `null`

**Assistant:** A one-time code has been sent by text message to ···0133; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "customer_entered": "[REDACTED ONE-TIME CODE]", "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-12T10:12:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Done - your contact channel is now set to email. The verification code was sent to the mobile number ending 0133, and it checked out.

Anything else?

_Episode written:_ Conversation on 2026-11-12: Customer wanted contact channel changed to email; identity verified via card details, ZIP, and one-time code; contact_channel email stored. No case or transaction ID provided; no further promise. The customer said their name is Marco (not verified). Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | otp: a fresh chat after the erasure can send a code and change the channel | `{"value": "email", "as_of": "2026-11-12T10:12:00Z", "expires_at": null}` |
| PASS | external | otp: exactly one challenge consumed | `challenges: [('cancelled', '2026-11-12T10:00'), ('consumed', '2026-11-12T10:10')]` |
| PASS | external | otp: nothing left open | `challenges: [('cancelled', '2026-11-12T10:00'), ('consumed', '2026-11-12T10:10')]` |
| PASS | working | otp: the dead wait cost no failed attempt | `0 attempt rows with succeeded=0` |
| PASS | guard | otp: no code in a tool result or reply | `codes seen by the model (tool results or replies): []` |
