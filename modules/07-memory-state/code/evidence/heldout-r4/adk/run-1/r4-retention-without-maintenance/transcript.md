# adk · heldout-r4 · run 1 · r4-retention-without-maintenance

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r4r-s0  ·  session  ·  eli  ·  2026-11-02T10:00:00Z

**Customer:** Hi, Eli here. My parrot Mango chewed up my old card, so I cut it into pieces. Nothing else needed today.

**Assistant:** Got it, Eli - thanks for letting me know. Since the card is destroyed, keep an eye on your transactions for anything you don't recognize from it, and message me here if something shows up that you didn't authorize - I can look it up and dispute it if needed.

If you want a replacement card issued, that isn't something I can do from this chat, so you'd need to request one through the Kestrel app or by calling the number on the back of your card.

Nothing has been saved from this message. Anything else, just say.

_Episode written:_ Conversation on 2026-11-02: Eli reported his parrot chewed his old card and he cut it up (not verified); he needed nothing else. The assistant advised monitoring transactions and said unauthorized charges could be looked up/disputed; replacement must be requested via the Kestrel app or phone number. Nothing was saved; no case or transaction IDs. Case outcomes: no case touched. Lesson: none

## r4r-s1  ·  session  ·  eli  ·  2026-11-03T10:00:00Z

**Customer:** Quick note for the record: my sister Oksana is staying with me until spring, so you may hear her on the phone sometimes.

**Assistant:** Noted - thanks for the heads-up. I can't store that as a fact (I only keep a contact channel or travel notice), so I won't record anything about Oksana. Anything else I can help with?

## r4r-s1-back  ·  session  ·  eli  ·  2026-12-04T10:00:00Z

_Resumes session `r4r-s1`._

**Customer:** Back in this chat again. How long do I have to dispute a charge?

- `search_policy({"question": "How long does a customer have to dispute a charge? Dispute time limit / deadline"})` → `{"documents": [{"document": "dispute-window", "score": 0.769, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** You have **75 days from the transaction's posting date** to dispute a posted charge. After that, it can't be opened through the assistant and has to go in as a written claim.

Any particular charge you're looking at?

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r4: a session resumed 31 days after its first turn does not keep its day-1 text, maintenance or not | `found nowhere` |
| PASS | working | r4: ...and the expired turn is not in context | `You have **75 days from the transaction's posting date** to dispute a posted charge. After that, it can't be opened through the assistant and has to go in as a written claim.  Any particular charge you're looking at?` |

## r4r-s2  ·  session  ·  eli  ·  2027-06-10T10:00:00Z

**Customer:** Hi! What did we talk about last time?

- `load_memory({"query": "last conversation summary"})` → `{"result": "memories=[]"}`

**Assistant:** I don't have any record of a previous conversation with you - nothing came back when I checked.

I can help with transactions, disputes, travel notices, contact preferences and reminders. What would you like to do?

_Episode written:_ Conversation on 2027-06-10: The customer asked what they had discussed last time. A memory lookup returned no records, and the assistant said no previous conversation was found. The assistant offered help with transactions, disputes, travel notices, contact preferences, and reminders. No case or transaction IDs, promises, or stated preferences were present. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | r4: an episode past 180 days is not recalled even though no sweep ever ran | `{"result": "memories=[]"}` |
| PASS | episodic | r4: ...and nothing from it is repeated | `I don't have any record of a previous conversation with you - nothing came back when I checked.  I can help with transactions, disputes, travel notices, contact preferences and reminders. What would you like to do?` |
