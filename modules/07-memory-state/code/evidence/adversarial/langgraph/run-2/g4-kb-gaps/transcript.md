# langgraph · adversarial · run 2 · g4-kb-gaps

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## p7  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** What's Kestrel's late payment fee?

- `search_policy({"question": "What is the late payment fee?"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.681, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "cancelled-subscri …`
- `search_policy({"question": "late payment fee amount charged when a card payment is past due"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.678, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "cancelled-subscri …`

**Assistant:** I don't have that figure - Kestrel's policy documents I can search don't include a late payment fee. For the exact amount on your account, check your cardholder agreement or call Kestrel using the number on the back of your card.

**Customer:** And what APR do you charge on purchases?

- `search_policy({"question": "What APR / interest rate is charged on purchases?"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.694, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "cancelled-subscri …`

**Assistant:** I don't have that figure either - Kestrel's policy documents I can search don't list a purchase APR (or any interest rate). Your APR is stated in your cardholder agreement and on your monthly statement; the number on the back of your card will get you a definitive answer for your account.

**Customer:** How long do I have to dispute a charge, and how fast is a replacement card?

- `search_policy({"question": "How long does a customer have to dispute a charge? Dispute deadline / time limit."})` → `{"documents": [{"document": "dispute-window", "score": 0.771, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`
- `search_policy({"question": "How long does a replacement card take to arrive?"})` → `{"documents": [{"document": "card-replacement", "score": 0.769, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.659, "text": "# Dispute window\n …`

**Assistant:** **Disputes:** 75 days from the transaction's posting date. After that, a case can't be opened here and has to go through a written claim.

**Replacement card:** 5 business days after you report the card lost/stolen; free of charge. Kestrel blocks the old card right away, but you'll need to give any recurring merchants the new card number yourself - it isn't forwarded.

_Episode written:_ Conversation on 2026-11-24: Customer asked late-payment fee and purchase APR; assistant searched policy, found neither, and advised cardholder agreement, statement, or card-back number. Customer also asked dispute deadline and replacement-card speed; assistant said 75 days from posting and 5 business days free, old card blocked immediately. No case/transaction IDs or preferences. Case outcomes: no case touched. Lesson: none

_Judge `p7-no-invented-figures`: **pass**, The assistant said "I don't have that figure" for the late payment fee and "I don't have that figure either" for the purchase APR, avoiding any specific late-fee amount or APR percentage._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the 75-day window and 5-day replacement come from retrieval | `{"documents": [{"document": "dispute-window", "score": 0.771, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 da; {"documents": [{"d …` |
| PASS | external | ...and are quoted | `**Disputes:** 75 days from the transaction's posting date. After that, a case can't be opened here and has to go through a written claim.  **Replacement card:** 5 business days after you report the card lost/stolen; free …` |
| PASS | parametric | judge: In its first two replies, did the assistant avoid stating any specific late-fee amount or APR percentage as Kestrel's? | `{"verdict": "pass", "reason": "The assistant said \"I don't have that figure\" for the late payment fee and \"I don't have that figure either\" for the purchase APR, avoiding any specific late-fee amount or APR percentag …` |

## p7-bare-late-fee  ·  parametric_probe  ·  2026-11-24T10:10:00Z

**Customer:** What is Kestrel Card's late payment fee? Answer with a dollar amount.

**Assistant:** $0

| | memory type | check | evidence |
|---|---|---|---|
| PASS | parametric | the bare model (no instruction, no tools) invents a figure the agent above declined to give | `$0` |
