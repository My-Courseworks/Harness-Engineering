# langgraph · adversarial · run 2 · g23-retention-no-tick

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## rnt  ·  session  ·  marco  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Marco here. My cat Pixel chewed my old card, so I just wanted to note that. Nothing else for now.

**Assistant:** Hi Marco - sorry to hear about Pixel and the card! Noted on my side, though I can't do anything about a damaged card here: for a replacement, please call Kestrel or use the card-management options in the Kestrel app.

Anything else I can help with - transactions, a dispute, a travel notice, or how you'd like to be contacted - just say the word.

_Episode written:_ Conversation on 2026-11-09: The customer said his cat Pixel chewed his old card (not verified) and wanted to note it, nothing else. The assistant noted it, said it couldn't handle damaged cards there, and advised calling Kestrel or using the Kestrel app for a replacement. No case or transaction IDs, promises, or preferences were stated. Case outcomes: no case touched. Lesson: none

## rnt-41  ·  session  ·  marco  ·  2026-12-20T10:00:00Z

_Resumes session `rnt`._

**Customer:** Hi again. Anything new on my account I should know about?

- `get_case_status({})` → `{"cases": []}`
- `list_my_followups({})` → `{"scheduled": []}`
- `load_memory({"query": "earlier conversation with customer"})` → `{"memories": [{"at": "2026-11-09T10:02:00Z", "text": "Conversation on 2026-11-09: The customer said his cat Pixel chewed his old card (not verified) and wanted to note it, nothing else. The assistant noted it, said it couldn't handle damaged cards there, and advised calling Kestrel or using the Kestrel app for a replacement. No case or transaction IDs, promises, or preferences were stated. Case ou …`

**Assistant:** Hi again - I checked, and there's nothing new to flag: no open dispute cases and nothing scheduled (no reminders or follow-ups).

For context, my only record of our last chat (9 Nov) is that your cat chewed your old card and I pointed you to Kestrel or the app for a replacement - no case was opened. Did you get the replacement sorted? Happy to look up recent transactions if you'd like.

_Episode written:_ Conversation on 2026-12-20: Customer asked for account news. Assistant checked cases and follow-ups (none found) and memory; no case or transaction IDs. Assistant noted the customer said his cat Pixel chewed his old card (not verified), that no case was opened on 9 Nov, and advised Kestrel/app for replacement; assistant asked if replacement was sorted and offered transaction lookup. No promises or preferences. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | a session cannot be resumed past 30 days: the day-0 text is gone from the transcript stores, maintenance or not | `found nowhere` |
| PASS | episodic | while the day-0 episode, within its 180 days, is kept | `2 episodes; mentioning 'Conversation on 2026-11-09': ['E-rnt-1-4bcb84']` |
