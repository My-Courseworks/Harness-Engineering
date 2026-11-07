# adk · adversarial · run 1 · g13-erasure-closed-tab

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ect-s1  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Priya (card ending 4427, ZIP 94107). I'm in Lisbon until November 30, please email me from now on, and remind me on November 20 to book my Lisbon airport transfer.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-09T10:00:00Z", "expires_at": null}}, "replaced": null}`
- `remember_customer_fact({"key": "travel_notice", "value": "Lisbon", "valid_until": "2026-11-30"})` → `{"stored": {"travel_notice": {"value": "Lisbon", "as_of": "2026-11-09T10:00:00Z", "valid_until": "2026-11-30", "expires_at": "2026-12-01T00:00:00Z"}}, "replaced": null}`
- `schedule_reminder({"note": "Book my Lisbon airport transfer", "remind_on": "2026-11-20"})` → `{"followup_id": "F-7ac05bb6", "due": "2026-11-20T09:00:00Z", "local_time": "2026-11-20 09:00 UTC"}`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-7ac05bb6", "action": "customer_reminder", "due": "2026-11-20T09:00:00Z", "status": "pending", "sent_on": "the contact channel on file when it is sent (currently email)", "note": "Book my Lisbon airport transfer"}]}`

**Assistant:** All set, Priya - you're verified.

- **Contact channel:** email from now on.
- **Travel notice:** Lisbon until 2026-11-30.
- **Reminder:** Nov 20 at 09:00 UTC - "Book my Lisbon airport transfer." It'll arrive by email (whatever channel is on file when it's sent).

Anything else?

_Episode written:_ Conversation on 2026-11-09: The customer said she is in Lisbon until 2026-11-30 (not verified); requested email contact and a Nov 20 reminder to book her Lisbon airport transfer. Identity verified. Email preference and travel notice stored; reminder F-7ac05bb6 scheduled for 2026-11-20 09:00 UTC, to be sent by email. No case/transaction ID present. Case outcomes: no case touched. Lesson: none

## ect-s2  ·  session  ·  priya  ·  2026-11-10T10:00:00Z

**Customer:** Please delete everything you remember about me: my preferences and our past conversations.

- `request_memory_erasure({})` → `{"recorded": "the erasure request is recorded and will run when this conversation ends, or within the next maintenance run if the chat is simply closed", "erases": "every remembered fact, every past-conversation summary, every conversation transcript including this one, and every pending reminder with its note", "kept": "dispute cases, transactions and messages already sent are bank records with t …`

**Assistant:** Your erasure request is recorded. Here's what it covers:

**Erased:** every remembered fact (like your contact channel and travel notice), every past-conversation summary, every conversation transcript including this one, and any pending reminders along with their notes.

**Kept:** dispute cases, transactions and messages already sent - those are bank records with their own legal retention rules.

It runs when this conversation ends, or by the next maintenance run if you just close the chat. Nothing else you need to do.

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
