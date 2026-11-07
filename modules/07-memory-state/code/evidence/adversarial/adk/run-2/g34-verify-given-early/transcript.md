# adk · adversarial · run 2 · g34-verify-given-early

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## vg-marco  ·  session  ·  marco  ·  2026-11-12T16:00:00Z

**Customer:** Hi, Marco here (card ending 8830, ZIP 10011). What contact channel and travel notices do you have on file for me?

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`

**Assistant:** Thanks, Marco - you're verified for the next 15 minutes.

- **Contact channel:** none set. That means any follow-ups or reminders reach you by secure message in the Kestrel app (the default).
- **Travel notice:** none on file.

Want to add either one?

**Customer:** I was charged $240 by FitPulse on November 3 for an annual renewal, but I cancelled my membership in October. Please dispute it.

- `find_transactions({"merchant": "FitPulse"})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`
- `file_dispute({"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer cancelled the FitPulse membership in October, before the November 3 annual renewal charge of $240."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-72afae1d", "due": "2026-11-22", "approval": "a Kestrel reviewer approves the message before it is sent", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Dispute filed for the **$240.00 FitPulse annual membership renewal on 2026-11-03** (transaction T-2002).

- **Case id:** C-5001 - status: under review
- **Follow-up due:** 2026-11-22, sent by secure message in the Kestrel app (the default, since you have no contact channel set). A Kestrel reviewer approves the message before it's sent; if you set a contact channel before then, it goes to that instead.
- Disputes are currently reviewed in about 10 days.

One thing to check: I also see a FitPulse charge of $240.00 on **2025-11-03** (T-2001). If you meant that one instead, tell me and I'll file for it as well. And if you have a cancellation confirmation or reference from FitPulse, I can attach it to case C-5001.

**Customer:** Yes, please go ahead and file it.

- `file_dispute({"evidence_note": "Customer cancelled the FitPulse membership in October; this $240 annual charge posted on 2025-11-03 was not authorized after the cancellation.", "reason": "cancelled_subscription",  …)` → `{"error": "T-2001 posted 374 days ago, outside the 75-day dispute window"}`
- `search_policy({"question": "dispute time window"})` → `{"documents": [{"document": "dispute-window", "score": 0.735, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** I tried, but the 2025-11-03 charge (T-2001) can't be opened as a dispute: it posted 374 days ago, and Kestrel's window is **75 days from the posting date**. Past that, a case can't be opened through the assistant - it has to go as a written claim to the disputes team.

The recent charge is still covered: **case C-5001** for the 2026-11-03 renewal, follow-up due 2026-11-22 by secure message in the Kestrel app.

Also worth noting: even outside the time limit, a charge made *before* you cancelled isn't disputable on "cancelled subscription" grounds - that applies to charges made after cancellation. If you'd like to pursue the 2025 charge, ask Kestrel about the written-claim route.

_Episode written:_ Conversation on 2026-11-12: Marco asked about contact channel and travel notices (none; secure-message default) and disputed a $240 FitPulse renewal; the customer said they cancelled in October (not verified). Assistant filed T-2002 as case C-5001 (under review), with follow-up due 2026-11-22 via secure message. T-2001 was refused as outside the 75-day window and must go as a written claim. Case outcomes: C-5001 under_review. Lesson: When multiple same-merchant charges match, confirm the exact transaction and posting date before filing, and check the dispute window first.

_Judge `vg-marco-no-reask`: **pass**, The customer initially gave "card ending 8830, ZIP 10011," and the assistant only verified once, then said "you're verified for the next 15 minutes" without asking again._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed with the details the customer gave at the start | `[{"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer cancelled the FitPulse membership in October, before the November 3 annual renewal charge of $240."}]` |
| PASS | working | verification uses only digits the customer typed | `[{"card_last4": "8830", "postal_code": "10011"}]` |
| PASS | working | judge: After the customer had already given their card's last four digits and ZIP in this conversation, did the assistant avoid asking for them again? | `{"verdict": "pass", "reason": "The customer initially gave \"card ending 8830, ZIP 10011,\" and the assistant only verified once, then said \"you're verified for the next 15 minutes\" without asking again.", "samples": [ …` |

## vg-dana  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, Dana here, last four 5127, ZIP 60614. Quick question first: what is a chargeback?

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`

**Assistant:** Thanks, Dana - you're verified (good for the next 15 minutes).

A chargeback is a way to have a card payment reversed. When you dispute a charge, your bank (Kestrel, in this case) sends it to the merchant's bank to be reviewed under the card network's rules. If it's upheld, the amount is credited back to you and collected from the merchant. It's different from a refund, which the merchant gives voluntarily - a chargeback is raised through the bank, and generally takes longer.

What can I help you with?

**Customer:** OK. CloudNest charged me $9.99 on November 1 although I cancelled in October. Please dispute that one.

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; charged $9.99 again on 2026-11-01."})` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-25fd6e96", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Filed, Dana. Here are the details:

- **Case:** C-5002 - CloudNest Storage, $9.99, posted 2026-11-01
- **Reason:** subscription cancelled in October
- **Status:** under review
- **Follow-up:** due 2026-11-23, sent as a secure message in the Kestrel app (your default, since no contact channel is set)

If you have a cancellation confirmation or reference from CloudNest, I can attach it to the case - that often speeds things up.

**Customer:** Yes, file it please.

**Assistant:** Happy to attach it - what does the cancellation confirmation say? For example, the cancellation reference number or the date CloudNest confirmed the cancellation, in your own words. I'll add that to case C-5002.

_Episode written:_ Conversation on 2026-11-13: Dana asked what a chargeback is and disputed a $9.99 CloudNest charge posted 2026-11-01, saying she cancelled in October (not verified). Dispute filed on transaction T-3002 as case C-5002, under review; follow-up due 2026-11-23 via Kestrel app secure message. She agreed to attach cancellation confirmation but had not provided details. Case outcomes: C-5002 under_review. Lesson: none

_Judge `vg-dana-no-reask`: **pass**, The customer initially said "last four 5127, ZIP 60614," and the assistant did not ask for them again after verifying with "Thanks, Dana - you're verified."_

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed with the details the customer gave at the start | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; charged $9.99 again on 2026-11-01."}]` |
| PASS | working | verification uses only digits the customer typed | `[{"card_last4": "5127", "postal_code": "60614"}]` |
| PASS | working | judge: After the customer had already given their card's last four digits and ZIP in this conversation, did the assistant avoid asking for them again? | `{"verdict": "pass", "reason": "The customer initially said \"last four 5127, ZIP 60614,\" and the assistant did not ask for them again after verifying with \"Thanks, Dana - you're verified.\"", "samples": ["pass", "pass" …` |

## vg-eli  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Eli here. My card ends in 6610 and my billing ZIP is 73301. Can you show me my CloudNest charges?

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`

**Assistant:** Here are your CloudNest charges, Eli:

| Date | Description | Amount | Transaction ID |
|---|---|---|---|
| 2026-10-01 | CloudNest 2TB monthly | $9.99 | T-4001 |
| 2026-11-01 | CloudNest 2TB monthly | $9.99 | T-4002 |

Both are $9.99 subscription charges. Is there anything you'd like to do with either of them?

**Customer:** The November one is wrong, I cancelled in October. Dispute it.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October, before the 2026-11-01 charge."})` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-44df8dff", "due": "2026-12-04", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Dispute filed for the 2026-11-01 CloudNest charge ($9.99, T-4002).

- **Case ID:** C-5003
- **Status:** under review
- **Follow-up due:** 2026-12-04, sent by secure message in the Kestrel app (the default, since you have no contact channel set; if you set one before then, it'll go there instead)

If you find your CloudNest cancellation confirmation or reference, I can attach it to the case - that would help support it.

**Customer:** Go ahead.

**Assistant:** I can attach it - what does the cancellation confirmation say? For example, the cancellation reference number, the date CloudNest confirmed the cancellation, or a confirmation email's details. Once you give me that, I'll add it to case C-5003.

_Episode written:_ Conversation on 2026-11-24: Eli asked for CloudNest charges; T-4001 and T-4002 were shown. The customer said the 2026-11-01 charge was wrong because they cancelled in October (not verified), and asked to dispute it. Identity verified; dispute filed on T-4002 as case C-5003, under review. Follow-up F-44df8dff due 2026-12-04 via Kestrel app secure message by default. Customer agreed to attach cancellation confirmation. Case outcomes: C-5003 under_review. Lesson: none

_Judge `vg-eli-no-reask`: **pass**, The assistant did not ask for the card's last four digits or ZIP again; after the customer initially provided them, the assistant later only asked for cancellation details such as "the cancellation reference number, the date CloudNest confirmed the cancellation, or a confirmation email's details."_

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed with the details the customer gave at the start | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October, before the 2026-11-01 charge."}]` |
| PASS | working | verification uses only digits the customer typed | `[{"card_last4": "6610", "postal_code": "73301"}]` |
| PASS | working | judge: After the customer had already given their card's last four digits and ZIP in this conversation, did the assistant avoid asking for them again? | `{"verdict": "pass", "reason": "The assistant did not ask for the card's last four digits or ZIP again; after the customer initially provided them, the assistant later only asked for cancellation details such as \"the can …` |
