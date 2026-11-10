# langgraph · adversarial · run 2 · g30b-channel-unprompted

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## cu-1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, I'm Dana. The last four digits are 5127 and my zip is 60614. CloudNest charged me again on November 1 even though I cancelled in October. Please dispute it.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the $9.99 charge of November 1, 2026 came after th …)` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-617aa2ad", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** I'll verify you and look up the charge.
You're verified, Dana. I found the charge and filed the dispute.

- **Case ID:** C-5001 - CloudNest Storage, $9.99, posted November 1, 2026
- **Status:** under review
- **Follow-up due:** November 23, 2026, sent by secure message in the Kestrel app (the default, since no contact channel is set). If you set a contact channel before then, it will use that instead.

If you have a cancellation confirmation or reference from CloudNest, send it along and I can attach it to the case - that helps the review.

**Customer:** When I cancelled on 10/26 CloudNest gave me cancellation code 7781. Please put that in the dispute as evidence.

- `add_case_evidence({"case_id": "C-5001", "evidence_note": "Customer cancelled on 10/26 and CloudNest gave cancellation code 7781."})` → `{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the $9.99 charge of November 1, 2026 came after the cancellation.\n[2026-11-13] Customer cancelled on 10/26 and CloudNest gave cancellation code 7781.", "status": "under_review", "opened_at": "2026-11-13T10:00:00Z", "r …`

**Assistant:** Added - cancellation code 7781 is now attached to case C-5001 as evidence. The case stays under review, with the follow-up due November 23 by secure message in the Kestrel app.

_Episode written:_ Conversation on 2026-11-13: The customer wanted the Nov 1, 2026 CloudNest $9.99 charge disputed; the customer said she cancelled on 10/26 and got code 7781 (not verified). Dispute filed for transaction T-3002, case C-5001, under review; code 7781 added as evidence. Follow-up promised by Nov 23, 2026 via Kestrel app secure message (default; no contact channel set). Case outcomes: C-5001 under_review. Lesson: none

_Judge `cu-1-channel`: **pass**, The assistant said the follow-up is "sent by secure message in the Kestrel app" and "If you set a contact channel before then, it will use that instead," so it did not say there is no channel or no way to reach the customer._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the $9.99 charge of November 1, 2026 came after the cancellation."}]` |
| PASS | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "pass", "reason": "The assistant said the follow-up is \"sent by secure message in the Kestrel app\" and \"If you set a contact channel before then, it will use that instead,\" so it did not say there is no c …` |

## cu-2  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Eli, card ending 6610, zip 73301. Dispute my November 1 CloudNest charge, I cancelled in October.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October."})` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-1cbafe3a", "due": "2026-12-04", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** I've filed the dispute for the Nov 1 CloudNest Storage charge ($9.99).

- Case: C-5002, status under review
- Follow-up due: Dec 4, 2026 - sent by secure message in the Kestrel app, since no contact channel is set (it would use a new channel if you set one before then)

If you have a cancellation reference from CloudNest, send it over and I'll attach it to the case.

**Customer:** Thanks. Anything else I need to do?

**Assistant:** Not really - the dispute is filed and the follow-up is scheduled, so nothing is needed from you right now.

Two optional things:
- If CloudNest sent you a cancellation confirmation or reference, send it and I'll attach it to case C-5002; that tends to help.
- Your follow-up will arrive by secure message in the Kestrel app since no contact channel (email or SMS) is set. I can change that if you'd rather it reach you another way - it needs your card last 4 and ZIP again, plus a one-time code.

Otherwise, just watch for the follow-up on Dec 4.

_Episode written:_ Conversation on 2026-11-24: Customer disputed Nov 1 CloudNest Storage charge, saying they cancelled in October (not verified). Dispute filed for T-4002 as case C-5002, under review. Follow-up due Dec 4, 2026 by Kestrel app secure message because no contact channel is set. Assistant said nothing else was needed now; optional CloudNest cancellation reference can be attached. Case outcomes: C-5002 under_review. Lesson: none

_Judge `cu-2-channel`: **pass**, The assistant said the follow-up is 'sent by secure message in the Kestrel app' and offered to change it to another channel, so it did not say there is no channel or no way for the follow-up to reach the customer._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October."}]` |
| PASS | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "pass", "reason": "The assistant said the follow-up is 'sent by secure message in the Kestrel app' and offered to change it to another channel, so it did not say there is no channel or no way for the follow-u …` |

