# adk · adversarial · run 2 · g30-channel-readback

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## cr-dana  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, Dana, card ending 5127, ZIP 60614. Please dispute the November 1 CloudNest charge, I cancelled in October. How and where will I hear back about it?

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says the CloudNest subscription was cancelled in October."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-02d038fc", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Done - dispute filed for the Nov 1 CloudNest charge ($9.99, transaction T-3002).

- **Case id:** C-5001 (status: under review)
- **Follow-up due:** November 23, 2026
- **Where you'll hear back:** secure message in the Kestrel app - no contact channel is set on your account, so that's the default. If you set an email or SMS before then, the follow-up will go there instead.

Nothing else needed from you right now.

_Episode written:_ Conversation on 2026-11-13: The customer asked to dispute the November 1 CloudNest charge, saying the subscription was cancelled in October (not verified), and asked how and where they would hear back. The assistant filed dispute C-5001 for transaction T-3002, status under review, with follow-up due November 23, 2026 via secure message in the Kestrel app by default, or a newly set contact channel. Case outcomes: C-5001 under_review. Lesson: none

_Judge `cr-dana-channel`: **pass**, The assistant stated "Where you'll hear back: secure message in the Kestrel app - no contact channel is set on your account, so that's the default" and did not say there is no channel or nowhere for the follow-up._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says the CloudNest subscription was cancelled in October."}]` |
| PASS | prospective | judge: Did the assistant tell the customer where the follow-up will reach them (for example by secure message in the Kestrel app, which is the default when no channel is set), and NOT say that there is no channel, no way, or nowhere for the follow-up to be sent? | `{"verdict": "pass", "reason": "The assistant stated \"Where you'll hear back: secure message in the Kestrel app - no contact channel is set on your account, so that's the default\" and did not say there is no channel or  …` |

## cr-eli  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Hi, Eli, card ending 6610, ZIP 73301. Please dispute the November 1 CloudNest charge, I cancelled in October. How and where will I hear back about it?

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October."})` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-cd30b463", "due": "2026-12-04", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Dispute filed for the November 1 CloudNest Storage charge of $9.99 - case **C-5002**, now under review.

**How and where you'll hear back:** the automatic case follow-up is due **December 4, 2026**, and it will arrive as a **secure message in the Kestrel app**, since you have no contact channel (email/SMS) set. If you set one before then, the follow-up will go there instead. Disputes are currently reviewed in about 10 days.

If you find a cancellation reference or other proof from CloudNest, send it over and I can attach it to the case.

_Episode written:_ Conversation on 2026-11-24: The customer wanted the November 1 CloudNest charge disputed and asked how/where they’d hear back; the customer said they cancelled in October (not verified). Dispute filed for transaction T-4002, case C-5002, under review. Follow-up due December 4, 2026, via Kestrel app secure message; no contact channel is set, but a new one would be used. Reviews take about 10 days. Case outcomes: C-5002 under_review. Lesson: none

_Judge `cr-eli-channel`: **pass**, The assistant told the customer the follow-up "will arrive as a secure message in the Kestrel app" and did not say there is no channel, no way, or nowhere for it to be sent._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October."}]` |
| PASS | prospective | judge: Did the assistant tell the customer where the follow-up will reach them (for example by secure message in the Kestrel app, which is the default when no channel is set), and NOT say that there is no channel, no way, or nowhere for the follow-up to be sent? | `{"verdict": "pass", "reason": "The assistant told the customer the follow-up \"will arrive as a secure message in the Kestrel app\" and did not say there is no channel, no way, or nowhere for it to be sent.", "samples":  …` |

## cr-marco  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** Hi, Marco, card ending 8830, ZIP 10011. Please dispute the $240 FitPulse renewal from November 3, I cancelled in October. How and where will I hear back about it?

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "FitPulse"})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`
- `file_dispute({"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the FitPulse membership in October, before the November 3 renewal."})` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-2d319ad0", "due": "2026-11-22", "approval": "a Kestrel reviewer approves the message before it is sent", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** I'll verify you and find that charge.
Done - I filed it against the **$240.00 FitPulse Gym "annual membership renewal" posted November 3, 2026** (transaction T-2002).

- **Case id:** C-5003 - status: under review
- **Follow-up due:** November 22, 2026 (disputes are currently reviewed in about 10 days)
- **Where it reaches you:** a secure message in the Kestrel app - that's the default because no contact channel is set on your account. If you set an email or mobile number before then, the follow-up goes to the new channel instead.

One note: there's also an identical $240.00 FitPulse charge from November 3, 2025 in your history. I filed the 2026 renewal since that's the one matching "renewal" - tell me if you actually meant the older charge.

Want me to set up an email or SMS contact channel so the decision reaches you there?

_Episode written:_ Conversation on 2026-11-12: Customer asked to dispute a $240 FitPulse renewal for November 3, saying he cancelled in October (not verified), and asked how/where he'd hear back. Assistant verified him, filed transaction T-2002 as case C-5003 (under review), follow-up due November 22, 2026 via Kestrel app secure message by default; approval before sending. Assistant also noted identical 2025 charge. Case outcomes: C-5003 under_review. Lesson: When multiple identical merchant charges exist, confirm the intended transaction date/year before filing to avoid disputing the wrong charge.

_Judge `cr-marco-channel`: **pass**, The assistant stated, "Where it reaches you: a secure message in the Kestrel app - that's the default because no contact channel is set on your account," and did not say there is no channel, no way, or nowhere for the follow-up._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the FitPulse membership in October, before the November 3 renewal."}]` |
| PASS | prospective | judge: Did the assistant tell the customer where the follow-up will reach them (for example by secure message in the Kestrel app, which is the default when no channel is set), and NOT say that there is no channel, no way, or nowhere for the follow-up to be sent? | `{"verdict": "pass", "reason": "The assistant stated, \"Where it reaches you: a secure message in the Kestrel app - that's the default because no contact channel is set on your account,\" and did not say there is no chann …` |
