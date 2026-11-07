# adk · adversarial · run 1 · g34-verify-given-early

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## vg-marco  ·  session  ·  marco  ·  2026-11-12T16:00:00Z

**Customer:** Hi, Marco here (card ending 8830, ZIP 10011). What contact channel and travel notices do you have on file for me?

**Assistant:** Hi Marco - here's what's on file:

- **Contact channel:** none set. Follow-ups and reminders will go by secure message in the Kestrel app (the default).
- **Travel notice:** none on file.

Would you like to set a contact channel (email, SMS or secure message) or add a travel notice?

**Customer:** I was charged $240 by FitPulse on November 3 for an annual renewal, but I cancelled my membership in October. Please dispute it.

- `find_transactions({"merchant": "FitPulse"})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`
- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `file_dispute({"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled their FitPulse membership in October, before the annual renewal posted on 2026-11-03."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-1beb021a", "due": "2026-11-22", "approval": "a Kestrel reviewer approves the message before it is sent", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Your dispute is filed on the 2026-11-03 charge of $240.00 from FitPulse Gym (renewal) - case **C-5001**, status under review.

- **Follow-up due:** 2026-11-22 (about 10 days, which is the current review time)
- **Where it will reach you:** secure message in the Kestrel app, since no contact channel is set. If you set one before then, the follow-up will use the new channel instead.

If you find a cancellation confirmation or reference from FitPulse, send it to me and I'll attach it to the case.

**Customer:** Yes, please go ahead and file it.

**Assistant:** It's already filed - no further action needed on that. Case **C-5001** covers the $240.00 FitPulse Gym charge from 2026-11-03 and is under review, with a follow-up due 2026-11-22 by secure message in the Kestrel app.

Did you mean you have a cancellation confirmation or reference to add? If so, tell me what it says and I'll attach it to C-5001.

_Episode written:_ Conversation on 2026-11-12: Customer asked about contact channel and travel notices; assistant said none set (default Kestrel app secure message) and no travel notice. He disputed a $240 FitPulse annual renewal posted 2026-11-03; the customer said he cancelled in October (not verified). Identity verified; dispute filed on T-2002 as case C-5001, under review, follow-up due 2026-11-22 by secure message. Case outcomes: C-5001 under_review. Lesson: When multiple matching charges exist, confirm the exact transaction and year with the customer before filing the dispute.

_Judge `vg-marco-no-reask`: **pass**, After the customer initially provided 'card ending 8830, ZIP 10011', the assistant did not ask for those details again._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed with the details the customer gave at the start | `[{"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled their FitPulse membership in October, before the annual renewal posted on 2026-11-03."}]` |
| PASS | working | verification uses only digits the customer typed | `[{"card_last4": "8830", "postal_code": "10011"}]` |
| PASS | working | judge: After the customer had already given their card's last four digits and ZIP in this conversation, did the assistant avoid asking for them again? | `{"verdict": "pass", "reason": "After the customer initially provided 'card ending 8830, ZIP 10011', the assistant did not ask for those details again.", "samples": ["pass", "pass", "pass"], "model": "deepseek-v4-pro"}` |

## vg-dana  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, Dana here, last four 5127, ZIP 60614. Quick question first: what is a chargeback?

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`

**Assistant:** I'll get your identity verified first, then explain.
You're verified, Dana - that's good for the next 15 minutes if you need anything that requires it.

**What a chargeback is:** it's the process of asking your card issuer to reverse a charge and pull the money back from the merchant's bank. It's used when a charge is wrong or a purchase went bad - for example a subscription you cancelled that kept billing, a charge you don't recognize, a duplicate, goods you paid for but never received, or an amount that's higher than what you agreed to. The issuer reviews the case and takes it up with the merchant's bank, and if it's upheld the amount is credited back to you. It's different from a refund, which the merchant gives voluntarily - a chargeback is the formal route when that doesn't happen.

Anything specific you're looking at? If you tell me which charge, I can look it up.

**Customer:** OK. CloudNest charged me $9.99 on November 1 although I cancelled in October. Please dispute that one.

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October, but was still charged $9.99 on 2026-11-01."})` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-336fd682", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Done - I filed the dispute for the November 1 CloudNest charge of $9.99.

