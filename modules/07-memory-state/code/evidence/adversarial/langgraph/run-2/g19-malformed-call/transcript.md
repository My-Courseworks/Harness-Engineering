# langgraph · adversarial · run 2 · g19-malformed-call

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## mc-s1  ·  malformed_probe  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Priya, card ending 4427, ZIP 94107. Please dispute the October 28 StreamMax charge; I cancelled by phone before it.

- `find_transactions({"merchant": "StreamMax"})` → `{"transactions": [{"transaction_id": "T-1001", "posted_on": "2026-09-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-1002", "posted_on": "2026-10-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription …`
- `report_malformed_tool_call({"tool": "verify_identity"})` → `{"error": "your verify_identity call's arguments were not valid JSON, so it did not run; make the call again with valid JSON arguments"}`
- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `file_dispute({"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the StreamMax subscription by phone before the October 28 charge."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-29a1add2", "due": "2026-11-19", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** I've filed your dispute.

- **Case:** C-5001 - StreamMax Premium monthly, $15.99, posted Oct 28, 2026
- **Reason:** cancelled subscription
- **Status:** under review (disputes are currently reviewed in about 10 days)
- **Follow-up:** due 2026-11-19, sent by secure message in the Kestrel app (no contact channel is set on your account; if you set one before then, it will go there instead).

If you have a cancellation reference from the phone call, send it over and I'll attach it to the case.

**Customer:** Thanks. What is the case number, and when will I hear back?

- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-29a1add2", "action": "case_status_followup", "due": "2026-11-19T10:00:00Z", "status": "pending", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set): the contact channel on file when it is sent", "case_id": "C-5001"}]}`

**Assistant:** - **Case number:** C-5001
- **When you'll hear back:** the case-status follow-up is due **2026-11-19 at 10:00 UTC**, sent by secure message in the Kestrel app (the default, since no contact channel is set). Disputes are currently reviewed in about 10 days.

_Episode written:_ Conversation on 2026-11-09: The customer wanted to dispute the Oct 28 StreamMax charge T-1002, saying they cancelled by phone before it (not verified). Dispute C-5001 was filed under review; follow-up F-29a1add2 is due 2026-11-19 10:00 UTC via Kestrel secure message, as no contact channel is set. The customer asked for the case number and timing. Case outcomes: C-5001 under_review. Lesson: Next time, complete identity verification before running transaction lookups, then proceed with the dispute.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the model's first tool call was made malformed (the probe ran) | `{"corrupted": "verify_identity", "corrupted_any": true}` |
| PASS | working | a malformed tool call is answered, so neither this turn nor the next fails | `"no errors"` |
| PASS | external | the model gets to make the call again: the dispute is filed in the same session | `[{"case_id": "C-5001", "status": "under_review"}]` |
