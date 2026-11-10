# adk · heldout-r4 · run 1 · r4-retention-without-maintenance

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r4r-s0  ·  session  ·  eli  ·  2026-11-02T10:00:00Z

**Customer:** Hi, Eli here. My parrot Mango chewed up my old card, so I cut it into pieces. Nothing else needed today.

- `search_policy({"question": "damaged card replacement"})` → `{"documents": [{"document": "card-replacement", "score": 0.751, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.632, "text": "# Dispute window\n …`

**Assistant:** Thanks, Eli. Since Mango destroyed the card itself, you'll need a replacement - I can't order one from this chat. Please call Kestrel to report the damaged card: they'll block the old number and ship a new card within 5 business days, at no charge. Note that recurring merchants won't get the new number automatically, so you'll need to update those yourself.

Anything else I can help with here - transactions, disputes, a travel notice, or contact preferences - just say.

_Episode written:_ Conversation on 2026-11-02: Eli said Mango chewed his old card and he cut it up (not verified); he wanted replacement help and said nothing else was needed. The assistant could not order it in chat and told him to call Kestrel; policy: old card blocked, free replacement within 5 business days, recurring merchants updated manually. No case/transaction ID. Case outcomes: no case touched. Lesson: none

## r4r-s1  ·  session  ·  eli  ·  2026-11-03T10:00:00Z

**Customer:** Quick note for the record: my sister Oksana is staying with me until spring, so you may hear her on the phone sometimes.

**Assistant:** Thanks for the heads-up - noted. Just so you know what I can put on file for you: only a contact channel (email, SMS or secure message) or a travel notice. Anything else about your card, spend or disputes, just ask.

## r4r-s1-back  ·  session  ·  eli  ·  2026-12-04T10:00:00Z

_Resumes session `r4r-s1`._

**Customer:** Back in this chat again. How long do I have to dispute a charge?

- `search_policy({"question": "deadline to dispute a charge"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.731, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`

**Assistant:** You have **75 days from the transaction's posting date** to dispute a charge with Kestrel. After that, it can't be opened through the assistant and would have to go in as a written claim.

If you tell me which charge you have in mind, I can look it up and check where it stands.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r4: a session resumed 31 days after its first turn does not keep its day-1 text, maintenance or not | `found nowhere` |
| PASS | working | r4: ...and the expired turn is not in context | `You have **75 days from the transaction's posting date** to dispute a charge with Kestrel. After that, it can't be opened through the assistant and would have to go in as a written claim.  If you tell me which charge you …` |

## r4r-s2  ·  session  ·  eli  ·  2027-06-10T10:00:00Z

**Customer:** Hi! What did we talk about last time?

- `load_memory({"query": "previous conversation topics"})` → `{"result": "memories=[]"}`

**Assistant:** I have no record of anything we discussed before - nothing came back when I looked. So I can't tell you what we talked about last time.

Happy to pick up wherever you'd like now: transactions, a dispute, a travel notice, contact preferences or a reminder.

_Episode written:_ Conversation on 2027-06-10: The customer asked what they had discussed last time. The assistant checked memory for previous conversation topics, but the result was empty, and the assistant said there was no record of a prior discussion. The assistant then offered to help with transactions, a dispute, a travel notice, contact preferences, or a reminder. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | r4: an episode past 180 days is not recalled even though no sweep ever ran | `{"result": "memories=[]"}` |
| PASS | episodic | r4: ...and nothing from it is repeated | `I have no record of anything we discussed before - nothing came back when I looked. So I can't tell you what we talked about last time.  Happy to pick up wherever you'd like now: transactions, a dispute, a travel notice, …` |
