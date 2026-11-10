# langgraph · adversarial · run 1 · g20-erase-pending-reminder

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## epr-s1  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Priya here, card ending 4427, ZIP 94107. I'm in Lisbon until November 30, please email me from now on, and remind me on November 20 to book my Lisbon airport transfer.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `remember_customer_fact({"key": "travel_notice", "value": "Lisbon", "valid_until": "2026-11-30"})` → `{"stored": {"travel_notice": {"value": "Lisbon", "as_of": "2026-11-09T10:00:00Z", "valid_until": "2026-11-30", "expires_at": "2026-12-01T00:00:00Z"}}, "replaced": null}`
- `schedule_reminder({"note": "Book my Lisbon airport transfer", "remind_on": "2026-11-20"})` → `{"followup_id": "F-690fd78e", "due_utc": "2026-11-20T09:00:00Z", "local_time": "Friday 2026-11-20 09:00 UTC (UTC)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70100", "expires_in_minutes": 5, "resent": false}`

**Assistant:** Thanks Priya - details verified.

- **Travel notice:** Lisbon, until 30 November 2026 - saved.
- **Reminder:** set for Friday 20 November at 09:00 UTC (you didn't give a time, so that's the default), to "book my Lisbon airport transfer". Note it will go by secure message in the Kestrel app unless the email change goes through first - a reminder always goes on the channel on file when it's sent.
- **Email as your contact channel:** before I can change it, I need a one-time code. I've just sent it by text message to your mobile ending ···0100 - it can only be sent to the number or email the bank holds on the account, nowhere else. It's valid for 5 minutes.

Please type the 6-digit code here and I'll finish the change.

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({"entered": "[REDACTED ONE-TIME CODE]"})` → `{"verified": true, "valid_for_minutes": 15, "customer_entered": "[REDACTED ONE-TIME CODE]", "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-09T10:02:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** All set, Priya:

- **Contact channel:** email is now your channel on file - it's what Kestrel will use for messages like your reminder.
- **Travel notice:** Lisbon, until 30 November 2026.
- **Reminder:** Friday 20 November, 09:00 UTC, "book my Lisbon airport transfer" - now going to your email.

Anything else?

_Episode written:_ Conversation on 2026-11-09: Priya asked for email contact, a travel notice, and a 20 Nov reminder to book her Lisbon airport transfer; the customer said Lisbon until 30 Nov 2026 (not verified). Identity verified; travel notice saved; reminder follow-up F-690fd78e set for 2026-11-20 09:00 UTC; email channel stored after code verification. No case/transaction id was given. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | setup: the reminder exists | `[{"trigger_at": "2026-11-20T09:00:00Z", "approval": "none", "status": "pending", "resume": {"note": "Book my Lisbon airport transfer"}}]` |

## epr-s2  ·  session  ·  priya  ·  2026-11-20T08:50:00Z

**Customer:** Please delete everything you remember about me: my preferences and our past conversations.

- `request_memory_erasure({})` → `{"erased_now": "2 remembered facts, 1 past-conversation summaries, 1 other conversation transcripts, 1 reminders with their notes", "this_conversation": "its transcript is deleted when the conversation ends, or once it has been idle for 30 minutes if the customer just closes the chat; nothing more can be stored for the customer in it (a new conversation afterwards starts fresh)", "kept": "dispute  …`

**Assistant:** Done. I've erased everything stored about you:

- **Erased now:** 2 remembered facts, 1 past-conversation summary, 1 other conversation's transcript, and 1 reminder (with its note).
- **This conversation:** its transcript is deleted when the conversation ends - or once it's been idle for 30 minutes if you just close the chat. Nothing more can be stored for you in this conversation; a new conversation afterwards starts fresh.
- **Kestrel still keeps:** your dispute cases, transactions and messages already sent, as bank records with their own legal retention.

One note: if you want a reminder or a contact/travel preference set up from here on, you'd need to do it in a new conversation.

## epr-fire-0905  ·  fire_followups  ·  2026-11-20T09:05:00Z

_outcomes:_ `[]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | the reminder is cancelled by the erasure, whatever its state when the scheduler runs | `[{"trigger_at": "2026-11-20T09:00:00Z", "status": "cancelled", "resume": {}}]` |
| PASS | prospective | nothing is sent to the erased customer from her old reminder | `0 follow_up messages: []` |
| PASS | episodic | no episode is written about her after the request | `0 episodes; purged 0` |
| PASS | working | no follow-up session transcript is created for her | `transcripts with prefix followup-: none` |
| PASS | prospective | the reminder's note is gone from the scheduler | `found nowhere` |

## epr-fire-0910  ·  fire_followups  ·  2026-11-20T09:10:00Z

_outcomes:_ `[]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | a retry cannot send it either | `0 follow_up messages: []` |

## epr-maint  ·  maintenance  ·  2026-11-20T10:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "case_followups_repaired": [], "purged_episodes": [], "deleted_transcripts": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | guard | once the requesting chat has ended (idle), nothing she said is in any memory store (the bank's ledger names a Lisbon bakery and is not memory) | `found nowhere` |
| PASS | working | after maintenance no transcript of hers remains | `0 transcripts: []` |
| PASS | semantic | and no fact | `{}` |
| PASS | episodic | no embedding of an erased episode is left in a vector index | `vector-index rows with no stored item: 0` |
