# langgraph · heldout-r4 · run 1 · r4-retention-without-maintenance

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r4r-s0  ·  session  ·  eli  ·  2026-11-02T10:00:00Z

**Customer:** Hi, Eli here. My parrot Mango chewed up my old card, so I cut it into pieces. Nothing else needed today.

**Assistant:** Got it, Eli - thanks for letting me know, and sorry about Mango's appetite.

One thing: I don't have a way to order a replacement card from here, so for a new card you'd need to contact Kestrel directly (the number on your statement or in the app). Your accounts and any transactions stay as they are - cutting up the card doesn't affect them.

Anything you need from me today, just say the word.

_Episode written:_ Conversation on 2026-11-02: The customer said parrot Mango chewed the old card and he cut it up (not verified); he said nothing else was needed. The assistant acknowledged this and said replacement cards can't be ordered here, advising him to contact Kestrel directly via statement/app; accounts/transactions remain unchanged. No case or transaction IDs, promises, or preferences stated. Case outcomes: no case touched. Lesson: none

## r4r-s1  ·  session  ·  eli  ·  2026-11-03T10:00:00Z

**Customer:** Quick note for the record: my sister Oksana is staying with me until spring, so you may hear her on the phone sometimes.

**Assistant:** Thanks for the heads-up. Just so you know, I can only keep two things on file - your contact channel and a travel notice - so I can't record a note about Oksana. It stays only in this conversation's transcript. Anything I can help you with today?

## r4r-s1-back  ·  session  ·  eli  ·  2026-12-04T10:00:00Z

_Resumes session `r4r-s1`._

**Customer:** Back in this chat again. How long do I have to dispute a charge?

- `search_policy({"question": "time limit to dispute a charge"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.744, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`

**Assistant:** You have **75 days from the posting date** of the charge to dispute it. After that, it can't be opened through this chat and would need a written claim.

If you tell me which charge you're looking at, I can check it's still within the window.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r4: a session resumed 31 days after its first turn does not keep its day-1 text, maintenance or not | `found nowhere` |
| PASS | working | r4: ...and the expired turn is not in context | `You have **75 days from the posting date** of the charge to dispute it. After that, it can't be opened through this chat and would need a written claim.  If you tell me which charge you're looking at, I can check it's st …` |

## r4r-s2  ·  session  ·  eli  ·  2027-06-10T10:00:00Z

**Customer:** Hi! What did we talk about last time?

- `load_memory({"query": "last conversation topics"})` → `{"memories": []}`

**Assistant:** I don't have any record of a previous conversation with you - nothing came back when I looked.

I can help with transactions, disputes, travel notices, contact preferences, reminders and card policy questions. What can I do for you?

_Episode written:_ Conversation on 2027-06-10: Customer asked what was discussed in a previous conversation. Assistant queried memory; no prior conversation records were returned, so assistant said it had no record and offered help with transactions, disputes, travel notices, contact preferences, reminders, and card policy questions. No case/transaction IDs, promises, or preferences were stated. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | r4: an episode past 180 days is not recalled even though no sweep ever ran | `{"memories": []}` |
| PASS | episodic | r4: ...and nothing from it is repeated | `I don't have any record of a previous conversation with you - nothing came back when I looked.  I can help with transactions, disputes, travel notices, contact preferences, reminders and card policy questions. What can I …` |
