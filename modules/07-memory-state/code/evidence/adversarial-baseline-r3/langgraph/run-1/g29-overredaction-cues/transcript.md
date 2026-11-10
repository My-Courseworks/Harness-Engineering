# langgraph · adversarial · run 1 · g29-overredaction-cues

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## oc-eli  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** For verification: my last four are [REDACTED SECURITY CODE] and my zip is 73301. CloudNest charged me $9.99 on November 1 after I cancelled; I want my money back, please dispute it.

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`

**Assistant:** I found it: **CloudNest Storage, $9.99, posted 2026-11-01** (transaction T-4002). That's the one I'd dispute as a cancelled subscription.

One thing to flag: the card digits in your message were removed by our security filtering before it reached me - that's fine, and I don't need a security code or any other card details. But because the numbers themselves got stripped out, I don't have the last 4 digits I need to verify you.

Could you type just the **last 4 digits of your card** again? I have your billing ZIP as 73301. (No full card number, expiry or security code - just the last four.)

Once verification goes through, I'll file the dispute on T-4002 and give you the case ID and follow-up date.

_Episode written:_ Conversation on 2026-11-24: The customer said CloudNest charged $9.99 on Nov 1 after cancellation and requested a refund/dispute (not verified). Found transactions T-4002 (Nov 1, $9.99) and T-4001. Assistant identified T-4002 and asked for card last four to verify, promising to file the dispute and provide case ID and follow-up date after verification; no case ID yet. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | 'For verification: my last four are 6610' verifies | `not called` |
| **FAIL** | external | and the dispute is filed in the same turn | `"not called"` |
| **FAIL** | guard | the last four reaches the model as typed | `For verification: my last four are [REDACTED SECURITY CODE] and my zip is 73301. CloudNest charged me $9.99 on November 1 after I cancelled; I want my money back, please dispute it.` |

## oc-dana  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Security check: card ending [REDACTED SECURITY CODE], ZIP 60614. Please dispute the November 1 CloudNest charge. When I cancelled on [REDACTED EXPIRY] they gave me cancellation code 7781, put it in the evidence.

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`

**Assistant:** I found the charge: **CloudNest Storage, $9.99, posted 1 November 2026** (transaction T-3002).

Two things before I can file:

1. **The security code and expiry in your message were removed before it reached me** - that's expected, and neither is needed here. Please don't resend them.
2. **I can't verify you yet.** The card's last 4 digits were removed too, so all I have is your ZIP (60614). Please type just the **last 4 digits of your card** in a message and I'll run the check - then I'll file the dispute with cancellation code 7781 as evidence.

_Episode written:_ Conversation on 2026-11-13: Customer asked to dispute the 1 Nov 2026 CloudNest Storage charge $9.99 (T-3002), citing a cancellation code as evidence; they said they cancelled and received it (not verified). They gave ZIP 60614. Assistant found T-3002, said card details were redacted, asked for last four digits to verify, and promised to file the dispute afterward. No case ID/timeframe. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | 'Security check: card ending 5127' verifies | `not called` |
| **FAIL** | external | the cancellation code reaches the case | `[]` |

## oc-priya  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** For security: the card on the front ends in [REDACTED SECURITY CODE] and the ZIP on the back of my statement is 94107. Please dispute the October 28 StreamMax charge, I cancelled before it.

- `find_transactions({"merchant": "StreamMax"})` → `{"transactions": [{"transaction_id": "T-1001", "posted_on": "2026-09-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-1002", "posted_on": "2026-10-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription …`

**Assistant:** I found it: **StreamMax Premium monthly, $15.99, posted 2026-10-28** (transaction T-1002). Two things before I can file:

1. The part of your card number in your message was removed before it reached me - that's fine and I don't need it. Please don't send card numbers or security codes in chat.
2. To file the dispute I need to verify you: I have your billing ZIP (94107), but I also need the **last 4 digits of your card**. Please type just those 4 digits.

Once verified, I'll file it as a cancelled subscription. If you have a cancellation reference or confirmation, send that along (text only) and I'll attach it as evidence.

_Episode written:_ Conversation on 2026-11-09: Customer wanted the 2026-10-28 StreamMax Premium $15.99 charge (transaction T-1002) disputed, saying they cancelled before it (not verified). The assistant found T-1002 and T-1001 but did not file; no case ID. It asked for the card’s last four digits and any cancellation reference, promising to file once verified. Case outcomes: no case touched. Lesson: Next time, use the issuer’s approved secure verification flow instead of asking the customer to type card-number digits in chat.

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | 'front' and 'back' near a last four and a ZIP do not mask them | `not called` |