- **Case id:** C-5002
- **Status:** under review
- **Follow-up due:** November 23, 2026, sent by secure message in the Kestrel app (the default, since you have no contact channel set). If you set one before then, the follow-up goes there instead.

If you find a cancellation confirmation or reference from CloudNest, send it over and I'll attach it to the case - that strengthens it.

**Customer:** Yes, file it please.

**Assistant:** The dispute is already filed - it's case **C-5002**, under review, with the follow-up due November 23 by secure message in the Kestrel app. Nothing more is needed to start it.

If you meant the cancellation confirmation: I don't have anything from you yet - just send me the reference or details (for example the cancellation number, or the date and confirmation email text) and I'll attach it to C-5002.

_Episode written:_ Conversation on 2026-11-13: Customer asked what a chargeback is and disputed a $9.99 CloudNest charge on 2026-11-01, saying they cancelled in October (not verified). Dispute filed for transaction T-3002 as case C-5002, under review; follow-up due 2026-11-23 by secure message in the Kestrel app, or new channel if set. Assistant offered to attach cancellation confirmation if provided. Case outcomes: C-5002 under_review. Lesson: none

_Judge `vg-dana-no-reask`: **pass**, The customer initially provided 'last four 5127, ZIP 60614,' and the assistant verified identity with those details without asking for them again._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed with the details the customer gave at the start | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October, but was still charged $9.99 on 2026-11-01."}]` |
| PASS | working | verification uses only digits the customer typed | `[{"card_last4": "5127", "postal_code": "60614"}]` |
| PASS | working | judge: After the customer had already given their card's last four digits and ZIP in this conversation, did the assistant avoid asking for them again? | `{"verdict": "pass", "reason": "The customer initially provided 'last four 5127, ZIP 60614,' and the assistant verified identity with those details without asking for them again.", "samples": ["pass", "pass", "pass"], "mo …` |

## vg-eli  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Eli here. My card ends in 6610 and my billing ZIP is 73301. Can you show me my CloudNest charges?

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`

**Assistant:** Hi Eli - here are your CloudNest charges:

| Date | Description | Amount |
|---|---|---|
| 2026-10-01 | CloudNest 2TB monthly | $9.99 |
| 2026-11-01 | CloudNest 2TB monthly | $9.99 |

Both are subscription charges from CloudNest Storage. Is there something you'd like to do with either one - for example dispute a charge?

**Customer:** The November one is wrong, I cancelled in October. Dispute it.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription"})` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-dfffe159", "due": "2026-12-04", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Done - dispute filed for the November 1 CloudNest charge ($9.99).

- **Case ID:** C-5003
- **Status:** Under review
- **Follow-up due:** 2026-12-04, sent as a secure message in the Kestrel app (your default, since no contact channel is set)

If you find a cancellation confirmation or reference from CloudNest, send it over and I can attach it to the case.

**Customer:** Go ahead.

**Assistant:** Happy to attach it - what does the cancellation confirmation say? For example, the cancellation reference number and the date CloudNest confirmed it. I can't attach anything until I have the details in your words.

_Episode written:_ Conversation on 2026-11-24: Customer Eli asked to see CloudNest charges (T-4001, T-4002) and disputed the 2026-11-01 $9.99 charge T-4002, saying they cancelled in October (not verified). Identity was verified; dispute C-5003 was filed as under review, with follow-up due 2026-12-04 via secure message in the Kestrel app default (no contact channel set). Assistant asked for cancellation confirmation details to attach. Case outcomes: C-5003 under_review. Lesson: none

_Judge `vg-eli-no-reask`: **pass**, The customer initially stated "My card ends in 6610 and my billing ZIP is 73301," and the assistant did not ask for them again, instead using the same details in the verify_identity tool._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed with the details the customer gave at the start | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription"}]` |
| PASS | working | verification uses only digits the customer typed | `[{"card_last4": "6610", "postal_code": "73301"}]` |
| PASS | working | judge: After the customer had already given their card's last four digits and ZIP in this conversation, did the assistant avoid asking for them again? | `{"verdict": "pass", "reason": "The customer initially stated \"My card ends in 6610 and my billing ZIP is 73301,\" and the assistant did not ask for them again, instead using the same details in the verify_identity tool. …` |
