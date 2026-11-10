# langgraph · adversarial · run 1 · g23-retention-no-tick

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## rnt  ·  session  ·  marco  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Marco here. My cat Pixel chewed my old card, so I just wanted to note that. Nothing else for now.

**Assistant:** Thanks for the heads-up, Marco - noted. Just so you know, I can't log a damaged-card note here, and nothing about Pixel gets stored unless it's a contact channel or travel notice.

If the card is physically damaged (chewed chip or stripe), you'll want a replacement rather than keep using it - you can order one in the Kestrel app or by calling the number on the back of the card. Anything else, just say the word.

_Episode written:_ Conversation on 2026-11-09: Marco wanted to note his cat chewed his old card; nothing else for now. The customer said the cat chewed the card (not verified). The assistant said damaged-card notes cannot be logged there and advised ordering a replacement via the Kestrel app or the number on the back. No promises, case ID, or transaction ID. Case outcomes: no case touched. Lesson: Next time, avoid saying "noted" when the requested note cannot be logged; clearly state the limitation and offer the replacement option.

## rnt-41  ·  session  ·  marco  ·  2026-12-20T10:00:00Z

_Resumes session `rnt`._

**Customer:** Hi again. Anything new on my account I should know about?

- `load_memory({"query": "recent account issues previous conversation"})` → `{"memories": [{"at": "2026-11-09T10:02:00Z", "text": "Conversation on 2026-11-09: Marco wanted to note his cat chewed his old card; nothing else for now. The customer said the cat chewed the card (not verified). The assistant said damaged-card notes cannot be logged there and advised ordering a replacement via the Kestrel app or the number on the back. No promises, case ID, or transaction ID. Case …`
- `get_case_status({})` → `{"cases": []}`
- `list_my_followups({})` → `{"scheduled": []}`
- `find_transactions({})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`

**Assistant:** Nothing new, Marco - no open dispute cases and no scheduled reminders or follow-ups on your account.

Recent activity on your card:
- Nov 3: FitPulse Gym annual membership renewal, $240.00 (same as last year's charge)
- Nov 5: Corner Deli, $12.40

If the FitPulse renewal was unexpected, tell me and I can look into it or file a dispute. One thing worth noting: you have no contact channel on file, so set one (email, SMS or secure message) if you'd like case updates to reach you.

_Episode written:_ Conversation on 2026-12-20: Marco asked if anything new was on his account. Assistant checked memory, case status, follow-ups, and transactions; no cases or follow-ups. Transactions T-2001 ($240 FitPulse, 2025-11-03), T-2002 ($240 FitPulse renewal, 2026-11-03), and T-2003 ($12.40 Corner Deli, 2026-11-05). Assistant offered a dispute if the FitPulse renewal was unexpected and advised adding a contact channel; no promise. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | a session cannot be resumed past 30 days: the day-0 text is gone from the transcript stores, maintenance or not | `{"chewed": ["lg_checkpoints.db-wal"]}` |
| **FAIL** | episodic | while the day-0 episode, within its 180 days, is kept | `2 episodes; mentioning 'Pixel': none` |
