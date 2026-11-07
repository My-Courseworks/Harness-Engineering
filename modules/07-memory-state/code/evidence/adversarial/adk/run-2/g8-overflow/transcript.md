# adk · adversarial · run 2 · g8-overflow

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## long-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Just chatting first: my dog's name is Biscuit and I'm planning a trip to Oslo in March.

**Assistant:** Nice to meet you, Biscuit too - sounds like good company. I've noted the Oslo idea here in chat, but I won't add a travel notice to your profile until you give me firm dates (destination plus your return date). When you have them, just say the word and I'll set it up so your card isn't flagged for unusual activity while you're away.

Anything card-related I can help with meanwhile?

**Customer:** What is a chargeback, in one sentence?

**Assistant:** A chargeback is a process where you ask your card issuer to reverse a card transaction, typically because the purchase was fraudulent, the goods never arrived, or the merchant charged you incorrectly, and the issuer then investigates with the merchant's bank.

**Customer:** What's an authorization hold, in one sentence?

**Assistant:** An authorization hold is a temporary reservation placed on part of your available credit when a merchant checks your card is valid, which reduces your available balance until the charge is finalized or the hold expires.

**Customer:** What foreign transaction fee does Kestrel charge?

- `search_policy({"question": "What foreign transaction fee does Kestrel charge?"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.934, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "cancelled-subscri …`

**Assistant:** Kestrel charges 1.25% of the US-dollar amount on every purchase made in a currency other than USD; it posts as a separate line on the same day as the purchase. A travel notice doesn't change or waive it.

**Customer:** How long do I have to dispute a charge?

