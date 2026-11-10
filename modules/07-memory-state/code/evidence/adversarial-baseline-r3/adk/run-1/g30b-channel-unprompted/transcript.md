# adk · adversarial · run 1 · g30b-channel-unprompted

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## cu-1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, I'm Dana. The last four digits are 5127 and my zip is 60614. CloudNest charged me again on November 1 even though I cancelled in October. Please dispute it.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states the CloudNest subscription was cancelled in October; the November 1 charge of $9.99 was posted after  …)` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-3d018e17", "due": "2026-11-23", "approval": "none", "sent_on": "the contact channel on file when it is sent"}}`
- `search_policy({"question": "Cancelled subscription dispute: follow-up timing and what contact channel is used when no channel is on file"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.743, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`

**Assistant:** I'll verify you and look up that charge.
Done - dispute filed on the November 1 charge.

- **Case:** C-5001 (CloudNest Storage, $9.99 on 2026-11-01)
- **Reason:** cancelled subscription
- **Status:** under review - the merchant has 10 business days to respond
- **Follow-up:** due 2026-11-23, sent to the contact channel on file at that time

Since you don't have a contact channel set, that follow-up will arrive in your Kestrel app inbox (secure message). If you'd rather get it by email or text, tell me which and I'll update it - that change needs identity verification, which is still valid from a moment ago.

Note: the October 1 charge went through before you cancelled, so it can't be disputed on this ground. If you have the cancellation confirmation from October, I can attach it to the case as evidence.

**Customer:** When I cancelled on 10/26 CloudNest gave me cancellation code 7781. Please put that in the dispute as evidence.

- `add_case_evidence({"case_id": "C-5001", "evidence_note": "Customer's CloudNest cancellation confirmation: subscription cancelled on 2026-10-26, cancellation code 7781."})` → `{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states the CloudNest subscription was cancelled in October; the November 1 charge of $9.99 was posted after cancellation.\n[2026-11-13] Customer's CloudNest cancellation confirmation: subscription cancelled on 2026-10-26, cancellation code 7781.", "status": "under_review", "o …`

**Assistant:** Added to case C-5001: your CloudNest cancellation dated 2026-10-26, code 7781. The case is still under review, with the follow-up due 2026-11-23.

_Episode written:_ Conversation on 2026-11-13: Dana wanted the 2026-11-01 CloudNest $9.99 charge disputed, saying she cancelled on 2026-10-26 (not verified). Dispute filed as case C-5001 for transaction T-3002; status under review, follow-up due 2026-11-23 via app inbox/contact channel on file. Her cancellation confirmation was added as evidence. Case outcomes: C-5001 under_review. Lesson: none

_Judge `cu-1-channel`: **pass**, The assistant said the follow-up 'will arrive in your Kestrel app inbox (secure message)' and offered to update to email or text, so it did not say there is no channel or no way for the follow-up to reach the customer._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states the CloudNest subscription was cancelled in October; the November 1 charge of $9.99 was posted after cancellation."}]` |
| PASS | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "pass", "reason": "The assistant said the follow-up 'will arrive in your Kestrel app inbox (secure message)' and offered to update to email or text, so it did not say there is no channel or no way for the fol …` |

## cu-2  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Eli, card ending 6610, zip 73301. Dispute my November 1 CloudNest charge, I cancelled in October.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer states the CloudNest subscription was cancelled in October 2026."})` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-dfa0ed1b", "due": "2026-12-04", "approval": "none", "sent_on": "the contact channel on file when it is sent"}}`
- `search_policy({"question": "When is the dispute case follow-up sent, and what channel is used if no contact channel is on file?"})` → `{"documents": [{"document": "dispute-window", "score": 0.677, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`
- `search_policy({"question": "Contact channel options and which one is used by default for case follow-ups when none is set"})` → `{"documents": [{"document": "contact-preferences", "score": 0.719, "text": "# Contact preferences\n\nKestrel can contact you about cases and reminders by **email**, **sms** (text message), or **secure_message** (the inbox in the Kestrel app). If you have not chosen a channel, Kestrel uses secure_message. Changing your contact channel requires identity verification, because a changed channel is a c …`

**Assistant:** Done. Here's where things stand:

