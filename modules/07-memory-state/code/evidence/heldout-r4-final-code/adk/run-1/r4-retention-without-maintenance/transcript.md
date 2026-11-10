# adk · heldout-r4 · run 1 · r4-retention-without-maintenance

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r4r-s0  ·  session  ·  eli  ·  2026-11-02T10:00:00Z

**Customer:** Hi, Eli here. My parrot Mango chewed up my old card, so I cut it into pieces. Nothing else needed today.

- `search_policy({"question": "damaged card replacement"})` → `{"documents": [{"document": "card-replacement", "score": 0.751, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.632, "text": "# Dispute window\n …`

**Assistant:** Thanks, Eli - good to know. Since the card is damaged, you'll need a replacement: report it to Kestrel (call the number on your statement, or use the Kestrel app) so the old card is blocked and a new one ships. Replacement takes about 5 business days and is free.

One thing to note: Kestrel doesn't forward your new card number to recurring merchants - you'll need to update those yourself once the new card arrives.

Is there anything else I can help with?

_Episode written:_ Conversation on 2026-11-02: The customer said his parrot chewed his old card and he cut it up (not verified), and said nothing else was needed today. The assistant advised reporting damage to Kestrel via phone/app so the old card is blocked and a free replacement ships in about 5 business days, and to update recurring merchants; no case or transaction ID. Case outcomes: no case touched. Lesson: none

## r4r-s1  ·  session  ·  eli  ·  2026-11-03T10:00:00Z

**Customer:** Quick note for the record: my sister Oksana is staying with me until spring, so you may hear her on the phone sometimes.

**Assistant:** Thanks for the heads-up - noted. There's nothing on your account I need to change for that (the only details I can save are a contact channel or a travel notice). Just say the word if you want either of those set up.

## r4r-s1-back  ·  session  ·  eli  ·  2026-12-04T10:00:00Z

_Resumes session `r4r-s1`._

**Customer:** Back in this chat again. How long do I have to dispute a charge?

- `search_policy({"question": "how long do I have to dispute a charge (dispute time limit)"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.779, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`
- `load_memory({"query": "earlier conversation dispute charge"})` → `{"result": "memories=[MemoryEntry(content=Content(\n  parts=[\n    Part(\n      text='Conversation on 2026-11-03: The customer said another customer (her sister) is staying with her until spring and may be heard on the phone (not verified). The assistant noted this, said no account change was needed, explained only a contact channel or travel notice can be saved, and offered to set either up. No c …`

**Assistant:** You have **75 days from the transaction's posting date** to dispute a charge. After that, it can't be opened through the assistant and would need to go to a written claim.

I also checked my notes from our earlier chats - I don't see any prior dispute or transaction we discussed, so nothing to pick up from there. If there's a charge you want to dispute, tell me which one and I'll look it up.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r4: a session resumed 31 days after its first turn does not keep its day-1 text, maintenance or not | `found nowhere` |
| PASS | working | r4: ...and the expired turn is not in context | `You have **75 days from the transaction's posting date** to dispute a charge. After that, it can't be opened through the assistant and would need to go to a written claim.  I also checked my notes from our earlier chats  …` |

## r4r-s2  ·  session  ·  eli  ·  2027-06-10T10:00:00Z

**Customer:** Hi! What did we talk about last time?

- `load_memory({"query": "previous conversation summary"})` → `{"result": "memories=[]"}`

**Assistant:** I'll check that.
I have no record of any earlier conversation with you, so I can't tell you what we talked about. What can I help you with today?

_Episode written:_ Conversation on 2027-06-10: The customer asked what they had discussed last time. The assistant checked long-term memory, found no earlier conversation record, and told the customer it had no record, then asked how to help. No case or transaction IDs, promises, or stated preferences. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | r4: an episode past 180 days is not recalled even though no sweep ever ran | `{"result": "memories=[]"}` |
| PASS | episodic | r4: ...and nothing from it is repeated | `I'll check that. I have no record of any earlier conversation with you, so I can't tell you what we talked about. What can I help you with today?` |
