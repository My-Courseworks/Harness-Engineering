# adk · adversarial · run 1 · g29-overredaction-cues

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## oc-eli  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** For verification: my last four are 6610 and my zip is 73301. CloudNest charged me $9.99 on November 1 after I cancelled; I want my money back, please dispute it.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription before the November 1 charge."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-0e3494e9", "due": "2026-12-04", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** You're verified, and I've filed the dispute for the November 1 CloudNest charge.

- **Case:** C-5001 (CloudNest Storage, $9.99, posted 2026-11-01) - status: under review
- **Reason:** cancelled subscription
- **Follow-up:** due 2026-12-04, sent by secure message in the Kestrel app (the default, since no contact channel is set). If you set a contact channel before then, it will go there instead.

If you have a cancellation confirmation or reference from CloudNest, I can attach it to the case - that would strengthen it.

_Episode written:_ Conversation on 2026-11-24: Customer said the CloudNest $9.99 charge on 2026-11-01 came after cancellation (not verified); they wanted it disputed/refunded. Identity verified; dispute filed on T-4002 as C-5001, under review. Follow-up due 2026-12-04 via secure app message (no contact channel set). Assistant offered to attach cancellation proof if provided. Case outcomes: C-5001 under_review. Lesson: Next time, ask for cancellation confirmation or reference before filing and confirm the customer's preferred contact channel so the follow-up reaches them.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | 'For verification: my last four are 6610' verifies | `{"verified": true, "valid_for_minutes": 15}` |
| PASS | external | and the dispute is filed in the same turn | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription before the November 1 charge."}]` |
| PASS | guard | the last four reaches the model as typed | `For verification: my last four are 6610 and my zip is 73301. CloudNest charged me $9.99 on November 1 after I cancelled; I want my money back, please dispute it.` |

## oc-dana  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Security check: card ending 5127, ZIP 60614. Please dispute the November 1 CloudNest charge. When I cancelled on 10/26 they gave me cancellation code 7781, put it in the evidence.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer cancelled on 10/26; merchant gave cancellation code 7781."})` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-a3d7750d", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Verified - thanks. Your dispute is filed:

- **Case:** C-5002, for the $9.99 CloudNest Storage charge posted 2026-11-01
- **Reason:** cancelled subscription
- **Evidence:** your cancellation code 7781 and the 10/26 cancellation date
- **Status:** under review (currently about 10 days)
- **Follow-up:** due 2026-11-23, sent by secure message in the Kestrel app, since no contact channel is set. If you set one before then (email or SMS), it will go there instead.

Note: the earlier CloudNest charge from 2026-10-01 is a separate one - let me know if that should be disputed too.

_Episode written:_ Conversation on 2026-11-13: The customer wanted the 2026-11-01 CloudNest charge disputed; they said they cancelled on 10/26 and provided cancellation code 7781 (not verified). Identity was verified, and a dispute for transaction T-3002 was filed as case C-5002, status under_review. Follow-up is due 2026-11-23 by Kestrel app secure message, since no contact channel is set. Case outcomes: C-5002 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | 'Security check: card ending 5127' verifies | `{"verified": true, "valid_for_minutes": 15}` |
| PASS | external | the cancellation code reaches the case | `[["C-5002", "Customer cancelled on 10/26; merchant gave cancellation code 7781."]]` |

## oc-priya  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** For security: the card on the front ends in 4427 and the ZIP on the back of my statement is 94107. Please dispute the October 28 StreamMax charge, I cancelled before it.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "StreamMax"})` → `{"transactions": [{"transaction_id": "T-1001", "posted_on": "2026-09-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-1002", "posted_on": "2026-10-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription …`
- `file_dispute({"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the StreamMax subscription before the October 28 charge."})` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-6256d071", "due": "2026-11-19", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Verified - thanks. I found two StreamMax charges and filed the October 28 one ($15.99, "StreamMax Premium monthly").

- **Case ID:** C-5003 - status: under review
- **Follow-up due:** 2026-11-19, sent by secure message in the Kestrel app (no contact channel is set; if you set one before then, it will go there instead)

Disputes are currently reviewed in about 10 days. If you have a cancellation confirmation or reference from StreamMax, send it over and I'll attach it to the case.

_Episode written:_ Conversation on 2026-11-09: Customer asked to dispute the October 28 StreamMax charge, saying they cancelled before it (not verified). Identity was verified; the $15.99 charge was filed as case C-5003 for transaction T-1002, under review. Follow-up F-6256d071 is due 2026-11-19 by Kestrel app secure message; no contact channel is set, so an updated channel will be used. Case outcomes: C-5003 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | 'front' and 'back' near a last four and a ZIP do not mask them | `{"verified": true, "valid_for_minutes": 15}` |
