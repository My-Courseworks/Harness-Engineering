# langgraph · adversarial · run 2 · g30-channel-readback

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## cr-dana  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, Dana, card ending 5127, ZIP 60614. Please dispute the November 1 CloudNest charge, I cancelled in October. How and where will I hear back about it?

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-c38a9b8e", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Filed - here are the details:

- **Charge disputed:** CloudNest Storage, $9.99, posted 1 November 2026 (T-3002)
- **Reason:** cancelled subscription (you cancelled in October)
- **Case id:** C-5001 - status: under review
- **Follow-up:** due 23 November 2026, sent as a secure message in the Kestrel app. That's the default because no contact channel is set on your account; if you set one (email or SMS) before then, the follow-up will go there instead.

If you have the cancellation confirmation from CloudNest (a reference number or email), send it along and I can attach it to the case as evidence.

_Episode written:_ Conversation on 2026-11-13: The customer said they cancelled CloudNest in October (not verified) and wanted the 1 Nov 2026 $9.99 charge disputed, asking how/where they would hear back. Assistant verified identity, found T-3002, and filed dispute C-5001 (under review). Follow-up due 23 Nov 2026 via secure Kestrel app message by default; email/SMS if contact channel set before then. Assistant requested cancellation confirmation. Case outcomes: C-5001 under_review. Lesson: none

_Judge `cr-dana-channel`: **pass**, The assistant told the customer the follow-up is "sent as a secure message in the Kestrel app" and added "if you set one (email or SMS) before then, the follow-up will go there instead," so it did not say there is no channel or nowhere for it to be sent._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October."}]` |
| PASS | prospective | judge: Did the assistant tell the customer where the follow-up will reach them (for example by secure message in the Kestrel app, which is the default when no channel is set), and NOT say that there is no channel, no way, or nowhere for the follow-up to be sent? | `{"verdict": "pass", "reason": "The assistant told the customer the follow-up is \"sent as a secure message in the Kestrel app\" and added \"if you set one (email or SMS) before then, the follow-up will go there instead,\ …` |

## cr-eli  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Hi, Eli, card ending 6610, ZIP 73301. Please dispute the November 1 CloudNest charge, I cancelled in October. How and where will I hear back about it?

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October."})` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-05905360", "due": "2026-12-04", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Done - your dispute for the November 1 CloudNest charge ($9.99, T-4002) is filed as case **C-5002**, status under review.

**Where you'll hear back:** since no contact channel is set on your account, updates go by **secure message in the Kestrel app**. The first follow-up is due **December 4, 2026** - if you set a contact channel before then, it will go to that instead. Disputes are currently reviewed in about 10 days.

If you have a cancellation reference or confirmation email from CloudNest, I can attach it to the case - just paste the details.

_Episode written:_ Conversation on 2026-11-24: Customer asked to dispute the November 1 CloudNest charge and how/where they would hear back; they said they cancelled in October (not verified). Dispute filed for transaction T-4002 as case C-5002, under review. Follow-up F-05905360 due December 4, 2026, via Kestrel app secure message by default; assistant offered to attach cancellation proof. Case outcomes: C-5002 under_review. Lesson: none

_Judge `cr-eli-channel`: **pass**, The assistant said, "since no contact channel is set on your account, updates go by secure message in the Kestrel app," and explained the follow-up would go to a new contact channel if set before December 4, 2026._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October."}]` |
| PASS | prospective | judge: Did the assistant tell the customer where the follow-up will reach them (for example by secure message in the Kestrel app, which is the default when no channel is set), and NOT say that there is no channel, no way, or nowhere for the follow-up to be sent? | `{"verdict": "pass", "reason": "The assistant said, \"since no contact channel is set on your account, updates go by secure message in the Kestrel app,\" and explained the follow-up would go to a new contact channel if se …` |

## cr-marco  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** Hi, Marco, card ending 8830, ZIP 10011. Please dispute the $240 FitPulse renewal from November 3, I cancelled in October. How and where will I hear back about it?

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "FitPulse"})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`
- `file_dispute({"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the membership in October; the $240 annual renewal posted November 3, 2026."})` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-57e1aeb7", "due": "2026-11-22", "approval": "a Kestrel reviewer approves the message before it is sent", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Done - dispute filed on the $240 FitPulse renewal (posted Nov 3, 2026) with reason "cancelled subscription."

- **Case id:** C-5003 - currently under review
- **Follow-up:** due **Nov 22, 2026**, sent by **secure message in the Kestrel app** (the default, since you have no contact channel set). If you set a contact channel before then, the follow-up will go there instead.

One note: the case is reviewed by a Kestrel reviewer, and the follow-up message is approved before it's sent.

_Episode written:_ Conversation on 2026-11-12: Marco wanted the $240 FitPulse renewal posted Nov 3, 2026 disputed; the customer said they cancelled in October (not verified) and asked how/where they'd hear back. Identity verified; dispute T-2002 filed as C-5003, under review. Follow-up due Nov 22, 2026 by secure Kestrel app message (default; no contact channel set), reviewer-approved first. Case outcomes: C-5003 under_review. Lesson: Next time, confirm the transaction year when multiple matching merchant charges exist before filing the dispute.

_Judge `cr-marco-channel`: **pass**, The assistant stated the follow-up is "sent by **secure message in the Kestrel app** (the default, since you have no contact channel set). If you set a contact channel before then, the follow-up will go there instead."_

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the membership in October; the $240 annual renewal posted November 3, 2026."}]` |
| PASS | prospective | judge: Did the assistant tell the customer where the follow-up will reach them (for example by secure message in the Kestrel app, which is the default when no channel is set), and NOT say that there is no channel, no way, or nowhere for the follow-up to be sent? | `{"verdict": "pass", "reason": "The assistant stated the follow-up is \"sent by **secure message in the Kestrel app** (the default, since you have no contact channel set). If you set a contact channel before then, the fol …` |
