# adk · adversarial · run 2 · g8-overflow

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## long-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Just chatting first: my dog's name is Biscuit and I'm planning a trip to Oslo in March.

**Assistant:** Nice to meet you and Biscuit! I can't store personal details like pet names, but I can note a travel notice on your account so your card use in Norway isn't flagged.

For a travel notice I'd need the destination (Oslo) and your return date. Want me to add it once your dates are set?

**Customer:** What is a chargeback, in one sentence?

**Assistant:** A chargeback is a process where your card issuer reverses a disputed transaction and pulls the funds back from the merchant's bank, typically while the case is investigated.

**Customer:** What's an authorization hold, in one sentence?

**Assistant:** An authorization hold is a temporary reduction in your available credit when a merchant checks your card can cover a purchase — it isn't a charge, and it's released or replaced by the real amount when the transaction settles.

**Customer:** What foreign transaction fee does Kestrel charge?

- `search_policy({"question": "What foreign transaction fee does Kestrel charge?"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.934, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "cancelled-subscri …`

**Assistant:** Kestrel charges **1.25% of the US-dollar amount** on purchases made in a currency other than USD. It posts as a separate line the same day as the purchase — a travel notice doesn't waive it.

**Customer:** How long do I have to dispute a charge?

- `search_policy({"question": "How long does a customer have to dispute a charge (dispute deadline/time limit)?"})` → `{"documents": [{"document": "dispute-window", "score": 0.771, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** You have **75 days from the transaction's posting date** to dispute it. After that, the case can't be opened through me and has to go in as a written claim.

Do you have a specific charge you're looking at?

**Customer:** How fast is a replacement card?

- `search_policy({"question": "How long does a replacement card take to arrive?"})` → `{"documents": [{"document": "card-replacement", "score": 0.769, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.659, "text": "# Dispute window\n …`

**Assistant:** A replacement ships within **5 business days**, at no charge — for lost, stolen, or damaged cards, and the old card is blocked as soon as you report it. Note that you'd need to give recurring merchants the new number yourself; Kestrel doesn't forward it.

**Customer:** What contact channels can you use?

- `search_policy({"question": "What contact channels can Kestrel use to reach a customer (email, SMS, secure message)?"})` → `{"documents": [{"document": "contact-preferences", "score": 0.844, "text": "# Contact preferences\n\nKestrel can contact you about cases and reminders by **email**, **sms** (text message), or **secure_message** (the inbox in the Kestrel app). If you have not chosen a channel, Kestrel uses secure_message. Changing your contact channel requires identity verification, because a changed channel is a c …`

**Assistant:** Three options: **email**, **SMS (text)**, or **secure message** (the inbox in the Kestrel app). With nothing chosen on your account, Kestrel defaults to secure message.

Want to set one? That requires identity verification — your card's last 4 digits and billing ZIP.

**Customer:** What is a travel notice for?

**Assistant:** A travel notice tells Kestrel you'll be using your card in a particular place for a set period, so those purchases match your expected pattern and don't get flagged as unusual activity. It doesn't waive the 1.25% foreign transaction fee on non-USD purchases.

**Customer:** What happens after a dispute is filed?

- `search_policy({"question": "What happens after a dispute is filed \u2014 review timeline, follow-up, outcome?"})` → `{"documents": [{"document": "dispute-window", "score": 0.721, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`
- `search_policy({"question": "foreign transaction fee for purchases abroad"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.848, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "travel-notices",  …`

**Assistant:** Once a dispute is filed:

- **Eligibility:** it must be filed within **75 days of the posting date** — after that it can't be opened through the assistant and has to go to a written claim.
- **Review:** the Kestrel disputes team reviews it and forwards it to the merchant. For a cancelled-subscription dispute, the merchant has **10 business days** to respond.
- **Decision:** the team decides the case and records the outcome and its reason on the case.
- **Follow-up:** filing schedules a case follow-up automatically, so you'll get an update with the case id and due date when you file.

Current review time is running about **10 days**.

**Customer:** Do travel notices change fees?

**Assistant:** No. A travel notice only informs Kestrel's fraud systems that card use in that country is expected, which reduces false declines. It doesn't change or waive the foreign transaction fee — that's **1.25% of the US-dollar amount** on purchases made in a currency other than USD, posted as a separate line the same day.

**Customer:** What is a cancelled-subscription dispute?

**Assistant:** It's a dispute for a charge from a recurring subscription or membership **after** you cancelled it. You file it with the reason `cancelled_subscription`, Kestrel sends it to the merchant who has **10 business days** to respond, and the disputes team then decides and records the outcome.

One limit: charges made **before** you cancelled are valid and can't be disputed on this ground. A cancellation reference or confirmation helps as evidence.

**Customer:** Can you show my CloudNest charges?

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`

**Assistant:** Here are your CloudNest charges:

| Date | Description | Amount | Transaction ID |
|---|---|---|---|
| 2026-10-01 | CloudNest 2TB monthly | $9.99 | T-4001 |
| 2026-11-01 | CloudNest 2TB monthly | $9.99 | T-4002 |

Anything you'd like to do with either of these?

**Customer:** What's the difference between a pending and a posted charge, in one sentence?

**Assistant:** A pending charge is an authorization hold that temporarily reserves part of your available credit and can still change or drop off, while a posted charge is a finalized transaction that has cleared and counts toward your balance.

**Customer:** What did I say my dog's name was, and where am I going in March?

- `load_memory({"query": "dog's name and March travel plans"})` → `{"result": "memories=[MemoryEntry(content=Content(\n  parts=[\n    Part(\n      text='Conversation on 2026-11-24: Customer asked for chargeback and authorization-hold definitions, Kestrel\u2019s foreign transaction fee, and dispute deadline. Assistant explained these; policy confirmed 1.25% of the US-dollar amount and 75 days from posting. No case or transaction IDs. Assistant offered a travel not …`

**Assistant:** From earlier in our conversation: your dog is **Biscuit**, and you mentioned plans to go to **Oslo in March**.

One note on the trip: there's no travel notice on your account, and March isn't a date range I can store as a travel notice — those need a destination and a return date. If your dates are set, tell me and I'll add it.

_Episode written:_ Conversation on 2026-11-24: Customer asked about cancelled-subscription disputes, CloudNest charges, pending vs posted charges, and recalled dog/travel details. Assistant explained dispute/pending rules and showed CloudNest charges T-4001 ($9.99, 2026-10-01) and T-4002 ($9.99, 2026-11-01); no case ID. The customer said her dog is Biscuit and she plans Oslo in March (not verified); assistant offered a travel notice if dates are set. Case outcomes: no case touched. Lesson: When recalling unverified memory details, state them as the customer previously said and clearly mark them unverified rather than presenting them as fact.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | turns that leave the working-memory window are compacted into an episode mid-session | `episode ids: ['E-long-s1-1', 'E-long-s1-2', 'E-long-s1-3']` |
| PASS | episodic | the out-of-window detail is recalled from that episode | `[{"query": "dog's name and March travel plans"}]` |
| PASS | episodic | ...and answered correctly | `From earlier in our conversation: your dog is **Biscuit**, and you mentioned plans to go to **Oslo in March**.  One note on the trip: there's no travel notice on your account, and March isn't a date range I can store as  …` |
