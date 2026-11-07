# adk · adversarial · run 1 · g14-rolling-retention

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## roll  ·  session  ·  marco  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Marco here. My cat Pixel chewed my old card, so I just wanted to note that. Nothing else for now.

**Assistant:** Hi Marco — sorry to hear Pixel got to the card. Just so you know, I can't record a note like that on your account, but nothing needs to be done on my side from that message alone.

If the card itself is damaged and you need a replacement, or you spot any transactions you don't recognize (a chewed card can still have its number used), tell me and I'll help — for a replacement you'd need to call Kestrel since I can't order one here.

_Episode written:_ Conversation on 2026-11-09: Marco said his cat Pixel chewed his old card (not verified) and wanted that noted; he said nothing else was needed. The assistant said it could not record such a note, advised no action was needed, and offered help if the card was damaged or unrecognized transactions appeared, noting replacements require calling Kestrel. No case or transaction ID was provided. Case outcomes: no case touched. Lesson: none

## roll-tick-29  ·  maintenance  ·  2026-12-08T09:00:00Z

_maintenance:_ `{"closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": []}`

## roll-29  ·  session  ·  marco  ·  2026-12-08T10:00:00Z

_Resumes session `roll`._

**Customer:** Hi again, just checking in. Anything I should know about my account?

- `get_case_status({})` → `{"cases": []}`
- `list_my_followups({})` → `{"scheduled": []}`
- `load_memory({"query": "recent conversation, account notes, pending requests"})` → `{"result": "memories=[MemoryEntry(content=Content(\n  parts=[\n    Part(\n      text='Conversation on 2026-11-09: Marco said his cat Pixel chewed his old card (not verified) and wanted that noted; he said nothing else was needed. The assistant said it could not record such a note, advised no action was needed, and offered help if the card was damaged or unrecognized transactions appeared, noting r …`

**Assistant:** Hi Marco — I checked, and there's nothing pending right now:

- **Dispute cases:** none open.
- **Scheduled reminders/follow-ups:** none.

Two small things worth knowing:

- **No contact channel is on file** for you, so any case follow-up or reminder would have nowhere to go. If you'd like, tell me email, SMS or secure message and I'll set it.
- I have a note from our conversation on 9 Nov about your cat Pixel chewing your card — nothing was filed then and no action was needed. If the card is actually damaged, replacements are handled by calling Kestrel.

Anything else I can look into?

_Episode written:_ Conversation on 2026-12-08: The customer asked for an account update. Assistant checked case status and follow-ups: no cases or scheduled items. No case or transaction IDs. Assistant said no contact channel is on file and offered to set email/SMS/secure message if provided. The customer previously said his cat chewed his card (not verified) and wanted it noted; no action was taken. Case outcomes: no case touched. Lesson: none

## roll-tick-58  ·  maintenance  ·  2027-01-06T09:00:00Z

_maintenance:_ `{"closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": []}`

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | a transcript line never outlives 30 days, even in a session that keeps being used | `{"Pixel": ["adk_sessions.db"]}` |

## roll-tick-232  ·  maintenance  ·  2027-06-29T09:00:00Z

_maintenance:_ `{"closed_idle_sessions": [], "purged_episodes": ["E-roll-1", "E-roll-2"], "deleted_transcripts": ["roll"]}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | and its episode is gone after 180 days | `found nowhere` |