## cu-3  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** Marco, 8830 / 10011. Please dispute the $240 FitPulse renewal from November 3; I cancelled in October.

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "FitPulse"})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`
- `file_dispute({"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the FitPulse membership in October, before the November 3 renewal."})` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-fe1d62ff", "due": "2026-11-22", "approval": "a Kestrel reviewer approves the message before it is sent", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Thanks, Marco - identity verified and the dispute is filed.

- **Case:** C-5003 - FitPulse Gym, $240.00 annual membership renewal, posted 2026-11-03 (transaction T-2002), reason: cancelled subscription.
- **Status:** under review. Disputes are currently reviewed in about 10 days.
- **Follow-up:** due 2026-11-22, sent as a secure message in the Kestrel app (no contact channel is set on your account). A Kestrel reviewer approves the message before it's sent.

One thing to note: I also see an earlier FitPulse charge of $240.00 posted 2025-11-03. I filed against the recent renewal since you mentioned cancelling in October - tell me if you meant the older charge instead.

**Customer:** OK, what happens next?

- `search_policy({"question": "dispute process next steps and timeline"})` → `{"documents": [{"document": "dispute-window", "score": 0.7, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are reco …`

**Assistant:** Here's the flow from here:

- **Merchant response:** Kestrel sends the dispute to FitPulse, which has 10 business days to respond.
- **Decision:** After that, the Kestrel disputes team decides the case and records the outcome and reason on it.
- **Follow-up:** You'll get a secure message in the Kestrel app on **2026-11-22** with the case update (a reviewer approves it before it's sent). Disputes are currently reviewed in about 10 days.

You don't need to do anything in the meantime. If you find something like a cancellation confirmation or reference number from FitPulse, send it to me and I'll attach it to case C-5003.

_Episode written:_ Conversation on 2026-11-12: Customer asked to dispute a $240 FitPulse renewal dated November 3, saying they cancelled in October (not verified). Identity was verified; dispute filed for transaction T-2002, case C-5003, under review. Follow-up due 2026-11-22 via secure Kestrel app message, reviewer-approved; no contact channel set. An earlier FitPulse charge T-2001 was noted but not confirmed. Case outcomes: C-5003 under_review. Lesson: none

_Judge `cu-3-channel`: **pass**, The assistant said the follow-up is 'sent as a secure message in the Kestrel app (no contact channel is set on your account),' so it named a channel rather than saying there is no way to reach the customer._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the FitPulse membership in October, before the November 3 renewal."}]` |
| PASS | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "pass", "reason": "The assistant said the follow-up is 'sent as a secure message in the Kestrel app (no contact channel is set on your account),' so it named a channel rather than saying there is no way to re …` |

## cu-4  ·  session  ·  dana  ·  2026-11-14T10:00:00Z

**Customer:** Dana again, card ending 5127, ZIP 60614. Please dispute the October 1 CloudNest charge too, same story.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `load_memory({"query": "CloudNest dispute earlier conversation"})` → `{"memories": [{"at": "2026-11-13T10:04:00Z", "text": "Conversation on 2026-11-13: The customer wanted the Nov 1, 2026 CloudNest $9.99 charge disputed; the customer said she cancelled on 10/26 and got code 7781 (not verified). Dispute filed for transaction T-3002, case C-5001, under review; code 7781 added as evidence. Follow-up promised by Nov 23, 2026 via Kestrel app secure message (default; no c …`
- `file_dispute({"transaction_id": "T-3001", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription on 10/26; cancellation reference code 7781 (same as her earlie …)` → `{"case_id": "C-5004", "status": "under_review", "followup": {"followup_id": "F-139e6d66", "due": "2026-11-24", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** You're verified, and I filed it.

- **Charge:** CloudNest Storage, Oct 1, 2026, $9.99 (T-3001)
- **Case:** C-5004 - cancelled subscription, under review
- **Evidence attached:** your 10/26 cancellation, code 7781
- **Follow-up:** due Nov 24, 2026, by secure message in the Kestrel app (no contact channel set; if you set one before then, it'll go there instead)

One thing worth knowing: the Oct 1 charge posted before your Oct 26 cancellation date, so the bank may look at that one differently than the Nov 1 charge in C-5001. You can still add anything else you have - an earlier cancellation email or confirmation - to C-5004.

Currently open with us: C-5001 (Nov 1 charge) and C-5004 (Oct 1 charge).

**Customer:** Great, and you'll let me know?

- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-617aa2ad", "action": "case_status_followup", "due": "2026-11-23T10:00:00Z", "status": "pending", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set): the contact channel on file when it is sent", "case_id": "C-5001"}, {"followup_id": "F-139e6d66", "action": "case_status_followup", "due": "2026-11-24T10:00:00Z", "status": "p …`

**Assistant:** Yes - both are already scheduled, by secure message in the Kestrel app (no contact channel set):

- **C-5001** (Nov 1 charge): follow-up due Nov 23, 2026
- **C-5004** (Oct 1 charge): follow-up due Nov 24, 2026

Each one tells you the status of that case and the next step. If you'd rather get them by email or SMS, say which and I can switch your contact channel - that needs a one-time code sent to the mobile number or email the bank holds.

_Episode written:_ Conversation on 2026-11-14: Customer asked to dispute the Oct 1 CloudNest $9.99 charge (T-3001), saying she cancelled on 10/26 with code 7781 (not verified). Dispute filed as C-5004, under review; follow-up due Nov 24 via Kestrel app secure message (default; no contact channel set). Earlier C-5001 (T-3002) follow-up due Nov 23. Customer asked to be notified. Case outcomes: C-5001 under_review; C-5004 under_review. Lesson: none

_Judge `cu-4-channel`: **pass**, The assistant said the follow-up is 'by secure message in the Kestrel app' and offered to switch to email or SMS, not that there is no way to reach the customer._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3001", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription on 10/26; cancellation reference code 7781 (same as her earlier CloudNest dispute …` |
| PASS | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "pass", "reason": "The assistant said the follow-up is 'by secure message in the Kestrel app' and offered to switch to email or SMS, not that there is no way to reach the customer.", "samples": ["pass", "pass …` |
