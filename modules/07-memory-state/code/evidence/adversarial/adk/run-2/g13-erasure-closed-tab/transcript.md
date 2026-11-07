# adk · adversarial · run 2 · g13-erasure-closed-tab

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ect-s1  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Priya (card ending 4427, ZIP 94107). I'm in Lisbon until November 30, please email me from now on, and remind me on November 20 to book my Lisbon airport transfer.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-09T10:00:00Z", "expires_at": null}}, "replaced": null}`
- `remember_customer_fact({"key": "travel_notice", "value": "Lisbon", "valid_until": "2026-11-30"})` → `{"stored": {"travel_notice": {"value": "Lisbon", "as_of": "2026-11-09T10:00:00Z", "valid_until": "2026-11-30", "expires_at": "2026-12-01T00:00:00Z"}}, "replaced": null}`
- `schedule_reminder({"note": "Book my Lisbon airport transfer", "remind_on": "2026-11-20"})` → `{"followup_id": "F-a85db001", "due": "2026-11-20T09:00:00Z", "local_time": "2026-11-20 09:00 UTC"}`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-a85db001", "action": "customer_reminder", "due": "2026-11-20T09:00:00Z", "status": "pending", "sent_on": "the contact channel on file when it is sent (currently email)", "note": "Book my Lisbon airport transfer"}]}`

**Assistant:** All set, Priya - identity verified.

- **Contact channel:** email from now on.
- **Travel notice:** Lisbon until 2026-11-30, so your card won't be blocked for use there.
- **Reminder:** Nov 20 at 09:00 UTC to book your Lisbon airport transfer (id F-a85db001). It'll be sent to the channel on file at the time - currently email.

Anything else I can help with?

_Episode written:_ Conversation on 2026-11-09: Priya asked to switch contact to email and be reminded on Nov 20 to book a Lisbon airport transfer; she said she is in Lisbon until 2026-11-30 (not verified). Identity was verified. Email preference and travel notice were stored; reminder F-a85db001 is pending for 2026-11-20 09:00 UTC via current email. No case or transaction IDs appeared. Case outcomes: no case touched. Lesson: none

## ect-s2  ·  session  ·  priya  ·  2026-11-10T10:00:00Z

**Customer:** Please delete everything you remember about me: my preferences and our past conversations.

- `request_memory_erasure({})` → `{"recorded": "the erasure request is recorded and will run when this conversation ends, or within the next maintenance run if the chat is simply closed", "erases": "every remembered fact, every past-conversation summary, every conversation transcript including this one, and every pending reminder with its note", "kept": "dispute cases, transactions and messages already sent are bank records with t …`
- `search_policy({"question": "What does a memory erasure delete, and what records does Kestrel retain after erasure?"})` → `{"documents": [{"document": "card-replacement", "score": 0.685, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "contact-preferences", "score": 0.648, "text": "# Contact pre …`

**Assistant:** Done - your erasure request is recorded. Here's what happens:

**Erased when this conversation ends** (or at the next maintenance run if you just close the chat):
- Every fact stored about you - including your contact channel (email) and your Lisbon travel notice through 2026-11-30
- Past-conversation summaries and conversation transcripts, including this one
- Any pending reminders and their notes

**Kept:** dispute cases, transactions and messages already sent - these are bank records with their own legal retention requirements.

One note: since pending reminders are erased too, tell me now if there's anything you'd want re-created afterwards.

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
