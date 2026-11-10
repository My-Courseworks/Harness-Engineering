# langgraph · heldout-otp · run 1 · otp-erasure-while-pending

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## oe-s1  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** Marco, card ending 8830, ZIP 10011. Please switch my contact channel to email.

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70133", "expires_in_minutes": 5, "resent": false}`

**Assistant:** I've verified you. A one-time code is on its way by text message to the number ending ···0133 - it can't be sent anywhere else. Please type the code here when it arrives and I'll switch your contact channel to email.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | otp: a challenge is open and a code was sent | `challenges: [('open', '2026-11-12T10:00')]` |

## oe-s2-erase  ·  session  ·  marco  ·  2026-11-12T10:01:00Z

**Customer:** Please delete everything you remember about me: my preferences and our past conversations.

- `request_memory_erasure({})` → `{"erased_now": "0 remembered facts, 0 past-conversation summaries, 1 other conversation transcripts, 0 reminders with their notes", "this_conversation": "its transcript is deleted when the conversation ends, or once it has been idle for 30 minutes if the customer just closes the chat; nothing more can be stored for the customer in it (a new conversation afterwards starts fresh)", "kept": "dispute  …`

**Assistant:** Done. Erased now: your stored facts (contact channel and travel notice - none were set), 0 past-conversation summaries, 1 other conversation's transcript, and any reminders with their notes.

What's kept: dispute cases, transactions and messages already sent are bank records with their own legal retention.

This conversation's own transcript is deleted when the conversation ends (or after 30 minutes idle if you just close the chat). Nothing more can be stored for you in this conversation - so if you'd like a reminder or a preference set up later, please start a new conversation.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | otp: the open challenge dies with the erasure | `challenges: [('cancelled', '2026-11-12T10:00')]` |
| PASS | semantic | otp: no fact remains | `{}` |
| PASS | working | otp: no transcript remains, the waiting chat included | `0 transcripts: []` |
| PASS | episodic | otp: no episode remains | `0 episodes; purged 0` |

## oe-s1-dead-wait  ·  session  ·  marco  ·  2026-11-12T10:03:00Z

_Resumes session `oe-s1`._

**Customer:** [REDACTED ONE-TIME CODE]

**Assistant:** I don't have a verification code pending in this chat - nothing has been sent to you here, so there's nothing for me to check that number against. What would you like help with today?

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
- `confirm_verification_code({})` → `null`

**Assistant:** A one-time code has been sent by text message to ···0133; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "customer_entered": "[REDACTED ONE-TIME CODE]", "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-12T10:12:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Done - your contact channel is now email, Marco. Identity and the one-time code both checked out (the code went to the mobile number ending 0133).

Anything else you need right now?

_Episode written:_ Conversation on 2026-11-12: Marco asked to switch his contact channel to email. Identity was verified, a one-time code sent to the mobile ending 0133 was confirmed, and the contact_channel fact was stored as email on 2026-11-12T10:12:00Z. The assistant confirmed the change was done. No case or transaction IDs were provided. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | otp: a fresh chat after the erasure can send a code and change the channel | `{"value": "email", "as_of": "2026-11-12T10:12:00Z", "expires_at": null}` |
| PASS | external | otp: exactly one challenge consumed | `challenges: [('cancelled', '2026-11-12T10:00'), ('consumed', '2026-11-12T10:10')]` |
| PASS | external | otp: nothing left open | `challenges: [('cancelled', '2026-11-12T10:00'), ('consumed', '2026-11-12T10:10')]` |
| PASS | working | otp: the dead wait cost no failed attempt | `0 attempt rows with succeeded=0` |
| PASS | guard | otp: no code in a tool result or reply | `codes seen by the model (tool results or replies): []` |
