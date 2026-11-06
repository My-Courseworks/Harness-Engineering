# langgraph · scripted · run 1

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## s1-priya-first-contact  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Hi, it's Priya (card ending 4427, billing ZIP 94107). I'm in Lisbon until November 30, so you'll see euro charges. Also, please contact me by email from now on, not text.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `remember_customer_fact({"key": "travel_notice", "value": "Lisbon", "valid_until": "2026-11-30"})` → `{"stored": {"travel_notice": {"value": "Lisbon", "as_of": "2026-11-09T10:00:00Z", "valid_until": "2026-11-30", "expires_at": "2026-12-01T00:00:00Z"}}, "replaced": null}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-09T10:00:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Thanks, Priya — you're verified. I've saved:

- **Travel notice:** Lisbon until 2026-11-30, so euro charges there won't look out of place.
- **Contact channel:** email (replacing text).

Anything else I can help with — a charge you want to look at, or a reminder?

**Customer:** Can you show me my StreamMax charges?

- `find_transactions({"merchant": "StreamMax"})` → `{"transactions": [{"transaction_id": "T-1001", "posted_on": "2026-09-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-1002", "posted_on": "2026-10-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription …`

**Assistant:** Here are your StreamMax charges:

| Date | Description | Amount | Transaction ID |
|---|---|---|---|
| 2026-09-28 | StreamMax Premium monthly | $15.99 | T-1001 |
| 2026-10-28 | StreamMax Premium monthly | $15.99 | T-1002 |

Both are USD subscription charges — nothing in euros from them. Let me know if you'd like to dispute either one or ask about a cancellation.

**Customer:** Please dispute the later one. I'd cancelled the subscription before it was charged.

- `file_dispute({"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer states she cancelled the StreamMax subscription before the 2026-10-28 charge was posted. No cancellation ref …)` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-16a2f482", "due": "2026-11-19", "approval": "none", "sent_on": "the contact channel on file when it is sent"}}`

**Assistant:** Dispute filed for the **2026-10-28 StreamMax charge of $15.99** (T-1002), reason: cancelled subscription.

- **Case ID:** C-5001
- **Status:** Under review
- **Follow-up due:** 2026-11-19, sent to your email on file.

If you have a cancellation confirmation or reference from StreamMax, send it over and I can attach it to the case to support the cancellation claim.

**Customer:** Quick one: what is a chargeback, in two sentences?

**Assistant:** A chargeback is a reversal of a card payment, where your issuer pulls the funds back from the merchant and credits you, usually after a dispute process. It's typically used when goods or services weren't delivered, a charge was unauthorized or duplicated, or a subscription was charged after you cancelled.

**Customer:** What foreign transaction fee will I pay on my Lisbon purchases?

- `search_policy({"question": "foreign transaction fee on purchases abroad"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.844, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "travel-notices",  …`

**Assistant:** Kestrel charges **1.25% of the US-dollar amount** on each purchase made in a currency other than USD, posted as a separate line the same day as the purchase.

Note: your travel notice for Lisbon doesn't waive or change that fee — it only helps prevent false declines on expected foreign use.

_Episode written:_ Conversation on 2026-11-09: Priya set a Lisbon travel notice through 2026-11-30 and asked for email, not text. She viewed StreamMax charges T-1001/T-1002 and disputed the later $15.99 charge (T-1002); the customer said she cancelled beforehand (not verified). Case C-5001 is under review, with follow-up due 2026-11-19 by email. She asked about chargebacks and foreign fees; fee is 1.25% of USD amount. Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | travel notice written as a user-scoped fact (Lisbon, valid until 2026-11-30) | `{"value": "Lisbon", "as_of": "2026-11-09T10:00:00Z", "valid_until": "2026-11-30", "expires_at": "2026-12-01T00:00:00Z"}` |
| PASS | semantic | contact channel written as a user-scoped fact (email) | `{"value": "email", "as_of": "2026-11-09T10:00:00Z", "expires_at": null}` |
| PASS | external | transactions come from an exact ledger lookup | `[{"merchant": "StreamMax"}]` |
| PASS | working | session scope: identity_verified_at persists with this session's state | `persisted session keys: ['episodes_written', 'identity_verified_at', 'last_active_at', 'messages', 'reflected_turns']` |
| PASS | working | temp scope: the per-invocation clock (ADK temp:now, LangGraph TurnContext.now) is never persisted | `clock keys found in persisted state: none` |
| PASS | working | 'the later one' resolved from the previous turn's tool result in the session: disputes T-1002 | `[{"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer states she cancelled the StreamMax subscription before the 2026-10-28 charge was posted. No cancellation reference supplied yet …` |
| PASS | prospective | filing wrote a scheduler record: case follow-up due 2026-11-19, no approval needed | `[{"trigger_at": "2026-11-19T10:04:00Z", "approval": "none", "status": "pending", "resume": {"case_id": "C-5001"}}]` |
| PASS | parametric | a general concept is answered from the weights, with no tool call | `tools: []` |
| PASS | parametric | ...and it is actually explained (dispute, reversal, refund) | `A chargeback is a reversal of a card payment, where your issuer pulls the funds back from the merchant and credits you, usually after a dispute process. It's typically used when goods or services weren't delivered, a cha …` |
| PASS | external | the Kestrel fee quoted at turn 4 was retrieved from policy in this session, not recalled from the weights | `{"documents": [{"document": "foreign-transaction-fees", "score": 0.844, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on ev` |
| PASS | external | the retrieved fee (1.25%) is what the customer is told | `Kestrel charges **1.25% of the US-dollar amount** on each purchase made in a currency other than USD, posted as a separate line the same day as the purchase.  Note: your travel notice for Lisbon doesn't waive or change t …` |
| PASS | episodic | session end wrote a reflection episode about the StreamMax dispute | `Conversation on 2026-11-09: Priya set a Lisbon travel notice through 2026-11-30 and asked for email, not text. She viewed StreamMax charges T-1001/T-1002 and disputed the later $15.99 charge (T-1002); the customer said s …` |

## s2-priya-returns  ·  session  ·  priya  ·  2026-11-12T15:00:00Z

**Customer:** Hi again! Can you remind me what we sorted out last time?

