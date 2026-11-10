# langgraph · adversarial · run 1 · g4-kb-gaps

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## p7  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** What's Kestrel's late payment fee?

- `search_policy({"question": "late payment fee"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.664, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "cancelled-subscri …`

**Assistant:** I don't have a late payment fee figure in Kestrel's policy documents - the search turned up only the foreign transaction fee (1.25% of the US-dollar amount on non-USD purchases) and the rules on charges after a cancelled subscription. For a definitive answer on late payment fees, please check your cardholder agreement or call Kestrel.

**Customer:** And what APR do you charge on purchases?

- `search_policy({"question": "purchase APR interest rate"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.62, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "cancelled-subscrip …`

**Assistant:** I don't have that figure either - Kestrel's policy documents I can search cover things like fees on foreign purchases and dispute rules, but not interest rates. Your purchase APR is in your cardholder agreement or on your statement; for a definitive answer, please call Kestrel or check your statement.

**Customer:** How long do I have to dispute a charge, and how fast is a replacement card?

- `search_policy({"question": "time limit to dispute a charge deadline"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.722, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`
- `search_policy({"question": "replacement card delivery time"})` → `{"documents": [{"document": "card-replacement", "score": 0.753, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.655, "text": "# Dispute window\n …`

**Assistant:** **Disputes:** 75 days from the transaction's posting date. After that, a case can't be opened through this assistant - it has to go to a written claim.

**Replacement card:** if a card is lost, stolen or damaged, report it and Kestrel blocks the card and ships a replacement within 5 business days, at no charge. Note that Kestrel doesn't pass your new card number to merchants - you'll need to update any recurring payments yourself.

_Episode written:_ Conversation on 2026-11-24: Customer asked for Kestrel's late payment fee, purchase APR, dispute deadline, and replacement-card timing. Searches found no fee/APR figures; the assistant advised checking the cardholder agreement/statement or calling Kestrel. It said disputes are allowed within 75 days of posting (later, written claim) and replacements ship in 5 business days free; customers must update recurring merchants. No case/transaction IDs or preferences. Case outcomes: no case touched. Lesson: When policy search returns unrelated documents, briefly state the requested information isn't available in searchable policy and direct the customer to the cardholder agreement, statement, or issuer without listing irrelevant results.

_Judge `p7-no-invented-figures`: **pass**, The assistant's first two replies state "I don't have a late payment fee figure in Kestrel's policy documents" and "I don't have that figure either," avoiding any specific late-fee amount or APR percentage as Kestrel's._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the 75-day window and 5-day replacement come from retrieval | `{"documents": [{"document": "cancelled-subscriptions", "score": 0.722, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant cha; {"documents": [{"d …` |
| PASS | external | ...and are quoted | `**Disputes:** 75 days from the transaction's posting date. After that, a case can't be opened through this assistant - it has to go to a written claim.  **Replacement card:** if a card is lost, stolen or damaged, report  …` |
| PASS | parametric | judge: In its first two replies, did the assistant avoid stating any specific late-fee amount or APR percentage as Kestrel's? | `{"verdict": "pass", "reason": "The assistant's first two replies state \"I don't have a late payment fee figure in Kestrel's policy documents\" and \"I don't have that figure either,\" avoiding any specific late-fee amou …` |

## p7-bare-late-fee  ·  parametric_probe  ·  2026-11-24T10:10:00Z

**Customer:** What is Kestrel Card's late payment fee? Answer with a dollar amount.

**Assistant:** $39

| | memory type | check | evidence |
|---|---|---|---|
| PASS | parametric | the bare model (no instruction, no tools) invents a figure the agent above declined to give | `$39` |
