# adk · adversarial · run 2 · g19-malformed-call

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## mc-s1  ·  malformed_probe  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Priya, card ending 4427, ZIP 94107. Please dispute the October 28 StreamMax charge; I cancelled by phone before it.

- `report_malformed_tool_call({})` → `{"error": "your last call's arguments were not valid JSON, so it did not run; make the call again with valid JSON arguments"}`
- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "StreamMax"})` → `{"transactions": [{"transaction_id": "T-1001", "posted_on": "2026-09-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-1002", "posted_on": "2026-10-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription …`
- `file_dispute({"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled by phone before the October 28 charge."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-4e18fcc2", "due": "2026-11-19", "approval": "none", "sent_on": "the contact channel on file when it is sent"}}`

**Assistant:** Done - I've filed the dispute for the October 28 StreamMax charge of $15.99 ($15.99, "StreamMax Premium monthly").

- **Case ID:** C-5001 (under review)
- **Follow-up due:** November 19, 2026

One thing: there's no contact channel on file, so the follow-up has nowhere to go. Would you like it sent by email, SMS, or secure message? Just tell me which and I'll set it.

**Customer:** Thanks. What is the case number, and when will I hear back?

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled by phone before the October 28 charge.", "status": "under_review", "opened_at": "2026-11-09T10:00:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null, "decision_id": null}]}`
- `search_policy({"question": "How long does a dispute review take and when will the customer hear back?"})` → `{"documents": [{"document": "dispute-window", "score": 0.765, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** - **Case number:** C-5001
- **Status:** Under review

The merchant has 10 business days to respond, and your case follow-up is due **November 19, 2026**.

Note the follow-up still has no contact channel to go to, so if you want to hear back automatically, tell me whether to use email, SMS, or secure message.

_Episode written:_ Conversation on 2026-11-09: Customer asked to dispute the October 28 StreamMax charge, saying they cancelled by phone before it (not verified). Identity was verified; dispute C-5001 was filed for transaction T-1002 ($15.99), status under review, follow-up F-4e18fcc2 due 2026-11-19. Assistant said the merchant has 10 business days to respond; no contact-channel preference was provided. Case outcomes: C-5001 under_review. Lesson: Next time, confirm or collect the customer's contact channel before filing a dispute with a follow-up, so the follow-up has a destination.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the model's first tool call was made malformed (the probe ran) | `{"corrupted": "verify_identity", "corrupted_any": true}` |
| PASS | working | a malformed tool call is answered, so neither this turn nor the next fails | `"no errors"` |
| PASS | external | the model gets to make the call again: the dispute is filed in the same session | `[{"case_id": "C-5001", "status": "under_review"}]` |
