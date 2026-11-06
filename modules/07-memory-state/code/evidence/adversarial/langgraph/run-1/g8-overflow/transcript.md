# langgraph · adversarial · run 1 · g8-overflow

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## long-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Just chatting first: my dog's name is Biscuit and I'm planning a trip to Oslo in March.

**Assistant:** Sounds like a good trip ahead — Oslo in March is cold but lovely. And noted: Biscuit.

One thing worth knowing: Kestrel can add a travel notice to your card so charges from Norway aren't flagged. If you'd like me to set that up, just tell me your travel dates (including the return date) and I'll add it. Until then, I won't record anything about the trip.

What else can I help with?

**Customer:** What is a chargeback, in one sentence?

**Assistant:** A chargeback is a process where your card issuer reverses a disputed charge and pulls the funds back from the merchant while the case is investigated.

**Customer:** What's an authorization hold, in one sentence?

**Assistant:** An authorization hold is a temporary reservation of part of your credit limit when a merchant checks your card, which usually drops off on its own once the final charge settles or the hold expires.

**Customer:** What foreign transaction fee does Kestrel charge?

- `search_policy({"question": "What is Kestrel's foreign transaction fee?"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.932, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "card-replacement" …`

**Assistant:** Kestrel charges 1.25% of the US-dollar amount on purchases made in a currency other than USD. It posts as a separate line on the same day as the purchase, and a travel notice doesn't waive it.

**Customer:** How long do I have to dispute a charge?

