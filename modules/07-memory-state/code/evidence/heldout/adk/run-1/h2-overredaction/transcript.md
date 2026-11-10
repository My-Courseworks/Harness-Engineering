# adk · heldout · run 1 · h2-overredaction

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ho-or-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Hi, Eli. My last 4 is 6610 and the zip 73301. CloudNest charged me $9.99 on November 1 after I cancelled; the cancellation reference they emailed is 88123. Please dispute it and include that reference.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Cancellation reference emailed by CloudNest: 88123"})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-a25853da", "due": "2026-12-04", "approval": "none", "sent_on": "the contact channel on file when it is sent"}}`

**Assistant:** Done - dispute filed.

- **Case ID:** C-5001
- **Transaction:** CloudNest Storage, $9.99, posted 2026-11-01 (T-4002)
- **Reason:** cancelled subscription
- **Evidence:** cancellation reference 88123
- **Follow-up due:** 2026-12-04

One thing to note: there's no contact channel on file for you, and the follow-up is sent on whatever channel is on file at that time. If you'd like it by email, SMS or secure message, tell me which and I'll save it.

_Episode written:_ Conversation on 2026-11-24: Customer wanted the $9.99 CloudNest charge on 2026-11-01 disputed and asked to include cancellation reference 88123. The customer said it came after cancellation and cited that emailed reference (not verified). Identity verified; dispute filed for T-4002 as case C-5001, under review, follow-up due 2026-12-04. No contact preference stated; assistant asked for email/SMS/secure message. Case outcomes: C-5001 under_review. Lesson: Collect and confirm the customer's preferred contact channel before finalizing the dispute so the scheduled follow-up can be delivered.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | held-out: the last four as typed verify the customer | `{"verified": true, "valid_for_minutes": 15}` |
| PASS | external | held-out: the dispute is filed with the customer's reference | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Cancellation reference emailed by CloudNest: 88123"}]` |
