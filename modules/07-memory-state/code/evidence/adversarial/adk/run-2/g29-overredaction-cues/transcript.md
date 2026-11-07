# adk · adversarial · run 2 · g29-overredaction-cues

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## oc-eli  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** For verification: my last four are 6610 and my zip is 73301. CloudNest charged me $9.99 on November 1 after I cancelled; I want my money back, please dispute it.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says the subscription was cancelled before the November 1 charge."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-0683f4b4", "due": "2026-12-04", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Thanks - you're verified, and the dispute is filed.

- **Charge:** CloudNest Storage, $9.99, posted 2026-11-01 (T-4002)
- **Case id:** C-5001 - status: under review
- **Follow-up due:** 2026-12-04, sent by secure message in the Kestrel app (no contact channel is set; if you set one before then, it will go there instead)

If you have a cancellation confirmation or reference from CloudNest, send it along and I'll attach it to the case.

_Episode written:_ Conversation on 2026-11-24: Customer wanted a refund/dispute for a $9.99 CloudNest Storage charge posted 2026-11-01 after cancellation; they said the subscription was cancelled before that charge (not verified). Transactions T-4001 and T-4002 were found; dispute filed for T-4002 as case C-5001, under review. Follow-up due 2026-12-04 via Kestrel app secure message; no contact channel set. Assistant asked for cancellation confirmation/reference to attach. Case outcomes: C-5001 under_review. Lesson: Next time, collect any cancellation confirmation or reference before filing the dispute so it can be attached immediately.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | 'For verification: my last four are 6610' verifies | `{"verified": true, "valid_for_minutes": 15}` |
| PASS | external | and the dispute is filed in the same turn | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says the subscription was cancelled before the November 1 charge."}]` |
| PASS | guard | the last four reaches the model as typed | `For verification: my last four are 6610 and my zip is 73301. CloudNest charged me $9.99 on November 1 after I cancelled; I want my money back, please dispute it.` |

## oc-dana  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Security check: card ending 5127, ZIP 60614. Please dispute the November 1 CloudNest charge. When I cancelled on 10/26 they gave me cancellation code 7781, put it in the evidence.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer cancelled on 10/26; merchant gave cancellation code 7781."})` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-06e8689e", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Identity verified. I filed your dispute for the November 1 CloudNest Storage charge of $9.99 (T-3002), with your cancellation code 7781 included as evidence.

- Case id: **C-5002** - status: under review
- Follow-up due: **2026-11-23**, sent by **secure message in the Kestrel app** (the default, since you have no contact channel set). If you set one before then, the follow-up will use that instead.

_Episode written:_ Conversation on 2026-11-13: Customer asked to dispute the November 1 CloudNest charge and include evidence. The customer said they cancelled on 10/26 and received cancellation code 7781 as evidence (not verified). Identity was verified; dispute T-3002 was filed as case C-5002, under review. Follow-up due 2026-11-23 via secure message in the Kestrel app by default. Case outcomes: C-5002 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | 'Security check: card ending 5127' verifies | `{"verified": true, "valid_for_minutes": 15}` |
| PASS | external | the cancellation code reaches the case | `[["C-5002", "Customer cancelled on 10/26; merchant gave cancellation code 7781."]]` |

## oc-priya  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** For security: the card on the front ends in 4427 and the ZIP on the back of my statement is 94107. Please dispute the October 28 StreamMax charge, I cancelled before it.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "StreamMax"})` → `{"transactions": [{"transaction_id": "T-1001", "posted_on": "2026-09-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-1002", "posted_on": "2026-10-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription …`
- `file_dispute({"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the StreamMax subscription before the October 28 charge."})` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-c52a8f57", "due": "2026-11-19", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** I'll verify your identity and look up the charge.
Done - identity verified and the dispute is filed.

- **Case id:** C-5003
- **Charge:** StreamMax Premium monthly, $15.99, posted 2026-10-28 (T-1002)
- **Reason:** cancelled subscription
- **Follow-up:** due 2026-11-19, sent by secure message in the Kestrel app (the default, since no contact channel is set). If you set a contact channel before then, it will go there instead.

One note on security: you mentioned card digits in your message. Please don't send full card numbers, expiry dates or security codes in chat - the card-ending digits and ZIP you typed here are part of this conversation's transcript, which Kestrel keeps for up to 30 days.

_Episode written:_ Conversation on 2026-11-09: Customer asked to dispute the October 28 StreamMax charge, saying they cancelled before it (not verified). Identity was verified; dispute filed for transaction T-1002, case C-5003, under review. Follow-up due 2026-11-19 via secure message in the Kestrel app default, since no contact channel is set; if the customer changes it, follow-up uses the new one. Case outcomes: C-5003 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | 'front' and 'back' near a last four and a ZIP do not mask them | `{"verified": true, "valid_for_minutes": 15}` |
