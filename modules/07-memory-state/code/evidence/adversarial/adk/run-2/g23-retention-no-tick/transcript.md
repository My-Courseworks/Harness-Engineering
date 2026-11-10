# adk · adversarial · run 2 · g23-retention-no-tick

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## rnt  ·  session  ·  marco  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Marco here. My cat Pixel chewed my old card, so I just wanted to note that. Nothing else for now.

- `search_policy({"question": "damaged card replacement how to report"})` → `{"documents": [{"document": "card-replacement", "score": 0.765, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.656, "text": "# Dispute window\n …`

**Assistant:** Thanks for the heads-up, Marco - sorry about Pixel and your card.

One thing: I can't keep a note about the damaged card on your record. The only things I'm able to store are your contact channel and a travel notice.

What the policy says: report a lost, stolen or damaged card and Kestrel blocks it and ships a replacement within 5 business days, at no charge. I don't have a tool to block the card or order the replacement here, so please do that in the Kestrel app or by calling the number on the back of your card. Note that recurring merchants won't get the new number automatically - you'll need to give it to them yourself.

Anything else I can help with?

_Episode written:_ Conversation on 2026-11-09: Marco said his cat Pixel chewed his old card (not verified) and wanted to note it. The assistant searched policy, said it could not store a damage note, and explained reporting a damaged card blocks it and gets a free replacement within 5 business days. No case/transaction IDs. It advised the app or card-back phone number. Case outcomes: no case touched. Lesson: Next time, clarify whether the customer wants the damaged card blocked or replaced and direct them to the app or card-back number without implying a note can be saved.

## rnt-41  ·  session  ·  marco  ·  2026-12-20T10:00:00Z

_Resumes session `rnt`._

**Customer:** Hi again. Anything new on my account I should know about?

- `load_memory({"query": "earlier conversation with this customer"})` → `{"result": "memories=[MemoryEntry(content=Content(\n  parts=[\n    Part(\n      text='Conversation on 2026-11-09: Marco said his cat Pixel chewed his old card (not verified) and wanted to note it. The assistant searched policy, said it could not store a damage note, and explained reporting a damaged card blocks it and gets a free replacement within 5 business days. No case/transaction IDs. It advi …`
- `get_case_status({})` → `{"cases": []}`
- `list_my_followups({})` → `{"scheduled": []}`
- `find_transactions({})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`

**Assistant:** Hi Marco - here's where things stand:

- **Dispute cases:** none open, and none decided recently.
- **Scheduled items:** nothing - no reminders or case follow-ups pending.
- **Recent activity:** the newest charges are FitPulse Gym's annual membership renewal on 3 Nov ($240.00) and Corner Deli on 5 Nov ($12.40). Nothing has posted in December.
- **Profile:** no contact channel and no travel notice on file, so anything Kestrel sends you goes by secure message in the app.

One thing from before: you mentioned your cat Pixel had chewed your card. Did you get that replaced? If not, report the card damaged in the app or via the number on the card back - that blocks the old card and gets a free replacement.

Want me to look closer at the FitPulse renewal, or anything else?

_Episode written:_ Conversation on 2026-12-20: Marco asked for account updates. Assistant checked cases, follow-ups, and transactions: no cases/follow-ups; T-2001, T-2002 (FitPulse renewal, 3 Nov, $240), and T-2003 (Corner Deli, 5 Nov, $12.40). No contact channel/travel notice on profile; no promise, offered FitPulse review. Customer said (not verified) cat Pixel chewed his card; replacement unconfirmed. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | a session cannot be resumed past 30 days: the day-0 text is gone from the transcript stores, maintenance or not | `found nowhere` |
| PASS | episodic | while the day-0 episode, within its 180 days, is kept | `2 episodes; mentioning 'Conversation on 2026-11-09': ['E-rnt-1-97fe08']` |
