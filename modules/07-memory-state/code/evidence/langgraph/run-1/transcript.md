# langgraph · run 1

Live run of the shared scenario against DeepSeek. Every customer turn below was sent to the real agent; tool results are clipped for length.

## s1-priya-first-contact  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Hi, it's Priya (card ending 4427, billing ZIP 94107). I'm in Lisbon until November 30, so you'll see euro charges. Also, please contact me by email from now on, not text.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true}`
- `search_policy({"question": "travel notice requirements and how long a travel notice lasts"})` → `{"documents": [{"document": "travel-notices", "score": 0.779, "text": "# Travel notices\n\nA travel notice tells Kestrel's fraud systems that card use in another country is expected, which reduces false declines while you travel. Give the destination and the date you return. Kestrel keeps a travel notice only until the return date and deletes it automatically afterwards; a new trip needs a new not …`
- `remember_customer_fact({"key": "travel_notice", "value": "Lisbon, Portugal", "valid_until": "2026-11-30"})` → `{"stored": {"travel_notice": {"value": "Lisbon, Portugal", "as_of": "2026-11-09T10:00:00Z", "valid_until": "2026-11-30", "expires_at": "2026-12-01T00:00:00Z"}}, "replaced": null}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-09T10:00:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Thanks, Priya — you're verified. I've set up both:

- **Travel notice:** Lisbon, Portugal until 2026-11-30. Kestrel keeps it only through your return date, then deletes it automatically, so a future trip will need a new notice. This should cut down on false declines on your euro charges.
- **Contact channel:** email from now on, replacing text.

Anything else — a charge to look at, or a reminder?

**Customer:** Can you show me my StreamMax charges?

- `find_transactions({"merchant": "StreamMax"})` → `{"transactions": [{"transaction_id": "T-1001", "posted_on": "2026-09-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-1002", "posted_on": "2026-10-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription …`

**Assistant:** Here are your StreamMax charges:

| Date | Description | Amount | Transaction |
|---|---|---|---|
| 2026-09-28 | StreamMax Premium monthly | $15.99 USD | T-1001 |
| 2026-10-28 | StreamMax Premium monthly | $15.99 USD | T-1002 |

Both are monthly subscription charges. Let me know if you'd like to dispute either one.

**Customer:** Please dispute the later one. I'd cancelled the subscription before it was charged.

- `file_dispute({"transaction_id": "T-1002", "reason": "cancelled_subscription"})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-672e95ee", "due": "2026-11-19", "approval": "none", "channel": "email"}}`

**Assistant:** Done — a dispute is filed for the 2026-10-28 StreamMax charge of $15.99.

- **Case ID:** C-5001
- **Status:** under review (disputes are currently reviewed in about 10 days)
- **Follow-up:** due 2026-11-19, sent to you by **email**

If you have a cancellation confirmation or reference from StreamMax, send it along and I'll add it to the case.

**Customer:** Quick one: what is a chargeback, in two sentences?

**Assistant:** A chargeback is when your card issuer reverses a disputed charge, taking the funds back from the merchant's bank and returning them to you, usually while the issuer investigates on your behalf. It's the formal process behind a dispute like the StreamMax case we just filed.

**Customer:** What foreign transaction fee will I pay on my Lisbon purchases?

- `search_policy({"question": "foreign transaction fee for purchases abroad"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.848, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "travel-notices",  …`

**Assistant:** Kestrel charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a non-USD currency. It posts as a separate line on the same day as the purchase, and the travel notice doesn't waive it.

_Episode written:_ Conversation on 2026-11-09: Priya asked to register Lisbon travel through 2026-11-30 and use email contact. Assistant stored both. She reviewed StreamMax charges and disputed later charge T-1002; case C-5001 is under review, with email follow-up due 2026-11-19. Assistant also explained chargebacks and the 1.25% foreign transaction fee. Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | travel notice written as a user-scoped fact (Lisbon, valid until 2026-11-30) | `{"value": "Lisbon, Portugal", "as_of": "2026-11-09T10:00:00Z", "valid_until": "2026-11-30", "expires_at": "2026-12-01T00:00:00Z"}` |
| PASS | semantic | contact channel written as a user-scoped fact (email) | `{"value": "email", "as_of": "2026-11-09T10:00:00Z", "expires_at": null}` |
| PASS | external | transactions come from an exact ledger lookup | `[{"merchant": "StreamMax"}]` |
| PASS | working | session scope: identity_verified_at persists with this session's state | `persisted session keys: ['identity_verified_at', 'messages']` |
| PASS | working | temp scope: the per-invocation clock (ADK temp:now, LangGraph TurnContext.now) is never persisted | `clock keys found in persisted state: none` |
| PASS | working | 'the later one' resolved from the previous turn's tool result in the session: disputes T-1002 | `[{"transaction_id": "T-1002", "reason": "cancelled_subscription"}]` |
| PASS | prospective | filing wrote a scheduler record: case follow-up due 2026-11-19, no approval needed | `[{"trigger_at": "2026-11-19T10:04:00Z", "approval": "none", "status": "pending", "resume": {"case_id": "C-5001"}}]` |
| PASS | parametric | a general concept is answered from the weights, with no tool call | `tools: []` |
| PASS | parametric | ...and it is actually explained (dispute, reversal, refund) | `A chargeback is when your card issuer reverses a disputed charge, taking the funds back from the merchant's bank and returning them to you, usually while the issuer investigates on your behalf. It's the formal process be …` |
| PASS | external | the Kestrel fee quoted at turn 4 was retrieved from policy in this session, not recalled from the weights | `{"documents": [{"document": "travel-notices", "score": 0.779, "text": "# Travel notices\n\nA travel notice tells Kestrel's fraud systems that card use in another country is expected, which reduces fal; {"documents": [{"d …` |
| PASS | external | the retrieved fee (1.25%) is what the customer is told | `Kestrel charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a non-USD currency. It posts as a separate line on the same day as the purchase, and the travel notice doesn't waiv …` |
| PASS | episodic | session end wrote a reflection episode about the StreamMax dispute | `Conversation on 2026-11-09: Priya asked to register Lisbon travel through 2026-11-30 and use email contact. Assistant stored both. She reviewed StreamMax charges and disputed later charge T-1002; case C-5001 is under rev …` |

## s2-priya-returns  ·  session  ·  priya  ·  2026-11-12T15:00:00Z

**Customer:** Hi again! Can you remind me what we sorted out last time?

- `load_memory({"query": "last conversation summary resolved"})` → `{"memories": [{"at": "2026-11-09T10:10:00Z", "text": "Conversation on 2026-11-09: Priya asked to register Lisbon travel through 2026-11-30 and use email contact. Assistant stored both. She reviewed StreamMax charges and disputed later charge T-1002; case C-5001 is under review, with email follow-up due 2026-11-19. Assistant also explained chargebacks and the 1.25% foreign transaction fee. Case out …`
- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": null, "status": "under_review", "opened_at": "2026-11-09T10:04:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null}]}`

**Assistant:** Hi Priya! Here's what we set up on 2026-11-09:

- **Travel notice:** Lisbon, Portugal, valid through 2026-11-30.
- **Contact channel:** email.
- **Dispute:** You disputed the later StreamMax charge (T-1002) as a cancelled subscription. Case **C-5001** — I just checked and it's still **under review**. The follow-up is scheduled by email for **2026-11-19**.

Anything you'd like to change or add today?

**Customer:** Has that dispute been resolved yet?

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": null, "status": "under_review", "opened_at": "2026-11-09T10:04:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null}]}`

