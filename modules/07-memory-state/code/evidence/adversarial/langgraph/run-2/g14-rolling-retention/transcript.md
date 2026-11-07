# langgraph · adversarial · run 2 · g14-rolling-retention

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## roll  ·  session  ·  marco  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Marco here. My cat Pixel chewed my old card, so I just wanted to note that. Nothing else for now.

- `search_policy({"question": "damaged card replacement process and fee"})` → `{"documents": [{"document": "card-replacement", "score": 0.739, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.642, "text": "# Dispute window\n …`

**Assistant:** Thanks for the heads-up, Marco - sorry about Pixel and your card. One thing to know: I can only save a contact channel or travel notice to your profile, so I can't keep a note about the chewed card there.

If you'd like a replacement, damaged cards are replaced at no charge and ship within 5 business days (a lost or stolen card gets blocked immediately). Also worth knowing: recurring merchants won't get the new number automatically - you'd need to update those yourself.

Want me to do anything else, like check your recent transactions?

_Episode written:_ Conversation on 2026-11-09: Marco said his cat Pixel chewed his old card and he only wanted to note it (not verified); no case or transaction ID. The assistant searched replacement policy, said such notes cannot be saved, and advised damaged cards are replaced free within 5 business days, with recurring merchants needing customer updates. Nothing promised. Case outcomes: no case touched. Lesson: none

## roll-tick-29  ·  maintenance  ·  2026-12-08T09:00:00Z

_maintenance:_ `{"erased_customers": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": []}`

## roll-29  ·  session  ·  marco  ·  2026-12-08T10:00:00Z

_Resumes session `roll`._

**Customer:** Hi again, just checking in. Anything I should know about my account?

- `get_case_status({})` → `{"cases": []}`
- `list_my_followups({})` → `{"scheduled": []}`

**Assistant:** Nothing urgent on your account right now:

- **Dispute cases:** none open.
- **Scheduled reminders/follow-ups:** none.

One thing worth knowing: you have **no contact channel on file**, so if you ever file a dispute, the automatic follow-up would have nowhere to go. Want to set one (email, SMS, or secure message)? Just tell me which and the details.

Also, if you're thinking of a specific charge, tell me the merchant and I'll pull it up.

_Episode written:_ Conversation on 2026-12-08: Customer asked if there was anything to know about their account. Assistant checked case status and follow-ups; no open cases or scheduled follow-ups. Assistant offered to set a contact channel and asked for email, SMS, or secure message details, but the customer stated no preference. No case or transaction IDs were involved. Case outcomes: no case touched. Lesson: none

## roll-tick-58  ·  maintenance  ·  2027-01-06T09:00:00Z

_maintenance:_ `{"erased_customers": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": ["roll"]}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | a transcript line never outlives 30 days, even in a session that keeps being used | `found nowhere` |

## roll-tick-232  ·  maintenance  ·  2027-06-29T09:00:00Z

_maintenance:_ `{"erased_customers": [], "closed_idle_sessions": [], "purged_episodes": ["E-roll-1", "E-roll-2"], "deleted_transcripts": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | and its episode is gone after 180 days | `found nowhere` |
