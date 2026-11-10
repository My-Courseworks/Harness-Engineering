# langgraph · adversarial · run 1 · g14-rolling-retention

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## roll  ·  session  ·  marco  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Marco here. My cat Pixel chewed my old card, so I just wanted to note that. Nothing else for now.

- `search_policy({"question": "damaged card replacement"})` → `{"documents": [{"document": "card-replacement", "score": 0.751, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.632, "text": "# Dispute window\n …`

**Assistant:** Hi Marco - noted, though I should be upfront: I can't store a general note like that. The only things I can keep for you are a contact channel or a travel notice.

If the card itself is damaged and you need a replacement, I don't have a tool to order one - you'd need to contact Kestrel directly (the number on the back of your card or in the app). Per policy, damaged cards are blocked and a replacement ships within 5 business days at no charge, and you'd need to give recurring merchants the new number yourself.

Anything else I can help with?

_Episode written:_ Conversation on 2026-11-09: Marco said his cat Pixel chewed his old card (not verified) and wanted to note it, nothing else for now. The assistant couldn't store a general note or order a replacement, advised contacting Kestrel directly, and cited policy: damaged cards are blocked, replacements ship within 5 business days free, and recurring merchants need the new number. Case outcomes: no case touched. Lesson: none

## roll-tick-29  ·  maintenance  ·  2026-12-08T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "case_followups_repaired": [], "purged_episodes": [], "deleted_transcripts": []}`

## roll-29  ·  session  ·  marco  ·  2026-12-08T10:00:00Z

_Resumes session `roll`._

**Customer:** Hi again, just checking in. Anything I should know about my account?

- `find_transactions({})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`
- `get_case_status({})` → `{"cases": []}`
- `list_my_followups({})` → `{"scheduled": []}`

**Assistant:** Nothing urgent. Quick summary:

- **Dispute cases:** none open.
- **Scheduled reminders/follow-ups:** none.
- **Recent activity:** FitPulse Gym annual membership renewal, $240.00, posted 2026-11-03 (there's also the original $240.00 membership from 2025-11-03), and Corner Deli, $12.40, posted 2026-11-05.

If that FitPulse renewal wasn't expected - an annual charge you meant to cancel, say - tell me and I can look into disputing it.

_Episode written:_ Conversation on 2026-12-08: Customer asked for an account update. Assistant checked transactions, case status, and follow-ups: no open cases or scheduled reminders. Transactions reviewed: T-2001 (FitPulse $240, 2025-11-03), T-2002 (FitPulse renewal $240, 2026-11-03), T-2003 (Corner Deli $12.40, 2026-11-05). Assistant offered to look into disputing the FitPulse renewal if unexpected; no timeframe promised. Case outcomes: no case touched. Lesson: none

## roll-tick-58  ·  maintenance  ·  2027-01-06T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "case_followups_repaired": [], "purged_episodes": [], "deleted_transcripts": ["roll"]}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | a transcript line never outlives 30 days, even in a session that keeps being used | `found nowhere` |

## roll-tick-232  ·  maintenance  ·  2027-06-29T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "case_followups_repaired": [], "purged_episodes": ["E-roll-1-e839a4", "E-roll-2-239711"], "deleted_transcripts": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | and its episode is gone after 180 days | `found nowhere` |
