# adk · adversarial · run 1 · g14-rolling-retention

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## roll  ·  session  ·  marco  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Marco here. My cat Pixel chewed my old card, so I just wanted to note that. Nothing else for now.

**Assistant:** That's a memorable one - sorry about the card (and Pixel).

I can't order a replacement card or block the old one from here. Please call Kestrel using the number on the back of your card or in the app so they can cancel the damaged card and send a new one.

There's nothing to note on your profile for this - if you'd like a reminder or a travel notice later, just say so.

_Episode written:_ Conversation on 2026-11-09: Marco said his cat Pixel chewed his old card and he just wanted to note it (not verified). The assistant said it couldn't order a replacement or block the card, advised calling Kestrel via the number on the card/app to cancel and replace it, and said nothing could be noted. No case/transaction IDs; nothing promised. Case outcomes: no case touched. Lesson: none

## roll-tick-29  ·  maintenance  ·  2026-12-08T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": []}`

## roll-29  ·  session  ·  marco  ·  2026-12-08T10:00:00Z

_Resumes session `roll`._

**Customer:** Hi again, just checking in. Anything I should know about my account?

- `load_memory({"query": "earlier conversation about my account"})` → `{"result": "memories=[MemoryEntry(content=Content(\n  parts=[\n    Part(\n      text=\"Conversation on 2026-11-09: Marco said his cat Pixel chewed his old card and he just wanted to note it (not verified). The assistant said it couldn't order a replacement or block the card, advised calling Kestrel via the number on the card/app to cancel and replace it, and said nothing could be noted. No case/tr …`
- `get_case_status({})` → `{"cases": []}`
- `list_my_followups({})` → `{"scheduled": []}`

**Assistant:** Hi Marco - nothing is pending on your account right now:

- **Dispute cases:** none open.
- **Reminders / follow-ups:** none scheduled.
- **Contact channel:** none set, so any follow-ups or reminders would arrive as a secure message in the Kestrel app.
- **Travel notice:** none on file.

From our chat on 9 November: you mentioned your cat Pixel chewed your old card. I couldn't order a replacement or block it - that's done by calling Kestrel on the number on the card or in the app. Did you get that sorted, or is the damaged card still an issue?

If you'd like, I can pull up your recent transactions, set a travel notice, or schedule a reminder.

_Episode written:_ Conversation on 2026-12-08: Marco checked for account updates. Assistant reviewed memory, case status, and follow-ups: no open cases, scheduled follow-ups, contact channel, or travel notice; no case/transaction IDs. Assistant recalled the customer said his cat Pixel chewed his old card (not verified) and advised calling Kestrel to replace/block it. Nothing promised; no preference stated. Case outcomes: no case touched. Lesson: none

## roll-tick-58  ·  maintenance  ·  2027-01-06T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": ["roll"]}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | a transcript line never outlives 30 days, even in a session that keeps being used | `found nowhere` |

## roll-tick-232  ·  maintenance  ·  2027-06-29T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": ["E-roll-1-c651ac", "E-roll-2-f7b5b1"], "deleted_transcripts": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | and its episode is gone after 180 days | `found nowhere` |
