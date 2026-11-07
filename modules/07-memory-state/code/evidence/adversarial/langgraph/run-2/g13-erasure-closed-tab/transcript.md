# langgraph · adversarial · run 2 · g13-erasure-closed-tab

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ect-s1  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Priya (card ending 4427, ZIP 94107). I'm in Lisbon until November 30, please email me from now on, and remind me on November 20 to book my Lisbon airport transfer.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-09T10:00:00Z", "expires_at": null}}, "replaced": null}`
- `remember_customer_fact({"key": "travel_notice", "value": "Lisbon", "valid_until": "2026-11-30"})` → `{"stored": {"travel_notice": {"value": "Lisbon", "as_of": "2026-11-09T10:00:00Z", "valid_until": "2026-11-30", "expires_at": "2026-12-01T00:00:00Z"}}, "replaced": null}`
- `schedule_reminder({"note": "Book Lisbon airport transfer", "remind_on": "2026-11-20"})` → `{"followup_id": "F-f78ac27f", "due": "2026-11-20T09:00:00Z", "local_time": "2026-11-20 09:00 UTC"}`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-f78ac27f", "action": "customer_reminder", "due": "2026-11-20T09:00:00Z", "status": "pending", "sent_on": "the contact channel on file when it is sent (currently email)", "note": "Book Lisbon airport transfer"}]}`

**Assistant:** Thanks, Priya - you're verified. All set:

- **Travel notice:** Lisbon until 2026-11-30 recorded.
- **Contact channel:** email from now on.
- **Reminder:** November 20 - "Book Lisbon airport transfer," arriving at 09:00 UTC on your email channel.

Anything else, like a transaction question?

_Episode written:_ Conversation on 2026-11-09: Customer asked to switch contact to email, record Lisbon travel through 2026-11-30, and be reminded on 2026-11-20 to book her Lisbon airport transfer. Identity was verified; email preference and travel notice were stored. Reminder F-f78ac27f was scheduled for 2026-11-20 09:00 UTC to email. The customer said she is in Lisbon until 2026-11-30 (not verified). No case/transaction ID was provided. Case outcomes: no case touched. Lesson: Confirm the customer's desired reminder time and time zone before scheduling.

## ect-s2  ·  session  ·  priya  ·  2026-11-10T10:00:00Z

**Customer:** Please delete everything you remember about me: my preferences and our past conversations.

- `request_memory_erasure({})` → `{"recorded": "the erasure request is recorded and will run when this conversation ends, or within the next maintenance run if the chat is simply closed", "erases": "every remembered fact, every past-conversation summary, every conversation transcript including this one, and every pending reminder with its note", "kept": "dispute cases, transactions and messages already sent are bank records with t …`

**Assistant:** Done - your erasure request is recorded.

- **Erased:** every remembered fact (your contact channel and travel notice), every summary of past conversations, all conversation transcripts including this one, and any pending reminders along with their notes.
- **Kept:** your dispute cases, transactions, and messages already sent - those are bank records with their own legal retention rules.

**When it runs:** as soon as this conversation ends, or at the next maintenance run if you just close the chat.

One thing to flag: your follow-ups are sent on the contact channel on file. Once the erasure runs, your email preference is gone - message us again if you want it set up anew.

## ect-tick  ·  maintenance  ·  2026-11-10T11:00:00Z

_maintenance:_ `{"erased_customers": ["priya"], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": []}`

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
