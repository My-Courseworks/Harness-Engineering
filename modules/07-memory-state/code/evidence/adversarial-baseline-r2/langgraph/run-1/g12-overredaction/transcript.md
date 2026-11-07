# langgraph · adversarial · run 1 · g12-overredaction

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## or-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, I'm Dana. The last four digits are [REDACTED SECURITY CODE] and my zip is 60614. CloudNest charged me again on November 1 even though I cancelled in October. Please dispute it.

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `search_policy({"question": "Dispute deadline for a cancelled subscription charge (how many days after the transaction can I file?)"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.842, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`

**Assistant:** Thanks, Dana. I can see the charge: **CloudNest Storage, $9.99, posted 2026-11-01** (the October 1 one, also $9.99, was before your cancellation, so it can't be disputed on that ground). The November charge is within Kestrel's 75-day dispute window.

One thing before I can file: the card digits in your message were removed before it reached me — that part isn't needed and I never see it. To verify your identity I need the **last 4 digits of your card typed here** (just the last 4 — never the security code, expiry or full number). Your ZIP 60614 is noted.

Once verified, I'll file the dispute as *cancelled subscription* for transaction T-3002.

**Customer:** When I cancelled on [REDACTED EXPIRY] CloudNest gave me cancellation code [REDACTED SECURITY CODE]. Please put that in the dispute as evidence.

**Assistant:** I have the case ready to file — but both details in that message were removed before it reached me: the expiry date (card data, not needed and better not sent) and the cancellation code. So I don't have the code yet.

To finish up, please send in one plain message:
1. the **last 4 digits of your card** (just those four digits) — needed to verify identity, and
2. the **CloudNest cancellation code** re-typed as text — I'll attach it as the evidence note.

Nothing else needed: no full card number, security code or expiry.

_Episode written:_ Conversation on 2026-11-13: The customer said CloudNest charged again on [REDACTED SECURITY CODE]-[REDACTED EXPIRY] after October cancellation and gave a cancellation code (not verified); she asked to dispute the charge and attach the code as evidence. Assistant found T-[REDACTED SECURITY CODE] ($9.99), said T-[REDACTED SECURITY CODE] cannot be disputed, requested identity verification and code retyped, and promised to file T-[REDACTED SECURITY CODE] as cancelled_subscription once verified. Not filed; no case ID. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | the last four, as typed, verify the customer | `not called` |
| **FAIL** | external | the dispute is filed | `"not called"` |
| **FAIL** | external | the numeric cancellation code reaches the case as evidence | `[]` |

## or-decide  ·  resolve_case  ·  2026-11-20T09:00:00Z

_resolved:_ `[{"error": "no case C-5001: the dispute it stands for was never filed"}]`

## or-followup  ·  fire_followups  ·  2026-11-23T12:00:00Z

_outcomes:_ `[]`

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | guard | no masking token reaches an outbound message, and no identifier is ever masked | `Conversation on 2026-11-13: The customer said CloudNest charged again on [REDACTED SECURITY CODE]-[REDACTED EXPIRY] after October cancellation and gave a cancellation code (not verified); she asked to dispute the charge  …` |
