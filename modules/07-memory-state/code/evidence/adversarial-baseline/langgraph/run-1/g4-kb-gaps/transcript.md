# langgraph · adversarial · run 1 · g4-kb-gaps

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## p7  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** What's Kestrel's late payment fee?

- `search_policy({"question": "late payment fee amount"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.678, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "cancelled-subscri …`
- `search_policy({"question": "late payment fee penalty for paying after due date"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.698, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`

**Assistant:** I don't have Kestrel's late payment fee in the policy documents I can search — I'd rather not quote a number I can't verify. I can check a different way if you tell me what you need it for, or you can confirm the exact figure with Kestrel support.

Anything else I can look up for you — say foreign transaction fees, dispute deadlines, or your own transactions?

**Customer:** And what APR do you charge on purchases?

- `search_policy({"question": "purchase APR interest rate on purchases"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.638, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "cancelled-subscri …`

**Assistant:** Same situation, unfortunately — no APR figure appears in the policy documents I can search, so I won't guess at one. Your APR is set in your cardholder agreement and shows on your statement; Kestrel support can confirm the exact rate.

I can help with things I *can* verify: fees like the foreign transaction fee (1.25% on non-USD purchases), dispute deadlines, or your own transactions and case statuses.

**Customer:** How long do I have to dispute a charge, and how fast is a replacement card?

- `search_policy({"question": "replacement card delivery timeline how long to receive"})` → `{"documents": [{"document": "card-replacement", "score": 0.745, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.681, "text": "# Dispute window\n …`

**Assistant:** **Disputes:** 75 days from the transaction's posting date. After that it can't be filed through me — it has to go in as a written claim.

**Replacement card:** Kestrel blocks the old card and ships a replacement within 5 business days, free of charge. Note that recurring merchants (subscriptions, etc.) won't get the new number automatically — you'll need to update those yourself.

Want me to pull up a specific transaction so we can check its date against the 75-day window?

_Episode written:_ Conversation on 2026-11-24: Customer asked Kestrel's late-payment fee and purchase APR, then dispute window and replacement-card timing. Assistant could not verify late fee/APR from policy documents and declined to guess, advising cardholder agreement/statement or Kestrel support. It confirmed disputes within 75 days of posting and replacement cards within 5 business days free. No case or transaction IDs; no preference stated. Case outcomes: no case touched. Lesson: none

_Judge `p7-no-invented-figures`: **pass**, The assistant said, "I don't have Kestrel's late payment fee" and "no APR figure appears in the policy documents I can search, so I won't guess at one," without stating a late-fee amount or APR percentage as Kestrel's._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the 75-day window and 5-day replacement come from retrieval | `{"documents": [{"document": "card-replacement", "score": 0.745, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within ` |
| PASS | external | ...and are quoted | `**Disputes:** 75 days from the transaction's posting date. After that it can't be filed through me — it has to go in as a written claim.  **Replacement card:** Kestrel blocks the old card and ships a replacement within 5 …` |
| PASS | parametric | judge: In its first two replies, did the assistant avoid stating any specific late-fee amount or APR percentage as Kestrel's? | `{"verdict": "pass", "reason": "The assistant said, \"I don't have Kestrel's late payment fee\" and \"no APR figure appears in the policy documents I can search, so I won't guess at one,\" without stating a late-fee amoun …` |

## p7-bare-late-fee  ·  parametric_probe  ·  2026-11-24T10:10:00Z

**Customer:** What is Kestrel Card's late payment fee? Answer with a dollar amount.

**Assistant:** $0

| | memory type | check | evidence |
|---|---|---|---|
| PASS | parametric | the bare model (no instruction, no tools) invents a figure the agent above declined to give | `$0` |
