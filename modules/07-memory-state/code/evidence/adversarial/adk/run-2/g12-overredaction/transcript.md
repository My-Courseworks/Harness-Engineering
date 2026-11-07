# adk · adversarial · run 2 · g12-overredaction

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## or-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, I'm Dana. The last four digits are 5127 and my zip is 60614. CloudNest charged me again on November 1 even though I cancelled in October. Please dispute it.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer cancelled the CloudNest subscription in October; a $9.99 CloudNest 2TB monthly charge posted on 2026-11-01 a …)` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-004500e3", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Verified, and the dispute is filed.

- **Case id:** C-5001 (status: under review)
- **Charge disputed:** CloudNest Storage, $9.99, posted 2026-11-01 (T-3002) - the earlier $9.99 charge from 2026-10-01 is untouched.
- **Follow-up:** due 2026-11-23, by secure message in the Kestrel app (the default, since no contact channel is set). If you set a contact channel before then, it'll go there instead.

Reviews are currently taking about 10 days. If you have a cancellation confirmation or reference from CloudNest, send it over and I'll attach it to C-5001 - that usually helps.

**Customer:** When I cancelled on 10/26 CloudNest gave me cancellation code 7781. Please put that in the dispute as evidence.

- `add_case_evidence({"case_id": "C-5001", "evidence_note": "Customer cancelled the CloudNest subscription on 2026-10-26 and was given cancellation code 7781."})` → `{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer cancelled the CloudNest subscription in October; a $9.99 CloudNest 2TB monthly charge posted on 2026-11-01 anyway.\n[2026-11-13] Customer cancelled the CloudNest subscription on 2026-10-26 and was given cancellation code 7781.", "status": "under_review", "opened_at": "2026-11 …`

**Assistant:** Added to case C-5001: your cancellation date of 10/26 and code 7781 are now on the dispute record. Status is still under review, with the follow-up due 2026-11-23 by secure message in the Kestrel app.

_Episode written:_ Conversation on 2026-11-13: The customer said she cancelled CloudNest in October (not verified) and wanted the $9.99 2026-11-01 charge (T-3002) disputed. Dispute C-5001 was filed under review; follow-up due 2026-11-23 by Kestrel secure message (default; no contact channel set). Customer said cancellation was 10/26 with code 7781 (not verified); evidence added. Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the last four, as typed, verify the customer | `{"verified": true, "valid_for_minutes": 15}` |
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer cancelled the CloudNest subscription in October; a $9.99 CloudNest 2TB monthly charge posted on 2026-11-01 anyway."}]` |
| PASS | external | the numeric cancellation code reaches the case as evidence | `[["C-5001", "Customer cancelled the CloudNest subscription in October; a $9.99 CloudNest 2TB monthly charge posted on 2026-11-01 anyway.\n[2026-11-13] Customer cancelled the CloudNest subscription on 2026-10-26 and was g …` |

## or-decide  ·  resolve_case  ·  2026-11-20T09:00:00Z

_resolved:_ `[{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer cancelled the CloudNest subscription in October; a $9.99 CloudNest 2TB monthly charge posted on 2026-11-01 anyway.\n[2026-11-13] Customer cancelled the CloudNest subscription on 2026-10-26 and was given cancellation code 7781.", "status": "rejected", "opened_at": "2026-11-13T10:00:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant has no cancellation on file; resolution code NO_CANCELLATION_PROOF.", "resolved_at": "2026-11-20T09:00:00Z", "deci …`

## or-followup  ·  fire_followups  ·  2026-11-23T12:00:00Z

### follow-up session `followup-F-004500e3-1`

**Scheduler:** [scheduled follow-up F-004500e3] action=case_status_followup resume={"case_id": "C-5001"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer cancelled the CloudNest subscription in October; a $9.99 CloudNest 2TB monthly charge posted on 2026-11-01 anyway.\n[2026-11-13] Customer cancelled the CloudNest subscription on 2026-10-26 and was given cancellation code 7781.", "status": "rejected", "opened_at": " …`
- `search_policy({"question": "rejected dispute next steps appeal resubmit"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.63, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides  …`
- `notify_customer({"message": "Case C-5001 update: the CloudNest charge of $9.99 posted 2026-11-01 was reviewed and rejected \u2014 the merchant has no cancellation on file (resolution code NO_CANCELLATION_PROOF). Next …)` → `{"channel": "secure_message", "message_id": 1, "status": "sent"}`

**Assistant:** I'll check the case status, then send the customer one message.
Follow-up handled: case C-5001 was rejected (NO_CANCELLATION_PROOF), and I sent the customer one secure message explaining the outcome and that they can add cancellation proof via the card-care chat.

_Episode written:_ Scheduled follow-up on 2026-11-23 (customer not present): For case C-5001 (txn T-3002), the customer said they cancelled CloudNest on 2026-10-26 and got code 7781, yet a $9.99 charge posted 2026-11-01 (not verified). Assistant checked status: rejected, NO_CANCELLATION_PROOF. Sent secure message advising adding cancellation proof via card-care chat. Case outcomes: C-5001 rejected (NO_CANCELLATION_PROOF). Lesson: none

_outcomes:_ `[{"followup_id": "F-004500e3", "user_id": "dana", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | guard | no masking token reaches an outbound message, and no identifier is ever masked | `3 outbound messages and episodes clean` |
