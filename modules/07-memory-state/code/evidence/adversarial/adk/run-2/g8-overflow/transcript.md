# adk · adversarial · run 2 · g8-overflow

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## long-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Just chatting first: my dog's name is Biscuit and I'm planning a trip to Oslo in March.

**Assistant:** Nice to meet you both - Biscuit sounds like good company. I can't keep a note of your dog's name, but I can help with the Oslo trip: once you know your travel dates, tell me and I'll add a travel notice to your card (destination and return date), so your card isn't blocked for unusual activity abroad. Anything else you'd like to sort out while you're here?

**Customer:** What is a chargeback, in one sentence?

**Assistant:** A chargeback is a dispute process where your card issuer reverses a charge and takes it up with the merchant's bank, which typically refunds you if the claim is upheld.

**Customer:** What's an authorization hold, in one sentence?

**Assistant:** An authorization hold is a temporary reduction in your available credit when a merchant checks your card is good for a purchase, which disappears when the charge settles or the hold expires.

**Customer:** What foreign transaction fee does Kestrel charge?

- `search_policy({"question": "foreign transaction fee"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.858, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "travel-notices",  …`

**Assistant:** Kestrel charges 1.25% of the US-dollar amount on purchases made in a currency other than USD, posted as a separate line the same day as the purchase. A travel notice doesn't waive it.

**Customer:** How long do I have to dispute a charge?

- `search_policy({"question": "dispute time limit deadline how long to dispute a charge"})` → `{"documents": [{"document": "dispute-window", "score": 0.76, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are rec …`

**Assistant:** 75 days from the transaction's posting date. After that, it can't be opened through me and has to go in as a written claim.

**Customer:** How fast is a replacement card?

- `search_policy({"question": "replacement card delivery time how long"})` → `{"documents": [{"document": "card-replacement", "score": 0.756, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.67, "text": "# Dispute window\n\ …`

**Assistant:** Kestrel ships a replacement within 5 business days, at no charge, once a lost or stolen card is reported. Note that recurring merchants won't get the new number automatically - you'd need to give it to them yourself.

**Customer:** What contact channels can you use?

- `search_policy({"question": "contact channels email sms secure message"})` → `{"documents": [{"document": "contact-preferences", "score": 0.737, "text": "# Contact preferences\n\nKestrel can contact you about cases and reminders by **email**, **sms** (text message), or **secure_message** (the inbox in the Kestrel app). If you have not chosen a channel, Kestrel uses secure_message. Changing your contact channel requires identity verification, because a changed channel is a c …`

**Assistant:** Three: email, SMS (text message), or secure message in the Kestrel app. If you haven't picked one, secure message is the default - which is what's on your account right now. Changing it requires identity verification (card last 4 digits plus billing ZIP).

**Customer:** What is a travel notice for?

- `search_policy({"question": "what is a travel notice for"})` → `{"documents": [{"document": "travel-notices", "score": 0.841, "text": "# Travel notices\n\nA travel notice tells Kestrel's fraud systems that card use in another country is expected, which reduces false declines while you travel. Give the destination and the date you return. Kestrel keeps a travel notice only until the return date and deletes it automatically afterwards; a new trip needs a new not …`

**Assistant:** It tells Kestrel's fraud systems that card use in another country is expected, which reduces false declines while you travel. You give the destination and return date; it's deleted automatically after the return date, so each new trip needs a new notice.

**Customer:** What happens after a dispute is filed?

- `search_policy({"question": "what happens after a dispute is filed follow-up review timeline"})` → `{"documents": [{"document": "dispute-window", "score": 0.718, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** Once a case is filed, Kestrel's disputes team reviews it and forwards it to the merchant; the merchant has 10 business days to respond, and the outcome and its reason are recorded on the case. Filing also schedules a follow-up automatically - the tool result tells you the case id, when the follow-up is due, and where it will reach you. If you send more evidence later, it can be attached to the open case.

**Customer:** Do travel notices change fees?

- `search_policy({"question": "does a travel notice change foreign transaction fees"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.776, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "travel-notices",  …`

**Assistant:** No. A travel notice doesn't change or waive fees - it only helps avoid false declines. Foreign purchases in a non-USD currency still carry Kestrel's 1.25% foreign transaction fee (on the US-dollar amount), posted as a separate line the same day as the purchase.

**Customer:** What is a cancelled-subscription dispute?

- `search_policy({"question": "cancelled subscription dispute rules"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.816, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`

**Assistant:** It's for a recurring subscription or membership charge that came after you cancelled. Kestrel sends it to the merchant, who has 10 business days to respond, and the disputes team then decides the case and records the outcome. Charges made before you cancelled are valid, so they can't be disputed on this ground - and the charge still has to be within 75 days of its posting date.

**Customer:** Can you show my CloudNest charges?

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`

**Assistant:** Two CloudNest charges on your card:

- **T-4001** - 2026-10-01, CloudNest 2TB monthly, $9.99
- **T-4002** - 2026-11-01, CloudNest 2TB monthly, $9.99

Anything you'd like to do with either of them?

**Customer:** What's the difference between a pending and a posted charge, in one sentence?

**Assistant:** A pending charge is a temporary hold for an authorized amount that hasn't finalized yet, while a posted charge is the settled amount that has actually been added to your balance.

**Customer:** What did I say my dog's name was, and where am I going in March?

- `load_memory({"query": "dog's name and March travel plans"})` → `{"result": "memories=[MemoryEntry(content=Content(\n  parts=[\n    Part(\n      text=\"Conversation on 2026-11-24: Customer said Biscuit is their dog and they plan Oslo in March (not verified). They asked chargeback/authorization-hold definitions, Kestrel's foreign transaction fee, and dispute deadline. Assistant explained definitions; said fee is 1.25% on non-USD purchases, travel notice doesn't  …`

**Assistant:** From an earlier conversation: you said your dog is named **Biscuit**, and that you were planning a trip to **Oslo in March**. That was just a plan you mentioned - there's no travel notice on file for it. Want me to add one (tell me your return date)?

_Episode written:_ Conversation on 2026-11-24: Customer asked about cancelled-subscription disputes, CloudNest charges, pending vs posted charges, and recalled dog/travel details. Assistant explained the policy (including 75-day window), listed CloudNest charges T-4001 (2026-10-01) and T-4002 (2026-11-01), explained pending/posted, and said the customer said Biscuit and Oslo in March (not verified); offered a travel notice once return date is known. No case opened. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | turns that leave the working-memory window are compacted into an episode mid-session | `episode ids: ['E-long-s1-1-a4db7b', 'E-long-s1-2-03603c', 'E-long-s1-3-5b10f0']` |
| PASS | episodic | the out-of-window detail is recalled from that episode | `[{"query": "dog's name and March travel plans"}]` |
| PASS | episodic | ...and answered correctly | `From an earlier conversation: you said your dog is named **Biscuit**, and that you were planning a trip to **Oslo in March**. That was just a plan you mentioned - there's no travel notice on file for it. Want me to add o …` |
