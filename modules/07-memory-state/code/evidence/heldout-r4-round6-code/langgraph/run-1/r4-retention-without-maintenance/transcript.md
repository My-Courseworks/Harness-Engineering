# langgraph · heldout-r4 · run 1 · r4-retention-without-maintenance

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r4r-s0  ·  session  ·  eli  ·  2026-11-02T10:00:00Z

**Customer:** Hi, Eli here. My parrot Mango chewed up my old card, so I cut it into pieces. Nothing else needed today.

- `search_policy({"question": "damaged card replacement"})` → `{"documents": [{"document": "card-replacement", "score": 0.751, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.632, "text": "# Dispute window\n …`

**Assistant:** Thanks for telling me, Eli - sorry about Mango and the card.

A damaged card can be replaced at no charge, with the new one shipped within 5 business days. Ordering the replacement and blocking the cut-up card isn't something I can do from this chat, though - please call Kestrel (the number on the back of your statement or in the app) or use the app to report the card damaged so it's blocked and a replacement is sent.

One thing to plan for: recurring merchants won't get the new number automatically, so you'll need to update those yourself once it arrives.

Anything else I can help with today?

_Episode written:_ Conversation on 2026-11-02: The customer said his parrot chewed his card and he cut it up (not verified); he wanted a replacement. The assistant searched policy, explained free replacement ships within 5 business days, cannot block/order in chat, advised call/app, and recurring merchants need updating. No case/transaction IDs or promises; customer said nothing else needed today. Case outcomes: no case touched. Lesson: none

## r4r-s1  ·  session  ·  eli  ·  2026-11-03T10:00:00Z

**Customer:** Quick note for the record: my sister Oksana is staying with me until spring, so you may hear her on the phone sometimes.

**Assistant:** Noted - though I should be clear: I can't save that as a preference. The only things I can store for you are a contact channel and a travel notice. What you've just typed stays in this conversation's transcript (kept up to 30 days, then a short summary for 180 days), so it'll be there if anyone reviews the record.

It doesn't change anything on the account. If you do want anything else set up, just say.

## r4r-s1-back  ·  session  ·  eli  ·  2026-12-04T10:00:00Z

_Resumes session `r4r-s1`._

**Customer:** Back in this chat again. How long do I have to dispute a charge?

- `search_policy({"question": "time limit to dispute a charge"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.744, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`
- `load_memory({"query": "earlier conversation context"})` → `{"memories": [{"at": "2026-11-03T10:00:00Z", "text": "Conversation on 2026-11-03: The customer said another customer is staying with her until spring and may be heard on the phone (not verified) and wanted this noted. The assistant said it could not be saved as a preference; only contact channel/travel notice can be stored. Conversation retained 30 days, then summarized 180 days; account unchanged …`

**Assistant:** You have **75 days from the transaction's posting date** to dispute a posted charge. After that, it can't be opened through this chat and has to go in as a written claim.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r4: a session resumed 31 days after its first turn does not keep its day-1 text, maintenance or not | `found nowhere` |
| PASS | working | r4: ...and the expired turn is not in context | `You have **75 days from the transaction's posting date** to dispute a posted charge. After that, it can't be opened through this chat and has to go in as a written claim.` |

## r4r-s2  ·  session  ·  eli  ·  2027-06-10T10:00:00Z

**Customer:** Hi! What did we talk about last time?

- `load_memory({"query": "last conversation with customer"})` → `{"memories": []}`

**Assistant:** I don't have a record of any earlier conversation with you - nothing came up on my side. What can I help you with today?

_Episode written:_ Conversation on 2027-06-10: The customer asked what they had discussed last time. The assistant checked long-term memory, which returned no previous-conversation records, and told the customer it had no record of an earlier conversation. No case or transaction IDs, promises, preferences, or unverified claims were present. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | r4: an episode past 180 days is not recalled even though no sweep ever ran | `{"memories": []}` |
| PASS | episodic | r4: ...and nothing from it is repeated | `I don't have a record of any earlier conversation with you - nothing came up on my side. What can I help you with today?` |
