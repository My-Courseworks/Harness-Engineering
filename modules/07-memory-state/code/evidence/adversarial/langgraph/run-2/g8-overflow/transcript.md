# langgraph · adversarial · run 2 · g8-overflow

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## long-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Just chatting first: my dog's name is Biscuit and I'm planning a trip to Oslo in March.

**Assistant:** Nice to meet you and Biscuit! I can't store notes about pets, but I can add a travel notice for Oslo to your profile once your dates are set, so card use abroad doesn't get flagged. Just tell me your travel dates (and when you're back) when you know them.

Anything else I can help with today?

**Customer:** What is a chargeback, in one sentence?

**Assistant:** A chargeback is a process where your card issuer reverses a disputed charge and pushes the money back to you while the bank investigates your claim with the merchant.

**Customer:** What's an authorization hold, in one sentence?

**Assistant:** An authorization hold is a temporary reserve your card issuer places on part of your available credit when a merchant checks your card, which reduces your available balance until the charge settles or the hold expires.

**Customer:** What foreign transaction fee does Kestrel charge?

- `search_policy({"question": "foreign transaction fee"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.858, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "travel-notices",  …`

**Assistant:** Kestrel charges 1.25% of the US-dollar amount on every purchase made in a currency other than USD; the fee posts as a separate line on the same day as the purchase. Note that a travel notice doesn't waive it.

**Customer:** How long do I have to dispute a charge?

- `search_policy({"question": "time limit to dispute a charge deadline"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.722, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`

**Assistant:** You have 75 days from the transaction's posting date to dispute a posted charge. After that, the case can't be opened through this chat and would need to go as a written claim.

**Customer:** How fast is a replacement card?

- `search_policy({"question": "replacement card delivery time"})` → `{"documents": [{"document": "card-replacement", "score": 0.753, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.655, "text": "# Dispute window\n …`

**Assistant:** A replacement card ships within 5 business days at no charge (Kestrel blocks the old card as soon as it's reported lost or stolen). Note that you'd need to give the new number to any recurring merchants yourself - Kestrel doesn't forward it.

**Customer:** What contact channels can you use?

- `search_policy({"question": "contact channels options email sms secure message"})` → `{"documents": [{"document": "contact-preferences", "score": 0.759, "text": "# Contact preferences\n\nKestrel can contact you about cases and reminders by **email**, **sms** (text message), or **secure_message** (the inbox in the Kestrel app). If you have not chosen a channel, Kestrel uses secure_message. Changing your contact channel requires identity verification, because a changed channel is a c …`

**Assistant:** Three options: email, SMS (text message), or secure message in the Kestrel app. With none chosen, Kestrel defaults to secure message that in-app inbox. Changing the channel requires identity verification (last 4 digits of your card and billing ZIP), so just say the word if you want to switch.

**Customer:** What is a travel notice for?

**Assistant:** A travel notice tells Kestrel's fraud systems that card use in another country is expected, which reduces false declines while you're away. Give the destination and your return date-Kestrel deletes the notice automatically after that date, so a new trip needs a new notice.

**Customer:** What happens after a dispute is filed?

- `search_policy({"question": "what happens after a dispute is filed review timeline"})` → `{"documents": [{"document": "dispute-window", "score": 0.729, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** Kestrel's disputes team reviews the case and forwards it to the merchant; the merchant then has 10 business days to respond, and the team decides the outcome and records it with its reason on the case. Filing also schedules an automatic follow-up that reports the status to you. Disputes are currently reviewed in about 10 days, and you can dispute a posted transaction within 75 days of its posting date.

**Customer:** Do travel notices change fees?

- `search_policy({"question": "travel notice foreign transaction fee effect"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.781, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "travel-notices",  …`

**Assistant:** No. A travel notice only reduces false declines; it doesn't change or waive fees. The foreign transaction fee is 1.25% of the US-dollar amount on any purchase made in a currency other than USD, and it posts as a separate line on the same day as the purchase.

**Customer:** What is a cancelled-subscription dispute?

- `search_policy({"question": "cancelled subscription dispute"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.809, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`

**Assistant:** It's a dispute for a recurring subscription or membership charge that came after you cancelled. Kestrel sends it to the merchant, who has 10 business days to respond; the disputes team then decides the case and records the outcome. Charges made before you cancelled are valid and can't be disputed on this ground. As with any dispute, it must be within 75 days of the charge's posting date.

If you've got a charge like that, tell me the merchant and I can look it up.

**Customer:** Can you show my CloudNest charges?

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`

**Assistant:** Two CloudNest Storage charges, both $9.99:

- **T-4001** - posted 2026-10-01, "CloudNest 2TB monthly"
- **T-4002** - posted 2026-11-01, "CloudNest 2TB monthly"

Let me know if either needs disputing.

**Customer:** What's the difference between a pending and a posted charge, in one sentence?

**Assistant:** A pending charge is an authorization that temporarily holds funds while a transaction settles, whereas a posted charge is the finalized amount that has actually been applied to your account and appears on your statement.

**Customer:** What did I say my dog's name was, and where am I going in March?

- `load_memory({"query": "dog's name and March travel destination"})` → `{"memories": [{"at": "2026-11-24T10:16:00Z", "text": "Conversation on 2026-11-24: The customer said their dog is Biscuit and they plan an Oslo trip in March (not verified). They asked about chargeback, authorization hold, foreign transaction fee, and dispute deadline. Assistant explained these, cited 1.25% fee (travel notice doesn't waive), 75 days from posting, and offered travel notice once date …`

**Assistant:** From an earlier conversation, you mentioned your dog is **Biscuit** and that you were planning a trip to **Oslo** in March.

One note on the trip: there's no travel notice on file for your account right now, so if you'd like one added once your dates are set, just tell me the destination and return date.

_Episode written:_ Conversation on 2026-11-24: Customer asked about cancelled-subscription disputes, wanted CloudNest charges shown, and asked pending vs posted. Assistant listed T-4001 (2026-10-01) and T-4002 (2026-11-01), both $9.99, with no case opened, and offered travel notice once dates are set. The customer said their dog is Biscuit and they plan an Oslo trip in March (not verified). Case outcomes: no case touched. Lesson: When repeating personal details recalled from memory, explicitly label them as unverified if the memory does.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | turns that leave the working-memory window are compacted into an episode mid-session | `episode ids: ['E-long-s1-1-a032d4', 'E-long-s1-2-475fd8', 'E-long-s1-3-e384c8']` |
| PASS | episodic | the out-of-window detail is recalled from that episode | `[{"query": "dog's name and March travel destination"}]` |
| PASS | episodic | ...and answered correctly | `From an earlier conversation, you mentioned your dog is **Biscuit** and that you were planning a trip to **Oslo** in March.  One note on the trip: there's no travel notice on file for your account right now, so if you'd  …` |
