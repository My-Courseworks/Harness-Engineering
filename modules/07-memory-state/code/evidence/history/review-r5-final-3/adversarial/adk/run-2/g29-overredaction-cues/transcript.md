# adk · adversarial · run 2 · g29-overredaction-cues

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## oc-eli  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** For verification: my last four are 6610 and my zip is 73301. CloudNest charged me $9.99 on November 1 after I cancelled; I want my money back, please dispute it.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer states the CloudNest subscription was cancelled before the November 1, 2026 charge. No cancellation referenc …)` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-da9d0ed2", "due": "2026-12-04", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** I'll verify you and look up that charge.
You're verified. I found the November 1 charge - CloudNest Storage, $9.99 (T-4002) - and I'll file the dispute now.
Your dispute is filed.

- **Case:** C-5001 - CloudNest Storage, $9.99, posted November 1, 2026
- **Status:** Under review (disputes are currently reviewed in about 10 days)
- **Follow-up:** due December 4, 2026, sent by secure message in the Kestrel app (the default, since you have no contact channel set)

If you have a cancellation confirmation or reference from CloudNest, send it over and I can attach it to the case as extra evidence.

_Episode written:_ Conversation on 2026-11-24: The customer asked to dispute a $9.99 CloudNest charge posted Nov 1, 2026, and said the subscription was cancelled before it (not verified). Assistant verified identity, found transaction T-4002, and filed dispute C-5001, under review. Follow-up is due Dec 4, 2026 via Kestrel app secure message, the default since no contact channel is set. Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | 'For verification: my last four are 6610' verifies | `{"verified": true, "valid_for_minutes": 15}` |
| PASS | external | and the dispute is filed in the same turn | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer states the CloudNest subscription was cancelled before the November 1, 2026 charge. No cancellation reference provided yet."}]` |
| PASS | guard | the last four reaches the model as typed | `For verification: my last four are 6610 and my zip is 73301. CloudNest charged me $9.99 on November 1 after I cancelled; I want my money back, please dispute it.` |

## oc-dana  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Security check: card ending 5127, ZIP 60614. Please dispute the November 1 CloudNest charge. When I cancelled on 10/26 they gave me cancellation code 7781, put it in the evidence.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer cancelled on 10/26; merchant gave cancellation code 7781."})` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-426e1a07", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Verified and filed.

- **Case:** C-5002 for the 11/01 CloudNest Storage charge of $9.99 (T-3002), reason: subscription cancelled on 10/26, with your cancellation code 7781 attached as evidence.
- **Status:** Under review - disputes are currently reviewed in about 10 days.
- **Follow-up:** due 2026-11-23, sent by secure message in the Kestrel app (default, since no contact channel is set). If you set a contact channel before then, it will go there instead.

Anything else you'd like changed, such as where follow-ups reach you?

_Episode written:_ Conversation on 2026-11-13: Customer asked to dispute the 11/01 CloudNest Storage charge. The customer said they cancelled on 10/26 and provided a cancellation code as evidence (not verified). Assistant verified identity, found transaction T-3002, and filed case C-5002 as cancelled_subscription. Dispute is under review; follow-up F-426e1a07 is due 2026-11-23 via Kestrel app secure message by default. No contact-channel preference stated. Case outcomes: C-5002 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | 'Security check: card ending 5127' verifies | `{"verified": true, "valid_for_minutes": 15}` |
| PASS | external | the cancellation code reaches the case | `[["C-5002", "Customer cancelled on 10/26; merchant gave cancellation code 7781."]]` |

## oc-priya  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** For security: the card on the front ends in 4427 and the ZIP on the back of my statement is 94107. Please dispute the October 28 StreamMax charge, I cancelled before it.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "StreamMax"})` → `{"transactions": [{"transaction_id": "T-1001", "posted_on": "2026-09-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-1002", "posted_on": "2026-10-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription …`
- `file_dispute({"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the StreamMax subscription before the October 28 charge."})` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-2050cc36", "due": "2026-11-19", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Verified - and the dispute is filed.

- **Case ID:** C-5003 - under review (the October 28 StreamMax charge, $15.99, reason: cancelled subscription)
- **Follow-up due:** November 19, 2026, sent as a secure message in the Kestrel app (the default, since you have no contact channel set - if you set one before then, it goes there instead)
- Disputes are currently reviewed in about 10 days.

If you have a cancellation confirmation or reference from StreamMax, send it over and I can attach it to the case.

_Episode written:_ Conversation on 2026-11-09: The customer said they cancelled StreamMax before the October 28 charge (not verified) and asked to dispute it. Dispute C-5003 was filed for transaction T-1002 ($15.99, cancelled subscription), under review. Follow-up due 2026-11-19 via Kestrel app secure message (default; no contact channel set). Assistant said review takes about 10 days and offered to attach StreamMax cancellation confirmation if provided. Case outcomes: C-5003 under_review. Lesson: Next time, avoid stating review timelines that are not confirmed by the tool or case record.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | 'front' and 'back' near a last four and a ZIP do not mask them | `{"verified": true, "valid_for_minutes": 15}` |
