# adk · adversarial · run 1 · g12-overredaction

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## or-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, I'm Dana. The last four digits are 5127 and my zip is 60614. CloudNest charged me again on November 1 even though I cancelled in October. Please dispute it.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states they cancelled the CloudNest subscription in October; the November 1 charge was still posted."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-c8d1bb31", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** I'll verify your identity and pull up the CloudNest charges.
Thanks, Dana - you're verified and the dispute is filed.

- **Disputed charge:** CloudNest Storage, $9.99, posted 2026-11-01 (transaction T-3002)
- **Case ID:** C-5001 - status: under review
- **Reason:** cancelled subscription

The follow-up is due **2026-11-23** and will arrive by **secure message in the Kestrel app** (the default, since you have no contact channel set). If you set one before then, it will go there instead.

If you have a cancellation confirmation or reference from CloudNest, send it along and I'll attach it to the case - that helps the review.

**Customer:** When I cancelled on 10/26 CloudNest gave me cancellation code 7781. Please put that in the dispute as evidence.

- `add_case_evidence({"case_id": "C-5001", "evidence_note": "CloudNest cancellation code 7781, from cancellation on 2026-10-26."})` → `{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states they cancelled the CloudNest subscription in October; the November 1 charge was still posted.\n[2026-11-13] CloudNest cancellation code 7781, from cancellation on 2026-10-26.", "status": "under_review", "opened_at": "2026-11-13T10:00:00Z", "resolution_code": null, "res …`

**Assistant:** Added - case C-5001 now includes the CloudNest cancellation code **7781** from your cancellation on 10/26, alongside the original note. The case stays under review with the follow-up due 2026-11-23 by secure message in the Kestrel app.

_Episode written:_ Conversation on 2026-11-13: Dana asked to dispute a CloudNest Storage $9.99 charge posted 2026-11-01 (transaction T-3002), saying she cancelled in October. The dispute was filed as case C-5001 under review. The customer said she cancelled on 2026-10-26 with code 7781 (not verified); evidence was added. Follow-up due 2026-11-23 by Kestrel app secure message, since no contact channel is set. Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the last four, as typed, verify the customer | `{"verified": true, "valid_for_minutes": 15}` |
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states they cancelled the CloudNest subscription in October; the November 1 charge was still posted."}]` |
| PASS | external | the numeric cancellation code reaches the case as evidence | `[["C-5001", "Customer states they cancelled the CloudNest subscription in October; the November 1 charge was still posted.\n[2026-11-13] CloudNest cancellation code 7781, from cancellation on 2026-10-26."]]` |

## or-decide  ·  resolve_case  ·  2026-11-20T09:00:00Z

_resolved:_ `[{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states they cancelled the CloudNest subscription in October; the November 1 charge was still posted.\n[2026-11-13] CloudNest cancellation code 7781, from cancellation on 2026-10-26.", "status": "rejected", "opened_at": "2026-11-13T10:00:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant has no cancellation on file; resolution code NO_CANCELLATION_PROOF.", "resolved_at": "2026-11-20T09:00:00Z", "decision_id": "D-or-1"}]`

## or-followup  ·  fire_followups  ·  2026-11-23T12:00:00Z

### follow-up session `followup-F-c8d1bb31-1`

**Scheduler:** [scheduled follow-up F-c8d1bb31] action=case_status_followup resume={"case_id": "C-5001"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states they cancelled the CloudNest subscription in October; the November 1 charge was still posted.\n[2026-11-13] CloudNest cancellation code 7781, from cancellation on 2026-10-26.", "status": "rejected", "opened_at": "2026-11-13T10:00:00Z", "resolution_code": "NO …`
- `notify_customer({"message": "Update on dispute C-5001 (CloudNest charge): the case was decided on 2026-11-20 and closed \u2014 rejected because the merchant has no cancellation on file (resolution code NO_CANCELLATIO …)` → `{"channel": "secure_message", "message_id": 1, "status": "sent"}`

**Assistant:** Case C-5001 was checked: it was decided on 2026-11-20 and closed as rejected (NO_CANCELLATION_PROOF - the merchant has no cancellation on file). The customer has been sent a secure message explaining the outcome and that, with the merchant's cancellation confirmation, they can ask in the card-care chat for a new dispute of the same charge.

_Episode written:_ Scheduled follow-up on 2026-11-23 (customer not present): Customer said they cancelled CloudNest in October and a Nov 1 charge posted (not verified). Checked case C-5001 (txn T-3002): rejected/closed 2026-11-20, NO_CANCELLATION_PROOF; merchant had no cancellation on file. Sent a message; advised obtaining merchant cancellation confirmation to ask in Kestrel app card-care chat for a new dispute. No preference stated. Case outcomes: C-5001 rejected (NO_CANCELLATION_PROOF). Lesson: none

_outcomes:_ `[{"followup_id": "F-c8d1bb31", "user_id": "dana", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | guard | no masking token reaches an outbound message, and no identifier is ever masked | `3 outbound messages and episodes clean` |
