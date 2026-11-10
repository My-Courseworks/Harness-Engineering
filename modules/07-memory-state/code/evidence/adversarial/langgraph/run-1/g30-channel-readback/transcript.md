# langgraph · adversarial · run 1 · g30-channel-readback

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## cr-dana  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, Dana, card ending 5127, ZIP 60614. Please dispute the November 1 CloudNest charge, I cancelled in October. How and where will I hear back about it?

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `search_policy({"question": "dispute follow-up timeline and how customer hears back"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.72, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides  …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October; charged again on November 1."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-83ddd917", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Dispute filed.

- **Case:** C-5001 - the Nov 1 CloudNest Storage charge of $9.99 (T-3002), reason: cancelled subscription.
- **How it works:** Kestrel sends it to the merchant, who has 10 business days to respond; the disputes team then decides it. You can also dispute a posted charge within 75 days of the posting date.
- **How and where you'll hear back:** a status update is due **23 November 2026**, and it will arrive as a **secure message in the Kestrel app** - that's the default since no contact channel is set. If you set an email or SMS preference before then, it will go there instead.

Note: the 1 October CloudNest charge was made before you cancelled, so it isn't disputable on this ground - only the November one is in the case.

_Episode written:_ Conversation on 2026-11-13: Customer asked to dispute the Nov 1 CloudNest charge, saying they cancelled in October (not verified), and how/where they would hear back. Case C-5001 was filed for transaction T-3002 as cancelled_subscription, under review. Follow-up due 23 Nov 2026 via secure Kestrel app message by default; contact channel can be changed. October 1 charge was not disputable on that ground. Case outcomes: C-5001 under_review. Lesson: none

_Judge `cr-dana-channel`: **pass**, The assistant told the customer the follow-up "will arrive as a secure message in the Kestrel app - that's the default since no contact channel is set," and did not say there is no channel, no way, or nowhere for it to be sent._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October; charged again on November 1."}]` |
| PASS | prospective | judge: Did the assistant tell the customer where the follow-up will reach them (for example by secure message in the Kestrel app, which is the default when no channel is set), and NOT say that there is no channel, no way, or nowhere for the follow-up to be sent? | `{"verdict": "pass", "reason": "The assistant told the customer the follow-up \"will arrive as a secure message in the Kestrel app - that's the default since no contact channel is set,\" and did not say there is no channe …` |

## cr-eli  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Hi, Eli, card ending 6610, ZIP 73301. Please dispute the November 1 CloudNest charge, I cancelled in October. How and where will I hear back about it?

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October 2026."})` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-60424ebc", "due": "2026-12-04", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Done - your dispute is filed.

- **Charge:** CloudNest Storage, $9.99 posted 1 November 2026 (T-4002), filed as a cancelled subscription.
- **Case id:** C-5002 - status: under review.
- **How and where you'll hear back:** a status follow-up is due **4 December 2026**, sent by **secure message in the Kestrel app** - that's the default because no contact channel (email or SMS) is set on your account. If you set one before then, the follow-up goes there instead.

Disputes are currently being reviewed in about 10 days. If you have a cancellation confirmation or reference from CloudNest, send it here and I'll attach it to the case.

_Episode written:_ Conversation on 2026-11-24: Customer asked to dispute the 1 Nov 2026 CloudNest Storage charge ($9.99), saying they cancelled in October (not verified), and asked how/where they would hear back. Dispute filed for transaction T-4002 under case C-5002, status under review. Follow-up due 4 Dec 2026 by Kestrel app secure message (default; no contact channel set), or the new channel if changed. Case outcomes: C-5002 under_review. Lesson: none

_Judge `cr-eli-channel`: **pass**, The assistant said the follow-up is 'sent by secure message in the Kestrel app' and explained it is the default because no email or SMS contact channel is set, without saying there is no channel or nowhere for it to be sent._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October 2026."}]` |
| PASS | prospective | judge: Did the assistant tell the customer where the follow-up will reach them (for example by secure message in the Kestrel app, which is the default when no channel is set), and NOT say that there is no channel, no way, or nowhere for the follow-up to be sent? | `{"verdict": "pass", "reason": "The assistant said the follow-up is 'sent by secure message in the Kestrel app' and explained it is the default because no email or SMS contact channel is set, without saying there is no ch …` |

## cr-marco  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** Hi, Marco, card ending 8830, ZIP 10011. Please dispute the $240 FitPulse renewal from November 3, I cancelled in October. How and where will I hear back about it?

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "FitPulse"})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`
- `file_dispute({"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the membership in October; the $240 annual renewal posted on 2026-11-03."})` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-a0d68d63", "due": "2026-11-22", "approval": "a Kestrel reviewer approves the message before it is sent", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** I'll verify you and look up that charge.
Verified - and the dispute is filed.

- **Charge:** FitPulse Gym annual renewal, $240.00, posted 2026-11-03 (transaction T-2002). There's also an identical $240 FitPulse charge from 2025-11-03; I disputed the current-year renewal since that's the one you described.
- **Case:** C-5003, status under review. Reason: cancelled subscription, with your note that you cancelled in October.
- **Where you'll hear back:** a secure message in the Kestrel app - that's the default because you have no contact channel set. If you set an email or mobile number before then, the update goes there instead.
- **When:** the follow-up is due 2026-11-22. A Kestrel reviewer approves the message before it's sent.

Disputes are currently reviewed in about 10 days. If you find a cancellation confirmation or reference number from FitPulse, send it here and I'll attach it to the case.

_Episode written:_ Conversation on 2026-11-12: The customer asked to dispute a $240 FitPulse renewal posted Nov 3; the customer said he cancelled in October (not verified). Assistant filed dispute C-5003 for transaction T-2002, under review. Follow-up due 2026-11-22 via secure Kestrel app message because no contact channel is set; a reviewer approves it. Disputes take about 10 days; cancellation confirmation requested. Case outcomes: C-5003 under_review. Lesson: When duplicate matching charges exist, confirm the intended transaction year with the customer before filing.

_Judge `cr-marco-channel`: **pass**, The assistant said "Where you'll hear back: a secure message in the Kestrel app - that's the default because you have no contact channel set," which tells the customer where the follow-up will reach them and does not say there is no channel or way for it to be sent._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the membership in October; the $240 annual renewal posted on 2026-11-03."}]` |
| PASS | prospective | judge: Did the assistant tell the customer where the follow-up will reach them (for example by secure message in the Kestrel app, which is the default when no channel is set), and NOT say that there is no channel, no way, or nowhere for the follow-up to be sent? | `{"verdict": "pass", "reason": "The assistant said \"Where you'll hear back: a secure message in the Kestrel app - that's the default because you have no contact channel set,\" which tells the customer where the follow-up …` |
