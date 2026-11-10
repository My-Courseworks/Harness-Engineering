# langgraph · heldout-r4 · run 1 · r4-retention-without-maintenance

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r4r-s0  ·  session  ·  eli  ·  2026-11-02T10:00:00Z

**Customer:** Hi, Eli here. My parrot Mango chewed up my old card, so I cut it into pieces. Nothing else needed today.

- `search_policy({"question": "damaged card replacement how to order"})` → `{"documents": [{"document": "card-replacement", "score": 0.739, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.635, "text": "# Dispute window\n …`

**Assistant:** Sounds like Mango earned his keep. Nothing filed or changed here.

One thing worth knowing: I can't order a replacement card in this chat - report the card as lost/damaged to Kestrel (or in the app) and they'll block it and ship a replacement within 5 business days at no charge. You'll need to give recurring merchants the new number yourself; Kestrel doesn't forward it.

Anything else, just message me.

_Episode written:_ Conversation on 2026-11-02: Customer said his parrot Mango chewed his card and he cut it up (not verified); he needed nothing else. Assistant filed/changed nothing and said replacement cannot be ordered in chat. Customer should report damage via Kestrel or app; card will be blocked and replacement shipped within 5 business days at no charge. No case or transaction ID. Case outcomes: no case touched. Lesson: none

## r4r-s1  ·  session  ·  eli  ·  2026-11-03T10:00:00Z

**Customer:** Quick note for the record: my sister Oksana is staying with me until spring, so you may hear her on the phone sometimes.

**Assistant:** Noted - if I hear another voice on the line, that'll be Oksana. Just so it's clear: I can't add that to your profile (I only record a contact channel or travel notice there), though anything you type here is kept in this conversation's transcript for up to 30 days, then a short summary for 180 days.

Anything I can help you with today?

## r4r-s1-back  ·  session  ·  eli  ·  2026-12-04T10:00:00Z

_Resumes session `r4r-s1`._

**Customer:** Back in this chat again. How long do I have to dispute a charge?

- `search_policy({"question": "time limit to dispute a charge"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.744, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`
- `load_memory({"query": "earlier conversation in this chat"})` → `{"memories": [{"at": "2026-11-03T10:00:00Z", "text": "Conversation on 2026-11-03: Customer said another customer is staying with them until spring and may be heard on the phone (not verified); wanted it noted. Assistant said it could not be added to the profile, only a contact channel or travel notice; typed info is kept in the transcript up to 30 days, then summarized for 180 days. No case/transa …`

**Assistant:** You have **75 days from the transaction's posting date** to dispute a charge. After that, it can't be opened through the assistant and has to go in as a written claim.

I don't see anything relevant from our earlier chats for this question - just a note from 2 November about a damaged card and one from 3 November. Is there something specific from a past conversation you wanted to pick up?

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r4: a session resumed 31 days after its first turn does not keep its day-1 text, maintenance or not | `found nowhere` |
| PASS | working | r4: ...and the expired turn is not in context | `You have **75 days from the transaction's posting date** to dispute a charge. After that, it can't be opened through the assistant and has to go in as a written claim.  I don't see anything relevant from our earlier chat …` |

## r4r-s2  ·  session  ·  eli  ·  2027-06-10T10:00:00Z

**Customer:** Hi! What did we talk about last time?

- `load_memory({"query": "last conversation summary"})` → `{"memories": []}`

**Assistant:** I don't have any record of a previous conversation - nothing came up when I looked. I can only see your current profile: no contact channel set (so follow-ups and reminders go by secure message in the Kestrel app), and no travel notice on file.

Happy to help with something new - transactions, a dispute, a travel notice or a reminder?

_Episode written:_ Conversation on 2027-06-10: The customer said there was a previous conversation (not verified) and asked what was discussed. Memory search returned none; assistant said no previous record, noted profile has no contact channel-follow-ups/reminders via secure message in Kestrel app-and no travel notice, and offered help with transactions, disputes, travel notices, or reminders. No case/transaction IDs. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | r4: an episode past 180 days is not recalled even though no sweep ever ran | `{"memories": []}` |
| PASS | episodic | r4: ...and nothing from it is repeated | `I don't have any record of a previous conversation - nothing came up when I looked. I can only see your current profile: no contact channel set (so follow-ups and reminders go by secure message in the Kestrel app), and n …` |
