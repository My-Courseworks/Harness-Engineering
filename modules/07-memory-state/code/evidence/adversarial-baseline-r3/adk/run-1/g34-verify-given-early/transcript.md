# adk · adversarial · run 1 · g34-verify-given-early

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## vg-marco  ·  session  ·  marco  ·  2026-11-12T16:00:00Z

**Customer:** Hi, Marco here (card ending 8830, ZIP 10011). What contact channel and travel notices do you have on file for me?

**Assistant:** Hi Marco - I have no contact channel and no travel notice on file for you right now.

If you'd like, tell me which channel you'd prefer (email, SMS or secure message) or your travel destination and return date, and I'll record it.

**Customer:** I was charged $240 by FitPulse on November 3 for an annual renewal, but I cancelled my membership in October. Please dispute it.

- `find_transactions({"merchant": "FitPulse"})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`
- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `file_dispute({"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says the FitPulse membership was cancelled in October 2026 before this annual renewal posted on 2026-11-03." …)` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-483d3bcb", "due": "2026-11-22", "approval": "a Kestrel reviewer approves the message before it is sent", "sent_on": "the contact channel on file when it is sent"}}`

**Assistant:** Filed. Here are the details:

- **Case:** C-5001 - FitPulse Gym annual renewal, $240.00, posted 2026-11-03
- **Status:** Under review
- **Reason:** Cancelled subscription (membership cancelled in October)

The follow-up on this case is due **2026-11-22**, and it will be sent on whatever contact channel is on file at that time. You currently have **no contact channel on file**, so it may not reach you - tell me if you'd like to add email, SMS or secure message.

One thing I noticed: there's also a FitPulse charge of $240.00 from 2025-11-03. I left that one alone, but let me know if you want it looked at too.

**Customer:** Yes, please go ahead and file it.

