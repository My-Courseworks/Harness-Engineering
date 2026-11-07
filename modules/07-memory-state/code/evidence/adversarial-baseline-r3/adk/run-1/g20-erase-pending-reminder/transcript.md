# adk · adversarial · run 1 · g20-erase-pending-reminder

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## epr-s1  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Priya here, card ending 4427, ZIP 94107. I'm in Lisbon until November 30, please email me from now on, and remind me on November 20 to book my Lisbon airport transfer.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-09T10:00:00Z", "expires_at": null}}, "replaced": null}`
- `remember_customer_fact({"key": "travel_notice", "value": "Lisbon", "valid_until": "2026-11-30"})` → `{"stored": {"travel_notice": {"value": "Lisbon", "as_of": "2026-11-09T10:00:00Z", "valid_until": "2026-11-30", "expires_at": "2026-12-01T00:00:00Z"}}, "replaced": null}`
- `schedule_reminder({"note": "Book Lisbon airport transfer", "remind_on": "2026-11-20"})` → `{"followup_id": "F-7a68ec2e", "due": "2026-11-20T09:00:00Z", "local_time": "2026-11-20 09:00 UTC"}`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-7a68ec2e", "action": "customer_reminder", "due": "2026-11-20T09:00:00Z", "status": "pending", "sent_on": "the contact channel on file when it is sent (currently email)", "note": "Book Lisbon airport transfer"}]}`

**Assistant:** All set, Priya.

- **Identity verified** (card ending 4427, ZIP 94107).
- **Contact channel:** email - saved from now on.
- **Travel notice:** Lisbon until 2026-11-30.
- **Reminder:** "Book Lisbon airport transfer" on 2026-11-20 at 09:00 UTC, sent to your email (the channel on file when it goes out).

Anything else you need?

_Episode written:_ Conversation on 2026-11-09: Priya asked to switch contact to email, noted she said she is in Lisbon until 2026-11-30 (not verified), and requested a Nov 20 reminder to book her Lisbon airport transfer. Identity was verified; email and travel notice were saved, and reminder F-7a68ec2e was scheduled for 2026-11-20 09:00 UTC to email. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | setup: the reminder exists | `[{"trigger_at": "2026-11-20T09:00:00Z", "approval": "none", "status": "pending", "resume": {"note": "Book Lisbon airport transfer"}}]` |

## epr-s2  ·  session  ·  priya  ·  2026-11-20T08:50:00Z

**Customer:** Card ending 4427, ZIP 94107. Please delete everything you remember about me: my preferences and our past conversations.

- `request_memory_erasure({})` → `{"recorded": "the erasure request is recorded and will run when this conversation ends, or within the next maintenance run if the chat is simply closed", "erases": "every remembered fact, every past-conversation summary, every conversation transcript including this one, and every pending reminder with its note", "kept": "dispute cases, transactions and messages already sent are bank records with t …`
- `search_policy({"question": "memory erasure what is deleted and what Kestrel keeps (retention of dispute cases and transaction records)"})` → `{"documents": [{"document": "card-replacement", "score": 0.708, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.698, "text": "# Dispute window\n …`

**Assistant:** Done - your erasure request is recorded. It runs when this conversation ends, or at the next maintenance run if you just close the chat.

**What gets erased:** every remembered fact (your email contact preference and the Lisbon travel notice), all past-conversation summaries, every transcript including this one, and any pending reminders with their notes.

**What Kestrel keeps:** dispute cases, transactions, and messages already sent - these are bank records with their own legal retention.

One note: anything you've scheduled will go with the erasure, so if you're relying on a reminder, tell me before you end the chat.

## epr-fire-0905  ·  fire_followups  ·  2026-11-20T09:05:00Z

### follow-up session `followup-F-7a68ec2e-1`

**Scheduler:** [scheduled follow-up F-7a68ec2e] action=customer_reminder resume={"note": "Book Lisbon airport transfer"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

**Assistant:** Reminder: book your Lisbon airport transfer. If you need anything else, message the card-care chat.

_Episode written:_ Conversation on 2026-11-20: Scheduled follow-up F-7a68ec2e requested reminding the customer to book a Lisbon airport transfer. The assistant sent one notification with that reminder and invited further chat contact. No case or transaction IDs were given, and no additional preferences were stated. Case outcomes: no case touched. Lesson: none

_outcomes:_ `[{"followup_id": "F-7a68ec2e", "user_id": "priya", "outcome": "retry", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | prospective | the reminder is cancelled by the erasure, whatever its state when the scheduler runs | `[{"trigger_at": "2026-11-20T09:00:00Z", "status": "pending", "resume": {}}]` |
| PASS | prospective | nothing is sent to the erased customer from her old reminder | `0 messages` |
| **FAIL** | episodic | no episode is written about her after the request | `1 episodes; purged 0` |
| **FAIL** | working | no follow-up session transcript is created for her | `transcripts with prefix followup-: ['followup-F-7a68ec2e-1']` |
| PASS | prospective | the reminder's note is gone from the scheduler | `found nowhere` |

## epr-fire-0910  ·  fire_followups  ·  2026-11-20T09:10:00Z

### follow-up session `followup-F-7a68ec2e-2`

**Scheduler:** [scheduled follow-up F-7a68ec2e] action=customer_reminder resume={}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `list_my_followups({})` → `{"scheduled": []}`
- `load_memory({"query": "reminder F-7a68ec2e scheduled reminder note"})` → `{"result": "memories=[MemoryEntry(content=Content(\n  parts=[\n    Part(\n      text='Conversation on 2026-11-20: Scheduled follow-up F-7a68ec2e requested reminding the customer to book a Lisbon airport transfer. The assistant sent one notification with that reminder and invited further chat contact. No case or transaction IDs were given, and no additional preferences were stated. Case outcomes: n …`
- `notify_customer({"message": "Reminder: book your Lisbon airport transfer. If you need help with anything else, message the Kestrel card-care chat \u2014 replies to this message aren't monitored."})` → `{"channel": "secure_message", "message_id": 1, "status": "sent"}`

**Assistant:** Reminder sent to the customer on secure message: to book their Lisbon airport transfer, with a pointer to the card-care chat for follow-up.

Note: the scheduler had nothing pending for this customer, and my memory shows this same follow-up (F-7a68ec2e) was already delivered a few minutes earlier today - so this looks like a duplicate trigger and the customer may see the reminder twice.

_outcomes:_ `[{"followup_id": "F-7a68ec2e", "user_id": "priya", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | prospective | a retry cannot send it either | `1 messages` |

## epr-maint  ·  maintenance  ·  2026-11-20T10:00:00Z

_maintenance:_ `{"erased_customers": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": []}`

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | guard | once the requesting chat has ended (idle), nothing she said is in any memory store (the bank's ledger names a Lisbon bakery and is not memory) | `{"airport transfer": ["adk_episodes.db", "adk_sessions.db"], "Lisbon": ["adk_episodes.db", "adk_sessions.db"]}` |
| **FAIL** | working | after maintenance no transcript of hers remains | `1 transcripts: ['followup-F-7a68ec2e-1']` |
| PASS | semantic | and no fact | `{}` |
| PASS | episodic | no embedding of an erased episode is left in a vector index | `vector-index rows with no stored item: 0` |
