# adk · adversarial · run 2 · g8-overflow

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## long-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Just chatting first: my dog's name is Biscuit and I'm planning a trip to Oslo in March.

**Assistant:** Nice to meet you and Biscuit! 🐾

Oslo in March is lovely (cold, but lovely). Two quick notes on the card side:

- I can't store your dog's name - I only keep a contact channel or a travel notice for you.
- If you'd like, I can add a **travel notice for Oslo** so your card doesn't get flagged while you're away. Just tell me the dates (or at least when you get back) and I'll set it.

**Customer:** What is a chargeback, in one sentence?

**Assistant:** A chargeback is a process where you ask your card issuer to reverse a card payment, typically by disputing it with the merchant's bank, which then decides whether you get your money back.

**Customer:** What's an authorization hold, in one sentence?

**Assistant:** An authorization hold is a temporary reduction in your available credit when a merchant checks your card can cover a purchase - the money isn't actually charged, and the hold drops off once the charge posts or expires.

**Customer:** What foreign transaction fee does Kestrel charge?

- `search_policy({"question": "foreign transaction fee"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.858, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "travel-notices",  …`

**Assistant:** Kestrel charges **1.25% of the US-dollar amount** on every purchase made in a currency other than USD; it posts as a separate line on the same day as the purchase. A travel notice doesn't waive it.

**Customer:** How long do I have to dispute a charge?

- `search_policy({"question": "dispute deadline how long to dispute a charge"})` → `{"documents": [{"document": "dispute-window", "score": 0.783, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** **75 days from the transaction's posting date.** After that, a case can't be opened through the assistant and has to go in as a written claim.

**Customer:** How fast is a replacement card?

- `search_policy({"question": "replacement card delivery time"})` → `{"documents": [{"document": "card-replacement", "score": 0.753, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.655, "text": "# Dispute window\n …`

**Assistant:** A replacement card ships **within 5 business days**, at no charge. Note that you'll need to give the new number to any recurring merchants yourself - Kestrel doesn't forward it.

**Customer:** What contact channels can you use?

- `search_policy({"question": "contact channels for follow-ups and reminders"})` → `{"documents": [{"document": "contact-preferences", "score": 0.693, "text": "# Contact preferences\n\nKestrel can contact you about cases and reminders by **email**, **sms** (text message), or **secure_message** (the inbox in the Kestrel app). If you have not chosen a channel, Kestrel uses secure_message. Changing your contact channel requires identity verification, because a changed channel is a c …`

**Assistant:** **Email, SMS, or secure message** (the Kestrel app inbox). You currently have none set, so everything goes by secure message. Changing the channel takes identity verification - just say the word if you want to switch.

**Customer:** What is a travel notice for?

**Assistant:** It tells Kestrel's fraud systems that card use abroad is expected, so you're less likely to get false declines while traveling. You give the destination and your return date - Kestrel keeps the notice only until that return date and then deletes it automatically, so a new trip needs a new notice. (It doesn't waive the 1.25% foreign transaction fee.)

You have none on file. Want me to add Oslo once you know your return date?

**Customer:** What happens after a dispute is filed?

- `search_policy({"question": "what happens after a dispute is filed process timeline"})` → `{"documents": [{"document": "dispute-window", "score": 0.715, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** Here's the flow: the case goes to Kestrel's disputes team, which reviews it and forwards it to the merchant (merchants get 10 business days to respond). The team then decides the case and records the outcome and its reason on the case. You also get a case id and an automatic follow-up, which currently reaches you by secure message in the Kestrel app since no channel is set - and disputes are currently being reviewed in about 10 days. Also note you must dispute within 75 days of the transaction posting.

**Customer:** Do travel notices change fees?

- `search_policy({"question": "foreign transaction fee and travel notice effect on fees"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.778, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "travel-notices",  …`

**Assistant:** No. A travel notice only helps with fraud detection - it reduces false declines. It does not change or waive the foreign transaction fee, which is 1.25% of the US-dollar amount on purchases in a currency other than USD, posted as a separate line the same day as the purchase.

**Customer:** What is a cancelled-subscription dispute?

**Assistant:** It's a dispute for a charge that came after you cancelled a recurring subscription or membership. You file it with the reason **cancelled_subscription**, Kestrel sends it to the merchant (who gets 10 business days to respond), and the disputes team decides it and records the outcome on the case.

One limit: charges made *before* you cancelled are valid and can't be disputed on that ground. You have 75 days from the posting date to file.

**Customer:** Can you show my CloudNest charges?

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`

**Assistant:** Two CloudNest charges:

- **T-4001** - 1 Oct 2026 - CloudNest 2TB monthly - $9.99
- **T-4002** - 1 Nov 2026 - CloudNest 2TB monthly - $9.99

Both are in USD. Need anything on either one?

**Customer:** What's the difference between a pending and a posted charge, in one sentence?

**Assistant:** A pending charge is a temporary authorization that reduces your available credit while the merchant finalizes it, and a posted charge is the completed transaction that appears on your statement and starts the clock on things like the 75-day dispute window.

**Customer:** What did I say my dog's name was, and where am I going in March?

- `load_memory({"query": "dog's name and March travel destination"})` → `{"result": "memories=[MemoryEntry(content=Content(\n  parts=[\n    Part(\n      text=\"Conversation on 2026-11-24: The customer said their dog is named Biscuit and they plan to visit Oslo in March (not verified). They asked definitions for chargeback and authorization hold, Kestrel's foreign transaction fee (1.25% of USD amount), and dispute deadline (75 days from posting). The assistant answered  …`

**Assistant:** From your earlier conversation: you said your dog is named **Biscuit**, and that you were planning to visit **Oslo** in March - though no dates were given, so it's not confirmed.

There's no travel notice on file for you right now. If the March trip is set, I can add a travel notice for Oslo with your return date.

_Episode written:_ Conversation on 2026-11-24: The customer asked definitions and CloudNest charges; the assistant explained cancelled-subscription and pending/posted charges and showed T-4001 and T-4002. The assistant offered a travel notice for Oslo with a return date if the trip is confirmed; no case or travel notice was created. The customer said their dog is Biscuit and they plan to visit Oslo in March (not verified). Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | turns that leave the working-memory window are compacted into an episode mid-session | `episode ids: ['E-long-s1-1-221c0e', 'E-long-s1-2-46c4e2', 'E-long-s1-3-067f96']` |
| PASS | episodic | the out-of-window detail is recalled from that episode | `[{"query": "dog's name and March travel destination"}]` |
| PASS | episodic | ...and answered correctly | `From your earlier conversation: you said your dog is named **Biscuit**, and that you were planning to visit **Oslo** in March - though no dates were given, so it's not confirmed.  There's no travel notice on file for you …` |