- `search_policy({"question": "How far back can a transaction be disputed? Is there a deadline or time limit for filing a dispute?"})` → `{"documents": [{"document": "dispute-window", "score": 0.772, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** I can't open that one, unfortunately. Kestrel's dispute window is **75 days from the posting date**, and the 2025-11-03 charge is well past that - so it can't be filed through me. A charge that old would have to go to the disputes team as a written claim rather than a case opened here; please contact Kestrel directly to start that.

Also worth knowing: if that charge was made before you cancelled, it counts as a valid charge and can't be disputed as a cancelled subscription.

Your active case C-5001 for the 2026-11-03 renewal is unaffected - follow-up due 2026-11-22.

_Episode written:_ Conversation on 2026-11-12: Customer asked for contact channel/travel notices on file; none. Customer said FitPulse membership was cancelled in October (not verified) and requested dispute of $240 renewal. Dispute filed on T-2002 as case C-5001 (under review); follow-up due 2026-11-22. Older T-2001 charge could not be filed due 75-day window; written claim advised. No channel preference stated. Case outcomes: C-5001 under_review. Lesson: Next time, check the dispute-window policy before offering to file an older charge so the customer is not told it can be filed and then refused.

_Judge `vg-marco-no-reask`: **pass**, The customer initially said "Marco here (card ending 8830, ZIP 10011)" and the assistant later used those same details via verify_identity without asking for them again._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed with the details the customer gave at the start | `[{"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says the FitPulse membership was cancelled in October 2026 before this annual renewal posted on 2026-11-03."}]` |
| PASS | working | verification uses only digits the customer typed | `[{"card_last4": "8830", "postal_code": "10011"}]` |
| PASS | working | judge: After the customer had already given their card's last four digits and ZIP in this conversation, did the assistant avoid asking for them again? | `{"verdict": "pass", "reason": "The customer initially said \"Marco here (card ending 8830, ZIP 10011)\" and the assistant later used those same details via verify_identity without asking for them again.", "samples": ["pa …` |

## vg-dana  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, Dana here, last four 5127, ZIP 60614. Quick question first: what is a chargeback?

**Assistant:** Hi Dana - happy to explain. A chargeback is the process where you ask your card issuer to reverse a card payment and pull the funds back from the merchant's bank. Typically it's used when goods never arrived, a charge was duplicated or the wrong amount, a subscription kept billing after you cancelled, or you don't recognise the charge. The issuer reviews the evidence from both sides and decides whether to credit you.

A few things worth knowing: it's different from a refund (the merchant returns the money themselves), and it's not the same as an authorization hold, which is just a temporary reserve that drops off on its own.

If you have a specific charge in mind, tell me which one and I can look it up and, if you want, file a dispute.

**Customer:** OK. CloudNest charged me $9.99 on November 1 although I cancelled in October. Please dispute that one.

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states the CloudNest subscription was cancelled in October 2026; the $9.99 charge posted 2026-11-01."})` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-09e16f17", "due": "2026-11-23", "approval": "none", "sent_on": "the contact channel on file when it is sent"}}`
- `search_policy({"question": "How long does a dispute take and when is the follow-up sent to the customer?"})` → `{"documents": [{"document": "dispute-window", "score": 0.773, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** Filed, Dana. Here are the details:

- **Case:** C-5002 (status: under review)
- **Charge:** CloudNest Storage, $9.99, posted 2026-11-01
- **Reason:** cancelled_subscription
- **Follow-up due:** 2026-11-23

The merchant has 10 business days to respond, then the disputes team decides and records the outcome on the case.

One thing to fix: there's **no contact channel on file**, and the follow-up goes out on whatever channel is on file at the time it's sent. Would you like it by email, SMS, or secure message? Just tell me which and I'll set it.

**Customer:** Yes, file it please.

**Assistant:** The dispute is already filed (case C-5002), so nothing more needed there. To set where the follow-up arrives, I just need the channel - email, SMS, or secure message. Which one would you like?

_Episode written:_ Conversation on 2026-11-13: The customer asked what a chargeback is, then disputed a $9.99 CloudNest Storage charge posted 2026-11-01. The customer said the subscription was cancelled in October 2026 (not verified). Identity was verified; dispute T-3002 was filed as case C-5002, under review, with follow-up due 2026-11-23. The customer did not specify a follow-up channel. Case outcomes: C-5002 under_review. Lesson: Next time, ask for the customer’s preferred follow-up contact channel before filing the dispute, so a later “file it” response is not ambiguous after the case has already been opened.

_Judge `vg-dana-no-reask`: **pass**, The customer initially said "last four 5127, ZIP 60614," and the assistant later used those same details in verify_identity without asking for them again._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed with the details the customer gave at the start | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states the CloudNest subscription was cancelled in October 2026; the $9.99 charge posted 2026-11-01."}]` |
| PASS | working | verification uses only digits the customer typed | `[{"card_last4": "5127", "postal_code": "60614"}]` |
| PASS | working | judge: After the customer had already given their card's last four digits and ZIP in this conversation, did the assistant avoid asking for them again? | `{"verdict": "pass", "reason": "The customer initially said \"last four 5127, ZIP 60614,\" and the assistant later used those same details in verify_identity without asking for them again.", "samples": ["pass", "pass", "p …` |

## vg-eli  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Eli here. My card ends in 6610 and my billing ZIP is 73301. Can you show me my CloudNest charges?

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`

**Assistant:** Here are your CloudNest charges:

| Date | Description | Amount |
|---|---|---|
| 2026-10-01 | CloudNest 2TB monthly | $9.99 |
| 2026-11-01 | CloudNest 2TB monthly | $9.99 |

Anything you'd like to do with these - for example, dispute one?

**Customer:** The November one is wrong, I cancelled in October. Dispute it.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer states the CloudNest subscription was cancelled in October 2026; the 2026-11-01 charge is after cancellation …)` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-71dffa2c", "due": "2026-12-04", "approval": "none", "sent_on": "the contact channel on file when it is sent"}}`

**Assistant:** Done. Dispute filed for the 2026-11-01 CloudNest charge ($9.99).

- **Case ID:** C-5003 - status: under review
- **Follow-up due:** 2026-12-04 (disputes are typically reviewed in about 10 days)

One thing to note: your follow-up will be sent on whatever contact channel is on file at that time, and you currently have none set. Want me to set one (email, SMS or secure message)? Also, if you have a cancellation confirmation from CloudNest, I can attach it to the case as evidence.

**Customer:** Go ahead.

**Assistant:** Which channel should I use - email, SMS or secure message? And if you have a cancellation reference or confirmation, send it along and I'll attach it to case C-5003.

_Episode written:_ Conversation on 2026-11-24: Customer wanted CloudNest charges and disputed the 2026-11-01 charge, saying the subscription was cancelled in October (not verified). Identity verified and dispute filed for transaction T-4002, case C-5003, status under_review; follow-up due 2026-12-04. Assistant said no contact channel is on file and asked which to use; customer said go ahead but did not choose. No channel set. Case outcomes: C-5003 under_review. Lesson: When a customer replies “go ahead” to a multi-option request, confirm the specific contact channel and evidence before treating it as a preference.

_Judge `vg-eli-no-reask`: **pass**, The assistant did not ask for the card last four digits or ZIP again after the customer said "My card ends in 6610 and my billing ZIP is 73301," and it later used those same details in the verify_identity tool._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed with the details the customer gave at the start | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer states the CloudNest subscription was cancelled in October 2026; the 2026-11-01 charge is after cancellation."}]` |
| PASS | working | verification uses only digits the customer typed | `[{"card_last4": "6610", "postal_code": "73301"}]` |
| PASS | working | judge: After the customer had already given their card's last four digits and ZIP in this conversation, did the assistant avoid asking for them again? | `{"verdict": "pass", "reason": "The assistant did not ask for the card last four digits or ZIP again after the customer said \"My card ends in 6610 and my billing ZIP is 73301,\" and it later used those same details in th …` |
