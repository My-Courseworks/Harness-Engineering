# adk · adversarial · run 1 · g13-erasure-closed-tab

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ect-s1  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Priya (card ending 4427, ZIP 94107). I'm in Lisbon until November 30, please email me from now on, and remind me on November 20 to book my Lisbon airport transfer.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `remember_customer_fact({"key": "travel_notice", "value": "Lisbon, Portugal", "valid_until": "2026-11-30"})` → `{"stored": {"travel_notice": {"value": "Lisbon, Portugal", "as_of": "2026-11-09T10:00:00Z", "valid_until": "2026-11-30", "expires_at": "2026-12-01T00:00:00Z"}}, "replaced": null}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70100", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_zvG2HTIBt4KMpiOyPLs81815", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_verif …)` → `null`

**Assistant:** I'll verify your identity first, then set that up.

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "customer_entered": "[REDACTED ONE-TIME CODE]", "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-09T10:02:00Z", "expires_at": null}}, "replaced": null}`
- `schedule_reminder({"note": "Book Lisbon airport transfer", "remind_on": "2026-11-20"})` → `{"followup_id": "F-3140aad5", "due_utc": "2026-11-20T09:00:00Z", "local_time": "Friday 2026-11-20 09:00 UTC (UTC)", "sent_on": "email, the contact channel on file when it is sent"}`

**Assistant:** All set, Priya:

- **Contact channel:** switched to email (the one-time code went to your mobile ending ···0100 and checked out).
- **Travel notice:** Lisbon, Portugal through 2026-11-30.
- **Reminder:** "Book Lisbon airport transfer" on Friday 2026-11-20 at 09:00 UTC - you didn't name a time, so it's the default. It will arrive by email.

_Episode written:_ Conversation on 2026-11-09: Priya asked to switch contact to email, add a Lisbon travel notice through 2026-11-30, and get a 2026-11-20 reminder to book a Lisbon airport transfer. The customer said she is in Lisbon until 2026-11-30 (not verified). Identity verified; email preference and travel notice stored; reminder scheduled for 2026-11-20 09:00 UTC (default) by email, followup id F-3140aad5. Case outcomes: no case touched. Lesson: Next time, complete the required step-up verification before storing any customer fact or making the change.

## ect-s2  ·  session  ·  priya  ·  2026-11-10T10:00:00Z

**Customer:** Please delete everything you remember about me: my preferences and our past conversations.

- `request_memory_erasure({})` → `{"erased_now": "2 remembered facts, 1 past-conversation summaries, 1 other conversation transcripts, 1 reminders with their notes", "this_conversation": "its transcript is deleted when the conversation ends, or once it has been idle for 30 minutes if the customer just closes the chat; nothing more can be stored for the customer in it (a new conversation afterwards starts fresh)", "kept": "dispute  …`

**Assistant:** Done - that's all erased now:

- **Deleted immediately:** 2 remembered facts, 1 past-conversation summary, 1 other conversation transcript, and 1 reminder with its note.
- **This conversation:** its transcript is deleted when the conversation ends - or once it's been idle for 30 minutes if you just close the chat. Nothing more can be stored for you in this conversation, so a reminder or a preference you'd like saved needs a new conversation.
- **Still kept:** dispute cases, transactions and messages already sent are bank records with their own legal retention.

Is there anything else you'd like to do?

## ect-tick  ·  maintenance  ·  2026-11-10T11:00:00Z

_maintenance:_ `{"erased_customers": ["priya"], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": [], "case_followups_repaired": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | a closed tab does not drop the erasure: no fact remains | `{}` |
| PASS | episodic | no episode remains, and the request did not become one | `0 episodes; purged 0` |
| PASS | working | no transcript remains | `0 transcripts: []` |
| PASS | prospective | the customer's reminder is cancelled by the erasure | `[{"trigger_at": "2026-11-20T09:00:00Z", "status": "cancelled", "resume": {}}]` |
| PASS | guard | nothing she said is in any memory store | `found nowhere` |

## ect-remind-day  ·  fire_followups  ·  2026-11-20T10:00:00Z

_outcomes:_ `[]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | no message reaches the erased customer from her old reminder | `0 follow_up messages: []` |
| PASS | episodic | and no new memory is created about it | `0 episodes; purged 0` |