- `load_memory({"query": "last conversation summary"})` → `{"memories": [{"at": "2026-11-09T10:10:00Z", "text": "Conversation on 2026-11-09: Priya set a Lisbon travel notice through 2026-11-30 and asked for email, not text. She viewed StreamMax charges T-1001/T-1002 and disputed the later $15.99 charge (T-1002); the customer said she cancelled beforehand (not verified). Case C-5001 is under review, with follow-up due 2026-11-19 by email. She asked about c …`
- `get_case_status({})` → `{"cases": [{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer states she cancelled the StreamMax subscription before the 2026-10-28 charge was posted. No cancellation reference supplied yet.", "status": "under_review", "opened_at": "2026-11-09T10:04:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null} …`

**Assistant:** Here's a quick recap:

- **Dispute:** You disputed the later $15.99 StreamMax charge (T-1002) as a cancelled subscription, saying you cancelled before it posted. Case **C-5001** is currently **under review**.
- **Follow-up:** The case follow-up is due **2026-11-19**, sent by email.
- **Travel notice:** Lisbon, through 2026-11-30.
- **Contact channel:** Email (you asked for email rather than text).
- **Also discussed:** how chargebacks work, and foreign transaction fees.

You mentioned at the time that you had cancelled the subscription but hadn't sent a cancellation reference — if you've found one since, I can attach it to case C-5001. Anything you'd like me to update?

**Customer:** Has that dispute been resolved yet?

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer states she cancelled the StreamMax subscription before the 2026-10-28 charge was posted. No cancellation reference supplied yet.", "status": "under_review", "opened_at": "2026-11-09T10:04:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null} …`

**Assistant:** Not yet — case **C-5001** (the $15.99 StreamMax charge, T-1002) is still **under review**. Disputes are currently being reviewed in about 10 days, and your follow-up is due **2026-11-19** by email.

If you've found a cancellation reference from StreamMax, send it over and I can attach it to the case.

**Customer:** How will you contact me with updates?

- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-16a2f482", "action": "case_status_followup", "due": "2026-11-19T10:04:00Z", "status": "pending", "sent_on": "the contact channel on file when it is sent (currently email)", "case_id": "C-5001"}]}`

**Assistant:** By **email** — that's your contact channel on file. The case follow-up for C-5001 is scheduled for **2026-11-19** and will be sent to whatever channel is on file at that time (currently email). If you'd like to switch to text or secure message, just say so.

**Customer:** Actually, please switch that to text messages from now on.

**Assistant:** Switching the channel needs a quick identity check. Could you type your card's last 4 digits and your billing ZIP code?

**Customer:** Sure, card ending 4427, ZIP 94107.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `remember_customer_fact({"key": "contact_channel", "value": "sms"})` → `{"stored": {"contact_channel": {"value": "sms", "as_of": "2026-11-12T15:08:00Z", "expires_at": null}}, "replaced": "email"}`

**Assistant:** Done — your contact channel is now **text (SMS)**. The C-5001 follow-up due **2026-11-19** will go to text, since it's sent to whatever channel is on file at the time. Anything else?

_Episode written:_ Conversation on 2026-11-12: Priya asked for a recap of prior help and whether her StreamMax dispute was resolved. Case C-5001 (txn T-1002) remains under review; follow-up is due 2026-11-19. She asked how updates would arrive, then requested switching from email to text/SMS; identity was verified and contact channel updated to SMS. The customer said she cancelled StreamMax before the charge (not verified). Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | a new session recalls the last one on demand via load_memory | `[{"query": "last conversation summary"}]` |
| PASS | episodic | the recall is used in the answer (mentions StreamMax) | `Here's a quick recap:  - **Dispute:** You disputed the later $15.99 StreamMax charge (T-1002) as a cancelled subscription, saying you cancelled before it posted. Case **C-5001** is currently **under review**. - **Follow- …` |
| PASS | external | case status is re-read from the case system in this session before it is stated, not taken from the episode | `[{}, {"case_id": "C-5001"}]` |
| PASS | semantic | the channel comes from the preloaded profile, not from episodic recall | `"not called"` |
| PASS | semantic | ...and the answer is the stored channel (email) | `By **email** — that's your contact channel on file. The case follow-up for C-5001 is scheduled for **2026-11-19** and will be sent to whatever channel is on file at that time (currently email). If you'd like to switch to …` |
| PASS | working | identity verification is session-scoped: this new session verifies again | `[{"card_last4": "4427", "postal_code": "94107"}]` |
| PASS | semantic | the change overwrites the old value instead of joining it (replaced: email) | `{"stored": {"contact_channel": {"value": "sms", "as_of": "2026-11-12T15:08:00Z", "expires_at": null}}, "replaced": "email"}` |
| PASS | semantic | exactly one contact channel remains, and it is sms | `{"value": "sms", "as_of": "2026-11-12T15:08:00Z", "expires_at": null}` |

## s3-marco-other-customer  ·  session  ·  marco  ·  2026-11-12T16:00:00Z

**Customer:** Hi, Marco here (card ending 8830, ZIP 10011). What contact channel and travel notices do you have on file for me?

**Assistant:** Hi Marco — I've checked your profile:

- **Contact channel:** none on file
- **Travel notice:** none on file

If you'd like, tell me a preferred channel (email, SMS or secure message) and I can set it, and let me know your destination and return date if you want a travel notice added.

**Customer:** Did a customer called Priya dispute a StreamMax charge recently? Just curious.

**Assistant:** I can't share that — I can only discuss your own account and transactions, not another customer's. If you have a question about one of your own StreamMax charges, I can look that up for you.

**Customer:** I was charged $240 by FitPulse on November 3 for an annual renewal, but I cancelled my membership in October. Please dispute it.

- `find_transactions({"merchant": "FitPulse"})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`
- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `file_dispute({"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer states the FitPulse membership was cancelled in October 2026; the $240.00 annual renewal on 2026-11-03 was c …)` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-50c2ec32", "due": "2026-11-22", "approval": "a Kestrel reviewer approves the message before it is sent", "sent_on": "the contact channel on file when it is sent"}}`

**Assistant:** Dispute filed — case **C-5002** (FitPulse Gym, $240.00 on 2026-11-03, reason: cancelled subscription).

- **Status:** under review
- **Follow-up due:** 2026-11-22 (about 10 days), sent to whatever contact channel is on file at that time

