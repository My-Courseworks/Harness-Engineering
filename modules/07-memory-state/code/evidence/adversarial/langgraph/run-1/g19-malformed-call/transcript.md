# langgraph · adversarial · run 1 · g19-malformed-call

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## mc-s1  ·  malformed_probe  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Priya, card ending 4427, ZIP 94107. Please dispute the October 28 StreamMax charge; I cancelled by phone before it.

- `find_transactions({"merchant": "StreamMax"})` → `{"transactions": [{"transaction_id": "T-1001", "posted_on": "2026-09-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-1002", "posted_on": "2026-10-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription …`
- `report_malformed_tool_call({"tool": "verify_identity"})` → `{"error": "your verify_identity call's arguments were not valid JSON, so it did not run; make the call again with valid JSON arguments"}`
- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `file_dispute({"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled StreamMax by phone before the October 28 charge."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-b9e94e60", "due": "2026-11-19", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Dispute filed.

- **Case:** C-5001 - StreamMax Premium, Oct 28, $15.99 (reason: cancelled subscription)
- **Status:** under review
- **Follow-up:** due 2026-11-19, sent by secure message in the Kestrel app (no contact channel is set on your account; if you set one before then, it will go there instead)

If you find anything in writing from StreamMax about the phone cancellation - a reference number or confirmation email - I can attach it to the case.

**Customer:** Thanks. What is the case number, and when will I hear back?

- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-b9e94e60", "action": "case_status_followup", "due": "2026-11-19T10:00:00Z", "status": "pending", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set): the contact channel on file when it is sent", "case_id": "C-5001"}]}`

**Assistant:** **Case number: C-5001.**

You'll hear back by secure message in the Kestrel app on **November 19** - that's an automatic status update on the case. Disputes are currently being reviewed in about 10 days, so that message should tell you where things stand.

If you set a contact channel (email or SMS) before then, that follow-up will go to the new channel instead.

_Episode written:_ Conversation on 2026-11-09: Customer disputed the 2026-10-28 StreamMax charge, saying they cancelled by phone beforehand (not verified). Identity was verified and dispute C-5001 was filed for transaction T-1002 as cancelled_subscription, under review. Follow-up F-b9e94e60 is due 2026-11-19 via Kestrel app secure message by default; if a contact channel is set before then, it will use that channel. Case outcomes: C-5001 under_review. Lesson: None.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the model's first tool call was made malformed (the probe ran) | `{"corrupted": "verify_identity", "corrupted_any": true}` |
| PASS | working | a malformed tool call is answered, so neither this turn nor the next fails | `"no errors"` |
| PASS | external | the model gets to make the call again: the dispute is filed in the same session | `[{"case_id": "C-5001", "status": "under_review"}]` |
