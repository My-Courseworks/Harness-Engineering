# langgraph · adversarial · run 1 · g29-overredaction-cues

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## oc-eli  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** For verification: my last four are 6610 and my zip is 73301. CloudNest charged me $9.99 on November 1 after I cancelled; I want my money back, please dispute it.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription before the November 1 charge."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-76fa774b", "due": "2026-12-04", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** You're verified, and I've filed the dispute.

- **Case:** C-5001 - CloudNest Storage, $9.99, posted November 1, 2026 (T-4002)
- **Reason:** cancelled subscription
- **Status:** under review
- **Follow-up:** due December 4, 2026, sent by secure message in the Kestrel app (the default, since you have no contact channel set - if you change it before then, the follow-up will use the new one)

If you have a cancellation confirmation or reference from CloudNest, send it along and I'll attach it to the case - that helps the review.

_Episode written:_ Conversation on 2026-11-24: Customer said they cancelled CloudNest before a $9.99 Nov. 1 charge (not verified) and asked to dispute it. Dispute filed on T-4002, case C-5001, under review. Follow-up F-76fa774b due Dec. 4, 2026 via Kestrel app secure message (default; no contact channel set). Assistant requested CloudNest cancellation confirmation/reference to attach. Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | 'For verification: my last four are 6610' verifies | `{"verified": true, "valid_for_minutes": 15}` |
| PASS | external | and the dispute is filed in the same turn | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription before the November 1 charge."}]` |
| PASS | guard | the last four reaches the model as typed | `For verification: my last four are 6610 and my zip is 73301. CloudNest charged me $9.99 on November 1 after I cancelled; I want my money back, please dispute it.` |

## oc-dana  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Security check: card ending 5127, ZIP 60614. Please dispute the November 1 CloudNest charge. When I cancelled on 10/26 they gave me cancellation code 7781, put it in the evidence.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled on 10/26; merchant gave cancellation code 7781."})` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-c0e89c0b", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Done. Details:

- **Dispute filed:** CloudNest Storage, $9.99, posted 2026-11-01 - case **C-5002**, status under review.
- **Reason:** cancelled subscription, with your cancellation code 7781 in the evidence.
- **Follow-up:** due **2026-11-23**, sent by secure message in the Kestrel app (no contact channel is set on your account; if you set one before then, it will use that instead).

Your verification is valid until 10:15 UTC if you need anything else that requires it.

_Episode written:_ Conversation on 2026-11-13: Customer asked to dispute the 2026-11-01 CloudNest Storage charge. Identity verified; transactions found. Dispute filed on T-3002 as case C-5002, under review, reason cancelled subscription; the customer said they cancelled on 10/26 with a cancellation code (not verified). Follow-up due 2026-11-23 via Kestrel app secure message; no contact channel set, so default. Case outcomes: C-5002 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | 'Security check: card ending 5127' verifies | `{"verified": true, "valid_for_minutes": 15}` |
| PASS | external | the cancellation code reaches the case | `[["C-5002", "Customer says they cancelled on 10/26; merchant gave cancellation code 7781."]]` |

## oc-priya  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** For security: the card on the front ends in 4427 and the ZIP on the back of my statement is 94107. Please dispute the October 28 StreamMax charge, I cancelled before it.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "StreamMax"})` → `{"transactions": [{"transaction_id": "T-1001", "posted_on": "2026-09-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-1002", "posted_on": "2026-10-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription …`
- `file_dispute({"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the StreamMax subscription before the October 28, 2026 charge."})` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-fc2acfb8", "due": "2026-11-19", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Verified, and the dispute is filed.

- **Case:** C-5003 - the October 28 StreamMax Premium charge of $15.99 (T-1002), disputed as a cancelled subscription.
- **Status:** under review (disputes are reviewed in about 10 days).
- **Follow-up:** due 2026-11-19, sent by secure message in the Kestrel app - the default, since you have no contact channel set. If you set one before then, the follow-up will go there instead.

If you have proof of the cancellation (a cancellation reference, confirmation email, etc.), send it along and I can attach it to case C-5003.

_Episode written:_ Conversation on 2026-11-09: Customer disputed the October 28 StreamMax charge, saying they cancelled before it (not verified). Identity was verified; T-1002 was found and dispute C-5003 filed as cancelled subscription. Status: under_review, review about 10 days; follow-up due 2026-11-19 via default Kestrel app secure message because no contact channel is set. Assistant offered to attach cancellation proof. Case outcomes: C-5003 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | 'front' and 'back' near a last four and a ZIP do not mask them | `{"verified": true, "valid_for_minutes": 15}` |
