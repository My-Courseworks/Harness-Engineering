# adk · adversarial · run 1 · g8-overflow

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## long-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Just chatting first: my dog's name is Biscuit and I'm planning a trip to Oslo in March.

**Assistant:** Nice to meet you and Biscuit! Sounds like a good March ahead.

One thing worth flagging: if you'd like, I can put a travel notice on your account for the Oslo trip so your card isn't flagged for out-of-country use — I'd just need your travel dates (departure and return day). Happy to do that whenever your plans firm up.

**Customer:** What is a chargeback, in one sentence?

**Assistant:** A chargeback is when your card issuer reverses a disputed charge and takes the money back from the merchant's bank, typically while the merchant has a chance to respond with evidence.

**Customer:** What's an authorization hold, in one sentence?

**Assistant:** An authorization hold is a temporary reduction in your available credit when a merchant checks your card can cover a purchase — it isn't a real charge and usually drops off once the transaction settles or expires.

**Customer:** What foreign transaction fee does Kestrel charge?

- `search_policy({"question": "What foreign transaction fee does Kestrel charge?"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.934, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "cancelled-subscri …`

**Assistant:** 1.25% of the US-dollar amount on any purchase made in a currency other than USD. It posts as a separate line the same day as the purchase, and a travel notice doesn't change or waive it.

**Customer:** How long do I have to dispute a charge?

- `search_policy({"question": "How long does a customer have to dispute a charge? Time limit / deadline for filing a dispute."})` → `{"documents": [{"document": "dispute-window", "score": 0.769, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** 75 days from the transaction's posting date. After that, it can't be opened through me and has to go in as a written claim.

**Customer:** How fast is a replacement card?

- `search_policy({"question": "How long does a replacement card take to arrive? Replacement card shipping timeline."})` → `{"documents": [{"document": "card-replacement", "score": 0.731, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.652, "text": "# Dispute window\n …`

**Assistant:** A replacement ships within 5 business days, at no charge, once you report the card lost or stolen. Heads-up: recurring merchants won't get the new number automatically — you'll need to give it to them yourself.

**Customer:** What contact channels can you use?

- `search_policy({"question": "What contact channels can Kestrel use to reach a customer? email, SMS, secure message"})` → `{"documents": [{"document": "contact-preferences", "score": 0.856, "text": "# Contact preferences\n\nKestrel can contact you about cases and reminders by **email**, **sms** (text message), or **secure_message** (the inbox in the Kestrel app). If you have not chosen a channel, Kestrel uses secure_message. Changing your contact channel requires identity verification, because a changed channel is a c …`

**Assistant:** Three: email, SMS (text message), or secure_message (the inbox in the Kestrel app). If you haven't picked one, secure_message is the default — and changing it requires identity verification.

**Customer:** What is a travel notice for?

- `search_policy({"question": "What is a travel notice for and how does it work at Kestrel?"})` → `{"documents": [{"document": "travel-notices", "score": 0.887, "text": "# Travel notices\n\nA travel notice tells Kestrel's fraud systems that card use in another country is expected, which reduces false declines while you travel. Give the destination and the date you return. Kestrel keeps a travel notice only until the return date and deletes it automatically afterwards; a new trip needs a new not …`

**Assistant:** It tells Kestrel's fraud systems that card use abroad is expected, which cuts down false declines while you travel. It needs the destination and your return date; it's kept only until that return date and then deleted automatically, so each new trip needs a new notice.

**Customer:** What happens after a dispute is filed?

- `search_policy({"question": "What happens after a dispute is filed? Review timeline and follow-up"})` → `{"documents": [{"document": "dispute-window", "score": 0.729, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** The disputes team reviews the case and forwards it to the merchant; for recurring-charge disputes the merchant has 10 business days to respond. The team then decides the case and records the outcome and its reason on the case, so you'll see the result there.

**Customer:** Do travel notices change fees?

**Assistant:** No — a travel notice doesn't change or waive any fee. The 1.25% foreign transaction fee on non-USD purchases still applies.

**Customer:** What is a cancelled-subscription dispute?

**Assistant:** It's a dispute for a recurring subscription or membership charge that hit your card after you cancelled. You file it with the reason cancelled_subscription; Kestrel sends it to the merchant, who has 10 business days to respond, and the disputes team decides the outcome. Charges made before you cancelled are valid and can't be disputed on that ground.

**Customer:** Can you show my CloudNest charges?

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`

**Assistant:** Here are your CloudNest Storage charges:

| Transaction | Posted | Description | Amount |
|---|---|---|---|
| T-4001 | 2026-10-01 | CloudNest 2TB monthly | $9.99 |
| T-4002 | 2026-11-01 | CloudNest 2TB monthly | $9.99 |

Both USD, subscription category. Anything you'd like to do with either one?

**Customer:** What's the difference between a pending and a posted charge, in one sentence?

**Assistant:** A pending charge is an authorization that temporarily reserves part of your available credit, while a posted charge is the finalized transaction that actually hits your balance and appears on your statement.

**Customer:** What did I say my dog's name was, and where am I going in March?

- `load_memory({"query": "dog's name and March trip destination Oslo"})` → `{"result": "memories=[]"}`

**Assistant:** Your dog is Biscuit, and you're planning a trip to Oslo in March. (Just so you know: I only keep contact-channel and travel-notice details on file — no stored profile of Biscuit.)

_Episode written:_ Conversation on 2026-11-24: Customer asked card-policy questions and to view CloudNest charges; assistant explained fees, disputes, replacement cards, contact channels, and travel notices, and showed transactions T-4001 and T-4002. No dispute/case was opened. Customer shared dog Biscuit and a planned Oslo trip in March; no travel dates supplied, so no travel notice was set. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | turns that leave the working-memory window are compacted into an episode mid-session | `episode ids: []` |
| PASS | episodic | the out-of-window detail is recalled from that episode | `[{"query": "dog's name and March trip destination Oslo"}]` |
| PASS | episodic | ...and answered correctly | `Your dog is Biscuit, and you're planning a trip to Oslo in March. (Just so you know: I only keep contact-channel and travel-notice details on file — no stored profile of Biscuit.)` |