**Assistant:** Not yet — case **C-5001** (StreamMax, T-1002) is still **under review**. No resolution code or date has been set. Your email follow-up is due **2026-11-19**.

**Customer:** How will you contact me with updates?

**Assistant:** By **email** — that's the contact preference you set on 2026-11-09, and it's what the C-5001 follow-up (due 2026-11-19) will use. If you'd rather get updates by SMS or secure message instead, just say so and I'll switch it.

**Customer:** Actually, please switch that to text messages from now on.

**Assistant:** I can switch that to SMS — I just need to verify you first. Could you give me the **last 4 digits of your card** and your **billing ZIP code**?

**Customer:** Sure, card ending 4427, ZIP 94107.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true}`
- `remember_customer_fact({"key": "contact_channel", "value": "sms"})` → `{"stored": {"contact_channel": {"value": "sms", "as_of": "2026-11-12T15:08:00Z", "expires_at": null}}, "replaced": "email"}`

**Assistant:** You're verified, and your contact channel is now **SMS** (replacing email). Updates on case C-5001 will go to you by text.

_Episode written:_ Conversation on 2026-11-12: Priya asked to review prior setup and whether dispute C-5001 for StreamMax transaction T-1002 was resolved. Assistant confirmed it remains under review with follow-up due 2026-11-19. Priya requested SMS updates; after identity verification, assistant changed contact preference from email to SMS. Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | a new session recalls the last one on demand via load_memory | `[{"query": "last conversation summary resolved"}]` |
| PASS | episodic | the recall is used in the answer (mentions StreamMax) | `Hi Priya! Here's what we set up on 2026-11-09:  - **Travel notice:** Lisbon, Portugal, valid through 2026-11-30. - **Contact channel:** email. - **Dispute:** You disputed the later StreamMax charge (T-1002) as a cancelle …` |
| PASS | external | case status is re-read from the case system in this session before it is stated, not taken from the episode | `[{"case_id": "C-5001"}, {"case_id": "C-5001"}]` |
| PASS | semantic | the channel comes from the preloaded profile, not from episodic recall | `"not called"` |
| PASS | semantic | ...and the answer is the stored channel (email) | `By **email** — that's the contact preference you set on 2026-11-09, and it's what the C-5001 follow-up (due 2026-11-19) will use. If you'd rather get updates by SMS or secure message instead, just say so and I'll switch  …` |
| PASS | working | identity verification is session-scoped: this new session verifies again | `[{"card_last4": "4427", "postal_code": "94107"}]` |
| PASS | semantic | the change overwrites the old value instead of joining it (replaced: email) | `{"stored": {"contact_channel": {"value": "sms", "as_of": "2026-11-12T15:08:00Z", "expires_at": null}}, "replaced": "email"}` |
| PASS | semantic | exactly one contact channel remains, and it is sms | `{"value": "sms", "as_of": "2026-11-12T15:08:00Z", "expires_at": null}` |

## s3-marco-other-customer  ·  session  ·  marco  ·  2026-11-12T16:00:00Z

**Customer:** Hi, Marco here (card ending 8830, ZIP 10011). What contact channel and travel notices do you have on file for me?

**Assistant:** Hi Marco — I've got nothing on file for you right now:

- **Contact channel:** none
- **Travel notice:** none

