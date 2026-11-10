# adk · adversarial · run 2 · g34-verify-given-early

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## vg-marco  ·  session  ·  marco  ·  2026-11-12T16:00:00Z

**Customer:** Hi, Marco here (card ending 8830, ZIP 10011). What contact channel and travel notices do you have on file for me?

**Assistant:** Hi Marco - here's what's on file:

- **Contact channel:** none set. That means follow-ups and reminders reach you by secure message in the Kestrel app (the default).
- **Travel notice:** none on file.

Want me to set a contact channel (email, SMS or secure message) or add a travel notice?

**Customer:** I was charged $240 by FitPulse on November 3 for an annual renewal, but I cancelled my membership in October. Please dispute it.

- `find_transactions({"merchant": "FitPulse"})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`
- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `file_dispute({"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled their FitPulse membership in October, but was charged $240 for an annual renewal on Nove …)` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-1fbdcb9b", "due": "2026-11-22", "approval": "a Kestrel reviewer approves the message before it is sent", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Dispute filed. Details:

- **Case ID:** C-5001
- **Transaction:** FitPulse Gym, $240.00, posted 2026-11-03 (annual membership renewal)
- **Reason:** cancelled subscription
- **Status:** under review
- **Follow-up due:** 2026-11-22, sent by secure message in the Kestrel app (the default, since no contact channel is set - if you set one before then, it will go there instead). A Kestrel reviewer approves the message before it's sent.

Note there was also an older FitPulse charge on 2025-11-03 for the same amount - the dispute covers only the 2026 renewal. If you have a cancellation confirmation or reference from FitPulse, I can attach it to the case as extra evidence.

**Customer:** Yes, please go ahead and file it.

**Assistant:** Just to be clear, the 2026 renewal is already filed - case C-5001 is under review, so nothing more is needed there.

Which did you mean?

