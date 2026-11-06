# langgraph · adversarial · run 2 · g8-overflow

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## long-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Just chatting first: my dog's name is Biscuit and I'm planning a trip to Oslo in March.

**Assistant:** Nice to meet Biscuit! And Oslo in March sounds great — though bring warm layers, it's still chilly then.

If you'd like, I can add a travel notice to your account once you have your dates — I'd just need the destination (Oslo) and your return date. That way Kestrel knows to expect card use abroad and won't flag it as unusual. Want me to set that up now, or wait until your plans firm up?

**Customer:** What is a chargeback, in one sentence?

**Assistant:** A chargeback is a process where you ask your card issuer to reverse a card payment — typically by disputing it with the merchant's bank — and get the money credited back if the claim is upheld.

**Customer:** What's an authorization hold, in one sentence?

**Assistant:** An authorization hold is a temporary reservation of part of your available credit (or balance) made when a merchant checks your card, which reduces your available limit until the transaction settles or the hold expires.

**Customer:** What foreign transaction fee does Kestrel charge?

- `search_policy({"question": "What foreign transaction fee does Kestrel charge?"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.934, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "cancelled-subscri …`

**Assistant:** Kestrel charges **1.25% of the US-dollar amount** on every purchase made in a non-USD currency, posted as a separate line on the same day as the purchase. A travel notice doesn't waive it.

**Customer:** How long do I have to dispute a charge?

- `search_policy({"question": "How long does a customer have to dispute a charge (dispute deadline / time limit)?"})` → `{"documents": [{"document": "dispute-window", "score": 0.771, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** **75 days from the transaction's posting date.** After that, a case can't be opened through the assistant — it would have to go in as a written claim to Kestrel.

**Customer:** How fast is a replacement card?

- `search_policy({"question": "How long does it take to receive a replacement card (delivery timeline)?"})` → `{"documents": [{"document": "card-replacement", "score": 0.757, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.682, "text": "# Dispute window\n …`

**Assistant:** Kestrel ships a replacement within **5 business days**, at no charge. If the card is lost or stolen, report it right away so it can be blocked immediately — and note that you'll need to give recurring merchants the new card number yourself, since Kestrel doesn't forward it.

**Customer:** What contact channels can you use?

- `search_policy({"question": "What contact channels can Kestrel use to reach a customer (email, SMS, secure message)?"})` → `{"documents": [{"document": "contact-preferences", "score": 0.844, "text": "# Contact preferences\n\nKestrel can contact you about cases and reminders by **email**, **sms** (text message), or **secure_message** (the inbox in the Kestrel app). If you have not chosen a channel, Kestrel uses secure_message. Changing your contact channel requires identity verification, because a changed channel is a c …`

**Assistant:** Three: **email**, **SMS (text)**, or **secure message** (the inbox in the Kestrel app). You don't have a channel set right now, so anything sent to you would go by secure message by default. Changing it requires identity verification — your card's last 4 digits and billing ZIP.

**Customer:** What is a travel notice for?

- `search_policy({"question": "What is a travel notice for and how does it work?"})` → `{"documents": [{"document": "travel-notices", "score": 0.84, "text": "# Travel notices\n\nA travel notice tells Kestrel's fraud systems that card use in another country is expected, which reduces false declines while you travel. Give the destination and the date you return. Kestrel keeps a travel notice only until the return date and deletes it automatically afterwards; a new trip needs a new noti …`

**Assistant:** A travel notice tells Kestrel's fraud systems that card use abroad is expected, which cuts down on false declines while you're away. You give the destination and return date; Kestrel keeps it only until that return date, then deletes it automatically — so each new trip needs a new notice.

For your Oslo plan, I'd just need your return date.

**Customer:** What happens after a dispute is filed?

- `search_policy({"question": "What happens after a dispute is filed \u2014 review timeline, who reviews it, follow-up?"})` → `{"documents": [{"document": "dispute-window", "score": 0.712, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** After filing, the Kestrel disputes team reviews the case and forwards it to the merchant. The merchant's response window and the review timeline depend on the dispute type — for a charge after a cancelled subscription, the merchant gets 10 business days to respond, then the disputes team decides the case and records the outcome and its reason on the case. (Currently, reviews are running about 10 days overall.)

You'll get a follow-up on the case automatically; it goes out on whatever contact channel is on file at that time.

**Customer:** Do travel notices change fees?

- `search_policy({"question": "Do travel notices change or waive foreign transaction fees?"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.763, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "travel-notices",  …`

**Assistant:** No. A travel notice only affects fraud screening — it does not change or waive fees. Kestrel charges a **1.25% foreign transaction fee on the US-dollar amount** of any purchase made in a currency other than USD; the fee posts as a separate line the same day as the purchase.

**Customer:** What is a cancelled-subscription dispute?

**Assistant:** It's a dispute reason for a recurring subscription or membership you cancelled and were then charged for anyway. Kestrel sends the dispute to the merchant, who has 10 business days to respond; the disputes team then decides the case and records the outcome.

One limit: charges made *before* you cancelled are valid and can't be disputed on this ground.

Also, a correction on my earlier message — I mentioned an "Oslo plan," but no travel notice is on file for you and you hadn't told me about a trip, so ignore that.

**Customer:** Can you show my CloudNest charges?

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`

**Assistant:** Two CloudNest Storage charges, both $9.99 for the 2TB monthly plan:

- **T-4001** — posted 2026-10-01
- **T-4002** — posted 2026-11-01

Both are within the 75-day dispute window.

**Customer:** What's the difference between a pending and a posted charge, in one sentence?

**Assistant:** A pending charge is a temporary authorization hold that reduces your available credit while the merchant finalizes the amount, whereas a posted charge is the final amount that has settled to your account and appears on your statement.

**Customer:** What did I say my dog's name was, and where am I going in March?

- `load_memory({"query": "dog's name, travel plans in March"})` → `{"memories": [{"at": "2026-11-24T10:16:00Z", "text": "Conversation on 2026-11-24: The customer said their dog is Biscuit and they plan an Oslo trip in March (not verified). They asked about chargebacks, authorization holds, Kestrel\u2019s foreign transaction fee, and the dispute deadline. Assistant explained the 1.25% non-USD fee and 75-day posting deadline. No case or transaction IDs; travel noti …`

**Assistant:** From my notes on an earlier conversation today: you said your dog is **Biscuit**, and that you were planning a trip to **Oslo in March**. Neither was verified, and no travel notice is on file for you — if you want one set up, just give me the destination and return date.

_Episode written:_ Conversation on 2026-11-24: Customer asked about cancelled-subscription disputes, pending vs posted charges, and CloudNest charges. Assistant explained and listed T-4001 and T-4002, each $9.99 and within the 75-day dispute window; no case opened. Assistant said no travel notice was on file and offered setup once destination/return date provided. The customer said their dog is Biscuit and an Oslo March trip (not verified). Case outcomes: no case touched. Lesson: Next time, check memory before correcting a prior message, so the assistant does not contradict earlier information about the customer's unverified travel plans.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | turns that leave the working-memory window are compacted into an episode mid-session | `episode ids: ['E-long-s1-1', 'E-long-s1-2', 'E-long-s1-3']` |
| PASS | episodic | the out-of-window detail is recalled from that episode | `[{"query": "dog's name, travel plans in March"}]` |
| PASS | episodic | ...and answered correctly | `From my notes on an earlier conversation today: you said your dog is **Biscuit**, and that you were planning a trip to **Oslo in March**. Neither was verified, and no travel notice is on file for you — if you want one se …` |
