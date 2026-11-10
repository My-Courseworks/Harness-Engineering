# adk · adversarial · run 1 · g30b-channel-unprompted

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## cu-1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, I'm Dana. The last four digits are 5127 and my zip is 60614. CloudNest charged me again on November 1 even though I cancelled in October. Please dispute it.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled her CloudNest subscription in October; the $9.99 CloudNest 2TB monthly charge posted 2026 …)` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-17220f08", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** You're verified, Dana - and I found the charge.

**Dispute filed**
- Case id: **C-5001**
- Charge: CloudNest Storage, "CloudNest 2TB monthly", **$9.99**, posted **2026-11-01** (transaction T-3002)
- Reason: subscription cancelled in October
- Status: under review - disputes are currently reviewed in about 10 days

**Follow-up:** due **2026-11-23**, sent by **secure message in the Kestrel app** (the default since you have no contact channel set). If you set a contact channel before then, it will go there instead.

If you have a cancellation confirmation or reference number from CloudNest, send it to me and I'll attach it to the case.

**Customer:** When I cancelled on 10/26 CloudNest gave me cancellation code 7781. Please put that in the dispute as evidence.

- `add_case_evidence({"case_id": "C-5001", "evidence_note": "CloudNest cancellation code 7781, given when the subscription was cancelled on 2026-10-26."})` → `{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled her CloudNest subscription in October; the $9.99 CloudNest 2TB monthly charge posted 2026-11-01 is after the cancellation.\n[2026-11-13] CloudNest cancellation code 7781, given when the subscription was cancelled on 2026-10-26.", "status": "under_review", " …`

**Assistant:** Added. Case **C-5001** now includes your CloudNest cancellation code **7781** (cancelled 2026-10-26) as evidence. The case is still under review, with the follow-up due **2026-11-23** by secure message in the Kestrel app.

_Episode written:_ Conversation on 2026-11-13: Dana asked to dispute a $9.99 CloudNest Storage charge posted 2026-11-01 (T-3002), saying she cancelled in October. The assistant verified her, filed dispute C-5001 under review, and added that the customer said she cancelled on 2026-10-26 with code 7781 (not verified) as evidence. Follow-up was promised for 2026-11-23 by Kestrel app secure message; if a contact channel changes, it will go there. Case outcomes: C-5001 under_review. Lesson: none

_Judge `cu-1-channel`: **pass**, The assistant said the follow-up is 'sent by secure message in the Kestrel app' and 'If you set a contact channel before then, it will go there instead', so it did not say there is no channel or no way for the follow-up to reach the customer._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled her CloudNest subscription in October; the $9.99 CloudNest 2TB monthly charge posted 2026-11-01 is after the …` |
| PASS | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "pass", "reason": "The assistant said the follow-up is 'sent by secure message in the Kestrel app' and 'If you set a contact channel before then, it will go there instead', so it did not say there is no chann …` |

## cu-2  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Eli, card ending 6610, zip 73301. Dispute my November 1 CloudNest charge, I cancelled in October.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the subscription in October; the 1 November CloudNest Storage 2TB monthly charge ($9.99) …)` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-888a4a66", "due": "2026-12-04", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** You're verified, Eli. I've filed the dispute.

- **Transaction:** CloudNest Storage, "CloudNest 2TB monthly" - $9.99, posted 1 Nov 2026 (T-4002)
- **Reason:** cancelled subscription (you cancelled in October)
- **Case:** C-5002, status under review
- **Follow-up:** due 4 Dec 2026, sent by secure message in the Kestrel app (the default, since no contact channel is set)

If you find a cancellation confirmation or reference from CloudNest, send it to me and I'll attach it to the case.

**Customer:** Thanks. Anything else I need to do?

