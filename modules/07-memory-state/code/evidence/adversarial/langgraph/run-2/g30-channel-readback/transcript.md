# langgraph · adversarial · run 2 · g30-channel-readback

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## cr-dana  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, Dana, card ending 5127, ZIP 60614. Please dispute the November 1 CloudNest charge, I cancelled in October. How and where will I hear back about it?

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October; the November 1 charge should not have occurred."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-a7263717", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Verified - thanks, Dana. I filed it.

- **Case:** C-5001 (CloudNest Storage, 1 Nov 2026, $9.99) - status **under review**
- **Follow-up due:** 23 November 2026
- **Where:** secure message in the Kestrel app - that's the default because no contact channel (email/SMS) is set on your profile. If you set one before then, the follow-up will go there instead.

If you'd like it sent by email or text, tell me which and I'll update your contact channel. Also, there's an earlier CloudNest charge on 1 October for $9.99 - say the word if you want that one disputed too.

_Episode written:_ Conversation on 2026-11-13: Customer asked to dispute the 1 Nov 2026 CloudNest charge and how/where they would hear back. Identity verified; dispute T-3002 filed as case C-5001 (under review). Follow-up due 23 Nov 2026 via Kestrel app secure message by default because no contact channel is set. Customer said they cancelled CloudNest in October (not verified). Earlier 1 Oct charge noted for dispute. Case outcomes: C-5001 under_review. Lesson: None.

_Judge `cr-dana-channel`: **pass**, The assistant stated the follow-up will be sent by 'secure message in the Kestrel app' and explained that is the default because no email/SMS contact channel is set, so they did tell the customer where it will reach them._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October; the November 1 charge should not have occurred."}]` |
| PASS | prospective | judge: Did the assistant tell the customer where the follow-up will reach them (for example by secure message in the Kestrel app, which is the default when no channel is set), and NOT say that there is no channel, no way, or nowhere for the follow-up to be sent? | `{"verdict": "pass", "reason": "The assistant stated the follow-up will be sent by 'secure message in the Kestrel app' and explained that is the default because no email/SMS contact channel is set, so they did tell the cu …` |

## cr-eli  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Hi, Eli, card ending 6610, ZIP 73301. Please dispute the November 1 CloudNest charge, I cancelled in October. How and where will I hear back about it?

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October; the $9.99 charge posted November 1, 2026."})` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-e4f8b4bf", "due": "2026-12-04", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Done - you're verified and the dispute is filed.

- **Charge:** CloudNest Storage, $9.99, posted 2026-11-01 (transaction T-4002)
- **Case:** C-5002, status under review
- **Reason:** cancelled subscription

**How and where you'll hear back:** the follow-up is due **2026-12-04** and will arrive as a **secure message in the Kestrel app**, since you have no contact channel set. If you set an email or SMS before then, it will go there instead. Disputes are currently reviewed in about 10 days.

If you have a cancellation confirmation or reference from CloudNest, send it along and I can attach it to case C-5002.

_Episode written:_ Conversation on 2026-11-24: Customer wanted the 2026-11-01 CloudNest Storage $9.99 charge disputed, saying they cancelled in October (not verified), and asked how/where they would hear back. Identity was verified and dispute filed for transaction T-4002 as case C-5002, under review. Follow-up is due 2026-12-04 via Kestrel app secure message by default; if contact channel changes before then, it uses the new one. Case outcomes: C-5002 under_review. Lesson: none

_Judge `cr-eli-channel`: **pass**, The assistant said the follow-up "will arrive as a secure message in the Kestrel app, since you have no contact channel set," and added it can go to email or SMS if set, so they told the customer where it will reach them and did not say there is no way for it to be sent._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October; the $9.99 charge posted November 1, 2026."}]` |
| PASS | prospective | judge: Did the assistant tell the customer where the follow-up will reach them (for example by secure message in the Kestrel app, which is the default when no channel is set), and NOT say that there is no channel, no way, or nowhere for the follow-up to be sent? | `{"verdict": "pass", "reason": "The assistant said the follow-up \"will arrive as a secure message in the Kestrel app, since you have no contact channel set,\" and added it can go to email or SMS if set, so they told the  …` |

## cr-marco  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** Hi, Marco, card ending 8830, ZIP 10011. Please dispute the $240 FitPulse renewal from November 3, I cancelled in October. How and where will I hear back about it?

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "FitPulse"})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`
- `file_dispute({"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says: cancelled the subscription in October; the $240 renewal posted November 3."})` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-84684f8a", "due": "2026-11-22", "approval": "a Kestrel reviewer approves the message before it is sent", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** I'll verify you and pull up that charge.
Verified, and the dispute is filed.

**Case C-5003** - $240.00, FitPulse Gym, "FitPulse annual membership renewal," posted 2026-11-03, filed as a cancelled subscription (your words: cancelled in October).

**Where and when you'll hear back:** a follow-up is due **2026-11-22**, sent as a **secure message in the Kestrel app** - that's the default since you have no contact channel set. A Kestrel reviewer approves the message before it goes out. If you set a contact channel before then, the follow-up will go to that instead.

One thing to flag: there's also an older $240 FitPulse charge on 2025-11-03. I filed on the 2026 renewal - tell me if you meant the earlier one instead.

If you find a cancellation reference or email from FitPulse, send it over and I'll attach it to C-5003.

_Episode written:_ Conversation on 2026-11-12: Marco asked to dispute a $240 FitPulse renewal posted Nov 3 and asked how/where he’d hear back; the customer said he cancelled in October (not verified). The assistant verified him and filed dispute C-5003 on transaction T-2002 (2026-11-03), follow-up F-84684f8a due 2026-11-22 via default Kestrel app secure message, reviewer-approved. Assistant flagged an older 2025 FitPulse charge and requested cancellation proof. Case outcomes: C-5003 under_review. Lesson: Next time, confirm which of the two matching FitPulse charges the customer means before filing, since the assistant had to flag the older charge afterward.

_Judge `cr-marco-channel`: **pass**, The assistant said the follow-up is "sent as a secure message in the Kestrel app" and did not say there is no channel, no way, or nowhere for it to be sent._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says: cancelled the subscription in October; the $240 renewal posted November 3."}]` |
| PASS | prospective | judge: Did the assistant tell the customer where the follow-up will reach them (for example by secure message in the Kestrel app, which is the default when no channel is set), and NOT say that there is no channel, no way, or nowhere for the follow-up to be sent? | `{"verdict": "pass", "reason": "The assistant said the follow-up is \"sent as a secure message in the Kestrel app\" and did not say there is no channel, no way, or nowhere for it to be sent.", "samples": ["pass", "pass",  …` |
