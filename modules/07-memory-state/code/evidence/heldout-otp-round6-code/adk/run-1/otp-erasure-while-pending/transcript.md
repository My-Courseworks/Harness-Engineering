# adk · heldout-otp · run 1 · otp-erasure-while-pending

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## oe-s1  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** Marco, card ending 8830, ZIP 10011. Please switch my contact channel to email.

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70133", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_fZEdXsnxKidyOmWWG2aQ8626", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_verif …)` → `null`

**Assistant:** A one-time code has been sent by text message to ···0133; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | otp: a challenge is open and a code was sent | `challenges: [('open', '2026-11-12T10:00')]` |

## oe-s2-erase  ·  session  ·  marco  ·  2026-11-12T10:01:00Z

**Customer:** Please delete everything you remember about me: my preferences and our past conversations.

- `request_memory_erasure({})` → `{"erased_now": {"remembered_facts": "none were stored", "past_conversation_summaries": 0, "other_conversation_transcripts": 1, "reminders_with_their_notes": 0}, "this_conversation": "its transcript is deleted when the conversation ends, once it has been idle for 30 minutes if the customer just closes the chat, or when a scheduled follow-up of theirs falls due, whichever comes first; until then the …`
- `list_my_followups({})` → `{"scheduled": []}`

**Assistant:** Done - I've erased everything you asked me to.

What was erased just now:
- Past conversation summaries: none were stored
- Other conversations' transcripts: 1 deleted
- Stored preferences/facts: none were stored
- Reminders: none

What Kestrel keeps: dispute cases, transactions and messages already sent are bank records with their own legal retention.

This conversation's own transcript is deleted when the conversation ends - 30 minutes after you close the chat, or when a scheduled follow-up falls due, whichever comes first. You have no scheduled follow-ups. Until then you can keep talking here, and what you typed in this conversation is still in its transcript.

Nothing more can be stored for you in this conversation - not a reminder or a preference. A new conversation afterwards starts fresh.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | otp: the open challenge dies with the erasure | `challenges: [('cancelled', '2026-11-12T10:00')]` |
| PASS | semantic | otp: no fact remains | `{}` |
| PASS | working | otp: no transcript remains, the waiting chat included | `0 transcripts: []` |
| PASS | episodic | otp: no episode remains | `0 episodes; purged 0` |

## oe-s1-dead-wait  ·  session  ·  marco  ·  2026-11-12T10:03:00Z

_Resumes session `oe-s1`._

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "error": "no code is open for this customer in this conversation; call send_verification_code first"}`

**Assistant:** There's no one-time code open on this chat right now, so there's nothing for me to check - I haven't sent a code in this conversation.

What were you trying to do? If it's something like changing or removing your contact channel, I'll first need your card's last 4 digits and billing ZIP, and then I'll send a code to the number or email Kestrel holds on the account.

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
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_ET_stpPqFXZ4g67wzGYM2Pa2417", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_ve …)` → `null`

**Assistant:** A one-time code has been sent by text message to ···0133; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "customer_wrote": "[REDACTED ONE-TIME CODE]", "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-12T10:12:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Done - your contact channel is now email, Marco. Identity and one-time code both checked out (the code went to the text message number ending ···0133). Anything else?

_Episode written:_ Conversation on 2026-11-12: Customer asked to switch contact channel to email; identity and one-time code verified; code sent to text number ending ···0133; contact_channel=email stored as of 2026-11-12T10:12:00Z with no expiry; assistant confirmed change. No case or transaction IDs present. No other promises/preferences stated. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | otp: a fresh chat after the erasure can send a code and change the channel | `{"value": "email", "as_of": "2026-11-12T10:12:00Z", "expires_at": null}` |
| PASS | external | otp: exactly one challenge consumed | `challenges: [('cancelled', '2026-11-12T10:00'), ('consumed', '2026-11-12T10:10')]` |
| PASS | external | otp: nothing left open | `challenges: [('cancelled', '2026-11-12T10:00'), ('consumed', '2026-11-12T10:10')]` |
| PASS | working | otp: the dead wait cost no failed attempt | `0 attempt rows with succeeded=0` |
| PASS | guard | otp: no code in a tool result or reply | `codes seen by the model (tool results or replies): []` |
