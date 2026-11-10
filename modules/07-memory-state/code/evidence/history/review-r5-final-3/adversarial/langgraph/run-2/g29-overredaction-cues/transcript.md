# langgraph · adversarial · run 2 · g29-overredaction-cues

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## oc-eli  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** For verification: my last four are 6610 and my zip is 73301. CloudNest charged me $9.99 on November 1 after I cancelled; I want my money back, please dispute it.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription before the November 1 charge."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-d6367ffa", "due": "2026-12-04", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Verified, and your dispute is filed.

- **Charge:** CloudNest Storage, $9.99, posted 2026-11-01 (T-4002)
- **Case:** C-5001, status under review
- **Follow-up:** due 2026-12-04, arriving by secure message in the Kestrel app (your default, since no contact channel is set - if you set one before then, it goes there instead)

Disputes are currently reviewed in about 10 days. If you find a cancellation confirmation or reference number from CloudNest, send it to me and I'll attach it to the case.

_Episode written:_ Conversation on 2026-11-24: Customer wanted a $9.99 CloudNest charge posted 2026-11-01 refunded/disputed; they said they cancelled before the charge (not verified). Identity was verified, transaction T-4002 was disputed, and case C-5001 was filed under review. Follow-up due 2026-12-04 via Kestrel app secure message by default; review estimated about 10 days. Assistant will attach cancellation proof if provided. No contact-channel preference stated. Case outcomes: C-5001 under_review. Lesson: Ask for cancellation documentation and the customer's preferred contact channel before closing, so evidence and follow-up routing are clear.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | 'For verification: my last four are 6610' verifies | `{"verified": true, "valid_for_minutes": 15}` |
| PASS | external | and the dispute is filed in the same turn | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription before the November 1 charge."}]` |
| PASS | guard | the last four reaches the model as typed | `For verification: my last four are 6610 and my zip is 73301. CloudNest charged me $9.99 on November 1 after I cancelled; I want my money back, please dispute it.` |

## oc-dana  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Security check: card ending 5127, ZIP 60614. Please dispute the November 1 CloudNest charge. When I cancelled on 10/26 they gave me cancellation code 7781, put it in the evidence.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer cancelled on 10/26; merchant gave cancellation code 7781."})` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-12b55c97", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** I'll verify your identity and look up that charge.
Done - dispute filed.

- **Case:** C-5002 (under review)
- **Charge:** CloudNest Storage, $9.99, posted 2026-11-01
- **Reason:** cancelled subscription
- **Evidence:** cancellation on 10/26, code 7781
- **Follow-up:** due 2026-11-23, arriving by secure message in the Kestrel app (your default, since no contact channel is set - if you set one before then, it'll go there instead)

One note: your message included your last four and ZIP, which are part of this conversation's transcript. Please don't send full card numbers, security codes or expiry dates.

_Episode written:_ Conversation on 2026-11-13: Customer asked to dispute a Nov 1 CloudNest charge, saying they cancelled 10/26 with code 7781 (not verified) and wanted that as evidence. Identity verified. Dispute T-3002 filed as C-5002, under review. Follow-up due 2026-11-23 by secure Kestrel app message, or a new channel if set. Case outcomes: C-5002 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | 'Security check: card ending 5127' verifies | `{"verified": true, "valid_for_minutes": 15}` |
| PASS | external | the cancellation code reaches the case | `[["C-5002", "Customer cancelled on 10/26; merchant gave cancellation code 7781."]]` |

## oc-priya  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** For security: the card on the front ends in 4427 and the ZIP on the back of my statement is 94107. Please dispute the October 28 StreamMax charge, I cancelled before it.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "StreamMax"})` → `{"transactions": [{"transaction_id": "T-1001", "posted_on": "2026-09-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-1002", "posted_on": "2026-10-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription …`
- `file_dispute({"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the StreamMax subscription before the October 28 charge."})` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-4d9b591f", "due": "2026-11-19", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** You're verified, and the dispute is filed.

- **Case:** C-5003 - the StreamMax Premium charge of $15.99 posted October 28 (T-1002), disputed as a cancelled subscription
- **Status:** under review (about 10 days currently)
- **Follow-up:** due November 19 - it will reach you by secure message in the Kestrel app, since no contact channel is set. If you set one before then, it will go there instead.

If you have a cancellation confirmation or reference from StreamMax, send it to me and I'll attach it to the case.

_Episode written:_ Conversation on 2026-11-09: The customer asked to dispute the October 28 StreamMax Premium charge of $15.99, saying they cancelled before it (not verified). Identity was verified; dispute C-5003 was filed for transaction T-1002 and is under review. Follow-up is due November 19 by secure message in the Kestrel app because no contact channel is set. The assistant requested any StreamMax cancellation confirmation. Case outcomes: C-5003 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | 'front' and 'back' near a last four and a ZIP do not mask them | `{"verified": true, "valid_for_minutes": 15}` |
