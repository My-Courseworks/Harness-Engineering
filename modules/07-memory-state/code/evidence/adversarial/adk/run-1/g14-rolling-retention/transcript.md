# adk · adversarial · run 1 · g14-rolling-retention

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## roll  ·  session  ·  marco  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Marco here. My cat Pixel chewed my old card, so I just wanted to note that. Nothing else for now.

**Assistant:** Thanks for the heads-up, Marco. Sorry about Pixel and your card.

I can't order a replacement card from here, so if the card is damaged and you need a new one, contact Kestrel (or the number on the back of the card) to request a replacement.

If anything else comes up - a transaction to dispute, a travel notice, or a reminder - just tell me.

_Episode written:_ Conversation on 2026-11-09: The customer said his cat chewed his old card (not verified) and wanted to note it, with nothing else. The assistant explained it could not order a replacement and advised contacting Kestrel or the number on the card to request one; no case or transaction IDs and no promises were given. No preference was stated. Case outcomes: no case touched. Lesson: none

## roll-tick-29  ·  maintenance  ·  2026-12-08T09:00:00Z

_maintenance:_ `{"erased_customers": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": []}`

## roll-29  ·  session  ·  marco  ·  2026-12-08T10:00:00Z

_Resumes session `roll`._

**Customer:** Hi again, just checking in. Anything I should know about my account?

- `load_memory({"query": "earlier conversation about my account"})` → `{"result": "memories=[MemoryEntry(content=Content(\n  parts=[\n    Part(\n      text='Conversation on 2026-11-09: The customer said his cat chewed his old card (not verified) and wanted to note it, with nothing else. The assistant explained it could not order a replacement and advised contacting Kestrel or the number on the card to request one; no case or transaction IDs and no promises were given …`
- `list_my_followups({})` → `{"scheduled": []}`
- `get_case_status({})` → `{"cases": []}`

**Assistant:** Nothing needs your attention right now: no open dispute cases, and nothing scheduled (no reminders or follow-ups).

A couple of things on file:
- Contact channel: none set - worth choosing one (email, SMS or secure message) so any case updates or reminders can reach you.
- Travel notice: none on file.

I also have a note from our chat on 9 November about your cat chewing your card - that was advice only, no case or request was opened. If you still need a replacement card, you'd need to contact Kestrel directly or call the number on the card.

Anything you'd like me to set up?

_Episode written:_ Conversation on 2026-12-08: Customer asked for account updates. Assistant found no open cases or follow-ups and no contact channel or travel notice. The customer said his cat chewed his old card on 2026-11-09 (not verified); no replacement was ordered. No case/transaction IDs, promises, or preferences. Assistant advised contacting Kestrel or the card number if still needed. Case outcomes: no case touched. Lesson: none

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
