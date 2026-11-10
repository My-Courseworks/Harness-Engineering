# adk · adversarial · run 2 · g20-erase-pending-reminder

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## epr-s1  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Priya here, card ending 4427, ZIP 94107. I'm in Lisbon until November 30, please email me from now on, and remind me on November 20 to book my Lisbon airport transfer.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `remember_customer_fact({"key": "travel_notice", "value": "Lisbon", "valid_until": "2026-11-30"})` → `{"stored": {"travel_notice": {"value": "Lisbon", "as_of": "2026-11-09T10:00:00Z", "valid_until": "2026-11-30", "expires_at": "2026-12-01T00:00:00Z"}}, "replaced": null}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70100", "expires_in_minutes": 5, "resent": false}`
- `schedule_reminder({"note": "Book my Lisbon airport transfer", "remind_on": "2026-11-20"})` → `{"followup_id": "F-9ea24ee8", "due_utc": "2026-11-20T09:00:00Z", "local_time": "Friday 2026-11-20 09:00 UTC (UTC)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_Ydd09ZnMFFnn1gK2BjmM9442", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_verif …)` → `null`

**Assistant:** A one-time code has been sent by text message to ···0100; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "customer_entered": "[REDACTED ONE-TIME CODE]", "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-09T10:02:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** All set, Priya:

- **Contact channel:** changed to email - the one-time code went to the mobile number on file (···0100) and checked out, so from now on we'll email you.
- **Travel notice:** Lisbon until 2026-11-30 is on file.
- **Reminder:** "Book my Lisbon airport transfer" is scheduled for Friday 2026-11-20 at 09:00 UTC (you didn't give a time, so that's the default). It arrives on the contact channel on file when it's sent - now email.

Anything else I can help with?

_Episode written:_ Conversation on 2026-11-09: Priya asked to switch to email, store a Lisbon travel notice until 2026-11-30, and be reminded on 2026-11-20 to book a Lisbon airport transfer. Identity was verified; contact channel set to email; travel notice stored; reminder followup F-9ea24ee8 scheduled for 2026-11-20 09:00 UTC. No case or transaction ID was provided. Case outcomes: no case touched. Lesson: Next time, ask for the customer’s preferred reminder time before scheduling instead of defaulting to 09:00 UTC.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | setup: the reminder exists | `[{"trigger_at": "2026-11-20T09:00:00Z", "approval": "none", "status": "pending", "resume": {"note": "Book my Lisbon airport transfer"}}]` |

## epr-s2  ·  session  ·  priya  ·  2026-11-20T08:50:00Z

**Customer:** Please delete everything you remember about me: my preferences and our past conversations.

- `request_memory_erasure({})` → `{"erased_now": "2 remembered facts, 1 past-conversation summaries, 1 other conversation transcripts, 1 reminders with their notes", "this_conversation": "its transcript is deleted when the conversation ends, or once it has been idle for 30 minutes if the customer just closes the chat; nothing more can be stored for the customer in it (a new conversation afterwards starts fresh)", "kept": "dispute  …`

**Assistant:** Done. I've erased everything stored about you now:

- **2 remembered facts** (your saved preferences, e.g. contact channel/travel notice)
- **1 past-conversation summary**
- **1 other conversation's transcript**
- **1 reminder**, including its note

What remains:
- This conversation's transcript is deleted when the conversation ends - or, if you just close the chat, once it's been idle for 30 minutes.
- Kestrel still keeps dispute cases, transactions and messages already sent as bank records, under their own legal retention rules.

Also note: nothing more can be stored for you in this conversation - no reminders, no preferences. If you'd like to set up a reminder or contact preference later, start a new conversation and it will begin fresh.

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

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": [], "case_followups_repaired": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | guard | once the requesting chat has ended (idle), nothing she said is in any memory store (the bank's ledger names a Lisbon bakery and is not memory) | `found nowhere` |
| PASS | working | after maintenance no transcript of hers remains | `0 transcripts: []` |
| PASS | semantic | and no fact | `{}` |
| PASS | episodic | no embedding of an erased episode is left in a vector index | `vector-index rows with no stored item: 0` |