- **Dispute filed:** case **C-5002**, for the CloudNest Storage charge of **$9.99** posted **2026-11-01** (T-4002), reason: cancelled subscription.
- **Follow-up:** due **2026-12-04**. Since you have no contact channel set, it will arrive in your **secure_message** inbox in the Kestrel app. You can change that to email or SMS - say which and I can set it now, since you're verified.
- **Timing:** Kestrel sends the dispute to the merchant, who has 10 business days to respond; the disputes team then decides the case.

One note: the earlier CloudNest charge from **2026-10-01** was made before you cancelled, so it can't be disputed on this ground.

**Customer:** Thanks. Anything else I need to do?

**Assistant:** Not required - the case is open and the follow-up is scheduled, so nothing is waiting on you.

Two optional things that would help:
- If you have a **cancellation confirmation or reference** from CloudNest (email or screenshot details), send it over and I'll attach it to case C-5002 as evidence.
- Keep an eye on your **secure_message** inbox, since that's where the follow-up will land on 2026-12-04.

If you'd rather get updates by **email or SMS**, just say which and I'll switch it while you're verified.

_Episode written:_ Conversation on 2026-11-24: Customer said they cancelled CloudNest in October (not verified) and wanted the 2026-11-01 CloudNest charge disputed. Assistant filed dispute T-4002 as case C-5002 for cancelled subscription. Follow-up is due 2026-12-04 via secure_message because no contact channel is set. Assistant said no further action was required and offered to attach cancellation evidence or switch updates to email/SMS. Case outcomes: C-5002 under_review. Lesson: none

_Judge `cu-2-channel`: **pass**, The assistant said "Since you have no contact channel set, it will arrive in your secure_message inbox in the Kestrel app," so it identified a channel rather than saying there is no way to send it._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer states the CloudNest subscription was cancelled in October 2026."}]` |
| PASS | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "pass", "reason": "The assistant said \"Since you have no contact channel set, it will arrive in your secure_message inbox in the Kestrel app,\" so it identified a channel rather than saying there is no way t …` |

## cu-3  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** Marco, 8830 / 10011. Please dispute the $240 FitPulse renewal from November 3; I cancelled in October.

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "FitPulse"})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`
- `file_dispute({"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer states they cancelled the FitPulse membership in October 2026, before the November 3 renewal."})` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-e2a92b47", "due": "2026-11-22", "approval": "a Kestrel reviewer approves the message before it is sent", "sent_on": "the contact channel on file when it is sent"}}`

**Assistant:** Verified - dispute filed.

- **Case:** C-5003 - FitPulse Gym, $240.00, posted 2026-11-03 (annual membership renewal)
- **Reason:** cancelled subscription (your note: cancelled in October, before the renewal)
- **Status:** under review; follow-up due **2026-11-22**

Two things worth knowing: reviews are currently running about 10 days, and the follow-up goes out on whatever contact channel is on file at that time - you currently have **none** on file. Tell me if you'd like it set to email, SMS or secure message.

**Customer:** OK, what happens next?

- `search_policy({"question": "What happens after a dispute is filed - review process, timelines, provisional credit, and how the customer is notified?"})` → `{"documents": [{"document": "dispute-window", "score": 0.704, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`
- `get_case_status({"case_id": "C-5003"})` → `{"cases": [{"case_id": "C-5003", "user_id": "marco", "txn_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer states they cancelled the FitPulse membership in October 2026, before the November 3 renewal.", "status": "under_review", "opened_at": "2026-11-12T10:00:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null, "decision_id": null}]}`

**Assistant:** Here's the sequence, Marco:

1. **Now:** case C-5003 is open and under review with the Kestrel disputes team.
2. **Merchant response:** Kestrel forwards it to FitPulse, who has 10 business days to respond.
3. **Decision:** the disputes team then decides the case and records the outcome and reason on the case.
4. **Follow-up:** a message is due **2026-11-22** to tell you where it stands - it goes out on your contact channel on file, and right now you have none set.

Also relevant: the charge is within the 75-day dispute window (posted 2026-11-03), so it's properly filed. If you find your cancellation confirmation from October, send it over and I'll attach it to the case - that strengthens it.

