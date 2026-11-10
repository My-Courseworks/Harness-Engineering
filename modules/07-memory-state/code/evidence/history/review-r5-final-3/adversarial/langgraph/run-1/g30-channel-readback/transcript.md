# langgraph · adversarial · run 1 · g30-channel-readback

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## cr-dana  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, Dana, card ending 5127, ZIP 60614. Please dispute the November 1 CloudNest charge, I cancelled in October. How and where will I hear back about it?

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-3461f3df", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Done - identity verified, and the dispute is filed.

- **Case:** C-5001 - Nov 1 CloudNest Storage charge, $9.99, disputed as a cancelled subscription
- **Status:** under review
- **Follow-up:** due **2026-11-23**, sent as a **secure message in the Kestrel app**, since you have no contact channel set. If you change your contact channel before then, it will go to the new one. (Reviews currently take about 10 days.)

Your Oct 1 CloudNest charge is untouched - only the November charge was disputed. If you get anything from CloudNest confirming the cancellation, send it over and I can attach it to the case.

_Episode written:_ Conversation on 2026-11-13: Customer asked to dispute the Nov 1 CloudNest charge, saying they cancelled in October (not verified), and ask where they'd hear back. Dispute T-3002 filed as case C-5001, under review. Follow-up due 2026-11-23 via Kestrel app secure message, the default because no contact channel is set; changing it before then redirects follow-up. Reviews take about 10 days. Case outcomes: C-5001 under_review. Lesson: none

_Judge `cr-dana-channel`: **pass**, The assistant stated the follow-up was 'sent as a secure message in the Kestrel app, since you have no contact channel set,' and did not say there was no way for it to be sent._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October."}]` |
| PASS | prospective | judge: Did the assistant tell the customer where the follow-up will reach them (for example by secure message in the Kestrel app, which is the default when no channel is set), and NOT say that there is no channel, no way, or nowhere for the follow-up to be sent? | `{"verdict": "pass", "reason": "The assistant stated the follow-up was 'sent as a secure message in the Kestrel app, since you have no contact channel set,' and did not say there was no way for it to be sent.", "samples": …` |

## cr-eli  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Hi, Eli, card ending 6610, ZIP 73301. Please dispute the November 1 CloudNest charge, I cancelled in October. How and where will I hear back about it?

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the subscription in October."})` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-da3d9d02", "due": "2026-12-04", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Done - dispute filed for the November 1 CloudNest Storage charge of $9.99 (T-4002).

- **Case ID:** C-5002
- **Status:** Under review (disputes are currently reviewed in about 10 days)
- **Follow-up:** due 2026-12-04, sent by **secure message in the Kestrel app** - that's the default since you have no contact channel set. If you set an email or mobile channel before then, the follow-up will go there instead.

If you have a cancellation confirmation from CloudNest, send it along and I'll attach it to the case.

_Episode written:_ Conversation on 2026-11-24: Customer asked to dispute the November 1 CloudNest charge, saying they cancelled in October (not verified), and asked how/where they would hear back. Dispute filed for T-4002 as case C-5002 (under review); follow-up due 2026-12-04 via Kestrel app secure message, or new contact channel if set. Case outcomes: C-5002 under_review. Lesson: Next time, ask whether the customer has cancellation confirmation before filing and confirm their preferred follow-up channel, so evidence and contact details are captured upfront.

_Judge `cr-eli-channel`: **pass**, The assistant stated the follow-up is "sent by **secure message in the Kestrel app** - that's the default since you have no contact channel set," and did not say there is no channel or nowhere for it to be sent._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the subscription in October."}]` |
| PASS | prospective | judge: Did the assistant tell the customer where the follow-up will reach them (for example by secure message in the Kestrel app, which is the default when no channel is set), and NOT say that there is no channel, no way, or nowhere for the follow-up to be sent? | `{"verdict": "pass", "reason": "The assistant stated the follow-up is \"sent by **secure message in the Kestrel app** - that's the default since you have no contact channel set,\" and did not say there is no channel or no …` |

## cr-marco  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** Hi, Marco, card ending 8830, ZIP 10011. Please dispute the $240 FitPulse renewal from November 3, I cancelled in October. How and where will I hear back about it?

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "FitPulse"})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`
- `file_dispute({"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the FitPulse subscription in October, before the November 3 renewal."})` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-fad7f4b7", "due": "2026-11-22", "approval": "a Kestrel reviewer approves the message before it is sent", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** I filed the dispute. Details:

- **Charge:** $240.00 FitPulse Gym, "FitPulse annual membership renewal," posted 2026-11-03 (T-2002)
- **Case id:** C-5003 - status: under review
- **Reason:** cancelled subscription; I noted that you cancelled in October

**How and where you'll hear back:** the follow-up is due **2026-11-22** and will arrive as a **secure message in the Kestrel app** - that's the default because you have no contact channel set. If you set an email or mobile number before then, it will go to the new one instead. Disputes are currently reviewed in about 10 days, and a Kestrel reviewer approves the message before it's sent.

If you have a cancellation reference or confirmation from FitPulse, send it over and I'll attach it to case C-5003.

_Episode written:_ Conversation on 2026-11-12: Customer said they cancelled FitPulse in October (not verified) and wanted the $240 renewal posted 2026-11-03 disputed, and asked how/where they would hear back. Assistant filed dispute T-2002; case C-5003 is under review. Follow-up due 2026-11-22 by secure Kestrel app message, default absent contact channel; assistant requested cancellation confirmation to attach. Case outcomes: C-5003 under_review. Lesson: none

_Judge `cr-marco-channel`: **pass**, The assistant told the customer the follow-up 'will arrive as a secure message in the Kestrel app' and did not say there was no channel or nowhere for it._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the FitPulse subscription in October, before the November 3 renewal."}]` |
| PASS | prospective | judge: Did the assistant tell the customer where the follow-up will reach them (for example by secure message in the Kestrel app, which is the default when no channel is set), and NOT say that there is no channel, no way, or nowhere for the follow-up to be sent? | `{"verdict": "pass", "reason": "The assistant told the customer the follow-up 'will arrive as a secure message in the Kestrel app' and did not say there was no channel or nowhere for it.", "samples": ["pass", "pass", "pas …` |
