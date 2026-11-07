# adk · adversarial · run 1 · g23-retention-no-tick

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## rnt  ·  session  ·  marco  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Marco here. My cat Pixel chewed my old card, so I just wanted to note that. Nothing else for now.

**Assistant:** Hi Marco - got it. Just so you know, I don't have a way to log a damaged card here, and I can't keep a note about it. To get it replaced, call Kestrel using the number on the back of your card (or on kestrelcard.com).

Nothing else needed - happy to help with transactions, disputes or a travel notice whenever you want.

_Episode written:_ Conversation on 2026-11-09: Marco said his cat Pixel chewed his old card (not verified) and wanted to note it, with nothing else needed. The assistant said damaged cards cannot be logged or noted and advised calling Kestrel using the number on the back of the card or kestrelcard.com to get it replaced. No case or transaction IDs, promises, or preferences were stated. Case outcomes: no case touched. Lesson: none

## rnt-41  ·  session  ·  marco  ·  2026-12-20T10:00:00Z

_Resumes session `rnt`._

**Customer:** Hi again. Anything new on my account I should know about?

- `load_memory({"query": "earlier conversation context"})` → `{"result": "memories=[MemoryEntry(content=Content(\n  parts=[\n    Part(\n      text='Conversation on 2026-11-09: Marco said his cat Pixel chewed his old card (not verified) and wanted to note it, with nothing else needed. The assistant said damaged cards cannot be logged or noted and advised calling Kestrel using the number on the back of the card or kestrelcard.com to get it replaced. No case or …`
- `find_transactions({})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`
- `get_case_status({})` → `{"cases": []}`
- `list_my_followups({})` → `{"scheduled": []}`

**Assistant:** Hi again, Marco. Here's what's on your account:

**Recent transactions**
- **Nov 3, 2026** - FitPulse Gym, "FitPulse annual membership renewal," **$240.00** (last year's same charge posted Nov 3, 2025)
- **Nov 5, 2026** - Corner Deli, **$12.40**

**Disputes:** you have no open cases.
**Scheduled reminders/follow-ups:** none.

Nothing else new. One note from our last conversation (Nov 9): you mentioned your cat chewed your card - if it's still damaged, Kestrel can't log that here, so call the number on the back of your card or visit kestrelcard.com to get a replacement ordered.

Was there anything specific you wanted to ask about - the FitPulse renewal, for instance?

_Episode written:_ Conversation on 2026-12-20: Marco asked for any new account information. Assistant checked memory, transactions, case status, and follow-ups: found FitPulse charges T-2001 ($240, 2025-11-03) and T-2002 ($240 renewal, 2026-11-03), Corner Deli T-2003 ($12.40, 2026-11-05), no cases, and no follow-ups. The customer said his cat chewed his card (not verified); only Kestrel replacement advice was given. No promises or preferences. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | a session cannot be resumed past 30 days: the day-0 text is gone from the transcript stores, maintenance or not | `found nowhere` |
| PASS | episodic | while the day-0 episode, within its 180 days, is kept | `2 episodes; mentioning 'Conversation on 2026-11-09': ['E-rnt-1-a9b9fb']` |
