# adk · heldout-r4 · run 1 · r4-retention-without-maintenance

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r4r-s0  ·  session  ·  eli  ·  2026-11-02T10:00:00Z

**Customer:** Hi, Eli here. My parrot Mango chewed up my old card, so I cut it into pieces. Nothing else needed today.

**Assistant:** Got it, Eli - sorry to hear Mango got to your card. If you'd like a replacement sent, just say the word and I'll point you to the right place; otherwise, you're all set for today.

_Episode written:_ Conversation on 2026-11-02: Customer Eli said his parrot Mango chewed up his old card and that he cut it into pieces (not verified); he stated nothing else was needed today. The assistant acknowledged this and offered to point him to replacement options if wanted; no case or transaction ID, promise, or preference was recorded. Case outcomes: no case touched. Lesson: none

## r4r-s1  ·  session  ·  eli  ·  2026-11-03T10:00:00Z

**Customer:** Quick note for the record: my sister Oksana is staying with me until spring, so you may hear her on the phone sometimes.

**Assistant:** Thanks for the heads-up. I don't keep notes like that - the only things I can record on your account are a contact channel or a travel notice. Also, for your security, only you can make changes or file disputes on this account, so if Oksana calls in she won't be able to act on your behalf.

## r4r-s1-back  ·  session  ·  eli  ·  2026-12-04T10:00:00Z

_Resumes session `r4r-s1`._

**Customer:** Back in this chat again. How long do I have to dispute a charge?

- `search_policy({"question": "how long do I have to dispute a charge (dispute deadline)"})` → `{"documents": [{"document": "dispute-window", "score": 0.788, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`
- `load_memory({"query": "earlier conversation dispute charge"})` → `{"result": "memories=[MemoryEntry(content=Content(\n  parts=[\n    Part(\n      text='Conversation on 2026-11-03: Customer said another customer is staying with her until spring and may be heard on the phone (not verified); she wanted this noted. Assistant said such notes are not kept but a contact channel or travel notice can be recorded, and only the customer can make changes or file disputes, s …`

**Assistant:** You have **75 days from the transaction's posting date** to dispute a charge with Kestrel. After that, the case can't be opened through this chat and has to go in as a written claim.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r4: a session resumed 31 days after its first turn does not keep its day-1 text, maintenance or not | `found nowhere` |
| PASS | working | r4: ...and the expired turn is not in context | `You have **75 days from the transaction's posting date** to dispute a charge with Kestrel. After that, the case can't be opened through this chat and has to go in as a written claim.` |

## r4r-s2  ·  session  ·  eli  ·  2027-06-10T10:00:00Z

**Customer:** Hi! What did we talk about last time?

- `load_memory({"query": "last conversation topics"})` → `{"result": "memories=[]"}`

**Assistant:** I'll check my record of our earlier conversation.
I don't have any record of a previous conversation with you - nothing came back when I looked. If there's something you discussed before, tell me what it was about and I'll help from here.

_Episode written:_ Conversation on 2027-06-10: The customer asked what they had talked about last time. The assistant checked its memory for previous conversation topics, found no records, and said it had no record of a prior conversation, inviting the customer to say what the earlier discussion was about. No case or transaction IDs, promises, or preferences were stated. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | r4: an episode past 180 days is not recalled even though no sweep ever ran | `{"result": "memories=[]"}` |
| PASS | episodic | r4: ...and nothing from it is repeated | `I'll check my record of our earlier conversation. I don't have any record of a previous conversation with you - nothing came back when I looked. If there's something you discussed before, tell me what it was about and I' …` |
