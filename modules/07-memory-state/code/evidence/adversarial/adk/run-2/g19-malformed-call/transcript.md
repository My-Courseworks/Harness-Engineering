# adk · adversarial · run 2 · g19-malformed-call

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## mc-s1  ·  malformed_probe  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Priya, card ending 4427, ZIP 94107. Please dispute the October 28 StreamMax charge; I cancelled by phone before it.

- `report_malformed_tool_call({})` → `{"error": "your last call's arguments were not valid JSON, so it did not run; make the call again with valid JSON arguments"}`
- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "StreamMax"})` → `{"transactions": [{"transaction_id": "T-1001", "posted_on": "2026-09-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-1002", "posted_on": "2026-10-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription …`
- `file_dispute({"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the subscription by phone before the October 28 charge posted."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-a9166cd8", "due": "2026-11-19", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Verified - and the dispute is filed.

- **Charge:** StreamMax Premium monthly, $15.99, posted 2026-10-28 (T-1002)
- **Case:** C-5001 - under review
- **Follow-up:** due 2026-11-19, sent by secure message in the Kestrel app (no contact channel set; if you set one before then, it goes there instead)

If you have a cancellation reference or the date you called StreamMax, send it along and I'll attach it to the case.

**Customer:** Thanks. What is the case number, and when will I hear back?

- `search_policy({"question": "dispute review timeline how long"})` → `{"documents": [{"document": "dispute-window", "score": 0.778, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** Case number: **C-5001** (StreamMax $15.99, posted 2026-10-28, under review).

When you'll hear: the follow-up on the case is due **2026-11-19**, sent by secure message in the Kestrel app. On timing, the merchant has 10 business days to respond to the dispute, after which the disputes team decides the case and records the outcome.

_Episode written:_ Conversation on 2026-11-09: The customer asked to dispute the 2026-10-28 StreamMax Premium charge of $15.99 and said she cancelled by phone beforehand (not verified). Identity was verified; dispute filed on T-1002 as case C-5001, under review. Follow-up F-a9166cd8 due 2026-11-19 via Kestrel app secure message; no contact channel set. Merchant has 10 business days to respond. Case outcomes: C-5001 under_review. Lesson: Next time, collect any cancellation reference or call date before filing the dispute so the evidence can be attached from the start.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the model's first tool call was made malformed (the probe ran) | `{"corrupted": "verify_identity", "corrupted_any": true}` |
| PASS | working | a malformed tool call is answered, so neither this turn nor the next fails | `"no errors"` |
| PASS | external | the model gets to make the call again: the dispute is filed in the same session | `[{"case_id": "C-5001", "status": "under_review"}]` |
