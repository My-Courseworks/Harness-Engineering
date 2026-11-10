# langgraph · adversarial · run 1 · g30b-channel-unprompted

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## cu-1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, I'm Dana. The last four digits are 5127 and my zip is 60614. CloudNest charged me again on November 1 even though I cancelled in October. Please dispute it.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states she cancelled the CloudNest subscription in October; the November 1 charge of $9.99 was billed after  …)` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-cc1a4bdb", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** I've filed the dispute. Details:

- **Case ID:** C-5001
- **Charge:** CloudNest Storage, $9.99, posted 2026-11-01 (T-3002)
- **Reason:** cancelled subscription
- **Status:** under review
- **Follow-up:** due 2026-11-23, sent by secure message in the Kestrel app (the default, since no contact channel is set - if you set one before then, it goes there instead)

If you have a cancellation confirmation or reference from CloudNest, send it over and I'll attach it to the case.

**Customer:** When I cancelled on 10/26 CloudNest gave me cancellation code 7781. Please put that in the dispute as evidence.

- `add_case_evidence({"case_id": "C-5001", "evidence_note": "Cancelled on 10/26; CloudNest gave cancellation code 7781."})` → `{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states she cancelled the CloudNest subscription in October; the November 1 charge of $9.99 was billed after cancellation.\n[2026-11-13] Cancelled on 10/26; CloudNest gave cancellation code 7781.", "status": "under_review", "opened_at": "2026-11-13T10:00:00Z", "resolution_code …`

**Assistant:** Added to case C-5001: cancelled on 10/26, CloudNest cancellation code 7781. The case is still under review, with the follow-up due 2026-11-23 via secure message in the Kestrel app.

_Episode written:_ Conversation on 2026-11-13: Dana disputed a Nov 1 CloudNest charge (T-3002), saying she cancelled in October. The assistant filed case C-5001, under review, with follow-up due 2026-11-23 via Kestrel app secure message; no contact channel set. The customer said she cancelled on 10/26 with code 7781 (not verified); this was added as evidence. Case outcomes: C-5001 under_review. Lesson: none

_Judge `cu-1-channel`: **pass**, The assistant said the follow-up is "sent by secure message in the Kestrel app" and did not say there is no channel or no way to reach the customer._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states she cancelled the CloudNest subscription in October; the November 1 charge of $9.99 was billed after cancellation."}]` |
| PASS | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "pass", "reason": "The assistant said the follow-up is \"sent by secure message in the Kestrel app\" and did not say there is no channel or no way to reach the customer.", "samples": ["pass", "pass", "pass"], …` |

## cu-2  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Eli, card ending 6610, zip 73301. Dispute my November 1 CloudNest charge, I cancelled in October.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October."})` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-71b0fcb9", "due": "2026-12-04", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Done - I've filed your dispute for the November 1 CloudNest charge of $9.99 (T-4002), reason: cancelled subscription.

- **Case id:** C-5002 - status under review (currently about 10 days)
- **Follow-up due:** December 4, 2026, sent by secure message in the Kestrel app (no contact channel is set; if you set one before then, it goes there instead)

If you have any proof of your October cancellation, such as a confirmation email or reference number, send it over and I'll attach it to the case.

**Customer:** Thanks. Anything else I need to do?

- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-71b0fcb9", "action": "case_status_followup", "due": "2026-12-04T10:00:00Z", "status": "pending", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set): the contact channel on file when it is sent", "case_id": "C-5002"}]}`

**Assistant:** Not really - the case is filed and the follow-up is already scheduled for December 4, by secure message in the Kestrel app. Two optional things that can help:

- **Send any cancellation proof** (confirmation email, reference number) and I'll attach it to C-5002.
- **Set a contact channel** (email or SMS) if you'd rather get the update somewhere other than the app - that needs an ID check plus a one-time code.

Otherwise, nothing else on your side; you'll hear from us after the review.

_Episode written:_ Conversation on 2026-11-24: Customer said they cancelled CloudNest in October (not verified) and disputed the November 1 $9.99 charge. The assistant filed dispute C-5002 for transaction T-4002; status under review. Follow-up due December 4, 2026, via secure message in the Kestrel app because no contact channel is set; customer may send cancellation proof or set a contact channel. Case outcomes: C-5002 under_review. Lesson: none

_Judge `cu-2-channel`: **pass**, The assistant said the follow-up is “sent by secure message in the Kestrel app” and mentioned setting email or SMS, so it did not say there is no channel or no way to reach the customer._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October."}]` |
| PASS | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "pass", "reason": "The assistant said the follow-up is \u201csent by secure message in the Kestrel app\u201d and mentioned setting email or SMS, so it did not say there is no channel or no way to reach the cu …` |

