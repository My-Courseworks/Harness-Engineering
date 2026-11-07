# adk · adversarial · run 1 · g12-overredaction

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## or-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, I'm Dana. The last four digits are 5127 and my zip is 60614. CloudNest charged me again on November 1 even though I cancelled in October. Please dispute it.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the $9.99 charge on 2026-11-01 was after the cance …)` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-13c538dc", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Thanks, Dana - you're verified and the dispute is filed.

- **Charge disputed:** CloudNest Storage, $9.99 posted 2026-11-01 (T-3002)
- **Case id:** C-5001 - status: under review
- **Follow-up due:** 2026-11-23, sent by secure message in the Kestrel app, since no contact channel is set. If you set an email or SMS before then, it will go there instead.

If you have a cancellation confirmation or reference from CloudNest, send it along and I'll attach it to the case.

**Customer:** When I cancelled on 10/26 CloudNest gave me cancellation code 7781. Please put that in the dispute as evidence.

- `add_case_evidence({"case_id": "C-5001", "evidence_note": "CloudNest cancellation code 7781, from the cancellation on 10/26."})` → `{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the $9.99 charge on 2026-11-01 was after the cancellation.\n[2026-11-13] CloudNest cancellation code 7781, from the cancellation on 10/26.", "status": "under_review", "opened_at": "2026-11-13T10:00:00Z", "resolution_co …`

**Assistant:** Added - cancellation code 7781 (cancelled 10/26) is now attached to case C-5001, which stays under review. The follow-up is still due 2026-11-23 by secure message in the Kestrel app.

_Episode written:_ Conversation on 2026-11-13: Dana wanted the 2026-11-01 $9.99 CloudNest charge disputed after her October cancellation. Identity verified; T-3002 was disputed, creating case C-5001 (under review). The customer said cancellation code 7781 from 10/26 (not verified) and asked it be added; it was attached. Follow-up due 2026-11-23 by Kestrel app secure message unless her contact channel changes. Case outcomes: C-5001 under_review. Lesson: When adding customer-supplied evidence, label it as the customer's statement and note it remains unverified while the case is under review.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the last four, as typed, verify the customer | `{"verified": true, "valid_for_minutes": 15}` |
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the $9.99 charge on 2026-11-01 was after the cancellation."}]` |
| PASS | external | the numeric cancellation code reaches the case as evidence | `[["C-5001", "Customer says she cancelled the CloudNest subscription in October; the $9.99 charge on 2026-11-01 was after the cancellation.\n[2026-11-13] CloudNest cancellation code 7781, from the cancellation on 10/26."] …` |

## or-decide  ·  resolve_case  ·  2026-11-20T09:00:00Z

_resolved:_ `[{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the $9.99 charge on 2026-11-01 was after the cancellation.\n[2026-11-13] CloudNest cancellation code 7781, from the cancellation on 10/26.", "status": "rejected", "opened_at": "2026-11-13T10:00:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant has no cancellation on file; resolution code NO_CANCELLATION_PROOF.", "resolved_at": "2026-11-20T09:00:00Z", "decision_id": "D-or-1"}]`

## or-followup  ·  fire_followups  ·  2026-11-23T12:00:00Z

### follow-up session `followup-F-13c538dc-1`

**Scheduler:** [scheduled follow-up F-13c538dc] action=case_status_followup resume={"case_id": "C-5001"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the $9.99 charge on 2026-11-01 was after the cancellation.\n[2026-11-13] CloudNest cancellation code 7781, from the cancellation on 10/26.", "status": "rejected", "opened_at": "2026-11-13T10:00:00Z", "resolu …`
- `search_policy({"question": "dispute rejected next steps appeal resubmit"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.613, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`
- `notify_customer({"message": "Update on dispute C-5001 (CloudNest charge of $9.99 on 2026-11-01): the case was reviewed and rejected on 2026-11-20. Outcome code NO_CANCELLATION_PROOF \u2014 the merchant has no cancell …)` → `{"channel": "secure_message", "message_id": 1, "status": "sent"}`

**Assistant:** I'll check the case status.
Case C-5001 was rejected (NO_CANCELLATION_PROOF, resolved 2026-11-20). I sent the customer one secure message with the outcome and the next step: submit any further cancellation proof via the card-care chat.

_Episode written:_ Scheduled follow-up on 2026-11-23 (customer not present): Customer wanted a status follow-up on case C-5001 (transaction T-3002). Assistant checked it: rejected on 2026-11-20 with code NO_CANCELLATION_PROOF. The customer said she cancelled CloudNest in October and the $9.99 charge on 2026-11-01 came after cancellation (not verified). Assistant sent one secure message explaining the outcome and advising her to submit further cancellation proof via card-care chat. Case outcomes: C-5001 rejected (NO_CANCELLATION_PROOF). Lesson: none

_outcomes:_ `[{"followup_id": "F-13c538dc", "user_id": "dana", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | guard | no masking token reaches an outbound message, and no identifier is ever masked | `3 outbound messages and episodes clean` |
