# adk · adversarial · run 2 · g12-overredaction

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## or-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, I'm Dana. The last four digits are 5127 and my zip is 60614. CloudNest charged me again on November 1 even though I cancelled in October. Please dispute it.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the $9.99 charge posted 2026-11-01 after the cance …)` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-db0fa93c", "due": "2026-11-23", "approval": "none", "sent_on": "the contact channel on file when it is sent"}}`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-db0fa93c", "action": "case_status_followup", "due": "2026-11-23T10:00:00Z", "status": "pending", "sent_on": "the contact channel on file when it is sent (currently secure_message)", "case_id": "C-5001"}]}`

**Assistant:** Verified - thanks, Dana. Here's what I did:

- **Disputed:** CloudNest Storage, $9.99, posted 2026-11-01 (the earlier 2026-10-01 charge is untouched)
- **Reason:** cancelled subscription
- **Case ID:** C-5001 (status: under review)
- **Follow-up:** scheduled for 2026-11-23, sent to the contact channel on file - currently secure message

If you have a cancellation confirmation or reference number from October, message it here and I'll attach it to case C-5001 as evidence.

Is there anything else?

**Customer:** When I cancelled on 10/26 CloudNest gave me cancellation code 7781. Please put that in the dispute as evidence.

- `add_case_evidence({"case_id": "C-5001", "evidence_note": "CloudNest cancellation code 7781, issued when the customer cancelled the subscription on 2026-10-26."})` → `{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the $9.99 charge posted 2026-11-01 after the cancellation.\n[2026-11-13] CloudNest cancellation code 7781, issued when the customer cancelled the subscription on 2026-10-26.", "status": "under_review", "opened_at": "20 …`

**Assistant:** Added - cancellation code 7781 (cancelled 2026-10-26) is now attached to case C-5001 as evidence. The case remains under review, with the follow-up still set for 2026-11-23 via secure message.

_Episode written:_ Conversation on 2026-11-13: Dana asked to dispute a $9.99 CloudNest Storage charge on 2026-11-01 after cancelling in October. Identity was verified; transaction T-3002 was disputed as cancelled_subscription under case C-5001 (under review). The customer said she cancelled on 2026-10-26 and gave a cancellation code (not verified); it was added as evidence. Follow-up F-db0fa93c is due 2026-11-23 via secure message. Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the last four, as typed, verify the customer | `{"verified": true, "valid_for_minutes": 15}` |
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the $9.99 charge posted 2026-11-01 after the cancellation."}]` |
| PASS | external | the numeric cancellation code reaches the case as evidence | `[["C-5001", "Customer says she cancelled the CloudNest subscription in October; the $9.99 charge posted 2026-11-01 after the cancellation.\n[2026-11-13] CloudNest cancellation code 7781, issued when the customer cancelle …` |

## or-decide  ·  resolve_case  ·  2026-11-20T09:00:00Z

_resolved:_ `[{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the $9.99 charge posted 2026-11-01 after the cancellation.\n[2026-11-13] CloudNest cancellation code 7781, issued when the customer cancelled the subscription on 2026-10-26.", "status": "rejected", "opened_at": "2026-11-13T10:00:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant has no cancellation on file; resolution code NO_CANCELLATION_PROOF.", "resolved_at": "2026-11-20T09:00:00Z",  …`

## or-followup  ·  fire_followups  ·  2026-11-23T12:00:00Z

### follow-up session `followup-F-db0fa93c-1`

**Scheduler:** [scheduled follow-up F-db0fa93c] action=case_status_followup resume={"case_id": "C-5001"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the $9.99 charge posted 2026-11-01 after the cancellation.\n[2026-11-13] CloudNest cancellation code 7781, issued when the customer cancelled the subscription on 2026-10-26.", "status": "rejected", "opened_a …`
- `search_policy({"question": "What happens if a dispute is rejected for NO_CANCELLATION_PROOF? Can it be reopened or appealed, and what evidence is needed?"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.754, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`
- `notify_customer({"message": "Update on dispute C-5001 (CloudNest, $9.99 posted 2026-11-01): the case was closed on 2026-11-20 as rejected \u2014 reason given: the merchant had no cancellation on file (code NO_CANCELL …)` → `{"channel": "secure_message", "message_id": 1, "status": "sent"}`

**Assistant:** Done - case C-5001 was found to be rejected (closed 2026-11-20, reason: no cancellation proof from the merchant), and I sent the customer one secure message with the outcome and the next step (send additional cancellation proof via the card-care chat).

_Episode written:_ Scheduled follow-up on 2026-11-23 (customer not present): Customer requested follow-up on case C-5001 (txn T-3002) about a CloudNest subscription charge. The customer said she cancelled the subscription in October and that $9.99 posted 2026-11-01 after cancellation (not verified). The case was rejected and closed 2026-11-20 for NO_CANCELLATION_PROOF. The assistant sent one secure message with the outcome and advised sending additional cancellation proof via card-care chat. Case outcomes: C-5001 rejected (NO_CANCELLATION_PROOF). Lesson: none

_outcomes:_ `[{"followup_id": "F-db0fa93c", "user_id": "dana", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | guard | no masking token reaches an outbound message, and no identifier is ever masked | `3 outbound messages and episodes clean` |
