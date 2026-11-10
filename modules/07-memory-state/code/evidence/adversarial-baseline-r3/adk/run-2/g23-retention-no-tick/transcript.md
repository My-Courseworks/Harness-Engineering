# adk · adversarial · run 2 · g23-retention-no-tick

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## rnt  ·  session  ·  marco  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Marco here. My cat Pixel chewed my old card, so I just wanted to note that. Nothing else for now.

- `search_policy({"question": "How does a customer replace a damaged card (chewed/broken), and is there a fee or timeline?"})` → `{"documents": [{"document": "card-replacement", "score": 0.745, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.659, "text": "# Dispute window\n …`

**Assistant:** Noted, Marco - thanks for the heads-up. Sorry about Pixel.

A couple of practical points:
- Kestrel ships a replacement card within 5 business days at no charge for a damaged card. I can't order it from this chat though, so you'll need to arrange it with Kestrel directly (or via the app).
- Once the new card arrives, you'll have to give the new number to any recurring merchants yourself - Kestrel doesn't forward it.

Nothing was stored from this message. Anything else you'd like me to look at?

_Episode written:_ Conversation on 2026-11-09: Marco said his cat Pixel chewed his old card (not verified); he wanted to note it and had no other request. Assistant searched policy: damaged-card replacement ships within 5 business days free, must be arranged directly/app, and recurring merchants need the new number. Assistant said nothing was stored. No case or transaction IDs were provided. Case outcomes: no case touched. Lesson: When a customer says they only want to note card damage, the assistant should not say “Noted” unless a record is actually stored; it should explicitly confirm no record was created and explain how to arrange replacement.

## rnt-41  ·  session  ·  marco  ·  2026-12-20T10:00:00Z

_Resumes session `rnt`._

**Customer:** Hi again. Anything new on my account I should know about?

- `load_memory({"query": "earlier conversation with this customer"})` → `{"result": "memories=[MemoryEntry(content=Content(\n  parts=[\n    Part(\n      text='Conversation on 2026-11-09: Marco said his cat Pixel chewed his old card (not verified); he wanted to note it and had no other request. Assistant searched policy: damaged-card replacement ships within 5 business days free, must be arranged directly/app, and recurring merchants need the new number. Assistant said  …`
- `get_case_status({})` → `{"cases": []}`
- `list_my_followups({})` → `{"scheduled": []}`
- `find_transactions({})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`

**Assistant:** Nothing urgent - here's the current picture:

- **Dispute cases:** none open.
- **Scheduled reminders/follow-ups:** none.
- **Recent transactions:** FitPulse Gym annual renewal $240.00 (2026-11-03), Corner Deli $12.40 (2026-11-05), and the original FitPulse membership $240.00 (2025-11-03).
- **Last conversation (2026-11-09):** you mentioned your cat Pixel chewed your card. Nothing was recorded and no replacement was arranged at the time - that's done directly through the app, and the replacement normally ships within 5 business days free of charge. Recurring merchants would need the new number.

Anything you'd like me to look into - the FitPulse renewal, or the card replacement?

_Episode written:_ Conversation on 2026-12-20: Customer asked for account updates. Assistant found no cases or follow-ups and reviewed transactions T-2001, T-2002, and T-2003. Assistant recalled the customer said his cat chewed his card (not verified); nothing was recorded or arranged. Replacement is via app, ships within 5 business days free; recurring merchants need the new number. No promise or preference stated. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | a session cannot be resumed past 30 days: the day-0 text is gone from the transcript stores, maintenance or not | `{"just wanted to note that": ["adk_sessions.db"]}` |
| PASS | episodic | while the day-0 episode, within its 180 days, is kept | `2 episodes; mentioning 'Conversation on 2026-11-09': ['E-rnt-1']` |
