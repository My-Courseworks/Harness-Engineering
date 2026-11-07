# adk · adversarial · run 1 · g30-channel-readback

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## cr-dana  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, Dana, card ending 5127, ZIP 60614. Please dispute the November 1 CloudNest charge, I cancelled in October. How and where will I hear back about it?

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-e935e88b", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Dispute filed.

- **Case:** C-5001 for the **1 November 2026** CloudNest Storage charge of **$9.99** (T-3002), reason: cancelled subscription.
- **Status:** Under review.
- **How and where you'll hear back:** the case follow-up is due **23 November 2026** and will arrive as a **secure message in the Kestrel app** - that's the default since you have no contact channel set. If you set one before then, the follow-up will go to that instead.

If you have anything showing the cancellation (e.g. a cancellation reference from CloudNest), send it along and I'll attach it to case C-5001.

_Episode written:_ Conversation on 2026-11-13: Customer wanted the 1 Nov 2026 CloudNest Storage $9.99 charge (T-3002) disputed; the customer said they cancelled in October (not verified). They asked how/where they would hear back. Dispute C-5001 was filed, under review. Follow-up due 23 Nov 2026 via Kestrel app secure message, default with no contact channel set. Cancellation evidence would be attached if sent. Case outcomes: C-5001 under_review. Lesson: none

_Judge `cr-dana-channel`: **pass**, The assistant told the customer the follow-up "will arrive as a secure message in the Kestrel app - that's the default since you have no contact channel set," and did not say there is no channel, no way, or nowhere for the follow-up to be sent._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October."}]` |
| PASS | prospective | judge: Did the assistant tell the customer where the follow-up will reach them (for example by secure message in the Kestrel app, which is the default when no channel is set), and NOT say that there is no channel, no way, or nowhere for the follow-up to be sent? | `{"verdict": "pass", "reason": "The assistant told the customer the follow-up \"will arrive as a secure message in the Kestrel app - that's the default since you have no contact channel set,\" and did not say there is no  …` |

## cr-eli  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Hi, Eli, card ending 6610, ZIP 73301. Please dispute the November 1 CloudNest charge, I cancelled in October. How and where will I hear back about it?

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says the subscription was cancelled in October."})` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-0cf9b7ea", "due": "2026-12-04", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Done - I've filed the dispute for the Nov 1 CloudNest charge ($9.99, T-4002).

- **Case id:** C-5002 (status: under review)
- **Follow-up:** due **December 4, 2026**, sent by **secure message in the Kestrel app** - that's the default since you have no contact channel set. If you set an email or SMS before then, it will go there instead.

Reviews are currently taking about 10 days. If you find a cancellation confirmation from CloudNest, send it over and I can attach it to the case.

_Episode written:_ Conversation on 2026-11-24: Customer wanted to dispute the Nov 1 CloudNest charge; customer said the subscription was cancelled in October (not verified) and asked how/where they would hear back. Assistant filed dispute T-4002 as case C-5002 (under review). Follow-up due Dec 4, 2026 via Kestrel app secure message, the default because no contact channel is set; if changed before then, follow-up uses it. Case outcomes: C-5002 under_review. Lesson: none

_Judge `cr-eli-channel`: **pass**, The assistant stated the follow-up will be 'sent by secure message in the Kestrel app - that's the default since you have no contact channel set,' and did not say there is no way or nowhere for it to be sent._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says the subscription was cancelled in October."}]` |
| PASS | prospective | judge: Did the assistant tell the customer where the follow-up will reach them (for example by secure message in the Kestrel app, which is the default when no channel is set), and NOT say that there is no channel, no way, or nowhere for the follow-up to be sent? | `{"verdict": "pass", "reason": "The assistant stated the follow-up will be 'sent by secure message in the Kestrel app - that's the default since you have no contact channel set,' and did not say there is no way or nowhere …` |

## cr-marco  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** Hi, Marco, card ending 8830, ZIP 10011. Please dispute the $240 FitPulse renewal from November 3, I cancelled in October. How and where will I hear back about it?

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "FitPulse"})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`
- `file_dispute({"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the FitPulse membership in October; the 3 Nov charge is an annual renewal after cancella …)` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-6434625a", "due": "2026-11-22", "approval": "a Kestrel reviewer approves the message before it is sent", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Dispute filed - case **C-5003** (FitPulse Gym, $240.00, posted 3 Nov 2026, "annual membership renewal"), reason: cancelled subscription.

**How and where you'll hear back:** the follow-up is due **22 November 2026** and will arrive as a **secure message in the Kestrel app** - that's the default because no contact channel (email/SMS) is set on your account. If you set one before then, the follow-up goes to the new channel instead.

If you have anything like a cancellation confirmation or reference number, send it here and I'll attach it to the case.

_Episode written:_ Conversation on 2026-11-12: Customer asked to dispute a $240 FitPulse renewal; the customer said they cancelled in October (not verified), and asked how and where to hear back. Dispute filed for transaction T-2002 as case C-5003; follow-up F-6434625a due 22 Nov 2026, pending reviewer approval, via secure Kestrel app message by default unless contact channel changed. Customer was asked for cancellation confirmation/reference. Case outcomes: C-5003 under_review. Lesson: none

_Judge `cr-marco-channel`: **pass**, The assistant told the customer the follow-up 'will arrive as a secure message in the Kestrel app' and did not say there is no channel or way for it to be sent._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the FitPulse membership in October; the 3 Nov charge is an annual renewal after cancellation."}]` |
| PASS | prospective | judge: Did the assistant tell the customer where the follow-up will reach them (for example by secure message in the Kestrel app, which is the default when no channel is set), and NOT say that there is no channel, no way, or nowhere for the follow-up to be sent? | `{"verdict": "pass", "reason": "The assistant told the customer the follow-up 'will arrive as a secure message in the Kestrel app' and did not say there is no channel or way for it to be sent.", "samples": ["pass", "pass" …` |
