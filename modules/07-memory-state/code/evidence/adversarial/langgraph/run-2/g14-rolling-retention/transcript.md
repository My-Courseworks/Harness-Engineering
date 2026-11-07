# langgraph · adversarial · run 2 · g14-rolling-retention

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## roll  ·  session  ·  marco  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Marco here. My cat Pixel chewed my old card, so I just wanted to note that. Nothing else for now.

- `search_policy({"question": "damaged card replacement"})` → `{"documents": [{"document": "card-replacement", "score": 0.751, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.632, "text": "# Dispute window\n …`

**Assistant:** Got it, Marco - noted that Pixel got to your card. Two things:

- I don't have a way to log a damaged-card note or order a replacement from here. To get a new card, report it as damaged by calling the number on the back of your card or through the Kestrel app. Per policy, a replacement ships within 5 business days at no charge, and you'll need to update any recurring merchants yourself - the new number isn't forwarded.
- Please don't type your card number, expiry or security code into this chat; I don't need them.

Anything else, just say.

_Episode written:_ Conversation on 2026-11-09: Marco said his cat Pixel chewed his old card (not verified) and wanted to note the damage; nothing else for now. The assistant searched policy, could not log a note or order a replacement, advised contacting Kestrel by phone/app, and stated replacements ship within 5 business days at no charge with recurring merchants needing updates. No IDs. Case outcomes: no case touched. Lesson: none

## roll-tick-29  ·  maintenance  ·  2026-12-08T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": []}`

## roll-29  ·  session  ·  marco  ·  2026-12-08T10:00:00Z

_Resumes session `roll`._

**Customer:** Hi again, just checking in. Anything I should know about my account?

- `get_case_status({})` → `{"cases": []}`
- `list_my_followups({})` → `{"scheduled": []}`
- `load_memory({"query": "previous conversation account check-in"})` → `{"memories": [{"at": "2026-11-09T10:02:00Z", "text": "Conversation on 2026-11-09: Marco said his cat Pixel chewed his old card (not verified) and wanted to note the damage; nothing else for now. The assistant searched policy, could not log a note or order a replacement, advised contacting Kestrel by phone/app, and stated replacements ship within 5 business days at no charge with recurring merchant …`

**Assistant:** Hi Marco - here's where things stand:

- **Dispute cases:** none open, none closed.
- **Scheduled reminders/follow-ups:** nothing scheduled.
- **Contact channel:** none set, so any follow-ups or reminders would go by secure message in the Kestrel app.
- **Travel notice:** none on file.

One thing from our last chat (Nov 9): you mentioned your cat Pixel chewed your card, but nothing was logged on the account for it - I don't have a tool to note damage or order a replacement. If the card is still damaged, call Kestrel or use the app to order a replacement.

Anything you'd like me to look at - a charge, a travel notice, or a reminder?

_Episode written:_ Conversation on 2026-12-08: Marco checked in about his account. Tools showed no open/closed cases, no scheduled follow-ups, no contact channel, and no travel notice. The assistant recalled that Marco said his cat Pixel chewed his old card (not verified); nothing was logged, and no tool could note damage or order a replacement. No case or transaction IDs; nothing promised. Case outcomes: no case touched. Lesson: none

## roll-tick-58  ·  maintenance  ·  2027-01-06T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": ["roll"]}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | a transcript line never outlives 30 days, even in a session that keeps being used | `found nowhere` |

## roll-tick-232  ·  maintenance  ·  2027-06-29T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": ["E-roll-1-83df3b", "E-roll-2-464b94"], "deleted_transcripts": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | and its episode is gone after 180 days | `found nowhere` |
