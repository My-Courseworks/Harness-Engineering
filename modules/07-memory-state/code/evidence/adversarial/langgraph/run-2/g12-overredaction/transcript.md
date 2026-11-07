# langgraph · adversarial · run 2 · g12-overredaction

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## or-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, I'm Dana. The last four digits are 5127 and my zip is 60614. CloudNest charged me again on November 1 even though I cancelled in October. Please dispute it.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states the CloudNest subscription was cancelled in October; the November 1 charge is a repeat monthly charge …)` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-741f3fd2", "due": "2026-11-23", "approval": "none", "sent_on": "the contact channel on file when it is sent"}}`

**Assistant:** I'll verify your identity and locate the charge.
Done - your dispute is filed.

- **Case:** C-5001, status *under review*
- **Charge:** CloudNest Storage, $9.99, posted 2026-11-01 (T-3002)
- **Reason:** cancelled subscription
- **Follow-up:** due **2026-11-23**

One thing to fix: there's no contact channel on file for you, and the follow-up is sent on whatever channel is on file when it's sent. If you tell me which you'd prefer - email, SMS, or secure message - I can set it now (you're verified for the next 15 minutes).

Also, if you have the cancellation confirmation or reference number from October, I can attach it to the case as evidence.

**Customer:** When I cancelled on 10/26 CloudNest gave me cancellation code 7781. Please put that in the dispute as evidence.

- `add_case_evidence({"case_id": "C-5001", "evidence_note": "CloudNest cancellation code 7781, issued when the customer cancelled the subscription on 2026-10-26."})` → `{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states the CloudNest subscription was cancelled in October; the November 1 charge is a repeat monthly charge after cancellation.\n[2026-11-13] CloudNest cancellation code 7781, issued when the customer cancelled the subscription on 2026-10-26.", "status": "under_review", "ope …`

**Assistant:** Added. Case C-5001 now shows the cancellation code 7781 with the 2026-10-26 cancellation date, alongside your original dispute reason. Status is still *under review*, follow-up due 2026-11-23.

Still open: no contact channel on file, so the follow-up has nowhere to go yet. Want me to set email, SMS, or secure message?

_Episode written:_ Conversation on 2026-11-13: Customer wanted a $9.99 Nov 1 CloudNest charge disputed; dispute filed as C-5001 for T-3002, under review, follow-up due 2026-11-23. The customer said she cancelled on 2026-10-26 with code 7781 (not verified); evidence added. No contact channel on file; no email/SMS/secure-message preference provided. Case outcomes: C-5001 under_review. Lesson: Next time, confirm the customer’s preferred contact channel before or immediately after filing so follow-up delivery isn’t left unresolved.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the last four, as typed, verify the customer | `{"verified": true, "valid_for_minutes": 15}` |
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states the CloudNest subscription was cancelled in October; the November 1 charge is a repeat monthly charge after cancellation …` |
| PASS | external | the numeric cancellation code reaches the case as evidence | `[["C-5001", "Customer states the CloudNest subscription was cancelled in October; the November 1 charge is a repeat monthly charge after cancellation.\n[2026-11-13] CloudNest cancellation code 7781, issued when the custo …` |

## or-decide  ·  resolve_case  ·  2026-11-20T09:00:00Z

_resolved:_ `[{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states the CloudNest subscription was cancelled in October; the November 1 charge is a repeat monthly charge after cancellation.\n[2026-11-13] CloudNest cancellation code 7781, issued when the customer cancelled the subscription on 2026-10-26.", "status": "rejected", "opened_at": "2026-11-13T10:00:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant has no cancellation on file; resolution code NO_CANCELLATION_PROOF.", "resolved_at": "2026-11-20T …`

## or-followup  ·  fire_followups  ·  2026-11-23T12:00:00Z

### follow-up session `followup-F-741f3fd2-1`

**Scheduler:** [scheduled follow-up F-741f3fd2] action=case_status_followup resume={"case_id": "C-5001"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states the CloudNest subscription was cancelled in October; the November 1 charge is a repeat monthly charge after cancellation.\n[2026-11-13] CloudNest cancellation code 7781, issued when the customer cancelled the subscription on 2026-10-26.", "status": "rejected …`
- `search_policy({"question": "What happens after a dispute is rejected for no cancellation proof? Can the customer appeal, and what is the deadline?"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.765, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`
- `notify_customer({"message": "Update on case C-5001 (CloudNest, Nov 1 charge): the dispute was rejected on 20 Nov \u2014 resolution code NO_CANCELLATION_PROOF, as the merchant had no cancellation on file. Your evidenc …)` → `{"channel": "secure_message", "message_id": 1, "status": "sent"}`

**Assistant:** I'll check the current status of the case.
**Follow-up F-741f3fd2 handled - case C-5001 checked and the customer notified.**

- **Case C-5001** (CloudNest, txn T-3002, cancelled_subscription): status **rejected**, resolved 2026-11-20, resolution code `NO_CANCELLATION_PROOF` - merchant had no cancellation on file. Customer's evidence (cancellation code 7781, 26 Oct) remains attached.
- Sent one message via secure message: outcome, the reason, and a pointer to the card-care chat for next steps. I did not state any appeal window or post-rejection deadline, since policy documents don't contain one.
- No questions asked; the customer was told to message the card-care chat if they want to act.

_Episode written:_ Scheduled follow-up on 2026-11-23 (customer not present): Follow-up F-741f3fd2 sought status of case C-5001 (txn T-3002, CloudNest Nov 1 cancelled_subscription charge). Assistant checked: rejected 2026-11-20, NO_CANCELLATION_PROOF; merchant had no cancellation on file. The customer said the subscription was cancelled in October (not verified). Assistant sent one secure message with the outcome and advised card-care chat for next steps; no appeal deadline promised. No preference stated. Case outcomes: C-5001 rejected (NO_CANCELLATION_PROOF). Lesson: none

_outcomes:_ `[{"followup_id": "F-741f3fd2", "user_id": "dana", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | guard | no masking token reaches an outbound message, and no identifier is ever masked | `3 outbound messages and episodes clean` |
