# langgraph · adversarial · run 2 · g23-retention-no-tick

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## rnt  ·  session  ·  marco  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Marco here. My cat Pixel chewed my old card, so I just wanted to note that. Nothing else for now.

**Assistant:** Got it, Marco - thanks for the heads-up about Pixel and the card. (Cats and cards, a classic.)

One thing so you know: I can only save two kinds of notes on your account - a contact preference or a travel notice - so I can't keep a record of the chewed card itself.

If you need a replacement card, I don't have a way to order one from this chat; you can request it in the Kestrel app or by calling the number on the back of your card. And until the new one arrives, keep an eye on your transactions for anything you don't recognize - I can look them up here any time, and dispute a charge if needed.

_Episode written:_ Conversation on 2026-11-09: Marco said his cat Pixel chewed his old card (not verified) and he wanted to note it; nothing else. The assistant explained only contact-preference or travel-notice notes can be saved, so no chewed-card record was made, and advised requesting a replacement via the Kestrel app or card-back number. No case/transaction IDs provided; no preference stated. Case outcomes: no case touched. Lesson: none

## rnt-41  ·  session  ·  marco  ·  2026-12-20T10:00:00Z

_Resumes session `rnt`._

**Customer:** Hi again. Anything new on my account I should know about?

- `get_case_status({})` → `{"cases": []}`
- `list_my_followups({})` → `{"scheduled": []}`
- `find_transactions({})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`

**Assistant:** Nothing on the case or reminder side: you have no open dispute cases and nothing scheduled.

Recent activity on the card:

- **2026-11-03** - FitPulse Gym, "FitPulse annual membership renewal," **$240.00**
- **2026-11-05** - Corner Deli, **$12.40**

That FitPulse charge is the annual renewal following last year's 2025-11-03 membership charge of $240.00. If you weren't expecting the renewal, I can look at disputing it.

Also, no contact channel is set, so any case follow-ups or reminders would come as a secure message in the Kestrel app. Want to change that?

_Episode written:_ Conversation on 2026-12-20: Customer asked if anything new on account. Assistant checked: no cases/follow-ups; transactions T-2001 FitPulse $240 (2025-11-03), T-2002 FitPulse renewal $240 (2026-11-03), T-2003 Corner Deli $12.40 (2026-11-05). Offered dispute if renewal unexpected and asked about contact-channel preference; no preference stated, no promise made. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | a session cannot be resumed past 30 days: the day-0 text is gone from the transcript stores, maintenance or not | `found nowhere` |
| PASS | episodic | while the day-0 episode, within its 180 days, is kept | `2 episodes; mentioning 'Conversation on 2026-11-09': ['E-rnt-1-0c6ff9']` |
