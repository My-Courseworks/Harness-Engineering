# adk · heldout-r4 · run 1 · r4-retention-without-maintenance

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r4r-s0  ·  session  ·  eli  ·  2026-11-02T10:00:00Z

**Customer:** Hi, Eli here. My parrot Mango chewed up my old card, so I cut it into pieces. Nothing else needed today.

**Assistant:** Got it, Eli - sorry to hear about Mango and the card. Nothing filed or changed on my end.

If you need a replacement card, you can order one in the Kestrel app or through Kestrel customer service. And please don't send me the card number or any details from the pieces - I don't need them. Anything else, just say the word.

_Episode written:_ Conversation on 2026-11-02: Eli said Mango, their parrot, chewed up their old card and they cut it into pieces (not verified); no further help was needed today. The assistant filed or changed nothing, gave no case or transaction IDs, promised nothing, and advised ordering a replacement via the Kestrel app or customer service without sending card details. Case outcomes: no case touched. Lesson: none

## r4r-s1  ·  session  ·  eli  ·  2026-11-03T10:00:00Z

**Customer:** Quick note for the record: my sister Oksana is staying with me until spring, so you may hear her on the phone sometimes.

**Assistant:** Got it - thanks for the heads-up. Oksana isn't something I can add to your profile; the only details I can save there are a contact channel and a travel notice, so nothing needs changing. If she'll be handling your account, she'd still need to be an authorized user with the bank - I can't set that up here.

## r4r-s1-back  ·  session  ·  eli  ·  2026-12-04T10:00:00Z

_Resumes session `r4r-s1`._

**Customer:** Back in this chat again. How long do I have to dispute a charge?

- `search_policy({"question": "how long do I have to dispute a charge (dispute deadline)"})` → `{"documents": [{"document": "dispute-window", "score": 0.788, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`
- `load_memory({"query": "earlier conversation about disputing a charge"})` → `{"result": "memories=[MemoryEntry(content=Content(\n  parts=[\n    Part(\n      text='Conversation on 2026-11-02: Eli said Mango, their parrot, chewed up their old card and they cut it into pieces (not verified); no further help was needed today. The assistant filed or changed nothing, gave no case or transaction IDs, promised nothing, and advised ordering a replacement via the Kestrel app or cust …`

**Assistant:** You have **75 days from the transaction's posting date** to dispute a charge. After 75 days it can't be opened through me - it would have to go to a written claim.

(I don't have any earlier dispute conversation on record for you; if you're thinking of a specific charge, tell me which one and I'll pull it up.)

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | r4: a session resumed 31 days after its first turn does not keep its day-1 text, maintenance or not | `{"Oksana": ["adk_sessions.db"]}` |
| PASS | working | r4: ...and the expired turn is not in context | `You have **75 days from the transaction's posting date** to dispute a charge. After 75 days it can't be opened through me - it would have to go to a written claim.  (I don't have any earlier dispute conversation on recor …` |

## r4r-s2  ·  session  ·  eli  ·  2027-06-10T10:00:00Z

**Customer:** Hi! What did we talk about last time?

- `load_memory({"query": "last conversation topics"})` → `{"result": "memories=[]"}`

**Assistant:** I don't have any record of a previous conversation with you - nothing came up when I checked. What can I help you with today?

_Episode written:_ Conversation on 2027-06-10: The customer asked what was discussed last time. The assistant called load_memory; it returned no memories, so the assistant said there was no record of a previous conversation and asked how to help. No case/transaction IDs, promises, or preferences were stated. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | r4: an episode past 180 days is not recalled even though no sweep ever ran | `{"result": "memories=[]"}` |
| PASS | episodic | r4: ...and nothing from it is repeated | `I don't have any record of a previous conversation with you - nothing came up when I checked. What can I help you with today?` |
