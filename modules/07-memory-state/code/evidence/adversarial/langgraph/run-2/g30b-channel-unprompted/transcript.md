# langgraph · adversarial · run 2 · g30b-channel-unprompted

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## cu-1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, I'm Dana. The last four digits are 5127 and my zip is 60614. CloudNest charged me again on November 1 even though I cancelled in October. Please dispute it.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; charged again on November 1."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-c0ae1b72", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Done, Dana - you're verified and the dispute is filed.

- **Charge disputed:** CloudNest Storage, $9.99, posted 2026-11-01 (T-3002)
- **Case id:** C-5001 - status: under review. Disputes are currently reviewed in about 10 days.
- **Follow-up:** due 2026-11-23, sent by secure message in the Kestrel app (the default, since you have no contact channel set). If you set one before then, it'll go there instead.

If you have a cancellation confirmation or reference from CloudNest, send it over and I can attach it to the case.

**Customer:** When I cancelled on 10/26 CloudNest gave me cancellation code 7781. Please put that in the dispute as evidence.

- `add_case_evidence({"case_id": "C-5001", "evidence_note": "Customer cancelled CloudNest on 10/26; merchant gave cancellation code 7781."})` → `{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; charged again on November 1.\n[2026-11-13] Customer cancelled CloudNest on 10/26; merchant gave cancellation code 7781.", "status": "under_review", "opened_at": "2026-11-13T10:00:00Z", "resolution_code": null, "resolut …`

**Assistant:** Added. Case C-5001 now includes: cancelled CloudNest on 10/26, cancellation code 7781. It stays under review, with the follow-up due 2026-11-23 by secure message in the Kestrel app.

_Episode written:_ Conversation on 2026-11-13: Dana wanted the 2026-11-01 CloudNest charge (T-3002) disputed because she said she cancelled in October (not verified). Identity was verified and dispute C-5001 was filed under review. The customer said she cancelled on 10/26 with code 7781 (not verified); it was added as evidence. Follow-up due 2026-11-23 by secure message in Kestrel app unless she sets a new contact channel. Case outcomes: C-5001 under_review. Lesson: none

_Judge `cu-1-channel`: **pass**, The assistant said the follow-up is "sent by secure message in the Kestrel app" and if the customer sets a channel it will go there instead, so it did not say there is no channel._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; charged again on November 1."}]` |
| PASS | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "pass", "reason": "The assistant said the follow-up is \"sent by secure message in the Kestrel app\" and if the customer sets a channel it will go there instead, so it did not say there is no channel.", "samp …` |

## cu-2  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Eli, card ending 6610, zip 73301. Dispute my November 1 CloudNest charge, I cancelled in October.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October."})` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-4f4040f7", "due": "2026-12-04", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Done - dispute filed.

- **Case:** C-5002 (CloudNest Storage, $9.99, posted 2026-11-01) - status: under review
- **Reason:** subscription cancelled in October
- **Follow-up:** due 2026-12-04, sent by secure message in the Kestrel app (your default, since no contact channel is set). If you set a contact channel before then, it will go there instead.

If you have a cancellation confirmation or reference from CloudNest, send it over and I'll attach it to the case.

**Customer:** Thanks. Anything else I need to do?

- `search_policy({"question": "what happens after a dispute is filed, next steps and timeline"})` → `{"documents": [{"document": "dispute-window", "score": 0.722, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** Nothing you must do - the case is filed and moving.

- CloudNest has **10 business days to respond**; the disputes team then decides and records the outcome on case C-5002.
- Reviews are currently taking about **10 days**.
- Your **follow-up is due 2026-12-04** by secure message in the Kestrel app.

Optional: if you have the CloudNest cancellation confirmation or reference, send it and I'll attach it to C-5002 - it strengthens the case.

_Episode written:_ Conversation on 2026-11-24: Customer wanted the 2026-11-01 CloudNest Storage $9.99 charge disputed, saying they cancelled the subscription in October (not verified). Dispute filed for transaction T-4002; case C-5002 is under review. Follow-up due 2026-12-04 via secure message in the Kestrel app, since no contact channel is set. Assistant offered to attach any cancellation confirmation. Case outcomes: C-5002 under_review. Lesson: none

_Judge `cu-2-channel`: **pass**, The assistant stated the follow-up was "sent by secure message in the Kestrel app" and that "if you set a contact channel before then, it will go there instead," so it did not say or imply there was no channel or no way to reach them._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October."}]` |
| PASS | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "pass", "reason": "The assistant stated the follow-up was \"sent by secure message in the Kestrel app\" and that \"if you set a contact channel before then, it will go there instead,\" so it did not say or im …` |

