# langgraph · adversarial · run 1 · g8-overflow

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## long-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Just chatting first: my dog's name is Biscuit and I'm planning a trip to Oslo in March.

**Assistant:** Nice to meet you and Biscuit. I can't keep a dog's name on file - I can only store a contact channel or a travel notice - but I'm happy to chat. When your Oslo trip is confirmed, tell me the dates and I can add a travel notice so your card isn't flagged for use abroad.

**Customer:** What is a chargeback, in one sentence?

**Assistant:** A chargeback is when your card issuer reverses a card payment and takes the money back from the merchant, usually after you dispute the charge.

**Customer:** What's an authorization hold, in one sentence?

**Assistant:** An authorization hold is a temporary freeze of part of your credit limit when a merchant checks your card, released once the final charge settles or the hold expires.

**Customer:** What foreign transaction fee does Kestrel charge?

- `search_policy({"question": "foreign transaction fee"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.858, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "travel-notices",  …`

**Assistant:** Kestrel charges 1.25% of the US-dollar amount on every purchase made in a currency other than USD. It posts as a separate line on the same day as the purchase, and a travel notice neither changes nor waives it.

**Customer:** How long do I have to dispute a charge?

- `search_policy({"question": "dispute deadline how long to dispute a charge"})` → `{"documents": [{"document": "dispute-window", "score": 0.783, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** You have 75 days from the transaction's posting date. After that, a case can't be opened through me and would need a written claim.

**Customer:** How fast is a replacement card?

- `search_policy({"question": "replacement card delivery time"})` → `{"documents": [{"document": "card-replacement", "score": 0.753, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.655, "text": "# Dispute window\n …`

**Assistant:** A replacement card ships within 5 business days, at no charge, once you report the old one lost, stolen or damaged. Note that recurring merchants won't get the new number automatically - you'll need to give it to them yourself.

**Customer:** What contact channels can you use?

- `search_policy({"question": "contact channels available"})` → `{"documents": [{"document": "contact-preferences", "score": 0.678, "text": "# Contact preferences\n\nKestrel can contact you about cases and reminders by **email**, **sms** (text message), or **secure_message** (the inbox in the Kestrel app). If you have not chosen a channel, Kestrel uses secure_message. Changing your contact channel requires identity verification, because a changed channel is a c …`

**Assistant:** Three: email, SMS (text message), or secure message in the Kestrel app. You currently have none set, so anything from Kestrel reaches you by secure message in the app. Switching to email or SMS requires identity verification - just say the word and I'll walk you through it.

**Customer:** What is a travel notice for?

**Assistant:** It tells Kestrel's fraud systems that card use in another country is expected, which cuts down on false declines while you travel. You give the destination and your return date; the notice is kept only until that date, then deleted automatically - so a new trip needs a new notice. Want me to add Oslo once you have your March dates?

**Customer:** What happens after a dispute is filed?

- `search_policy({"question": "what happens after a dispute is filed, timeline"})` → `{"documents": [{"document": "dispute-window", "score": 0.734, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** Once filed, you get a case id and a follow-up is scheduled automatically (by secure message in the app for you, since no channel is set). The Kestrel disputes team reviews the case - currently about 10 days - and forwards it to the merchant, who has 10 business days to respond. The team then decides, and the outcome and its reason are recorded on the case. You can add evidence to an open case at any time; a decided case can't take more evidence.

**Customer:** Do travel notices change fees?

- `search_policy({"question": "travel notice effect on fees, foreign transaction fee"})` → `{"documents": [{"document": "travel-notices", "score": 0.771, "text": "# Travel notices\n\nA travel notice tells Kestrel's fraud systems that card use in another country is expected, which reduces false declines while you travel. Give the destination and the date you return. Kestrel keeps a travel notice only until the return date and deletes it automatically afterwards; a new trip needs a new not …`

**Assistant:** No. A travel notice only tells the fraud systems to expect use abroad, which reduces false declines - it doesn't change fees. The foreign transaction fee is 1.25% of the US-dollar amount on every purchase in a currency other than USD, and posts as a separate line the same day, travel notice or not.

**Customer:** What is a cancelled-subscription dispute?

**Assistant:** It's for a recurring subscription or membership you cancelled and were still charged for afterwards. You file it with the reason "cancelled subscription"; Kestrel sends it to the merchant, who has 10 business days to respond, then the disputes team decides and records the outcome.

One limit: charges made before you cancelled are valid and can't be disputed on this ground.

**Customer:** Can you show my CloudNest charges?

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`

**Assistant:** Two CloudNest Storage charges:

- **T-4001** - 2026-10-01, "CloudNest 2TB monthly", $9.99
- **T-4002** - 2026-11-01, "CloudNest 2TB monthly", $9.99

Want me to dispute one of them, or is there something else you'd like to check?

**Customer:** What's the difference between a pending and a posted charge, in one sentence?

**Assistant:** A pending charge is an authorization hold that reserves part of your available credit when the merchant first contacts the bank, while a posted (settled) charge is the final amount actually billed once the merchant completes the transaction - so pending amounts can change or drop off, but a posted amount is what counts.

**Customer:** What did I say my dog's name was, and where am I going in March?

- `load_memory({"query": "dog's name and March travel plans"})` → `{"memories": [{"at": "2026-11-24T10:16:00Z", "text": "Conversation on 2026-11-24: Customer said Biscuit is their dog and they planned an Oslo trip in March (not verified). They asked for one-sentence definitions of chargeback and authorization hold, Kestrel's foreign transaction fee, and the dispute deadline; assistant answered all. No case or transaction IDs. Assistant said to share confirmed Osl …`

**Assistant:** From an earlier conversation today, you said your dog is **Biscuit**, and that you were planning a trip to **Oslo in March**. Both come from that conversation rather than from anything on file - no travel notice is currently set on your account, so the Oslo dates were never confirmed or added.

If you'd like the travel notice set up, give me the destination and the date you return and I'll add it. (Only your contact channel and a travel notice are kept as saved facts, so Biscuit's name lives in the conversation transcript, not in your profile.)

_Episode written:_ Conversation on 2026-11-24: Customer asked about cancelled-subscription disputes, CloudNest charges, and a one-sentence pending vs posted explanation, then recalled dog/travel facts. Assistant explained definitions and showed T-4001 and T-4002. Customer said Biscuit is their dog and planned Oslo in March (not verified). No case filed. Assistant offered a travel notice if destination and return date are provided. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | turns that leave the working-memory window are compacted into an episode mid-session | `episode ids: ['E-long-s1-1-b27509', 'E-long-s1-2-4be3bf', 'E-long-s1-3-e64318']` |
| PASS | episodic | the out-of-window detail is recalled from that episode | `[{"query": "dog's name and March travel plans"}]` |
| PASS | episodic | ...and answered correctly | `From an earlier conversation today, you said your dog is **Biscuit**, and that you were planning a trip to **Oslo in March**. Both come from that conversation rather than from anything on file - no travel notice is curre …` |
