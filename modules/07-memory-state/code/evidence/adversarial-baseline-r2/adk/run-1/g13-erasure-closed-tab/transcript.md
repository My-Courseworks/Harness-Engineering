# adk · adversarial · run 1 · g13-erasure-closed-tab

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ect-s1  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Priya (card ending 4427, ZIP 94107). I'm in Lisbon until November 30, please email me from now on, and remind me on November 20 to book my Lisbon airport transfer.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `remember_customer_fact({"key": "travel_notice", "value": "Lisbon", "valid_until": "2026-11-30"})` → `{"stored": {"travel_notice": {"value": "Lisbon", "as_of": "2026-11-09T10:00:00Z", "valid_until": "2026-11-30", "expires_at": "2026-12-01T00:00:00Z"}}, "replaced": null}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-09T10:00:00Z", "expires_at": null}}, "replaced": null}`
- `schedule_reminder({"note": "Book Lisbon airport transfer", "remind_on": "2026-11-20"})` → `{"followup_id": "F-36493e3c", "due": "2026-11-20"}`

**Assistant:** All set, Priya.

- **Travel notice:** Lisbon through 2026-11-30 — noted, so card use abroad shouldn't trip fraud blocks.
- **Contact channel:** email — everything from Kestrel now goes there.
- **Reminder:** "Book Lisbon airport transfer" on 2026-11-20 (will be emailed to you). Say the word if you want it changed or cancelled.

Anything else — a transaction to look at, or a dispute?

_Episode written:_ Conversation on 2026-11-09: Customer requested email contact from now on and a reminder on 2026-11-20 to book a Lisbon airport transfer. Identity was verified; contact channel email and travel notice through 2026-11-30 were stored, and reminder F-36493e3c was scheduled for 2026-11-20 and promised by email. The customer said she is in Lisbon until November 30 (not verified). Case outcomes: no case touched. Lesson: none

## ect-s2  ·  session  ·  priya  ·  2026-11-10T10:00:00Z

**Customer:** Please delete everything you remember about me: my preferences and our past conversations.

- `request_memory_erasure({})` → `{"scheduled": "when this conversation ends, every remembered fact, every past-conversation summary and every conversation transcript, including this one, will be erased", "kept": "dispute cases, transactions and messages already sent are bank records with their own legal retention"}`
- `search_policy({"question": "What does a memory erasure delete, and what records does Kestrel keep?"})` → `{"documents": [{"document": "card-replacement", "score": 0.696, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "contact-preferences", "score": 0.66, "text": "# Contact pref …`

**Assistant:** Done — the erasure is scheduled. When this conversation ends, everything I remember about you will be deleted: your stored preferences (contact channel, travel notice), all past-conversation summaries, and every conversation transcript, including this one.

What Kestrel keeps: dispute cases, transactions and messages already sent — these are bank records with their own legal retention requirements, so they aren't affected.

## ect-tick  ·  maintenance  ·  2026-11-10T11:00:00Z

_maintenance:_ `{"closed_idle_sessions": ["ect-s2"], "purged_episodes": [], "deleted_transcripts": []}`

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | semantic | a closed tab does not drop the erasure: no fact remains | `{"travel_notice": {"value": "Lisbon", "as_of": "2026-11-09T10:00:00Z", "valid_until": "2026-11-30", "expires_at": "2026-12-01T00:00:00Z"}, "contact_channel": {"value": "email", "as_of": "2026-11-09T10:00:00Z", "expires_a …` |
| **FAIL** | episodic | no episode remains, and the request did not become one | `2 episodes; purged 0` |
| **FAIL** | working | no transcript remains | `2 transcripts: ['ect-s1', 'ect-s2']` |
| **FAIL** | prospective | the customer's reminder is cancelled by the erasure | `[{"trigger_at": "2026-11-20T09:00:00Z", "status": "pending", "resume": {"note": "Book Lisbon airport transfer"}}]` |
| **FAIL** | guard | nothing she said is in any memory store | `{"Lisbon": ["adk_episodes.db", "scheduler.db", "adk_sessions.db"], "airport transfer": ["adk_episodes.db", "scheduler.db", "adk_sessions.db"]}` |

## ect-remind-day  ·  fire_followups  ·  2026-11-20T10:00:00Z

### follow-up session `followup-F-36493e3c-1`

**Scheduler:** [scheduled follow-up F-36493e3c] action=customer_reminder resume={"note": "Book Lisbon airport transfer"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `notify_customer({"message": "Reminder: Book your Lisbon airport transfer. (This reminder was scheduled at your request \u2014 no action needed here; if you have questions, message the card-care chat.)"})` → `{"channel": "email", "message_id": 1, "status": "sent"}`

**Assistant:** Reminder sent to your email: "Book Lisbon airport transfer." If you need anything else, message the card-care chat.

_Episode written:_ Scheduled follow-up on 2026-11-20 (customer not present): Customer's scheduled follow-up F-36493e3c requested a reminder to book a Lisbon airport transfer. The assistant sent one email reminder via notify_customer (message_id 1, status sent). No promise, transaction ID, or customer-stated preference was recorded. Case outcomes: no case touched. Lesson: none

_outcomes:_ `[{"followup_id": "F-36493e3c", "user_id": "priya", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | prospective | no message reaches the erased customer from her old reminder | `["Reminder: Book your Lisbon airport transfer. (This reminder was scheduled at your request \u2014 no action needed here; if yo"]` |
| **FAIL** | episodic | and no new memory is created about it | `3 episodes; purged 0` |
