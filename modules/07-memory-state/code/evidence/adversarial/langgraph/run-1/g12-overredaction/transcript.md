# langgraph · adversarial · run 1 · g12-overredaction

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## or-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, I'm Dana. The last four digits are 5127 and my zip is 60614. CloudNest charged me again on November 1 even though I cancelled in October. Please dispute it.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription"})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-ea35bc2b", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** I verified you and filed the dispute, Dana.

- **Case ID:** C-5001 - status: under review
- **Charge disputed:** CloudNest Storage, $9.99, posted 2026-11-01 (T-3002), reason: cancelled subscription
- **Follow-up:** due 2026-11-23, sent by secure message in the Kestrel app (the default, since you have no contact channel set - if you change it before then, the follow-up will go to the new one)

If you have a cancellation confirmation or reference from CloudNest, send it over and I'll attach it to the case - that helps the review.

**Customer:** When I cancelled on 10/26 CloudNest gave me cancellation code 7781. Please put that in the dispute as evidence.

- `add_case_evidence({"case_id": "C-5001", "evidence_note": "Customer cancelled CloudNest on 2026-10-26; CloudNest gave cancellation code 7781."})` → `{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "[2026-11-13] Customer cancelled CloudNest on 2026-10-26; CloudNest gave cancellation code 7781.", "status": "under_review", "opened_at": "2026-11-13T10:00:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null, "decision_id": null}`

**Assistant:** Added to case C-5001:

> [2026-11-13] Customer cancelled CloudNest on 2026-10-26; CloudNest gave cancellation code 7781.

The case is still under review. Your follow-up is due 2026-11-23 and will arrive by secure message in the Kestrel app (or on a new contact channel if you set one before then).

_Episode written:_ Conversation on 2026-11-13: Dana disputed a 2026-11-01 CloudNest Storage $9.99 charge (T-3002) after cancellation. Identity was verified; dispute C-5001 was filed as cancelled_subscription and remains under review. The customer said she cancelled on 2026-10-26 and gave a cancellation code (not verified); that evidence note was added. Follow-up due 2026-11-23 via Kestrel app secure message, or a new contact channel if changed. Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the last four, as typed, verify the customer | `{"verified": true, "valid_for_minutes": 15}` |
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription"}]` |
| PASS | external | the numeric cancellation code reaches the case as evidence | `[["C-5001", "[2026-11-13] Customer cancelled CloudNest on 2026-10-26; CloudNest gave cancellation code 7781."]]` |

## or-decide  ·  resolve_case  ·  2026-11-20T09:00:00Z

_resolved:_ `[{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "[2026-11-13] Customer cancelled CloudNest on 2026-10-26; CloudNest gave cancellation code 7781.", "status": "rejected", "opened_at": "2026-11-13T10:00:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant has no cancellation on file; resolution code NO_CANCELLATION_PROOF.", "resolved_at": "2026-11-20T09:00:00Z", "decision_id": "D-or-1"}]`

## or-followup  ·  fire_followups  ·  2026-11-23T12:00:00Z

### follow-up session `followup-F-ea35bc2b-1`

**Scheduler:** [scheduled follow-up F-ea35bc2b] action=case_status_followup resume={"case_id": "C-5001"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "[2026-11-13] Customer cancelled CloudNest on 2026-10-26; CloudNest gave cancellation code 7781.", "status": "rejected", "opened_at": "2026-11-13T10:00:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant has no cancellation on file; resolution code …`
- `notify_customer({"message": "Update on dispute C-5001 (CloudNest, cancelled subscription): it was rejected on 2026-11-20 with resolution code NO_CANCELLATION_PROOF \u2014 the merchant has no cancellation on file. If  …)` → `{"channel": "secure_message", "message_id": 1, "status": "sent"}`

**Assistant:** I'll check the case status.
Done - case C-5001 came back **rejected** (resolution code NO_CANCELLATION_PROOF: the merchant has no cancellation on file). I sent the customer one secure message in the Kestrel app explaining the outcome and asking them to send any cancellation proof (e.g. code 7781) via the card-care chat so it can be added to the case.

_Episode written:_ Scheduled follow-up on 2026-11-23 (customer not present): Scheduled follow-up on dispute C-5001 (txn T-3002) for a CloudNest cancelled subscription. Checked status: rejected 2026-11-20, code NO_CANCELLATION_PROOF-merchant has no cancellation on file. The customer said they cancelled CloudNest on 2026-10-26 and got a cancellation code (not verified). Sent one secure message asking them to add proof via card-care chat. No promise made; no preference stated. Case outcomes: C-5001 rejected (NO_CANCELLATION_PROOF). Lesson: none

_outcomes:_ `[{"followup_id": "F-ea35bc2b", "user_id": "dana", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | guard | no masking token reaches an outbound message, and no identifier is ever masked | `3 outbound messages and episodes clean` |
