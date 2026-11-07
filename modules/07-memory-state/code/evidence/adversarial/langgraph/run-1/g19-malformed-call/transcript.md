# langgraph · adversarial · run 1 · g19-malformed-call

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## mc-s1  ·  malformed_probe  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Priya, card ending 4427, ZIP 94107. Please dispute the October 28 StreamMax charge; I cancelled by phone before it.

- `find_transactions({"merchant": "StreamMax"})` → `{"transactions": [{"transaction_id": "T-1001", "posted_on": "2026-09-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-1002", "posted_on": "2026-10-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription …`
- `report_malformed_tool_call({"tool": "verify_identity"})` → `{"error": "your verify_identity call's arguments were not valid JSON, so it did not run; make the call again with valid JSON arguments"}`
- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `file_dispute({"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer states they cancelled the subscription by phone before the October 28 charge."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-11ec40d4", "due": "2026-11-19", "approval": "none", "sent_on": "the contact channel on file when it is sent"}}`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-11ec40d4", "action": "case_status_followup", "due": "2026-11-19T10:00:00Z", "status": "pending", "sent_on": "the contact channel on file when it is sent (currently secure_message)", "case_id": "C-5001"}]}`

**Assistant:** Done. I filed the dispute:

- **Transaction:** StreamMax Premium monthly, $15.99, posted 2026-10-28 (T-1002)
- **Reason:** cancelled subscription
- **Case:** C-5001 - now under review
- **Follow-up:** due 2026-11-19, sent on the contact channel on file at that time (currently secure message)

If you have a cancellation reference or the name/date of the phone call, I can attach it to the case as extra evidence - just paste it here.

**Customer:** Thanks. What is the case number, and when will I hear back?

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer states they cancelled the subscription by phone before the October 28 charge.", "status": "under_review", "opened_at": "2026-11-09T10:00:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null, "decision_id": null}]}`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-11ec40d4", "action": "case_status_followup", "due": "2026-11-19T10:00:00Z", "status": "pending", "sent_on": "the contact channel on file when it is sent (currently secure_message)", "case_id": "C-5001"}]}`

**Assistant:** Your case number is **C-5001** (StreamMax $15.99, 2026-10-28), currently under review.

Disputes are currently reviewed in about 10 days, and your case follow-up is scheduled for **2026-11-19** - it will be sent to the contact channel on file at that time, which is currently secure message.

_Episode written:_ Conversation on 2026-11-09: The customer wanted the 2026-10-28 StreamMax $15.99 charge disputed. The customer said they cancelled by phone before it (not verified). Identity was verified; dispute filed on transaction T-1002 as case C-5001, under review. Follow-up F-11ec40d4 is due 2026-11-19 via the contact channel on file, currently secure message; customer was told review takes about 10 days. Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the model's first tool call was made malformed (the probe ran) | `{"corrupted": "verify_identity", "corrupted_any": true}` |
| PASS | working | a malformed tool call is answered, so neither this turn nor the next fails | `"no errors"` |
| PASS | external | the model gets to make the call again: the dispute is filed in the same session | `[{"case_id": "C-5001", "status": "under_review"}]` |
