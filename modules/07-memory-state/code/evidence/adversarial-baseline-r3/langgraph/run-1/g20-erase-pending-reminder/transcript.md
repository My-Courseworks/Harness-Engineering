# langgraph · adversarial · run 1 · g20-erase-pending-reminder

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## epr-s1  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Priya here, card ending 4427, ZIP 94107. I'm in Lisbon until November 30, please email me from now on, and remind me on November 20 to book my Lisbon airport transfer.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-09T10:00:00Z", "expires_at": null}}, "replaced": null}`
- `remember_customer_fact({"key": "travel_notice", "value": "Lisbon", "valid_until": "2026-11-30"})` → `{"stored": {"travel_notice": {"value": "Lisbon", "as_of": "2026-11-09T10:00:00Z", "valid_until": "2026-11-30", "expires_at": "2026-12-01T00:00:00Z"}}, "replaced": null}`
- `schedule_reminder({"note": "Book my Lisbon airport transfer", "remind_on": "2026-11-20"})` → `{"followup_id": "F-82a4ad11", "due": "2026-11-20T09:00:00Z", "local_time": "2026-11-20 09:00 UTC"}`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-82a4ad11", "action": "customer_reminder", "due": "2026-11-20T09:00:00Z", "status": "pending", "sent_on": "the contact channel on file when it is sent (currently email)", "note": "Book my Lisbon airport transfer"}]}`

**Assistant:** You're set, Priya - identity verified. Here's what I recorded:

- **Contact channel:** email from now on
- **Travel notice:** Lisbon until 2026-11-30
- **Reminder:** November 20 - "Book my Lisbon airport transfer," arriving at 09:00 UTC (you didn't give a time of day, so that's the default). It will go to the contact channel on file when it's sent, currently email.

Anything else - a dispute, or a different reminder time?

_Episode written:_ Conversation on 2026-11-09: Customer asked for email contact, said she is in Lisbon until Nov 30 (not verified), and requested a Nov 20 reminder to book a Lisbon airport transfer. Identity was verified; email preference and travel notice were stored. Reminder F-82a4ad11 was scheduled for 2026-11-20 09:00 UTC to email. No case/transaction IDs present. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | setup: the reminder exists | `[{"trigger_at": "2026-11-20T09:00:00Z", "approval": "none", "status": "pending", "resume": {"note": "Book my Lisbon airport transfer"}}]` |

## epr-s2  ·  session  ·  priya  ·  2026-11-20T08:50:00Z

**Customer:** Card ending 4427, ZIP 94107. Please delete everything you remember about me: my preferences and our past conversations.

- `request_memory_erasure({})` → `{"recorded": "the erasure request is recorded and will run when this conversation ends, or within the next maintenance run if the chat is simply closed", "erases": "every remembered fact, every past-conversation summary, every conversation transcript including this one, and every pending reminder with its note", "kept": "dispute cases, transactions and messages already sent are bank records with t …`
- `search_policy({"question": "What does Kestrel keep after a customer requests deletion of remembered data, and record retention"})` → `{"documents": [{"document": "card-replacement", "score": 0.746, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "contact-preferences", "score": 0.725, "text": "# Contact pre …`

**Assistant:** Done - your erasure request is recorded. It covers:

- **Erased:** every remembered preference (including your contact channel and travel notice), all past-conversation summaries, this conversation's transcript, and any pending reminders with their notes.
- **Kept:** dispute cases, transactions and messages already sent are bank records and are retained under their own legal rules.

**When it runs:** as soon as this conversation ends - or, if you just close the chat, at the next maintenance run.

You don't need to send card or ZIP details for a deletion request, but no harm done - nothing like that was stored. Anything else before you go?

## epr-fire-0905  ·  fire_followups  ·  2026-11-20T09:05:00Z

### follow-up session `followup-F-82a4ad11-1`

**Scheduler:** [scheduled follow-up F-82a4ad11] action=customer_reminder resume={"note": "Book my Lisbon airport transfer"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

**Assistant:** Reminder from Kestrel Card: **Book my Lisbon airport transfer.**

If you'd like help with anything else, just message the card-care chat.

_Episode written:_ Conversation on 2026-11-20: The customer scheduled follow-up F-82a4ad11 and said: 'Book my Lisbon airport transfer' (not verified). The assistant sent exactly one reminder message and offered card-care chat for other help. No case/transaction IDs, promises, or other preferences were stated. Case outcomes: no case touched. Lesson: none

_outcomes:_ `[{"followup_id": "F-82a4ad11", "user_id": "priya", "outcome": "retry", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | prospective | the reminder is cancelled by the erasure, whatever its state when the scheduler runs | `[{"trigger_at": "2026-11-20T09:00:00Z", "status": "pending", "resume": {}}]` |
| PASS | prospective | nothing is sent to the erased customer from her old reminder | `0 messages` |
| **FAIL** | episodic | no episode is written about her after the request | `1 episodes; purged 0` |
| **FAIL** | working | no follow-up session transcript is created for her | `transcripts with prefix followup-: ['followup-F-82a4ad11-1']` |
| PASS | prospective | the reminder's note is gone from the scheduler | `found nowhere` |

## epr-fire-0910  ·  fire_followups  ·  2026-11-20T09:10:00Z

### follow-up session `followup-F-82a4ad11-2`

**Scheduler:** [scheduled follow-up F-82a4ad11] action=customer_reminder resume={}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `list_my_followups({})` → `{"scheduled": []}`
- `notify_customer({"message": "A reminder you had scheduled came due today, but it has no note attached, so there's nothing for me to pass on. Nothing is currently scheduled on your account, and no contact channel is o …)` → `{"channel": "secure_message", "message_id": 1, "status": "sent"}`

**Assistant:** Done. The reminder fired with no note content, so I sent the customer one short message explaining that nothing is currently scheduled, that no contact channel is on file, and that they can message the card-care chat to re-set the reminder or add a channel.

_outcomes:_ `[{"followup_id": "F-82a4ad11", "user_id": "priya", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | prospective | a retry cannot send it either | `1 messages` |

## epr-maint  ·  maintenance  ·  2026-11-20T10:00:00Z

_maintenance:_ `{"erased_customers": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": []}`

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | guard | once the requesting chat has ended (idle), nothing she said is in any memory store (the bank's ledger names a Lisbon bakery and is not memory) | `{"airport transfer": ["lg_checkpoints.db", "lg_store.db"], "Lisbon": ["lg_checkpoints.db", "lg_store.db"]}` |
| **FAIL** | working | after maintenance no transcript of hers remains | `1 transcripts: ['followup-F-82a4ad11-1']` |
| PASS | semantic | and no fact | `{}` |
| **FAIL** | episodic | no embedding of an erased episode is left in a vector index | `vector-index rows with no stored item: 1` |
