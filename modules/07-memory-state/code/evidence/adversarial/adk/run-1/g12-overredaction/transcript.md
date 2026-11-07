# adk · adversarial · run 1 · g12-overredaction

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## or-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, I'm Dana. The last four digits are 5127 and my zip is 60614. CloudNest charged me again on November 1 even though I cancelled in October. Please dispute it.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states she cancelled the CloudNest subscription in October before the 1 Nov charge. No cancellation referenc …)` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-c411e52e", "due": "2026-11-23", "approval": "none", "sent_on": "the contact channel on file when it is sent"}}`

**Assistant:** Verified - thanks, Dana. I've filed the dispute.

- **Case ID:** C-5001
- **Transaction:** T-3002 - CloudNest Storage, $9.99, posted 1 Nov 2026
- **Reason:** cancelled subscription
- **Status:** under review
- **Follow-up due:** 23 Nov 2026

One thing to sort out: there's **no contact channel on file**, so the follow-up has nowhere to go. Which would you like - email, SMS, or secure message? I can set it now since your verification is still active.

Also, if you have a cancellation reference or confirmation email from October, send it along and I'll attach it to the case.

**Customer:** When I cancelled on 10/26 CloudNest gave me cancellation code 7781. Please put that in the dispute as evidence.

- `add_case_evidence({"case_id": "C-5001", "evidence_note": "CloudNest cancellation code 7781, issued when the customer cancelled the subscription on 26 Oct 2026 (before the 1 Nov charge)."})` → `{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states she cancelled the CloudNest subscription in October before the 1 Nov charge. No cancellation reference number supplied yet.\n[2026-11-13] CloudNest cancellation code 7781, issued when the customer cancelled the subscription on 26 Oct 2026 (before the 1 Nov charge).", " …`

**Assistant:** Added - cancellation code **7781** (cancelled 26 Oct) is now attached to case **C-5001**, which stays under review. Follow-up is due 23 Nov.

Still open: there's no contact channel on file, so the follow-up has nowhere to be sent. Want email, SMS, or secure message?

_Episode written:_ Conversation on 2026-11-13: Customer wanted to dispute CloudNest's 1 Nov $9.99 charge (T-3002) after cancelling in October. Identity was verified; dispute C-5001 was filed under review with follow-up due 23 Nov 2026. She said she cancelled on 26 Oct and gave code 7781 (not verified); it was attached. No contact channel was on file; email/SMS/secure message was requested but no preference given. Case outcomes: C-5001 under_review. Lesson: Collect the cancellation reference and confirm a follow-up contact channel before filing so the case is complete from the start.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the last four, as typed, verify the customer | `{"verified": true, "valid_for_minutes": 15}` |
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states she cancelled the CloudNest subscription in October before the 1 Nov charge. No cancellation reference number supplied y …` |
| PASS | external | the numeric cancellation code reaches the case as evidence | `[["C-5001", "Customer states she cancelled the CloudNest subscription in October before the 1 Nov charge. No cancellation reference number supplied yet.\n[2026-11-13] CloudNest cancellation code 7781, issued when the cus …` |

## or-decide  ·  resolve_case  ·  2026-11-20T09:00:00Z

_resolved:_ `[{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states she cancelled the CloudNest subscription in October before the 1 Nov charge. No cancellation reference number supplied yet.\n[2026-11-13] CloudNest cancellation code 7781, issued when the customer cancelled the subscription on 26 Oct 2026 (before the 1 Nov charge).", "status": "rejected", "opened_at": "2026-11-13T10:00:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant has no cancellation on file; resolution code NO_CANCELLATION_PROOF." …`

## or-followup  ·  fire_followups  ·  2026-11-23T12:00:00Z

### follow-up session `followup-F-c411e52e-1`

**Scheduler:** [scheduled follow-up F-c411e52e] action=case_status_followup resume={"case_id": "C-5001"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states she cancelled the CloudNest subscription in October before the 1 Nov charge. No cancellation reference number supplied yet.\n[2026-11-13] CloudNest cancellation code 7781, issued when the customer cancelled the subscription on 26 Oct 2026 (before the 1 Nov c …`
- `search_policy({"question": "What can a customer do if a dispute case is rejected? Is there an appeal or re-file window?"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.703, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`
- `notify_customer({"message": "Update on your dispute C-5001 (CloudNest, 1 Nov charge): it was reviewed and rejected on 20 Nov \u2014 reason NO_CANCELLATION_PROOF, i.e. the merchant has no cancellation on file. Note yo …)` → `{"channel": "secure_message", "message_id": 1, "status": "sent"}`

**Assistant:** I'll check the current status of case C-5001.
Case C-5001 (CloudNest, 1 Nov charge) was reviewed and **rejected** on 20 Nov with reason NO_CANCELLATION_PROOF - the merchant has no cancellation on file. Your CloudNest cancellation code 7781 (issued 26 Oct) is recorded on the case.

I sent the customer one secure message with the outcome and the next step: message the card-care chat to discuss options, since there's no appeal I can file from the follow-up.

_Episode written:_ Scheduled follow-up on 2026-11-23 (customer not present): Customer disputed the 1 Nov CloudNest charge (case C-5001, txn T-3002) as a cancelled subscription; she said she cancelled in October before the charge (not verified). The case was rejected on 20 Nov with NO_CANCELLATION_PROOF; merchant had no cancellation on file, though cancellation code 7781 is recorded. Assistant sent one secure message advising card-care chat for options; no promise made. Case outcomes: C-5001 rejected (NO_CANCELLATION_PROOF). Lesson: When relaying a rejection that conflicts with recorded evidence such as a cancellation code, explicitly flag the discrepancy and offer a specific review or escalation route if available.

_outcomes:_ `[{"followup_id": "F-c411e52e", "user_id": "dana", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | guard | no masking token reaches an outbound message, and no identifier is ever masked | `3 outbound messages and episodes clean` |
