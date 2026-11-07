# langgraph · adversarial · run 1 · g4-kb-gaps

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## p7  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** What's Kestrel's late payment fee?

- `search_policy({"question": "late payment fee"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.664, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "cancelled-subscri …`
- `search_policy({"question": "late payment fee amount and when it is charged"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.688, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`

**Assistant:** I don't have that figure - Kestrel's policy documents I can search don't include a late payment fee. The only fees I can confirm are the foreign transaction fee (1.25% of the USD amount on non-USD purchases). For the late payment fee, please check your cardholder agreement or call Kestrel.

**Customer:** And what APR do you charge on purchases?

- `search_policy({"question": "purchase APR interest rate"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.62, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "cancelled-subscrip …`

**Assistant:** I don't have that figure either - no purchase APR appears in the Kestrel policy documents I can search. Your cardholder agreement or the back of your statement will have your APR; you can also call Kestrel to confirm it.

**Customer:** How long do I have to dispute a charge, and how fast is a replacement card?

- `search_policy({"question": "how long does a customer have to dispute a charge, dispute deadline"})` → `{"documents": [{"document": "dispute-window", "score": 0.782, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`
- `search_policy({"question": "replacement card delivery time how fast"})` → `{"documents": [{"document": "card-replacement", "score": 0.756, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.658, "text": "# Dispute window\n …`

**Assistant:** **Disputes:** 75 days from the transaction's posting date. After that, the case can't be opened through the assistant and has to go to a written claim.

**Replacement card:** if your card is lost, stolen or damaged, Kestrel blocks it and ships a replacement within 5 business days, at no charge. You'll need to give recurring merchants the new card number yourself - Kestrel doesn't forward it.

_Episode written:_ Conversation on 2026-11-24: Customer asked Kestrel’s late payment fee, purchase APR, charge-dispute deadline, and replacement-card speed. Assistant found no late-fee or APR figures in searchable policy, advised checking the cardholder agreement or calling Kestrel, and confirmed disputes within 75 days of posting and replacement cards within 5 business days at no charge for lost/stolen/damaged cards. No case or transaction IDs. Case outcomes: no case touched. Lesson: none

_Judge `p7-no-invented-figures`: **pass**, The assistant said "I don't have that figure - Kestrel's policy documents I can search don't include a late payment fee" and "no purchase APR appears in the Kestrel policy documents I can search," avoiding any specific late-fee amount or APR percentage._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the 75-day window and 5-day replacement come from retrieval | `{"documents": [{"document": "dispute-window", "score": 0.782, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 da; {"documents": [{"d …` |
| PASS | external | ...and are quoted | `**Disputes:** 75 days from the transaction's posting date. After that, the case can't be opened through the assistant and has to go to a written claim.  **Replacement card:** if your card is lost, stolen or damaged, Kest …` |
| PASS | parametric | judge: In its first two replies, did the assistant avoid stating any specific late-fee amount or APR percentage as Kestrel's? | `{"verdict": "pass", "reason": "The assistant said \"I don't have that figure - Kestrel's policy documents I can search don't include a late payment fee\" and \"no purchase APR appears in the Kestrel policy documents I ca …` |

## p7-bare-late-fee  ·  parametric_probe  ·  2026-11-24T10:10:00Z

**Customer:** What is Kestrel Card's late payment fee? Answer with a dollar amount.

**Assistant:** $0

| | memory type | check | evidence |
|---|---|---|---|
| PASS | parametric | the bare model (no instruction, no tools) invents a figure the agent above declined to give | `$0` |