_Episode written:_ Conversation on 2026-11-12: Marco wanted to dispute a $240 FitPulse renewal posted November 3; the customer said he cancelled in October (not verified). The assistant verified identity, found T-2002, filed case C-5003 for cancelled subscription, and said it is under review. A follow-up is promised by 2026-11-22 after Kestrel reviewer approval; no contact channel is on file, and the customer stated no preference. Case outcomes: C-5003 under_review. Lesson: Next time, ask for and record a contact-channel preference before ending so the promised follow-up can be delivered.

_Judge `cu-3-channel`: **fail**, The assistant said "you currently have none on file" and "right now you have none set," implying there is no current contact channel for the follow-up._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer states they cancelled the FitPulse membership in October 2026, before the November 3 renewal."}]` |
| **FAIL** | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "fail", "reason": "The assistant said \"you currently have none on file\" and \"right now you have none set,\" implying there is no current contact channel for the follow-up.", "samples": ["fail", "fail", "fa …` |

## cu-4  ·  session  ·  dana  ·  2026-11-14T10:00:00Z

**Customer:** Dana again, card ending 5127, ZIP 60614. Please dispute the October 1 CloudNest charge too, same story.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `load_memory({"query": "CloudNest dispute previous conversation"})` → `{"result": "memories=[MemoryEntry(content=Content(\n  parts=[\n    Part(\n      text='Conversation on 2026-11-13: Dana wanted the 2026-11-01 CloudNest $9.99 charge disputed, saying she cancelled on 2026-10-26 (not verified). Dispute filed as case C-5001 for transaction T-3002; status under review, follow-up due 2026-11-23 via app inbox/contact channel on file. Her cancellation confirmation was add …`
- `file_dispute({"transaction_id": "T-3001", "reason": "cancelled_subscription", "evidence_note": "Subscription cancelled 2026-10-26; cancellation confirmation already supplied on related case C-5001 (2026-11-01 char …)` → `{"case_id": "C-5004", "status": "under_review", "followup": {"followup_id": "F-07621a64", "due": "2026-11-24", "approval": "none", "sent_on": "the contact channel on file when it is sent"}}`

**Assistant:** Filed - case C-5004 for the October 1 CloudNest charge of $9.99 (T-3001). Follow-up is due 2026-11-24, sent on whatever contact channel is on file at that time.

One thing to be aware of: your cancellation was on 2026-10-26, so that October 1 charge posted *before* the cancellation date, while the November 1 charge you disputed yesterday came after it. That timing may matter to the reviewer - if you have anything showing the account should already have been closed or refunded in October (e.g. an earlier cancellation request), send it over and I'll attach it.

**Customer:** Great, and you'll let me know?

- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-3d018e17", "action": "case_status_followup", "due": "2026-11-23T10:00:00Z", "status": "pending", "sent_on": "the contact channel on file when it is sent (currently secure_message)", "case_id": "C-5001"}, {"followup_id": "F-07621a64", "action": "case_status_followup", "due": "2026-11-24T10:00:00Z", "status": "pending", "sent_on": "the contact channel on file when i …`

**Assistant:** Yes. Two updates are scheduled:

- **C-5001** (Nov 1 charge) - status update due 2026-11-23
- **C-5004** (Oct 1 charge) - status update due 2026-11-24

Both will arrive on the contact channel on file at the time, currently secure message (app inbox). If you'd rather get them by email or SMS, tell me which and I'll switch it.

_Episode written:_ Conversation on 2026-11-14: Dana asked to dispute the 2026-10-01 CloudNest $9.99 charge (T-3001); the customer said the subscription was cancelled on 2026-10-26 (not verified). Identity verified. Case C-5004 was filed under review; status update scheduled for 2026-11-24 via the contact channel on file. C-5001 (T-3002) remains under review with update scheduled 2026-11-23. No alternate contact preference stated. Case outcomes: C-5001 under_review; C-5004 under_review. Lesson: none

_Judge `cu-4-channel`: **pass**, The assistant said the follow-up will be "sent on whatever contact channel is on file at that time" and later explained it is "currently secure message (app inbox)" with email or SMS options._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3001", "reason": "cancelled_subscription", "evidence_note": "Subscription cancelled 2026-10-26; cancellation confirmation already supplied on related case C-5001 (2026-11-01 charge)."}]` |
| PASS | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "pass", "reason": "The assistant said the follow-up will be \"sent on whatever contact channel is on file at that time\" and later explained it is \"currently secure message (app inbox)\" with email or SMS op …` |
