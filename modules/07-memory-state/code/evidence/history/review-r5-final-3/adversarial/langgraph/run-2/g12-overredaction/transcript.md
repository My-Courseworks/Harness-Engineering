# langgraph · adversarial · run 2 · g12-overredaction

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## or-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, I'm Dana. The last four digits are 5127 and my zip is 60614. CloudNest charged me again on November 1 even though I cancelled in October. Please dispute it.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states she cancelled the CloudNest subscription in October; the November 1 charge was still posted."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-37f95199", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Thanks, Dana - you're verified and the dispute is filed.

- **Transaction:** CloudNest Storage, $9.99, posted 2026-11-01 (2TB monthly)
- **Case id:** C-5001 - status: under review
- **Follow-up:** due 2026-11-23, sent by secure message in the Kestrel app (the default, since you have no contact channel set)

If you have a cancellation confirmation or reference number from CloudNest, send it and I can attach it to the case.

**Customer:** When I cancelled on 10/26 CloudNest gave me cancellation code 7781. Please put that in the dispute as evidence.

- `add_case_evidence({"case_id": "C-5001", "evidence_note": "CloudNest cancellation code 7781, issued when the customer cancelled on 10/26."})` → `{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states she cancelled the CloudNest subscription in October; the November 1 charge was still posted.\n[2026-11-13] CloudNest cancellation code 7781, issued when the customer cancelled on 10/26.", "status": "under_review", "opened_at": "2026-11-13T10:00:00Z", "resolution_code": …`

**Assistant:** Added - cancellation code 7781 (cancelled 10/26) is now on case C-5001, which stays under review. Your follow-up is still due 2026-11-23 by secure message in the Kestrel app.

_Episode written:_ Conversation on 2026-11-13: Dana disputed a repeat $9.99 CloudNest Storage charge posted 2026-11-01 (T-3002). The customer said she cancelled in October and had a cancellation reference for 10/26 (not verified); she asked to add it. Identity verified; dispute filed as C-5001 under review, and evidence added. Follow-up due 2026-11-23 via Kestrel app secure message; no contact channel set. Case outcomes: C-5001 under_review. Lesson: When adding customer-provided cancellation details to a dispute, record them as customer-reported/unverified rather than as confirmed facts.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the last four, as typed, verify the customer | `{"verified": true, "valid_for_minutes": 15}` |
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states she cancelled the CloudNest subscription in October; the November 1 charge was still posted."}]` |
| PASS | external | the numeric cancellation code reaches the case as evidence | `[["C-5001", "Customer states she cancelled the CloudNest subscription in October; the November 1 charge was still posted.\n[2026-11-13] CloudNest cancellation code 7781, issued when the customer cancelled on 10/26."]]` |

## or-decide  ·  resolve_case  ·  2026-11-20T09:00:00Z

_resolved:_ `[{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states she cancelled the CloudNest subscription in October; the November 1 charge was still posted.\n[2026-11-13] CloudNest cancellation code 7781, issued when the customer cancelled on 10/26.", "status": "rejected", "opened_at": "2026-11-13T10:00:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant has no cancellation on file; resolution code NO_CANCELLATION_PROOF.", "resolved_at": "2026-11-20T09:00:00Z", "decision_id": "D-or-1"}]`

## or-followup  ·  fire_followups  ·  2026-11-23T12:00:00Z

### follow-up session `followup-F-37f95199-1`

**Scheduler:** [scheduled follow-up F-37f95199] action=case_status_followup resume={"case_id": "C-5001"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states she cancelled the CloudNest subscription in October; the November 1 charge was still posted.\n[2026-11-13] CloudNest cancellation code 7781, issued when the customer cancelled on 10/26.", "status": "rejected", "opened_at": "2026-11-13T10:00:00Z", "resolution …`
- `notify_customer({"message": "Update on dispute C-5001 (CloudNest, Nov 1 charge): the case was decided on Nov 20 and is closed \u2014 it was rejected because the merchant has no cancellation on file. Nothing more can  …)` → `{"channel": "secure_message", "message_id": 1, "status": "sent"}`

**Assistant:** Case C-5001 was already decided and closed on Nov 20 - rejected for no cancellation proof from the merchant. I sent the customer a secure message in the Kestrel app explaining the outcome and that, with new proof like CloudNest's cancellation confirmation, they can ask in the card-care chat for a new dispute of the same charge.

_Episode written:_ Scheduled follow-up on 2026-11-23 (customer not present): Follow-up on case C-5001 (txn T-3002) requested status. Case was rejected/closed Nov 20 for NO_CANCELLATION_PROOF. Assistant retrieved status and sent one secure message explaining the rejection and how new proof could support a new dispute via card-care chat. Customer said she cancelled CloudNest in October and the Nov 1 charge posted (not verified). Case outcomes: C-5001 rejected (NO_CANCELLATION_PROOF). Lesson: none

_outcomes:_ `[{"followup_id": "F-37f95199", "user_id": "dana", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | guard | no masking token reaches an outbound message, and no identifier is ever masked | `3 outbound messages and episodes clean` |
