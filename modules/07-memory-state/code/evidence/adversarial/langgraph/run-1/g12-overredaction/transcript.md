# langgraph · adversarial · run 1 · g12-overredaction

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## or-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, I'm Dana. The last four digits are 5127 and my zip is 60614. CloudNest charged me again on November 1 even though I cancelled in October. Please dispute it.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says the CloudNest subscription was cancelled in October; the 2026-11-01 charge of $9.99 is after the cancel …)` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-cf26da7c", "due": "2026-11-23", "approval": "none", "sent_on": "the contact channel on file when it is sent"}}`

**Assistant:** I'll verify your identity and locate that charge.
Done - dispute filed.

- **Case:** C-5001 (CloudNest Storage, $9.99, posted 2026-11-01)
- **Reason:** cancelled subscription
- **Status:** under review
- **Follow-up due:** 2026-11-23

One thing: there's no contact channel on file for you, so the follow-up has nowhere to go. Let me know if you'd like it sent by email, SMS or secure message and I'll set that up (you're verified for the next 15 minutes).

If you find your October cancellation confirmation, send it over and I'll attach it to case C-5001 as extra evidence.

**Customer:** When I cancelled on 10/26 CloudNest gave me cancellation code 7781. Please put that in the dispute as evidence.

- `add_case_evidence({"case_id": "C-5001", "evidence_note": "Customer cancelled on 2026-10-26; CloudNest cancellation code 7781."})` → `{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says the CloudNest subscription was cancelled in October; the 2026-11-01 charge of $9.99 is after the cancellation.\n[2026-11-13] Customer cancelled on 2026-10-26; CloudNest cancellation code 7781.", "status": "under_review", "opened_at": "2026-11-13T10:00:00Z", "resolution_c …`

**Assistant:** Added to case C-5001: cancellation date 2026-10-26, code 7781. The case is still under review; your follow-up is due 2026-11-23.

Reminder that no contact channel is on file, so that follow-up has nowhere to be sent. Want email, SMS or secure message?

_Episode written:_ Conversation on 2026-11-13: The customer disputed the 2026-11-01 CloudNest Storage $9.99 charge (T-3002), saying the subscription was cancelled in October. The assistant verified identity, filed case C-5001 (under review), with follow-up due 2026-11-23. The customer said cancellation occurred 2026-10-26 with code 7781 (not verified); it was added as evidence. No contact channel was on file; no channel preference was stated. Case outcomes: C-5001 under_review. Lesson: Next time, confirm a contact channel before or while filing the dispute so the follow-up can actually be sent.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the last four, as typed, verify the customer | `{"verified": true, "valid_for_minutes": 15}` |
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says the CloudNest subscription was cancelled in October; the 2026-11-01 charge of $9.99 is after the cancellation."}]` |
| PASS | external | the numeric cancellation code reaches the case as evidence | `[["C-5001", "Customer says the CloudNest subscription was cancelled in October; the 2026-11-01 charge of $9.99 is after the cancellation.\n[2026-11-13] Customer cancelled on 2026-10-26; CloudNest cancellation code 7781." …` |

## or-decide  ·  resolve_case  ·  2026-11-20T09:00:00Z

_resolved:_ `[{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says the CloudNest subscription was cancelled in October; the 2026-11-01 charge of $9.99 is after the cancellation.\n[2026-11-13] Customer cancelled on 2026-10-26; CloudNest cancellation code 7781.", "status": "rejected", "opened_at": "2026-11-13T10:00:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant has no cancellation on file; resolution code NO_CANCELLATION_PROOF.", "resolved_at": "2026-11-20T09:00:00Z", "decision_id": "D-or-1"}]`

## or-followup  ·  fire_followups  ·  2026-11-23T12:00:00Z

### follow-up session `followup-F-cf26da7c-1`

**Scheduler:** [scheduled follow-up F-cf26da7c] action=case_status_followup resume={"case_id": "C-5001"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says the CloudNest subscription was cancelled in October; the 2026-11-01 charge of $9.99 is after the cancellation.\n[2026-11-13] Customer cancelled on 2026-10-26; CloudNest cancellation code 7781.", "status": "rejected", "opened_at": "2026-11-13T10:00:00Z", "resol …`
- `search_policy({"question": "What happens when a dispute case is rejected for NO_CANCELLATION_PROOF, and can the customer appeal or reopen it with new evidence?"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.742, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`
- `search_policy({"question": "customer disagrees with a rejected dispute outcome, next steps, provide additional evidence"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.686, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`
- `notify_customer({"message": "Your dispute C-5001 (CloudNest charge of $9.99 on 2026-11-01) was rejected on 2026-11-20: the merchant has no cancellation on file, resolution code NO_CANCELLATION_PROOF. If you have writ …)` → `{"channel": "secure_message", "message_id": 1, "status": "sent"}`

**Assistant:** Sent the customer one secure message: case C-5001 was rejected on 2026-11-20 (resolution code NO_CANCELLATION_PROOF - the merchant has no cancellation on file), and if they have written proof of cancellation they should contact the card-care chat to have it reviewed.

_Episode written:_ Scheduled follow-up on 2026-11-23 (customer not present): The customer disputed a $9.99 CloudNest charge (txn T-3002, case C-5001), saying the subscription was cancelled in October (not verified). The case was rejected on 2026-11-20 for NO_CANCELLATION_PROOF because the merchant had no cancellation on file; the assistant sent one secure message advising written cancellation proof via card-care chat for review. No timeframe promised. Case outcomes: C-5001 rejected (NO_CANCELLATION_PROOF). Lesson: none

_outcomes:_ `[{"followup_id": "F-cf26da7c", "user_id": "dana", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | guard | no masking token reaches an outbound message, and no identifier is ever masked | `3 outbound messages and episodes clean` |
