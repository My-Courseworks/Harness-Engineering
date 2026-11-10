# langgraph · adversarial · run 1 · g8-overflow

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## long-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Just chatting first: my dog's name is Biscuit and I'm planning a trip to Oslo in March.

**Assistant:** Nice to meet Biscuit! And Oslo in March sounds great - brisk, but the fjord views are worth it.

Two quick notes since you're just chatting:

- I can only save two kinds of personal facts for you: a contact channel and a travel notice - so I haven't noted Biscuit anywhere.
- If you'd like, I can put a travel notice on file for Oslo once you know your dates (I just need the destination and the date you return). That way your card use abroad isn't mistaken for unusual activity. The profile currently shows no travel notice on file.

Want me to set that up now, or wait until your plans firm up?

**Customer:** What is a chargeback, in one sentence?

**Assistant:** A chargeback is when your card issuer reverses a disputed charge and pulls the money back from the merchant's bank, which then has the chance to contest it.

**Customer:** What's an authorization hold, in one sentence?

**Assistant:** An authorization hold is a temporary reservation placed on part of your available credit when a merchant checks your card, before the charge actually settles.

**Customer:** What foreign transaction fee does Kestrel charge?

- `search_policy({"question": "foreign transaction fee"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.858, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "travel-notices",  …`

**Assistant:** Kestrel charges **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. It posts as a separate line on the same day as the purchase, and a travel notice doesn't waive or change it.

**Customer:** How long do I have to dispute a charge?

- `search_policy({"question": "dispute deadline how long to dispute a charge"})` → `{"documents": [{"document": "dispute-window", "score": 0.783, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** **75 days from the posting date.** After that, a dispute can't be opened through the assistant and has to go in as a written claim.

**Customer:** How fast is a replacement card?

- `search_policy({"question": "replacement card delivery time"})` → `{"documents": [{"document": "card-replacement", "score": 0.753, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.655, "text": "# Dispute window\n …`

**Assistant:** A replacement ships within **5 business days**, at no charge. Note that Kestrel doesn't forward your new card number to recurring merchants - you'll need to update those yourself.

**Customer:** What contact channels can you use?

- `search_policy({"question": "contact channel options email sms secure message"})` → `{"documents": [{"document": "contact-preferences", "score": 0.749, "text": "# Contact preferences\n\nKestrel can contact you about cases and reminders by **email**, **sms** (text message), or **secure_message** (the inbox in the Kestrel app). If you have not chosen a channel, Kestrel uses secure_message. Changing your contact channel requires identity verification, because a changed channel is a c …`

**Assistant:** Three options: **email**, **sms** (text message), or **secure_message** (the inbox in the Kestrel app).

Your profile currently has no channel chosen, so anything I send - case follow-ups and reminders - goes by secure message in the app. Changing it requires identity verification (card last 4 and billing ZIP, plus a one-time code). Want to switch to email or sms?

**Customer:** What is a travel notice for?

**Assistant:** A travel notice tells Kestrel's fraud systems that card use in another country is expected, which cuts down on false declines while you're away. I just need the destination and your return date; Kestrel keeps it only until that date and then deletes it automatically, so each new trip needs a new notice.

For your Oslo trip in March, I can set it up whenever you know the return date.

**Customer:** What happens after a dispute is filed?

- `search_policy({"question": "what happens after a dispute is filed review timeline evidence"})` → `{"documents": [{"document": "dispute-window", "score": 0.721, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** Once a dispute is filed, the Kestrel disputes team reviews it and forwards it to the merchant. For a cancelled-subscription charge, the merchant has 10 business days to respond; the disputes team then decides the case and records the outcome and its reason on the case. You can add more evidence to an open case any time while it's open.

Two things to know:
- The window: you can dispute a posted transaction within **75 days of its posting date**; after that it has to go in as a written claim.
- Filing schedules a follow-up automatically. With no contact channel set, it reaches you by secure message in the Kestrel app.

One correction: I mentioned an "Oslo trip in March" last message - that was my mistake. There's no travel notice on your account and you hadn't told me about one.

**Customer:** Do travel notices change fees?

- `search_policy({"question": "do travel notices affect fees foreign transaction fee"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.78, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "travel-notices", " …`

**Assistant:** No. A travel notice doesn't change or waive fees - it only reduces the chance of false declines while you're away.

Foreign purchases still carry Kestrel's **1.25% fee on the US-dollar amount** for any purchase in a currency other than USD, posted as a separate line on the same day as the purchase.

**Customer:** What is a cancelled-subscription dispute?

**Assistant:** It's a dispute for a recurring subscription or membership you cancelled but were charged for again afterwards. You file it with the reason **cancelled_subscription**; Kestrel sends it to the merchant, who has 10 business days to respond, then the disputes team decides and records the outcome.

Important limit: charges made *before* you cancelled are valid and can't be disputed on that ground. It also has to be within **75 days of the charge's posting date**.

**Customer:** Can you show my CloudNest charges?

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`

**Assistant:** You have two CloudNest Storage charges:

| Date | Description | Amount |
|---|---|---|
| 2026-10-01 | CloudNest 2TB monthly | $9.99 |
| 2026-11-01 | CloudNest 2TB monthly | $9.99 |

Both are subscriptions, in USD. If one of these was charged after you cancelled, it can be disputed within 75 days of its posting date.

**Customer:** What's the difference between a pending and a posted charge, in one sentence?

**Assistant:** A pending charge is an authorization that temporarily holds part of your available credit while the merchant finalizes the transaction, whereas a posted charge is a completed transaction that has been added to your balance.

**Customer:** What did I say my dog's name was, and where am I going in March?

- `load_memory({"query": "dog's name and March travel plans"})` → `{"memories": [{"at": "2026-11-24T10:26:00Z", "text": "Conversation on 2026-11-24: Customer asked about replacement card timing, contact channels, travel notices, dispute handling, and whether travel notices affect fees. Assistant explained 5-business-day replacement, secure message default, dispute review, 75-day window, and 1.25% foreign fee. No case/transaction IDs, promises, or preferences; ass …`

**Assistant:** I have no record of a dog's name - nothing about that in your past conversations or your profile.

For March: one earlier conversation mentions a trip to **Oslo**, but that was never confirmed and there's **no travel notice on file** for your account, so I can't treat it as your plan. If you'd like, tell me the destination and return date and I'll add a travel notice.

_Episode written:_ Conversation on 2026-11-24: Customer asked about cancelled-subscription disputes, their CloudNest charges, pending vs posted charges, and their dog name/March travel plans. Assistant explained dispute rules, listed CloudNest charges T-4001 and T-4002, explained pending/posted charges, and said no dog-name record; an earlier Oslo reference was unconfirmed with no travel notice on file. No dispute/case was opened; assistant offered to add a travel notice if destination/return date provided. Case outcomes: no case touched. Lesson: When a travel plan is unconfirmed, do not repeat the destination from memory; say only that no confirmed March travel plan is on file unless the customer provides one.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | turns that leave the working-memory window are compacted into an episode mid-session | `episode ids: ['E-long-s1-1-ea3689', 'E-long-s1-2-0d1ff6', 'E-long-s1-3-cf900f']` |
| PASS | episodic | the out-of-window detail is recalled from that episode | `[{"query": "dog's name and March travel plans"}]` |
| **FAIL** | episodic | ...and answered correctly | `I have no record of a dog's name - nothing about that in your past conversations or your profile.  For March: one earlier conversation mentions a trip to **Oslo**, but that was never confirmed and there's **no travel not …` |
