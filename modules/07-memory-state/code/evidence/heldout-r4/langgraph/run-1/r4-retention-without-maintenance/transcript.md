# langgraph · heldout-r4 · run 1 · r4-retention-without-maintenance

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r4r-s0  ·  session  ·  eli  ·  2026-11-02T10:00:00Z

**Customer:** Hi, Eli here. My parrot Mango chewed up my old card, so I cut it into pieces. Nothing else needed today.

**Assistant:** Sorry to hear about Mango's handiwork. I can't order a replacement card from here - for that, call Kestrel or use the "Replace card" option in the Kestrel app. Once the new card arrives, remember to update any recurring payments (subscriptions, bills) that were tied to the old one.

Nothing has been changed on your account today. If a dispute, travel notice or reminder comes up later, just message me.

_Episode written:_ Conversation on 2026-11-02: Eli said their parrot Mango chewed up their old card, so they cut it into pieces (not verified). They said nothing else was needed. The assistant said a replacement could not be ordered there, directed Eli to call Kestrel or use the app's "Replace card" option, and advised updating recurring payments. No account changes or IDs. Case outcomes: no case touched. Lesson: none

## r4r-s1  ·  session  ·  eli  ·  2026-11-03T10:00:00Z

**Customer:** Quick note for the record: my sister Oksana is staying with me until spring, so you may hear her on the phone sometimes.

**Assistant:** Thanks for the heads-up. I can only store a contact channel or a travel notice, so I can't put a note about your sister on file - but it's good to know. Anything I can help you with today?

## r4r-s1-back  ·  session  ·  eli  ·  2026-12-04T10:00:00Z

_Resumes session `r4r-s1`._

**Customer:** Back in this chat again. How long do I have to dispute a charge?

- `search_policy({"question": "How long does a customer have to dispute a charge (dispute time limit deadline)?"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.768, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`

**Assistant:** You have **75 days from the transaction's posting date** to dispute a charge with Kestrel. After that, it can't be opened through the assistant and has to go as a written claim.

If you tell me which charge it is, I can check the posting date and file the dispute for you.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r4: a session resumed 31 days after its first turn does not keep its day-1 text, maintenance or not | `found nowhere` |
| PASS | working | r4: ...and the expired turn is not in context | `You have **75 days from the transaction's posting date** to dispute a charge with Kestrel. After that, it can't be opened through the assistant and has to go as a written claim.  If you tell me which charge it is, I can  …` |

## r4r-s2  ·  session  ·  eli  ·  2027-06-10T10:00:00Z

**Customer:** Hi! What did we talk about last time?

- `load_memory({"query": "what we talked about last conversation"})` → `{"memories": []}`

**Assistant:** I don't have any record of a previous conversation with you - nothing came back when I checked. If there was something specific you discussed (a transaction, a dispute, a travel notice), tell me what it was about and I'll help from here.

_Episode written:_ Conversation on 2027-06-10: The customer asked what they discussed last time. A memory lookup returned no records, and the assistant said no previous conversation was found, then asked for specifics about any transaction, dispute, or travel notice. The customer asked about a prior conversation (not verified). Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | r4: an episode past 180 days is not recalled even though no sweep ever ran | `{"memories": []}` |
| PASS | episodic | r4: ...and nothing from it is repeated | `I don't have any record of a previous conversation with you - nothing came back when I checked. If there was something specific you discussed (a transaction, a dispute, a travel notice), tell me what it was about and I'l …` |
