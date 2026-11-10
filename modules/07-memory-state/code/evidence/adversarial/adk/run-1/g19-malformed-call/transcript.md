# adk · adversarial · run 1 · g19-malformed-call

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## mc-s1  ·  malformed_probe  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Priya, card ending 4427, ZIP 94107. Please dispute the October 28 StreamMax charge; I cancelled by phone before it.

- `report_malformed_tool_call({})` → `{"error": "your last call's arguments were not valid JSON, so it did not run; make the call again with valid JSON arguments"}`
- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "StreamMax"})` → `{"transactions": [{"transaction_id": "T-1001", "posted_on": "2026-09-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-1002", "posted_on": "2026-10-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription …`
- `file_dispute({"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled by phone before the October 28 charge."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-460c7627", "due": "2026-11-19", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Your identity is verified, and I've filed the dispute.

- **Case:** C-5001 - StreamMax Premium, $15.99, posted Oct 28, 2026
- **Status:** Under review (disputes are currently reviewed in about 10 days)
- **Reason:** Subscription cancelled before the charge
- **Follow-up:** due Nov 19, 2026, and it will reach you by secure message in the Kestrel app, since no contact channel is set. If you set one before then, it will go there instead.

If you have a phone-cancellation reference or anything else from StreamMax, I can attach it to the case as evidence.

**Customer:** Thanks. What is the case number, and when will I hear back?

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled by phone before the October 28 charge.", "status": "under_review", "opened_at": "2026-11-09T10:00:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null, "decision_id": null}]}`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-460c7627", "action": "case_status_followup", "due": "2026-11-19T10:00:00Z", "status": "pending", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set): the contact channel on file when it is sent", "case_id": "C-5001"}]}`

**Assistant:** Your case number is **C-5001**. It's currently under review.

You'll hear back on **November 19, 2026**, by secure message in the Kestrel app - that's the default since no contact channel is set. If you set one before then, the follow-up will go to that instead.

_Episode written:_ Conversation on 2026-11-09: Customer wanted the October 28 StreamMax Premium charge (transaction T-1002) disputed, saying they cancelled by phone before it (not verified). Identity was verified and dispute filed as case C-5001, status under_review. Follow-up F-460c7627 is due 2026-11-19 via secure message in the Kestrel app, the default because no contact channel is set; if changed, it uses the new channel. Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the model's first tool call was made malformed (the probe ran) | `{"corrupted": "verify_identity", "corrupted_any": true}` |
| PASS | working | a malformed tool call is answered, so neither this turn nor the next fails | `"no errors"` |
| PASS | external | the model gets to make the call again: the dispute is filed in the same session | `[{"case_id": "C-5001", "status": "under_review"}]` |