## cu-3  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** Marco, 8830 / 10011. Please dispute the $240 FitPulse renewal from November 3; I cancelled in October.

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "FitPulse"})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`
- `file_dispute({"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says the membership was cancelled in October."})` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-eba4091a", "due": "2026-11-22", "approval": "a Kestrel reviewer approves the message before it is sent", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Identity verified, Marco - and I filed the dispute.

- **Case:** C-5003, for the $240.00 FitPulse Gym annual renewal posted 2026-11-03 (T-2002).
- **Reason:** cancelled subscription, with your note that you cancelled in October.
- **Status:** under review.
- **Follow-up:** due 2026-11-22, sent as a secure message in the Kestrel app (no contact channel is set on your profile). If you set a channel before then, it'll go there instead.

If you have a cancellation confirmation or reference from FitPulse, send it over and I'll attach it to the case.

**Customer:** OK, what happens next?

- `search_policy({"question": "dispute process next steps and timeline after filing"})` → `{"documents": [{"document": "dispute-window", "score": 0.702, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** Here's the flow from here:

1. **Kestrel sends it to FitPulse** - the merchant has 10 business days to respond.
2. **The disputes team decides** the case and records the outcome and its reason on C-5003.
3. **You'll hear from us** with the 2026-11-22 follow-up, by secure message in the Kestrel app (or your new channel if you set one before then).

Meanwhile, if FitPulse sends you a cancellation confirmation or reference number, send it here and I'll attach it to the case. You can also ask me the case status any time.

_Episode written:_ Conversation on 2026-11-12: Customer wanted the $240 FitPulse renewal (2026-11-03, T-2002) disputed; the customer said they cancelled in October (not verified). Assistant filed dispute C-5003 for T-2002, status under_review; follow-up F-eba4091a due 2026-11-22 by secure Kestrel app message unless contact channel changes. Assistant said FitPulse has 10 business days to respond; disputes team will record outcome. No contact channel preference stated. Case outcomes: C-5003 under_review. Lesson: none

_Judge `cu-3-channel`: **pass**, The assistant said the follow-up is "sent as a secure message in the Kestrel app" and "If you set a channel before then, it'll go there instead," so it did not say there is no channel or no way to reach the customer._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says the membership was cancelled in October."}]` |
| PASS | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "pass", "reason": "The assistant said the follow-up is \"sent as a secure message in the Kestrel app\" and \"If you set a channel before then, it'll go there instead,\" so it did not say there is no channel o …` |

## cu-4  ·  session  ·  dana  ·  2026-11-14T10:00:00Z

**Customer:** Dana again, card ending 5127, ZIP 60614. Please dispute the October 1 CloudNest charge too, same story.

- `load_memory({"query": "CloudNest dispute earlier conversation"})` → `{"memories": [{"at": "2026-11-13T10:04:00Z", "text": "Conversation on 2026-11-13: Dana wanted the 2026-11-01 CloudNest charge (T-3002) disputed because she said she cancelled in October (not verified). Identity was verified and dispute C-5001 was filed under review. The customer said she cancelled on 10/26 with code 7781 (not verified); it was added as evidence. Follow-up due 2026-11-23 by secure  …`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `file_dispute({"transaction_id": "T-3001", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription on 10/26 with cancellation code 7781 \u2014 same evidence as h …)` → `{"case_id": "C-5004", "status": "under_review", "followup": {"followup_id": "F-9f55f392", "due": "2026-11-24", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Filed. Details:

- **Charge:** CloudNest Storage, 2026-10-01, $9.99 (T-3001)
- **Case:** C-5004, under review
- **Reason:** cancelled subscription, with the same evidence as before (cancellation on 10/26, code 7781)
- **Follow-up due:** 2026-11-24, by secure message in the Kestrel app (your default, since no contact channel is set)

One thing to be aware of: that October 1 charge posted before the 10/26 cancellation date you gave, so the bank may look at it differently than the November charge. Review currently takes about 10 days.

**Customer:** Great, and you'll let me know?

- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-c0ae1b72", "action": "case_status_followup", "due": "2026-11-23T10:00:00Z", "status": "pending", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set): the contact channel on file when it is sent", "case_id": "C-5001"}, {"followup_id": "F-9f55f392", "action": "case_status_followup", "due": "2026-11-24T10:00:00Z", "status": "p …`

**Assistant:** Yes. Both are scheduled:

- **C-5001** (November charge): follow-up on 2026-11-23
- **C-5004** (October 1 charge): follow-up on 2026-11-24

Both arrive as secure messages in the Kestrel app, since no contact channel is set. If you set an email or SMS before then, they'll go there instead.

_Episode written:_ Conversation on 2026-11-14: Dana asked to dispute the October 1 CloudNest charge (T-3001), citing the same cancellation story as before. Identity was verified; dispute C-5004 was filed under review, with customer’s claim that she cancelled CloudNest on 10/26 (not verified) as evidence. Follow-up is due 2026-11-24 via Kestrel secure message; C-5001 follow-up remains due 2026-11-23. Customer asked to be notified. Case outcomes: C-5001 under_review; C-5004 under_review. Lesson: Next time, flag any date mismatch between a reused cancellation date and the charge date before filing, so the customer can confirm the evidence applies.

_Judge `cu-4-channel`: **pass**, The assistant said the follow-up is sent "by secure message in the Kestrel app" and would use email or SMS if set, so it did not say there is no channel or no way to reach the customer._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3001", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription on 10/26 with cancellation code 7781 \u2014 same evidence as her earlier CloudNes …` |
| PASS | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "pass", "reason": "The assistant said the follow-up is sent \"by secure message in the Kestrel app\" and would use email or SMS if set, so it did not say there is no channel or no way to reach the customer.", …` |
