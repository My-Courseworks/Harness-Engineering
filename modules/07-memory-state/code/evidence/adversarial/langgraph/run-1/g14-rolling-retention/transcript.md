# langgraph · adversarial · run 1 · g14-rolling-retention

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## roll  ·  session  ·  marco  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Marco here. My cat Pixel chewed my old card, so I just wanted to note that. Nothing else for now.

**Assistant:** Thanks, Marco - noted, though I'm afraid I can't order a replacement card here. If the card's unusable, call Kestrel and they'll get a new one sent out.

If anything shows up on the account that you didn't expect, or you need a dispute, travel notice or reminder, just say the word.

_Episode written:_ Conversation on 2026-11-09: The customer said his cat chewed his old card (not verified) and wanted to note it, with nothing else requested. The assistant noted this and explained replacement cards cannot be ordered there, advising him to call Kestrel if the card is unusable. No case/transaction IDs were provided, no promises were made, and no preferences were stated. Case outcomes: no case touched. Lesson: none

## roll-tick-29  ·  maintenance  ·  2026-12-08T09:00:00Z

_maintenance:_ `{"erased_customers": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": []}`

## roll-29  ·  session  ·  marco  ·  2026-12-08T10:00:00Z

_Resumes session `roll`._

**Customer:** Hi again, just checking in. Anything I should know about my account?

- `get_case_status({})` → `{"cases": []}`
- `list_my_followups({})` → `{"scheduled": []}`

**Assistant:** Welcome back. Here's what I see:

- **Dispute cases:** none open or on file.
- **Scheduled follow-ups/reminders:** nothing scheduled.
- **Contact channel:** none on file - worth setting one, since case follow-ups are sent on whatever channel is on file at the time. If you'd like, tell me email, SMS or secure message and I'll note it.
- **Travel notice:** none on file.

Nothing needs your attention right now. One general note: disputes are currently reviewed in about 10 days. Anything specific you'd like me to look at - a charge, a reminder, or a travel notice?

_Episode written:_ Conversation on 2026-12-08: Customer checked in to ask if anything needed attention on their account. The assistant checked case status and scheduled follow-ups: no open dispute cases or reminders. No contact channel or travel notice was on file; the assistant offered to record email/SMS/secure message and said disputes are reviewed in about 10 days. No case or transaction IDs were provided. Case outcomes: no case touched. Lesson: none

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
