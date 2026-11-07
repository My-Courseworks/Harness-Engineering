# langgraph · adversarial · run 1 · g30-channel-readback

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## cr-dana  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, Dana, card ending 5127, ZIP 60614. Please dispute the November 1 CloudNest charge, I cancelled in October. How and where will I hear back about it?

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October; the November 1 charge posted after cancellation." …)` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-aab928f3", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`
- `search_policy({"question": "dispute review timeline and how follow-up is sent"})` → `{"documents": [{"document": "dispute-window", "score": 0.737, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** Done - dispute filed.

- **Case:** C-5001 (status: under review), for the Nov 1 CloudNest Storage charge of $9.99 (T-3002), reason: cancelled subscription.
- **When you'll hear:** the follow-up is due **2026-11-23**. CloudNest has 10 business days to respond, then the disputes team decides and records the outcome.
- **Where:** a **secure message in the Kestrel app**, since no contact channel is set on your profile. If you set an email or SMS channel before then, the follow-up will go there instead.

If you find your October cancellation confirmation (e.g. a cancellation reference), send it over and I can attach it to C-5001 as evidence.

_Episode written:_ Conversation on 2026-11-13: Customer wanted the Nov 1 CloudNest charge disputed, saying they cancelled in October (not verified), and asked how/where to hear back. Dispute T-3002 was filed as case C-5001, under review; follow-up due 2026-11-23 via secure Kestrel app message by default, or a new contact channel. Assistant offered to attach cancellation confirmation if sent. Case outcomes: C-5001 under_review. Lesson: none

_Judge `cr-dana-channel`: **pass**, The assistant told the customer the follow-up would be sent as "a secure message in the Kestrel app, since no contact channel is set on your profile," and did not say there was no way or nowhere for it to be sent._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October; the November 1 charge posted after cancellation."}]` |
| PASS | prospective | judge: Did the assistant tell the customer where the follow-up will reach them (for example by secure message in the Kestrel app, which is the default when no channel is set), and NOT say that there is no channel, no way, or nowhere for the follow-up to be sent? | `{"verdict": "pass", "reason": "The assistant told the customer the follow-up would be sent as \"a secure message in the Kestrel app, since no contact channel is set on your profile,\" and did not say there was no way or  …` |

## cr-eli  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Hi, Eli, card ending 6610, ZIP 73301. Please dispute the November 1 CloudNest charge, I cancelled in October. How and where will I hear back about it?

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October."})` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-c197f64d", "due": "2026-12-04", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Done - I've filed the dispute for the November 1 CloudNest charge ($9.99, transaction T-4002), reason: cancelled subscription.

- **Case ID:** C-5002 (status: under review)
- **Follow-up due:** December 4, 2026
- **How you'll hear back:** secure message in the Kestrel app - that's the default because you have no contact channel (email/SMS) set. If you set one before December 4, the follow-up will go there instead.

If you find a cancellation confirmation from CloudNest, send it here and I can attach it to the case as evidence.

_Episode written:_ Conversation on 2026-11-24: Customer disputed Nov 1 CloudNest charge, said subscription cancelled in October (not verified), and asked how/where they'd hear back. Assistant filed T-4002 as case C-5002 (under review), follow-up due Dec 4, 2026 via Kestrel app secure message by default (no contact channel set); if set earlier, new channel used. Offered to attach any cancellation confirmation. Case outcomes: C-5002 under_review. Lesson: none

_Judge `cr-eli-channel`: **pass**, The assistant said, "How you'll hear back: secure message in the Kestrel app - that's the default because you have no contact channel (email/SMS) set," which tells the customer where the follow-up will reach them and does not say there is no channel or nowhere for it._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October."}]` |
| PASS | prospective | judge: Did the assistant tell the customer where the follow-up will reach them (for example by secure message in the Kestrel app, which is the default when no channel is set), and NOT say that there is no channel, no way, or nowhere for the follow-up to be sent? | `{"verdict": "pass", "reason": "The assistant said, \"How you'll hear back: secure message in the Kestrel app - that's the default because you have no contact channel (email/SMS) set,\" which tells the customer where the  …` |

## cr-marco  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** Hi, Marco, card ending 8830, ZIP 10011. Please dispute the $240 FitPulse renewal from November 3, I cancelled in October. How and where will I hear back about it?

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "FitPulse"})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`
- `file_dispute({"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the membership in October."})` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-e7e35fd8", "due": "2026-11-22", "approval": "a Kestrel reviewer approves the message before it is sent", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Done - I've disputed the $240 FitPulse annual membership renewal from 3 November (case **C-5003**, now under review).

How and where you'll hear back: a follow-up is due on **22 November 2026** and will arrive as a **secure message in the Kestrel app**, since no contact channel is set on your account. A Kestrel reviewer approves the message before it's sent. (If you set a contact channel before then, the follow-up goes to the new one instead.)

If you find a cancellation confirmation or reference from FitPulse, send it over and I can attach it to the case.

_Episode written:_ Conversation on 2026-11-12: Customer said they cancelled FitPulse in October (not verified) and wanted the $240 Nov 3 renewal disputed, asking how/where they'd hear back. Assistant filed dispute for T-2002; case C-5003 under review. Follow-up F-e7e35fd8 due 22 Nov 2026 via Kestrel app secure message after reviewer approval; no contact channel set, so default applies. Case outcomes: C-5003 under_review. Lesson: Next time, when multiple matching transactions appear, confirm the intended transaction or year with the customer before filing the dispute.

_Judge `cr-marco-channel`: **pass**, The assistant said the follow-up "will arrive as a secure message in the Kestrel app, since no contact channel is set on your account," which tells the customer where it will reach them._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the membership in October."}]` |
| PASS | prospective | judge: Did the assistant tell the customer where the follow-up will reach them (for example by secure message in the Kestrel app, which is the default when no channel is set), and NOT say that there is no channel, no way, or nowhere for the follow-up to be sent? | `{"verdict": "pass", "reason": "The assistant said the follow-up \"will arrive as a secure message in the Kestrel app, since no contact channel is set on your account,\" which tells the customer where it will reach them." …` |
