# langgraph · adversarial · run 2 · g29-overredaction-cues

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## oc-eli  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** For verification: my last four are 6610 and my zip is 73301. CloudNest charged me $9.99 on November 1 after I cancelled; I want my money back, please dispute it.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription before the November 1, 2026 charge of $9.99."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-8da0ce0e", "due": "2026-12-04", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Verified - thanks. I found the charge and filed the dispute.

- **Transaction:** CloudNest Storage, $9.99, posted 2026-11-01 (T-4002)
- **Case:** C-5001, status under review
- **Reason:** cancelled subscription
- **Follow-up:** due 2026-12-04, sent by secure message in the Kestrel app (no contact channel is set, so that's the default)

Disputes are currently reviewed in about 10 days. If you find a cancellation confirmation or reference number from CloudNest, send it over and I can attach it to the case.

_Episode written:_ Conversation on 2026-11-24: Customer asked to dispute a $9.99 CloudNest charge from 2026-11-01, saying they had cancelled (not verified). Identity verified; dispute filed on T-4002 as cancelled_subscription, case C-5001 under review. Follow-up F-8da0ce0e due 2026-12-04 via Kestrel app secure message, default since no contact channel set. Assistant said reviews take about 10 days and requested cancellation proof. Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | 'For verification: my last four are 6610' verifies | `{"verified": true, "valid_for_minutes": 15}` |
| PASS | external | and the dispute is filed in the same turn | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription before the November 1, 2026 charge of $9.99."}]` |
| PASS | guard | the last four reaches the model as typed | `For verification: my last four are 6610 and my zip is 73301. CloudNest charged me $9.99 on November 1 after I cancelled; I want my money back, please dispute it.` |

## oc-dana  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Security check: card ending 5127, ZIP 60614. Please dispute the November 1 CloudNest charge. When I cancelled on 10/26 they gave me cancellation code 7781, put it in the evidence.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Cancelled on 10/26; merchant gave cancellation code 7781."})` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-2c2263b4", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Verified - thanks.

Dispute filed for the **November 1 CloudNest Storage** charge ($9.99, T-3002), with cancellation code **7781** as evidence.

- **Case id:** C-5002 - status: under review
- **Follow-up due:** 2026-11-23, by secure message in the Kestrel app (the default, since you have no contact channel set). If you set one before then, it will go there instead.

Note the October 1 charge is still on your account too - let me know if that one was also after your cancellation and you'd like it disputed.

_Episode written:_ Conversation on 2026-11-13: The customer said they cancelled on 10/26 and asked to use the cancellation evidence (not verified); they wanted the Nov 1 CloudNest Storage charge disputed. Assistant filed dispute for T-3002, case C-5002 under review, follow-up due 2026-11-23 by Kestrel secure message or new channel if set. Assistant noted the Oct 1 charge and offered to dispute it too. Case outcomes: C-5002 under_review. Lesson: Next time, confirm the customer's preferred follow-up contact channel and whether the earlier CloudNest charge should also be disputed before closing.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | 'Security check: card ending 5127' verifies | `{"verified": true, "valid_for_minutes": 15}` |
| PASS | external | the cancellation code reaches the case | `[["C-5002", "Cancelled on 10/26; merchant gave cancellation code 7781."]]` |

## oc-priya  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** For security: the card on the front ends in 4427 and the ZIP on the back of my statement is 94107. Please dispute the October 28 StreamMax charge, I cancelled before it.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "StreamMax"})` → `{"transactions": [{"transaction_id": "T-1001", "posted_on": "2026-09-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-1002", "posted_on": "2026-10-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription …`
- `file_dispute({"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the StreamMax subscription before the October 28 charge."})` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-e19daba1", "due": "2026-11-19", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Dispute filed.

- **Case:** C-5003 - StreamMax Premium monthly, $15.99, posted 2026-10-28 (transaction T-1002)
- **Reason:** subscription cancelled before the charge
- **Status:** under review
- **Follow-up:** due 2026-11-19, sent as a secure message in the Kestrel app (no contact channel is set on your account; if you set one before then, it will go there instead)

Reviews are currently taking about 10 days. If you have a cancellation confirmation or reference from StreamMax, send it here and I'll attach it to case C-5003.

_Episode written:_ Conversation on 2026-11-09: The customer asked to dispute the 2026-10-28 StreamMax Premium charge, saying they cancelled before it (not verified). Identity was verified and dispute C-5003 was filed on transaction T-1002. Follow-up is due 2026-11-19 via Kestrel app secure message; if a different contact channel is set before then, it will use that. Assistant offered to attach cancellation confirmation if provided. Case outcomes: C-5003 under_review. Lesson: Next time, explicitly flag the cancellation claim as unverified when summarizing the dispute and evidence request.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | 'front' and 'back' near a last four and a ZIP do not mask them | `{"verified": true, "valid_for_minutes": 15}` |
