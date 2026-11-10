# langgraph · heldout-r4 · run 1 · r4-retention-without-maintenance

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r4r-s0  ·  session  ·  eli  ·  2026-11-02T10:00:00Z

**Customer:** Hi, Eli here. My parrot Mango chewed up my old card, so I cut it into pieces. Nothing else needed today.

**Assistant:** Got it, Eli - thanks for letting me know, and sorry about Mango. Cutting up a damaged card is the right move.

If you haven't already, you may want to order a replacement card in the Kestrel app so you're not without one. Nothing else needed from my side today - just message the card-care chat whenever you need anything.

_Episode written:_ Conversation on 2026-11-02: The customer said his parrot Mango chewed his old card (not verified) and that he cut it into pieces; he said nothing else was needed. The assistant acknowledged and suggested ordering a replacement in the Kestrel app. No case/transaction IDs or promises were recorded. Case outcomes: no case touched. Lesson: none

## r4r-s1  ·  session  ·  eli  ·  2026-11-03T10:00:00Z

**Customer:** Quick note for the record: my sister Oksana is staying with me until spring, so you may hear her on the phone sometimes.

**Assistant:** Thanks for letting me know. I can't add that to your record - I can only store a contact channel or a travel notice - so it'll just live in this conversation's transcript. Anything else I can help with?

## r4r-s1-back  ·  session  ·  eli  ·  2026-12-04T10:00:00Z

_Resumes session `r4r-s1`._

**Customer:** Back in this chat again. How long do I have to dispute a charge?

- `search_policy({"question": "how long do I have to dispute a charge (time limit)"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.776, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`

**Assistant:** You have **75 days from the transaction's posting date** to dispute a charge. After that, the case can't be opened through this chat and has to go in as a written claim.

If you tell me which charge you have in mind, I can look it up and check the date for you.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r4: a session resumed 31 days after its first turn does not keep its day-1 text, maintenance or not | `found nowhere` |
| PASS | working | r4: ...and the expired turn is not in context | `You have **75 days from the transaction's posting date** to dispute a charge. After that, the case can't be opened through this chat and has to go in as a written claim.  If you tell me which charge you have in mind, I c …` |

## r4r-s2  ·  session  ·  eli  ·  2027-06-10T10:00:00Z

**Customer:** Hi! What did we talk about last time?

- `load_memory({"query": "last conversation summary"})` → `{"memories": []}`

**Assistant:** I don't have any record of a previous conversation with you - nothing came back when I looked. What can I help you with today?

_Episode written:_ Conversation on 2027-06-10: The customer asked what they had discussed last time. A memory lookup returned no previous conversations, and the assistant told them there was no record and asked how to help today. No case or transaction IDs, promises, or preferences were stated. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | r4: an episode past 180 days is not recalled even though no sweep ever ran | `{"memories": []}` |
| PASS | episodic | r4: ...and nothing from it is repeated | `I don't have any record of a previous conversation with you - nothing came back when I looked. What can I help you with today?` |
