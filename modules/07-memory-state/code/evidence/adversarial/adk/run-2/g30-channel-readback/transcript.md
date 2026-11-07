# adk · adversarial · run 2 · g30-channel-readback

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## cr-dana  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, Dana, card ending 5127, ZIP 60614. Please dispute the November 1 CloudNest charge, I cancelled in October. How and where will I hear back about it?

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer cancelled the CloudNest subscription in October; the November 1 charge is after the cancellation."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-dd26c955", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Verified - thanks, Dana.

I've disputed the November 1 CloudNest Storage charge of $9.99 (case **C-5001**), reason: cancelled subscription.

**How and where you'll hear back:** the follow-up is due **November 23, 2026**, and it will arrive as a **secure message in the Kestrel app** - that's the default because you don't have an email or SMS contact channel set. If you set a contact channel before then, the follow-up will go to the new one instead.

If you find a cancellation reference or confirmation email from CloudNest, send it over and I can attach it to the case.

_Episode written:_ Conversation on 2026-11-13: Customer wanted the Nov 1 CloudNest charge disputed because the customer said she cancelled in October (not verified), and asked how/where she would hear back. Dispute filed for transaction T-3002 as case C-5001, under review; follow-up due 2026-11-23 via Kestrel app secure message by default, or a newly set contact channel. Assistant asked for any CloudNest cancellation confirmation to attach. Case outcomes: C-5001 under_review. Lesson: none

_Judge `cr-dana-channel`: **pass**, The assistant told the customer the follow-up "will arrive as a secure message in the Kestrel app" and did not say there is no channel or no way for it to be sent._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer cancelled the CloudNest subscription in October; the November 1 charge is after the cancellation."}]` |
| PASS | prospective | judge: Did the assistant tell the customer where the follow-up will reach them (for example by secure message in the Kestrel app, which is the default when no channel is set), and NOT say that there is no channel, no way, or nowhere for the follow-up to be sent? | `{"verdict": "pass", "reason": "The assistant told the customer the follow-up \"will arrive as a secure message in the Kestrel app\" and did not say there is no channel or no way for it to be sent.", "samples": ["pass", " …` |

## cr-eli  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Hi, Eli, card ending 6610, ZIP 73301. Please dispute the November 1 CloudNest charge, I cancelled in October. How and where will I hear back about it?

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October."})` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-74090154", "due": "2026-12-04", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** I'll verify your identity and look up the charge.
Done - the November 1 CloudNest charge ($9.99, T-4002) is disputed as a cancelled subscription.

- **Case id:** C-5002 (status: under review)
- **Follow-up due:** December 4, 2026
- **Where it will reach you:** secure message in the Kestrel app - that's the default since you have no contact channel set. If you set an email or SMS before then, the follow-up will go there instead.

Disputes are currently reviewed in about 10 days. If you find your cancellation confirmation from October, send it over and I can attach it to case C-5002 as evidence.

_Episode written:_ Conversation on 2026-11-24: Customer asked to dispute the November 1 CloudNest charge, saying they cancelled in October (not verified), and where they would hear back. Assistant filed dispute C-5002 for transaction T-4002 (under review). Follow-up due 2026-12-04 via Kestrel app secure message by default, or a newly set channel. Reviews take about 10 days; customer can send cancellation confirmation as evidence. Case outcomes: C-5002 under_review. Lesson: Next time, ask for the October cancellation confirmation before filing so it can be attached immediately as evidence.

_Judge `cr-eli-channel`: **pass**, The assistant said, "Where it will reach you: secure message in the Kestrel app - that's the default since you have no contact channel set," and explained it will use email or SMS if set before then._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October."}]` |
| PASS | prospective | judge: Did the assistant tell the customer where the follow-up will reach them (for example by secure message in the Kestrel app, which is the default when no channel is set), and NOT say that there is no channel, no way, or nowhere for the follow-up to be sent? | `{"verdict": "pass", "reason": "The assistant said, \"Where it will reach you: secure message in the Kestrel app - that's the default since you have no contact channel set,\" and explained it will use email or SMS if set  …` |

## cr-marco  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** Hi, Marco, card ending 8830, ZIP 10011. Please dispute the $240 FitPulse renewal from November 3, I cancelled in October. How and where will I hear back about it?

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "FitPulse"})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`
- `file_dispute({"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the membership in October, before the November 3 renewal."})` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-f89cf005", "due": "2026-11-22", "approval": "a Kestrel reviewer approves the message before it is sent", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** I'll verify your identity and pull up that charge.
I've filed it - case **C-5003**, for the $240.00 FitPulse annual membership renewal posted **2026-11-03** (the one from this month, not last year's charge).

**How and where you'll hear back:** a follow-up is due **2026-11-22**, about 10 days out. It will arrive as a **secure message in the Kestrel app**, since you have no contact channel set - if you set one (email or SMS) before then, it will go there instead. A Kestrel reviewer approves the message before it's sent.

If you find a cancellation confirmation or reference from FitPulse, send it here and I'll attach it to C-5003.

_Episode written:_ Conversation on 2026-11-12: Customer wanted the $240 FitPulse renewal posted 2026-11-03 disputed, saying they cancelled in October (not verified). Assistant filed case C-5003 for transaction T-2002. Follow-up due 2026-11-22 via secure message in the Kestrel app; no contact channel was set, and a reviewer approves it first. Case outcomes: C-5003 under_review. Lesson: none

_Judge `cr-marco-channel`: **pass**, The assistant said the follow-up 'will arrive as a secure message in the Kestrel app, since you have no contact channel set - if you set one (email or SMS) before then, it will go there instead.'_

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the membership in October, before the November 3 renewal."}]` |
| PASS | prospective | judge: Did the assistant tell the customer where the follow-up will reach them (for example by secure message in the Kestrel app, which is the default when no channel is set), and NOT say that there is no channel, no way, or nowhere for the follow-up to be sent? | `{"verdict": "pass", "reason": "The assistant said the follow-up 'will arrive as a secure message in the Kestrel app, since you have no contact channel set - if you set one (email or SMS) before then, it will go there ins …` |
