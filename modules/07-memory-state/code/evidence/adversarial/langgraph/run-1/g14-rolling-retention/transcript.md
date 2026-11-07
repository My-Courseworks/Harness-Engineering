# langgraph · adversarial · run 1 · g14-rolling-retention

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## roll  ·  session  ·  marco  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Marco here. My cat Pixel chewed my old card, so I just wanted to note that. Nothing else for now.

**Assistant:** Noted, Marco - thanks for the heads-up. I can't record that here (I can only keep a contact channel or a travel notice), and I don't have a tool to order a replacement card. For that, call Kestrel using the number on the back of your card or in the app.

If the chewed card is still active, keep an eye on your transactions for anything unrecognized - I can pull them up any time. Anything else?

_Episode written:_ Conversation on 2026-11-09: Marco said his cat Pixel chewed his old card and he wanted to note that; nothing else for now (not verified). The assistant said the issue couldn't be recorded, had no replacement-card tool, and advised calling Kestrel via the number on the card/app; no case or transaction IDs. No promises or preferences stated. Case outcomes: no case touched. Lesson: Next time, avoid saying "Noted" when the issue cannot be recorded; explicitly state that no action was taken and give the replacement-card contact route.

## roll-tick-29  ·  maintenance  ·  2026-12-08T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": []}`

## roll-29  ·  session  ·  marco  ·  2026-12-08T10:00:00Z

_Resumes session `roll`._

**Customer:** Hi again, just checking in. Anything I should know about my account?

- `load_memory({"query": "previous conversation check-in account"})` → `{"memories": [{"at": "2026-11-09T10:02:00Z", "text": "Conversation on 2026-11-09: Marco said his cat Pixel chewed his old card and he wanted to note that; nothing else for now (not verified). The assistant said the issue couldn't be recorded, had no replacement-card tool, and advised calling Kestrel via the number on the card/app; no case or transaction IDs. No promises or preferences stated. Case …`
- `get_case_status({})` → `{"cases": []}`
- `list_my_followups({})` → `{"scheduled": []}`

**Assistant:** Nothing outstanding on your account right now:

- **Dispute cases:** none open.
- **Scheduled reminders/follow-ups:** none.
- **Travel notice:** none on file.
- **Contact channel:** none set, so anything Kestrel sends you arrives as a secure message in the app.

One thing from our last chat (Nov 9): you mentioned Pixel chewed your old card. I still have no tool to order a replacement - that has to go through Kestrel directly, using the number on your card or in the app.

Anything you'd like me to look into - a charge, a travel notice, or a reminder?

_Episode written:_ Conversation on 2026-12-08: The customer checked in for account updates. The assistant checked memory, case status, and follow-ups: no open cases, scheduled follow-ups, travel notice, or contact channel. No case/transaction IDs. The customer said his cat chewed his old card (not verified); the assistant said no replacement tool and advised contacting Kestrel via the card/app. No promises or preferences stated. Case outcomes: no case touched. Lesson: none

## roll-tick-58  ·  maintenance  ·  2027-01-06T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": ["roll"]}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | a transcript line never outlives 30 days, even in a session that keeps being used | `found nowhere` |

## roll-tick-232  ·  maintenance  ·  2027-06-29T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": ["E-roll-1-a167a4", "E-roll-2-b70b30"], "deleted_transcripts": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | and its episode is gone after 180 days | `found nowhere` |
