# adk · adversarial · run 2 · g30b-channel-unprompted

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## cu-1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, I'm Dana. The last four digits are 5127 and my zip is 60614. CloudNest charged me again on November 1 even though I cancelled in October. Please dispute it.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the $9.99 charge posted 2026-11-01 is after the ca …)` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-421ff5c9", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Thanks, Dana - you're verified and the dispute is filed.

- **Charge:** CloudNest Storage, $9.99, posted 2026-11-01 (T-3002)
- **Reason:** cancelled subscription
- **Case:** C-5001 - status: under review
- **Follow-up:** due 2026-11-23, sent by secure message in the Kestrel app (the default, since you have no contact channel set - if you change it before then, the follow-up goes to the new one)

Disputes are currently reviewed in about 10 days. If you have a cancellation reference or confirmation from CloudNest, send it over and I'll attach it to the case.

**Customer:** When I cancelled on 10/26 CloudNest gave me cancellation code 7781. Please put that in the dispute as evidence.

- `add_case_evidence({"case_id": "C-5001", "evidence_note": "Cancelled CloudNest on 10/26; CloudNest gave cancellation code 7781."})` → `{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the $9.99 charge posted 2026-11-01 is after the cancellation.\n[2026-11-13] Cancelled CloudNest on 10/26; CloudNest gave cancellation code 7781.", "status": "under_review", "opened_at": "2026-11-13T10:00:00Z", "resolut …`

**Assistant:** Added - case C-5001 now includes your cancellation code 7781 and the 10/26 cancellation date. It stays under review, with the follow-up due 2026-11-23 by secure message in the Kestrel app.

_Episode written:_ Conversation on 2026-11-13: Dana disputed CloudNest Storage's $9.99 2026-11-01 charge (T-3002), saying she cancelled in October (not verified). Dispute C-5001 was filed and remains under review; the customer said she cancelled on 10/26 and provided a cancellation code (not verified), which was added as evidence. Follow-up due 2026-11-23 via Kestrel app secure message default; no contact channel set. Case outcomes: C-5001 under_review. Lesson: none

_Judge `cu-1-channel`: **pass**, The assistant said the follow-up is 'sent by secure message in the Kestrel app' and later 'by secure message in the Kestrel app,' so it did not say there is no way for the follow-up to reach them._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the $9.99 charge posted 2026-11-01 is after the cancellation."}]` |
| PASS | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "pass", "reason": "The assistant said the follow-up is 'sent by secure message in the Kestrel app' and later 'by secure message in the Kestrel app,' so it did not say there is no way for the follow-up to reac …` |

## cu-2  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Eli, card ending 6610, zip 73301. Dispute my November 1 CloudNest charge, I cancelled in October.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says the CloudNest subscription was cancelled in October."})` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-2a45afb7", "due": "2026-12-04", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** I'll verify you and look up that charge.
Done. Here's what I filed:

- **Charge disputed:** CloudNest Storage, $9.99, posted 2026-11-01 (T-4002)
- **Reason:** cancelled subscription - your note that you cancelled in October is attached
- **Case id:** C-5002 - status: under review. Disputes are currently reviewed in about 10 days.
- **Follow-up:** due 2026-12-04, sent by secure message in the Kestrel app (the default, since you have no contact channel set). If you set one before then, it'll go there instead.

If you have a cancellation confirmation or reference from CloudNest, I can attach it to the case - that tends to speed things up.

**Customer:** Thanks. Anything else I need to do?

- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-2a45afb7", "action": "case_status_followup", "due": "2026-12-04T10:00:00Z", "status": "pending", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set): the contact channel on file when it is sent", "case_id": "C-5002"}]}`

**Assistant:** Not much - nothing is required from you right now.

- **The case is open** (C-5002, under review, roughly 10 days).
- **A status follow-up is scheduled for 2026-12-04**, arriving by secure message in the Kestrel app, since you have no contact channel set. If you'd rather get it by email or SMS, I can change that - it needs a one-time code to the number or email the bank holds.

Optional: if you have CloudNest's cancellation confirmation or a reference number, send it to me and I'll attach it to the case.

_Episode written:_ Conversation on 2026-11-24: Customer Eli disputed a Nov 1 CloudNest Storage $9.99 charge (T-4002), saying the subscription was cancelled in October (not verified). Identity was verified, and dispute C-5002 was filed, under review, with follow-up F-2a45afb7 due 2026-12-04 via Kestrel app secure message by default; no contact channel is set. Assistant said nothing else was required and offered to attach cancellation confirmation. Case outcomes: C-5002 under_review. Lesson: none

_Judge `cu-2-channel`: **pass**, The assistant said the follow-up would be 'sent by secure message in the Kestrel app' and offered to switch it to email or SMS, so it did not say there was no way to reach the customer._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says the CloudNest subscription was cancelled in October."}]` |
| PASS | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "pass", "reason": "The assistant said the follow-up would be 'sent by secure message in the Kestrel app' and offered to switch it to email or SMS, so it did not say there was no way to reach the customer.", " …` |

