# langgraph · adversarial · run 2 · g19-malformed-call

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## mc-s1  ·  malformed_probe  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Priya, card ending 4427, ZIP 94107. Please dispute the October 28 StreamMax charge; I cancelled by phone before it.

- `find_transactions({"merchant": "StreamMax"})` → `{"transactions": [{"transaction_id": "T-1001", "posted_on": "2026-09-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-1002", "posted_on": "2026-10-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription …`
- `report_malformed_tool_call({"tool": "verify_identity"})` → `{"error": "your verify_identity call's arguments were not valid JSON, so it did not run; make the call again with valid JSON arguments"}`
- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `file_dispute({"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled StreamMax by phone before the October 28 charge."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-7439c4a6", "due": "2026-11-19", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Done - I verified you and filed the dispute.

- **Charge:** StreamMax Premium monthly, $15.99, posted 2026-10-28 (T-1002)
- **Reason:** cancelled subscription
- **Case:** C-5001, under review
- **Follow-up:** due 2026-11-19, sent by secure message in the Kestrel app - the default since no contact channel is set. If you change your contact channel before then, the follow-up goes to the new one.

Reviews currently take about 10 days. If you have a cancellation reference from the phone call, I can attach it to the case - just tell me what it says.

**Customer:** Thanks. What is the case number, and when will I hear back?

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled StreamMax by phone before the October 28 charge.", "status": "under_review", "opened_at": "2026-11-09T10:00:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null, "decision_id": null}]}`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-7439c4a6", "action": "case_status_followup", "due": "2026-11-19T10:00:00Z", "status": "pending", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set): the contact channel on file when it is sent", "case_id": "C-5001"}]}`

**Assistant:** - **Case number:** C-5001 (status: under review)
- **When you'll hear back:** a follow-up is scheduled for 2026-11-19, sent by secure message in the Kestrel app, since no contact channel is set. Changing your contact channel before then means it goes to the new one instead.

Reviews are currently running about 10 days, so that timeline lines up.

_Episode written:_ Conversation on 2026-11-09: Customer wanted to dispute the October 28 StreamMax charge. Assistant verified identity and filed dispute for T-1002, case C-5001 under review. Follow-up due 2026-11-19 via secure message in the Kestrel app; it will use a changed contact channel if updated. Customer asked for case number and timing; provided. The customer said they cancelled by phone before the charge (not verified). Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the model's first tool call was made malformed (the probe ran) | `{"corrupted": "verify_identity", "corrupted_any": true}` |
| PASS | working | a malformed tool call is answered, so neither this turn nor the next fails | `"no errors"` |
| PASS | external | the model gets to make the call again: the dispute is filed in the same session | `[{"case_id": "C-5001", "status": "under_review"}]` |
