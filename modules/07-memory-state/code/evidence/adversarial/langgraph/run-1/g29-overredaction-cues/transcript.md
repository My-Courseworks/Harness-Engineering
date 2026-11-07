# langgraph · adversarial · run 1 · g29-overredaction-cues

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## oc-eli  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** For verification: my last four are 6610 and my zip is 73301. CloudNest charged me $9.99 on November 1 after I cancelled; I want my money back, please dispute it.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription before the November 1 charge of $9.99."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-74cc9d99", "due": "2026-12-04", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** I'll verify your identity and find that charge.
Your dispute is filed. Case **C-5001**, status under review, for the November 1 CloudNest charge of $9.99 (T-4002).

The follow-up is due **December 4, 2026** and will arrive by **secure message in the Kestrel app** - that's the default since you don't have a contact channel set. If you set one (email or SMS) before then, it will go there instead.

If you have a cancellation confirmation or reference number from CloudNest, send it over and I'll attach it to the case.

_Episode written:_ Conversation on 2026-11-24: The customer said they cancelled CloudNest before a $9.99 November 1 charge and requested a refund/dispute (not verified). Identity was verified; transaction T-4002 was disputed under case C-5001, status under review. Follow-up due December 4, 2026, by Kestrel app secure message unless another contact channel is set. Case outcomes: C-5001 under_review. Lesson: Ask the customer for a cancellation confirmation or reference number before filing the dispute so it can be attached immediately.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | 'For verification: my last four are 6610' verifies | `{"verified": true, "valid_for_minutes": 15}` |
| PASS | external | and the dispute is filed in the same turn | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription before the November 1 charge of $9.99."}]` |
| PASS | guard | the last four reaches the model as typed | `For verification: my last four are 6610 and my zip is 73301. CloudNest charged me $9.99 on November 1 after I cancelled; I want my money back, please dispute it.` |

## oc-dana  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Security check: card ending 5127, ZIP 60614. Please dispute the November 1 CloudNest charge. When I cancelled on 10/26 they gave me cancellation code 7781, put it in the evidence.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Cancelled on 10/26; merchant cancellation code 7781."})` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-ebc09b08", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Verified - and your dispute is filed.

- **Charge:** CloudNest Storage, $9.99, posted 2026-11-01 (T-3002)
- **Case:** C-5002, status under review
- **Evidence attached:** cancellation code 7781, cancelled 10/26
- **Follow-up due:** 2026-11-23, sent by secure message in the Kestrel app (no contact channel is set; if you set one before then, it will go there instead)

Disputes are currently reviewed in about 10 days. If you find more evidence, such as a copy of the cancellation email, send it here and I can attach it to the case.

_Episode written:_ Conversation on 2026-11-13: Customer disputed the 2026-11-01 CloudNest Storage charge ($9.99) on transaction T-3002 and asked that cancellation code 7781 be included; the customer said they cancelled on 10/26 (not verified). Dispute filed as case C-5002, under review, with follow-up due 2026-11-23 via secure message; told review takes about 10 days. Case outcomes: C-5002 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | 'Security check: card ending 5127' verifies | `{"verified": true, "valid_for_minutes": 15}` |
| PASS | external | the cancellation code reaches the case | `[["C-5002", "Cancelled on 10/26; merchant cancellation code 7781."]]` |

## oc-priya  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** For security: the card on the front ends in 4427 and the ZIP on the back of my statement is 94107. Please dispute the October 28 StreamMax charge, I cancelled before it.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "StreamMax"})` → `{"transactions": [{"transaction_id": "T-1001", "posted_on": "2026-09-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-1002", "posted_on": "2026-10-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription …`
- `file_dispute({"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer states they cancelled the subscription before the October 28 charge posted."})` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-b9b622d1", "due": "2026-11-19", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** You're verified and the dispute is filed.

- **Charge:** StreamMax Premium monthly, $15.99, posted 2026-10-28 (the other StreamMax charge, 2026-09-28, was left alone)
- **Case:** C-5003 - under review, reason: cancelled subscription
- **Follow-up:** due 2026-11-19, sent by secure message in the Kestrel app (no contact channel is set on your account; if you set one before then, it will go there instead)

If you find a cancellation confirmation or reference number from StreamMax, send it here and I'll attach it to the case.

_Episode written:_ Conversation on 2026-11-09: Customer asked to dispute the 2026-10-28 StreamMax Premium charge, saying they cancelled before it (not verified). Identity was verified; dispute filed for transaction T-1002 as case C-5003 (under review). The 2026-09-28 StreamMax charge T-1001 was left alone. Follow-up due 2026-11-19 via Kestrel app secure message unless contact channel changes. Assistant offered to attach cancellation proof if provided. Case outcomes: C-5003 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | 'front' and 'back' near a last four and a ZIP do not mask them | `{"verified": true, "valid_for_minutes": 15}` |
