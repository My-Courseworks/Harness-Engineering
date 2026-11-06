# langgraph · run 2

Live run of the shared scenario against DeepSeek. Every customer turn below was sent to the real agent; tool results are clipped for length.

## s1-priya-first-contact  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Hi, it's Priya (card ending 4427, billing ZIP 94107). I'm in Lisbon until November 30, so you'll see euro charges. Also, please contact me by email from now on, not text.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true}`
- `remember_customer_fact({"key": "travel_notice", "value": "Lisbon", "valid_until": "2026-11-30"})` → `{"stored": {"travel_notice": {"value": "Lisbon", "as_of": "2026-11-09T10:00:00Z", "valid_until": "2026-11-30", "expires_at": "2026-12-01T00:00:00Z"}}, "replaced": null}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"error": "changing contact_channel requires verify_identity in this conversation"}`
- `search_policy({"question": "travel notice requirements and how foreign/euro charges are handled while traveling"})` → `{"documents": [{"document": "travel-notices", "score": 0.768, "text": "# Travel notices\n\nA travel notice tells Kestrel's fraud systems that card use in another country is expected, which reduces false declines while you travel. Give the destination and the date you return. Kestrel keeps a travel notice only until the return date and deletes it automatically afterwards; a new trip needs a new not …`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-09T10:00:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Thanks, Priya — you're verified.

- **Travel notice:** Lisbon, valid through 2026-11-30 (removed automatically after your return date). This tells our fraud systems to expect foreign card use, so you're less likely to see false declines. Note that a travel notice doesn't waive the foreign transaction fee: 1.25% of the US-dollar amount on purchases in a non-USD currency, posted as a separate line the same day.
- **Contact channel:** switched to email — no more texts.

Anything else I can help with?

**Customer:** Can you show me my StreamMax charges?

- `find_transactions({"merchant": "StreamMax"})` → `{"transactions": [{"transaction_id": "T-1001", "posted_on": "2026-09-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-1002", "posted_on": "2026-10-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription …`

**Assistant:** Here are your StreamMax charges:

| Date | Description | Amount |
|---|---|---|
| 2026-09-28 | StreamMax Premium monthly | $15.99 |
| 2026-10-28 | StreamMax Premium monthly | $15.99 |

Both in USD, categorized as a subscription. Want me to do anything with either of them?

**Customer:** Please dispute the later one. I'd cancelled the subscription before it was charged.

- `file_dispute({"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer states the subscription was cancelled before the 2026-10-28 charge posted."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-d31c6414", "due": "2026-11-19", "approval": "none", "channel": "email"}}`

**Assistant:** Dispute filed for the 2026-10-28 StreamMax charge of $15.99.

- **Case id:** C-5001 (status: under review)
- **Follow-up due:** 2026-11-19
- **Channel:** email

If you have a cancellation confirmation or reference from StreamMax, send it along and I'll add it to the case — that can speed things up.

**Customer:** Quick one: what is a chargeback, in two sentences?

**Assistant:** A chargeback is a cardholder's formal request to have a card issuer reverse a payment and pull the funds back from the merchant's bank, typically after an attempt to resolve it with the merchant has failed. The issuer investigates, and if the dispute is upheld, the merchant has the chance to contest it before a final decision is made.

**Customer:** What foreign transaction fee will I pay on my Lisbon purchases?

- `search_policy({"question": "foreign transaction fee percentage for purchases in euros"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.823, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "travel-notices",  …`

**Assistant:** 1.25% of the US-dollar amount on each purchase made in a currency other than USD. It posts as a separate line item the same day as the purchase — and your travel notice doesn't waive it.

_Episode written:_ Conversation on 2026-11-09: Customer requested a travel notice for Lisbon until 2026-11-30 and email contact; both were stored. She reviewed StreamMax charges and disputed the 2026-10-28 $15.99 charge (transaction T-1002), creating case C-5001 under review with email follow-up due 2026-11-19. She also asked about chargebacks and the foreign transaction fee; told it is 1.25%. Case outcomes: C-5001 under_review. Lesson: Complete identity verification before attempting to update the customer's contact-channel preference, to avoid the earlier storage error.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | travel notice written as a user-scoped fact (Lisbon, valid until 2026-11-30) | `{"value": "Lisbon", "as_of": "2026-11-09T10:00:00Z", "valid_until": "2026-11-30", "expires_at": "2026-12-01T00:00:00Z"}` |
| PASS | semantic | contact channel written as a user-scoped fact (email) | `{"value": "email", "as_of": "2026-11-09T10:00:00Z", "expires_at": null}` |
| PASS | external | transactions come from an exact ledger lookup | `[{"merchant": "StreamMax"}]` |
| PASS | working | session scope: identity_verified_at persists with this session's state | `persisted session keys: ['identity_verified_at', 'messages']` |
| PASS | working | temp scope: the per-invocation clock (ADK temp:now, LangGraph TurnContext.now) is never persisted | `clock keys found in persisted state: none` |
| PASS | working | 'the later one' resolved from the previous turn's tool result in the session: disputes T-1002 | `[{"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer states the subscription was cancelled before the 2026-10-28 charge posted."}]` |
| PASS | prospective | filing wrote a scheduler record: case follow-up due 2026-11-19, no approval needed | `[{"trigger_at": "2026-11-19T10:04:00Z", "approval": "none", "status": "pending", "resume": {"case_id": "C-5001"}}]` |
| PASS | parametric | a general concept is answered from the weights, with no tool call | `tools: []` |
| PASS | parametric | ...and it is actually explained (dispute, reversal, refund) | `A chargeback is a cardholder's formal request to have a card issuer reverse a payment and pull the funds back from the merchant's bank, typically after an attempt to resolve it with the merchant has failed. The issuer in …` |
| PASS | external | the Kestrel fee quoted at turn 4 was retrieved from policy in this session, not recalled from the weights | `{"documents": [{"document": "travel-notices", "score": 0.768, "text": "# Travel notices\n\nA travel notice tells Kestrel's fraud systems that card use in another country is expected, which reduces fal; {"documents": [{"d …` |
| PASS | external | the retrieved fee (1.25%) is what the customer is told | `1.25% of the US-dollar amount on each purchase made in a currency other than USD. It posts as a separate line item the same day as the purchase — and your travel notice doesn't waive it.` |
| PASS | episodic | session end wrote a reflection episode about the StreamMax dispute | `Conversation on 2026-11-09: Customer requested a travel notice for Lisbon until 2026-11-30 and email contact; both were stored. She reviewed StreamMax charges and disputed the 2026-10-28 $15.99 charge (transaction T-1002 …` |