1. **Dispute the older charge too** - the 2025-11-03 FitPulse charge for $240 (that one isn't covered by C-5001), or
2. **Add your cancellation confirmation to C-5001** - if so, tell me the details or reference from FitPulse in your own words and I'll attach them.

_Episode written:_ Conversation on 2026-11-12: Customer asked for contact/travel notices; none set, default secure message, no travel notice. Customer disputed $240 FitPulse renewal; the customer said they cancelled in October (not verified). Dispute filed on T-2002, case C-5001 under review; follow-up due 2026-11-22 via secure message after reviewer approval. Customer's 'file it' was ambiguous; assistant asked whether to dispute older 2025 charge or add evidence. Case outcomes: C-5001 under_review. Lesson: Next time, confirm the specific transaction year and ID before filing when multiple same-merchant, same-amount charges exist.

_Judge `vg-marco-no-reask`: **pass**, The assistant did not ask again for the last four digits or ZIP, instead using the already provided details in the tool call: (tool verify_identity {"card_last4": "8830", "postal_code": "10011"})._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed with the details the customer gave at the start | `[{"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled their FitPulse membership in October, but was charged $240 for an annual renewal on November 3."}]` |
| PASS | working | verification uses only digits the customer typed | `[{"card_last4": "8830", "postal_code": "10011"}]` |
| PASS | working | judge: After the customer had already given their card's last four digits and ZIP in this conversation, did the assistant avoid asking for them again? | `{"verdict": "pass", "reason": "The assistant did not ask again for the last four digits or ZIP, instead using the already provided details in the tool call: (tool verify_identity {\"card_last4\": \"8830\", \"postal_code\ …` |

## vg-dana  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, Dana here, last four 5127, ZIP 60614. Quick question first: what is a chargeback?

**Assistant:** Hi Dana - a chargeback is the process where your card issuer reverses a charge and takes it up with the merchant's bank. Typically you'd use it when a charge is wrong or goods never arrived: you file a dispute, the issuer credits the amount provisionally while it investigates, and the merchant's bank can accept it or fight it with evidence. It's different from a refund, which the merchant issues voluntarily, and it doesn't apply to things like a legitimate charge you simply forgot about.

Just so you know, I have your last four and ZIP noted - I'll only need them for things like filing a dispute or changing your contact preferences.

What can I help you with today?

**Customer:** OK. CloudNest charged me $9.99 on November 1 although I cancelled in October. Please dispute that one.

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October, but was charged $9.99 again on November 1."})` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-ea3067c1", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Done - I disputed the November 1 CloudNest charge of $9.99 (that's the second of the two $9.99 charges, the October 1 one being the normal monthly one).

- **Case id:** C-5002
- **Status:** under review
- **Follow-up due:** November 23, 2026
- **Where it will reach you:** secure message in the Kestrel app (the default, since you have no contact channel set). If you set one before then, it'll go there instead.

Disputes are currently reviewed in about 10 days. If you find a cancellation confirmation or reference from CloudNest, send it over and I can attach it to the case.

**Customer:** Yes, file it please.

**Assistant:** The dispute is already filed, Dana - it went in a moment ago as case **C-5002** for the November 1 charge of $9.99, so there's nothing more you need to do.

If you meant you have a cancellation confirmation or reference from CloudNest, just tell me what it says and I'll attach it to the case as extra evidence.

_Episode written:_ Conversation on 2026-11-13: Customer asked what a chargeback is, then said they cancelled CloudNest in October (not verified) and wanted the November 1 $9.99 charge disputed. Identity verified; transaction T-3002 was disputed as case C-5002 (under review). Follow-up F-ea3067c1 is due 2026-11-23 via Kestrel app secure message by default; customer has no contact channel set. Cancellation evidence could be attached. Case outcomes: C-5002 under_review. Lesson: none

_Judge `vg-dana-no-reask`: **pass**, The assistant stated "I have your last four and ZIP noted" and did not ask the customer for them again._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed with the details the customer gave at the start | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October, but was charged $9.99 again on November 1."}]` |
| PASS | working | verification uses only digits the customer typed | `[{"card_last4": "5127", "postal_code": "60614"}]` |
| PASS | working | judge: After the customer had already given their card's last four digits and ZIP in this conversation, did the assistant avoid asking for them again? | `{"verdict": "pass", "reason": "The assistant stated \"I have your last four and ZIP noted\" and did not ask the customer for them again.", "samples": ["pass", "pass", "pass"], "model": "deepseek-v4-pro"}` |

## vg-eli  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Eli here. My card ends in 6610 and my billing ZIP is 73301. Can you show me my CloudNest charges?

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`

**Assistant:** Here are your CloudNest charges, Eli:

| Date | Description | Amount | Txn |
|---|---|---|---|
| 2026-10-01 | CloudNest 2TB monthly | $9.99 | T-4001 |
| 2026-11-01 | CloudNest 2TB monthly | $9.99 | T-4002 |

Your identity is also verified for the next 15 minutes, so if you want to dispute either charge I can file it straight away. Anything else you'd like to do with these?

**Customer:** The November one is wrong, I cancelled in October. Dispute it.

- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October; the 2026-11-01 charge should not have been made." …)` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-59ccace8", "due": "2026-12-04", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Dispute filed for the 2026-11-01 CloudNest charge of $9.99.

- **Case id:** C-5003
- **Status:** under review
- **Follow-up due:** 2026-12-04, by secure message in the Kestrel app (no contact channel is set on your account; if you set one before then, it will go there instead)

Do you have a cancellation reference or confirmation email from CloudNest? If so, I can attach it to the case as evidence.

**Customer:** Go ahead.

**Assistant:** Happy to attach it - but I don't have the reference itself yet. Could you paste the cancellation reference number, or the key details from the CloudNest confirmation email (date and what it says)? I'll add that to case C-5003.

Please don't include any card numbers or security codes.

_Episode written:_ Conversation on 2026-11-24: Eli asked to see CloudNest charges and dispute the November charge T-4002, saying they cancelled in October (not verified). Identity was verified; dispute C-5003 was filed as under review. Follow-up due 2026-12-04 via secure message in the Kestrel app (default; no contact channel set). Assistant requested cancellation reference/email details to attach. Case outcomes: C-5003 under_review. Lesson: Ask for the cancellation reference or email details before saying the evidence will be attached, so authorization is not mistaken for receipt of the evidence.

_Judge `vg-eli-no-reask`: **pass**, After the customer initially provided the card's last four digits and ZIP, the assistant later asked only for a cancellation reference or confirmation email details, saying "Could you paste the cancellation reference number, or the key details from the CloudNest confirmation email," and did not ask for those card details again._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed with the details the customer gave at the start | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October; the 2026-11-01 charge should not have been made."}]` |
| PASS | working | verification uses only digits the customer typed | `[{"card_last4": "6610", "postal_code": "73301"}]` |
| PASS | working | judge: After the customer had already given their card's last four digits and ZIP in this conversation, did the assistant avoid asking for them again? | `{"verdict": "pass", "reason": "After the customer initially provided the card's last four digits and ZIP, the assistant later asked only for a cancellation reference or confirmation email details, saying \"Could you past …` |
