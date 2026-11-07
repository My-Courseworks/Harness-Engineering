# adk · adversarial · run 2 · g23-retention-no-tick

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## rnt  ·  session  ·  marco  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Marco here. My cat Pixel chewed my old card, so I just wanted to note that. Nothing else for now.

**Assistant:** Sorry to hear that, Marco - hopefully Pixel's fine. Noted.

I can't order a replacement card from this chat, so if the card's damaged and you need a new one, contact Kestrel support directly. Anything else I can help with - transactions, disputes, travel notices, reminders - just say.

_Episode written:_ Conversation on 2026-11-09: The customer said his cat Pixel chewed his old card and he only wanted to note it (not verified). The assistant acknowledged and said replacement cards can't be ordered in chat; he should contact Kestrel support directly if he needs a new one. No case or transaction IDs. Case outcomes: no case touched. Lesson: none

## rnt-41  ·  session  ·  marco  ·  2026-12-20T10:00:00Z

_Resumes session `rnt`._

**Customer:** Hi again. Anything new on my account I should know about?

- `load_memory({"query": "recent conversation, account updates, dispute"})` → `{"result": "memories=[MemoryEntry(content=Content(\n  parts=[\n    Part(\n      text=\"Conversation on 2026-11-09: The customer said his cat Pixel chewed his old card and he only wanted to note it (not verified). The assistant acknowledged and said replacement cards can't be ordered in chat; he should contact Kestrel support directly if he needs a new one. No case or transaction IDs. Case outcomes …`
- `get_case_status({})` → `{"cases": []}`

**Assistant:** Hi - I checked. Nothing new since we last spoke:

- **Dispute cases:** none open, none recent.
- **Travel notice:** none on file.
- **Contact channel:** none set, so any follow-ups or reminders would arrive as a secure message in the Kestrel app.

Last time you mentioned your cat chewed your old card and you just wanted it noted - no card replacement can be arranged in chat, so you'd need to contact Kestrel support directly for that.

Want me to look through your recent transactions, or set up a travel notice or reminder while you're here?

_Episode written:_ Conversation on 2026-12-20: Customer asked if anything new on account. Assistant checked: no open/recent dispute cases, no travel notice, no contact channel; no case or transaction IDs. Assistant recalled customer said cat Pixel chewed old card and only wanted it noted (not verified); replacement not available in chat, contact Kestrel support. No promises. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | a session cannot be resumed past 30 days: the day-0 text is gone from the transcript stores, maintenance or not | `found nowhere` |
| PASS | episodic | while the day-0 episode, within its 180 days, is kept | `2 episodes; mentioning 'Conversation on 2026-11-09': ['E-rnt-1-6ac67a']` |
