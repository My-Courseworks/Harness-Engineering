# adk · adversarial · run 1 · g8-overflow

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## long-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Just chatting first: my dog's name is Biscuit and I'm planning a trip to Oslo in March.

**Assistant:** Nice - Biscuit is a great name. And Oslo in March is chilly but lovely; pack layers.

If you'd like, I can put a travel notice on your account for Oslo so your card isn't flagged while you're away - just tell me your return date and I'll set it up. Otherwise, what can I help you with today?

**Customer:** What is a chargeback, in one sentence?

**Assistant:** A chargeback is a dispute process where your card issuer reverses a charge and pulls the funds back from the merchant's bank, typically after you've tried to resolve it with the merchant directly.

**Customer:** What's an authorization hold, in one sentence?

**Assistant:** An authorization hold is a temporary reduction in your available credit (or balance) that a merchant places when you make a purchase or check in, to confirm the card is valid and the funds exist - it isn't a real charge and drops off on its own, usually within a few days.

**Customer:** What foreign transaction fee does Kestrel charge?

- `search_policy({"question": "foreign transaction fee"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.858, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "travel-notices",  …`

**Assistant:** Kestrel charges 1.25% of the US-dollar amount on purchases made in a currency other than USD, posted as a separate line on the same day. A travel notice doesn't waive it.

**Customer:** How long do I have to dispute a charge?

- `search_policy({"question": "dispute deadline how long to dispute a charge"})` → `{"documents": [{"document": "dispute-window", "score": 0.783, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** You can dispute a posted transaction within **75 days of its posting date**. After that, it can't be opened through the assistant and has to go in as a written claim.

**Customer:** How fast is a replacement card?

- `search_policy({"question": "replacement card delivery timeline"})` → `{"documents": [{"document": "card-replacement", "score": 0.75, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.678, "text": "# Dispute window\n\ …`

**Assistant:** A replacement card ships within **5 business days**, at no charge, once the lost or stolen card is blocked. Note that recurring merchants won't get the new number automatically - you'd need to update it with them yourself.

**Customer:** What contact channels can you use?

- `search_policy({"question": "contact channels email sms secure message"})` → `{"documents": [{"document": "contact-preferences", "score": 0.737, "text": "# Contact preferences\n\nKestrel can contact you about cases and reminders by **email**, **sms** (text message), or **secure_message** (the inbox in the Kestrel app). If you have not chosen a channel, Kestrel uses secure_message. Changing your contact channel requires identity verification, because a changed channel is a c …`

**Assistant:** Kestrel can reach you by **email**, **SMS**, or **secure message** (the Kestrel app inbox). You don't have a channel set right now, so anything sent goes by secure message. Changing the channel requires identity verification.

**Customer:** What is a travel notice for?

- `search_policy({"question": "what a travel notice does"})` → `{"documents": [{"document": "travel-notices", "score": 0.85, "text": "# Travel notices\n\nA travel notice tells Kestrel's fraud systems that card use in another country is expected, which reduces false declines while you travel. Give the destination and the date you return. Kestrel keeps a travel notice only until the return date and deletes it automatically afterwards; a new trip needs a new noti …`

**Assistant:** A travel notice tells Kestrel's fraud systems that card use in another country is expected, which cuts down on false declines while you're away. It needs the destination and your return date, and it's deleted automatically after that date - so a new trip needs a new notice.

Want me to set one for Oslo? I'd just need your return date.

**Customer:** What happens after a dispute is filed?

- `search_policy({"question": "what happens after a dispute is filed timeline review"})` → `{"documents": [{"document": "dispute-window", "score": 0.717, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** Once filed, the Kestrel disputes team reviews the case and forwards it to the merchant. The merchant has **10 business days** to respond, then the disputes team decides the case and records the outcome and its reason on the case. The follow-up on your case is scheduled automatically when you file, so you'll get an update without having to chase it.

A dispute also has to be filed within **75 days of the posting date** - after that it can't be opened through the assistant and has to go as a written claim.

**Customer:** Do travel notices change fees?

- `search_policy({"question": "travel notice effect on foreign transaction fees"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.769, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "travel-notices",  …`

**Assistant:** No. A travel notice doesn't change or waive the foreign transaction fee, which is **1.25% of the US-dollar amount** on purchases in any currency other than USD and posts as a separate line the same day. The notice only affects fraud screening.

**Customer:** What is a cancelled-subscription dispute?

- `search_policy({"question": "cancelled subscription dispute reason"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.806, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`

**Assistant:** It's the dispute reason to use when you cancelled a recurring subscription or membership and the merchant charged you again afterwards. Kestrel sends it to the merchant, who has 10 business days to respond, then the disputes team decides and records the outcome. Note that charges made before you cancelled are valid and can't be disputed on this ground.

**Customer:** Can you show my CloudNest charges?

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`

**Assistant:** You have two CloudNest Storage charges:

- **T-4001** - 2026-10-01, CloudNest 2TB monthly, $9.99
- **T-4002** - 2026-11-01, CloudNest 2TB monthly, $9.99

**Customer:** What's the difference between a pending and a posted charge, in one sentence?

**Assistant:** A pending charge is an authorization hold that reduces your available credit while the merchant finalizes it, and a posted charge is the settled amount that actually hits your statement.

**Customer:** What did I say my dog's name was, and where am I going in March?

- `load_memory({"query": "dog's name and travel plans for March"})` → `{"result": "memories=[MemoryEntry(content=Content(\n  parts=[\n    Part(\n      text='Conversation on 2026-11-24: Customer asked for one-sentence definitions of chargeback and authorization hold, Kestrel\u2019s foreign transaction fee, and dispute deadline; they said their dog is Biscuit and they plan Oslo in March (not verified). Assistant answered all, citing 1.25% FX fee and 75-day dispute wind …`

**Assistant:** From what I have of your earlier conversation: your dog is **Biscuit**, and you mentioned plans to go to **Oslo in March**. Note that's only what you said then - no travel notice is on file for the trip, so if you want one added, tell me the destination and your return date.

_Episode written:_ Conversation on 2026-11-24: Customer asked what a cancelled-subscription dispute is, requested CloudNest charges, a one-sentence pending/posted distinction, and recalled dog/travel details. Assistant explained the cancelled_subscription reason, listed CloudNest charges T-4001 and T-4002, explained pending vs posted, and said the customer said dog Biscuit and Oslo in March (not verified). No case ID; offered a travel notice if given a return date; none set. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | turns that leave the working-memory window are compacted into an episode mid-session | `episode ids: ['E-long-s1-1-3955ba', 'E-long-s1-2-ac120c', 'E-long-s1-3-0b116e']` |
| PASS | episodic | the out-of-window detail is recalled from that episode | `[{"query": "dog's name and travel plans for March"}]` |
| PASS | episodic | ...and answered correctly | `From what I have of your earlier conversation: your dog is **Biscuit**, and you mentioned plans to go to **Oslo in March**. Note that's only what you said then - no travel notice is on file for the trip, so if you want o …` |
