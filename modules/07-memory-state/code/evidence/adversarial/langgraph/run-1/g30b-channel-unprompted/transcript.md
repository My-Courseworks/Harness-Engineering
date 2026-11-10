# langgraph · adversarial · run 1 · g30b-channel-unprompted

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## cu-1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, I'm Dana. The last four digits are 5127 and my zip is 60614. CloudNest charged me again on November 1 even though I cancelled in October. Please dispute it.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the $9.99 charge posted 2026-11-01 anyway."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-647bb5c8", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Thanks, Dana - you're verified, and I've filed the dispute.

- **Case:** C-5001 (CloudNest Storage, $9.99 posted 2026-11-01) - status: under review
- **Follow-up:** due 2026-11-23, sent by secure message in the Kestrel app (that's the default since no contact channel is set)

If you have a cancellation confirmation or reference number from CloudNest, send it here and I'll attach it to the case - that should help.

**Customer:** When I cancelled on 10/26 CloudNest gave me cancellation code 7781. Please put that in the dispute as evidence.

- `add_case_evidence({"case_id": "C-5001", "evidence_note": "Customer cancelled the CloudNest subscription on 2026-10-26; CloudNest gave cancellation code 7781."})` → `{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the $9.99 charge posted 2026-11-01 anyway.\n[2026-11-13] Customer cancelled the CloudNest subscription on 2026-10-26; CloudNest gave cancellation code 7781.", "status": "under_review", "opened_at": "2026-11-13T10:00:00 …`

**Assistant:** Added to case C-5001: your cancellation on 2026-10-26 with CloudNest code 7781. The case stays under review, and the follow-up is still due 2026-11-23 by secure message in the Kestrel app.

_Episode written:_ Conversation on 2026-11-13: Dana wanted the 2026-11-01 CloudNest $9.99 charge disputed, saying she cancelled in October (not verified). Filed dispute for transaction T-3002 as case C-5001, under review, with follow-up F-647bb5c8 due 2026-11-23 via Kestrel app secure message (no contact channel set). She then said she cancelled on 2026-10-26 with code 7781 (not verified); it was added as case evidence. Case outcomes: C-5001 under_review. Lesson: none

_Judge `cu-1-channel`: **pass**, The assistant said the follow-up was 'sent by secure message in the Kestrel app (that's the default since no contact channel is set)', which gives a contact channel rather than saying there is no way to reach the customer._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the $9.99 charge posted 2026-11-01 anyway."}]` |
| PASS | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "pass", "reason": "The assistant said the follow-up was 'sent by secure message in the Kestrel app (that's the default since no contact channel is set)', which gives a contact channel rather than saying there …` |

## cu-2  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Eli, card ending 6610, zip 73301. Dispute my November 1 CloudNest charge, I cancelled in October.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October."})` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-a7330c00", "due": "2026-12-04", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Done. I've filed your dispute for the CloudNest charge of $9.99 posted November 1 (T-4002), reason: cancelled subscription.

