# adk · adversarial · run 1 · g23-retention-no-tick

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## rnt  ·  session  ·  marco  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Marco here. My cat Pixel chewed my old card, so I just wanted to note that. Nothing else for now.

- `search_policy({"question": "Damaged card replacement \u2014 how does a customer get a new card if their card is damaged?"})` → `{"documents": [{"document": "card-replacement", "score": 0.759, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.631, "text": "# Dispute window\n …`

**Assistant:** Thanks for the heads-up, Marco - sorry about Pixel. Just so you know, I can only store two kinds of notes: your preferred contact channel and a travel notice. A general note like this one doesn't have a place to live, so I haven't saved anything.

On the card itself: for a damaged card, Kestrel blocks it and ships a replacement within 5 business days at no charge - report it through the app or by phone to get that started. One thing to keep in mind: recurring merchants won't be updated automatically, so you'd need to give them the new card number yourself.

Anything you'd like me to do now?

_Episode written:_ Conversation on 2026-11-09: The customer said his cat chewed his old card and he wanted to note it, nothing else (not verified). No case or transaction ID. The assistant did not save a general note; it explained free damaged-card replacement within 5 business days via app/phone and that recurring merchants need the new card number from the customer. No preference or promise stated. Case outcomes: no case touched. Lesson: none

## rnt-41  ·  session  ·  marco  ·  2026-12-20T10:00:00Z

_Resumes session `rnt`._

**Customer:** Hi again. Anything new on my account I should know about?

- `load_memory({"query": "previous conversation account updates"})` → `{"result": "memories=[MemoryEntry(content=Content(\n  parts=[\n    Part(\n      text='Conversation on 2026-11-09: The customer said his cat chewed his old card and he wanted to note it, nothing else (not verified). No case or transaction ID. The assistant did not save a general note; it explained free damaged-card replacement within 5 business days via app/phone and that recurring merchants need t …`
- `get_case_status({})` → `{"cases": []}`
- `list_my_followups({})` → `{"scheduled": []}`

**Assistant:** I'll check what's on your account.
Nothing new - no dispute cases, no scheduled reminders or case follow-ups on your account right now. Your profile also has no contact channel or travel notice on file.

The only earlier conversation I have a record of is from 9 November, when you mentioned your cat chewed your old card - no case was opened and nothing was changed then.

Anything I can help with today, like a transaction to look into or a travel notice to add?

_Episode written:_ Conversation on 2026-12-20: Customer asked if anything new was on the account. The assistant checked memory, case status, and follow-ups, finding no cases, reminders, or follow-ups. No case or transaction IDs. The customer said his cat chewed his old card (not verified). Nothing was promised and no preference was stated. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | a session cannot be resumed past 30 days: the day-0 text is gone from the transcript stores, maintenance or not | `{"chewed": ["adk_sessions.db"]}` |
| **FAIL** | episodic | while the day-0 episode, within its 180 days, is kept | `2 episodes; mentioning 'Pixel': none` |