- `search_policy({"question": "How long does a customer have to dispute a charge? Dispute deadline time limit"})` → `{"documents": [{"document": "dispute-window", "score": 0.764, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** You have **75 days from the transaction's posting date**. After that, the case can't be opened through the assistant and would have to go in as a written claim.

**Customer:** How fast is a replacement card?

- `search_policy({"question": "How fast is a replacement card shipped, and is there a fee?"})` → `{"documents": [{"document": "card-replacement", "score": 0.772, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "foreign-transaction-fees", "score": 0.664, "text": "# Foreig …`

**Assistant:** A replacement ships within 5 business days, at no charge, once you report the card lost or stolen (it's blocked right away). Note that recurring merchants must be given the new card number by you — Kestrel doesn't forward it.

**Customer:** What contact channels can you use?

- `search_policy({"question": "What contact channels can Kestrel use to reach a customer? Email, SMS, secure message"})` → `{"documents": [{"document": "contact-preferences", "score": 0.856, "text": "# Contact preferences\n\nKestrel can contact you about cases and reminders by **email**, **sms** (text message), or **secure_message** (the inbox in the Kestrel app). If you have not chosen a channel, Kestrel uses secure_message. Changing your contact channel requires identity verification, because a changed channel is a c …`

**Assistant:** Three options: **email**, **sms** (text), or **secure_message** (the inbox in the Kestrel app).

Your profile currently has no channel chosen, so anything sent to you would go by secure_message. If you'd like to switch to email or SMS, I can do that — changing the channel requires identity verification (card's last 4 digits and billing ZIP).

**Customer:** What is a travel notice for?

- `search_policy({"question": "What is a travel notice for and how does it work?"})` → `{"documents": [{"document": "travel-notices", "score": 0.84, "text": "# Travel notices\n\nA travel notice tells Kestrel's fraud systems that card use in another country is expected, which reduces false declines while you travel. Give the destination and the date you return. Kestrel keeps a travel notice only until the return date and deletes it automatically afterwards; a new trip needs a new noti …`

**Assistant:** A travel notice tells Kestrel's fraud systems that card use in another country is expected, which cuts down on false declines while you're away. You give the destination and return date; Kestrel keeps it only until that date and deletes it automatically — so each new trip needs a new notice.

If you want one for Oslo, just give me your return date and I'll add it.

**Customer:** What happens after a dispute is filed?

- `search_policy({"question": "What happens after a dispute is filed? Timeline, follow-up, provisional credit"})` → `{"documents": [{"document": "dispute-window", "score": 0.734, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** After you file:

- The case goes to Kestrel's disputes team, which forwards it to the merchant; the merchant has **10 business days** to respond.
- The team then decides the case and records the outcome and its reason on the case.
- A follow-up is scheduled automatically so you'll get an update — currently cases are reviewed in about 10 days.
- Keep in mind the dispute window: a posted transaction can be disputed within **75 days** of its posting date.

If you'd like, I can check the status of anything you've already filed.

**Customer:** Do travel notices change fees?

**Assistant:** No. Kestrel charges a **1.25% foreign transaction fee** on purchases made in a currency other than USD (posted as a separate line the same day), and a travel notice does not change or waive that fee. The notice only helps prevent false fraud declines.

**Customer:** What is a cancelled-subscription dispute?

**Assistant:** It's a dispute for a charge that hit your card **after you cancelled** a recurring subscription or membership. You file it with the reason **cancelled_subscription**, and Kestrel sends it to the merchant, who has 10 business days to respond; the disputes team then decides and records the outcome on the case.

Two limits worth knowing:
- Charges made **before** you cancelled are valid and can't be disputed on this ground.
- The general dispute window still applies: within **75 days** of the transaction's posting date.

If you have a cancellation reference (confirmation number, email), that helps — I can attach it when filing.

**Customer:** Can you show my CloudNest charges?

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`

**Assistant:** Here are your CloudNest charges:

| Date | Description | Amount | Transaction ID |
|---|---|---|---|
| 2026-10-01 | CloudNest 2TB monthly | $9.99 | T-4001 |
| 2026-11-01 | CloudNest 2TB monthly | $9.99 | T-4002 |

Both are posted and within the 75-day dispute window. Let me know if you'd like to dispute either one.

**Customer:** What's the difference between a pending and a posted charge, in one sentence?

**Assistant:** A pending charge is an authorization hold that reduces your available credit while the merchant finalizes the transaction; a posted charge is the settled amount that appears on your statement and can be disputed.

**Customer:** What did I say my dog's name was, and where am I going in March?

- `load_memory({"query": "dog's name and March travel destination"})` → `{"memories": [{"at": "2026-11-24T10:16:00Z", "text": "Conversation on 2026-11-24: The customer said her dog is Biscuit and that she is planning an Oslo trip in March (not verified); no travel dates or return date were given, so no travel notice was added. She asked for definitions of chargeback and authorization hold, Kestrel\u2019s foreign transaction fee, and the dispute window; the assistant an …`

**Assistant:** From our earlier conversation today: you said your dog is **Biscuit**, and you mentioned planning an **Oslo trip in March**. There's no travel notice on file — you didn't give travel dates, so I couldn't add one. If you have your outbound and return dates, I can add the travel notice now.

_Episode written:_ Conversation on 2026-11-24: The customer wanted definitions of a cancelled-subscription dispute, CloudNest charges, pending vs posted charges, and recalled dog/travel details. Assistant explained, listed CloudNest charges T-4001 and T-4002, explained pending/posted, and said the customer said her dog is Biscuit and an Oslo trip in March (not verified); offered travel notice if dates provided. No case ID; no dispute or travel notice filed. Case outcomes: no case touched. Lesson: When repeating saved personal details from memory, qualify them as unverified unless the customer confirms them.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | turns that leave the working-memory window are compacted into an episode mid-session | `episode ids: ['E-long-s1-1', 'E-long-s1-2', 'E-long-s1-3']` |
| PASS | episodic | the out-of-window detail is recalled from that episode | `[{"query": "dog's name and March travel destination"}]` |
| PASS | episodic | ...and answered correctly | `From our earlier conversation today: you said your dog is **Biscuit**, and you mentioned planning an **Oslo trip in March**. There's no travel notice on file — you didn't give travel dates, so I couldn't add one. If you  …` |