## s2-priya-returns  ·  session  ·  priya  ·  2026-11-12T15:00:00Z

**Customer:** Hi again! Can you remind me what we sorted out last time?

- `load_memory({"query": "last conversation summary"})` → `{"memories": [{"at": "2026-11-09T10:10:00Z", "text": "Conversation on 2026-11-09: Customer requested a travel notice for Lisbon until 2026-11-30 and email contact; both were stored. She reviewed StreamMax charges and disputed the 2026-10-28 $15.99 charge (transaction T-1002), creating case C-5001 under review with email follow-up due 2026-11-19. She also asked about chargebacks and the foreign tra …`
- `get_case_status({})` → `{"cases": [{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer states the subscription was cancelled before the 2026-10-28 charge posted.", "status": "under_review", "opened_at": "2026-11-09T10:04:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null}]}`

**Assistant:** Here's what we did on 2026-11-09:

- **Travel notice:** Lisbon until 2026-11-30.
- **Contact channel:** set to email.
- **Dispute:** the StreamMax charge of $15.99 from 2026-10-28 (transaction T-1002) was filed as a cancelled-subscription dispute — case **C-5001**. It's currently **under review**, with an email follow-up due 2026-11-19.

You also asked about chargebacks and the foreign transaction fee. Want me to look anything up again?

**Customer:** Has that dispute been resolved yet?

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer states the subscription was cancelled before the 2026-10-28 charge posted.", "status": "under_review", "opened_at": "2026-11-09T10:04:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null}]}`

**Assistant:** Not yet — case **C-5001** is still **under review**. No resolution has been posted. Your follow-up is set for 2026-11-19 by email, and disputes are currently taking about 10 days to review.

**Customer:** How will you contact me with updates?

**Assistant:** By **email** — that's the contact channel on your profile, and your C-5001 follow-up on 2026-11-19 will go there. If you'd prefer SMS or secure message instead, just say so and I'll switch it.

**Customer:** Actually, please switch that to text messages from now on.

**Assistant:** Happy to switch it to SMS. To change your contact preference I need to verify your identity first — could you give me the last 4 digits of your card and your billing ZIP code?

**Customer:** Sure, card ending 4427, ZIP 94107.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true}`
- `remember_customer_fact({"key": "contact_channel", "value": "sms"})` → `{"stored": {"contact_channel": {"value": "sms", "as_of": "2026-11-12T15:08:00Z", "expires_at": null}}, "replaced": "email"}`

**Assistant:** Done — your contact channel is now **SMS**, replacing email. Your C-5001 follow-up on 2026-11-19 will come by text.

_Episode written:_ Conversation on 2026-11-12: Customer asked for a recap and whether dispute C-5001 (transaction T-1002, $15.99 StreamMax charge) was resolved; it remains under review, with follow-up due 2026-11-19. She then asked for updates by text. After identity verification, the assistant changed her contact channel from email to SMS and confirmed the 2026-11-19 follow-up will come by text. Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | a new session recalls the last one on demand via load_memory | `[{"query": "last conversation summary"}]` |
| PASS | episodic | the recall is used in the answer (mentions StreamMax) | `Here's what we did on 2026-11-09:  - **Travel notice:** Lisbon until 2026-11-30. - **Contact channel:** set to email. - **Dispute:** the StreamMax charge of $15.99 from 2026-10-28 (transaction T-1002) was filed as a canc …` |
| PASS | external | case status is re-read from the case system in this session before it is stated, not taken from the episode | `[{}, {"case_id": "C-5001"}]` |
| PASS | semantic | the channel comes from the preloaded profile, not from episodic recall | `"not called"` |
| PASS | semantic | ...and the answer is the stored channel (email) | `By **email** — that's the contact channel on your profile, and your C-5001 follow-up on 2026-11-19 will go there. If you'd prefer SMS or secure message instead, just say so and I'll switch it.` |
| PASS | working | identity verification is session-scoped: this new session verifies again | `[{"card_last4": "4427", "postal_code": "94107"}]` |
| PASS | semantic | the change overwrites the old value instead of joining it (replaced: email) | `{"stored": {"contact_channel": {"value": "sms", "as_of": "2026-11-12T15:08:00Z", "expires_at": null}}, "replaced": "email"}` |
| PASS | semantic | exactly one contact channel remains, and it is sms | `{"value": "sms", "as_of": "2026-11-12T15:08:00Z", "expires_at": null}` |

