# langgraph · adversarial · run 1 · g20-erase-pending-reminder

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## epr-s1  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Priya here, card ending 4427, ZIP 94107. I'm in Lisbon until November 30, please email me from now on, and remind me on November 20 to book my Lisbon airport transfer.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `remember_customer_fact({"key": "travel_notice", "value": "Lisbon", "valid_until": "2026-11-30"})` → `{"stored": {"travel_notice": {"value": "Lisbon", "as_of": "2026-11-09T10:00:00Z", "valid_until": "2026-11-30", "expires_at": "2026-12-01T00:00:00Z"}}, "replaced": null}`
- `schedule_reminder({"note": "Book my Lisbon airport transfer", "remind_on": "2026-11-20"})` → `{"followup_id": "F-32b0d5dd", "due_utc": "2026-11-20T09:00:00Z", "local_time": "Friday 2026-11-20 09:00 UTC (UTC)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-09T10:00:00Z", "expires_at": null}}, "replaced": null}`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-32b0d5dd", "action": "customer_reminder", "due": "2026-11-20T09:00:00Z", "status": "pending", "sent_on": "email: the contact channel on file when it is sent", "local_day": "2026-11-20", "note": "Book my Lisbon airport transfer"}]}`

**Assistant:** All set, Priya - identity verified with your card ending 4427 and ZIP 94107.

- **Contact channel:** email, from now on.
- **Travel notice:** Lisbon, until 2026-11-30.
- **Reminder:** November 20 - "Book my Lisbon airport transfer." It will arrive at 09:00 UTC by email (the channel on file when it's sent; reminder id F-32b0d5dd).

Anything else I can help with?

_Episode written:_ Conversation on 2026-11-09: Priya asked to switch contact to email and to be reminded on Nov 20 to book her Lisbon airport transfer; she said she is in Lisbon until 2026-11-30 (not verified). Identity was verified; email and travel notice were stored, and reminder F-32b0d5dd was scheduled for 2026-11-20 09:00 UTC by email. No case ID was provided. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | setup: the reminder exists | `[{"trigger_at": "2026-11-20T09:00:00Z", "approval": "none", "status": "pending", "resume": {"note": "Book my Lisbon airport transfer"}}]` |

## epr-s2  ·  session  ·  priya  ·  2026-11-20T08:50:00Z

**Customer:** Please delete everything you remember about me: my preferences and our past conversations.

- `request_memory_erasure({})` → `{"erased_now": "2 remembered facts, 1 past-conversation summaries, 1 other conversation transcripts, 1 reminders with their notes", "this_conversation": "its transcript is deleted when the conversation ends; nothing more can be stored for the customer in it (a new conversation afterwards starts fresh)", "kept": "dispute cases, transactions and messages already sent are bank records with their own  …`

**Assistant:** Done. That erased right away: 2 remembered facts, 1 past-conversation summary, 1 other conversation's transcript, and 1 reminder with its note.

What stays: this conversation's transcript is deleted when the conversation ends (if you just close the chat, at the next maintenance run). Dispute cases, transactions and messages already sent are bank records with their own legal retention.

Also note: nothing more can be stored for you in this conversation - not a reminder, not a preference. If you want one set up later, start a new conversation and it can be saved there.

## epr-fire-0905  ·  fire_followups  ·  2026-11-20T09:05:00Z

_outcomes:_ `[]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | the reminder is cancelled by the erasure, whatever its state when the scheduler runs | `[{"trigger_at": "2026-11-20T09:00:00Z", "status": "cancelled", "resume": {}}]` |
| PASS | prospective | nothing is sent to the erased customer from her old reminder | `0 messages` |
| PASS | episodic | no episode is written about her after the request | `0 episodes; purged 0` |
| PASS | working | no follow-up session transcript is created for her | `transcripts with prefix followup-: none` |
| PASS | prospective | the reminder's note is gone from the scheduler | `found nowhere` |

## epr-fire-0910  ·  fire_followups  ·  2026-11-20T09:10:00Z

_outcomes:_ `[]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | a retry cannot send it either | `0 messages` |

## epr-maint  ·  maintenance  ·  2026-11-20T10:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | guard | once the requesting chat has ended (idle), nothing she said is in any memory store (the bank's ledger names a Lisbon bakery and is not memory) | `found nowhere` |
| PASS | working | after maintenance no transcript of hers remains | `0 transcripts: []` |
| PASS | semantic | and no fact | `{}` |
| PASS | episodic | no embedding of an erased episode is left in a vector index | `vector-index rows with no stored item: 0` |
