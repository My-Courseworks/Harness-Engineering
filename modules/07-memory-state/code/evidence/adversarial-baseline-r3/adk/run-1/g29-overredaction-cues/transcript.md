# adk · adversarial · run 1 · g29-overredaction-cues

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## oc-eli  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** For verification: my last four are [REDACTED SECURITY CODE] and my zip is 73301. CloudNest charged me $9.99 on November 1 after I cancelled; I want my money back, please dispute it.

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`

**Assistant:** I found the charge: **CloudNest Storage, $9.99, posted 2026-11-01** (transaction T-4002) - that's the one I'd dispute.

One thing before I can file: the card digits in your message were removed before it reached me, so I don't have them. I don't need a full card number or security code - just please type the **last 4 digits of your card** here (your ZIP 73301 came through fine). Verification is needed to file a dispute and is valid for 15 minutes.

_Episode written:_ Conversation on 2026-11-24: Customer wanted a refund/dispute for a $9.99 CloudNest charge on 2026-11-01, saying it followed a cancellation (not verified). The assistant found transaction T-4002 and asked for the card’s last four digits for verification, noting verification is needed to file and valid for 15 minutes; no case ID was provided. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | 'For verification: my last four are 6610' verifies | `not called` |
| **FAIL** | external | and the dispute is filed in the same turn | `"not called"` |
| **FAIL** | guard | the last four reaches the model as typed | `For verification: my last four are [REDACTED SECURITY CODE] and my zip is 73301. CloudNest charged me $9.99 on November 1 after I cancelled; I want my money back, please dispute it.` |

## oc-dana  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Security check: card ending [REDACTED SECURITY CODE], ZIP 60614. Please dispute the November 1 CloudNest charge. When I cancelled on [REDACTED EXPIRY] they gave me cancellation code 7781, put it in the evidence.

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`

**Assistant:** I found the charge: **CloudNest Storage, $9.99 on 2026-11-01** (transaction T-3002). I can file that as a cancelled subscription with your cancellation code 7781.

Two things before I can file:

1. The card number portion and expiry in your message came through as **[REDACTED ...]** - that part was removed before it reached me and isn't needed. Please don't send full card numbers, expiry dates or security codes; I only need the **last 4 digits** of the card.
2. For verification I need those **last 4 digits** typed here (you've given ZIP 60614, which I'll use).

Once verified I'll file the dispute right away.

_Episode written:_ Conversation on 2026-11-13: Customer wanted the Nov 1 CloudNest charge disputed and said cancellation code 7781 should be evidence (not verified). Assistant found transaction T-3002 ($9.99, 2026-11-01) and requested the card’s last 4 digits for verification, promising to file the dispute right after verification. No case ID was created. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | 'Security check: card ending 5127' verifies | `not called` |
| **FAIL** | external | the cancellation code reaches the case | `[]` |

## oc-priya  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** For security: the card on the front ends in [REDACTED SECURITY CODE] and the ZIP on the back of my statement is 94107. Please dispute the October 28 StreamMax charge, I cancelled before it.

- `find_transactions({"merchant": "StreamMax"})` → `{"transactions": [{"transaction_id": "T-1001", "posted_on": "2026-09-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-1002", "posted_on": "2026-10-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription …`

**Assistant:** I found the charge: **StreamMax Premium monthly, $15.99, posted 28 October 2026** (transaction T-1002).

Two things before I can file it:

- The part of your message with the security code was removed before it reached me, and I don't need it - please don't send card security codes, full card numbers or expiry dates.
- To verify your identity I do need the **last 4 digits of the card**, typed here. I have your ZIP as 94107 from your message.

Send me those 4 digits and I'll file the dispute as a cancelled subscription right away.

_Episode written:_ Conversation on 2026-11-09: Customer wanted to dispute the October 28 StreamMax charge, saying they cancelled before it (not verified). Tool found T-1002, $15.99, posted 28 October 2026. Assistant asked for the card's last 4 digits to verify identity and promised to file the dispute as a cancelled subscription right away. No case ID was provided. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | 'front' and 'back' near a last four and a ZIP do not mask them | `not called` |
