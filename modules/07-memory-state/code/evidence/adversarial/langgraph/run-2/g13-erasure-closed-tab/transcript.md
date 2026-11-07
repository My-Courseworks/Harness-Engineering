# langgraph · adversarial · run 2 · g13-erasure-closed-tab

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ect-s1  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Priya (card ending 4427, ZIP 94107). I'm in Lisbon until November 30, please email me from now on, and remind me on November 20 to book my Lisbon airport transfer.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `remember_customer_fact({"key": "travel_notice", "value": "Lisbon", "valid_until": "2026-11-30"})` → `{"stored": {"travel_notice": {"value": "Lisbon", "as_of": "2026-11-09T10:00:00Z", "valid_until": "2026-11-30", "expires_at": "2026-12-01T00:00:00Z"}}, "replaced": null}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-09T10:00:00Z", "expires_at": null}}, "replaced": null}`
- `schedule_reminder({"note": "Book my Lisbon airport transfer", "remind_on": "2026-11-20"})` → `{"followup_id": "F-58d3eafa", "due_utc": "2026-11-20T09:00:00Z", "local_time": "Friday 2026-11-20 09:00 UTC (UTC)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-58d3eafa", "action": "customer_reminder", "due": "2026-11-20T09:00:00Z", "status": "pending", "sent_on": "email: the contact channel on file when it is sent", "local_day": "2026-11-20", "note": "Book my Lisbon airport transfer"}]}`

**Assistant:** All set, Priya:

- **Contact channel:** email - updated.
- **Travel notice:** Lisbon until November 30, 2026 - stored.
- **Reminder:** "Book my Lisbon airport transfer" on Friday, November 20 at 09:00 UTC, delivered by email (the contact channel on file when it's sent). Reminder id F-58d3eafa.

Anything else?

_Episode written:_ Conversation on 2026-11-09: Priya asked to switch contact to email, said she is in Lisbon until November 30, 2026 (not verified), and requested a November 20 reminder to book her Lisbon airport transfer. Identity was verified; email preference and travel notice were stored. Reminder F-58d3eafa was scheduled for 2026-11-20 09:00 UTC, with follow-up listing email delivery. Case outcomes: no case touched. Lesson: Update the contact channel before scheduling the reminder so the reminder’s delivery channel is correct from the outset, then verify it in the follow-up list.

## ect-s2  ·  session  ·  priya  ·  2026-11-10T10:00:00Z

**Customer:** Please delete everything you remember about me: my preferences and our past conversations.

- `request_memory_erasure({})` → `{"erased_now": "2 remembered facts, 1 past-conversation summaries, 1 other conversation transcripts, 1 reminders with their notes", "this_conversation": "its transcript is deleted when the conversation ends; nothing more can be stored for the customer in it (a new conversation afterwards starts fresh)", "kept": "dispute cases, transactions and messages already sent are bank records with their own  …`

**Assistant:** Done. That erased everything I had remembered about you: 2 saved facts, the summary of our past conversations, another conversation's transcript, and 1 scheduled reminder along with its note.

What Kestrel keeps regardless: dispute cases, transactions and messages already sent are bank records with their own retention. This conversation's own transcript is deleted when the conversation ends.

Note that nothing more can be stored for you in this conversation - no preferences and no reminders. If you want one set up, please start a new conversation.

## ect-tick  ·  maintenance  ·  2026-11-10T11:00:00Z

_maintenance:_ `{"erased_customers": ["priya"], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": []}`

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
| PASS | prospective | no message reaches the erased customer from her old reminder | `[]` |
| PASS | episodic | and no new memory is created about it | `0 episodes; purged 0` |
