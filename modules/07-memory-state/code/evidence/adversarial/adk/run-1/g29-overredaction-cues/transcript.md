# adk · adversarial · run 1 · g29-overredaction-cues

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## oc-eli  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** For verification: my last four are 6610 and my zip is 73301. CloudNest charged me $9.99 on November 1 after I cancelled; I want my money back, please dispute it.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription before the November 1 charge of $9.99."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-626c1a36", "due": "2026-12-04", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** You're verified, and the dispute is filed.

- **Case id:** C-5001 - the Nov 1 CloudNest Storage charge of $9.99 (T-4002), disputed as a cancelled subscription.
- **Status:** under review. Disputes are currently reviewed in about 10 days.
- **Follow-up:** due **December 4, 2026**, and it will reach you by secure message in the Kestrel app, since no contact channel is set. If you set one before then, it'll go there instead.

If you have a cancellation confirmation or reference number from CloudNest, send it over and I'll attach it to the case.

_Episode written:_ Conversation on 2026-11-24: Customer said they cancelled CloudNest before the Nov 1 $9.99 charge (not verified) and wanted a refund/dispute. Identity verified; dispute filed for T-4002 as C-5001, under review. Follow-up due Dec 4, 2026 via Kestrel secure message because no contact channel is set; a changed channel would be used. Assistant requested CloudNest cancellation confirmation/reference. Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | 'For verification: my last four are 6610' verifies | `{"verified": true, "valid_for_minutes": 15}` |
| PASS | external | and the dispute is filed in the same turn | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription before the November 1 charge of $9.99."}]` |
| PASS | guard | the last four reaches the model as typed | `For verification: my last four are 6610 and my zip is 73301. CloudNest charged me $9.99 on November 1 after I cancelled; I want my money back, please dispute it.` |

## oc-dana  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Security check: card ending 5127, ZIP 60614. Please dispute the November 1 CloudNest charge. When I cancelled on 10/26 they gave me cancellation code 7781, put it in the evidence.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer cancelled on 10/26; merchant gave cancellation code 7781."})` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-156f8f9f", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Verified - and the dispute is filed.

- **Charge:** CloudNest Storage, $9.99, posted 2026-11-01 (T-3002)
- **Case id:** C-5002 - status: under review
- **Evidence attached:** cancellation on 10/26, cancellation code 7781
- **Follow-up due:** 2026-11-23, sent by secure message in the Kestrel app (the default, since no contact channel is set). If you set a channel before then, it will go there instead.

One note: the code 7781 reached me fine. If you ever need to send a full card number, security code or expiry date, please don't - those aren't needed here.

_Episode written:_ Conversation on 2026-11-13: Customer asked to dispute the 2026-11-01 CloudNest charge; the customer said they cancelled on 10/26 and provided cancellation code 7781 (not verified) as evidence. Identity was verified, and the assistant filed dispute case C-5002 for transaction T-3002. Follow-up F-156f8f9f is due 2026-11-23 via Kestrel app secure message unless the contact channel is changed. Case outcomes: C-5002 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | 'Security check: card ending 5127' verifies | `{"verified": true, "valid_for_minutes": 15}` |
| PASS | external | the cancellation code reaches the case | `[["C-5002", "Customer cancelled on 10/26; merchant gave cancellation code 7781."]]` |

## oc-priya  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** For security: the card on the front ends in 4427 and the ZIP on the back of my statement is 94107. Please dispute the October 28 StreamMax charge, I cancelled before it.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "StreamMax"})` → `{"transactions": [{"transaction_id": "T-1001", "posted_on": "2026-09-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-1002", "posted_on": "2026-10-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription …`
- `file_dispute({"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the StreamMax subscription before the October 28 charge."})` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-46d84568", "due": "2026-11-19", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** You're verified, and the dispute is filed.

- **Charge:** StreamMax Premium monthly, $15.99, posted 2026-10-28 (transaction T-1002)
- **Case:** C-5003, reason: cancelled subscription - now under review
- **Follow-up:** due 2026-11-19, sent as a secure message in the Kestrel app (the default, since no contact channel is set); if you set a contact channel before then, it will go there instead

If you have a cancellation reference or confirmation email from StreamMax, send it along and I'll attach it to the case.

_Episode written:_ Conversation on 2026-11-09: Customer wanted the 2026-10-28 StreamMax charge disputed, saying they cancelled before it (not verified). Identity was verified; dispute filed for transaction T-1002 as case C-5003, under review. Follow-up due 2026-11-19 via Kestrel app secure message by default unless a contact channel is set. Assistant asked for cancellation reference/email to attach. Case outcomes: C-5003 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | 'front' and 'back' near a last four and a ZIP do not mask them | `{"verified": true, "valid_for_minutes": 15}` |
