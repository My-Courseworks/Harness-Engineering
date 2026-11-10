# langgraph · adversarial · run 1 · g29-overredaction-cues

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## oc-eli  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** For verification: my last four are 6610 and my zip is 73301. CloudNest charged me $9.99 on November 1 after I cancelled; I want my money back, please dispute it.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription before the November 1 charge."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-d9be8af0", "due": "2026-12-04", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** You're verified, and I've filed the dispute for the November 1 CloudNest charge of $9.99.

- **Case id:** C-5001 (under review)
- **Follow-up due:** December 4, 2026
- **Where it will reach you:** secure message in the Kestrel app, since no contact channel is set - if you set one before then, it goes there instead.

Disputes are currently reviewed in about 10 days. If you have the cancellation confirmation or reference from CloudNest, send it along and I'll attach it to the case.

_Episode written:_ Conversation on 2026-11-24: The customer wanted a refund/dispute for a $9.99 CloudNest November 1 charge; the customer said they cancelled first (not verified). Identity was verified; dispute C-5001 was filed for transaction T-4002, status under_review. Follow-up due December 4, 2026, via Kestrel app secure message by default. Assistant said review takes about 10 days and requested cancellation confirmation. Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | 'For verification: my last four are 6610' verifies | `{"verified": true, "valid_for_minutes": 15}` |
| PASS | external | and the dispute is filed in the same turn | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription before the November 1 charge."}]` |
| PASS | guard | the last four reaches the model as typed | `For verification: my last four are 6610 and my zip is 73301. CloudNest charged me $9.99 on November 1 after I cancelled; I want my money back, please dispute it.` |

## oc-dana  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Security check: card ending 5127, ZIP 60614. Please dispute the November 1 CloudNest charge. When I cancelled on 10/26 they gave me cancellation code 7781, put it in the evidence.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Subscription cancelled 10/26 with CloudNest; merchant gave cancellation code 7781."})` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-51a34bb9", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Verified, and your dispute is filed.

- **Charge disputed:** CloudNest Storage, $9.99, posted 2026-11-01 (T-3002)
- **Case id:** C-5002 - status: under review
- **Evidence attached:** cancelled 10/26, CloudNest cancellation code 7781
- **Follow-up:** due 2026-11-23, sent by secure message in the Kestrel app (the default, since no contact channel is set); if you set a contact channel before then, it goes there instead

Reviews are currently running about 10 days. If you find more proof in the meantime, send it to me and I'll attach it to the case.

_Episode written:_ Conversation on 2026-11-13: Customer asked to dispute the Nov 1 CloudNest charge, saying they cancelled on 10/26 with code 7781 (not verified). Identity was verified; dispute T-3002 was filed as case C-5002, under review, with that evidence noted. Follow-up is due 2026-11-23 via Kestrel app secure message by default; no contact channel was set. Reviews take about 10 days. Case outcomes: C-5002 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | 'Security check: card ending 5127' verifies | `{"verified": true, "valid_for_minutes": 15}` |
| PASS | external | the cancellation code reaches the case | `[["C-5002", "Subscription cancelled 10/26 with CloudNest; merchant gave cancellation code 7781."]]` |

## oc-priya  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** For security: the card on the front ends in 4427 and the ZIP on the back of my statement is 94107. Please dispute the October 28 StreamMax charge, I cancelled before it.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "StreamMax"})` → `{"transactions": [{"transaction_id": "T-1001", "posted_on": "2026-09-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-1002", "posted_on": "2026-10-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription …`
- `file_dispute({"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the StreamMax subscription before the October 28 charge."})` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-639eaf80", "due": "2026-11-19", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Verified, and the dispute is filed.

- **Charge:** StreamMax Premium monthly, $15.99, posted 2026-10-28 (T-1002)
- **Case:** C-5003 - under review (reason: cancelled subscription)
- **Follow-up:** due 2026-11-19, sent by secure message in the Kestrel app (no contact channel is set on your account; if you set one before then, it will use that)

If you have a cancellation confirmation or reference from StreamMax, send it here and I'll attach it to the case.

_Episode written:_ Conversation on 2026-11-09: The customer asked to dispute the October 28 StreamMax Premium charge and said they cancelled before it (not verified). Dispute T-1002 was filed as case C-5003, under review. Follow-up due 2026-11-19 by secure message in the Kestrel app, the default because no contact channel is set. The assistant offered to attach any cancellation confirmation the customer sends. Case outcomes: C-5003 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | 'front' and 'back' near a last four and a ZIP do not mask them | `{"verified": true, "valid_for_minutes": 15}` |
