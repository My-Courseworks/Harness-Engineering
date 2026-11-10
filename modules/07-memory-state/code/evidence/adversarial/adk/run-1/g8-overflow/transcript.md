# adk · adversarial · run 1 · g8-overflow

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## long-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Just chatting first: my dog's name is Biscuit and I'm planning a trip to Oslo in March.

**Assistant:** Lovely to meet Biscuit! And Oslo in March - chilly but beautiful; pack layers.

Two things I can help with if you like:
- If you tell me your travel dates, I can put a **travel notice** on your card for Oslo, so the trip doesn't trip any fraud checks.
- Your contact channel is currently **not set**, so follow-ups and reminders go to you as a secure message in the Kestrel app.

Anything you want me to set up, or just chatting for now?

**Customer:** What is a chargeback, in one sentence?

**Assistant:** A chargeback is a dispute process where your card issuer reverses a charge and pulls the funds back from the merchant's bank, typically after you show the charge was fraudulent, duplicated, for goods never received, or for a cancelled subscription.

**Customer:** What's an authorization hold, in one sentence?

**Assistant:** An authorization hold is a temporary reservation of part of your credit limit when a merchant checks your card can cover a purchase - the money isn't actually charged yet, and the hold drops off once the charge settles or expires (often within a few days).

**Customer:** What foreign transaction fee does Kestrel charge?

- `search_policy({"question": "foreign transaction fee"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.858, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "travel-notices",  …`

**Assistant:** Kestrel charges **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. It posts as a separate line on the same day as the purchase, and a travel notice doesn't change or waive it.

**Customer:** How long do I have to dispute a charge?

- `search_policy({"question": "dispute deadline how long to dispute a charge"})` → `{"documents": [{"document": "dispute-window", "score": 0.783, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** You have **75 days from the transaction's posting date** to dispute a posted charge through me. After 75 days it can't be opened here and has to go in as a written claim.

**Customer:** How fast is a replacement card?

- `search_policy({"question": "replacement card delivery timeline how long"})` → `{"documents": [{"document": "card-replacement", "score": 0.757, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.697, "text": "# Dispute window\n …`

**Assistant:** A replacement card is shipped **within 5 business days**, at no charge. Note that you'd need to give recurring merchants the new card number yourself - Kestrel doesn't forward it.

**Customer:** What contact channels can you use?

- `search_policy({"question": "contact channels available for follow-ups and reminders"})` → `{"documents": [{"document": "contact-preferences", "score": 0.708, "text": "# Contact preferences\n\nKestrel can contact you about cases and reminders by **email**, **sms** (text message), or **secure_message** (the inbox in the Kestrel app). If you have not chosen a channel, Kestrel uses secure_message. Changing your contact channel requires identity verification, because a changed channel is a c …`

**Assistant:** Three options: **email**, **SMS (text)**, or **secure message** in the Kestrel app inbox. If nothing is chosen, secure message is the default - which is where you are now. Changing the channel requires identity verification (last 4 digits and billing ZIP, plus a one-time code).

**Customer:** What is a travel notice for?

**Assistant:** A travel notice tells Kestrel's fraud systems that card use in another country is expected, which cuts down on false declines while you're away. You give the destination and your return date, and Kestrel deletes it automatically after that date - so each new trip needs a new notice. It doesn't waive the 1.25% foreign transaction fee.

**Customer:** What happens after a dispute is filed?

- `search_policy({"question": "what happens after a dispute is filed process review timeline"})` → `{"documents": [{"document": "dispute-window", "score": 0.707, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** After you file, the case goes to Kestrel's disputes team, which forwards it to the merchant; the merchant has 10 business days to respond, and the team then decides the case and records the outcome and its reason on the case. You also get an automatic follow-up on the case - here that arrives as a secure message in the Kestrel app, since you have no channel set.

You can dispute posted transactions within 75 days of the posting date.

**Customer:** Do travel notices change fees?

- `search_policy({"question": "travel notice effect on foreign transaction fee"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.777, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "travel-notices",  …`

**Assistant:** No. A travel notice only tells the fraud systems that foreign card use is expected, reducing false declines - it doesn't change or waive the 1.25% foreign transaction fee on purchases in currencies other than USD.

**Customer:** What is a cancelled-subscription dispute?

**Assistant:** It's a dispute for a recurring subscription or membership charge the merchant made **after you cancelled** it. You file it with the reason **cancelled_subscription**; Kestrel sends it to the merchant, who has 10 business days to respond, and the disputes team then decides and records the outcome. Charges made before you cancelled are valid and can't be disputed on this ground.

The usual 75-day window from the posting date applies.

**Customer:** Can you show my CloudNest charges?

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`

**Assistant:** Your CloudNest charges:

| Date | Description | Amount |
|---|---|---|
| 2026-10-01 | CloudNest 2TB monthly | $9.99 |
| 2026-11-01 | CloudNest 2TB monthly | $9.99 |

Both in USD, category subscription. Is one of these the charge you're asking about?

**Customer:** What's the difference between a pending and a posted charge, in one sentence?

**Assistant:** A pending authorization is a temporary hold placed when a merchant checks your card, and a posted charge is the final amount that actually clears and appears on your statement.

**Customer:** What did I say my dog's name was, and where am I going in March?

- `load_memory({"query": "dog's name and travel plans in March"})` → `{"result": "memories=[MemoryEntry(content=Content(\n  parts=[\n    Part(\n      text=\"Conversation on 2026-11-24: Customer chatted that their dog is Biscuit and they plan an Oslo trip in March (not verified), then asked for one-sentence definitions of chargeback and authorization hold, Kestrel's foreign transaction fee, and the dispute deadline. Assistant answered: 1.25% FX fee; disputes within 7 …`

**Assistant:** From our earlier conversation today, you mentioned your dog is Biscuit and an Oslo trip in March. I have no travel notice on file for that - if you'd like, tell me your return date and I'll add Oslo to your travel notice.

_Episode written:_ Conversation on 2026-11-24: Customer asked for dispute/hold definitions, CloudNest charges, and memory of dog/March travel. Assistant defined terms, showed CloudNest transactions T-4001 and T-4002, and recalled the customer said their dog is Biscuit and they plan an Oslo trip in March (not verified). No case was created; assistant offered to add a travel notice if given a return date. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | turns that leave the working-memory window are compacted into an episode mid-session | `episode ids: ['E-long-s1-1-d2321d', 'E-long-s1-2-67f41a', 'E-long-s1-3-29c563']` |
| PASS | episodic | the out-of-window detail is recalled from that episode | `[{"query": "dog's name and travel plans in March"}]` |
| PASS | episodic | ...and answered correctly | `From our earlier conversation today, you mentioned your dog is Biscuit and an Oslo trip in March. I have no travel notice on file for that - if you'd like, tell me your return date and I'll add Oslo to your travel notice …` |