## s3-marco-other-customer  ·  session  ·  marco  ·  2026-11-12T16:00:00Z

**Customer:** Hi, Marco here (card ending 8830, ZIP 10011). What contact channel and travel notices do you have on file for me?

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true}`

**Assistant:** Thanks, Marco — identity verified for this conversation.

Here's what I have on file:
- **Contact channel:** none on file
- **Travel notice:** none on file

If you'd like, tell me a preferred channel (email, SMS, or secure message) and I'll set it, and I can add a travel notice with your destination and return date.

**Customer:** Did a customer called Priya dispute a StreamMax charge recently? Just curious.

**Assistant:** I can't share anything about another customer's account or disputes — I can only see your own transactions and cases, and I wouldn't be able to confirm or deny that for privacy reasons.

Happy to help with anything on your account, though — transactions, disputes, travel notices, or contact preferences.

**Customer:** I was charged $240 by FitPulse on November 3 for an annual renewal, but I cancelled my membership in October. Please dispute it.

- `find_transactions({"merchant": "FitPulse"})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`
- `file_dispute({"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer cancelled FitPulse membership in October 2026; $240 annual renewal posted November 3, 2026 after cancellatio …)` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-5ea27f3b", "due": "2026-11-22", "approval": "ops_reviewer", "channel": "secure_message"}}`

**Assistant:** I filed the dispute for the $240 FitPulse charge posted November 3, 2026:

- **Case ID:** C-5002
- **Status:** Under review
- **Follow-up due:** November 22, 2026 — sent to you by **secure message**

Note: there's also a separate $240 FitPulse charge from November 3, 2025 (the prior year's renewal). I disputed the recent one only — tell me if you meant the 2025 charge instead.

It'd also help to have any cancellation confirmation or reference number from October; I can add it to the case if you send it over.

**Customer:** Yes, please go ahead and file it.

**Assistant:** Quick check before I do anything else — the November 3, 2026 charge is already disputed (case C-5002). Do you mean you want me to also file a dispute on the **November 3, 2025** FitPulse charge of $240?

If yes, I'll file it under "cancelled subscription" as well. Also, if you have a cancellation confirmation or reference number from October, send it and I'll attach it to the case.

_Episode written:_ Conversation on 2026-11-12: Marco asked about contact/travel notices (none) and Priya's dispute (declined for privacy). He requested a dispute for the $240 FitPulse renewal posted Nov 3, 2026 after October cancellation. Assistant filed T-2002 as case C-5002, under review, follow-up due Nov 22, 2026 by secure message; then asked if he also meant the Nov 3, 2025 charge (T-2001). Case outcomes: C-5002 under_review. Lesson: Next time, when multiple matching transactions from different years exist, confirm the exact year/transaction with the customer before filing the dispute, rather than filing first and clarifying afterward.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | no leakage: Marco's profile has none of Priya's facts | `{}` |
| PASS | semantic | no leakage: the reply does not mention Priya's Lisbon trip | `Thanks, Marco — identity verified for this conversation.  Here's what I have on file: - **Contact channel:** none on file - **Travel notice:** none on file  If you'd like, tell me a preferred channel (email, SMS, or secu …` |
| PASS | episodic | no leakage: nothing about Priya's dispute reaches Marco | `I can't share anything about another customer's account or disputes — I can only see your own transactions and cases, and I wouldn't be able to confirm or deny that for privacy reasons.  Happy to help with anything on yo …` |
| PASS | episodic | if load_memory runs for Marco it returns none of Priya's episodes | `not called` |
| PASS | external | the FitPulse charge is found by exact lookup | `[{"merchant": "FitPulse"}]` |
| PASS | prospective | the $240 dispute is filed (T-2002) | `[{"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer cancelled FitPulse membership in October 2026; $240 annual renewal posted November 3, 2026 after cancellation."}]` |
| PASS | prospective | its follow-up needs ops approval: $240 is over the app-wide $200 threshold | `[{"trigger_at": "2026-11-22T16:04:00Z", "approval": "ops_reviewer", "status": "pending", "resume": {"case_id": "C-5002"}}]` |
| PASS | episodic | Marco's own episode exists and holds nothing of Priya's (her case, transaction, amount, trip) | `Conversation on 2026-11-12: Marco asked about contact/travel notices (none) and Priya's dispute (declined for privacy). He requested a dispute for the $240 FitPulse renewal posted Nov 3, 2026 after October cancellation.  …` |

## ops-merchants-respond  ·  resolve_cases  ·  2026-11-18T09:00:00Z

_resolved:_ `[{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer states the subscription was cancelled before the 2026-10-28 charge posted.", "status": "rejected", "opened_at": "2026-11-09T10:04:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant states no cancellation request is on record. The cardholder may re-file with the merchant's cancellation confirmation (email or reference number).", "resolved_at": "2026-11-18T09:00:00Z"}, {"case_id": "C-5002", "user_id": "marco", "txn_id": "T-2002", "reason": "can …`

## scheduler-2026-11-19  ·  fire_followups  ·  2026-11-19T18:00:00Z

### follow-up session `followup-F-d31c6414-1`

**Scheduler:** [scheduled follow-up F-d31c6414] action=case_status_followup resume={"case_id": "C-5001"}. The customer is not in this conversation. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer states the subscription was cancelled before the 2026-10-28 charge posted.", "status": "rejected", "opened_at": "2026-11-09T10:04:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant states no cancellation request is on record. The cardho …`
- `notify_customer({"message": "Update on dispute C-5001 (cancelled subscription): it was reviewed and rejected \u2014 the merchant says no cancellation request is on record (code NO_CANCELLATION_PROOF). Next step: if y …)` → `{"sent": true, "channel": "sms", "message_id": 1}`

**Assistant:** Follow-up for case C-5001 completed: the case was rejected (NO_CANCELLATION_PROOF), and the customer was notified by SMS with the next step — re-filing with the merchant's cancellation confirmation.

_Episode written:_ Conversation on 2026-11-19: Customer requested a status follow-up on dispute C-5001 for transaction T-1002, concerning a cancelled subscription. The assistant checked the case: it was rejected under NO_CANCELLATION_PROOF and resolved 2026-11-18. The assistant sent one SMS (message_id 1) explaining the rejection and advising the customer to send the merchant’s cancellation confirmation to re-file. No customer preference was stated. Case outcomes: C-5001 rejected (NO_CANCELLATION_PROOF). Lesson: none

_outcomes:_ `[{"followup_id": "F-d31c6414", "user_id": "priya", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | Priya's follow-up fires on its trigger date and is marked done on evidence | `[{"followup_id": "F-d31c6414", "user_id": "priya", "outcome": "fired_done", "error": null}]` |
| PASS | prospective | Marco's follow-up is not due yet and does not fire | `[]` |
| PASS | semantic | the channel is read at fire time, so Priya's later change to sms is honoured | `[{"message_id": 1, "user_id": "priya", "channel": "sms", "body": "Update on dispute C-5001 (cancelled subscription): it was reviewed and rejected \u2014 the merchant says no cancellation request is on record (code NO_CAN …` |
| PASS | episodic | the follow-up session's episode carries the case system's outcome code | `latest episode outcome codes: ['NO_CANCELLATION_PROOF']` |

## s4-priya-after-rejection  ·  session  ·  priya  ·  2026-11-20T11:00:00Z

**Customer:** I got your text. Why was the StreamMax dispute rejected, and what can I do now?

- `get_case_status({"case_id": null})` → `{"cases": [{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer states the subscription was cancelled before the 2026-10-28 charge posted.", "status": "rejected", "opened_at": "2026-11-09T10:04:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant states no cancellation request is on record. The cardho …`
- `load_memory({"query": "StreamMax dispute follow-up text"})` → `{"memories": [{"at": "2026-11-12T15:10:00Z", "text": "Conversation on 2026-11-12: Customer asked for a recap and whether dispute C-5001 (transaction T-1002, $15.99 StreamMax charge) was resolved; it remains under review, with follow-up due 2026-11-19. She then asked for updates by text. After identity verification, the assistant changed her contact channel from email to SMS and confirmed the 2026- …`
- `search_policy({"question": "What can a customer do after a dispute is rejected \u2014 appeal or resubmit, deadlines?"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.727, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`
- `find_transactions({"merchant": "StreamMax"})` → `{"transactions": [{"transaction_id": "T-1001", "posted_on": "2026-09-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-1002", "posted_on": "2026-10-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription …`

**Assistant:** Your StreamMax case (C-5001, the $15.99 charge posted 2026-10-28) was rejected on 2026-11-18. The resolution code is **NO_CANCELLATION_PROOF** — StreamMax told us there's no cancellation request on record, so we couldn't support the "cancelled subscription" claim.

What you can do now:

1. **Get proof of cancellation from StreamMax** — the confirmation email or a reference/ticket number showing you cancelled before 2026-10-28.
2. **Re-file the dispute** with that as evidence. StreamMax will get another chance to respond.
3. **Watch the clock**: disputes must be filed within 75 days of the posting date, so for this charge the last day is **2027-01-11**.

To re-file here I'll need to verify you again in this chat (card's last 4 digits and billing ZIP). Want to go ahead? If you have the cancellation reference handy, include it and I'll attach it to the new filing.

One note: only the 2026-10-28 charge was in the case. The earlier 2026-09-28 charge was made before your cancellation, so it can't be disputed on that ground.

**Customer:** OK. Please send me a reminder on November 29 to set up a travel notice for my Porto trip.

- `schedule_reminder({"note": "Set up a travel notice for the Porto trip.", "remind_on": "2026-11-29"})` → `{"followup_id": "F-daa407ce", "due": "2026-11-29"}`

**Assistant:** Done — I've scheduled a reminder for **2026-11-29** to set up your travel notice for Porto. It'll come by text to your usual number.

Heads up: your existing travel notice covers Lisbon only, through 2026-11-30, so Porto won't be covered until you add it. When you're ready, just tell me the Porto dates and I'll set it up.

**Customer:** Before I go, give me a quick recap of everything we've discussed across our conversations.

- `load_memory({"query": "recap of all past conversations, preferences, disputes, travel notices"})` → `{"memories": [{"at": "2026-11-09T10:10:00Z", "text": "Conversation on 2026-11-09: Customer requested a travel notice for Lisbon until 2026-11-30 and email contact; both were stored. She reviewed StreamMax charges and disputed the 2026-10-28 $15.99 charge (transaction T-1002), creating case C-5001 under review with email follow-up due 2026-11-19. She also asked about chargebacks and the foreign tra …`

**Assistant:** Here's the recap:

**Nov 9** — You set up a travel notice for **Lisbon through 2026-11-30** and asked for email contact. You disputed the **2026-10-28 StreamMax charge ($15.99, transaction T-1002)** as a cancelled subscription — that became case **C-5001**. You also asked about chargebacks and the foreign transaction fee (1.25%).

**Nov 12** — You checked in on C-5001 (still under review, follow-up due 2026-11-19) and asked for updates by **text**; after identity verification I switched your contact channel from email to SMS.

**Nov 19** — A scheduled text went out: C-5001 had been **rejected** (code NO_CANCELLATION_PROOF) on 2026-11-18, because StreamMax says there's no cancellation request on record.

**Today** — I explained the rejection: re-file with the merchant's cancellation confirmation (email or reference number). The 75-day dispute window for that charge runs to **2027-01-11**. I also scheduled a **Nov 29 text reminder** to set up a travel notice for your **Porto** trip (Porto isn't covered yet — only Lisbon is, and only until Nov 30).

Open items: re-filing C-5001 with proof of cancellation, and adding Porto to your travel notice.

_Episode written:_ Conversation on 2026-11-20: Customer asked why StreamMax dispute C-5001 (txn T-1002) was rejected and next steps. Assistant explained the NO_CANCELLATION_PROOF rejection and re-filing with cancellation proof; deadline 2027-01-11. Customer requested a 2026-11-29 text reminder to set up a Porto travel notice; scheduled as F-daa407ce. She prefers SMS updates and asked for a recap. Case outcomes: C-5001 rejected (NO_CANCELLATION_PROOF). Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the rejection reason comes from the case system | `[{"case_id": null}]` |
| PASS | external | ...and is relayed (cancellation confirmation) | `Your StreamMax case (C-5001, the $15.99 charge posted 2026-10-28) was rejected on 2026-11-18. The resolution code is **NO_CANCELLATION_PROOF** — StreamMax told us there's no cancellation request on record, so we couldn't …` |
| PASS | prospective | a customer-requested reminder becomes a scheduler record for 2026-11-29 | `[{"trigger_at": "2026-11-29T09:00:00Z", "approval": "none", "status": "pending", "resume": {"note": "Set up a travel notice for the Porto trip."}}]` |
| PASS | episodic | a cross-session recap is built from load_memory run in this session | `[{"query": "StreamMax dispute follow-up text"}, {"query": "recap of all past conversations, preferences, disputes, travel notices"}]` |
| PASS | episodic | ...and uses more than one past episode (StreamMax and the switch to text) | `Here's the recap:  **Nov 9** — You set up a travel notice for **Lisbon through 2026-11-30** and asked for email contact. You disputed the **2026-10-28 StreamMax charge ($15.99, transaction T-1002)** as a cancelled subscr …` |

## scheduler-2026-11-22-a  ·  fire_followups  ·  2026-11-22T18:00:00Z

_outcomes:_ `[{"followup_id": "F-5ea27f3b", "user_id": "marco", "outcome": "awaiting_approval"}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | Marco's follow-up is due but parked: its approval field names ops_reviewer | `[{"followup_id": "F-5ea27f3b", "user_id": "marco", "outcome": "awaiting_approval"}]` |
| PASS | prospective | nothing is sent to Marco without the sign-off | `0 messages` |

## ops-lead-approves-marco  ·  approve_followups  ·  marco

_approved:_ `[{"followup_id": "F-5ea27f3b", "user_id": "marco", "action": "case_status_followup", "trigger_at": "2026-11-22T16:04:00Z", "approval": "ops_reviewer", "status": "pending", "attempts": 0, "approved_by": "ops-lead", "created_at": "2026-11-12T16:04:00Z", "fired_at": null, "done_at": null, "last_error": null, "resume": {"case_id": "C-5002"}}]`

## scheduler-2026-11-22-b  ·  fire_followups  ·  2026-11-22T18:30:00Z

### follow-up session `followup-F-5ea27f3b-1`

**Scheduler:** [scheduled follow-up F-5ea27f3b] action=case_status_followup resume={"case_id": "C-5002"}. The customer is not in this conversation. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `get_case_status({"case_id": "C-5002"})` → `{"cases": [{"case_id": "C-5002", "user_id": "marco", "txn_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer cancelled FitPulse membership in October 2026; $240 annual renewal posted November 3, 2026 after cancellation.", "status": "rejected", "opened_at": "2026-11-12T16:04:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant states no cancellat …`
- `notify_customer({"message": "Update on your dispute C-5002 (FitPulse $240): it was rejected on Nov 18 because the merchant has no cancellation request on record. You can re-file if you send us the merchant's cancella …)` → `{"sent": true, "channel": "secure_message", "message_id": 2}`

**Assistant:** I'll check the case status first.
Done — case C-5002 was checked and the customer was notified via secure message.

**Outcome:** Dispute C-5002 (FitPulse, $240 cancelled-subscription claim) was **rejected** on 2026-11-18 with resolution code `NO_CANCELLATION_PROOF` — the merchant has no cancellation request on record.

**Next step sent to customer:** Re-file with the merchant's cancellation confirmation (email or reference number).

_Episode written:_ Conversation on 2026-11-22: Scheduled follow-up for case C-5002 (transaction T-2002), a FitPulse $240 cancelled-subscription dispute. Checked status: rejected on Nov 18 under NO_CANCELLATION_PROOF because merchant has no cancellation record. Sent one secure message (message_id 2) telling customer to reply with merchant cancellation confirmation to reopen dispute. No customer preference stated. Case outcomes: C-5002 rejected (NO_CANCELLATION_PROOF). Lesson: none

_outcomes:_ `[{"followup_id": "F-5ea27f3b", "user_id": "marco", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | after approval Marco's follow-up fires and completes | `[{"followup_id": "F-5ea27f3b", "user_id": "marco", "outcome": "fired_done", "error": null}]` |
| PASS | prospective | with no channel on file it uses the default secure_message | `[{"message_id": 2, "user_id": "marco", "channel": "secure_message", "body": "Update on your dispute C-5002 (FitPulse $240): it was rejected on Nov 18 because the merchant has no cancellation request on record. You can re …` |

## scheduler-2026-11-22-c  ·  fire_followups  ·  2026-11-22T19:00:00Z

_outcomes:_ `[]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | done flag: a second run fires nothing | `[]` |

## promote-recurring-lesson  ·  promote  ·  2026-11-23T09:00:00Z

_Promoted to v2:_ Ask the cardholder for the merchant’s cancellation confirmation (email or reference number) before calling file_dispute, and pass those confirmation details as evidence_note; if the cardholder cannot provide them, do not call file_dispute.

_Evidence:_ episodes ['E-followup-F-d31c6414-1', 'E-s4-priya-after-rejection', 'E-followup-F-5ea27f3b-1'] from customers ['marco', 'priya']

| | memory type | check | evidence |
|---|---|---|---|
| PASS | procedural | a rule is promoted only from episodes of two different customers | `{"resolution_code": "NO_CANCELLATION_PROOF", "users": ["marco", "priya"], "episodes": ["E-followup-F-d31c6414-1", "E-s4-priya-after-rejection", "E-followup-F-5ea27f3b-1"], "lessons": ["none", "none", "none"], "notes": [" …` |
| PASS | procedural | the promoted rule lives in a new instruction version (v2), now active | `active: v2` |

## s5-dana-under-v2  ·  session  ·  dana  ·  2026-11-24T10:00:00Z

**Customer:** Hi, I'm Dana (card ending 5127, ZIP 60614). I cancelled CloudNest Storage in October but they still charged me $9.99 on November 1. Please dispute it.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`

**Assistant:** Thanks, Dana — you're verified. I found the charge: **CloudNest Storage, $9.99, posted 2026-11-01** (transaction T-3002).

Before I file the dispute as a cancelled subscription, I need proof of your cancellation — the confirmation email or a reference number from CloudNest. Do you have that handy? I'll include it with the dispute.

**Customer:** Sure, the cancellation reference CloudNest gave me is CN-77812.

- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Cancellation reference from CloudNest: CN-77812 (subscription cancelled in October 2026)"})` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-c4bfbc8b", "due": "2026-12-04", "approval": "none", "channel": "secure_message"}}`
- `search_policy({"question": "How long do dispute reviews take and how are customers followed up?"})` → `{"documents": [{"document": "dispute-window", "score": 0.749, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** Done — your dispute is filed.

- **Case ID:** C-5003 (status: under review)
- **Charge:** CloudNest Storage, $9.99, posted 2026-11-01
- **Reason:** cancelled subscription, with your cancellation reference CN-77812 attached as evidence
- **Next step:** we follow up automatically on **2026-12-04** via **secure message**. CloudNest has 10 business days to respond to the dispute.

Note that the October 1 charge of $9.99 was made before you cancelled, so it can't be disputed on these grounds — only the November 1 charge is in this case. Anything else I can help with?

_Episode written:_ Conversation on 2026-11-24: Customer asked to dispute a $9.99 CloudNest Storage charge posted 2026-11-01 after cancelling in October. Assistant verified identity, found T-3002, collected cancellation reference CN-77812, filed case C-5003 under review; follow-up due 2026-12-04 via secure message, and CloudNest has 10 business days to respond. October charge T-3001 was noted not disputable on those grounds. Case outcomes: C-5003 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | procedural | under v2 the agent does not file before asking for the cancellation confirmation | `"not called"` |
| PASS | procedural | ...it asks for it | `Thanks, Dana — you're verified. I found the charge: **CloudNest Storage, $9.99, posted 2026-11-01** (transaction T-3002).  Before I file the dispute as a cancelled subscription, I need proof of your cancellation — the co …` |
| PASS | procedural | ...and files with it as evidence | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Cancellation reference from CloudNest: CN-77812 (subscription cancelled in October 2026)"}]` |

## retraction-drill  ·  retract  ·  2026-11-24T12:00:00Z

_Registry history:_ `[{"event": "baseline", "version": "v1"}, {"event": "promoted", "version": "v2", "based_on": "v1", "by": "ops-lead (scripted reviewer)", "at": "2026-11-23T09:00:00Z"}, {"event": "retracted", "version": "v2", "active_now": "v1", "by": "ops-lead (scripted reviewer)", "reason": "retraction drill: prove a promoted rule can be removed", "at": "2026-11-24T12:00:00Z"}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | procedural | the retraction path restores v1 | `active: v1` |

## s5c-eli-control-under-v1  ·  session  ·  eli  ·  2026-11-24T13:00:00Z

**Customer:** Hi, I'm Eli (card ending 6610, ZIP 73301). I cancelled CloudNest Storage in October but they still charged me $9.99 on November 1. Please dispute it.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer states the CloudNest Storage subscription was cancelled in October 2026; the $9.99 charge posted 2026-11-01. …)` → `{"case_id": "C-5004", "status": "under_review", "followup": {"followup_id": "F-17ad2040", "due": "2026-12-04", "approval": "none", "channel": "secure_message"}}`

**Assistant:** Done — your dispute is filed.

- **Case ID:** C-5004 (status: under review)
- **Charge disputed:** CloudNest Storage, $9.99 on Nov 1, 2026 (transaction T-4002)
- **Reason:** cancelled subscription
- **Follow-up:** due Dec 4, 2026, sent via secure message

Reviews currently take about 10 days, so the Dec 4 follow-up should land around when a decision is expected. Note that there's also an Oct 1 CloudNest charge of $9.99 on your account — let me know if you'd like that one disputed too.

_Episode written:_ Conversation on 2026-11-24: Customer Eli wanted the Nov 1, 2026 CloudNest Storage $9.99 charge disputed after cancelling in October. The assistant verified identity, found the charge, filed dispute T-4002 under case C-5004 (under review), and promised a follow-up by Dec 4, 2026 via secure message. The assistant also noted an Oct 1 charge and offered to dispute it; no other preference was stated. Case outcomes: C-5004 under_review. Lesson: None; the assistant handled the request appropriately by filing the correct disputed transaction, clearly documenting the follow-up date, and offering to review the earlier matching charge.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | procedural | control: the same request under v1 is filed straight away, without the promoted check | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer states the CloudNest Storage subscription was cancelled in October 2026; the $9.99 charge posted 2026-11-01."}]` |

## scheduler-2026-11-29  ·  fire_followups  ·  2026-11-29T18:00:00Z

### follow-up session `followup-F-daa407ce-1`

**Scheduler:** [scheduled follow-up F-daa407ce] action=customer_reminder resume={"note": "Set up a travel notice for the Porto trip."}. The customer is not in this conversation. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `notify_customer({"message": "Reminder: you asked to be reminded to set up a travel notice for your Porto trip. Reply here with your Porto travel dates (and return date) and we'll add the notice so your card isn't blo …)` → `{"sent": true, "channel": "sms", "message_id": 3}`

**Assistant:** Sent the reminder by SMS: it asks the customer to reply with their Porto travel dates so a travel notice can be added.

_Episode written:_ Conversation on 2026-11-29: Customer wanted a reminder to set up a travel notice for their Porto trip. Using case F-daa407ce, the assistant sent one SMS reminder (message_id 3) asking for Porto travel and return dates so the notice could be added. No customer preference was stated. Case outcomes: no case touched. Lesson: none

_outcomes:_ `[{"followup_id": "F-daa407ce", "user_id": "priya", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | Priya's reminder fires on the date she chose | `[{"followup_id": "F-daa407ce", "user_id": "priya", "outcome": "fired_done", "error": null}]` |
| PASS | prospective | the reminder carries its resume note to her current channel | `{"message_id": 3, "user_id": "priya", "channel": "sms", "body": "Reminder: you asked to be reminded to set up a travel notice for your Porto trip. Reply here with your Porto travel dates (and return date) and we'll add t …` |

## s6a-priya-staleness  ·  session  ·  priya  ·  2026-12-03T10:00:00Z

**Customer:** I'm in Porto now and just saw a charge from Livraria Porto. Is my travel notice still active?

- `load_memory({"query": "travel notice Porto"})` → `{"memories": [{"at": "2026-11-29T18:00:00Z", "text": "Conversation on 2026-11-29: Customer wanted a reminder to set up a travel notice for their Porto trip. Using case F-daa407ce, the assistant sent one SMS reminder (message_id 3) asking for Porto travel and return dates so the notice could be added. No customer preference was stated. Case outcomes: no case touched. Lesson: none", "similarity": 0. …`

**Assistant:** No — there's no travel notice on your account right now, so nothing is active for Porto.

What I can see from our history: your earlier notice covered Lisbon only through 2026-11-30, and the SMS reminder on 2026-11-29 asking for your Porto dates was never followed up with them, so a Porto notice was never added.

Want me to set one up now? I just need your return date, e.g. "Porto, back 2026-12-15."

_Episode written:_ Conversation on 2026-12-03: Customer in Porto asked whether their travel notice was active after seeing a Livraria Porto charge. Assistant checked history and said no active Porto notice: the prior Lisbon notice ended 2026-11-30, and case F-daa407ce's 2026-11-29 SMS request for Porto dates got no follow-up. Assistant offered to set up a notice and asked for the return date. No preference stated. Case outcomes: C-5001 rejected (NO_CANCELLATION_PROOF). Lesson: Ask for both the Porto travel date and return date upfront when setting up the travel notice, not only the return date.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | staleness: the Lisbon notice expired on 2026-11-30 and is deleted at turn start, not by any tool | `null` |
| PASS | semantic | ...the agent did not delete it itself | `"not called"` |
| PASS | semantic | staleness: the reply says no notice is active | `No — there's no travel notice on your account right now, so nothing is active for Porto.  What I can see from our history: your earlier notice covered Lisbon only through 2026-11-30, and the SMS reminder on 2026-11-29 as …` |
| PASS | semantic | staleness: the expired Lisbon notice is not presented as current | `No — there's no travel notice on your account right now, so nothing is active for Porto.  What I can see from our history: your earlier notice covered Lisbon only through 2026-11-30, and the SMS reminder on 2026-11-29 as …` |

## s6b-priya-forgetting-and-secrets  ·  session  ·  priya  ·  2026-12-03T10:30:00Z

**Customer:** Please set a travel notice for Porto until December 10.

- `remember_customer_fact({"key": "travel_notice", "value": "Porto", "valid_until": "2026-12-10"})` → `{"stored": {"travel_notice": {"value": "Porto", "as_of": "2026-12-03T10:30:00Z", "valid_until": "2026-12-10", "expires_at": "2026-12-11T00:00:00Z"}}, "replaced": null}`

**Assistant:** Done — I've noted a travel notice for Porto through December 10, 2026. Anything else before your trip?

**Customer:** Actually, on second thought, delete that travel notice. I'd rather you didn't keep my travel plans.

- `forget_customer_fact({"key": "travel_notice"})` → `{"forgotten": "travel_notice", "had_value": true}`

**Assistant:** The travel notice is deleted — I'm no longer keeping any travel plans on file for you.

**Customer:** In case you need it, my full card number is [REDACTED CARD NUMBER].

**Assistant:** Thanks, but I don't need that — your full card number has been masked and isn't stored. If we ever need to verify you, I'll just ask for the last 4 digits and billing ZIP.

_Episode written:_ Conversation on 2026-12-03: Customer asked to set a Porto travel notice through December 10, 2026, then reversed and asked to delete it, preferring no travel plans kept. The notice was stored then deleted. No case or transaction IDs were provided. Customer volunteered a full card number; assistant said it was masked/not stored and verification uses last 4 digits plus billing ZIP. Case outcomes: no case touched. Lesson: Confirm whether the customer wants travel-plan data retained before storing it, since this customer later asked for deletion and said they preferred no travel plans kept.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | a new fact can be written | `[{"key": "travel_notice", "value": "Porto", "valid_until": "2026-12-10"}]` |
| PASS | semantic | deletion on request: forget_customer_fact runs | `[{"key": "travel_notice"}]` |
| PASS | semantic | ...and the fact is gone from the store | `null` |
| PASS | guard | a pasted card number is masked before it enters the session | `In case you need it, my full card number is [REDACTED CARD NUMBER].` |
| PASS | guard | the card number is in no store: sessions, memory, bank, scheduler | `found in: nowhere` |

## s7-parametric-ablation  ·  session  ·  priya  ·  2026-12-03T11:00:00Z

_Tools removed for this session: search_policy_

**Customer:** What foreign transaction fee does Kestrel charge on euro purchases?

**Assistant:** I don't have the policy lookup tool available in this session, so I can't retrieve Kestrel's current foreign transaction fee — and I won't guess at a number. Please check the fees section of your cardholder agreement, or ask again a bit later and I'll look it up.

_Episode written:_ Conversation on 2026-12-03: Customer asked what foreign transaction fee Kestrel charges on euro purchases. The assistant could not access the policy lookup tool, declined to guess, advised checking the cardholder agreement’s fees section, or asking again later for a lookup. No case or transaction IDs were provided, no specific follow-up was promised, and no preference was stated. Case outcomes: no case touched. Lesson: When the policy lookup tool is unavailable, the assistant should offer a clear escalation or callback path instead of only directing the customer to the cardholder agreement.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | parametric | with retrieval removed the agent still engages with the fee question | `I don't have the policy lookup tool available in this session, so I can't retrieve Kestrel's current foreign transaction fee — and I won't guess at a number. Please check the fees section of your cardholder agreement, or …` |
| PASS | parametric | ...but the weights cannot supply Kestrel's 1.25% | `I don't have the policy lookup tool available in this session, so I can't retrieve Kestrel's current foreign transaction fee — and I won't guess at a number. Please check the fees section of your cardholder agreement, or …` |

## s7b-bare-weights-probe  ·  parametric_probe  ·  2026-12-03T11:10:00Z

**Customer:** What foreign transaction fee does Kestrel Card charge on euro purchases? Answer with a number.

**Assistant:** 0

| | memory type | check | evidence |
|---|---|---|---|
| PASS | parametric | the bare model (no instruction, no tools) still answers with a figure from the weights | `0` |
| PASS | parametric | ...and the weights do not hold Kestrel's 1.25%: the floor is generic, not this issuer's | `0` |

## retention-2027-06-15  ·  retention_sweep  ·  2027-06-15T00:00:00Z

_purged:_ `["E-s1-priya-first-contact", "E-s2-priya-returns", "E-s3-marco-other-customer", "E-followup-F-d31c6414-1", "E-s4-priya-after-rejection", "E-followup-F-5ea27f3b-1", "E-s5-dana-under-v2", "E-s5c-eli-control-under-v1", "E-followup-F-daa407ce-1", "E-s6a-priya-staleness", "E-s6b-priya-forgetting-and-secrets", "E-s7-parametric-ablation"]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | forgetting on purpose: episodes past their 180-day retention are deleted | `0 episodes; purged 12` |

## s8-priya-after-retention  ·  session  ·  priya  ·  2027-06-15T10:00:00Z

**Customer:** Hi! What did we talk about last time?

- `load_memory({"query": "last conversation summary"})` → `{"memories": []}`

**Assistant:** I don't have any record of our previous conversation — nothing came up when I checked. The only thing I have on file for you is your contact preference (SMS).

Is there something I can help you with today?

_Episode written:_ Conversation on 2027-06-15: Customer asked what was discussed in their last conversation. The assistant checked long-term memory, found no prior records, and said only the customer’s SMS contact preference was on file. No case or transaction ID was provided, and no follow-up was promised. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | recall after retention finds nothing, because nothing is kept | `{"memories": []}` |
