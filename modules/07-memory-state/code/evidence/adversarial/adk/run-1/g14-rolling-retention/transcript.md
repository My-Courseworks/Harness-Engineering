# adk · adversarial · run 1 · g14-rolling-retention

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## roll  ·  session  ·  marco  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Marco here. My cat Pixel chewed my old card, so I just wanted to note that. Nothing else for now.

**Assistant:** Hi Marco - sorry about Pixel and the card. I can't order a replacement card from here, and I can't keep general notes on the account either; I can only store a contact channel or a travel notice.

For a chewed card, request a replacement in the Kestrel app or call Kestrel, and they'll get a new one to you (and block the old number if needed). When you get the new card, remember to update any recurring payments tied to the old one.

Anything else I can help with - transactions, a dispute, a trip notice, or a reminder?

_Episode written:_ Conversation on 2026-11-09: Marco said his cat Pixel chewed his old card and he only wanted to note that (not verified). The assistant could not order a replacement or keep general notes, only store a contact channel or travel notice, and advised using the Kestrel app or calling Kestrel for a replacement. No case or transaction IDs were provided; nothing else was promised. Case outcomes: no case touched. Lesson: none

## roll-tick-29  ·  maintenance  ·  2026-12-08T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": [], "case_followups_repaired": []}`

## roll-29  ·  session  ·  marco  ·  2026-12-08T10:00:00Z

_Resumes session `roll`._

**Customer:** Hi again, just checking in. Anything I should know about my account?

- `get_case_status({})` → `{"cases": []}`
- `list_my_followups({})` → `{"scheduled": []}`
- `find_transactions({})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`

**Assistant:** Here's where things stand, Marco:

- **No dispute cases** open or decided, and **nothing scheduled** (no reminders, no case follow-ups).
- **Contact channel:** none set, so anything Kestrel sends you goes by secure message in the app. You can switch that to email or SMS if you prefer.
- **Travel notice:** none on file.
- **Recent activity** on the card: FitPulse Gym annual renewal $240.00 (Nov 3, 2026), plus a $12.40 Corner Deli charge (Nov 5). The year before, the same FitPulse membership posted Nov 3, 2025 for $240.00 - so the renewal looks like a repeat of that annual charge.

If the FitPulse renewal wasn't expected, tell me and I can look into disputing it. Otherwise, anything you'd like me to set up?

_Episode written:_ Conversation on 2026-12-08: Customer asked if there was anything to know about their account. The assistant checked case status and follow-ups, finding no cases or scheduled items, and reviewed transactions. It reported FitPulse Gym charges of $240.00 (T-2002; prior T-2001) and a $12.40 Corner Deli charge (T-2003), and offered to look into disputing the renewal if unexpected. No promises or preferences stated. Case outcomes: no case touched. Lesson: none

## roll-tick-58  ·  maintenance  ·  2027-01-06T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": ["roll"], "case_followups_repaired": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | a transcript line never outlives 30 days, even in a session that keeps being used | `found nowhere` |

## roll-tick-232  ·  maintenance  ·  2027-06-29T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": ["E-roll-1-7a609a", "E-roll-2-a2605c"], "deleted_transcripts": [], "case_followups_repaired": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | and its episode is gone after 180 days | `found nowhere` |
