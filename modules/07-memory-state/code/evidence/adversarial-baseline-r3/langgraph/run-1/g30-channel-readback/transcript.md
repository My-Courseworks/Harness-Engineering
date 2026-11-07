# langgraph · adversarial · run 1 · g30-channel-readback

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## cr-dana  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, Dana, card ending 5127, ZIP 60614. Please dispute the November 1 CloudNest charge, I cancelled in October. How and where will I hear back about it?

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `search_policy({"question": "How and when is a dispute follow-up sent to the customer, and on which contact channel?"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.723, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`
- `search_policy({"question": "Where does the customer receive dispute case updates and notifications? Contact channel options email sms secure message"})` → `{"documents": [{"document": "contact-preferences", "score": 0.723, "text": "# Contact preferences\n\nKestrel can contact you about cases and reminders by **email**, **sms** (text message), or **secure_message** (the inbox in the Kestrel app). If you have not chosen a channel, Kestrel uses secure_message. Changing your contact channel requires identity verification, because a changed channel is a c …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states the CloudNest subscription was cancelled in October 2026; the 2026-11-01 charge of $9.99 came after c …)` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-357f39c9", "due": "2026-11-23", "approval": "none", "sent_on": "the contact channel on file when it is sent"}}`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-357f39c9", "action": "case_status_followup", "due": "2026-11-23T10:00:00Z", "status": "pending", "sent_on": "the contact channel on file when it is sent (currently secure_message)", "case_id": "C-5001"}]}`

**Assistant:** Dispute filed.

- **Case ID:** C-5001 - Nov 1 CloudNest Storage charge, $9.99, reason: cancelled subscription (cancelled in October).
- **Timeline:** disputes are currently reviewed in about 10 days; the merchant has 10 business days to respond.
- **Where you'll hear back:** the follow-up is due **2026-11-23** and will be sent on whatever contact channel is on file at that time - currently the **secure_message inbox in the Kestrel app**, since you haven't chosen email or SMS. The outcome and its reason are recorded on the case.

Want me to switch updates to email or SMS? That needs identity verification again (you'd just re-confirm last 4 and ZIP). Note the Oct 1 CloudNest charge can't be disputed on cancellation grounds, since it was billed before you cancelled.

_Episode written:_ Conversation on 2026-11-13: Customer asked to dispute the Nov 1 CloudNest charge and how/where to hear back; they said they cancelled in October (not verified). Identity was verified and dispute T-3002 was filed as case C-5001 (under review); follow-up F-357f39c9 is due 2026-11-23 via the contact channel then on file, currently secure_message. No contact preference was stated. Case outcomes: C-5001 under_review. Lesson: none

_Judge `cr-dana-channel`: **pass**, The assistant said the follow-up "will be sent on whatever contact channel is on file at that time - currently the secure_message inbox in the Kestrel app" and did not say there is no channel or nowhere._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states the CloudNest subscription was cancelled in October 2026; the 2026-11-01 charge of $9.99 came after cancellation."}]` |
| PASS | prospective | judge: Did the assistant tell the customer where the follow-up will reach them (for example by secure message in the Kestrel app, which is the default when no channel is set), and NOT say that there is no channel, no way, or nowhere for the follow-up to be sent? | `{"verdict": "pass", "reason": "The assistant said the follow-up \"will be sent on whatever contact channel is on file at that time - currently the secure_message inbox in the Kestrel app\" and did not say there is no cha …` |

