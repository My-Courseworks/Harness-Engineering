# langgraph · adversarial · run 2 · g23-retention-no-tick

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## rnt  ·  session  ·  marco  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Marco here. My cat Pixel chewed my old card, so I just wanted to note that. Nothing else for now.

- `search_policy({"question": "What should a customer do if their card is physically damaged (e.g. chewed) and needs a replacement?"})` → `{"documents": [{"document": "card-replacement", "score": 0.741, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.639, "text": "# Dispute window\n …`

**Assistant:** Hi Marco - glad Pixel's okay. Two quick things:

- I can't save general notes like that. The only things I'm able to store are your preferred contact channel and a travel notice - so nothing about the chewed card was recorded.
- If the card is damaged and you need a replacement, you'll need to report it to Kestrel directly (by phone or in the app) - I don't have a tool here to block or reorder a card. Per policy, a replacement ships within 5 business days at no charge, and you'll need to give recurring merchants the new card number yourself, since Kestrel doesn't forward it.

Anything else, just say the word.

_Episode written:_ Conversation on 2026-11-09: The customer said his cat chewed his old card (not verified) and wanted to note it. The assistant said general notes cannot be saved-only preferred contact channel or travel notice-so nothing was recorded. No case/transaction IDs. The assistant advised reporting damage directly to Kestrel; replacements ship within 5 business days at no charge, and recurring merchants need the new number. Case outcomes: no case touched. Lesson: none

## rnt-41  ·  session  ·  marco  ·  2026-12-20T10:00:00Z

_Resumes session `rnt`._

**Customer:** Hi again. Anything new on my account I should know about?

- `get_case_status({})` → `{"cases": []}`
- `list_my_followups({})` → `{"scheduled": []}`
- `find_transactions({})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`

**Assistant:** Nothing new on your account right now: no open dispute cases and nothing scheduled (no reminders or case follow-ups).

Your most recent posted transactions: FitPulse Gym annual renewal, $240.00 on 2026-11-03, and Corner Deli, $12.40 on 2026-11-05.

One thing worth noting: you have no contact channel on file, so if you ever file a dispute, the follow-up will have nowhere to go. Want me to set email, SMS or secure message? Also, if you meant a specific earlier conversation, tell me what it was about and I'll look it up.

_Episode written:_ Conversation on 2026-12-20: Customer asked for any new account updates. Assistant checked case status and follow-ups (none) and transactions: T-2001 FitPulse Gym $240 on 2025-11-03; T-2002 renewal $240 on 2026-11-03; T-2003 Corner Deli $12.40 on 2026-11-05. Assistant noted no contact channel and offered email, SMS, or secure message. No promises made. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | a session cannot be resumed past 30 days: the day-0 text is gone from the transcript stores, maintenance or not | `{"just wanted to note that": ["lg_checkpoints.db-wal"]}` |
| PASS | episodic | while the day-0 episode, within its 180 days, is kept | `2 episodes; mentioning 'Conversation on 2026-11-09': ['E-rnt-1']` |
