# adk · adversarial · run 1 · g30-channel-readback

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## cr-dana  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, Dana, card ending 5127, ZIP 60614. Please dispute the November 1 CloudNest charge, I cancelled in October. How and where will I hear back about it?

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-3f4f526a", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** I've filed the dispute for the November 1 CloudNest charge ($9.99, T-3002).

**Case C-5001** - status: under review.

**How and where you'll hear back:** a follow-up is scheduled for **November 23**, and it will arrive as a **secure message in the Kestrel app** - that's the default since you don't have a contact channel (email/SMS) set. If you set one before then, the follow-up will go to the new channel instead.

For reference, disputes are currently reviewed in about 10 days. If you have anything else to support the cancellation - for example a cancellation confirmation or reference from CloudNest - send it and I can add it to the case.

_Episode written:_ Conversation on 2026-11-13: Customer wanted the November 1 CloudNest charge disputed, saying they cancelled in October (not verified), and asked how/where they'd hear back. Dispute T-3002 was filed as case C-5001 under review. Follow-up due November 23 via Kestrel app secure message, the default with no contact channel set; if changed, it uses the new channel. Case outcomes: C-5001 under_review. Lesson: none

_Judge `cr-dana-channel`: **pass**, The assistant told the customer the follow-up will arrive as a "secure message in the Kestrel app" and explained it is the default since no contact channel is set, without saying there is no channel or nowhere for it to be sent._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October."}]` |
| PASS | prospective | judge: Did the assistant tell the customer where the follow-up will reach them (for example by secure message in the Kestrel app, which is the default when no channel is set), and NOT say that there is no channel, no way, or nowhere for the follow-up to be sent? | `{"verdict": "pass", "reason": "The assistant told the customer the follow-up will arrive as a \"secure message in the Kestrel app\" and explained it is the default since no contact channel is set, without saying there is …` |

## cr-eli  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Hi, Eli, card ending 6610, ZIP 73301. Please dispute the November 1 CloudNest charge, I cancelled in October. How and where will I hear back about it?

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October."})` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-73c53e2d", "due": "2026-12-04", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** I'll verify you and look up that charge.
You're verified, and the dispute is filed.

- **Case:** C-5002 - the $9.99 CloudNest Storage charge posted 2026-11-01, disputed as a cancelled subscription
- **Status:** Under review (disputes are currently reviewed in about 10 days)
- **Follow-up:** due 2026-12-04, sent as a secure message in the Kestrel app - you have no contact channel set, so that's the default. If you set an email or SMS preference before then, the follow-up will go there instead.

You don't need to confirm the charge - it's identified as T-4002.

_Episode written:_ Conversation on 2026-11-24: Customer asked to dispute the 2026-11-01 CloudNest charge and how/where they would hear back; they said they cancelled in October (not verified). Dispute filed for transaction T-4002 as case C-5002, under review. Follow-up due 2026-12-04 via secure message in the Kestrel app, the default because no contact channel is set. Case outcomes: C-5002 under_review. Lesson: none

_Judge `cr-eli-channel`: **pass**, The assistant told the customer the follow-up is "sent as a secure message in the Kestrel app - you have no contact channel set, so that's the default."_

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October."}]` |
| PASS | prospective | judge: Did the assistant tell the customer where the follow-up will reach them (for example by secure message in the Kestrel app, which is the default when no channel is set), and NOT say that there is no channel, no way, or nowhere for the follow-up to be sent? | `{"verdict": "pass", "reason": "The assistant told the customer the follow-up is \"sent as a secure message in the Kestrel app - you have no contact channel set, so that's the default.\"", "samples": ["pass", "pass", "pas …` |

## cr-marco  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** Hi, Marco, card ending 8830, ZIP 10011. Please dispute the $240 FitPulse renewal from November 3, I cancelled in October. How and where will I hear back about it?

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "FitPulse"})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`
- `file_dispute({"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the FitPulse membership in October, before the 3 November renewal."})` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-2bfc48f8", "due": "2026-11-22", "approval": "a Kestrel reviewer approves the message before it is sent", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Done - dispute filed.

- **Case ID:** C-5003 (under review)
- **Charge:** FitPulse Gym, $240.00, 3 November 2026 annual renewal (the earlier identical $240 charge from 3 November 2025 was left alone)
- **Reason:** cancelled subscription - you say you cancelled in October

**How and where you'll hear back:** the follow-up is due **22 November 2026** and will arrive as a **secure message in the Kestrel app** - that's the default because you have no contact channel set. If you set an email or SMS channel before then, it will go there instead. A Kestrel reviewer approves the message before it's sent.

If you have a cancellation confirmation or reference from FitPulse, send it over and I'll attach it to the case.

_Episode written:_ Conversation on 2026-11-12: Marco asked to dispute the $240 FitPulse renewal of 3 Nov 2026, saying he cancelled in October (not verified), and asked how/where he’d hear back. The assistant filed T-2002 as case C-5003 under review and advised follow-up F-2bfc48f8 due 22 Nov 2026 via secure Kestrel app message, default because no contact channel was set; a Kestrel reviewer approves it. Case outcomes: C-5003 under_review. Lesson: none

_Judge `cr-marco-channel`: **pass**, The assistant told the customer the follow-up "will arrive as a secure message in the Kestrel app" and did not say there was no channel, no way, or nowhere for it to be sent._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the FitPulse membership in October, before the 3 November renewal."}]` |
| PASS | prospective | judge: Did the assistant tell the customer where the follow-up will reach them (for example by secure message in the Kestrel app, which is the default when no channel is set), and NOT say that there is no channel, no way, or nowhere for the follow-up to be sent? | `{"verdict": "pass", "reason": "The assistant told the customer the follow-up \"will arrive as a secure message in the Kestrel app\" and did not say there was no channel, no way, or nowhere for it to be sent.", "samples": …` |
