# adk · adversarial · run 1 · g8-overflow

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## long-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Just chatting first: my dog's name is Biscuit and I'm planning a trip to Oslo in March.

**Assistant:** Biscuit is a great name. For the Oslo trip - I can add a travel notice to your account once you know your dates (I just need the destination and the date you return), so Kestrel knows you'll be using the card abroad. Want me to set that up now or closer to March?

**Customer:** What is a chargeback, in one sentence?

**Assistant:** A chargeback is a reversal of a card payment, where the card issuer takes the money back from the merchant and credits it to you, typically after you dispute a charge.

**Customer:** What's an authorization hold, in one sentence?

**Assistant:** An authorization hold is a temporary reservation of part of your available credit when a merchant checks your card, which usually drops off within a few days (or longer for things like hotel or car rental deposits) and is replaced by the actual charge.

**Customer:** What foreign transaction fee does Kestrel charge?

- `search_policy({"question": "foreign transaction fee"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.858, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "travel-notices",  …`

**Assistant:** Kestrel charges 1.25% of the US-dollar amount on every purchase made in a currency other than USD, and it posts as a separate line on the same day as the purchase. A travel notice doesn't waive it.

**Customer:** How long do I have to dispute a charge?

- `search_policy({"question": "dispute deadline how long to dispute a charge"})` → `{"documents": [{"document": "dispute-window", "score": 0.783, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** You have 75 days from the transaction's posting date to dispute it through me. After that, it can't be opened here and would need to go in as a written claim.

**Customer:** How fast is a replacement card?

- `search_policy({"question": "replacement card delivery time"})` → `{"documents": [{"document": "card-replacement", "score": 0.753, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.655, "text": "# Dispute window\n …`

**Assistant:** A replacement ships within 5 business days at no charge. Note that you'd need to give the new card number to any recurring merchants yourself - Kestrel doesn't forward it.

**Customer:** What contact channels can you use?

- `search_policy({"question": "contact channel options"})` → `{"documents": [{"document": "contact-preferences", "score": 0.702, "text": "# Contact preferences\n\nKestrel can contact you about cases and reminders by **email**, **sms** (text message), or **secure_message** (the inbox in the Kestrel app). If you have not chosen a channel, Kestrel uses secure_message. Changing your contact channel requires identity verification, because a changed channel is a c …`

**Assistant:** Three options: email, SMS (text message), or secure message in the Kestrel app inbox. If no channel is chosen, Kestrel uses secure message - which is your current setting. Changing it requires identity verification. Want to switch to email or SMS?

**Customer:** What is a travel notice for?

**Assistant:** A travel notice tells Kestrel's fraud systems that card use in another country is expected, which reduces false declines while you travel. You give the destination and the return date; Kestrel keeps it only until that return date and deletes it automatically, so each new trip needs a new notice.

Want me to add Oslo now? I'd need your return date.

**Customer:** What happens after a dispute is filed?

**Assistant:** Here's the flow, per Kestrel's rules:

- **Filing:** you get a case id, and a status follow-up is scheduled automatically to the contact channel on file when it's sent - with none set, that's a secure message in the Kestrel app.
- **Review:** Kestrel's disputes team reviews the case (currently about 10 days) and forwards it to the merchant.
- **Merchant:** has 10 business days to respond.
- **Decision:** the disputes team decides the case and records the outcome and its reason on the case.

Disputes must be filed within 75 days of the charge's posting date. You can also add more evidence to an open case at any point while it's undecided.

**Customer:** Do travel notices change fees?

- `search_policy({"question": "foreign transaction fee and travel notice"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.799, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "travel-notices",  …`

**Assistant:** No. A travel notice only helps prevent false declines - it doesn't change or waive any fee. The foreign transaction fee is 1.25% of the US-dollar amount on every purchase made in a currency other than USD, and it posts as a separate line the same day as the purchase.

**Customer:** What is a cancelled-subscription dispute?

**Assistant:** It's a dispute for a recurring subscription or membership charge that hit your card after you cancelled. Kestrel sends it to the merchant, who has 10 business days to respond; the disputes team then decides the case and records the outcome. Charges made before you cancelled are valid and can't be disputed on this ground.

**Customer:** Can you show my CloudNest charges?

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`

**Assistant:** Two CloudNest charges:

| Transaction | Posted | Description | Amount |
|---|---|---|---|
| T-4001 | 2026-10-01 | CloudNest 2TB monthly | $9.99 |
| T-4002 | 2026-11-01 | CloudNest 2TB monthly | $9.99 |

Both are within the 75-day dispute window. Let me know if you want to dispute either one.

**Customer:** What's the difference between a pending and a posted charge, in one sentence?

**Assistant:** A pending charge is an authorization hold that reduces your available credit while the merchant finalizes the transaction, whereas a posted charge is the settled amount that appears on your statement and starts the 75-day dispute clock.

**Customer:** What did I say my dog's name was, and where am I going in March?

- `load_memory({"query": "dog's name; travel plans in March"})` → `{"result": "memories=[MemoryEntry(content=Content(\n  parts=[\n    Part(\n      text='Conversation on 2026-11-24: Customer said dog Biscuit and Oslo trip in March (not verified). They asked about chargeback, authorization hold, Kestrel\u2019s foreign transaction fee, and dispute deadline. Assistant explained each, cited 1.25% foreign fee and 75-day dispute window, and offered a travel notice once  …`

**Assistant:** From an earlier conversation I have: your dog is Biscuit, and you mentioned a trip to Oslo in March.

Note that no travel notice is on file for your account - so if you want Oslo added, tell me your return date and I'll record it.

_Episode written:_ Conversation on 2026-11-24: Customer asked about cancelled-subscription disputes, CloudNest charges, pending vs posted charges, and recalled dog/travel details. Assistant explained definitions, listed transactions T-4001 and T-4002 (both within 75 days), and offered to dispute either; no case was opened. Assistant said the customer said dog Biscuit and March Oslo trip (not verified); no travel notice on file, and offered to record one. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | turns that leave the working-memory window are compacted into an episode mid-session | `episode ids: ['E-long-s1-1-9f02c4', 'E-long-s1-2-1046a1', 'E-long-s1-3-c7b0fb']` |
| PASS | episodic | the out-of-window detail is recalled from that episode | `[{"query": "dog's name; travel plans in March"}]` |
| PASS | episodic | ...and answered correctly | `From an earlier conversation I have: your dog is Biscuit, and you mentioned a trip to Oslo in March.  Note that no travel notice is on file for your account - so if you want Oslo added, tell me your return date and I'll  …` |