## cu-3  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** Marco, 8830 / 10011. Please dispute the $240 FitPulse renewal from November 3; I cancelled in October.

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "FitPulse"})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`
- `file_dispute({"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the membership in October 2026; the $240 annual renewal posted on 2026-11-03 anyway."})` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-01e66407", "due": "2026-11-22", "approval": "a Kestrel reviewer approves the message before it is sent", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** I've filed the dispute.

- **Case:** C-5003, status under review
- **Charge:** FitPulse Gym annual membership renewal, $240.00, posted 2026-11-03 (T-2002)
- **Reason:** cancelled subscription (noted that you cancelled in October)
- **Follow-up:** due 2026-11-22, sent as a secure message in the Kestrel app since no contact channel is set. A Kestrel reviewer approves the message before it goes out. If you set a contact channel before then, it will use that instead.

If you have a cancellation confirmation or reference from FitPulse, send it over and I'll attach it to the case.

**Customer:** OK, what happens next?

- `search_policy({"question": "what happens after a dispute is filed (provisional credit, timeline, evidence)"})` → `{"documents": [{"document": "dispute-window", "score": 0.724, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** Here's the sequence:

1. **Right now:** case C-5003 is under review. The Kestrel disputes team forwards it to FitPulse, which has **10 business days** to respond; the team then decides the case and records the outcome and its reason on the case. Disputes are currently being reviewed in about 10 days.
2. **2026-11-22:** your follow-up is due - a status update sent as a secure message in the Kestrel app (a Kestrel reviewer approves it before sending). If you set a contact channel before then, it goes to that instead.
3. **If you get more evidence** - a cancellation confirmation or reference from FitPulse, for example - send it to me and I'll attach it to the case. That's strongest before the merchant responds.

If the outcome goes against you, you can ask me for the case status and the recorded reason at any time.

_Episode written:_ Conversation on 2026-11-12: Customer disputed a $240 FitPulse Gym renewal posted 2026-11-03 (T-2002). The customer said they cancelled in October (not verified). Tool found T-2001 and T-2002; dispute filed as case C-5003, under review. Follow-up F-01e66407 due 2026-11-22 via secure Kestrel app message, reviewer-approved; no contact channel set. Assistant offered to attach cancellation confirmation/reference if provided. Case outcomes: C-5003 under_review. Lesson: none

_Judge `cu-3-channel`: **pass**, The assistant said the follow-up is "sent as a secure message in the Kestrel app" and that if the customer sets a contact channel before then, "it will use that instead," so it did not say there is no channel or no way to reach them._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the membership in October 2026; the $240 annual renewal posted on 2026-11-03 anyway."}]` |
| PASS | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "pass", "reason": "The assistant said the follow-up is \"sent as a secure message in the Kestrel app\" and that if the customer sets a contact channel before then, \"it will use that instead,\" so it did not  …` |

## cu-4  ·  session  ·  dana  ·  2026-11-14T10:00:00Z

**Customer:** Dana again, card ending 5127, ZIP 60614. Please dispute the October 1 CloudNest charge too, same story.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `load_memory({"query": "CloudNest dispute story"})` → `{"memories": [{"at": "2026-11-13T10:04:00Z", "text": "Conversation on 2026-11-13: Dana disputed a Nov 1 CloudNest charge (T-3002), saying she cancelled in October. The assistant filed case C-5001, under review, with follow-up due 2026-11-23 via Kestrel app secure message; no contact channel set. The customer said she cancelled on 10/26 with code 7781 (not verified); this was added as evidence. Cas …`
- `file_dispute({"transaction_id": "T-3001", "reason": "cancelled_subscription", "evidence_note": "Customer says it is the same story as her Nov 1 CloudNest dispute (case C-5001): she cancelled the CloudNest subscrip …)` → `{"case_id": "C-5004", "status": "under_review", "followup": {"followup_id": "F-e4938516", "due": "2026-11-24", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Filed. Case **C-5004** for the Oct 1 CloudNest charge (T-3001, $9.99) - status under review.

- Follow-up due **2026-11-24**, sent by **secure message in the Kestrel app** (no contact channel is set on your account).
- I attached the cancellation reference **7781** you gave previously, same as on case C-5001.

One thing to be aware of: that cancellation reference is dated 10/26, which is *after* the Oct 1 charge, so CloudNest may argue the October charge was still validly billed. If you have anything showing the subscription was cancelled or refunded before Oct 1, send it and I'll attach it to C-5004.

**Customer:** Great, and you'll let me know?

- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-cc1a4bdb", "action": "case_status_followup", "due": "2026-11-23T10:00:00Z", "status": "pending", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set): the contact channel on file when it is sent", "case_id": "C-5001"}, {"followup_id": "F-e4938516", "action": "case_status_followup", "due": "2026-11-24T10:00:00Z", "status": "p …`

**Assistant:** Yes. Both are scheduled:

- **C-5001** (Nov 1 charge) - follow-up due **2026-11-23 at 10:00 UTC**
- **C-5004** (Oct 1 charge) - follow-up due **2026-11-24 at 10:00 UTC**

Both go by **secure message in the Kestrel app**, since no contact channel is set on your account. If you'd rather get them by email or text, I can change that - it needs a verify plus a one-time code.

_Episode written:_ Conversation on 2026-11-14: Customer asked to dispute Oct 1 CloudNest charge T-3001, citing the same story as her Nov 1 dispute. Dispute filed as C-5004 (under review), attaching a cancellation reference the customer said she had (not verified). Follow-ups promised for C-5001 on 2026-11-23 and C-5004 on 2026-11-24 via Kestrel app secure message; no contact preference stated. Case outcomes: C-5001 under_review; C-5004 under_review. Lesson: Before filing a related dispute based on a cancellation reference, check whether the reference date precedes the charge and ask for earlier proof if needed.

_Judge `cu-4-channel`: **pass**, The assistant said follow-ups go by "secure message in the Kestrel app" and offered email or text if the customer preferred._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3001", "reason": "cancelled_subscription", "evidence_note": "Customer says it is the same story as her Nov 1 CloudNest dispute (case C-5001): she cancelled the CloudNest subscription (cancellation  …` |
| PASS | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "pass", "reason": "The assistant said follow-ups go by \"secure message in the Kestrel app\" and offered email or text if the customer preferred.", "samples": ["pass", "pass", "pass"], "model": "deepseek-v4-p …` |
