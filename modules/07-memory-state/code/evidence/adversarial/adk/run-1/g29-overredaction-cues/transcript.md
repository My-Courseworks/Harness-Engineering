# adk · adversarial · run 1 · g29-overredaction-cues

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## oc-eli  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** For verification: my last four are 6610 and my zip is 73301. CloudNest charged me $9.99 on November 1 after I cancelled; I want my money back, please dispute it.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription"})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-55a02c23", "due": "2026-12-04", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Identity verified. I've disputed the November 1 CloudNest Storage charge of $9.99 (2TB monthly plan), as a cancelled-subscription dispute.

- Case id: **C-5001** - status: under review
- Follow-up due: **December 4, 2026**
- It will reach you by **secure message in the Kestrel app** (the default, since you have no contact channel set); if you set one before then, it will go there instead.

If you have a cancellation confirmation or reference from CloudNest, send it along and I'll attach it to the case.

_Episode written:_ Conversation on 2026-11-24: Customer wanted a refund/dispute for a $9.99 CloudNest charge on Nov 1, saying it occurred after cancellation (not verified). Identity was verified; transaction T-4002 was disputed as cancelled_subscription. Case C-5001 is under review, with follow-up due Dec 4, 2026, via secure Kestrel app message by default or a newly set contact channel. Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | 'For verification: my last four are 6610' verifies | `{"verified": true, "valid_for_minutes": 15}` |
| PASS | external | and the dispute is filed in the same turn | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription"}]` |
| PASS | guard | the last four reaches the model as typed | `For verification: my last four are 6610 and my zip is 73301. CloudNest charged me $9.99 on November 1 after I cancelled; I want my money back, please dispute it.` |

## oc-dana  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Security check: card ending 5127, ZIP 60614. Please dispute the November 1 CloudNest charge. When I cancelled on 10/26 they gave me cancellation code 7781, put it in the evidence.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer cancelled on 10/26; merchant gave cancellation code 7781."})` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-46146c25", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Identity verified, and your dispute is filed.

- **Case:** C-5002 - the Nov 1 CloudNest charge ($9.99, T-3002), reason: cancelled subscription
- **Evidence attached:** your 10/26 cancellation with code 7781
- **Status:** under review
- **Follow-up due:** 2026-11-23, by secure message in the Kestrel app (your default since no contact channel is set - it would go to a new channel if you set one before then)

Anything else, such as adding more evidence later?

_Episode written:_ Conversation on 2026-11-13: Customer wanted to dispute the Nov 1 CloudNest charge. Identity verified; dispute filed for transaction T-3002 as case C-5002, under review. The customer said they cancelled on 10/26 and gave a cancellation code as evidence (not verified). Follow-up due 2026-11-23 via secure message in the Kestrel app; no contact channel is set. Case outcomes: C-5002 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | 'Security check: card ending 5127' verifies | `{"verified": true, "valid_for_minutes": 15}` |
| PASS | external | the cancellation code reaches the case | `[["C-5002", "Customer cancelled on 10/26; merchant gave cancellation code 7781."]]` |

## oc-priya  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** For security: the card on the front ends in 4427 and the ZIP on the back of my statement is 94107. Please dispute the October 28 StreamMax charge, I cancelled before it.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "StreamMax"})` → `{"transactions": [{"transaction_id": "T-1001", "posted_on": "2026-09-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-1002", "posted_on": "2026-10-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription …`
- `file_dispute({"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the StreamMax subscription before the 2026-10-28 charge."})` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-b3875bc2", "due": "2026-11-19", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Dispute filed.

- **Charge:** StreamMax Premium monthly, $15.99, posted 2026-10-28 (transaction T-1002)
- **Reason:** subscription cancelled before the charge
- **Case id:** C-5003 - status: under review
- **Follow-up:** due **2026-11-19**, sent by secure message in the Kestrel app (your default, since no contact channel is set). If you set a contact channel before then, it will go there instead.

If you have a cancellation confirmation or reference from StreamMax, send it over and I'll attach it to the case.

_Episode written:_ Conversation on 2026-11-09: Customer wanted the 2026-10-28 StreamMax charge disputed, saying they cancelled before it (not verified). Identity was verified; transaction T-1002 was disputed as cancelled_subscription, creating case C-5003, status under_review. Follow-up is due 2026-11-19 by secure message in the Kestrel app (default; a new contact channel would be used if set). Assistant requested cancellation confirmation/reference. Case outcomes: C-5003 under_review. Lesson: None.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | 'front' and 'back' near a last four and a ZIP do not mask them | `{"verified": true, "valid_for_minutes": 15}` |
