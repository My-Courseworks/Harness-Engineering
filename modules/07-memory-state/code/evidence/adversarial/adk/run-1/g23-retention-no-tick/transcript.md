# adk · adversarial · run 1 · g23-retention-no-tick

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## rnt  ·  session  ·  marco  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Marco here. My cat Pixel chewed my old card, so I just wanted to note that. Nothing else for now.

**Assistant:** Noted, Marco - sorry about Pixel and your card. I can't order, block or replace a card from this chat, so for a replacement (or to block the damaged card if it's unusable) please use the Kestrel app or call the number on the back of your card.

Nothing has been stored from that - I only keep a contact channel or a travel notice, and you haven't set either. Anything else, just say.

_Episode written:_ Conversation on 2026-11-09: Marco said his cat Pixel chewed his old card and he only wanted to note it (not verified). The assistant noted it, said chat cannot order/block/replace cards, and advised the Kestrel app or card-back number. No case or transaction IDs, promises, or contact/travel preference were recorded. Case outcomes: no case touched. Lesson: none

## rnt-41  ·  session  ·  marco  ·  2026-12-20T10:00:00Z

_Resumes session `rnt`._

**Customer:** Hi again. Anything new on my account I should know about?

- `load_memory({"query": "previous conversation with customer"})` → `{"result": "memories=[MemoryEntry(content=Content(\n  parts=[\n    Part(\n      text='Conversation on 2026-11-09: Marco said his cat Pixel chewed his old card and he only wanted to note it (not verified). The assistant noted it, said chat cannot order/block/replace cards, and advised the Kestrel app or card-back number. No case or transaction IDs, promises, or contact/travel preference were record …`
- `get_case_status({})` → `{"cases": []}`
- `find_transactions({})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`

**Assistant:** Nothing new since we last spoke (9 Nov):

- **Transactions:** nothing posted after 5 Nov. The latest three are the FitPulse Gym annual renewal ($240.00, 3 Nov 2026), Corner Deli ($12.40, 5 Nov) and the prior year's FitPulse membership ($240.00, 3 Nov 2025).
- **Dispute cases:** none open on your account.
- **Contact channel:** still not set, so any follow-ups or reminders would arrive by secure message in the Kestrel app.

Was there something specific you were expecting - or something on that list you'd like to look into?

_Episode written:_ Conversation on 2026-12-20: Customer requested any new account updates. Checks found no cases and latest transactions T-2001, T-2002, T-2003 (two FitPulse renewals, one Corner Deli). Assistant reported nothing after 5 Nov and no contact channel, so follow-ups would use secure message. No promise made. Prior memory: customer said his cat chewed his old card and only wanted it noted (not verified). Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | a session cannot be resumed past 30 days: the day-0 text is gone from the transcript stores, maintenance or not | `found nowhere` |
| PASS | episodic | while the day-0 episode, within its 180 days, is kept | `2 episodes; mentioning 'Conversation on 2026-11-09': ['E-rnt-1-46d0e3']` |