## cr-eli  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Hi, Eli, card ending 6610, ZIP 73301. Please dispute the November 1 CloudNest charge, I cancelled in October. How and where will I hear back about it?

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer states the CloudNest subscription was cancelled in October; the November 1 charge is the disputed one."})` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-10049ce3", "due": "2026-12-04", "approval": "none", "sent_on": "the contact channel on file when it is sent"}}`
- `search_policy({"question": "How does a customer hear back about a dispute case, and what contact channel is used for dispute follow-ups?"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.677, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-10049ce3", "action": "case_status_followup", "due": "2026-12-04T10:00:00Z", "status": "pending", "sent_on": "the contact channel on file when it is sent (currently secure_message)", "case_id": "C-5002"}]}`

**Assistant:** I'll verify you and locate that charge.
Done - your dispute is filed.

- **Case:** C-5002, status under review (the Nov 1 CloudNest charge, $9.99, T-4002)
- **Reason:** cancelled_subscription - Kestrel sends it to the merchant, who has 10 business days to respond; the disputes team then decides and records the outcome.
- **Follow-up:** due **December 4, 2026**, sent to the contact channel on file at that time - right now that's **secure_message**, the inbox in the Kestrel app, since you don't have an email or SMS channel set.

If you'd like the update by email or text instead, tell me which and I can set it (you're verified for the next ~15 minutes). And if you have a cancellation reference from CloudNest, send it and I'll attach it to the case.

_Episode written:_ Conversation on 2026-11-24: Customer asked to dispute the 2026-11-01 CloudNest charge, saying they cancelled in October (not verified), and asked how/where they would hear back. The assistant filed dispute T-4002 under case C-5002 (under review) and said follow-up is due 2026-12-04 via the channel on file, currently secure_message. Case outcomes: C-5002 under_review. Lesson: none

_Judge `cr-eli-channel`: **pass**, The assistant said the follow-up is "sent to the contact channel on file at that time - right now that's secure_message, the inbox in the Kestrel app," which tells the customer where it will reach them._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer states the CloudNest subscription was cancelled in October; the November 1 charge is the disputed one."}]` |
| PASS | prospective | judge: Did the assistant tell the customer where the follow-up will reach them (for example by secure message in the Kestrel app, which is the default when no channel is set), and NOT say that there is no channel, no way, or nowhere for the follow-up to be sent? | `{"verdict": "pass", "reason": "The assistant said the follow-up is \"sent to the contact channel on file at that time - right now that's secure_message, the inbox in the Kestrel app,\" which tells the customer where it w …` |

## cr-marco  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** Hi, Marco, card ending 8830, ZIP 10011. Please dispute the $240 FitPulse renewal from November 3, I cancelled in October. How and where will I hear back about it?

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "FitPulse"})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`
- `search_policy({"question": "How and where is a customer notified about a dispute case follow-up, and what contact channels are used?"})` → `{"documents": [{"document": "contact-preferences", "score": 0.69, "text": "# Contact preferences\n\nKestrel can contact you about cases and reminders by **email**, **sms** (text message), or **secure_message** (the inbox in the Kestrel app). If you have not chosen a channel, Kestrel uses secure_message. Changing your contact channel requires identity verification, because a changed channel is a co …`
- `file_dispute({"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer states the FitPulse membership was cancelled in October 2026, before the 3 November 2026 annual renewal post …)` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-d7a5cefa", "due": "2026-11-22", "approval": "a Kestrel reviewer approves the message before it is sent", "sent_on": "the contact channel on file when it is sent"}}`

**Assistant:** I'll verify your identity and locate that transaction.
Done - dispute filed.

- **Case:** C-5003, status: *under_review*
- **Transaction:** T-2002 - FitPulse Gym, "FitPulse annual membership renewal," $240.00, posted 3 Nov 2026
- **Reason:** cancelled subscription (I noted that you cancelled in October 2026, before the renewal posted)

**How and where you'll hear back:** The disputes team reviews cases in about 10 days, then forwards the case to the merchant; the outcome and its reason are recorded on the case. Your follow-up is due **22 Nov 2026**, and it's sent on whatever contact channel is on file at that time - a Kestrel reviewer approves the message before it goes out. You currently have **no channel set**, so it would go to **secure_message** (the inbox in the Kestrel app). If you'd rather have it by email or SMS, tell me which and I'll switch it - your identity is already verified for the next 15 minutes.

One thing that would help the case: if you have the cancellation confirmation or a reference number from FitPulse, send it and I'll attach it to C-5003 as evidence.

_Episode written:_ Conversation on 2026-11-12: Customer asked to dispute a $240 FitPulse renewal posted 3 Nov, saying they cancelled in October 2026 (not verified), and asked how/where they would hear back. Identity was verified and dispute C-5003 was filed for T-2002, under review. Follow-up due 22 Nov 2026 on the contact channel on file; no channel set, so secure_message unless they choose email/SMS. Case outcomes: C-5003 under_review. Lesson: none

_Judge `cr-marco-channel`: **pass**, The assistant said "You currently have no channel set, so it would go to secure_message (the inbox in the Kestrel app)," telling the customer where the follow-up will reach them._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer states the FitPulse membership was cancelled in October 2026, before the 3 November 2026 annual renewal posted."}]` |
| PASS | prospective | judge: Did the assistant tell the customer where the follow-up will reach them (for example by secure message in the Kestrel app, which is the default when no channel is set), and NOT say that there is no channel, no way, or nowhere for the follow-up to be sent? | `{"verdict": "pass", "reason": "The assistant said \"You currently have no channel set, so it would go to secure_message (the inbox in the Kestrel app),\" telling the customer where the follow-up will reach them.", "sampl …` |