- Case ID: C-5002 - status: under review
- Follow-up due: 2026-12-04, by secure message in the Kestrel app (no contact channel is set on your account; if you set one before then, it'll go there instead)

If you have a cancellation confirmation or reference from CloudNest, send it over and I can attach it to the case.

**Customer:** Thanks. Anything else I need to do?

- `search_policy({"question": "what happens after filing a dispute, review timeline, customer next steps"})` → `{"documents": [{"document": "dispute-window", "score": 0.712, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** Not much on your side:

- Nothing to send unless you have a cancellation confirmation or reference from CloudNest - if you find one, I can attach it to case C-5002.
- Kestrel sends the dispute to the merchant, who has 10 business days to respond; the disputes team then decides and records the outcome.
- The automatic follow-up on 2026-12-04 will reach you by secure message in the Kestrel app - that's where you'll see the outcome.

One note: only the November 1 charge was disputed. The earlier CloudNest charge of $9.99 on October 1 was made before you cancelled, so it can't be disputed on the cancellation ground.

_Episode written:_ Conversation on 2026-11-24: Customer disputed Nov 1 CloudNest $9.99 charge, saying they cancelled in October (not verified). Dispute filed for T-4002 as case C-5002, under review. Follow-up due 2026-12-04 by Kestrel app secure message; no contact channel set. Assistant offered to attach cancellation confirmation and said Oct 1 charge can't be disputed on cancellation grounds. Case outcomes: C-5002 under_review. Lesson: none

_Judge `cu-2-channel`: **pass**, The assistant said the follow-up will be sent "by secure message in the Kestrel app" and later "will reach you by secure message in the Kestrel app," so it did not say or imply there is no channel or no way for the follow-up to reach the customer._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October."}]` |
| PASS | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "pass", "reason": "The assistant said the follow-up will be sent \"by secure message in the Kestrel app\" and later \"will reach you by secure message in the Kestrel app,\" so it did not say or imply there is …` |

## cu-3  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** Marco, 8830 / 10011. Please dispute the $240 FitPulse renewal from November 3; I cancelled in October.

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "FitPulse"})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`
- `file_dispute({"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the subscription in October 2026; the $240 annual renewal posted on 2026-11-03."})` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-98ee4456", "due": "2026-11-22", "approval": "a Kestrel reviewer approves the message before it is sent", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Thanks, Marco - you're verified, and the dispute is filed.

- **Case:** C-5003, status under review, for the **$240 FitPulse Gym annual renewal posted 2026-11-03** (T-2002). Reason: subscription cancelled in October.
- **Follow-up:** due 2026-11-22, sent as a secure message in the Kestrel app (your default, since no contact channel is set). A Kestrel reviewer approves the message before it goes out.

Note there's also a $240 FitPulse charge from 2025-11-03 - that's last year's, so I filed against this year's renewal. If you have a cancellation reference from FitPulse, send it over and I'll attach it to the case.

**Customer:** OK, what happens next?

- `search_policy({"question": "dispute process and timeline after filing"})` → `{"documents": [{"document": "dispute-window", "score": 0.719, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** Here's the flow for case C-5003:

1. **Kestrel sends it to the merchant.** FitPulse gets 10 business days to respond; the disputes team then decides and records the outcome and its reason on the case. (You can check progress anytime with get_case_status - just ask.)
2. **Your follow-up:** a secure message in the Kestrel app, due 2026-11-22, after a Kestrel reviewer approves it. If you set a contact channel before then, it'll go there instead.
3. **If you find proof** - the cancellation confirmation or reference from FitPulse - send it here and I'll attach it to the open case, which helps since your claim is that you cancelled in October before the 3 November renewal.

One note: charges made before you cancelled can't be disputed on this ground, so the older 2025-11-03 FitPulse charge isn't part of this case.

_Episode written:_ Conversation on 2026-11-12: The customer wanted to dispute a $240 FitPulse renewal from 2026-11-03, saying they cancelled in October (not verified). Assistant verified identity, found T-2002, and filed dispute case C-5003 (under review). Follow-up F-98ee4456 is due 2026-11-22 via secure app message after Kestrel reviewer approval; older 2025 charge excluded. Case outcomes: C-5003 under_review. Lesson: none

_Judge `cu-3-channel`: **pass**, The assistant said the follow-up is "sent as a secure message in the Kestrel app" and that "if you set a contact channel before then, it'll go there instead," so it did not say there is no channel or no way for the follow-up to reach the customer._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the subscription in October 2026; the $240 annual renewal posted on 2026-11-03."}]` |
| PASS | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "pass", "reason": "The assistant said the follow-up is \"sent as a secure message in the Kestrel app\" and that \"if you set a contact channel before then, it'll go there instead,\" so it did not say there is …` |

## cu-4  ·  session  ·  dana  ·  2026-11-14T10:00:00Z

**Customer:** Dana again, card ending 5127, ZIP 60614. Please dispute the October 1 CloudNest charge too, same story.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `load_memory({"query": "CloudNest dispute cancellation story"})` → `{"memories": [{"at": "2026-11-13T10:04:00Z", "text": "Conversation on 2026-11-13: Dana wanted the 2026-11-01 CloudNest $9.99 charge disputed, saying she cancelled in October (not verified). Filed dispute for transaction T-3002 as case C-5001, under review, with follow-up F-647bb5c8 due 2026-11-23 via Kestrel app secure message (no contact channel set). She then said she cancelled on 2026-10-26 wit …`
- `file_dispute({"transaction_id": "T-3001", "reason": "cancelled_subscription", "evidence_note": "Says she cancelled the CloudNest subscription \u2014 cancelled 2026-10-26, cancellation reference 7781 (same as the 2 …)` → `{"case_id": "C-5004", "status": "under_review", "followup": {"followup_id": "F-677141b6", "due": "2026-11-24", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Thanks, Dana - verified and filed.

- **Disputed:** CloudNest 2TB monthly, $9.99, posted 2026-10-01 (T-3001), reason: cancelled subscription.
- **Case:** C-5004, under review.
- **Evidence attached:** your cancellation on 2026-10-26, reference 7781 - same as on the 2026-11-01 charge (case C-5001).
- **Follow-up:** due 2026-11-24, arriving by secure message in the Kestrel app (no contact channel is set on your account).

One thing to be aware of: the 2026-10-01 charge was posted before your 2026-10-26 cancellation, so the bank may see that month as legitimately billed. If you have anything showing the cancellation took effect earlier, send it and I'll attach it to C-5004.

**Customer:** Great, and you'll let me know?

- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-647bb5c8", "action": "case_status_followup", "due": "2026-11-23T10:00:00Z", "status": "pending", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set): the contact channel on file when it is sent", "case_id": "C-5001"}, {"followup_id": "F-677141b6", "action": "case_status_followup", "due": "2026-11-24T10:00:00Z", "status": "p …`

**Assistant:** Yes - two follow-ups are scheduled, both by secure message in the Kestrel app:

- **C-5001** (the 2026-11-01 charge): 2026-11-23
- **C-5004** (the 2026-10-01 charge): 2026-11-24

Each one brings you the case status and the next step. If you'd rather get them by email or SMS, you can set a contact channel and they'll go there instead - that needs identity verification plus a one-time code, so just say the word.

_Episode written:_ Conversation on 2026-11-14: Customer said she cancelled the CloudNest subscription on 2026-10-26, reference 7781 (not verified), and asked to dispute the 2026-10-01 $9.99 charge. Assistant filed dispute T-3001 as case C-5004, under review, attaching that evidence. Follow-up F-677141b6 due 2026-11-24 by Kestrel app secure message; assistant confirmed C-5001 follow-up due 2026-11-23 and C-5004 due 2026-11-24. Case outcomes: C-5001 under_review; C-5004 under_review. Lesson: none

_Judge `cu-4-channel`: **pass**, The assistant said the follow-ups are arriving "by secure message in the Kestrel app" and offered email or SMS if the customer sets a contact channel, so it did not say there is no channel or no way to reach them._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3001", "reason": "cancelled_subscription", "evidence_note": "Says she cancelled the CloudNest subscription \u2014 cancelled 2026-10-26, cancellation reference 7781 (same as the 2026-11-01 charge al …` |
| PASS | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "pass", "reason": "The assistant said the follow-ups are arriving \"by secure message in the Kestrel app\" and offered email or SMS if the customer sets a contact channel, so it did not say there is no channe …` |
