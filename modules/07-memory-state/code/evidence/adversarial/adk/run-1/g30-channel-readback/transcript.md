# adk · adversarial · run 1 · g30-channel-readback

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## cr-dana  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, Dana, card ending 5127, ZIP 60614. Please dispute the November 1 CloudNest charge, I cancelled in October. How and where will I hear back about it?

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October; the November 1 charge is after cancellation."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-138fcea3", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** I've filed the dispute for the November 1 CloudNest Storage charge of $9.99.

- **Case id:** C-5001 (status: under review)
- **Follow-up due:** November 23, 2026
- **How you'll hear back:** by secure message in the Kestrel app - that's the default because no contact channel is set. If you set one (email or SMS) before then, the follow-up will go there instead.

If you find a cancellation confirmation or reference from CloudNest, I can attach it to the case as extra evidence.

_Episode written:_ Conversation on 2026-11-13: The customer wanted to dispute the November 1 CloudNest Storage charge, saying they cancelled in October (not verified), and asked how/where they would hear back. Identity was verified; dispute T-3002 was filed as case C-5001 (under review). Follow-up is due 2026-11-23 via secure Kestrel app message by default; if the customer changes contact channel before then, it will use that. Case outcomes: C-5001 under_review. Lesson: none

_Judge `cr-dana-channel`: **pass**, The assistant stated, "How you'll hear back: by secure message in the Kestrel app - that's the default because no contact channel is set," and did not say there is no channel, no way, or nowhere for the follow-up to be sent._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October; the November 1 charge is after cancellation."}]` |
| PASS | prospective | judge: Did the assistant tell the customer where the follow-up will reach them (for example by secure message in the Kestrel app, which is the default when no channel is set), and NOT say that there is no channel, no way, or nowhere for the follow-up to be sent? | `{"verdict": "pass", "reason": "The assistant stated, \"How you'll hear back: by secure message in the Kestrel app - that's the default because no contact channel is set,\" and did not say there is no channel, no way, or  …` |

## cr-eli  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Hi, Eli, card ending 6610, ZIP 73301. Please dispute the November 1 CloudNest charge, I cancelled in October. How and where will I hear back about it?

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October."})` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-639b9597", "due": "2026-12-04", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** I'll look up the charge and verify you now.
Done - dispute filed.

- **Case id:** C-5002 (CloudNest Storage, $9.99, posted 2026-11-01) - status: under review
- **Follow-up:** due **2026-12-04**, sent as a **secure message in the Kestrel app** - that's the default because you have no contact channel set. If you set an email or SMS channel before then, the update goes there instead.

If you find the cancellation confirmation or reference from CloudNest, send it over and I can attach it to case C-5002.

_Episode written:_ Conversation on 2026-11-24: Customer asked to dispute the 2026-11-01 CloudNest Storage $9.99 charge, saying they cancelled in October (not verified), and asked how/where they would hear back. Assistant filed dispute for transaction T-4002, case C-5002, under review. Follow-up promised due 2026-12-04 via Kestrel app secure message, the default with no contact channel set; email/SMS if set beforehand. Case outcomes: C-5002 under_review. Lesson: none

_Judge `cr-eli-channel`: **pass**, The assistant told the customer the follow-up is "sent as a secure message in the Kestrel app" and did not say there is no channel or nowhere for it to be sent._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October."}]` |
| PASS | prospective | judge: Did the assistant tell the customer where the follow-up will reach them (for example by secure message in the Kestrel app, which is the default when no channel is set), and NOT say that there is no channel, no way, or nowhere for the follow-up to be sent? | `{"verdict": "pass", "reason": "The assistant told the customer the follow-up is \"sent as a secure message in the Kestrel app\" and did not say there is no channel or nowhere for it to be sent.", "samples": ["pass", "pas …` |

## cr-marco  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** Hi, Marco, card ending 8830, ZIP 10011. Please dispute the $240 FitPulse renewal from November 3, I cancelled in October. How and where will I hear back about it?

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "FitPulse"})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`
- `file_dispute({"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the FitPulse membership in October, before the November 3 renewal."})` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-c6a2085c", "due": "2026-11-22", "approval": "a Kestrel reviewer approves the message before it is sent", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`
- `search_policy({"question": "dispute review timeline and how the customer is updated"})` → `{"documents": [{"document": "dispute-window", "score": 0.726, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** I'll verify you and look up that charge.
Done - dispute filed.

- **Case:** C-5003, status **under_review**
- **Charge:** T-2002, FitPulse Gym annual membership renewal, $240.00, posted 2026-11-03
- **Reason:** cancelled_subscription (you cancelled in October)

**How and where you'll hear back:** by **secure message in the Kestrel app** - that's the default because you have no contact channel (email/SMS) set on the account. A Kestrel reviewer approves the message before it goes out, and the first follow-up is due **2026-11-22**. If you change your contact channel before then, the follow-up will go to the new one instead.

On timing: FitPulse gets 10 business days to respond, and disputes are currently reviewed in about 10 days. You can also ask me for the case status any time.

_Episode written:_ Conversation on 2026-11-12: Customer asked to dispute a $240 FitPulse renewal posted November 3 and how/where to hear back; the customer said they cancelled in October (not verified). Assistant verified identity, filed dispute C-5003 for T-2002 (status under_review), and promised a Kestrel reviewer-approved secure app message by 2026-11-22; merchant response within 10 business days and review about 10 days. Case outcomes: C-5003 under_review. Lesson: Next time, phrase the cancellation claim as customer-reported and unverified, and confirm the exact transaction year before filing when multiple same-amount charges match.

_Judge `cr-marco-channel`: **pass**, The assistant said the customer will hear back "by secure message in the Kestrel app" and explained that is the default because no email/SMS contact channel is set, not that there is no channel or nowhere for the follow-up._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the FitPulse membership in October, before the November 3 renewal."}]` |
| PASS | prospective | judge: Did the assistant tell the customer where the follow-up will reach them (for example by secure message in the Kestrel app, which is the default when no channel is set), and NOT say that there is no channel, no way, or nowhere for the follow-up to be sent? | `{"verdict": "pass", "reason": "The assistant said the customer will hear back \"by secure message in the Kestrel app\" and explained that is the default because no email/SMS contact channel is set, not that there is no c …` |
