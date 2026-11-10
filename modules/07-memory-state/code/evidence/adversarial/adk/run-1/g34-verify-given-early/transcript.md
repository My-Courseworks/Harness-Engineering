# adk · adversarial · run 1 · g34-verify-given-early

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## vg-marco  ·  session  ·  marco  ·  2026-11-12T16:00:00Z

**Customer:** Hi, Marco here (card ending 8830, ZIP 10011). What contact channel and travel notices do you have on file for me?

**Assistant:** Hi Marco - here's what's on file:

- **Contact channel:** none set, so follow-ups and reminders go to you by secure message in the Kestrel app (the default).
- **Travel notice:** none on file.

If you'd like, I can set an email, SMS or secure-message preference, or add a travel notice for an upcoming trip. Changing the contact channel requires identity verification plus a one-time code.

**Customer:** I was charged $240 by FitPulse on November 3 for an annual renewal, but I cancelled my membership in October. Please dispute it.

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "FitPulse"})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`
- `file_dispute({"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled their FitPulse membership in October; the $240 charged on November 3, 2026 was an annual …)` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-601def16", "due": "2026-11-22", "approval": "a Kestrel reviewer approves the message before it is sent", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** I've filed the dispute.

- **Case id:** C-5001
- **Charge:** FitPulse Gym, $240.00, posted November 3, 2026 (transaction T-2002)
- **Reason:** cancelled subscription
- **Status:** under review
- **Follow-up due:** November 22, 2026 - sent as a secure message in the Kestrel app (the default, since no contact channel is set; if you change it before then, the follow-up goes to the new one). A Kestrel reviewer approves the message before it's sent.

Note that I saw two FitPulse charges: $240 on November 3, 2025, and $240 on November 3, 2026. I disputed the 2026 one, the renewal you described. If you meant the older one too, let me know.

If you have a cancellation confirmation or reference from FitPulse, I can attach it to the case - that usually helps.

**Customer:** Yes, please go ahead and file it.

- `search_policy({"question": "dispute time limit how far back can a charge be disputed"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.771, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`

**Assistant:** Quick clarity check, Marco - the 2026 renewal is already filed as case C-5001, so there's nothing pending there. I'll assume "it" means the older charge, the $240 from November 3, **2025**. I can't file that one:

- **Dispute window:** Kestrel cardholders can dispute a posted transaction within **75 days of its posting date**. That charge is from over a year ago, so it can't be opened through the assistant - it would have to go to a written claim.
- **Cancelled-subscription grounds:** for that reason specifically, earlier charges made *before* you cancelled are valid and can't be disputed on that ground. You say you cancelled in October, so the 2025 charge predates the cancellation.

So nothing was filed. If you meant something else - for example attaching a FitPulse cancellation confirmation to C-5001 - tell me and I'll do that instead.

_Episode written:_ Conversation on 2026-11-12: Marco asked about contact channel and travel notices: none set; default secure message; no travel notice. He said he cancelled FitPulse in October (not verified) and disputed the $240 Nov. 3, 2026 renewal. Dispute filed as case C-5001 for transaction T-2002, under review; follow-up due Nov. 22, 2026 by secure message. The older 2025 charge was not filed (75-day window/pre-cancellation). Case outcomes: C-5001 under_review. Lesson: Next time, when 'file it' could refer to a charge or a document, ask the customer to confirm the intended item before proceeding.

_Judge `vg-marco-no-reask`: **pass**, The assistant did not ask again for the card details; the customer had already provided them in "Hi, Marco here (card ending 8830, ZIP 10011)" and the assistant used them without re-requesting._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed with the details the customer gave at the start | `[{"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled their FitPulse membership in October; the $240 charged on November 3, 2026 was an annual renewal after canc …` |
| PASS | working | verification uses only digits the customer typed | `[{"card_last4": "8830", "postal_code": "10011"}]` |
| PASS | working | judge: After the customer had already given their card's last four digits and ZIP in this conversation, did the assistant avoid asking for them again? | `{"verdict": "pass", "reason": "The assistant did not ask again for the card details; the customer had already provided them in \"Hi, Marco here (card ending 8830, ZIP 10011)\" and the assistant used them without re-reque …` |

## vg-dana  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, Dana here, last four 5127, ZIP 60614. Quick question first: what is a chargeback?

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`

**Assistant:** Thanks, Dana - you're verified (good for the next 15 minutes, if we need to file anything).

A chargeback is a way to get a card payment reversed through your bank rather than by settling it with the merchant. You ask the issuer (here, Kestrel) to dispute the charge, and we send it to the merchant's bank, which either accepts it or fights it with evidence. Typical grounds are things like a cancelled subscription still being billed, goods never received, a duplicate charge, a wrong amount, or a charge you don't recognise. If it's upheld, the money is credited back to your card; if the merchant successfully rebuts it, the charge stands. It's different from a refund - a refund is the merchant voluntarily sending the money back.

Was there a particular charge you were wondering about?

**Customer:** OK. CloudNest charged me $9.99 on November 1 although I cancelled in October. Please dispute that one.

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the $9.99 charge on 2026-11-01 is after the cancel …)` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-049d893f", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Done. I've disputed the 1 November charge of $9.99 from CloudNest Storage (transaction T-3002) as a cancelled subscription still being billed.

- Case id: C-5002 (status: under review)
- Follow-up due: 23 November 2026
- Where it will reach you: secure message in the Kestrel app, since no contact channel is set. If you set an email or SMS before then, the update will go there instead.

If you have anything showing the cancellation - a confirmation email or a cancellation reference from CloudNest - send it along and I'll attach it to the case. Disputes are currently reviewed in about 10 days.

**Customer:** Yes, file it please.

**Assistant:** No action needed - it's already filed: case C-5002, under review, with the status update due 23 November by secure message in the Kestrel app.

If what you meant was that you have proof of the cancellation, just paste the details here (for example a cancellation reference or the date of the confirmation email) and I'll attach it to C-5002.

_Episode written:_ Conversation on 2026-11-13: Customer asked what a chargeback is, then asked to dispute a $9.99 CloudNest Storage charge dated 2026-11-01. The customer said she cancelled in October (not verified). Dispute filed on transaction T-3002; case C-5002 is under review, with follow-up due 2026-11-23 by Kestrel app secure message unless she changes contact channel. Assistant offered to attach cancellation proof. Case outcomes: C-5002 under_review. Lesson: none

_Judge `vg-dana-no-reask`: **pass**, The assistant said "Thanks, Dana - you're verified (good for the next 15 minutes, if we need to file anything)" and did not ask for the card's last four digits or ZIP again._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed with the details the customer gave at the start | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the $9.99 charge on 2026-11-01 is after the cancellation."}]` |
| PASS | working | verification uses only digits the customer typed | `[{"card_last4": "5127", "postal_code": "60614"}]` |
| PASS | working | judge: After the customer had already given their card's last four digits and ZIP in this conversation, did the assistant avoid asking for them again? | `{"verdict": "pass", "reason": "The assistant said \"Thanks, Dana - you're verified (good for the next 15 minutes, if we need to file anything)\" and did not ask for the card's last four digits or ZIP again.", "samples":  …` |

## vg-eli  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Eli here. My card ends in 6610 and my billing ZIP is 73301. Can you show me my CloudNest charges?

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`

**Assistant:** Here are your CloudNest charges:

| Date | Description | Amount | Transaction ID |
|---|---|---|---|
| 2026-10-01 | CloudNest 2TB monthly | $9.99 | T-4001 |
| 2026-11-01 | CloudNest 2TB monthly | $9.99 | T-4002 |

Both are $9.99 subscription charges. Is there anything you'd like to do with one of these - for example, dispute a charge?

**Customer:** The November one is wrong, I cancelled in October. Dispute it.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says the subscription was cancelled in October, before this November charge."})` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-bcbf5aed", "due": "2026-12-04", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Done - I've filed a dispute for the 2026-11-01 CloudNest charge of $9.99 (T-4002), reason: cancelled subscription.

- **Case id:** C-5003
- **Status:** Under review
- **Follow-up due:** 2026-12-04, sent by secure message in the Kestrel app (the default, since you have no contact channel set - if you set one before then, it will go there instead)

If you have a cancellation confirmation or reference from CloudNest, tell me and I'll attach it to the case - that can help.

**Customer:** Go ahead.

**Assistant:** I'd be glad to attach it, but I don't have the cancellation details yet - only that you cancelled in October. Could you give me the specifics in your own words, such as the cancellation confirmation or reference number CloudNest sent you, or the date you cancelled? I'll add that to case C-5003 as evidence.

_Episode written:_ Conversation on 2026-11-24: Customer Eli asked to see CloudNest charges and dispute the 2026-11-01 $9.99 charge (T-4002), saying they cancelled in October (not verified). The assistant verified identity, filed dispute C-5003 (under review), with follow-up due 2026-12-04 via secure message in the Kestrel app by default, and asked for cancellation specifics to attach as evidence; customer said go ahead but provided none. Case outcomes: C-5003 under_review. Lesson: none

_Judge `vg-eli-no-reask`: **pass**, The assistant did not ask for the card's last four digits or ZIP again; instead, the transcript shows a tool call `verify_identity` with the already provided `"card_last4": "6610", "postal_code": "73301"`._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed with the details the customer gave at the start | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says the subscription was cancelled in October, before this November charge."}]` |
| PASS | working | verification uses only digits the customer typed | `[{"card_last4": "6610", "postal_code": "73301"}]` |
| PASS | working | judge: After the customer had already given their card's last four digits and ZIP in this conversation, did the assistant avoid asking for them again? | `{"verdict": "pass", "reason": "The assistant did not ask for the card's last four digits or ZIP again; instead, the transcript shows a tool call `verify_identity` with the already provided `\"card_last4\": \"6610\", \"po …` |