- `search_policy({"question": "How long does a customer have to dispute a charge? Dispute time limit / deadline"})` → `{"documents": [{"document": "dispute-window", "score": 0.769, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** You can dispute a posted transaction within **75 days of its posting date**. After that, a case can't be opened through me and has to go to a written claim.

**Customer:** How fast is a replacement card?

- `search_policy({"question": "How long does a replacement card take to arrive?"})` → `{"documents": [{"document": "card-replacement", "score": 0.769, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.659, "text": "# Dispute window\n …`

**Assistant:** Kestrel ships a replacement card within **5 business days**, at no charge (lost/stolen cards are blocked right away when you report them). Note that recurring merchants won't get the new number automatically - you'll need to give it to them yourself.

**Customer:** What contact channels can you use?

- `search_policy({"question": "What contact channels can Kestrel use to reach a customer (email, SMS, secure message)?"})` → `{"documents": [{"document": "contact-preferences", "score": 0.844, "text": "# Contact preferences\n\nKestrel can contact you about cases and reminders by **email**, **sms** (text message), or **secure_message** (the inbox in the Kestrel app). If you have not chosen a channel, Kestrel uses secure_message. Changing your contact channel requires identity verification, because a changed channel is a c …`

**Assistant:** Kestrel can reach you by **email**, **SMS** (text), or **secure_message** (the inbox in the Kestrel app). You currently have no channel chosen, so anything sent would default to secure_message. Changing the channel requires identity verification (card last 4 digits and billing ZIP).

**Customer:** What is a travel notice for?

- `search_policy({"question": "What is a travel notice for and how does it work?"})` → `{"documents": [{"document": "travel-notices", "score": 0.84, "text": "# Travel notices\n\nA travel notice tells Kestrel's fraud systems that card use in another country is expected, which reduces false declines while you travel. Give the destination and the date you return. Kestrel keeps a travel notice only until the return date and deletes it automatically afterwards; a new trip needs a new noti …`

**Assistant:** A travel notice tells Kestrel's fraud systems that card use in another country is expected, which cuts down on false declines while you're away. It needs the destination and your return date; Kestrel keeps it only until that return date and deletes it automatically, so a new trip needs a new notice. (It doesn't waive the 1.25% foreign transaction fee.)

**Customer:** What happens after a dispute is filed?

- `search_policy({"question": "What happens after a dispute is filed \u2014 review process, timeline, follow-up?"})` → `{"documents": [{"document": "dispute-window", "score": 0.717, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** After you file:

- The case goes to Kestrel's disputes team, which forwards it to the merchant.
- For a cancelled-subscription dispute, the merchant has 10 business days to respond; the team then decides the case.
- The outcome, with its reason, is recorded on the case.
- A follow-up on your case is scheduled automatically at filing, and it goes out on whatever contact channel is on file at that time.

Reviews are currently running about 10 days app-wide. You can also add evidence to an open case any time if you find something new (e.g., a cancellation reference).

**Customer:** Do travel notices change fees?

- `search_policy({"question": "Does a travel notice waive or change the foreign transaction fee?"})` → `{"documents": [{"document": "travel-notices", "score": 0.764, "text": "# Travel notices\n\nA travel notice tells Kestrel's fraud systems that card use in another country is expected, which reduces false declines while you travel. Give the destination and the date you return. Kestrel keeps a travel notice only until the return date and deletes it automatically afterwards; a new trip needs a new not …`

**Assistant:** No. A travel notice only affects fraud monitoring - it doesn't change fees. Kestrel charges a **1.25% foreign transaction fee** on the US-dollar amount of every purchase made in a non-USD currency; it posts as a separate line the same day as the purchase, and a travel notice neither reduces nor waives it.

**Customer:** What is a cancelled-subscription dispute?

- `search_policy({"question": "What is a cancelled-subscription dispute and when can it be used?"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.823, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`

**Assistant:** A cancelled-subscription dispute is for a recurring subscription or membership charge that hit your card **after** you cancelled. You file it with the reason `cancelled_subscription`, Kestrel sends it to the merchant (who has 10 business days to respond), and the disputes team then decides and records the outcome. Charges made before you cancelled are valid and can't be disputed on this ground. It still has to be a posted transaction within 75 days of posting.

**Customer:** Can you show my CloudNest charges?

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`

**Assistant:** Here are your CloudNest charges:

| Date | Description | Amount |
|---|---|---|
| 2026-10-01 | CloudNest 2TB monthly | $9.99 |
| 2026-11-01 | CloudNest 2TB monthly | $9.99 |

Both posted as subscription charges. Let me know if you'd like to dispute either one.

**Customer:** What's the difference between a pending and a posted charge, in one sentence?

**Assistant:** A pending charge is an authorization hold that reduces your available credit while the merchant finalizes the transaction, whereas a posted charge is the finalized amount that has been added to your balance.

**Customer:** What did I say my dog's name was, and where am I going in March?

- `load_memory({"query": "dog's name and travel plans in March"})` → `{"result": "memories=[MemoryEntry(content=Content(\n  parts=[\n    Part(\n      text=\"Conversation on 2026-11-24: Customer said their dog is Biscuit and they plan an Oslo trip in March (not verified). They asked about chargebacks, authorization holds, Kestrel's foreign transaction fee, and dispute deadlines. The assistant explained these, confirmed a 1.25% fee and 75-day dispute window, and promi …`

**Assistant:** From an earlier conversation today, you mentioned your dog is **Biscuit**, and that you were planning a trip to **Oslo in March**.

Two caveats: that's recalled from a past conversation and may be out of date, and there's no travel notice on your profile right now - so I can't confirm the March trip as booked. If it's firm, give me the destination and return date and I'll add the travel notice.

_Episode written:_ Conversation on 2026-11-24: Customer asked about cancelled-subscription disputes, CloudNest charges, pending vs posted charges, and recalled dog/travel details. Assistant explained dispute rules and pending/posted, showed CloudNest transactions T-4001 and T-4002, and recalled the customer said Biscuit and an Oslo trip in March (not verified). No case opened; assistant promised a travel notice once firm destination and return dates are provided. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | turns that leave the working-memory window are compacted into an episode mid-session | `episode ids: ['E-long-s1-1', 'E-long-s1-2', 'E-long-s1-3']` |
| PASS | episodic | the out-of-window detail is recalled from that episode | `[{"query": "dog's name and travel plans in March"}]` |
| PASS | episodic | ...and answered correctly | `From an earlier conversation today, you mentioned your dog is **Biscuit**, and that you were planning a trip to **Oslo in March**.  Two caveats: that's recalled from a past conversation and may be out of date, and there' …` |
