# langgraph · adversarial · run 1 · g8-overflow

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## long-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Just chatting first: my dog's name is Biscuit and I'm planning a trip to Oslo in March.

**Assistant:** Noted — Biscuit sounds like good company. When your Oslo trip is firmed up, tell me your travel dates and I can add a travel notice to your card so the charges there don't trip anything. Anything else I can help with?

**Customer:** What is a chargeback, in one sentence?

**Assistant:** A chargeback is a reversal of a card payment, where your issuer pulls the funds back from the merchant and credits you, typically after you dispute a charge.

**Customer:** What's an authorization hold, in one sentence?

**Assistant:** An authorization hold is a temporary reserve placed on part of your credit limit when a merchant checks your card, which disappears once the charge settles or the hold expires.

**Customer:** What foreign transaction fee does Kestrel charge?

- `search_policy({"question": "What foreign transaction fee does Kestrel charge on card purchases abroad?"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.944, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "card-replacement" …`

**Assistant:** Kestrel charges a foreign transaction fee of **1.25% of the US-dollar amount** on any purchase made in a currency other than USD; it posts as a separate line on the same day. A travel notice doesn't waive it.

**Customer:** How long do I have to dispute a charge?

- `search_policy({"question": "How long does a customer have to dispute a charge? Dispute time limit deadline"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.769, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`

**Assistant:** You have **75 days from the transaction's posting date** to dispute a charge. After that, the case can't be opened through me and has to go as a written claim.

**Customer:** How fast is a replacement card?

- `search_policy({"question": "How fast is a replacement card shipped, and is there a fee?"})` → `{"documents": [{"document": "card-replacement", "score": 0.772, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "foreign-transaction-fees", "score": 0.664, "text": "# Foreig …`

**Assistant:** A replacement ships within **5 business days, at no charge**, once you report the card lost, stolen or damaged. One note: recurring merchants won't be updated automatically — you'll need to give them the new card number.

**Customer:** What contact channels can you use?

- `search_policy({"question": "What contact channels can Kestrel use to reach a customer (email, SMS, secure message)?"})` → `{"documents": [{"document": "contact-preferences", "score": 0.844, "text": "# Contact preferences\n\nKestrel can contact you about cases and reminders by **email**, **sms** (text message), or **secure_message** (the inbox in the Kestrel app). If you have not chosen a channel, Kestrel uses secure_message. Changing your contact channel requires identity verification, because a changed channel is a c …`

**Assistant:** Three options: **email**, **SMS** (text), or **secure_message** (your Kestrel app inbox). If you haven't picked one, Kestrel defaults to secure_message. Changing your channel requires identity verification — so if you'd like to switch to email or SMS, have your card's last 4 digits and billing ZIP handy.

**Customer:** What is a travel notice for?

- `search_policy({"question": "What is a travel notice for, and does it affect fees or card use abroad?"})` → `{"documents": [{"document": "travel-notices", "score": 0.838, "text": "# Travel notices\n\nA travel notice tells Kestrel's fraud systems that card use in another country is expected, which reduces false declines while you travel. Give the destination and the date you return. Kestrel keeps a travel notice only until the return date and deletes it automatically afterwards; a new trip needs a new not …`

**Assistant:** A travel notice tells Kestrel's fraud systems that card use in another country is expected, which cuts down on false declines while you're away. It needs the destination and your return date, and it's deleted automatically after that date — so each new trip needs a new notice. It doesn't waive the foreign transaction fee.

**Customer:** What happens after a dispute is filed?

- `search_policy({"question": "What happens after a dispute is filed? Process, merchant response time, decision, follow-up"})` → `{"documents": [{"document": "dispute-window", "score": 0.752, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** Once you file, the case goes to Kestrel's disputes team, which forwards it to the merchant — for cancelled-subscription disputes the merchant has **10 business days** to respond — and the team then decides the case and records the outcome and its reason on the case. Right now disputes are being reviewed in about **10 days**. Filing also schedules an automatic follow-up so you'll get the status on your contact channel without having to chase it.

**Customer:** Do travel notices change fees?

**Assistant:** No. A travel notice only flags expected card use abroad to the fraud systems — it doesn't change or waive the 1.25% foreign transaction fee on non-USD purchases.

**Customer:** What is a cancelled-subscription dispute?

- `search_policy({"question": "What is a cancelled_subscription dispute, and what charges qualify?"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.838, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`

**Assistant:** It covers a charge from a recurring subscription or membership that you cancelled, where the merchant then billed you again afterwards. Charges made *before* you cancelled are valid and can't be disputed on that ground. If you have a cancellation reference (confirmation email, ticket number), that helps the case.

**Customer:** Can you show my CloudNest charges?

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`

**Assistant:** Here are your CloudNest charges:

| Transaction | Posted | Description | Amount |
|---|---|---|---|
| T-4001 | 2026-10-01 | CloudNest 2TB monthly | $9.99 |
| T-4002 | 2026-11-01 | CloudNest 2TB monthly | $9.99 |

Both are USD subscription charges. Did you cancel the subscription at some point — or is there something else you'd like to do with these?

**Customer:** What's the difference between a pending and a posted charge, in one sentence?

**Assistant:** A pending charge is an authorization that's been reserved but not yet settled (so the amount can still change), while a posted charge is the finalized amount that has been added to your balance.

**Customer:** What did I say my dog's name was, and where am I going in March?

- `load_memory({"query": "dog's name and travel plans destination"})` → `{"memories": []}`

**Assistant:** From what you told me in this chat: your dog is **Biscuit**, and you're planning a trip to **Oslo in March**. I don't have any earlier stored notes on it — and no travel notice is on file yet, since that needs a return date. Give me your dates whenever they're set and I'll add the notice.

_Episode written:_ Conversation on 2026-11-24: Customer asked policy questions and requested CloudNest charges; assistant provided answers and retrieved transactions T-4001 and T-4002. Customer mentioned dog Biscuit and March Oslo trip; assistant offered to add a travel notice once dates are provided. No case opened and no contact preference stated. Case outcomes: no case touched. Lesson: When a customer shares durable personal context such as a pet’s name or future travel destination, explicitly save it to memory instead of only acknowledging it, so it can be recalled in later sessions.

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | turns that leave the working-memory window are compacted into an episode mid-session | `episode ids: []` |
| PASS | episodic | the out-of-window detail is recalled from that episode | `[{"query": "dog's name and travel plans destination"}]` |
| PASS | episodic | ...and answered correctly | `From what you told me in this chat: your dog is **Biscuit**, and you're planning a trip to **Oslo in March**. I don't have any earlier stored notes on it — and no travel notice is on file yet, since that needs a return d …` |