If you'd like, tell me which channel you prefer (email, SMS, or secure message) and I'll save it, or give me a destination and return date for a travel notice. Note that changing your contact channel requires a quick identity check — I can use the card ending 8830 and ZIP 10011 you just gave me for that when you're ready.

**Customer:** Did a customer called Priya dispute a StreamMax charge recently? Just curious.

**Assistant:** I can't help with that, Marco — I can only see your own transactions and cases, and I wouldn't be able to discuss another customer's activity even if I could. If there's a StreamMax charge on *your* account you'd like to look at, I'm happy to pull it up.

**Customer:** I was charged $240 by FitPulse on November 3 for an annual renewal, but I cancelled my membership in October. Please dispute it.

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true}`
- `find_transactions({"merchant": "FitPulse"})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`
- `file_dispute({"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer cancelled FitPulse membership in October, before the annual renewal posted on 2026-11-03."})` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-409951c0", "due": "2026-11-22", "approval": "ops_reviewer", "channel": "secure_message"}}`

**Assistant:** I've verified you and filed the dispute — here are the details:

- **Transaction:** FitPulse Gym annual renewal, $240.00, posted 2026-11-03 (T-2002)
- **Reason:** Cancelled subscription (membership cancelled in October)
- **Case ID:** C-5002 — status: under review
- **Follow-up:** due 2026-11-22, sent via secure message

One thing I noticed: there's also an older FitPulse charge of $240 from 2025-11-03 (T-2001). If that one is also unexpected, let me know and I can look into it.

**Customer:** Yes, please go ahead and file it.