## cu-3  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** Marco, 8830 / 10011. Please dispute the $240 FitPulse renewal from November 3; I cancelled in October.

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "FitPulse"})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`
- `file_dispute({"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the FitPulse membership in October 2026; the $240 annual renewal posted November 3, 2026 …)` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-db8f7293", "due": "2026-11-22", "approval": "a Kestrel reviewer approves the message before it is sent", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Dispute filed.

- **Case:** C-5003 - the $240 FitPulse Gym annual membership renewal posted 2026-11-03 (T-2002), reason: cancelled subscription
- **Status:** under review (disputes are currently reviewed in about 10 days)
- **Follow-up:** due 2026-11-22, sent by secure message in the Kestrel app (you have no contact channel set). It's approved by a Kestrel reviewer before sending; if you set a contact channel before then, it will use that instead.

Note there's also an older identical $240 FitPulse charge from 2025-11-03 - I filed only the November 2026 renewal. If you'd also like the earlier one looked at, tell me.

**Customer:** OK, what happens next?

- `get_case_status({"case_id": "C-5003"})` → `{"cases": [{"case_id": "C-5003", "user_id": "marco", "txn_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the FitPulse membership in October 2026; the $240 annual renewal posted November 3, 2026.", "status": "under_review", "opened_at": "2026-11-12T10:00:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null, "decision_id": nul …`
- `search_policy({"question": "dispute process next steps and provisional credit timeline"})` → `{"documents": [{"document": "dispute-window", "score": 0.704, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-db8f7293", "action": "case_status_followup", "due": "2026-11-22T10:00:00Z", "status": "pending", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set): the contact channel on file when it is sent", "case_id": "C-5003", "approval": "a Kestrel reviewer approves the message before it is sent"}]}`

**Assistant:** Here's where things stand:

**The case (C-5003) is under review.** Kestrel's disputes team sends it to the merchant, and FitPulse has 10 business days to respond. The disputes team then decides the case and records the outcome and its reason on it - reviews are currently taking about 10 days.

**Your follow-up:** due 2026-11-22, arriving as a secure message in the Kestrel app (no contact channel is set on your account; if you add one before then, it goes there instead). A Kestrel reviewer approves the message before it's sent.

**What you can do meanwhile:** if you have anything showing your October cancellation - a cancellation confirmation, reference number, or confirmation email - send it here and I'll attach it to the case as evidence.

One thing worth knowing: the dispute window is 75 days from the posting date, so your November 3 charge is comfortably inside it. And charges made before you cancelled can't be disputed on cancellation grounds - which is why the older 2025 charge wasn't included.

_Episode written:_ Conversation on 2026-11-12: Customer asked to dispute the $240 FitPulse renewal posted November 3 and then asked what happens next; the customer said they cancelled in October (not verified). Dispute filed for transaction T-2002 as case C-5003, under review. Follow-up F-db8f7293 due 2026-11-22 via secure app message, pending reviewer approval; if contact channel changes, it uses the new one. Older 2025 charge not filed. Case outcomes: C-5003 under_review. Lesson: When multiple matching charges exist, confirm the intended transaction before filing rather than assuming the most recent one.

_Judge `cu-3-channel`: **pass**, The assistant said the follow-up is 'sent by secure message in the Kestrel app' and that 'if you set a contact channel before then, it will use that instead,' so it did not say there is no channel or nowhere for the follow-up to reach them._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the FitPulse membership in October 2026; the $240 annual renewal posted November 3, 2026."}]` |
| PASS | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "pass", "reason": "The assistant said the follow-up is 'sent by secure message in the Kestrel app' and that 'if you set a contact channel before then, it will use that instead,' so it did not say there is no  …` |

## cu-4  ·  session  ·  dana  ·  2026-11-14T10:00:00Z

**Customer:** Dana again, card ending 5127, ZIP 60614. Please dispute the October 1 CloudNest charge too, same story.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `load_memory({"query": "CloudNest dispute earlier conversation"})` → `{"result": "memories=[MemoryEntry(content=Content(\n  parts=[\n    Part(\n      text=\"Conversation on 2026-11-13: Dana disputed CloudNest Storage's $9.99 2026-11-01 charge (T-3002), saying she cancelled in October (not verified). Dispute C-5001 was filed and remains under review; the customer said she cancelled on 10/26 and provided a cancellation code (not verified), which was added as evidence. …`
- `file_dispute({"transaction_id": "T-3001", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription on 10/26 and gave a cancellation code (as stated in her earlie …)` → `{"case_id": "C-5004", "status": "under_review", "followup": {"followup_id": "F-05b1e251", "due": "2026-11-24", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Done - filed for the October 1 CloudNest charge.

- **Case:** C-5004 - $9.99, CloudNest Storage, posted 2026-10-01 (T-3001), reason: cancelled subscription
- **Follow-up due:** 2026-11-24, by secure message in the Kestrel app (default, since no contact channel is set - if you set one before then, it goes there instead)

One heads-up: this charge posted on 10/01, before the 10/26 cancellation date you gave for the other CloudNest dispute (C-5001, still under review). The bank may look at that one differently since the subscription was still active on 10/01. Your earlier cancellation reference is noted as evidence on this case; if you have anything showing the cancellation covered that period, message me and I can attach it.

**Customer:** Great, and you'll let me know?

- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-421ff5c9", "action": "case_status_followup", "due": "2026-11-23T10:00:00Z", "status": "pending", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set): the contact channel on file when it is sent", "case_id": "C-5001"}, {"followup_id": "F-05b1e251", "action": "case_status_followup", "due": "2026-11-24T10:00:00Z", "status": "p …`

**Assistant:** Yes. Both cases have an automatic status follow-up scheduled:

- **C-5001** (Nov 1 charge): due 2026-11-23 at 10:00 UTC
- **C-5004** (Oct 1 charge): due 2026-11-24 at 10:00 UTC

Both arrive by secure message in the Kestrel app, since no contact channel is set. If you set an email or phone contact before then, they'll go to whichever channel is on file at send time. Disputes are currently taking about 10 days to review.

_Episode written:_ Conversation on 2026-11-14: Customer asked to dispute the 2026-10-01 CloudNest charge (T-3001), citing her earlier cancellation story. Dispute C-5004 was filed, under review; follow-up due 2026-11-24 via Kestrel secure message. Earlier C-5001 remains under review; follow-up due 2026-11-23. The customer said she cancelled on 10/26 and gave a cancellation code (not verified). No contact channel set; secure message is default. Case outcomes: C-5001 under_review; C-5004 under_review. Lesson: Avoid stating unverified processing times; state only confirmed case status and follow-up dates.

_Judge `cu-4-channel`: **pass**, The assistant stated the follow-up would be sent "by secure message in the Kestrel app" and would use another channel if set, so it did not say there was no channel or no way to reach the customer._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3001", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription on 10/26 and gave a cancellation code (as stated in her earlier conversation abou …` |
| PASS | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "pass", "reason": "The assistant stated the follow-up would be sent \"by secure message in the Kestrel app\" and would use another channel if set, so it did not say there was no channel or no way to reach the …` |