- `search_policy({"question": "dispute review timeline and what the customer needs to do next"})` → `{"documents": [{"document": "dispute-window", "score": 0.723, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** Not much - it's mostly on our side now:

- Kestrel sends the dispute to CloudNest, which has 10 business days to respond, and the disputes team then decides the case.
- Your follow-up is already scheduled for 4 Dec 2026 by secure message in the Kestrel app.
- The one thing that would help: if you have a cancellation confirmation or reference from CloudNest (email, ticket number), send it here and I'll attach it to C-5002.

No other action needed from you.

_Episode written:_ Conversation on 2026-11-24: Customer wanted the November 1 CloudNest charge disputed, saying the subscription was cancelled in October (not verified). Identity verified; transaction T-4002 found and dispute C-5002 filed under review. Follow-up promised due 2026-12-04 by secure message in the Kestrel app (default; no contact channel set). Customer asked next steps; assistant said no other action and requested cancellation confirmation/reference. Case outcomes: C-5002 under_review. Lesson: none

_Judge `cu-2-channel`: **pass**, The assistant stated the follow-up is "sent by secure message in the Kestrel app," so it did not say there is no channel or no way to reach the customer._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the subscription in October; the 1 November CloudNest Storage 2TB monthly charge ($9.99) still posted."}]` |
| PASS | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "pass", "reason": "The assistant stated the follow-up is \"sent by secure message in the Kestrel app,\" so it did not say there is no channel or no way to reach the customer.", "samples": ["pass", "pass", "pa …` |

## cu-3  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** Marco, 8830 / 10011. Please dispute the $240 FitPulse renewal from November 3; I cancelled in October.

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "FitPulse"})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`
- `file_dispute({"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the membership in October."})` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-069b0bb9", "due": "2026-11-22", "approval": "a Kestrel reviewer approves the message before it is sent", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Verified, and the dispute is filed.

- **Case:** C-5003 - FitPulse Gym, $240.00, posted 2026-11-03 ("annual membership renewal")
- **Reason:** cancelled subscription (your note: cancelled in October)
- **Status:** under review - Kestrel is currently reviewing disputes in about 10 days
- **Follow-up:** due 2026-11-22, sent by secure message in the Kestrel app (that's the default since you have no contact channel set). A Kestrel reviewer approves the message before it goes out.

If you have a cancellation confirmation or reference number from FitPulse, send it over and I'll attach it to the case.

**Customer:** OK, what happens next?

- `get_case_status({"case_id": "C-5003"})` → `{"cases": [{"case_id": "C-5003", "user_id": "marco", "txn_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the membership in October.", "status": "under_review", "opened_at": "2026-11-12T10:00:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null, "decision_id": null}]}`
- `search_policy({"question": "what happens after a dispute is filed: review timeline and provisional credit"})` → `{"documents": [{"document": "dispute-window", "score": 0.724, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** Here's the path from here:

- **Now:** C-5003 is open and under review. Kestrel sends the dispute to FitPulse, and the merchant has 10 business days to respond. The disputes team then decides the case and records the outcome and its reason on it.
- **2026-11-22:** your follow-up is due and will arrive by secure message in the Kestrel app (the default, since no contact channel is set). A reviewer approves that message before it's sent.
- **During review:** if you find anything useful - a cancellation confirmation, an email or reference number from FitPulse - send it and I'll attach it to C-5003.
- **At the end:** if you disagree with the outcome, message me and I'll check the case and tell you your options.

You don't need to do anything to keep the case moving.

_Episode written:_ Conversation on 2026-11-12: Customer asked to dispute the $240 FitPulse renewal posted 2026-11-03. The customer said they cancelled in October (not verified). The assistant verified identity and filed dispute C-5003 for transaction T-2002, under review. Follow-up F-069b0bb9 is due 2026-11-22 via secure app message after reviewer approval; merchant has 10 business days to respond. No contact-channel preference stated. Case outcomes: C-5003 under_review. Lesson: When multiple same-merchant transactions exist, explicitly confirm the exact transaction ID with the customer before filing the dispute.

_Judge `cu-3-channel`: **pass**, The assistant said the follow-up is 'sent by secure message in the Kestrel app (that's the default since you have no contact channel set)', so it did not say there was no channel or no way to reach the customer._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the membership in October."}]` |
| PASS | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "pass", "reason": "The assistant said the follow-up is 'sent by secure message in the Kestrel app (that's the default since you have no contact channel set)', so it did not say there was no channel or no way  …` |

## cu-4  ·  session  ·  dana  ·  2026-11-14T10:00:00Z

**Customer:** Dana again, card ending 5127, ZIP 60614. Please dispute the October 1 CloudNest charge too, same story.

- `load_memory({"query": "CloudNest dispute October charge cancellation"})` → `{"result": "memories=[MemoryEntry(content=Content(\n  parts=[\n    Part(\n      text='Conversation on 2026-11-13: Dana asked to dispute a $9.99 CloudNest Storage charge posted 2026-11-01 (T-3002), saying she cancelled in October. The assistant verified her, filed dispute C-5001 under review, and added that the customer said she cancelled on 2026-10-26 with code 7781 (not verified) as evidence. Fol …`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `file_dispute({"transaction_id": "T-3001", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription on 2026-10-26, cancellation reference 7781 (same as the Novemb …)` → `{"case_id": "C-5004", "status": "under_review", "followup": {"followup_id": "F-13e38ae2", "due": "2026-11-24", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Done - filed for the October 1 CloudNest Storage charge of $9.99 (T-3001).

- Case id: **C-5004**, status under review (same reason as your November dispute: subscription cancelled)
- Evidence attached: your cancellation on 2026-10-26, reference 7781
- Follow-up due **2026-11-24**, by secure message in the Kestrel app (no contact channel is set; if you set one before then, it will go there)

Your earlier case C-5001 (the November 1 charge) is still under review with its follow-up on 2026-11-23.

**Customer:** Great, and you'll let me know?

- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-17220f08", "action": "case_status_followup", "due": "2026-11-23T10:00:00Z", "status": "pending", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set): the contact channel on file when it is sent", "case_id": "C-5001"}, {"followup_id": "F-13e38ae2", "action": "case_status_followup", "due": "2026-11-24T10:00:00Z", "status": "p …`

**Assistant:** Yes. Both case check-ins are scheduled:

- **C-5001** (Nov 1 charge) - 2026-11-23 at 10:00 UTC
- **C-5004** (Oct 1 charge) - 2026-11-24 at 10:00 UTC

Both will arrive by secure message in the Kestrel app, since no contact channel is set. If you'd like them sent to your email or by SMS instead, I can set that up - it just needs a quick identity check and a one-time code.

_Episode written:_ Conversation on 2026-11-14: Customer wanted to dispute the October 1 CloudNest charge (T-3001), citing the same cancellation story. Identity verified; dispute C-5004 filed under review. Follow-up due 2026-11-24 via Kestrel secure message, using any new contact channel. Earlier C-5001 remains under review; follow-up due 2026-11-23. The customer said she cancelled on 2026-10-26 with reference 7781 (not verified). Case outcomes: C-5001 under_review; C-5004 under_review. Lesson: When relying on a customer's prior cancellation claim as evidence, label it as customer-reported and not independently verified.

_Judge `cu-4-channel`: **pass**, The assistant said follow-up would be "by secure message in the Kestrel app" and offered to set up email or SMS, so it did not say there is no channel or no way to send it._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3001", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription on 2026-10-26, cancellation reference 7781 (same as the November charge dispute). …` |
| PASS | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "pass", "reason": "The assistant said follow-up would be \"by secure message in the Kestrel app\" and offered to set up email or SMS, so it did not say there is no channel or no way to send it.", "samples": [ …` |
