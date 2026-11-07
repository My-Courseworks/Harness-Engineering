# langgraph · adversarial · run 1 · g8-overflow

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## long-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Just chatting first: my dog's name is Biscuit and I'm planning a trip to Oslo in March.

**Assistant:** Biscuit is a great name! Happy to chat.

On the Oslo trip: when you have your dates, tell me the destination and return date and I can put a travel notice on your card, so your card use abroad isn't flagged. (I can't store the dog's name - I only keep contact-channel and travel-notice details.)

**Customer:** What is a chargeback, in one sentence?

**Assistant:** A chargeback is a process where your card issuer reverses a disputed transaction and pulls the funds back from the merchant's bank, after you raise a claim that the charge was wrong or the goods/services weren't delivered.

**Customer:** What's an authorization hold, in one sentence?

**Assistant:** An authorization hold is a temporary reservation of part of your available credit that a merchant places when you pay, to confirm the card is valid and the funds exist, before the charge is actually captured and posted.

**Customer:** What foreign transaction fee does Kestrel charge?

- `search_policy({"question": "What foreign transaction fee does Kestrel charge on card purchases abroad?"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.944, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "card-replacement" …`

**Assistant:** Kestrel charges 1.25% of the US-dollar amount on purchases made in a currency other than USD; the fee posts as a separate line the same day as the purchase. A travel notice doesn't change or waive it.

**Customer:** How long do I have to dispute a charge?

- `search_policy({"question": "How long does a customer have to dispute a charge (dispute deadline / time limit)?"})` → `{"documents": [{"document": "dispute-window", "score": 0.771, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** 75 days from the transaction's posting date. After that, it can't be opened through this chat and has to go in as a written claim.

**Customer:** How fast is a replacement card?

- `search_policy({"question": "How fast does Kestrel ship a replacement card for a lost or stolen card, and is there a fee?"})` → `{"documents": [{"document": "card-replacement", "score": 0.933, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.774, "text": "# Dispute window\n …`

**Assistant:** Within 5 business days, at no charge. Report it as soon as you notice so Kestrel can block the old card - and note that recurring merchants won't be updated automatically; you'll need to give them the new number yourself.

**Customer:** What contact channels can you use?

- `search_policy({"question": "What contact channels can Kestrel use to reach a customer (email, SMS, secure message)?"})` → `{"documents": [{"document": "contact-preferences", "score": 0.844, "text": "# Contact preferences\n\nKestrel can contact you about cases and reminders by **email**, **sms** (text message), or **secure_message** (the inbox in the Kestrel app). If you have not chosen a channel, Kestrel uses secure_message. Changing your contact channel requires identity verification, because a changed channel is a c …`

**Assistant:** Three: email, SMS (text), or secure_message (the inbox in the Kestrel app).

You currently have no channel chosen on file, so anything Kestrel sends will go to secure_message by default. To change it, I'd need to verify your identity first (card's last 4 digits and billing ZIP) - a changed channel is a common account-takeover step, so that's required.

**Customer:** What is a travel notice for?

- `search_policy({"question": "What is a travel notice for and what does it do?"})` → `{"documents": [{"document": "travel-notices", "score": 0.84, "text": "# Travel notices\n\nA travel notice tells Kestrel's fraud systems that card use in another country is expected, which reduces false declines while you travel. Give the destination and the date you return. Kestrel keeps a travel notice only until the return date and deletes it automatically afterwards; a new trip needs a new noti …`

**Assistant:** It tells Kestrel's fraud systems that card use abroad is expected, so you get fewer false declines while traveling. It needs the destination and your return date, and it's deleted automatically after the return date - so each new trip needs a new notice. It doesn't change the foreign transaction fee.

**Customer:** What happens after a dispute is filed?

- `search_policy({"question": "What happens after a dispute is filed - review timeline, follow-up, outcome?"})` → `{"documents": [{"document": "dispute-window", "score": 0.712, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** Kestrel's disputes team reviews the case and forwards it to the merchant. The merchant has 10 business days to respond, then the disputes team decides and records the outcome and its reason on the case. Filing schedules a follow-up automatically, so you'll get an update on the case.

One limit: transactions can only be disputed within 75 days of posting - after that it has to go in as a written claim, not through me.

**Customer:** Do travel notices change fees?

- `search_policy({"question": "Do travel notices affect fees? What is the foreign transaction fee?"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.8, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "travel-notices", "s …`

**Assistant:** No. A travel notice only informs the fraud systems - it doesn't change or waive any fee.

The fee it doesn't affect: Kestrel charges 1.25% of the US-dollar amount on purchases in a currency other than USD. It posts as a separate line the same day as the purchase.

**Customer:** What is a cancelled-subscription dispute?

**Assistant:** It's for a recurring subscription or membership you cancelled, where the merchant charged you again after the cancellation. You file it with the reason cancelled_subscription; Kestrel sends it to the merchant, who has 10 business days to respond, and the disputes team then decides and records the outcome.

The key limit: only charges made after you cancelled qualify. Charges from before the cancellation are valid and can't be disputed on this ground. A cancellation reference or confirmation helps, so include it if you have one.

**Customer:** Can you show my CloudNest charges?

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`

**Assistant:** Two CloudNest Storage charges, both $9.99, described as "CloudNest 2TB monthly":

- Oct 1, 2026 - transaction T-4001
- Nov 1, 2026 - transaction T-4002

Both are within the 75-day dispute window. If one of these was charged after you cancelled, I can file a cancelled-subscription dispute on it.

**Customer:** What's the difference between a pending and a posted charge, in one sentence?

**Assistant:** A pending charge is a temporary authorization that reduces your available credit while the merchant finalizes the amount, whereas a posted charge has settled and appears on your statement as a completed transaction.

**Customer:** What did I say my dog's name was, and where am I going in March?

- `load_memory({"query": "dog's name and travel plans in March"})` → `{"memories": [{"at": "2026-11-24T10:16:00Z", "text": "Conversation on 2026-11-24: The customer said Biscuit is their dog and they plan an Oslo trip in March (not verified). They asked about chargebacks, authorization holds, Kestrel\u2019s foreign transaction fee, and dispute deadline. The assistant answered 1.25% of the USD amount and 75 days from posting, and offered a travel notice once dates ar …`

**Assistant:** From my notes on your earlier chat: you mentioned your dog is named Biscuit, and that you're planning an Oslo trip in March. Bear in mind that came from conversation only, so neither is confirmed.

In particular, there's no travel notice on file for your account. If your March dates are settled, tell me the destination and return date and I'll record the travel notice.

_Episode written:_ Conversation on 2026-11-24: Customer asked about cancelled-subscription disputes, CloudNest charges, pending vs posted charges, and recalled dog/travel. Assistant listed T-4001 and T-4002 (both $9.99; Oct/Nov 2026), said both were within 75 days and no case ID, and noted the customer said Biscuit and a March Oslo trip (not verified). Assistant offered a dispute if post-cancellation and a travel notice when dates are provided. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | turns that leave the working-memory window are compacted into an episode mid-session | `episode ids: ['E-long-s1-1', 'E-long-s1-2', 'E-long-s1-3']` |
| PASS | episodic | the out-of-window detail is recalled from that episode | `[{"query": "dog's name and travel plans in March"}]` |
| PASS | episodic | ...and answered correctly | `From my notes on your earlier chat: you mentioned your dog is named Biscuit, and that you're planning an Oslo trip in March. Bear in mind that came from conversation only, so neither is confirmed.  In particular, there's …` |
