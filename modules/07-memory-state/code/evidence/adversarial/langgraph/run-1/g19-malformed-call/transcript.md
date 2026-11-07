# langgraph · adversarial · run 1 · g19-malformed-call

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## mc-s1  ·  malformed_probe  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Priya, card ending 4427, ZIP 94107. Please dispute the October 28 StreamMax charge; I cancelled by phone before it.

- `find_transactions({"merchant": "StreamMax"})` → `{"transactions": [{"transaction_id": "T-1001", "posted_on": "2026-09-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-1002", "posted_on": "2026-10-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription …`
- `report_malformed_tool_call({"tool": "verify_identity"})` → `{"error": "your verify_identity call's arguments were not valid JSON, so it did not run; make the call again with valid JSON arguments"}`
- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `file_dispute({"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the subscription by phone before the October 28 charge."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-3b28d87a", "due": "2026-11-19", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Done - I've disputed the October 28 StreamMax Premium charge of $15.99 (transaction T-1002), reason: subscription cancelled before the charge.

- **Case id:** C-5001 - status: under review
- **Follow-up due:** 2026-11-19
- **Where it will reach you:** secure message in the Kestrel app, since no contact channel is set (if you set an email or SMS before then, it goes there instead).

You're verified for the next 15 minutes, so if you have something like a cancellation reference from the phone call, I can attach it to the case - that helps.

**Customer:** Thanks. What is the case number, and when will I hear back?

**Assistant:** Your case number is **C-5001**.

You'll hear back with a follow-up on **2026-11-19**, sent by secure message in the Kestrel app (no contact channel is set on your account). The case shows as under review until then.

_Episode written:_ Conversation on 2026-11-09: Customer wanted the October 28 StreamMax charge disputed, saying they had cancelled by phone before it (not verified). Assistant filed dispute for transaction T-1002, case C-5001, status under review. Follow-up due 2026-11-19 by secure message in the Kestrel app, since no contact channel is set. Assistant confirmed case number and follow-up date. Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the model's first tool call was made malformed (the probe ran) | `{"corrupted": "verify_identity", "corrupted_any": true}` |
| PASS | working | a malformed tool call is answered, so neither this turn nor the next fails | `"no errors"` |
| PASS | external | the model gets to make the call again: the dispute is filed in the same session | `[{"case_id": "C-5001", "status": "under_review"}]` |
