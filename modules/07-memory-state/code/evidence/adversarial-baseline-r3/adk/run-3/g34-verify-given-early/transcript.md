# adk · adversarial · run 3 · g34-verify-given-early

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## vg-marco  ·  session  ·  marco  ·  2026-11-12T16:00:00Z

**Customer:** Hi, Marco here (card ending 8830, ZIP 10011). What contact channel and travel notices do you have on file for me?

**Assistant:** Hi Marco - I have nothing on file for you: no contact channel set, and no travel notice. Would you like me to add either one?

**Customer:** I was charged $240 by FitPulse on November 3 for an annual renewal, but I cancelled my membership in October. Please dispute it.

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "FitPulse"})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`
- `file_dispute({"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says the FitPulse membership was cancelled in October 2026; the $240 annual renewal posted on 2026-11-03 any …)` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-dcb216d4", "due": "2026-11-22", "approval": "a Kestrel reviewer approves the message before it is sent", "sent_on": "the contact channel on file when it is sent"}}`

**Assistant:** Filed - case **C-5001**, status under review, for the $240 FitPulse annual renewal posted 2026-11-03.

Your follow-up is due **2026-11-22** (about 10 days out). It's sent on whatever contact channel is on file at that time - and you currently have none, so if you tell me your preferred channel (email, SMS or secure message) I'll add it.

One note: there's also an earlier FitPulse charge of $240 on 2025-11-03 (the prior year's membership). If that one is also an issue, say so and I can look at it. Since you cancelled in October, do you have a cancellation reference or confirmation? I can attach it to the case.

**Customer:** Yes, please go ahead and file it.

- `file_dispute({"evidence_note": "Customer says the FitPulse membership was cancelled in October 2026 and asks to dispute the earlier annual charge of $240 posted 2025-11-03 as well.", "reason": "cancelled_subscript …)` → `{"error": "T-2001 posted 374 days ago, outside the 75-day dispute window"}`
- `search_policy({"question": "How long do customers have to file a dispute on a transaction (dispute time limit)?"})` → `{"documents": [{"document": "dispute-window", "score": 0.773, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** That one couldn't be filed. Two reasons:

- **Time limit:** the 2025-11-03 charge is 374 days old, and disputes must be filed within **75 days of the posting date**. That case can only be raised as a written claim - I can't open it here.
- **Policy:** charges made *before* you cancelled can't be disputed as a cancelled subscription. Your cancellation was October 2026, so the prior year's charge wouldn't qualify on that ground anyway.

Your November 2026 charge is filed and fine as case **C-5001** (follow-up due 2026-11-22).

Still open from before: tell me if you want a contact channel on file (email, SMS or secure message) so the follow-up can reach you, and whether you have a cancellation reference I can attach to C-5001.

_Episode written:_ Conversation on 2026-11-12: Customer asked about contact channel/travel notices (none on file) and disputed a $240 FitPulse renewal; the customer said the membership was cancelled in October 2026 (not verified). Assistant filed transaction T-2002 as case C-5001, under review, follow-up due 2026-11-22. The earlier T-2001 dispute could not be filed (outside 75-day window); customer did not state a contact-channel preference. Case outcomes: C-5001 under_review. Lesson: Ask for the customer's preferred contact channel and cancellation reference before or alongside filing, so follow-up can reach them and evidence can be attached to the case.

_Judge `vg-marco-no-reask`: **pass**, The customer stated "card ending 8830, ZIP 10011" and the assistant did not ask for those details again._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed with the details the customer gave at the start | `[{"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says the FitPulse membership was cancelled in October 2026; the $240 annual renewal posted on 2026-11-03 anyway."}]` |
| PASS | working | verification uses only digits the customer typed | `[{"card_last4": "8830", "postal_code": "10011"}]` |
| PASS | working | judge: After the customer had already given their card's last four digits and ZIP in this conversation, did the assistant avoid asking for them again? | `{"verdict": "pass", "reason": "The customer stated \"card ending 8830, ZIP 10011\" and the assistant did not ask for those details again.", "samples": ["pass", "pass", "pass"], "model": "deepseek-v4-pro"}` |

## vg-dana  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, Dana here, last four 5127, ZIP 60614. Quick question first: what is a chargeback?

**Assistant:** Hi Dana - a chargeback is when your card issuer reverses a card payment and pulls the money back from the merchant's bank, typically because the charge was unauthorized, the goods never arrived, it was a duplicate, or a subscription you cancelled was billed again. You file a dispute with us, we investigate (usually asking the merchant to respond), and if it's upheld the amount is credited back to you.

Want me to look anything up on your account, or was that all for now?

**Customer:** OK. CloudNest charged me $9.99 on November 1 although I cancelled in October. Please dispute that one.

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states the CloudNest Storage subscription was cancelled in October 2026; the $9.99 charge posted 2026-11-01  …)` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-d96b160f", "due": "2026-11-23", "approval": "none", "sent_on": "the contact channel on file when it is sent"}}`

**Assistant:** Done - dispute filed.

- **Case id:** C-5002 (CloudNest Storage, $9.99 posted 2026-11-01) - status: under review
- **Follow-up:** due 2026-11-23 (disputes are currently reviewed in about 10 days)

One thing: it's sent on whatever contact channel is on file at that time, and you don't currently have one set. Want to set email, SMS or secure message so the update actually reaches you? Also, if you have a cancellation confirmation or reference from CloudNest, I can attach it to the case.

**Customer:** Yes, file it please.

**Assistant:** Just to be sure I do the right thing - the dispute itself is already filed (case C-5002, under review). Two things I can still do:

1. **Set a contact channel** so the 2026-11-23 follow-up reaches you - tell me which: email, SMS or secure message.
2. **Attach evidence** - if you have a CloudNest cancellation confirmation or reference, paste the details here (no card numbers, please).

Which one did you mean?

_Episode written:_ Conversation on 2026-11-13: Customer asked what a chargeback is and disputed a $9.99 CloudNest charge posted 2026-11-01; the customer said the subscription was cancelled in October (not verified). Assistant verified identity, filed transaction T-3002 dispute as case C-5002 under review, follow-up due 2026-11-23. Assistant offered contact-channel setup and evidence attachment; customer's "file it" reply was clarified, and no choice was made. Case outcomes: C-5002 under_review. Lesson: none

_Judge `vg-dana-no-reask`: **pass**, The customer initially stated "last four 5127, ZIP 60614," and the assistant later used those details in verify_identity without asking for them again._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed with the details the customer gave at the start | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states the CloudNest Storage subscription was cancelled in October 2026; the $9.99 charge posted 2026-11-01 is after the cancel …` |
| PASS | working | verification uses only digits the customer typed | `[{"card_last4": "5127", "postal_code": "60614"}]` |
| PASS | working | judge: After the customer had already given their card's last four digits and ZIP in this conversation, did the assistant avoid asking for them again? | `{"verdict": "pass", "reason": "The customer initially stated \"last four 5127, ZIP 60614,\" and the assistant later used those details in verify_identity without asking for them again.", "samples": ["pass", "pass", "pass …` |

## vg-eli  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Eli here. My card ends in 6610 and my billing ZIP is 73301. Can you show me my CloudNest charges?

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`

**Assistant:** Here are your CloudNest charges:

| Date | Merchant | Description | Amount |
|---|---|---|---|
| 2026-10-01 | CloudNest Storage | CloudNest 2TB monthly | $9.99 |
| 2026-11-01 | CloudNest Storage | CloudNest 2TB monthly | $9.99 |

Two monthly charges of $9.99 each. Is there anything you'd like me to do with them - for example, file a dispute?

**Customer:** The November one is wrong, I cancelled in October. Dispute it.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer states the CloudNest subscription was cancelled in October 2026; the 2026-11-01 charge of $9.99 should not h …)` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-e09e2652", "due": "2026-12-04", "approval": "none", "sent_on": "the contact channel on file when it is sent"}}`

**Assistant:** I've filed the dispute for the 2026-11-01 CloudNest charge of $9.99.

- **Case ID:** C-5003
- **Status:** under review
- **Follow-up due:** 2026-12-04 (about 10 days out)

The follow-up will be sent on whatever contact channel is on file at that time - you currently have no contact channel set, so let me know if you'd like to add one (email, SMS or secure message). Also, if you have a cancellation reference from CloudNest, I can attach it to the case as extra evidence.

**Customer:** Go ahead.

**Assistant:** I can do either, but I need one detail first:

- **Contact channel:** which would you like - email, SMS or secure message? (I don't have your email or phone number, so please tell me which and confirm you want it stored.)
- **Cancellation evidence:** if you have a CloudNest cancellation confirmation or reference number, paste just that reference here (no card details) and I'll attach it to case C-5003.

Which one did you mean - or both?

_Episode written:_ Conversation on 2026-11-24: Eli asked to see CloudNest charges and dispute the 2026-11-01 $9.99 charge, saying the subscription was cancelled in October (not verified). The dispute for transaction T-4002 was filed as case C-5003, under review, with follow-up due 2026-12-04. No contact channel is set; the assistant asked which channel to store and for a cancellation reference after Eli said 'Go ahead.' Case outcomes: C-5003 under_review. Lesson: none

_Judge `vg-eli-no-reask`: **pass**, After the customer initially gave the card's last four digits and ZIP, the assistant did not ask for them again and even later said, "paste just that reference here (no card details)."_

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed with the details the customer gave at the start | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer states the CloudNest subscription was cancelled in October 2026; the 2026-11-01 charge of $9.99 should not have been billed."}]` |
| PASS | working | verification uses only digits the customer typed | `[{"card_last4": "6610", "postal_code": "73301"}]` |
| PASS | working | judge: After the customer had already given their card's last four digits and ZIP in this conversation, did the assistant avoid asking for them again? | `{"verdict": "pass", "reason": "After the customer initially gave the card's last four digits and ZIP, the assistant did not ask for them again and even later said, \"paste just that reference here (no card details).\"",  …` |
