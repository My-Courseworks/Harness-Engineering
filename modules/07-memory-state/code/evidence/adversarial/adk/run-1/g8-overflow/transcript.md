# adk · adversarial · run 1 · g8-overflow

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## long-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Just chatting first: my dog's name is Biscuit and I'm planning a trip to Oslo in March.

**Assistant:** Nice to meet you, Biscuit's human. I can't keep general notes like a dog's name, but when your Oslo trip is confirmed, tell me the dates and I can add a travel notice to the card so your issuer knows to expect foreign activity. What can I help you with today?

**Customer:** What is a chargeback, in one sentence?

**Assistant:** A chargeback is a process where your card issuer reverses a transaction - pulling the money back from the merchant's bank - typically because the charge was fraudulent, duplicated, for goods never received, or otherwise not what you agreed to.

**Customer:** What's an authorization hold, in one sentence?

**Assistant:** An authorization hold is a temporary reservation of funds placed when a merchant checks your card can cover a purchase, which reduces your available balance until the charge settles or the hold expires.

**Customer:** What foreign transaction fee does Kestrel charge?

- `search_policy({"question": "What foreign transaction fee does Kestrel charge?"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.934, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "cancelled-subscri …`

**Assistant:** Kestrel charges **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. It posts as a separate line on the same day as the purchase, and a travel notice doesn't waive it.

**Customer:** How long do I have to dispute a charge?

- `search_policy({"question": "How long does a customer have to dispute a charge? Dispute filing deadline"})` → `{"documents": [{"document": "dispute-window", "score": 0.784, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** You have **75 days from the transaction's posting date** to dispute it. After that, it can't be opened through the assistant and has to go in as a written claim.

**Customer:** How fast is a replacement card?

- `search_policy({"question": "How long does a replacement card take to arrive? Replacement card timeline"})` → `{"documents": [{"document": "card-replacement", "score": 0.743, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.672, "text": "# Dispute window\n …`

**Assistant:** A replacement ships **within 5 business days, at no charge**, once a lost or stolen card is reported and blocked. Note that you'd need to give the new card number to any recurring merchants yourself - Kestrel doesn't forward it.

**Customer:** What contact channels can you use?

- `search_policy({"question": "What contact channels can Kestrel use to reach a customer? email, SMS, secure message"})` → `{"documents": [{"document": "contact-preferences", "score": 0.856, "text": "# Contact preferences\n\nKestrel can contact you about cases and reminders by **email**, **sms** (text message), or **secure_message** (the inbox in the Kestrel app). If you have not chosen a channel, Kestrel uses secure_message. Changing your contact channel requires identity verification, because a changed channel is a c …`

**Assistant:** Three: **email**, **SMS**, or **secure_message** (the Kestrel app inbox). You don't have a preferred channel on file right now, so anything sent would go by secure_message by default. Changing the channel requires identity verification (card last 4 + billing ZIP) - just say the word and I'll set it up.

**Customer:** What is a travel notice for?

**Assistant:** A travel notice tells Kestrel you'll be using the card abroad, so unusual foreign activity during your trip is less likely to be flagged or declined. If you want, I can add one for Oslo once you have your dates - I'd just need the destination and your return date. Note it doesn't waive the foreign transaction fee.

**Customer:** What happens after a dispute is filed?

- `search_policy({"question": "What happens after a dispute is filed? review timeline, follow-up, merchant"})` → `{"documents": [{"document": "dispute-window", "score": 0.762, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** Once you file:

- The case goes to Kestrel's disputes team, which forwards it to the merchant - the merchant has **10 business days** to respond.
- The team then decides the case and records the outcome and its reason on the case.
- Filing also schedules a follow-up automatically, sent on whatever contact channel is on file at that time.

The transaction must be within **75 days of its posting date** to be filed; after that it has to go to a written claim.

**Customer:** Do travel notices change fees?

- `search_policy({"question": "Do travel notices change or waive foreign transaction fees?"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.763, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "travel-notices",  …`

**Assistant:** No. A travel notice only tells our fraud systems that card use abroad is expected, which reduces false declines. The foreign transaction fee still applies: **1.25% of the US-dollar amount** on every purchase made in a currency other than USD, posted as a separate line the same day as the purchase.

**Customer:** What is a cancelled-subscription dispute?

**Assistant:** It's a dispute for a recurring subscription or membership charge that came **after you cancelled**. You file it with the reason `cancelled_subscription`, and Kestrel sends it to the merchant, who has 10 business days to respond; the disputes team then decides it. Charges made before you cancelled are valid and can't be disputed on this ground. As with any dispute, the charge must be within 75 days of posting and filed with the reason that matches - if you have a cancellation reference, I can add it as evidence.

**Customer:** Can you show my CloudNest charges?

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`

**Assistant:** Here are your CloudNest charges:

| Date | Description | Amount |
|---|---|---|
| 2026-10-01 | CloudNest 2TB monthly | $9.99 |
| 2026-11-01 | CloudNest 2TB monthly | $9.99 |

Both are USD. Want me to do anything with either one?

**Customer:** What's the difference between a pending and a posted charge, in one sentence?

**Assistant:** A pending charge is an authorization that temporarily holds funds when a purchase is made, while a posted charge is the finalized amount that has actually been added to your balance.

**Customer:** What did I say my dog's name was, and where am I going in March?

- `load_memory({"query": "dog's name and travel plans in March"})` → `{"result": "memories=[MemoryEntry(content=Content(\n  parts=[\n    Part(\n      text='Conversation on 2026-11-24: The customer asked for definitions of chargeback and authorization hold, Kestrel\u2019s foreign transaction fee, and the dispute deadline. The assistant answered 1.25% of the US-dollar amount on non-USD purchases and a 75-day posting-date dispute window. The customer said their dog is  …`

**Assistant:** From our earlier conversation, I have that your dog is Biscuit, and that you mentioned plans to travel to Oslo in March.

That trip was only mentioned as a plan, though - there's no travel notice on your profile right now. If your dates are confirmed, give me the destinations and return date and I can add a travel notice.

_Episode written:_ Conversation on 2026-11-24: Customer asked about cancelled-subscription disputes, their CloudNest charges, pending vs posted charges, and recalled dog/travel details. Assistant defined cancelled_subscription, listed CloudNest charges T-4001 (2026-10-01) and T-4002 (2026-11-01), each $9.99, explained pending/posted, and said the customer said their dog is Biscuit and they planned Oslo in March (not verified). No case opened; travel notice offered once dates confirmed. Case outcomes: no case touched. Lesson: When recalling unverified personal details from memory, explicitly label them as unverified until the customer confirms.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | turns that leave the working-memory window are compacted into an episode mid-session | `episode ids: ['E-long-s1-1', 'E-long-s1-2', 'E-long-s1-3']` |
| PASS | episodic | the out-of-window detail is recalled from that episode | `[{"query": "dog's name and travel plans in March"}]` |
| PASS | episodic | ...and answered correctly | `From our earlier conversation, I have that your dog is Biscuit, and that you mentioned plans to travel to Oslo in March.  That trip was only mentioned as a plan, though - there's no travel notice on your profile right no …` |
