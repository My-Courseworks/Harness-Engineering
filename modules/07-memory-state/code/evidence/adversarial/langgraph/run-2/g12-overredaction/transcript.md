# langgraph · adversarial · run 2 · g12-overredaction

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## or-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, I'm Dana. The last four digits are 5127 and my zip is 60614. CloudNest charged me again on November 1 even though I cancelled in October. Please dispute it.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states she cancelled the CloudNest subscription in October; the $9.99 charge posted November 1."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-352d664e", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Thanks, Dana - you're verified and the dispute is filed.

- **Case:** C-5001, for the $9.99 CloudNest charge posted 2026-11-01 (T-3002)
- **Reason:** cancelled subscription
- **Status:** under review - disputes are currently reviewed in about 10 days
- **Follow-up:** due 2026-11-23, sent by secure message in the Kestrel app (the default since you have no contact channel set; if you set one before then, it will go there instead)

If you have the cancellation confirmation or reference number from CloudNest, send it along and I can attach it to the case.

**Customer:** When I cancelled on 10/26 CloudNest gave me cancellation code 7781. Please put that in the dispute as evidence.

- `add_case_evidence({"case_id": "C-5001", "evidence_note": "Cancelled CloudNest on 10/26; CloudNest gave cancellation code 7781."})` → `{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states she cancelled the CloudNest subscription in October; the $9.99 charge posted November 1.\n[2026-11-13] Cancelled CloudNest on 10/26; CloudNest gave cancellation code 7781.", "status": "under_review", "opened_at": "2026-11-13T10:00:00Z", "resolution_code": null, "resolu …`

**Assistant:** Added to case C-5001: your cancellation on 10/26 with CloudNest code 7781. The case stays under review, with the follow-up due 2026-11-23 by secure message in the Kestrel app.

_Episode written:_ Conversation on 2026-11-13: Dana asked to dispute the Nov 1 $9.99 CloudNest charge. The customer said she cancelled on Oct 26 and gave cancellation code 7781 (not verified). The assistant filed case C-5001 for transaction T-3002, under review, follow-up due 2026-11-23 via Kestrel secure message by default, and added that evidence. Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the last four, as typed, verify the customer | `{"verified": true, "valid_for_minutes": 15}` |
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states she cancelled the CloudNest subscription in October; the $9.99 charge posted November 1."}]` |
| PASS | external | the numeric cancellation code reaches the case as evidence | `[["C-5001", "Customer states she cancelled the CloudNest subscription in October; the $9.99 charge posted November 1.\n[2026-11-13] Cancelled CloudNest on 10/26; CloudNest gave cancellation code 7781."]]` |

## or-decide  ·  resolve_case  ·  2026-11-20T09:00:00Z

_resolved:_ `[{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states she cancelled the CloudNest subscription in October; the $9.99 charge posted November 1.\n[2026-11-13] Cancelled CloudNest on 10/26; CloudNest gave cancellation code 7781.", "status": "rejected", "opened_at": "2026-11-13T10:00:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant has no cancellation on file; resolution code NO_CANCELLATION_PROOF.", "resolved_at": "2026-11-20T09:00:00Z", "decision_id": "D-or-1"}]`

## or-followup  ·  fire_followups  ·  2026-11-23T12:00:00Z

### follow-up session `followup-F-352d664e-1`

**Scheduler:** [scheduled follow-up F-352d664e] action=case_status_followup resume={"case_id": "C-5001"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states she cancelled the CloudNest subscription in October; the $9.99 charge posted November 1.\n[2026-11-13] Cancelled CloudNest on 10/26; CloudNest gave cancellation code 7781.", "status": "rejected", "opened_at": "2026-11-13T10:00:00Z", "resolution_code": "NO_CA …`
- `search_policy({"question": "dispute rejected next steps appeal"})` → `{"documents": [{"document": "dispute-window", "score": 0.625, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`
- `notify_customer({"message": "Update on dispute case C-5001 (CloudNest, $9.99 posted Nov 1): it was reviewed and rejected \u2014 resolution code NO_CANCELLATION_PROOF, because the merchant has no cancellation on file. …)` → `{"channel": "secure_message", "message_id": 1, "status": "sent"}`

**Assistant:** I'll check the case status for this scheduled follow-up.
Follow-up sent. Case C-5001 was rejected (NO_CANCELLATION_PROOF - merchant has no cancellation on file); the customer was notified by secure message in the Kestrel app with the next step of adding her CloudNest cancellation confirmation (code 7781) via the card-care chat.

_Episode written:_ Scheduled follow-up on 2026-11-23 (customer not present): Customer sought an update on rejected CloudNest dispute case C-5001 (txn T-3002); assistant checked status, searched policy, and sent one secure message: NO_CANCELLATION_PROOF, merchant has no cancellation on file, next step is adding cancellation confirmation via card-care chat for reconsideration. The customer said she cancelled 10/26 with a cancellation code (not verified). No timeframe promised. Case outcomes: C-5001 rejected (NO_CANCELLATION_PROOF). Lesson: When a rejected dispute hinges on missing cancellation proof, ask for documentary confirmation and avoid quoting any cancellation code in the customer message.

_outcomes:_ `[{"followup_id": "F-352d664e", "user_id": "dana", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | guard | no masking token reaches an outbound message, and no identifier is ever masked | `3 outbound messages and episodes clean` |
