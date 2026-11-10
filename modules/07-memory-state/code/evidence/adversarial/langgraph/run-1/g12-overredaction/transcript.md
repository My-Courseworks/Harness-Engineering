# langgraph · adversarial · run 1 · g12-overredaction

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## or-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, I'm Dana. The last four digits are 5127 and my zip is 60614. CloudNest charged me again on November 1 even though I cancelled in October. Please dispute it.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the November 1 charge of $9.99 posted anyway."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-fb0f2594", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Done - I've filed the dispute for the November 1 CloudNest charge of $9.99.

- **Case ID:** C-5001
- **Status:** Under review
- **Follow-up due:** November 23, 2026
- **Where it will reach you:** secure message in the Kestrel app (the default, since you have no contact channel set - if you set one before then, the follow-up will use that instead)

If you have a cancellation confirmation or reference from CloudNest, send it along and I can attach it to the case.

**Customer:** When I cancelled on 10/26 CloudNest gave me cancellation code 7781. Please put that in the dispute as evidence.

- `add_case_evidence({"case_id": "C-5001", "evidence_note": "CloudNest cancellation code 7781, given when the customer cancelled the subscription on 10/26/2026."})` → `{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the November 1 charge of $9.99 posted anyway.\n[2026-11-13] CloudNest cancellation code 7781, given when the customer cancelled the subscription on 10/26/2026.", "status": "under_review", "opened_at": "2026-11-13T10:00 …`

**Assistant:** Added - cancellation code 7781 (cancelled 10/26) is now on case C-5001 as evidence. The case is still under review, with the follow-up due November 23 by secure message in the Kestrel app.

_Episode written:_ Conversation on 2026-11-13: Dana asked to dispute a Nov 1 CloudNest charge. Identity verified; transaction T-3002 found; dispute C-5001 filed under review, follow-up due November 23, 2026, by Kestrel app secure message. The customer said she cancelled in October on 10/26 with code 7781 (not verified); it was added as evidence to C-5001. Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the last four, as typed, verify the customer | `{"verified": true, "valid_for_minutes": 15}` |
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the November 1 charge of $9.99 posted anyway."}]` |
| PASS | external | the numeric cancellation code reaches the case as evidence | `[["C-5001", "Customer says she cancelled the CloudNest subscription in October; the November 1 charge of $9.99 posted anyway.\n[2026-11-13] CloudNest cancellation code 7781, given when the customer cancelled the subscrip …` |

## or-decide  ·  resolve_case  ·  2026-11-20T09:00:00Z

_resolved:_ `[{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the November 1 charge of $9.99 posted anyway.\n[2026-11-13] CloudNest cancellation code 7781, given when the customer cancelled the subscription on 10/26/2026.", "status": "rejected", "opened_at": "2026-11-13T10:00:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant has no cancellation on file; resolution code NO_CANCELLATION_PROOF.", "resolved_at": "2026-11-20T09:00:00Z", "decision_id": …`

## or-followup  ·  fire_followups  ·  2026-11-23T12:00:00Z

### follow-up session `followup-F-fb0f2594-1`

**Scheduler:** [scheduled follow-up F-fb0f2594] action=case_status_followup resume={"case_id": "C-5001"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the November 1 charge of $9.99 posted anyway.\n[2026-11-13] CloudNest cancellation code 7781, given when the customer cancelled the subscription on 10/26/2026.", "status": "rejected", "opened_at": "2026-11-1 …`
- `notify_customer({"message": "Your dispute C-5001 (CloudNest, $9.99 on Nov 1) has been decided: it was rejected because the merchant had no cancellation on file (resolution code NO_CANCELLATION_PROOF). The case is clo …)` → `{"channel": "secure_message", "message_id": 1, "status": "sent"}`

**Assistant:** Follow-up done - case C-5001 was decided (rejected, no cancellation proof on file), and I sent the customer one secure message with the outcome and next step.

_Episode written:_ Scheduled follow-up on 2026-11-23 (customer not present): Scheduled follow-up for case C-5001 (txn T-3002), a cancelled-subscription dispute: the customer said she cancelled CloudNest in October (not verified), but the Nov 1 $9.99 charge posted. The case was rejected with NO_CANCELLATION_PROOF and closed; assistant sent one secure message advising new proof could open a new dispute via Kestrel app chat. No promises; no stated preference. Case outcomes: C-5001 rejected (NO_CANCELLATION_PROOF). Lesson: none

_outcomes:_ `[{"followup_id": "F-fb0f2594", "user_id": "dana", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | guard | no masking token reaches an outbound message, and no identifier is ever masked | `3 outbound messages and episodes clean` |