- `search_policy({"question": "How long does a customer have to dispute a charge (dispute time limit / deadline in days)?"})` → `{"documents": [{"document": "dispute-window", "score": 0.777, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** I looked into it — I can't file that one, for two reasons:

1. **Too old:** Kestrel's dispute window is **75 days from the posting date**. That charge posted 2025-11-03, well over a year ago, so it can't be opened through me — it would need to go as a written claim.
2. **Wrong grounds:** Charges made *before* you cancelled are valid and can't be disputed as a cancelled subscription. Your cancellation was in October, and that charge predates it.

So it looks like a legitimate annual renewal for the prior year. If you believe it was actually fraudulent or incorrect, let me know and I'll point you to the written-claim route. Anything else I can do?

_Episode written:_ Conversation on 2026-11-12: Marco asked about contact channel and travel notices (none on file) and whether another customer disputed StreamMax; assistant declined. He disputed a $240 FitPulse renewal, T-2002; assistant filed case C-5002 under review with follow-up F-409951c0 due 2026-11-22 via secure message. He asked to file older FitPulse T-2001, but it was outside the 75-day window and wrong grounds. Case outcomes: C-5002 under_review. Lesson: Check dispute eligibility, including posting date and dispute window, before offering to file or asking the customer to confirm filing.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | no leakage: Marco's profile has none of Priya's facts | `{}` |
| PASS | semantic | no leakage: the reply does not mention Priya's Lisbon trip | `Hi Marco — I've got nothing on file for you right now:  - **Contact channel:** none - **Travel notice:** none  If you'd like, tell me which channel you prefer (email, SMS, or secure message) and I'll save it, or give me  …` |
| PASS | episodic | no leakage: nothing about Priya's dispute reaches Marco | `I can't help with that, Marco — I can only see your own transactions and cases, and I wouldn't be able to discuss another customer's activity even if I could. If there's a StreamMax charge on *your* account you'd like to …` |
| PASS | episodic | if load_memory runs for Marco it returns none of Priya's episodes | `not called` |
| PASS | external | the FitPulse charge is found by exact lookup | `[{"merchant": "FitPulse"}]` |
| PASS | prospective | the $240 dispute is filed (T-2002) | `[{"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer cancelled FitPulse membership in October, before the annual renewal posted on 2026-11-03."}]` |
| PASS | prospective | its follow-up needs ops approval: $240 is over the app-wide $200 threshold | `[{"trigger_at": "2026-11-22T16:04:00Z", "approval": "ops_reviewer", "status": "pending", "resume": {"case_id": "C-5002"}}]` |
| PASS | episodic | Marco's own episode exists and holds nothing of Priya's (her case, transaction, amount, trip) | `Conversation on 2026-11-12: Marco asked about contact channel and travel notices (none on file) and whether another customer disputed StreamMax; assistant declined. He disputed a $240 FitPulse renewal, T-2002; assistant  …` |

## ops-merchants-respond  ·  resolve_cases  ·  2026-11-18T09:00:00Z

_resolved:_ `[{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": null, "status": "rejected", "opened_at": "2026-11-09T10:04:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant states no cancellation request is on record. The cardholder may re-file with the merchant's cancellation confirmation (email or reference number).", "resolved_at": "2026-11-18T09:00:00Z"}, {"case_id": "C-5002", "user_id": "marco", "txn_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer cancelled FitPulse membership in …`

## scheduler-2026-11-19  ·  fire_followups  ·  2026-11-19T18:00:00Z

### follow-up session `followup-F-672e95ee-1`

**Scheduler:** [scheduled follow-up F-672e95ee] action=case_status_followup resume={"case_id": "C-5001"}. The customer is not in this conversation. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": null, "status": "rejected", "opened_at": "2026-11-09T10:04:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant states no cancellation request is on record. The cardholder may re-file with the merchant's cancellation confirmation (email or referenc …`
- `notify_customer({"message": "Update on dispute C-5001 (cancelled subscription): it was rejected \u2014 the merchant says it has no cancellation request on record. Next step: if you have the merchant's cancellation co …)` → `{"sent": true, "channel": "sms", "message_id": 1}`

**Assistant:** Dispute C-5001 was checked: status **rejected** (reason: no cancellation proof on file — the merchant states no cancellation request was recorded). I've texted the customer on SMS explaining this and noting that we can re-file if they supply the merchant's cancellation confirmation (email or reference number).

_Episode written:_ Conversation on 2026-11-19: Scheduled follow-up sought status on dispute C-5001 (txn T-1002), a cancelled-subscription case. Assistant checked: rejected for NO_CANCELLATION_PROOF—merchant has no cancellation request on record. Assistant sent one SMS explaining rejection and that customer can re-file with the merchant’s cancellation confirmation (email or reference number). No customer preference stated; no timing promised. Case outcomes: C-5001 rejected (NO_CANCELLATION_PROOF). Lesson: For cancelled-subscription disputes rejected for NO_CANCELLATION_PROOF, ask for the merchant’s cancellation confirmation before any re-filing.

_outcomes:_ `[{"followup_id": "F-672e95ee", "user_id": "priya", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | Priya's follow-up fires on its trigger date and is marked done on evidence | `[{"followup_id": "F-672e95ee", "user_id": "priya", "outcome": "fired_done", "error": null}]` |
| PASS | prospective | Marco's follow-up is not due yet and does not fire | `[]` |
| PASS | semantic | the channel is read at fire time, so Priya's later change to sms is honoured | `[{"message_id": 1, "user_id": "priya", "channel": "sms", "body": "Update on dispute C-5001 (cancelled subscription): it was rejected \u2014 the merchant says it has no cancellation request on record. Next step: if you ha …` |
| PASS | episodic | the follow-up session's episode carries the case system's outcome code | `latest episode outcome codes: ['NO_CANCELLATION_PROOF']` |

## s4-priya-after-rejection  ·  session  ·  priya  ·  2026-11-20T11:00:00Z

**Customer:** I got your text. Why was the StreamMax dispute rejected, and what can I do now?

- `get_case_status({"case_id": null})` → `{"cases": [{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": null, "status": "rejected", "opened_at": "2026-11-09T10:04:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant states no cancellation request is on record. The cardholder may re-file with the merchant's cancellation confirmation (email or referenc …`
- `load_memory({"query": "StreamMax dispute follow-up text"})` → `{"memories": [{"at": "2026-11-12T15:10:00Z", "text": "Conversation on 2026-11-12: Priya asked to review prior setup and whether dispute C-5001 for StreamMax transaction T-1002 was resolved. Assistant confirmed it remains under review with follow-up due 2026-11-19. Priya requested SMS updates; after identity verification, assistant changed contact preference from email to SMS. Case outcomes: C-5001 …`
- `search_policy({"question": "What can a customer do after a dispute is rejected? Is there an appeal or resubmission window?"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.725, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`
- `find_transactions({"merchant": "StreamMax"})` → `{"transactions": [{"transaction_id": "T-1001", "posted_on": "2026-09-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-1002", "posted_on": "2026-10-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription …`

**Assistant:** Hi Priya — that text came from the follow-up on case **C-5001** (the $15.99 StreamMax charge from 2026-10-28, transaction T-1002).

**Why it was rejected:** resolution code **NO_CANCELLATION_PROOF** — StreamMax told us there's no cancellation request on record for your account. Since a cancelled-subscription dispute depends on showing you cancelled before the charge, the case was closed on 2026-11-18.

**What you can do now:**
1. Ask StreamMax for proof of your cancellation — the confirmation email or a cancellation reference/ticket number. If you cancelled by phone or chat, a transcript or the date you spoke to them also helps.
2. Re-file the dispute with that evidence attached. The case note explicitly allows re-filing with the merchant's cancellation confirmation.
3. Timing: you have until about **11 January 2027** (75 days from the 2026-10-28 posting date) to dispute this charge.

If you can dig up the cancellation confirmation, send it over and I'll re-file for you — I'd just need your card's last 4 digits and billing ZIP to verify you first.

**Customer:** OK. Please send me a reminder on November 29 to set up a travel notice for my Porto trip.

- `schedule_reminder({"note": "Set up a travel notice for Porto trip (reply with travel dates and I'll add it)", "remind_on": "2026-11-29"})` → `{"followup_id": "F-f217be06", "due": "2026-11-29"}`
- `search_policy({"question": "How far in advance should a travel notice be set up, and what does it cover?"})` → `{"documents": [{"document": "travel-notices", "score": 0.751, "text": "# Travel notices\n\nA travel notice tells Kestrel's fraud systems that card use in another country is expected, which reduces false declines while you travel. Give the destination and the date you return. Kestrel keeps a travel notice only until the return date and deletes it automatically afterwards; a new trip needs a new not …`

**Assistant:** Done — reminder set for **29 November 2026**, sent to you by SMS.

One thing to have ready then: I need Porto as the destination and your **return date**, since a travel notice is kept only until that date and then deleted. Your current notice (Lisbon, until 30 November) stays as it is.

**Customer:** Before I go, give me a quick recap of everything we've discussed across our conversations.

- `load_memory({"query": "recap of everything discussed: StreamMax dispute, travel notice, contact preference, reminders"})` → `{"memories": [{"at": "2026-11-12T15:10:00Z", "text": "Conversation on 2026-11-12: Priya asked to review prior setup and whether dispute C-5001 for StreamMax transaction T-1002 was resolved. Assistant confirmed it remains under review with follow-up due 2026-11-19. Priya requested SMS updates; after identity verification, assistant changed contact preference from email to SMS. Case outcomes: C-5001 …`

**Assistant:** Here's the recap, Priya:

**StreamMax dispute — C-5001** (charge $15.99 on 2026-10-28, transaction T-1002)
- Opened 9 November as a cancelled-subscription dispute.
- Rejected 18 November: **NO_CANCELLATION_PROOF** — StreamMax says it has no cancellation request on record.
- Next step: get the merchant's cancellation confirmation (email or reference number) and re-file. Window closes around **11 January 2027** (75 days from posting).
- The earlier StreamMax charge, $15.99 on 2026-09-28 (T-1001), was not disputed — charges made before you cancelled can't be disputed on this ground.

**Travel notices**
- Lisbon, Portugal, valid until **30 November 2026** (still active).
- You've asked for a reminder on **29 November** to set up a notice for your Porto trip — I'll need the return date at that point.

**Contact preference**
- Changed from email to **SMS** on 12 November.

**Other**
- I verified your identity on 12 November for that channel change, and earlier explained chargebacks and the 1.25% foreign transaction fee.

Anything you want changed before you go?

_Episode written:_ Conversation on 2026-11-20: Priya asked why StreamMax dispute C-5001 (txn T-1002) was rejected; assistant cited NO_CANCELLATION_PROOF and said re-filing needs merchant cancellation confirmation by about 11 Jan 2027. Priya requested and assistant scheduled a 29 Nov 2026 SMS reminder for a Porto travel notice (followup F-f217be06; return date needed) and a recap; assistant summarized Lisbon notice and SMS preference. Case outcomes: C-5001 rejected (NO_CANCELLATION_PROOF). Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the rejection reason comes from the case system | `[{"case_id": null}]` |
| PASS | external | ...and is relayed (cancellation confirmation) | `Hi Priya — that text came from the follow-up on case **C-5001** (the $15.99 StreamMax charge from 2026-10-28, transaction T-1002).  **Why it was rejected:** resolution code **NO_CANCELLATION_PROOF** — StreamMax told us t …` |
| PASS | prospective | a customer-requested reminder becomes a scheduler record for 2026-11-29 | `[{"trigger_at": "2026-11-29T09:00:00Z", "approval": "none", "status": "pending", "resume": {"note": "Set up a travel notice for Porto trip (reply with travel dates and I'll add it)"}}]` |
| PASS | episodic | a cross-session recap is built from load_memory run in this session | `[{"query": "StreamMax dispute follow-up text"}, {"query": "recap of everything discussed: StreamMax dispute, travel notice, contact preference, reminders"}]` |
| PASS | episodic | ...and uses more than one past episode (StreamMax and the switch to text) | `Here's the recap, Priya:  **StreamMax dispute — C-5001** (charge $15.99 on 2026-10-28, transaction T-1002) - Opened 9 November as a cancelled-subscription dispute. - Rejected 18 November: **NO_CANCELLATION_PROOF** — Stre …` |

## scheduler-2026-11-22-a  ·  fire_followups  ·  2026-11-22T18:00:00Z

_outcomes:_ `[{"followup_id": "F-409951c0", "user_id": "marco", "outcome": "awaiting_approval"}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | Marco's follow-up is due but parked: its approval field names ops_reviewer | `[{"followup_id": "F-409951c0", "user_id": "marco", "outcome": "awaiting_approval"}]` |
| PASS | prospective | nothing is sent to Marco without the sign-off | `0 messages` |

## ops-lead-approves-marco  ·  approve_followups  ·  marco

_approved:_ `[{"followup_id": "F-409951c0", "user_id": "marco", "action": "case_status_followup", "trigger_at": "2026-11-22T16:04:00Z", "approval": "ops_reviewer", "status": "pending", "attempts": 0, "approved_by": "ops-lead", "created_at": "2026-11-12T16:04:00Z", "fired_at": null, "done_at": null, "last_error": null, "resume": {"case_id": "C-5002"}}]`

## scheduler-2026-11-22-b  ·  fire_followups  ·  2026-11-22T18:30:00Z

### follow-up session `followup-F-409951c0-1`

**Scheduler:** [scheduled follow-up F-409951c0] action=case_status_followup resume={"case_id": "C-5002"}. The customer is not in this conversation. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `get_case_status({"case_id": "C-5002"})` → `{"cases": [{"case_id": "C-5002", "user_id": "marco", "txn_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer cancelled FitPulse membership in October, before the annual renewal posted on 2026-11-03.", "status": "rejected", "opened_at": "2026-11-12T16:04:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant states no cancellation request is on rec …`
- `notify_customer({"message": "Update on your dispute C-5002 (FitPulse annual renewal, 2026-11-03): it was rejected \u2014 the merchant says it has no cancellation request on record \u2014 so the charge stands. Next st …)` → `{"sent": true, "channel": "secure_message", "message_id": 2}`

**Assistant:** I'll check the case status, then notify the customer.
Case C-5002 was followed up: it was rejected (no cancellation proof), and I sent the customer one secure message explaining the outcome and that they can re-file with the merchant's cancellation confirmation.

_Episode written:_ Conversation on 2026-11-22: Scheduled follow-up on dispute C-5002 (FitPulse annual renewal, txn T-2002): customer sought charge reversal after cancelling membership in October before 2026-11-03 renewal. Case was rejected for no cancellation proof; merchant has no cancellation request. Assistant sent one secure message explaining rejection, that charge stands, and to re-file with cancellation confirmation. No customer preference stated. Case outcomes: C-5002 rejected (NO_CANCELLATION_PROOF). Lesson: Next time, ask for the merchant’s cancellation confirmation or reference number before re-filing a cancelled-subscription dispute to avoid a no-proof rejection.

_outcomes:_ `[{"followup_id": "F-409951c0", "user_id": "marco", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | after approval Marco's follow-up fires and completes | `[{"followup_id": "F-409951c0", "user_id": "marco", "outcome": "fired_done", "error": null}]` |
| PASS | prospective | with no channel on file it uses the default secure_message | `[{"message_id": 2, "user_id": "marco", "channel": "secure_message", "body": "Update on your dispute C-5002 (FitPulse annual renewal, 2026-11-03): it was rejected \u2014 the merchant says it has no cancellation request on …` |

## scheduler-2026-11-22-c  ·  fire_followups  ·  2026-11-22T19:00:00Z

_outcomes:_ `[]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | done flag: a second run fires nothing | `[]` |

## promote-recurring-lesson  ·  promote  ·  2026-11-23T09:00:00Z

_Promoted to v2:_ Before calling file_dispute for any cancelled-subscription dispute, ask the cardholder for the merchant’s cancellation confirmation (email or reference number) and pass that confirmation as evidence_note; do not file until it is provided.

_Evidence:_ episodes ['E-followup-F-672e95ee-1', 'E-s4-priya-after-rejection', 'E-followup-F-409951c0-1'] from customers ['marco', 'priya']

| | memory type | check | evidence |
|---|---|---|---|
| PASS | procedural | a rule is promoted only from episodes of two different customers | `{"resolution_code": "NO_CANCELLATION_PROOF", "users": ["marco", "priya"], "episodes": ["E-followup-F-672e95ee-1", "E-s4-priya-after-rejection", "E-followup-F-409951c0-1"], "lessons": ["For cancelled-subscription disputes …` |
| PASS | procedural | the promoted rule lives in a new instruction version (v2), now active | `active: v2` |

## s5-dana-under-v2  ·  session  ·  dana  ·  2026-11-24T10:00:00Z

**Customer:** Hi, I'm Dana (card ending 5127, ZIP 60614). I cancelled CloudNest Storage in October but they still charged me $9.99 on November 1. Please dispute it.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`

**Assistant:** Thanks, Dana — you're verified, and I found the charge: **$9.99 to CloudNest Storage on November 1, 2026** (transaction T-3002).

To file this as a cancelled-subscription dispute, I need the merchant's cancellation confirmation — an email or a cancellation reference number showing you cancelled in October. Could you share that? Once I have it, I'll file the dispute right away.

**Customer:** Sure, the cancellation reference CloudNest gave me is CN-77812.

- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Cancellation reference from CloudNest: CN-77812 (cancelled October 2026)"})` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-60214c64", "due": "2026-12-04", "approval": "none", "channel": "secure_message"}}`

**Assistant:** Done, Dana. Your dispute is filed.

- **Case ID:** C-5003
- **Charge:** $9.99 — CloudNest Storage, November 1, 2026
- **Reason:** Cancelled subscription (evidence: cancellation ref CN-77812)
- **Status:** Under review
- **Follow-up:** due **December 4, 2026**, sent by **secure message**

Disputes are currently reviewed in about 10 days. If anything changes or you get more documentation from CloudNest, let me know.

_Episode written:_ Conversation on 2026-11-24: Dana asked to dispute a $9.99 CloudNest Storage charge from November 1 after cancelling in October. The assistant verified identity, found transaction T-3002, obtained cancellation reference CN-77812, and filed dispute C-5003 as cancelled subscription. Status: under review; follow-up due December 4, 2026 by secure message. Case outcomes: C-5003 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | procedural | under v2 the agent does not file before asking for the cancellation confirmation | `"not called"` |
| PASS | procedural | ...it asks for it | `Thanks, Dana — you're verified, and I found the charge: **$9.99 to CloudNest Storage on November 1, 2026** (transaction T-3002).  To file this as a cancelled-subscription dispute, I need the merchant's cancellation confi …` |
| PASS | procedural | ...and files with it as evidence | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Cancellation reference from CloudNest: CN-77812 (cancelled October 2026)"}]` |

## retraction-drill  ·  retract  ·  2026-11-24T12:00:00Z

_Registry history:_ `[{"event": "baseline", "version": "v1"}, {"event": "promoted", "version": "v2", "based_on": "v1", "by": "ops-lead (scripted reviewer)", "at": "2026-11-23T09:00:00Z"}, {"event": "retracted", "version": "v2", "active_now": "v1", "by": "ops-lead (scripted reviewer)", "reason": "retraction drill: prove a promoted rule can be removed", "at": "2026-11-24T12:00:00Z"}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | procedural | the retraction path restores v1 | `active: v1` |

## s5c-eli-control-under-v1  ·  session  ·  eli  ·  2026-11-24T13:00:00Z

**Customer:** Hi, I'm Eli (card ending 6610, ZIP 73301). I cancelled CloudNest Storage in October but they still charged me $9.99 on November 1. Please dispute it.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer states the CloudNest Storage subscription was cancelled in October; the $9.99 charge posted 2026-11-01 after …)` → `{"case_id": "C-5004", "status": "under_review", "followup": {"followup_id": "F-8431e282", "due": "2026-12-04", "approval": "none", "channel": "secure_message"}}`

**Assistant:** Thanks Eli — identity verified, and I've filed the dispute.

- **Case ID:** C-5004 — for the $9.99 CloudNest Storage charge on 2026-11-01 (transaction T-4002)
- **Reason:** cancelled subscription
- **Status:** under review (typically about 10 days)
- **Follow-up:** due 2026-12-04, sent to you by secure message

If you have a cancellation confirmation number or email from CloudNest, send it along and I'll add it to the case.

_Episode written:_ Conversation on 2026-11-24: Eli reported a $9.99 CloudNest Storage charge on 2026-11-01 after cancelling in October and asked to dispute it. Identity was verified; dispute was filed for transaction T-4002 under case C-5004, status under review. Follow-up is due 2026-12-04 by secure message; cancellation confirmation was requested. Case outcomes: C-5004 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | procedural | control: the same request under v1 is filed straight away, without the promoted check | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer states the CloudNest Storage subscription was cancelled in October; the $9.99 charge posted 2026-11-01 after cancellation."}]` |

## scheduler-2026-11-29  ·  fire_followups  ·  2026-11-29T18:00:00Z

### follow-up session `followup-F-f217be06-1`

**Scheduler:** [scheduled follow-up F-f217be06] action=customer_reminder resume={"note": "Set up a travel notice for Porto trip (reply with travel dates and I'll add it)"}. The customer is not in this conversation. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `notify_customer({"message": "Reminder: you asked about setting up a travel notice for your Porto trip. Reply with your travel dates (departure and return) and I'll add the notice to your card."})` → `{"sent": true, "channel": "sms", "message_id": 3}`

**Assistant:** Reminder sent by SMS: I let the customer know we can set up the Porto travel notice as soon as they reply with their travel dates.

_Episode written:_ Conversation on 2026-11-29: Customer had asked about setting up a travel notice for a Porto trip. Assistant carried out scheduled follow-up F-f217be06 by sending one SMS reminder (message_id 3) asking the customer to reply with departure and return dates; notice will be added once dates are provided. No other preference stated. Case outcomes: no case touched. Lesson: none

_outcomes:_ `[{"followup_id": "F-f217be06", "user_id": "priya", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | Priya's reminder fires on the date she chose | `[{"followup_id": "F-f217be06", "user_id": "priya", "outcome": "fired_done", "error": null}]` |
| PASS | prospective | the reminder carries its resume note to her current channel | `{"message_id": 3, "user_id": "priya", "channel": "sms", "body": "Reminder: you asked about setting up a travel notice for your Porto trip. Reply with your travel dates (departure and return) and I'll add the notice to yo …` |

## s6a-priya-staleness  ·  session  ·  priya  ·  2026-12-03T10:00:00Z

**Customer:** I'm in Porto now and just saw a charge from Livraria Porto. Is my travel notice still active?

- `load_memory({"query": "travel notice Porto"})` → `{"memories": [{"at": "2026-11-29T18:00:00Z", "text": "Conversation on 2026-11-29: Customer had asked about setting up a travel notice for a Porto trip. Assistant carried out scheduled follow-up F-f217be06 by sending one SMS reminder (message_id 3) asking the customer to reply with departure and return dates; notice will be added once dates are provided. No other preference stated. Case outcomes: n …`

**Assistant:** No — there's no travel notice on your account, so nothing is active for Porto.

Here's why: you set up a 29 Nov SMS reminder asking for your trip dates, and the notice was never added because we didn't get a return date. Lisbon notice is also past its end date (30 Nov), so nothing covers you now.

If you give me your return date, I'll add Porto right away. Want me to look at the Livraria Porto charge too?

_Episode written:_ Conversation on 2026-12-03: Customer in Porto asked if their travel notice was active after a Livraria Porto charge. Assistant said none was active: reminder F-f217be06/message_id 3 asked for trip dates, but no return date was provided; Lisbon notice ended 30 Nov. Assistant offered to add Porto right away if given return date and review the charge. No case/transaction IDs or preference stated. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | staleness: the Lisbon notice expired on 2026-11-30 and is deleted at turn start, not by any tool | `null` |
| PASS | semantic | ...the agent did not delete it itself | `"not called"` |
| PASS | semantic | staleness: the reply says no notice is active | `No — there's no travel notice on your account, so nothing is active for Porto.  Here's why: you set up a 29 Nov SMS reminder asking for your trip dates, and the notice was never added because we didn't get a return date. …` |
| PASS | semantic | staleness: the expired Lisbon notice is not presented as current | `No — there's no travel notice on your account, so nothing is active for Porto.  Here's why: you set up a 29 Nov SMS reminder asking for your trip dates, and the notice was never added because we didn't get a return date. …` |

## s6b-priya-forgetting-and-secrets  ·  session  ·  priya  ·  2026-12-03T10:30:00Z

**Customer:** Please set a travel notice for Porto until December 10.

- `remember_customer_fact({"key": "travel_notice", "value": "Porto", "valid_until": "2026-12-10"})` → `{"stored": {"travel_notice": {"value": "Porto", "as_of": "2026-12-03T10:30:00Z", "valid_until": "2026-12-10", "expires_at": "2026-12-11T00:00:00Z"}}, "replaced": null}`
- `search_policy({"question": "travel notice coverage and rules"})` → `{"documents": [{"document": "travel-notices", "score": 0.777, "text": "# Travel notices\n\nA travel notice tells Kestrel's fraud systems that card use in another country is expected, which reduces false declines while you travel. Give the destination and the date you return. Kestrel keeps a travel notice only until the return date and deletes it automatically afterwards; a new trip needs a new not …`

**Assistant:** Travel notice set: **Porto, valid through December 10, 2026** (return date). Kestrel will delete it automatically after that date, so a future trip needs a new notice. Card use in Portugal during that period should be less likely to trigger fraud declines.

**Customer:** Actually, on second thought, delete that travel notice. I'd rather you didn't keep my travel plans.

- `forget_customer_fact({"key": "travel_notice"})` → `{"forgotten": "travel_notice", "had_value": true}`

**Assistant:** Done — the Porto travel notice is deleted and nothing about your travel plans is stored. Your contact channel (SMS) is still on file; tell me if you'd like that removed too.

**Customer:** In case you need it, my full card number is [REDACTED CARD NUMBER].

**Assistant:** Thanks, but that wasn't needed — your full card number has been masked and I haven't stored it. Please don't send card numbers, security codes or passwords here. If we ever need to verify you, I'll only ask for the last 4 digits and billing ZIP.

_Episode written:_ Conversation on 2026-12-03: Customer requested a Porto travel notice through Dec 10, 2026; assistant stored it, explained auto-deletion, then deleted it when customer said they preferred no travel plans kept. Customer sent a full card number; assistant masked it, did not store it, and warned against sending card data. No case or transaction IDs appeared. Case outcomes: no case touched. Lesson: Before storing travel-related facts, confirm the customer is comfortable with retention and explain deletion timing first, since the customer later asked to remove the notice to avoid keeping travel plans.

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

**Assistant:** I don't have a way to pull up Kestrel's fee schedule in this conversation right now, so I can't quote you a foreign transaction fee from memory. Please check the terms in your cardholder agreement or the fees page in your account, or contact support and they can confirm the exact rate.

_Episode written:_ Conversation on 2026-12-03: Customer asked the foreign transaction fee Kestrel charges on euro purchases. The assistant could not access Kestrel’s fee schedule and did not quote a rate; they advised checking the cardholder agreement, the account fees page, or contacting support. No case or transaction ID, promise, or customer preference was stated. Case outcomes: no case touched. Lesson: Next time, the assistant should try to retrieve or escalate for the exact fee schedule instead of only directing the customer elsewhere.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | parametric | with retrieval removed the agent still engages with the fee question | `I don't have a way to pull up Kestrel's fee schedule in this conversation right now, so I can't quote you a foreign transaction fee from memory. Please check the terms in your cardholder agreement or the fees page in you …` |
| PASS | parametric | ...but the weights cannot supply Kestrel's 1.25% | `I don't have a way to pull up Kestrel's fee schedule in this conversation right now, so I can't quote you a foreign transaction fee from memory. Please check the terms in your cardholder agreement or the fees page in you …` |

## s7b-bare-weights-probe  ·  parametric_probe  ·  2026-12-03T11:10:00Z

**Customer:** What foreign transaction fee does Kestrel Card charge on euro purchases? Answer with a number.

**Assistant:** 0

| | memory type | check | evidence |
|---|---|---|---|
| PASS | parametric | the bare model (no instruction, no tools) still answers with a figure from the weights | `0` |
| PASS | parametric | ...and the weights do not hold Kestrel's 1.25%: the floor is generic, not this issuer's | `0` |

## retention-2027-06-15  ·  retention_sweep  ·  2027-06-15T00:00:00Z

_purged:_ `["E-s1-priya-first-contact", "E-s2-priya-returns", "E-s3-marco-other-customer", "E-followup-F-672e95ee-1", "E-s4-priya-after-rejection", "E-followup-F-409951c0-1", "E-s5-dana-under-v2", "E-s5c-eli-control-under-v1", "E-followup-F-f217be06-1", "E-s6a-priya-staleness", "E-s6b-priya-forgetting-and-secrets", "E-s7-parametric-ablation"]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | forgetting on purpose: episodes past their 180-day retention are deleted | `0 episodes; purged 12` |

## s8-priya-after-retention  ·  session  ·  priya  ·  2027-06-15T10:00:00Z

**Customer:** Hi! What did we talk about last time?

- `load_memory({"query": "last conversation summary"})` → `{"memories": []}`

**Assistant:** I don't have any record of our earlier conversations, sorry — nothing turned up when I checked.

What I do have on file for you: your contact channel is SMS, and there's no travel notice saved. If you're thinking of a specific transaction or case, tell me which one and I'll look it up.

_Episode written:_ Conversation on 2027-06-15: Customer asked what was discussed in the previous conversation. The assistant checked memory and found no prior-conversation record, then said none was available and offered to look up a specific transaction or case. No case or transaction IDs were provided, no action was taken, and no promise or customer preference was stated beyond the on-file SMS contact channel. Case outcomes: no case touched. Lesson: When the memory lookup returns no results, the assistant should state that no prior conversation was found and ask for a transaction or case ID, rather than volunteering unrelated profile details.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | recall after retention finds nothing, because nothing is kept | `{"memories": []}` |
