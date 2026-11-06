# adk · adversarial · run 1 · g8-overflow

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## long-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Just chatting first: my dog's name is Biscuit and I'm planning a trip to Oslo in March.

**Assistant:** Nice to meet you and Biscuit! Oslo in March sounds great — though pack warm, it's still proper winter there.

Just so you know: I can only save two things to your profile — a contact channel (email, SMS or secure message) and a travel notice. If you'd like, once you have your dates I can add a travel notice for Oslo so your card use there doesn't get flagged; I'd just need your return date. What else can I help with?

**Customer:** What is a chargeback, in one sentence?

**Assistant:** A chargeback is a process where your card issuer reverses a disputed transaction and pulls the funds back from the merchant, typically after an investigation.

**Customer:** What's an authorization hold, in one sentence?

**Assistant:** An authorization hold is a temporary hold placed on part of your available credit when a merchant checks your card, which is released or converted into a real charge once the transaction settles.

**Customer:** What foreign transaction fee does Kestrel charge?

- `search_policy({"question": "What foreign transaction fee does Kestrel charge?"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.934, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "cancelled-subscri …`

**Assistant:** Kestrel charges **1.25% of the US-dollar amount** on any purchase made in a currency other than USD. It posts as a separate line the same day as the purchase, and a travel notice doesn't waive or change it.

**Customer:** How long do I have to dispute a charge?

- `search_policy({"question": "How long does a customer have to dispute a charge (dispute deadline)?"})` → `{"documents": [{"document": "dispute-window", "score": 0.782, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** You have **75 days from the transaction's posting date** to dispute a posted charge. After that, it can't be opened through me and would need to go in as a written claim.

**Customer:** How fast is a replacement card?

- `search_policy({"question": "How long does a replacement card take to arrive?"})` → `{"documents": [{"document": "card-replacement", "score": 0.769, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.659, "text": "# Dispute window\n …`

**Assistant:** A replacement card is shipped within **5 business days** at no charge. Note that recurring merchants won't be updated automatically — you'd need to give them the new card number yourself.

**Customer:** What contact channels can you use?

- `search_policy({"question": "What contact channels are available for customer messages and follow-ups?"})` → `{"documents": [{"document": "contact-preferences", "score": 0.712, "text": "# Contact preferences\n\nKestrel can contact you about cases and reminders by **email**, **sms** (text message), or **secure_message** (the inbox in the Kestrel app). If you have not chosen a channel, Kestrel uses secure_message. Changing your contact channel requires identity verification, because a changed channel is a c …`

**Assistant:** Three: **email**, **SMS**, and **secure message** (the Kestrel app inbox). You don't have a channel on file yet, so secure message is the default. Changing it requires identity verification — your card's last 4 digits and billing ZIP — if you'd like to set one.

**Customer:** What is a travel notice for?

- `search_policy({"question": "What is a travel notice for and how does it work?"})` → `{"documents": [{"document": "travel-notices", "score": 0.84, "text": "# Travel notices\n\nA travel notice tells Kestrel's fraud systems that card use in another country is expected, which reduces false declines while you travel. Give the destination and the date you return. Kestrel keeps a travel notice only until the return date and deletes it automatically afterwards; a new trip needs a new noti …`

**Assistant:** A travel notice tells Kestrel's fraud systems that card use abroad is expected, which cuts down on false declines while you're away. I'd need the destination and your return date — it's kept only until that date and then deleted automatically, so each new trip needs a new notice. Note it doesn't waive the 1.25% foreign transaction fee.

**Customer:** What happens after a dispute is filed?

- `search_policy({"question": "What happens after a dispute case is filed \u2014 the review process and timeline?"})` → `{"documents": [{"document": "dispute-window", "score": 0.722, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** After you file (within 75 days of the posting date):

- The **Kestrel disputes team reviews** the case — currently about **10 days**.
- It's then **forwarded to the merchant**, who has **10 business days** to respond.
- The disputes team decides the case and **records the outcome and its reason** on the case.
- A **follow-up is scheduled automatically** and sent to whatever contact channel is on file.

You can add more evidence to an open case at any time. Want me to look up a specific case?

**Customer:** Do travel notices change fees?

- `search_policy({"question": "Do travel notices affect or waive foreign transaction fees? What is the foreign transaction fee?"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.774, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "travel-notices",  …`

**Assistant:** No. A travel notice only tells our fraud systems to expect foreign card use — it doesn't change or waive fees. The **foreign transaction fee of 1.25% of the US-dollar amount** applies to every purchase in a non-USD currency, and posts as a separate line on the same day as the purchase.

**Customer:** What is a cancelled-subscription dispute?

**Assistant:** It's a dispute for a recurring subscription or membership charge that the merchant made **after you cancelled** it. Use the reason `cancelled_subscription`, and include any cancellation reference as evidence. Kestrel sends it to the merchant, who has **10 business days** to respond; the disputes team then decides and records the outcome. Charges made **before** you cancelled are valid and can't be disputed on this ground.

**Customer:** Can you show my CloudNest charges?

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`

**Assistant:** Your CloudNest Storage charges:

| Date | Description | Amount | Transaction |
|---|---|---|---|
| 2026-10-01 | CloudNest 2TB monthly | $9.99 USD | T-4001 |
| 2026-11-01 | CloudNest 2TB monthly | $9.99 USD | T-4002 |

Both are posted subscription charges. Let me know if you'd like to dispute either one.

**Customer:** What's the difference between a pending and a posted charge, in one sentence?

**Assistant:** A pending charge is a temporary authorization that reduces your available credit while the merchant finalizes it, whereas a posted charge is a completed transaction that has settled and appears on your statement.

**Customer:** What did I say my dog's name was, and where am I going in March?

- `load_memory({"query": "dog's name and travel plans in March"})` → `{"result": "memories=[MemoryEntry(content=Content(\n  parts=[\n    Part(\n      text='Conversation on 2026-11-24: The customer said their dog is Biscuit and they plan an Oslo trip in March (not verified). They asked about chargeback and authorization-hold definitions, Kestrel\u2019s foreign transaction fee, and dispute deadline. Assistant answered 1.25% of the US-dollar amount and 75 days from pos …`

**Assistant:** From our earlier conversation: you mentioned your dog is **Biscuit**, and that you had an **Oslo** trip planned for March — but that was never set up as an official travel notice on your account, so there's no travel notice on file right now.

Want me to add Oslo as a travel notice (and give me the return date)?

_Episode written:_ Conversation on 2026-11-24: Customer asked definitions of cancelled-subscription and pending vs posted charges, and to see CloudNest charges. Assistant explained the definitions and listed CloudNest subscription charges T-4001 and T-4002. Assistant retrieved memory: customer said their dog is Biscuit and they plan an Oslo trip in March (not verified); no travel notice was on file. No case ID or promise was made. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | turns that leave the working-memory window are compacted into an episode mid-session | `episode ids: ['E-long-s1-1', 'E-long-s1-2', 'E-long-s1-3']` |
| PASS | episodic | the out-of-window detail is recalled from that episode | `[{"query": "dog's name and travel plans in March"}]` |
| PASS | episodic | ...and answered correctly | `From our earlier conversation: you mentioned your dog is **Biscuit**, and that you had an **Oslo** trip planned for March — but that was never set up as an official travel notice on your account, so there's no travel not …` |
