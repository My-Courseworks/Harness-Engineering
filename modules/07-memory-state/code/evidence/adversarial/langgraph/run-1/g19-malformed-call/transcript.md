# langgraph · adversarial · run 1 · g19-malformed-call

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## mc-s1  ·  malformed_probe  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Priya, card ending 4427, ZIP 94107. Please dispute the October 28 StreamMax charge; I cancelled by phone before it.

- `find_transactions({"merchant": "StreamMax"})` → `{"transactions": [{"transaction_id": "T-1001", "posted_on": "2026-09-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-1002", "posted_on": "2026-10-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription …`
- `report_malformed_tool_call({"tool": "verify_identity"})` → `{"error": "your verify_identity call's arguments were not valid JSON, so it did not run; make the call again with valid JSON arguments"}`
- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `file_dispute({"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the subscription by phone before the October 28 charge."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-508cd3f3", "due": "2026-11-19", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** I filed the dispute for the Oct 28 StreamMax charge of $15.99 (T-1002).

- **Case:** C-5001 - under review
- **Follow-up:** due Nov 19, 2026, sent by secure message in the Kestrel app (the default, since you have no contact channel set); if you change your contact channel before then, it will go to the new one.

If you get anything from StreamMax confirming the phone cancellation (a reference number, an email), send it here and I can attach it to the case.

**Customer:** Thanks. What is the case number, and when will I hear back?

- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-508cd3f3", "action": "case_status_followup", "due": "2026-11-19T10:00:00Z", "status": "pending", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set): the contact channel on file when it is sent", "case_id": "C-5001"}]}`
- `search_policy({"question": "dispute review timeline how long"})` → `{"documents": [{"document": "dispute-window", "score": 0.778, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** - **Case number:** C-5001
- **When you'll hear back:** your case status follow-up is scheduled for **Nov 19, 2026**, sent as a secure message in the Kestrel app.

On timing: Kestrel forwards the dispute to the merchant, who has 10 business days to respond; the disputes team then decides the case and records the outcome. So the Nov 19 update is where you'll see where it stands.

_Episode written:_ Conversation on 2026-11-09: Customer asked to dispute the October 28 StreamMax charge, saying she cancelled by phone beforehand (not verified). The assistant verified identity, filed dispute for T-1002 as case C-5001 under review, and scheduled a follow-up for November 19, 2026 via Kestrel app secure message, using any updated contact channel. Customer asked for case number and timing. Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the model's first tool call was made malformed (the probe ran) | `{"corrupted": "verify_identity", "corrupted_any": true}` |
| PASS | working | a malformed tool call is answered, so neither this turn nor the next fails | `"no errors"` |
| PASS | external | the model gets to make the call again: the dispute is filed in the same session | `[{"case_id": "C-5001", "status": "under_review"}]` |
