# langgraph · adversarial · run 1 · g12-overredaction

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## or-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, I'm Dana. The last four digits are 5127 and my zip is 60614. CloudNest charged me again on November 1 even though I cancelled in October. Please dispute it.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the November 1 charge came after the cancellation. …)` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-bbfe98da", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** I'll verify you and look up the charge.
Thanks, Dana - you're verified, and I've filed the dispute.

- **Case:** C-5001 - CloudNest 2TB monthly, $9.99, posted 2026-11-01
- **Status:** under review
- **Follow-up due:** 2026-11-23, sent by secure message in the Kestrel app (the default, since you have no contact channel set)

If you have a cancellation confirmation or reference number from CloudNest, send it over and I'll attach it to the case.

**Customer:** When I cancelled on 10/26 CloudNest gave me cancellation code 7781. Please put that in the dispute as evidence.

- `add_case_evidence({"case_id": "C-5001", "evidence_note": "Cancelled the CloudNest subscription on 10/26; CloudNest gave cancellation code 7781."})` → `{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the November 1 charge came after the cancellation.\n[2026-11-13] Cancelled the CloudNest subscription on 10/26; CloudNest gave cancellation code 7781.", "status": "under_review", "opened_at": "2026-11-13T10:00:00Z", "r …`

**Assistant:** Added to case C-5001: your 10/26 cancellation, code 7781. The case is still under review, and the follow-up is due 2026-11-23 by secure message in the Kestrel app.

_Episode written:_ Conversation on 2026-11-13: Customer Dana wanted the 2026-11-01 CloudNest charge ($9.99, T-3002) disputed after she said she cancelled in October (not verified). Assistant verified identity, filed dispute C-5001 (under review), and added later evidence that the customer said she cancelled on 10/26 with cancellation code 7781 (not verified). Follow-up due 2026-11-23 by secure message in the Kestrel app; no contact channel set. Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the last four, as typed, verify the customer | `{"verified": true, "valid_for_minutes": 15}` |
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the November 1 charge came after the cancellation."}]` |
| PASS | external | the numeric cancellation code reaches the case as evidence | `[["C-5001", "Customer says she cancelled the CloudNest subscription in October; the November 1 charge came after the cancellation.\n[2026-11-13] Cancelled the CloudNest subscription on 10/26; CloudNest gave cancellation  …` |

## or-decide  ·  resolve_case  ·  2026-11-20T09:00:00Z

_resolved:_ `[{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the November 1 charge came after the cancellation.\n[2026-11-13] Cancelled the CloudNest subscription on 10/26; CloudNest gave cancellation code 7781.", "status": "rejected", "opened_at": "2026-11-13T10:00:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant has no cancellation on file; resolution code NO_CANCELLATION_PROOF.", "resolved_at": "2026-11-20T09:00:00Z", "decision_id": "D-or-1" …`

## or-followup  ·  fire_followups  ·  2026-11-23T12:00:00Z

### follow-up session `followup-F-bbfe98da-1`

**Scheduler:** [scheduled follow-up F-bbfe98da] action=case_status_followup resume={"case_id": "C-5001"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the November 1 charge came after the cancellation.\n[2026-11-13] Cancelled the CloudNest subscription on 10/26; CloudNest gave cancellation code 7781.", "status": "rejected", "opened_at": "2026-11-13T10:00:0 …`
- `notify_customer({"message": "Update on dispute C-5001 (CloudNest charge of Nov 1): the case was decided on Nov 20 and closed in the merchant's favour \u2014 they had no cancellation on file (resolution code NO_CANCEL …)` → `{"channel": "secure_message", "message_id": 1, "status": "sent"}`

**Assistant:** The follow-up for case C-5001 was sent: the case was decided on Nov 20 and closed in the merchant's favour (no cancellation proof on file), and the customer was told that new proof, such as CloudNest's cancellation confirmation, would let them open a new dispute of the same charge via the card-care chat. Message sent by secure message in the Kestrel app.

_Episode written:_ Scheduled follow-up on 2026-11-23 (customer not present): Customer disputed case C-5001/txn T-3002, saying she cancelled CloudNest in October and the Nov 1 charge came after (not verified). The case was rejected on Nov 20 with NO_CANCELLATION_PROOF. The assistant sent one secure message: closed in the merchant's favour; new proof could support a new dispute via card-care chat. Case outcomes: C-5001 rejected (NO_CANCELLATION_PROOF). Lesson: none

_outcomes:_ `[{"followup_id": "F-bbfe98da", "user_id": "dana", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | guard | no masking token reaches an outbound message, and no identifier is ever masked | `3 outbound messages and episodes clean` |
