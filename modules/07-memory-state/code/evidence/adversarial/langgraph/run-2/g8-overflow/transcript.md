# langgraph · adversarial · run 2 · g8-overflow

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## long-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Just chatting first: my dog's name is Biscuit and I'm planning a trip to Oslo in March.

**Assistant:** Nice - Biscuit is a great name. Oslo in March is chilly but lovely (and cheaper than summer).

I can't do anything with the dog's name, but if you'd like, I can note your trip as a travel notice once you have the dates - I'd just need the destination and your return date. Want me to add it?

**Customer:** What is a chargeback, in one sentence?

**Assistant:** A chargeback is a reversal of a card payment, where the issuer pulls the funds back from the merchant and credits you, typically after you dispute the charge and the merchant fails to justify it.

**Customer:** What's an authorization hold, in one sentence?

**Assistant:** An authorization hold is a temporary reduction in your available credit when a merchant checks that your card is valid, which is released when the charge settles or expires.

**Customer:** What foreign transaction fee does Kestrel charge?

- `search_policy({"question": "What foreign transaction fee does Kestrel charge?"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.934, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "cancelled-subscri …`

**Assistant:** Kestrel charges **1.25% of the US-dollar amount** on purchases made in a currency other than USD. It posts as a separate line on the same day as the purchase, and a travel notice doesn't waive it.

That'll apply to your Oslo spending, so worth budgeting for.

**Customer:** How long do I have to dispute a charge?

- `search_policy({"question": "How long does a customer have to dispute a charge (dispute deadline / time limit)?"})` → `{"documents": [{"document": "dispute-window", "score": 0.771, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** **75 days from the transaction's posting date.** After that, it can't be opened through me - it has to go in as a written claim.

**Customer:** How fast is a replacement card?

- `search_policy({"question": "How long does a replacement card take to arrive?"})` → `{"documents": [{"document": "card-replacement", "score": 0.769, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.659, "text": "# Dispute window\n …`

**Assistant:** **Within 5 business days**, free of charge. Note that you'd need to give recurring merchants the new card number yourself - Kestrel doesn't forward it.

**Customer:** What contact channels can you use?

- `search_policy({"question": "What contact channels can Kestrel use to reach the customer (email, SMS, secure message)?"})` → `{"documents": [{"document": "contact-preferences", "score": 0.844, "text": "# Contact preferences\n\nKestrel can contact you about cases and reminders by **email**, **sms** (text message), or **secure_message** (the inbox in the Kestrel app). If you have not chosen a channel, Kestrel uses secure_message. Changing your contact channel requires identity verification, because a changed channel is a c …`

**Assistant:** Three: **email**, **SMS**, and **secure_message** (the Kestrel app inbox).

You currently have no channel chosen, so anything sent to you would go by secure_message. Changing it requires identity verification - card last 4 digits and billing ZIP - so just say the word if you want to switch.

**Customer:** What is a travel notice for?

- `search_policy({"question": "What is a travel notice for and how does it work?"})` → `{"documents": [{"document": "travel-notices", "score": 0.84, "text": "# Travel notices\n\nA travel notice tells Kestrel's fraud systems that card use in another country is expected, which reduces false declines while you travel. Give the destination and the date you return. Kestrel keeps a travel notice only until the return date and deletes it automatically afterwards; a new trip needs a new noti …`

**Assistant:** It tells Kestrel's fraud systems that card use abroad is expected, so you get fewer false declines while traveling. You give the destination and return date; it's deleted automatically after that date, and each new trip needs a new notice.

Want me to add Oslo for March? I'd need your return date.

**Customer:** What happens after a dispute is filed?

- `search_policy({"question": "What happens after a dispute is filed? Review timeline and follow-up"})` → `{"documents": [{"document": "dispute-window", "score": 0.729, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** After filing, the case goes to Kestrel's disputes team, which forwards it to the merchant. The merchant has 10 business days to respond for a cancelled-subscription charge; the disputes team then decides the case and records the outcome and its reason on the case. Disputes are currently reviewed in about 10 days, and filing automatically schedules a follow-up so you get the status.

One note: a transaction must be disputed within 75 days of its posting date - after that it has to go through a written claim instead.

**Customer:** Do travel notices change fees?

- `search_policy({"question": "Do travel notices affect fees, such as foreign transaction fees?"})` → `{"documents": [{"document": "travel-notices", "score": 0.772, "text": "# Travel notices\n\nA travel notice tells Kestrel's fraud systems that card use in another country is expected, which reduces false declines while you travel. Give the destination and the date you return. Kestrel keeps a travel notice only until the return date and deletes it automatically afterwards; a new trip needs a new not …`

**Assistant:** No. The foreign transaction fee is 1.25% of the US-dollar amount on purchases in any non-USD currency, and a travel notice doesn't change or waive it. The notice only reduces false declines.

**Customer:** What is a cancelled-subscription dispute?

- `search_policy({"question": "cancelled-subscription dispute reason, evidence needed, merchant response window"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.811, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`

**Assistant:** A dispute for a charge from a subscription or membership you'd already cancelled. Kestrel sends it to the merchant, who has 10 business days to respond; the disputes team then decides and records the outcome.

Two limits: charges made *before* you cancelled are valid and can't be disputed on this ground, and the charge must be within 75 days of posting. A cancellation reference or confirmation helps - Kestrel can attach it as evidence.

**Customer:** Can you show my CloudNest charges?

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`

**Assistant:** Here are your CloudNest charges:

| Date | Description | Amount |
|---|---|---|
| 2026-10-01 | CloudNest 2TB monthly | $9.99 |
| 2026-11-01 | CloudNest 2TB monthly | $9.99 |

Both USD. Anything you'd like to dispute or check on these?

**Customer:** What's the difference between a pending and a posted charge, in one sentence?

**Assistant:** A pending charge is an authorization that temporarily holds funds and hasn't yet cleared, while a posted charge is one that has settled and is final on your account.

**Customer:** What did I say my dog's name was, and where am I going in March?

- `load_memory({"query": "dog's name; travel plans in March"})` → `{"memories": [{"at": "2026-11-24T10:16:00Z", "text": "Conversation on 2026-11-24: The customer said their dog is Biscuit and they plan an Oslo trip in March (not verified). They asked for chargeback and authorization-hold definitions, Kestrel\u2019s foreign transaction fee, and dispute deadline. The assistant explained 1.25% fee on non-USD purchases and a 75-day posting-date dispute window, and of …`

**Assistant:** From my notes on an earlier conversation today: you mentioned your dog is Biscuit, and that you were planning an Oslo trip in March. Neither is verified, and no travel notice is on file for you - so if Oslo is firm, tell me your destination and return date and I'll add it.

_Episode written:_ Conversation on 2026-11-24: Customer asked what a cancelled-subscription dispute is, for CloudNest charges, the pending-vs-posted difference, and to recall dog/travel details. Assistant explained policy and pending/posted, listed transactions T-4001 and T-4002, and retrieved notes: the customer said their dog is Biscuit and they plan an Oslo trip in March (not verified). Assistant offered a travel notice once dates are known; no case opened. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | turns that leave the working-memory window are compacted into an episode mid-session | `episode ids: ['E-long-s1-1', 'E-long-s1-2', 'E-long-s1-3']` |
| PASS | episodic | the out-of-window detail is recalled from that episode | `[{"query": "dog's name; travel plans in March"}]` |
| PASS | episodic | ...and answered correctly | `From my notes on an earlier conversation today: you mentioned your dog is Biscuit, and that you were planning an Oslo trip in March. Neither is verified, and no travel notice is on file for you - so if Oslo is firm, tell …` |