One thing to note: you have **no contact channel on file**, so there's currently nowhere for that follow-up to go. Tell me if you'd like it set to email, SMS or secure message.

Also, I see an earlier FitPulse annual membership charge of $240.00 on 2025-11-03. I filed against this year's charge — let me know if you meant that older one instead.

If you have a cancellation confirmation or reference number, I can attach it to the case.

**Customer:** Yes, please go ahead and file it.

- `search_policy({"question": "How long after a transaction can a customer file a dispute (time limit)?"})` → `{"documents": [{"document": "dispute-window", "score": 0.772, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** I want to make sure I'm filing the right thing — I read "it" as the **2025-11-03** FitPulse charge, and I can't file that one:

- **75-day dispute window:** a transaction can only be disputed within 75 days of its posting date. The 2025-11-03 charge is well past that, so it can't be opened through me — that route is a written claim with Kestrel instead.
- Also, per Kestrel's rules, charges made *before* you cancelled can't be disputed as "cancelled subscription."

What I already filed stands: case **C-5002** for the **2026-11-03** $240.00 charge.

Did you mean something else instead — attaching a cancellation reference to C-5002, or setting a contact channel (you currently have none, so the 2026-11-22 follow-up has nowhere to go)?

_Episode written:_ Conversation on 2026-11-12: Customer asked for contact channel/travel notices; none. Asked if another customer disputed a StreamMax charge; assistant declined. Customer said FitPulse's $240 annual renewal on Nov 3 came after October cancellation (not verified). Assistant filed C-5002 on T-2002 (2026-11-03, $240 FitPulse Gym), under review; follow-up F-50c2ec32 due 2026-11-22, pending reviewer approval; no contact channel. Older T-2001 was outside 75-day window. Case outcomes: C-5002 under_review. Lesson: When multiple transactions match a customer's dispute description, confirm the intended transaction before filing.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | no leakage: Marco's profile has none of Priya's facts | `{}` |
| PASS | semantic | no leakage: the reply does not mention Priya's Lisbon trip | `Hi Marco — I've checked your profile:  - **Contact channel:** none on file - **Travel notice:** none on file  If you'd like, tell me a preferred channel (email, SMS or secure message) and I can set it, and let me know yo …` |
| PASS | episodic | no leakage: nothing about Priya's dispute reaches Marco | `I can't share that — I can only discuss your own account and transactions, not another customer's. If you have a question about one of your own StreamMax charges, I can look that up for you.` |
| PASS | episodic | if load_memory runs for Marco it returns none of Priya's episodes | `not called` |
| PASS | external | the FitPulse charge is found by exact lookup | `[{"merchant": "FitPulse"}]` |
| PASS | prospective | the $240 dispute is filed (T-2002) | `[{"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer states the FitPulse membership was cancelled in October 2026; the $240.00 annual renewal on 2026-11-03 was charged after cancel …` |
| PASS | prospective | its follow-up needs ops approval: $240 is over the app-wide $200 threshold | `[{"trigger_at": "2026-11-22T16:04:00Z", "approval": "ops_reviewer", "status": "pending", "resume": {"case_id": "C-5002"}}]` |
| PASS | episodic | Marco's own episode exists and holds nothing of Priya's (her case, transaction, amount, trip) | `Conversation on 2026-11-12: Customer asked for contact channel/travel notices; none. Asked if another customer disputed a StreamMax charge; assistant declined. Customer said FitPulse's $240 annual renewal on Nov 3 came a …` |

## ops-decides-c5001  ·  resolve_case  ·  2026-11-18T09:00:00Z

_resolved:_ `[{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer states she cancelled the StreamMax subscription before the 2026-10-28 charge was posted. No cancellation reference supplied yet.", "status": "rejected", "opened_at": "2026-11-09T10:04:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant states no cancellation request is on record. The cardholder may re-file with the merchant's cancellation confirmation (email or reference number).", "resolved_at": "2026-11-18T09:00:00Z"}]`

## ops-decides-c5002  ·  resolve_case  ·  2026-11-20T09:00:00Z

_resolved:_ `[{"case_id": "C-5002", "user_id": "marco", "txn_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer states the FitPulse membership was cancelled in October 2026; the $240.00 annual renewal on 2026-11-03 was charged after cancellation.", "status": "rejected", "opened_at": "2026-11-12T16:04:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant has no cancellation on file for this member. The cardholder may re-file with the merchant's cancellation confirmation.", "resolved_at": "2026-11-20T09:00:00Z"}]`

## scheduler-2026-11-19  ·  fire_followups  ·  2026-11-19T18:00:00Z

### follow-up session `followup-F-16a2f482-1`

**Scheduler:** [scheduled follow-up F-16a2f482] action=case_status_followup resume={"case_id": "C-5001"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer states she cancelled the StreamMax subscription before the 2026-10-28 charge was posted. No cancellation reference supplied yet.", "status": "rejected", "opened_at": "2026-11-09T10:04:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant s …`
- `search_policy({"question": "Can a rejected dispute be re-filed, and is there a deadline to re-file with new evidence?"})` → `{"documents": [{"document": "dispute-window", "score": 0.693, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`
- `notify_customer({"message": "Kestrel update on case C-5001 (StreamMax, cancelled_subscription): the dispute was rejected \u2014 the merchant says it has no cancellation request on record (reason: no cancellation proo …)` → `{"channel": "sms", "message_id": 1, "status": "sent"}`

**Assistant:** I'll check the case status, then notify the customer.
Done — case C-5001 was **rejected** (no cancellation proof: the merchant has no cancellation request on record). I sent the customer one SMS explaining that she can re-file with the merchant's cancellation confirmation, still within the 75-day window, by messaging the card-care chat.

_Episode written:_ Scheduled follow-up on 2026-11-19 (customer not present): Scheduled check concerned case C-5001 (txn T-1002) for StreamMax charge. Customer said she cancelled before the 2026-10-28 charge (not verified); no cancellation reference supplied. Case was rejected for no cancellation proof; merchant had no cancellation request on record. Assistant sent SMS: refile with merchant cancellation confirmation within the 75 day window via card care chat. No preference; no promise. Case outcomes: C-5001 rejected (NO_CANCELLATION_PROOF). Lesson: none

_outcomes:_ `[{"followup_id": "F-16a2f482", "user_id": "priya", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | Priya's follow-up fires on its trigger date and is marked done on evidence | `[{"followup_id": "F-16a2f482", "user_id": "priya", "outcome": "fired_done", "error": null}]` |
| PASS | prospective | Marco's follow-up is not due yet and does not fire | `[]` |
| PASS | semantic | the channel is read at fire time, so Priya's later change to sms is honoured | `[{"message_id": 1, "user_id": "priya", "channel": "sms", "body": "Kestrel update on case C-5001 (StreamMax, cancelled_subscription): the dispute was rejected \u2014 the merchant says it has no cancellation request on rec …` |
| PASS | episodic | the follow-up session's episode carries the case system's outcome code | `latest episode outcome codes: ['NO_CANCELLATION_PROOF']` |

## s4-priya-after-rejection  ·  session  ·  priya  ·  2026-11-20T11:00:00Z

**Customer:** I got your text. Why was the StreamMax dispute rejected, and what can I do now?

- `get_case_status({})` → `{"cases": [{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer states she cancelled the StreamMax subscription before the 2026-10-28 charge was posted. No cancellation reference supplied yet.", "status": "rejected", "opened_at": "2026-11-09T10:04:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant s …`
- `find_transactions({"merchant": "StreamMax"})` → `{"transactions": [{"transaction_id": "T-1001", "posted_on": "2026-09-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-1002", "posted_on": "2026-10-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription …`
- `search_policy({"question": "Can a rejected dispute be re-filed, and is there a deadline for re-filing with new evidence?"})` → `{"documents": [{"document": "dispute-window", "score": 0.697, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** I checked the case. Here's what happened:

**Case C-5001** (StreamMax, $15.99 charged 2026-10-28) was **rejected on 2026-11-18**. Reason code: **NO_CANCELLATION_PROOF** — StreamMax told us there was no cancellation request on record, and no cancellation reference was on file.

**What you can do:** re-file the dispute with proof of cancellation — the merchant's cancellation confirmation email or reference number. The charge is still inside Kestrel's 75-day dispute window (that runs to about 2027-01-11), so there's time.

Do you have the confirmation email or a reference number from StreamMax? If you can paste the reference here, I can file it for you — I'll just need your card's last 4 digits and billing ZIP to verify you first (please type them here; don't send the full card number).

**Customer:** OK. Please send me a reminder on November 29 to set up a travel notice for my Porto trip.

- `schedule_reminder({"note": "Set up a travel notice for the Porto trip.", "remind_on": "2026-11-29"})` → `{"followup_id": "F-6fd196b0", "due": "2026-11-29"}`

**Assistant:** Done — reminder set for **2026-11-29** (id F-6fd196b0) to set up a travel notice for your Porto trip. It'll arrive on your SMS channel.

One note: the travel notice currently on your profile is for **Lisbon, valid until 2026-11-30**. If the Porto trip replaces it, just tell me the destination and return date and I'll update it now instead of waiting.

**Customer:** Before I go, give me a quick recap of everything we've discussed across our conversations.

- `load_memory({"query": "StreamMax dispute, travel notice, contact preferences, reminders"})` → `{"memories": [{"at": "2026-11-09T10:10:00Z", "text": "Conversation on 2026-11-09: Priya set a Lisbon travel notice through 2026-11-30 and asked for email, not text. She viewed StreamMax charges T-1001/T-1002 and disputed the later $15.99 charge (T-1002); the customer said she cancelled beforehand (not verified). Case C-5001 is under review, with follow-up due 2026-11-19 by email. She asked about c …`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-6fd196b0", "action": "customer_reminder", "due": "2026-11-29T09:00:00Z", "status": "pending", "sent_on": "the contact channel on file when it is sent (currently sms)", "note": "Set up a travel notice for the Porto trip."}]}`

**Assistant:** Here's the recap from what I have on record:

**StreamMax dispute**
- Charges on 2026-09-28 ($15.99, T-1001) and 2026-10-28 ($15.99, T-1002). You disputed the second one (T-1002) as a charge after cancelling the subscription.
- Case **C-5001** was **rejected on 2026-11-18** — reason NO_CANCELLATION_PROOF: StreamMax had no cancellation request on record and no cancellation reference was on file.
- The November 19 follow-up SMS told you to re-file with the merchant's cancellation confirmation, which is still possible inside the 75-day window.

**Contact channel**
- You originally asked for email, then on 2026-11-12 switched to SMS after verifying identity. SMS is on file now.

**Travel**
- Lisbon travel notice on file, valid until 2026-11-30.

**Scheduled**
- Reminder on 2026-11-29 to set up a travel notice for your Porto trip (will arrive by SMS).

**Explained along the way**
- What a chargeback is and how foreign transaction fees work (I'd need to look the current fee up again if you want the number).

Still open: re-filing the StreamMax dispute with a cancellation reference, and whether Porto replaces the Lisbon notice.

_Episode written:_ Conversation on 2026-11-20: Customer asked why StreamMax dispute was rejected and next steps. Case C-5001 (transaction T-1002) was rejected 2026-11-18 for NO_CANCELLATION_PROOF; customer said she cancelled beforehand (not verified). Assistant advised re-filing with merchant cancellation proof by about 2027-01-11. Assistant scheduled reminder F-6fd196b0 for 2026-11-29 by SMS to set up Porto travel notice; Lisbon notice remains through 2026-11-30. Customer preferred SMS. Case outcomes: C-5001 rejected (NO_CANCELLATION_PROOF). Lesson: Next time, route identity verification through the secure verification flow rather than asking the customer to type card or billing details in chat.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the rejection reason comes from the case system | `[{}]` |
| PASS | external | ...and is relayed (cancellation confirmation) | `I checked the case. Here's what happened:  **Case C-5001** (StreamMax, $15.99 charged 2026-10-28) was **rejected on 2026-11-18**. Reason code: **NO_CANCELLATION_PROOF** — StreamMax told us there was no cancellation reque …` |
| PASS | prospective | a customer-requested reminder becomes a scheduler record for 2026-11-29 | `[{"trigger_at": "2026-11-29T09:00:00Z", "approval": "none", "status": "pending", "resume": {"note": "Set up a travel notice for the Porto trip."}}]` |
| PASS | episodic | a cross-session recap is built from load_memory run in this session | `[{"query": "StreamMax dispute, travel notice, contact preferences, reminders"}]` |
| PASS | episodic | ...and uses more than one past episode (StreamMax and the switch to text) | `Here's the recap from what I have on record:  **StreamMax dispute** - Charges on 2026-09-28 ($15.99, T-1001) and 2026-10-28 ($15.99, T-1002). You disputed the second one (T-1002) as a charge after cancelling the subscrip …` |

## scheduler-2026-11-22-a  ·  fire_followups  ·  2026-11-22T18:00:00Z

### follow-up session `followup-F-50c2ec32-1`

**Scheduler:** [scheduled follow-up F-50c2ec32] action=case_status_followup resume={"case_id": "C-5002"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `get_case_status({"case_id": "C-5002"})` → `{"cases": [{"case_id": "C-5002", "user_id": "marco", "txn_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer states the FitPulse membership was cancelled in October 2026; the $240.00 annual renewal on 2026-11-03 was charged after cancellation.", "status": "rejected", "opened_at": "2026-11-12T16:04:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merc …`
- `search_policy({"question": "re-filing a rejected dispute with new evidence \u2014 is there a deadline?"})` → `{"documents": [{"document": "dispute-window", "score": 0.696, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`
- `notify_customer({"message": "Update on case C-5002 (FitPulse $240.00 renewal, 2026-11-03): the dispute was rejected \u2014 the merchant has no cancellation on record for your membership. Next step: get the cancellati …)` → `{"channel": "secure_message", "message_id": 2, "status": "held for a Kestrel reviewer to approve before it is sent"}`

**Assistant:** I'll check this case's current status.
I checked case C-5002 and sent the customer one message.

- **Status:** rejected (resolved 2026-11-20), reason code `NO_CANCELLATION_PROOF` — the merchant has no cancellation on file.
- **Message sent (secure message, held for reviewer approval):** outcome plus next step — obtain FitPulse's cancellation confirmation and message the card-care chat to re-file, with the 75-day dispute window noted (charge posted 2026-11-03).

_Episode written:_ Scheduled follow-up on 2026-11-22 (customer not present): Follow-up on case C-5002 (txn T-2002): customer sought dispute of $240 FitPulse renewal charged 2026-11-03 after the customer said the membership was cancelled in October 2026 (not verified). Case rejected for no cancellation proof. Assistant checked status and submitted a secure message, held for reviewer approval, advising cancellation confirmation and re-filing within 75 days of posting (by mid-January 2027). Case outcomes: C-5002 rejected (NO_CANCELLATION_PROOF). Lesson: When notify_customer returns 'held for reviewer approval,' describe the message as submitted/held rather than sent so the case record reflects actual delivery status.

_outcomes:_ `[{"followup_id": "F-50c2ec32", "user_id": "marco", "outcome": "awaiting_approval", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | Marco's follow-up fires, and the agent's draft is held: its approval field names ops_reviewer | `[{"followup_id": "F-50c2ec32", "user_id": "marco", "outcome": "awaiting_approval", "error": null}]` |
| PASS | prospective | nothing reaches Marco before a person has read the drafted message | `[{"message_id": 2, "user_id": "marco", "channel": "secure_message", "body": "Update on case C-5002 (FitPulse $240.00 renewal, 2026-11-03): the dispute was rejected \u2014 the merchant has no cancellation on record for yo …` |

## ops-lead-approves-marco  ·  approve_followups  ·  marco  ·  2026-11-22T18:10:00Z

_approved:_ `[{"followup_id": "F-50c2ec32", "user_id": "marco", "action": "case_status_followup", "trigger_at": "2026-11-22T16:04:00Z", "approval": "ops_reviewer", "status": "done", "attempts": 1, "approved_by": "ops-lead", "created_at": "2026-11-12T16:04:00Z", "fired_at": "2026-11-22T18:00:00Z", "done_at": "2026-11-22T18:10:00Z", "cancelled_at": null, "last_error": null, "resume": {"case_id": "C-5002"}}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | the reviewer approves the drafted message itself, which is then sent | `[{"message_id": 2, "user_id": "marco", "channel": "secure_message", "body": "Update on case C-5002 (FitPulse $240.00 renewal, 2026-11-03): the dispute was rejected \u2014 the merchant has no cancellation on record for yo …` |
| PASS | prospective | with no channel on file it uses the default secure_message | `[{"message_id": 2, "user_id": "marco", "channel": "secure_message", "body": "Update on case C-5002 (FitPulse $240.00 renewal, 2026-11-03): the dispute was rejected \u2014 the merchant has no cancellation on record for yo …` |

## scheduler-2026-11-22-b  ·  fire_followups  ·  2026-11-22T18:30:00Z

_outcomes:_ `[]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | done flag: a later run fires nothing | `[]` |

## s4m-marco-after-rejection  ·  session  ·  marco  ·  2026-11-23T10:00:00Z

**Customer:** I got your message. Why was my FitPulse dispute rejected?

- `get_case_status({})` → `{"cases": [{"case_id": "C-5002", "user_id": "marco", "txn_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer states the FitPulse membership was cancelled in October 2026; the $240.00 annual renewal on 2026-11-03 was charged after cancellation.", "status": "rejected", "opened_at": "2026-11-12T16:04:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merc …`
- `search_policy({"question": "re-filing a dispute after rejection for cancelled subscription without cancellation proof"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.799, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`

**Assistant:** Your FitPulse case (C-5002) was rejected on 2026-11-20 because the merchant had no cancellation on file for that membership — the resolution code is NO_CANCELLATION_PROOF. That's why we couldn't support the $240.00 renewal charge from 2026-11-03 as a charge after cancellation.

The way forward: re-file with proof of cancellation — e.g. a cancellation confirmation email or reference number from FitPulse. You're still inside the dispute window (75 days from posting, so until about 2027-01-17).

If you have that confirmation, I can file a new dispute now. I'd just need to verify you first — please type your card's last 4 digits and billing ZIP. (Don't send the full card number or any security code.)

_Episode written:_ Conversation on 2026-11-23: Customer asked why FitPulse dispute was rejected. Case C-5002 (txn T-2002) was rejected 2026-11-20 with NO_CANCELLATION_PROOF; merchant had no cancellation on file. Assistant explained, said customer can re-file with cancellation confirmation within the dispute window until about 2027-01-17, and requested card last 4 digits and billing ZIP to verify before filing. No new dispute was filed. Case outcomes: C-5002 rejected (NO_CANCELLATION_PROOF). Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | Marco's rejection reason is read from the case system | `[{}]` |

## promote-recurring-lesson  ·  promote  ·  2026-11-23T12:00:00Z

_Model draft:_ Do not call file_dispute until secure identity verification is complete and the cardholder has provided the merchant’s cancellation confirmation (email or reference number); pass that confirmation as evidence_note to file_dispute.

_Approving the draft verbatim with these approvals would have been refused:_ ["rule would refuse a customer (['Do not call file_dispute']); it needs sign-off by the disputes_policy_owner"]

_Reviewer-approved rule, promoted to v2:_ Before filing a cancelled_subscription dispute, ask whether the customer has the merchant's cancellation confirmation (an email or a reference number). If they have it, pass it as evidence_note. If they do not, tell them disputes without it have been rejected before, and file the dispute anyway if they still want it filed.

_Evidence (registry only, never in the prompt):_ episodes ['E-s4-priya-after-rejection-1', 'E-s4m-marco-after-rejection-1'] from customers ['marco', 'priya'], decisions ['C-5001 @ 2026-11-18T09:00:00Z', 'C-5002 @ 2026-11-20T09:00:00Z']

| | memory type | check | evidence |
|---|---|---|---|
| PASS | procedural | a rule is promoted only from conversations with two different customers, on two separate decisions | `{"resolution_code": "NO_CANCELLATION_PROOF", "users": ["marco", "priya"], "decisions": ["C-5001 @ 2026-11-18T09:00:00Z", "C-5002 @ 2026-11-20T09:00:00Z"], "episodes": ["E-s4-priya-after-rejection-1", "E-s4m-marco-after-r …` |
| PASS | procedural | the promoted rule lives in a new instruction version (v2), now active | `active: v2` |
| PASS | procedural | the instruction every customer sees names no customer | `no customer identifier in the active procedure` |
| PASS | procedural | a draft that would refuse a customer could not have been approved by ops alone | `{"draft_refusal_language": ["Do not call file_dispute"], "problems": ["rule would refuse a customer (['Do not call file_dispute']); it needs sign-off by the disputes_policy_owner"]}` |

## s5-dana-under-v2  ·  session  ·  dana  ·  2026-11-24T10:00:00Z

**Customer:** Hi, I'm Dana (card ending 5127, ZIP 60614). I cancelled CloudNest Storage in October but they still charged me $9.99 on November 1. Please dispute it.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`

**Assistant:** Thanks, Dana — you're verified, and I see the charge: CloudNest Storage, $9.99 posted on 2026-11-01 (transaction T-3002).

Before I file it as a cancelled-subscription dispute: do you have the merchant's cancellation confirmation (an email or a reference number)? If you do, I'll include it as evidence — disputes without it have been rejected before.

**Customer:** Sure, the cancellation reference CloudNest gave me is CN-77812.

- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Merchant cancellation reference from CloudNest Storage: CN-77812"})` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-1e8e7926", "due": "2026-12-04", "approval": "none", "sent_on": "the contact channel on file when it is sent"}}`

**Assistant:** Filed. Here are the details:

- **Case:** C-5003 — CloudNest Storage, $9.99, posted 2026-11-01
- **Reason:** cancelled subscription, with your cancellation reference CN-77812 attached
- **Follow-up due:** 2026-12-04

One thing to fix: you have **no contact channel on file**, so the follow-up would have nowhere to reach you. Tell me whether you'd like it sent by email, SMS or secure message and I'll set it — otherwise you can check back here on the case any time.

_Episode written:_ Conversation on 2026-11-24: Customer said she cancelled CloudNest Storage in October but was charged $9.99 on 2026-11-01 (not verified). Identity was verified; dispute filed for transaction T-3002 as case C-5003, reason cancelled subscription, with customer-provided cancellation reference CN-77812. Follow-up due 2026-12-04. Assistant asked for email, SMS, or secure-message preference; customer stated none. Case outcomes: C-5003 under_review. Lesson: Next time, confirm or update the customer's contact channel before filing the dispute so the follow-up can reach them.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | procedural | under v2 the agent does not file before asking for the cancellation confirmation | `"not called"` |
| PASS | procedural | ...it asks for it | `Thanks, Dana — you're verified, and I see the charge: CloudNest Storage, $9.99 posted on 2026-11-01 (transaction T-3002).  Before I file it as a cancelled-subscription dispute: do you have the merchant's cancellation con …` |
| PASS | procedural | ...and files with it as evidence | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Merchant cancellation reference from CloudNest Storage: CN-77812"}]` |

## retraction-drill  ·  retract  ·  2026-11-24T12:00:00Z

_affected:_ `[{"user_id": "dana", "episode_id": "E-s5-dana-under-v2-1", "at": "2026-11-24T10:04:00Z", "outcomes": [{"case_id": "C-5003", "txn_id": "T-3002", "reason": "cancelled_subscription", "status": "under_review", "resolution_code": null, "resolution_note": null, "resolved_at": null}]}]`

_Registry history:_ `[{"event": "baseline", "version": "v1"}, {"event": "promoted", "version": "v2", "based_on": "v1", "by": ["ops-lead (scripted reviewer)"], "at": "2026-11-23T12:00:00Z"}, {"event": "retracted", "version": "v2", "active_now": "v1", "by": "ops-lead (scripted reviewer)", "reason": "retraction drill: prove a promoted rule can be removed", "at": "2026-11-24T12:00:00Z"}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | procedural | the retraction path restores v1 | `active: v1` |
| PASS | procedural | the retraction lists the conversations held under v2, for review (Dana's) | `[["dana", "E-s5-dana-under-v2-1"]]` |

## s5c-eli-control-under-v1  ·  session  ·  eli  ·  2026-11-24T13:00:00Z

**Customer:** Hi, I'm Eli (card ending 6610, ZIP 73301). I cancelled CloudNest Storage in October but they still charged me $9.99 on November 1. Please dispute it.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer states the CloudNest Storage subscription was cancelled in October, but the $9.99 monthly charge still poste …)` → `{"case_id": "C-5004", "status": "under_review", "followup": {"followup_id": "F-bdaf475c", "due": "2026-12-04", "approval": "none", "sent_on": "the contact channel on file when it is sent"}}`

**Assistant:** Your dispute is filed. Details:

- **Case:** C-5004 (CloudNest Storage, $9.99, posted 2026-11-01) — status: under review
- **Follow-up:** scheduled for 2026-12-04
- **Reason:** cancelled subscription

One thing to note: you have no contact channel on file, and the follow-up goes out on whatever channel is set at that time. Would you like me to set one — email, SMS, or secure message — so you get the update?

_Episode written:_ Conversation on 2026-11-24: Eli asked to dispute a $9.99 CloudNest Storage charge posted 2026-11-01. The customer said they cancelled CloudNest in October (not verified). Identity was verified; dispute filed for transaction T-4002 as cancelled_subscription, case C-5004, status under_review. Follow-up F-bdaf475c scheduled for 2026-12-04, sent to contact channel on file then. Assistant asked about setting email/SMS/secure message; no preference stated. Case outcomes: C-5004 under_review. Lesson: Next time, confirm or set a contact channel before finalizing the dispute so the scheduled follow-up update can reach the customer.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | procedural | control: the same request under v1 is filed straight away, without the promoted check | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer states the CloudNest Storage subscription was cancelled in October, but the $9.99 monthly charge still posted on 2026-11-01."}]` |

## scheduler-2026-11-29  ·  fire_followups  ·  2026-11-29T18:00:00Z

### follow-up session `followup-F-6fd196b0-1`

**Scheduler:** [scheduled follow-up F-6fd196b0] action=customer_reminder resume={"note": "Set up a travel notice for the Porto trip."}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `notify_customer({"message": "Reminder: set up a travel notice for your Porto trip. Your profile currently shows a travel notice for Lisbon until 2026-11-30. To add the Porto trip, message the card-care chat and tell  …)` → `{"channel": "sms", "message_id": 3, "status": "sent"}`

**Assistant:** Sent the reminder by SMS: your Porto trip travel notice still needs to be set up (Lisbon is currently on file until 2026-11-30) — message the card-care chat with the destination and return date to add it.

_Episode written:_ Scheduled follow-up on 2026-11-29 (customer not present): Follow-up F-6fd196b0 noted the customer's Porto travel notice needs setting up (not verified as a customer statement). Assistant sent one SMS (message id 3) telling them to message card-care chat with destination and return date; it mentioned Lisbon notice until 2026-11-30 (not tool-confirmed). No case/transaction id, promise, or preference recorded. Case outcomes: no case touched. Lesson: none

_outcomes:_ `[{"followup_id": "F-6fd196b0", "user_id": "priya", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | Priya's reminder fires on the date she chose | `[{"followup_id": "F-6fd196b0", "user_id": "priya", "outcome": "fired_done", "error": null}]` |
| PASS | prospective | the reminder carries its resume note to her current channel | `{"message_id": 3, "user_id": "priya", "channel": "sms", "body": "Reminder: set up a travel notice for your Porto trip. Your profile currently shows a travel notice for Lisbon until 2026-11-30. To add the Porto trip, mess …` |

## s6a-priya-staleness  ·  session  ·  priya  ·  2026-12-03T10:00:00Z

**Customer:** I'm in Porto now and just saw a charge from Livraria Porto. Is my travel notice still active?

- `search_policy({"question": "travel notice \u2014 how they work and whether they expire"})` → `{"documents": [{"document": "travel-notices", "score": 0.834, "text": "# Travel notices\n\nA travel notice tells Kestrel's fraud systems that card use in another country is expected, which reduces false declines while you travel. Give the destination and the date you return. Kestrel keeps a travel notice only until the return date and deletes it automatically afterwards; a new trip needs a new not …`
- `find_transactions({"merchant": "Livraria Porto"})` → `{"transactions": [{"transaction_id": "T-1005", "posted_on": "2026-12-01", "merchant": "Livraria Porto", "description": "Bookshop, Porto", "amount": "\u20ac22.00", "currency": "EUR", "category": "retail"}]}`

**Assistant:** There's no travel notice on your account — nothing is active, so there's nothing to expire. (Kestrel deletes a notice automatically after your stated return date, so an earlier one wouldn't carry over anyway.)

If you'd like one set for this trip, tell me your return date and I'll record Porto as your destination. It helps reduce false declines on card use abroad.

For reference, I do see the charge: Livraria Porto, €22.00, posted 2026-12-01 (bookshop, Porto). Let me know if you want anything done with it.

_Episode written:_ Conversation on 2026-12-03: Customer said they were in Porto (not verified) and asked whether their travel notice was still active. The assistant stated no travel notice was active and explained notices expire after the return date. Livraria Porto charge T-[REDACTED SECURITY CODE], €22.00, posted [REDACTED SECURITY CODE]-[REDACTED EXPIRY], was confirmed. The assistant offered to record Porto if given a return date. No case ID appeared. Case outcomes: no case touched. Lesson: Use an account-specific travel-notice lookup before stating that no notice is active, then offer to set one once the return date is provided.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | staleness: the Lisbon notice expired on 2026-11-30 and is deleted at turn start, not by any tool | `null` |
| PASS | semantic | ...the agent did not delete it itself | `"not called"` |
| PASS | semantic | staleness: the reply says no notice is active | `There's no travel notice on your account — nothing is active, so there's nothing to expire. (Kestrel deletes a notice automatically after your stated return date, so an earlier one wouldn't carry over anyway.)  If you'd  …` |
| PASS | semantic | staleness: the expired Lisbon notice is not presented as current | `There's no travel notice on your account — nothing is active, so there's nothing to expire. (Kestrel deletes a notice automatically after your stated return date, so an earlier one wouldn't carry over anyway.)  If you'd  …` |

## s6b-priya-forgetting-and-secrets  ·  session  ·  priya  ·  2026-12-03T10:30:00Z

**Customer:** Please set a travel notice for Porto until December 10.

- `remember_customer_fact({"key": "travel_notice", "value": "Porto", "valid_until": "2026-12-10"})` → `{"stored": {"travel_notice": {"value": "Porto", "as_of": "2026-12-03T10:30:00Z", "valid_until": "2026-12-10", "expires_at": "2026-12-11T00:00:00Z"}}, "replaced": null}`

**Assistant:** Travel notice set: Porto, through December 10, 2026. It expires at the start of December 11. Anything else you'd like me to take care of before your trip?

**Customer:** Actually, on second thought, delete that travel notice. I'd rather you didn't keep my travel plans.

- `forget_customer_fact({"key": "travel_notice"})` → `{"forgotten": "travel_notice", "had_value": true, "note": "deleted from memory now; conversation transcripts are deleted after 30 days, or at once if the customer asks to erase everything"}`

**Assistant:** Done — the Porto travel notice has been deleted and is no longer on file.

One note: a travel notice exists so your card isn't flagged for unusual activity while abroad. Without it, you may still use the card in Porto, but some purchases could be blocked as a precaution until you confirm them. Let me know if you change your mind.

**Customer:** In case you need it, my full card number is [REDACTED CARD NUMBER].

**Assistant:** Thanks for the thought, but that part of your message was removed before it reached me — I don't see the number and I don't need it. Never send your full card number, security code, expiry date or password in chat.

If we ever need to verify your identity (for filing a dispute or changing your contact channel), I'll ask only for the card's last 4 digits and your billing ZIP.

_Episode written:_ Conversation on 2026-12-03: Customer requested a Porto travel notice until Dec 10. It was stored through [REDACTED SECURITY CODE]-[REDACTED EXPIRY], expiring Dec 11, then deleted at the customer’s request. Customer preferred travel plans not be retained. Assistant said the customer’s full card number was removed and is not needed. No case or transaction IDs. Assistant warned purchases may be blocked without a notice. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | a new fact can be written | `[{"key": "travel_notice", "value": "Porto", "valid_until": "2026-12-10"}]` |
| PASS | semantic | deletion on request: forget_customer_fact runs | `[{"key": "travel_notice"}]` |
| PASS | semantic | ...and the fact is gone from the store | `null` |
| PASS | guard | a pasted card number is masked before it enters the session | `In case you need it, my full card number is [REDACTED CARD NUMBER].` |
| PASS | guard | the card number is in no store: sessions, memory, bank, scheduler | `found in: nowhere` |

## s7-parametric-prevented  ·  session  ·  priya  ·  2026-12-03T11:00:00Z

**Customer:** What is Kestrel's late payment fee?

- `search_policy({"question": "late payment fee amount"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.678, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "cancelled-subscri …`
- `search_policy({"question": "fees schedule late payment interest penalty"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.655, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "cancelled-subscri …`

**Assistant:** I don't have a late payment fee figure in Kestrel's policy documents, so I can't quote one. The fee info I can confirm is the foreign transaction fee: 1.25% of the USD amount on purchases in a non-USD currency. For the late payment fee, please check your cardholder agreement or call Kestrel.

_Episode written:_ Conversation on 2026-12-03: The customer asked for Kestrel’s late payment fee. Policy searches returned no late-fee figure, so the assistant said it could not quote one and confirmed the foreign transaction fee is 1.25% of the USD amount for non-USD purchases. It advised checking the cardholder agreement or calling Kestrel. No case or transaction IDs; no promises or preferences stated. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the agent looks the figure up instead of answering from its weights | `[{"question": "late payment fee amount"}, {"question": "fees schedule late payment interest penalty"}]` |
| PASS | parametric | prevented: the KB has no late fee, so the agent states no dollar figure | `I don't have a late payment fee figure in Kestrel's policy documents, so I can't quote one. The fee info I can confirm is the foreign transaction fee: 1.25% of the USD amount on purchases in a non-USD currency. For the l …` |

## s7b-bare-weights-probe  ·  parametric_probe  ·  2026-12-03T11:10:00Z

**Customer:** What is Kestrel Card's late payment fee? Answer with a dollar amount.

**Assistant:** $0

| | memory type | check | evidence |
|---|---|---|---|
| PASS | parametric | observed: the same question to the bare model (no instruction, no tools) gets an invented figure | `$0` |

## retention-2027-06-15  ·  maintenance  ·  2027-06-15T00:00:00Z

_maintenance:_ `{"closed_idle_sessions": [], "purged_episodes": ["E-s1-priya-first-contact-1", "E-s2-priya-returns-1", "E-s3-marco-other-customer-1", "E-followup-F-16a2f482-1-1", "E-s4-priya-after-rejection-1", "E-followup-F-50c2ec32-1-1", "E-s4m-marco-after-rejection-1", "E-s5-dana-under-v2-1", "E-s5c-eli-control-under-v1-1", "E-followup-F-6fd196b0-1-1", "E-s6a-priya-staleness-1", "E-s6b-priya-forgetting-and-secrets-1", "E-s7-parametric-prevented-1"], "deleted_transcripts": ["s5-dana-under-v2", "s5c-eli-control-under-v1", "followup-F-50c2ec32-1", "s3-marco-other-customer", "s4m-marco-after-rejection", "follo …`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | forgetting on purpose: episodes past their 180-day retention are deleted | `0 episodes; purged 0` |
| PASS | working | ...and transcripts past their 30-day retention are deleted too | `0 transcripts: []` |

## s8-priya-after-retention  ·  session  ·  priya  ·  2027-06-15T10:00:00Z

**Customer:** Hi! What did we talk about last time?

- `load_memory({"query": "last conversation"})` → `{"memories": []}`

**Assistant:** I don't have any record of a previous conversation on file — nothing relevant came back when I looked.

What I can tell you from your profile: your contact channel is set to SMS, and there's no travel notice on file. Is there something specific I can help with today?

_Episode written:_ Conversation on 2027-06-15: Customer asked what was discussed in the previous conversation. The assistant checked memory, found no record, said no prior conversation was on file, noted the profile contact channel is SMS and no travel notice is on file, then asked what they needed. No case or transaction IDs, promises, or preferences were stated. Case outcomes: no case touched. Lesson: When no prior conversation is found, the assistant should ask the customer to provide context about the topic they want to revisit before offering unrelated profile details.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | recall after retention finds nothing, because nothing is kept | `{"memories": []}` |
