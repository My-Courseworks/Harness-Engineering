# adk · adversarial · run 1 · g12-overredaction

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## or-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, I'm Dana. The last four digits are 5127 and my zip is 60614. CloudNest charged me again on November 1 even though I cancelled in October. Please dispute it.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription"})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-501f9095", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Done, Dana - identity verified and the dispute is filed.

- Charge disputed: CloudNest Storage, $9.99, posted 2026-11-01 (T-3002)
- Reason: subscription cancelled in October
- Case id: **C-5001**, status: under review

Your follow-up is due **2026-11-23**. It will reach you by **secure message in the Kestrel app**, since no contact channel is set on your account - if you set an email or SMS before then, it'll go there instead. Disputes are currently reviewed in about 10 days.

If you have a cancellation confirmation or reference from CloudNest, send it over and I'll attach it to the case.

**Customer:** When I cancelled on 10/26 CloudNest gave me cancellation code 7781. Please put that in the dispute as evidence.

- `add_case_evidence({"case_id": "C-5001", "evidence_note": "Customer cancelled on 10/26; CloudNest gave cancellation code 7781."})` → `{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "[2026-11-13] Customer cancelled on 10/26; CloudNest gave cancellation code 7781.", "status": "under_review", "opened_at": "2026-11-13T10:00:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null, "decision_id": null}`

**Assistant:** Added to case C-5001: your cancellation date (10/26) and CloudNest cancellation code 7781. The case stays under review, with the status follow-up due 2026-11-23 by secure message in the Kestrel app.

_Episode written:_ Conversation on 2026-11-13: Dana wanted the 2026-11-01 CloudNest Storage $9.99 charge disputed after she said she cancelled in October. Identity was verified, transaction T-3002 was found, and dispute C-5001 was filed under review. The customer said she cancelled on 10/26 with CloudNest code 7781 (not verified); it was added as evidence. Follow-up due 2026-11-23 via Kestrel app secure message. Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the last four, as typed, verify the customer | `{"verified": true, "valid_for_minutes": 15}` |
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription"}]` |
| PASS | external | the numeric cancellation code reaches the case as evidence | `[["C-5001", "[2026-11-13] Customer cancelled on 10/26; CloudNest gave cancellation code 7781."]]` |

## or-decide  ·  resolve_case  ·  2026-11-20T09:00:00Z

_resolved:_ `[{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "[2026-11-13] Customer cancelled on 10/26; CloudNest gave cancellation code 7781.", "status": "rejected", "opened_at": "2026-11-13T10:00:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant has no cancellation on file; resolution code NO_CANCELLATION_PROOF.", "resolved_at": "2026-11-20T09:00:00Z", "decision_id": "D-or-1"}]`

## or-followup  ·  fire_followups  ·  2026-11-23T12:00:00Z

### follow-up session `followup-F-501f9095-1`

**Scheduler:** [scheduled follow-up F-501f9095] action=case_status_followup resume={"case_id": "C-5001"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "[2026-11-13] Customer cancelled on 10/26; CloudNest gave cancellation code 7781.", "status": "rejected", "opened_at": "2026-11-13T10:00:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant has no cancellation on file; resolution code NO_CANCELLATIO …`
- `notify_customer({"message": "Status update on dispute C-5001 (CloudNest charge): the case was decided on 20 Nov 2026 and rejected \u2014 the merchant has no cancellation on file (resolution code NO_CANCELLATION_PROOF …)` → `{"channel": "secure_message", "message_id": 1, "status": "sent"}`

**Assistant:** I'll check the case status.
Sent the customer one secure message: dispute C-5001 was decided on 20 Nov 2026 and rejected (NO_CANCELLATION_PROOF), the case is closed and takes no more evidence, and with new proof - e.g. CloudNest's cancellation confirmation - they can message the card-care chat to file a new dispute of the same charge.

_Episode written:_ Scheduled follow-up on 2026-11-23 (customer not present): Customer sought status of dispute C-5001 (txn T-3002, CloudNest charge). The customer said the subscription was cancelled on 10/26 and CloudNest gave a cancellation code (not verified). Case was rejected on 20 Nov 2026 under NO_CANCELLATION_PROOF and is closed; no new evidence can be added. Assistant sent one secure message advising that new proof may support a new dispute. Case outcomes: C-5001 rejected (NO_CANCELLATION_PROOF). Lesson: none

_outcomes:_ `[{"followup_id": "F-501f9095", "user_id": "dana", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | guard | no masking token reaches an outbound message, and no identifier is ever masked | `3 outbound messages and episodes clean` |
