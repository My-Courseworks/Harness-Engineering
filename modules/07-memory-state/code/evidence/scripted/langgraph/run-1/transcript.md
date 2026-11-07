# langgraph · scripted · run 1

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## s1-priya-first-contact  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Hi, it's Priya (card ending 4427, billing ZIP 94107). I'm in Lisbon until November 30, so you'll see euro charges. Also, please contact me by email from now on, not text.

- `remember_customer_fact({"key": "travel_notice", "value": "Lisbon", "valid_until": "2026-11-30"})` → `{"stored": {"travel_notice": {"value": "Lisbon", "as_of": "2026-11-09T10:00:00Z", "valid_until": "2026-11-30", "expires_at": "2026-12-01T00:00:00Z"}}, "replaced": null}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"error": "changing contact_channel requires verify_identity in this conversation"}`
- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-09T10:00:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Both are set, Priya:

- **Travel notice:** Lisbon through 2026-11-30 - euro charges from there won't look unusual.
- **Contact channel:** email (replacing text).

I verified your identity to make the contact change. Anything else I can help with?

**Customer:** Can you show me my StreamMax charges?

- `find_transactions({"merchant": "StreamMax"})` → `{"transactions": [{"transaction_id": "T-1001", "posted_on": "2026-09-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-1002", "posted_on": "2026-10-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription …`

**Assistant:** Here are your StreamMax charges:

| Date | Description | Amount | Transaction ID |
|---|---|---|---|
| 2026-09-28 | StreamMax Premium monthly | $15.99 | T-1001 |
| 2026-10-28 | StreamMax Premium monthly | $15.99 | T-1002 |

That's two monthly subscription charges, both in USD. Anything you'd like to do with either one?

**Customer:** Please dispute the later one. I'd cancelled the subscription before it was charged.

- `file_dispute({"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer states the subscription was cancelled before the 2026-10-28 charge."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-c5d1d732", "due": "2026-11-19", "approval": "none", "sent_on": "the contact channel on file when it is sent"}}`

**Assistant:** Done - your dispute is filed.

- **Case ID:** C-5001
- **Transaction:** StreamMax, 2026-10-28, $15.99 (T-1002)
- **Reason:** cancelled subscription
- **Status:** under review
- **Follow-up due:** 2026-11-19, sent to the contact channel on file at that time (currently email)

If you find your cancellation confirmation, send it over and I can attach it to the case - it helps speed things up.

**Customer:** Quick one: what is a chargeback, in two sentences?

**Assistant:** A chargeback is when your card issuer reverses a charge and takes the money back from the merchant's bank after you dispute it, typically because the goods never arrived, the charge was wrong or duplicated, or a cancelled subscription kept billing. You're credited while the issuer investigates, and the merchant can respond with evidence before it's final.

**Customer:** What foreign transaction fee will I pay on my Lisbon purchases?

- `search_policy({"question": "What is the foreign transaction fee on purchases made abroad / in foreign currencies?"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.847, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "travel-notices",  …`

**Assistant:** **1.25% of the US-dollar amount** on any purchase made in a currency other than USD. It posts as a separate line on the same day as the purchase, and a travel notice doesn't waive it.

_Episode written:_ Conversation on 2026-11-09: Priya set a Lisbon travel notice through 2026-11-30 and changed contact from text to email after identity verification. She asked about StreamMax charges and disputed T-1002 ($15.99, 2026-10-28), saying the subscription was cancelled beforehand (not verified). Case C-5001 is under review, follow-up due 2026-11-19 via email. Foreign purchases incur 1.25%. Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | travel notice written as a user-scoped fact (Lisbon, valid until 2026-11-30) | `{"value": "Lisbon", "as_of": "2026-11-09T10:00:00Z", "valid_until": "2026-11-30", "expires_at": "2026-12-01T00:00:00Z"}` |
| PASS | semantic | contact channel written as a user-scoped fact (email) | `{"value": "email", "as_of": "2026-11-09T10:00:00Z", "expires_at": null}` |
| PASS | external | transactions come from an exact ledger lookup | `[{"merchant": "StreamMax"}]` |
| PASS | working | session scope: identity_verified_at persists with this session's state | `persisted session keys: ['episodes_written', 'first_active_at', 'identity_verified_at', 'last_active_at', 'messages', 'reflected_turns']` |
| PASS | working | temp scope: the per-invocation clock (ADK temp:now, LangGraph TurnContext.now) is never persisted | `clock keys found in persisted state: none` |
| PASS | working | 'the later one' resolved from the previous turn's tool result in the session: disputes T-1002 | `[{"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer states the subscription was cancelled before the 2026-10-28 charge."}]` |
| PASS | prospective | filing wrote a scheduler record: case follow-up due 2026-11-19, no approval needed | `[{"trigger_at": "2026-11-19T10:04:00Z", "approval": "none", "status": "pending", "resume": {"case_id": "C-5001"}}]` |
| PASS | parametric | a general concept is answered from the weights, with no tool call | `tools: []` |
| PASS | parametric | ...and it is actually explained (dispute, reversal, refund) | `A chargeback is when your card issuer reverses a charge and takes the money back from the merchant's bank after you dispute it, typically because the goods never arrived, the charge was wrong or duplicated, or a cancelle …` |
| PASS | external | the Kestrel fee quoted at turn 4 was retrieved from policy in this session, not recalled from the weights | `{"documents": [{"document": "foreign-transaction-fees", "score": 0.847, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on ev` |
| PASS | external | the retrieved fee (1.25%) is what the customer is told | `**1.25% of the US-dollar amount** on any purchase made in a currency other than USD. It posts as a separate line on the same day as the purchase, and a travel notice doesn't waive it.` |
| PASS | episodic | session end wrote a reflection episode about the StreamMax dispute | `Conversation on 2026-11-09: Priya set a Lisbon travel notice through 2026-11-30 and changed contact from text to email after identity verification. She asked about StreamMax charges and disputed T-1002 ($15.99, 2026-10-2 …` |

## s2-priya-returns  ·  session  ·  priya  ·  2026-11-12T15:00:00Z

**Customer:** Hi again! Can you remind me what we sorted out last time?

- `load_memory({"query": "last conversation summary"})` → `{"memories": [{"at": "2026-11-09T10:10:00Z", "text": "Conversation on 2026-11-09: Priya set a Lisbon travel notice through 2026-11-30 and changed contact from text to email after identity verification. She asked about StreamMax charges and disputed T-1002 ($15.99, 2026-10-28), saying the subscription was cancelled beforehand (not verified). Case C-5001 is under review, follow-up due 2026-11-19 via …`
- `get_case_status({})` → `{"cases": [{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer states the subscription was cancelled before the 2026-10-28 charge.", "status": "under_review", "opened_at": "2026-11-09T10:04:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null, "decision_id": null}]}`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-c5d1d732", "action": "case_status_followup", "due": "2026-11-19T10:04:00Z", "status": "pending", "sent_on": "the contact channel on file when it is sent (currently email)", "case_id": "C-5001"}]}`

**Assistant:** I'll check what I have on our earlier conversation.
Here's where things stand:

**Your profile (current)**
- Contact channel: email
- Travel notice: Lisbon, until 2026-11-30

**Your dispute**
- Case C-5001 - StreamMax charge of $15.99 on 2026-10-28, disputed as a cancelled subscription. Status: **under review**.
- Follow-up due 2026-11-19, sent to the contact channel on file at that time (currently email).

Nothing else is scheduled right now. Want me to add anything to the case, or is there something else I can help with?

**Customer:** Has that dispute been resolved yet?

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer states the subscription was cancelled before the 2026-10-28 charge.", "status": "under_review", "opened_at": "2026-11-09T10:04:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null, "decision_id": null}]}`

**Assistant:** Not yet. Case C-5001 (StreamMax, $15.99 on 2026-10-28) is still **under review** - no resolution posted as of now.

The follow-up is due 2026-11-19 and will go to your email on file. If you have anything else to support it - like a cancellation reference - I can attach it to the case.

**Customer:** How will you contact me with updates?

- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-c5d1d732", "action": "case_status_followup", "due": "2026-11-19T10:04:00Z", "status": "pending", "sent_on": "the contact channel on file when it is sent (currently email)", "case_id": "C-5001"}]}`

**Assistant:** By **email** - that's the contact channel on your profile. The C-5001 follow-up on 2026-11-19 is set to go out on whatever channel is on file at that time, which is currently email.

You can switch it to SMS or secure message any time - changing it needs a quick identity check (card last 4 digits and billing ZIP).

**Customer:** Actually, please switch that to text messages from now on.

**Assistant:** Happy to switch it to SMS. I just need a quick identity check first - please send me the **last 4 digits of your card** and your **billing ZIP code**. (Only those two things - please don't send the full card number, expiry or security code.)

**Customer:** Sure, card ending 4427, ZIP 94107.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `remember_customer_fact({"key": "contact_channel", "value": "sms"})` → `{"stored": {"contact_channel": {"value": "sms", "as_of": "2026-11-12T15:08:00Z", "expires_at": null}}, "replaced": "email"}`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-c5d1d732", "action": "case_status_followup", "due": "2026-11-19T10:04:00Z", "status": "pending", "sent_on": "the contact channel on file when it is sent (currently sms)", "case_id": "C-5001"}]}`

**Assistant:** Done - you're verified and your contact channel is now **SMS** (previously email).

The C-5001 follow-up due 2026-11-19 will now arrive by text. Anything else?

_Episode written:_ Conversation on 2026-11-12: Customer asked to recall prior arrangements and whether dispute C-5001 (StreamMax, $15.99, txn T-1002) was resolved; it remains under review, not resolved. Customer said the subscription was cancelled before the charge (not verified). Customer requested SMS updates; identity was verified and contact channel changed to SMS. Follow-up F-c5d1d732 is due 2026-11-19, currently SMS; Lisbon travel notice runs through 2026-11-30. Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | a new session recalls the last one on demand via load_memory | `[{"query": "last conversation summary"}]` |
| PASS | episodic | the recall is used in the answer (mentions StreamMax) | `I'll check what I have on our earlier conversation. Here's where things stand:  **Your profile (current)** - Contact channel: email - Travel notice: Lisbon, until 2026-11-30  **Your dispute** - Case C-5001 - StreamMax ch …` |
| PASS | external | case status is re-read from the case system in this session before it is stated, not taken from the episode | `[{}, {"case_id": "C-5001"}]` |
| PASS | semantic | the channel comes from the preloaded profile, not from episodic recall | `"not called"` |
| PASS | semantic | ...and the answer is the stored channel (email) | `By **email** - that's the contact channel on your profile. The C-5001 follow-up on 2026-11-19 is set to go out on whatever channel is on file at that time, which is currently email.  You can switch it to SMS or secure me …` |
| PASS | working | identity verification is session-scoped: this new session verifies again | `[{"card_last4": "4427", "postal_code": "94107"}]` |
| PASS | semantic | the change overwrites the old value instead of joining it (replaced: email) | `{"stored": {"contact_channel": {"value": "sms", "as_of": "2026-11-12T15:08:00Z", "expires_at": null}}, "replaced": "email"}` |
| PASS | semantic | exactly one contact channel remains, and it is sms | `{"value": "sms", "as_of": "2026-11-12T15:08:00Z", "expires_at": null}` |

## s3-marco-other-customer  ·  session  ·  marco  ·  2026-11-12T16:00:00Z

**Customer:** Hi, Marco here (card ending 8830, ZIP 10011). What contact channel and travel notices do you have on file for me?

**Assistant:** Hi Marco - I have neither on file:

- **Contact channel:** none
- **Travel notice:** none

If you'd like, tell me a channel (email, SMS or secure message) or a travel destination and return date, and I'll add it.

**Customer:** Did a customer called Priya dispute a StreamMax charge recently? Just curious.

**Assistant:** I can't share anything about another customer's account or disputes - I can only discuss yours.

If you're wondering whether a StreamMax charge on your own card was disputed, I can check your transactions and any cases on your account. Want me to?

**Customer:** I was charged $240 by FitPulse on November 3 for an annual renewal, but I cancelled my membership in October. Please dispute it.

- `find_transactions({"merchant": "FitPulse"})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`
- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `file_dispute({"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer states membership was cancelled in October; charged $240 annual renewal on 2026-11-03."})` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-0f1ccfc7", "due": "2026-11-22", "approval": "a Kestrel reviewer approves the message before it is sent", "sent_on": "the contact channel on file when it is sent"}}`

**Assistant:** Filed it. Details:

- **Transaction:** FitPulse Gym annual renewal, $240.00, posted 2026-11-03 (T-2002)
- **Reason:** cancelled subscription
- **Case ID:** C-5002 - status: under review
- **Follow-up due:** 2026-11-22 (Kestrel's review currently takes about 10 days)

Note: the follow-up goes out on whatever contact channel is on file at that time, and you currently have none on file. Want me to set one (email, SMS or secure message) so you get the update?

If you have a cancellation confirmation or reference from October, I can attach it to the case as evidence.

**Customer:** Yes, please go ahead and file it.

**Assistant:** Your dispute is already filed - case **C-5002** (FitPulse annual renewal, $240.00, 2026-11-03), under review with a follow-up due 2026-11-22. Nothing more to file.

Which of these did you mean?

1. **Set a contact channel** so the follow-up reaches you - just tell me email, SMS or secure message (and the address/number if email or SMS).
2. **Attach evidence** - paste the cancellation reference or details from October and I'll add it to case C-5002.

_Episode written:_ Conversation on 2026-11-12: Marco asked about his contact channel and travel notices (none on file) and about another customer's StreamMax dispute; assistant declined. He disputed a $240 FitPulse renewal (T-2002, posted 2026-11-03); the customer said he cancelled membership in October (not verified). Dispute C-5002 filed, under review; follow-up due 2026-11-22. No contact channel set; assistant asked whether to add one or evidence. Case outcomes: C-5002 under_review. Lesson: Next time, when multiple same-merchant transactions match an approximate date, confirm the exact transaction/year with the customer before filing.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | no leakage: Marco's profile has none of Priya's facts | `{}` |
| PASS | semantic | no leakage: the reply does not mention Priya's Lisbon trip | `Hi Marco - I have neither on file:  - **Contact channel:** none - **Travel notice:** none  If you'd like, tell me a channel (email, SMS or secure message) or a travel destination and return date, and I'll add it.` |
| PASS | episodic | no leakage: nothing about Priya's dispute reaches Marco | `I can't share anything about another customer's account or disputes - I can only discuss yours.  If you're wondering whether a StreamMax charge on your own card was disputed, I can check your transactions and any cases o …` |
| PASS | episodic | if load_memory runs for Marco it returns none of Priya's episodes | `not called` |
| PASS | external | the FitPulse charge is found by exact lookup | `[{"merchant": "FitPulse"}]` |
| PASS | prospective | the $240 dispute is filed (T-2002) | `[{"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer states membership was cancelled in October; charged $240 annual renewal on 2026-11-03."}]` |
| PASS | prospective | its follow-up needs ops approval: $240 is over the app-wide $200 threshold | `[{"trigger_at": "2026-11-22T16:04:00Z", "approval": "ops_reviewer", "status": "pending", "resume": {"case_id": "C-5002"}}]` |
| PASS | episodic | Marco's own episode exists and holds nothing of Priya's (her case, transaction, amount, trip) | `Conversation on 2026-11-12: Marco asked about his contact channel and travel notices (none on file) and about another customer's StreamMax dispute; assistant declined. He disputed a $240 FitPulse renewal (T-2002, posted  …` |

## ops-decides-c5001  ·  resolve_case  ·  2026-11-18T09:00:00Z

_resolved:_ `[{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer states the subscription was cancelled before the 2026-10-28 charge.", "status": "rejected", "opened_at": "2026-11-09T10:04:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant states no cancellation request is on record. The cardholder may re-file with the merchant's cancellation confirmation (email or reference number).", "resolved_at": "2026-11-18T09:00:00Z", "decision_id": "D-ops-decides-c5001"}]`

## ops-decides-c5002  ·  resolve_case  ·  2026-11-20T09:00:00Z

_resolved:_ `[{"case_id": "C-5002", "user_id": "marco", "txn_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer states membership was cancelled in October; charged $240 annual renewal on 2026-11-03.", "status": "rejected", "opened_at": "2026-11-12T16:04:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant has no cancellation on file for this member. The cardholder may re-file with the merchant's cancellation confirmation.", "resolved_at": "2026-11-20T09:00:00Z", "decision_id": "D-ops-decides-c5002"}]`

## scheduler-2026-11-19  ·  fire_followups  ·  2026-11-19T18:00:00Z

### follow-up session `followup-F-c5d1d732-1`

**Scheduler:** [scheduled follow-up F-c5d1d732] action=case_status_followup resume={"case_id": "C-5001"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer states the subscription was cancelled before the 2026-10-28 charge.", "status": "rejected", "opened_at": "2026-11-09T10:04:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant states no cancellation request is on record. The cardholder ma …`
- `notify_customer({"message": "Update on your dispute C-5001 (subscription charge from 2026-10-28): it was rejected on 2026-11-18 because the merchant says no cancellation request is on record (code NO_CANCELLATION_PRO …)` → `{"channel": "sms", "message_id": 1, "status": "sent"}`

**Assistant:** I'll check the case status.
Case C-5001 was rejected on 2026-11-18 (reason: no cancellation proof on record). I've sent the customer an SMS with the outcome and the next step - re-filing with the merchant's cancellation confirmation via the card-care chat.

_Episode written:_ Scheduled follow-up on 2026-11-19 (customer not present): Customer sought resolution of dispute C-5001 (txn T-1002), a 2026-10-28 subscription charge; it was rejected on 2026-11-18 for NO_CANCELLATION_PROOF. The customer said the subscription was cancelled before the charge (not verified). Assistant checked status and sent one SMS with the outcome and next step: re-file via card-care chat with merchant cancellation confirmation. No preference or promise stated. Case outcomes: C-5001 rejected (NO_CANCELLATION_PROOF). Lesson: none

_outcomes:_ `[{"followup_id": "F-c5d1d732", "user_id": "priya", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | Priya's follow-up fires on its trigger date and is marked done on evidence | `[{"followup_id": "F-c5d1d732", "user_id": "priya", "outcome": "fired_done", "error": null}]` |
| PASS | prospective | Marco's follow-up is not due yet and does not fire | `[]` |
| PASS | semantic | the channel is read at fire time, so Priya's later change to sms is honoured | `[{"message_id": 1, "user_id": "priya", "channel": "sms", "body": "Update on your dispute C-5001 (subscription charge from 2026-10-28): it was rejected on 2026-11-18 because the merchant says no cancellation request is on …` |
| PASS | episodic | the follow-up session's episode carries the case system's outcome code | `latest episode outcome codes: ['NO_CANCELLATION_PROOF']` |

## s4-priya-after-rejection  ·  session  ·  priya  ·  2026-11-20T11:00:00Z

**Customer:** I got your text. Why was the StreamMax dispute rejected, and what can I do now?

- `get_case_status({})` → `{"cases": [{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer states the subscription was cancelled before the 2026-10-28 charge.", "status": "rejected", "opened_at": "2026-11-09T10:04:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant states no cancellation request is on record. The cardholder ma …`
- `load_memory({"query": "StreamMax dispute"})` → `{"memories": [{"at": "2026-11-09T10:10:00Z", "text": "Conversation on 2026-11-09: Priya set a Lisbon travel notice through 2026-11-30 and changed contact from text to email after identity verification. She asked about StreamMax charges and disputed T-1002 ($15.99, 2026-10-28), saying the subscription was cancelled beforehand (not verified). Case C-5001 is under review, follow-up due 2026-11-19 via …`
- `search_policy({"question": "Can a customer re-file a dispute that was rejected for no cancellation proof, and what evidence is needed?"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.741, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`
- `find_transactions({"merchant": "StreamMax"})` → `{"transactions": [{"transaction_id": "T-1001", "posted_on": "2026-09-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-1002", "posted_on": "2026-10-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription …`

**Assistant:** Here's what the record shows:

**Case C-5001 - StreamMax, $15.99, 2026-10-28 (T-1002)**
- Status: **rejected** on 2026-11-18
- Reason code: `NO_CANCELLATION_PROOF` - the merchant told us there's no cancellation request on record, and we had no cancellation confirmation on file to counter that.

That's the text you got: the case was decided on 2026-11-18, so the follow-up arrived after the fact rather than as an update.

**What you can do now:** you can re-file. The charge posted 2026-10-28 and disputes are accepted within **75 days of the posting date**, so you're well inside the window (until roughly 2027-01-11). A re-file only stands a chance with evidence the merchant accepts - a cancellation confirmation email or the merchant's cancellation/ticket reference number showing you cancelled before 2026-10-28.

Do you have a cancellation confirmation or reference from StreamMax? If so, tell me what it is and, to file, I'll need your card's last 4 digits and billing ZIP typed here so I can verify you first. If you don't have proof yet, ask StreamMax support for written confirmation of your cancellation date - that's the missing piece the first case failed on.

**Customer:** OK. Please send me a reminder on November 29 to set up a travel notice for my Porto trip.

- `list_my_followups({})` → `{"scheduled": []}`
- `schedule_reminder({"note": "Set up a travel notice for your Porto trip", "remind_on": "2026-11-29"})` → `{"followup_id": "F-b34f219d", "due": "2026-11-29T09:00:00Z", "local_time": "2026-11-29 09:00 UTC"}`

**Assistant:** Done - reminder set for **2026-11-29 at 09:00 UTC** (id F-b34f219d), delivered to your SMS channel.

One thing to note: your current travel notice is Lisbon through 2026-11-30. If Porto starts before then, adding it will replace the Lisbon notice rather than sit alongside it - so when you set it up, tell me the Porto dates and I'll sort it out. You can also just reply to the reminder then.

**Customer:** Before I go, give me a quick recap of everything we've discussed across our conversations.

- `load_memory({"query": "Priya conversations summary travel notice contact channel StreamMax dispute"})` → `{"memories": [{"at": "2026-11-09T10:10:00Z", "text": "Conversation on 2026-11-09: Priya set a Lisbon travel notice through 2026-11-30 and changed contact from text to email after identity verification. She asked about StreamMax charges and disputed T-1002 ($15.99, 2026-10-28), saying the subscription was cancelled beforehand (not verified). Case C-5001 is under review, follow-up due 2026-11-19 via …`

**Assistant:** Here's the recap from our past conversations (current as of today, 2026-11-20):

**StreamMax dispute - C-5001**
- 2026-11-09: you disputed T-1002, $15.99 posted 2026-10-28, as `cancelled_subscription`, saying you'd cancelled before the charge (no proof supplied at the time).
- 2026-11-12: you checked in - it was still under review.
- 2026-11-18: the case was **rejected** for `NO_CANCELLATION_PROOF` (merchant says no cancellation request on record). The follow-up SMS went out 2026-11-19. Today we covered re-filing with a cancellation confirmation or merchant reference - you're inside the 75-day window until about 2027-01-11.

**Travel notice**
- Set 2026-11-09: Lisbon, valid through 2026-11-30. That's the notice on file now.

**Contact channel**
- Was email (changed 2026-11-09), then you asked for SMS on 2026-11-12. SMS is current, and that's where the reminder will arrive.

**Reminders**
- New today: F-b34f219d, 2026-11-29 at 09:00 UTC, to set up a travel notice for Porto. Nothing else is scheduled.

**Also mentioned:** foreign purchases carry a 1.25% fee.

One open point: if Porto starts before 2026-11-30, adding that notice will replace the Lisbon one - tell me the dates when you're ready.

_Episode written:_ Conversation on 2026-11-20: Customer asked about rejected StreamMax case C-5001 (transaction T-1002, $15.99, 2026-10-28) and next steps. Assistant explained no-cancellation-proof rejection and possible re-filing with merchant confirmation/reference within 75 days (until about 2027-01-11). The customer said subscription was cancelled beforehand (not verified). Assistant set SMS reminder F-b34f219d for 2026-11-29 09:00 UTC to arrange a Porto travel notice; Lisbon notice is through 2026-11-30. SMS is current. Case outcomes: C-5001 rejected (NO_CANCELLATION_PROOF). Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the rejection reason comes from the case system | `[{}]` |
| PASS | external | ...and is relayed (cancellation confirmation) | `Here's what the record shows:  **Case C-5001 - StreamMax, $15.99, 2026-10-28 (T-1002)** - Status: **rejected** on 2026-11-18 - Reason code: `NO_CANCELLATION_PROOF` - the merchant told us there's no cancellation request o …` |
| PASS | prospective | a customer-requested reminder becomes a scheduler record for 2026-11-29 | `[{"trigger_at": "2026-11-29T09:00:00Z", "approval": "none", "status": "pending", "resume": {"note": "Set up a travel notice for your Porto trip"}}]` |
| PASS | episodic | a cross-session recap is built from load_memory run in this session | `[{"query": "StreamMax dispute"}, {"query": "Priya conversations summary travel notice contact channel StreamMax dispute"}]` |
| PASS | episodic | ...and uses more than one past episode (StreamMax and the switch to text) | `Here's the recap from our past conversations (current as of today, 2026-11-20):  **StreamMax dispute - C-5001** - 2026-11-09: you disputed T-1002, $15.99 posted 2026-10-28, as `cancelled_subscription`, saying you'd cance …` |

## scheduler-2026-11-22-a  ·  fire_followups  ·  2026-11-22T18:00:00Z

### follow-up session `followup-F-0f1ccfc7-1`

**Scheduler:** [scheduled follow-up F-0f1ccfc7] action=case_status_followup resume={"case_id": "C-5002"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `get_case_status({"case_id": "C-5002"})` → `{"cases": [{"case_id": "C-5002", "user_id": "marco", "txn_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer states membership was cancelled in October; charged $240 annual renewal on 2026-11-03.", "status": "rejected", "opened_at": "2026-11-12T16:04:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant has no cancellation on file for this member …`
- `notify_customer({"message": "Update on dispute C-5002 (the $240 annual renewal charged 2026-11-03): the case was closed on 2026-11-20 as rejected \u2014 the merchant has no cancellation on file for your membership. N …)` → `{"channel": "secure_message", "message_id": 2, "status": "held for a Kestrel reviewer to approve before it is sent"}`

**Assistant:** I'll check the case status now.
Done. Case C-5002 was rejected on 2026-11-20 (resolution code NO_CANCELLATION_PROOF), and I sent the customer one secure message explaining the outcome and that they can re-file with the merchant's cancellation confirmation. The message is held for a Kestrel reviewer to approve before it goes out.

_Episode written:_ Scheduled follow-up on 2026-11-22 (customer not present): The customer said membership was cancelled in October and disputed a $240 annual renewal charged 2026-11-03 (not verified). Assistant checked case C-5002 (txn T-2002): rejected 2026-11-20, code NO_CANCELLATION_PROOF, merchant had no cancellation on file. Assistant sent one secure message explaining outcome and that customer may re-file with merchant cancellation confirmation; message held for reviewer approval. Case outcomes: C-5002 rejected (NO_CANCELLATION_PROOF). Lesson: none

_outcomes:_ `[{"followup_id": "F-0f1ccfc7", "user_id": "marco", "outcome": "awaiting_approval", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | Marco's follow-up fires, and the agent's draft is held: its approval field names ops_reviewer | `[{"followup_id": "F-0f1ccfc7", "user_id": "marco", "outcome": "awaiting_approval", "error": null}]` |
| PASS | prospective | nothing reaches Marco before a person has read the drafted message | `[{"message_id": 2, "user_id": "marco", "channel": "secure_message", "body": "Update on dispute C-5002 (the $240 annual renewal charged 2026-11-03): the case was closed on 2026-11-20 as rejected - the merchant has no canc …` |

## ops-lead-approves-marco  ·  approve_followups  ·  marco  ·  2026-11-22T18:10:00Z

_approved:_ `[{"followup_id": "F-0f1ccfc7", "user_id": "marco", "action": "case_status_followup", "trigger_at": "2026-11-22T16:04:00Z", "approval": "ops_reviewer", "status": "done", "attempts": 1, "approved_by": "ops-lead", "created_at": "2026-11-12T16:04:00Z", "fired_at": "2026-11-22T18:00:00Z", "done_at": "2026-11-22T18:10:00Z", "cancelled_at": null, "last_error": null, "resume": {"case_id": "C-5002"}}]`

_rejected:_ `[]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | the reviewer approves the drafted message itself, which is then sent | `[{"message_id": 2, "user_id": "marco", "channel": "secure_message", "body": "Update on dispute C-5002 (the $240 annual renewal charged 2026-11-03): the case was closed on 2026-11-20 as rejected - the merchant has no canc …` |
| PASS | prospective | with no channel on file it uses the default secure_message | `[{"message_id": 2, "user_id": "marco", "channel": "secure_message", "body": "Update on dispute C-5002 (the $240 annual renewal charged 2026-11-03): the case was closed on 2026-11-20 as rejected - the merchant has no canc …` |
| PASS | guard | no outbound message or episode so far carries a masking token or a masked identifier | `8 outbound messages and episodes clean` |

## scheduler-2026-11-22-b  ·  fire_followups  ·  2026-11-22T18:30:00Z

_outcomes:_ `[]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | done flag: a later run fires nothing | `[]` |

## s4m-marco-after-rejection  ·  session  ·  marco  ·  2026-11-23T10:00:00Z

**Customer:** I got your message. Why was my FitPulse dispute rejected?

- `get_case_status({"case_id": null})` → `{"cases": [{"case_id": "C-5002", "user_id": "marco", "txn_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer states membership was cancelled in October; charged $240 annual renewal on 2026-11-03.", "status": "rejected", "opened_at": "2026-11-12T16:04:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant has no cancellation on file for this member …`
- `list_my_followups({})` → `{"scheduled": []}`
- `search_policy({"question": "re-filing a dispute after rejection for no cancellation proof, deadlines"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.732, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`

**Assistant:** Your dispute on the FitPulse charge (case C-5002) was rejected on 20 Nov with the reason **no cancellation proof**: the merchant has no cancellation on file for your membership, so they contested it. The charge itself was the $240 annual renewal dated 2026-11-03.

You can re-file if you can supply FitPulse's cancellation confirmation (the email or a reference number). Two things to note:

- The dispute window is 75 days from the charge's posting date, which for this charge runs to about **17 Jan 2027**.
- Re-filing is a new dispute, so I'd need to verify your identity first - card last 4 digits and billing ZIP.

If you have the confirmation handy, send it over and I'll start the re-file.

_Episode written:_ Conversation on 2026-11-23: Customer asked why FitPulse dispute was rejected. Assistant explained case C-5002 (txn T-2002) was rejected 20 Nov for no cancellation proof; the $240 renewal dated 2026-11-03 was contested because the merchant had no cancellation on file. Customer said membership was cancelled in October (not verified). Assistant offered re-filing with FitPulse cancellation confirmation by 17 Jan 2027, subject to identity verification. Case outcomes: C-5002 rejected (NO_CANCELLATION_PROOF). Lesson: Next time, verify any dispute-window deadline in the policy document before stating it to the customer.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | Marco's rejection reason is read from the case system | `[{"case_id": null}]` |

## promote-recurring-lesson  ·  promote  ·  2026-11-23T12:00:00Z

_Model draft:_ Before calling file_dispute, ask the cardholder for the merchant’s cancellation confirmation (email or reference number) and only call file_dispute once it is provided, passing that confirmation as the evidence_note. Before stating any dispute-window deadline, verify the deadline in the policy document.

_Routing probe (ops-only approval):_ REFUSED: Before calling file_dispute, ask the cardholder for the merchant’s can; REFUSED: File a cancelled_subscription dispute only after the customer provides; REFUSED: Require the merchant's cancellation confirmation before calling file_d; REFUSED: Decline to file a cancelled_subscription dispute until the customer su; REFUSED: Refuse cancelled_subscription disputes that lack a cancellation confir; REFUSED: Hold off on filing a cancelled_subscription dispute until a cancellati; REFUSED: A cancelled_subscription dispute must include the merchant's cancellat; REFUSED: Without a cancellation confirmation, a cancelled_subscription dispute ; REFUSED: Ask whether the customer has the merchant's cancellation confirmation,

_Reviewer-approved rule, promoted to v2:_ Before filing a cancelled_subscription dispute, ask whether the customer has the merchant's cancellation confirmation (an email or a reference number). If they have it, pass it as evidence_note. If they do not, tell them disputes without it have been rejected before, and file the dispute anyway if they still want it filed.

_Evidence (registry only, never in the prompt):_ episodes ['E-s4-priya-after-rejection-1', 'E-s4m-marco-after-rejection-1'] from customers ['marco', 'priya'], decisions ['D-ops-decides-c5001', 'D-ops-decides-c5002']

| | memory type | check | evidence |
|---|---|---|---|
| PASS | procedural | a rule is promoted only from conversations with two different customers, on two separate decisions | `{"resolution_code": "NO_CANCELLATION_PROOF", "users": ["marco", "priya"], "decisions": ["D-ops-decides-c5001", "D-ops-decides-c5002"], "episodes": ["E-s4-priya-after-rejection-1", "E-s4m-marco-after-rejection-1"], "lesso …` |
| PASS | procedural | the promoted rule lives in a new instruction version (v2), now active | `active: v2` |
| PASS | procedural | the instruction every customer sees names no customer | `no customer identifier in the active procedure` |
| PASS | procedural | routing by source: no rule text, the model's draft or any paraphrased refusal, ships on ops approval alone | `all 9 refused` |

## s5-dana-under-v2  ·  session  ·  dana  ·  2026-11-24T10:00:00Z

**Customer:** Hi, I'm Dana (card ending 5127, ZIP 60614). I cancelled CloudNest Storage in October but they still charged me $9.99 on November 1. Please dispute it.

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`

**Assistant:** I'll look up the charge and verify your identity.
I found the charge: **CloudNest Storage, $9.99, posted 2026-11-01** (transaction T-3002). Your identity is verified, so I can file right away.

One question first: for cancelled-subscription disputes we ask whether you have the merchant's cancellation confirmation - an email or a reference number from when you cancelled in October. Do you have that? If so, I'll attach it as evidence with your dispute.

**Customer:** Sure, the cancellation reference CloudNest gave me is CN-77812.

- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Merchant cancellation reference: CN-77812 (subscription cancelled in October)."})` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-578e4df1", "due": "2026-12-04", "approval": "none", "sent_on": "the contact channel on file when it is sent"}}`

**Assistant:** Done - your dispute is filed.

- **Case ID:** C-5003 (CloudNest Storage, $9.99, 2026-11-01), status: under review
- **Cancellation reference CN-77812** was attached as evidence
- **Follow-up due:** 2026-12-04

One thing to note: the follow-up goes out on whatever contact channel is on file when it's sent, and you currently have none set. Would you like to add one - email, SMS, or secure message? You can also add more evidence to case C-5003 at any time if you find more from CloudNest.

_Episode written:_ Conversation on 2026-11-24: The customer said she cancelled CloudNest in October (not verified) and disputed the 2026-11-01 $9.99 charge; she provided CN-77812 (not verified). Identity verified; dispute filed on T-3002 as C-5003, under review, with follow-up F-578e4df1 due 2026-12-04. No contact-channel preference stated. Case outcomes: C-5003 under_review. Lesson: Confirm and record a follow-up contact channel before finalizing the dispute, since none was on file when the follow-up was scheduled.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | procedural | under v2 the agent does not file before asking for the cancellation confirmation | `"not called"` |
| PASS | procedural | ...it asks for it | `I'll look up the charge and verify your identity. I found the charge: **CloudNest Storage, $9.99, posted 2026-11-01** (transaction T-3002). Your identity is verified, so I can file right away.  One question first: for ca …` |
| PASS | procedural | ...and files with it as evidence | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Merchant cancellation reference: CN-77812 (subscription cancelled in October)."}]` |

## retraction-drill  ·  retract  ·  2026-11-24T12:00:00Z

_affected:_ `[{"user_id": "dana", "episode_id": "E-s5-dana-under-v2-1", "at": "2026-11-24T10:04:00Z", "outcomes": [{"case_id": "C-5003", "txn_id": "T-3002", "reason": "cancelled_subscription", "status": "under_review", "resolution_code": null, "resolution_note": null, "resolved_at": null, "decision_id": null}]}]`

_Registry history:_ `[{"event": "baseline", "version": "v1"}, {"event": "promoted", "version": "v2", "based_on": "v1", "by": ["ops-lead (scripted reviewer)", "disputes-policy-owner (scripted reviewer)"], "at": "2026-11-23T12:00:00Z"}, {"event": "retracted", "version": "v2", "active_now": "v1", "by": "ops-lead (scripted reviewer)", "reason": "retraction drill: prove a promoted rule can be removed", "at": "2026-11-24T12:00:00Z"}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | procedural | the retraction path restores v1 | `active: v1` |
| PASS | procedural | the retraction lists the conversations held under v2, for review (Dana's) | `[["dana", "E-s5-dana-under-v2-1"]]` |

## s5c-eli-control-under-v1  ·  session  ·  eli  ·  2026-11-24T13:00:00Z

**Customer:** Hi, I'm Eli (card ending 6610, ZIP 73301). I cancelled CloudNest Storage in October but they still charged me $9.99 on November 1. Please dispute it.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer states the CloudNest Storage subscription was cancelled in October 2026, but a $9.99 charge posted on 2026-1 …)` → `{"case_id": "C-5004", "status": "under_review", "followup": {"followup_id": "F-a4a147ee", "due": "2026-12-04", "approval": "none", "sent_on": "the contact channel on file when it is sent"}}`

**Assistant:** I'll verify your identity and look up that charge.
Done - your dispute is filed.

- **Case:** C-5004, status **under review**
- **Charge:** CloudNest Storage, $9.99, posted 2026-11-01
- **Follow-up due:** 2026-12-04, sent automatically on whatever contact channel is on file

One thing: you have **no contact channel on file**, so the follow-up has nowhere to go. If you'd like, tell me whether you want email, SMS or secure message and I'll set it (changing the contact channel requires re-verifying your card and ZIP at that point).

If you have a cancellation confirmation or reference from CloudNest, send it over and I'll attach it to the case.

_Episode written:_ Conversation on 2026-11-24: Eli asked to dispute a $9.99 CloudNest Storage charge posted 2026-11-01; the customer said the subscription was cancelled in October (not verified). Identity verified; dispute C-5004 filed for transaction T-4002, under review, follow-up due 2026-12-04. Assistant noted no contact channel on file and offered email, SMS, or secure message after re-verification; no preference stated. Case outcomes: C-5004 under_review. Lesson: Next time, the assistant should confirm the customer's contact channel before or immediately after filing the dispute so the follow-up due 2026-12-04 can be delivered.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | procedural | control: the same request under v1 is filed straight away, without the promoted check | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer states the CloudNest Storage subscription was cancelled in October 2026, but a $9.99 charge posted on 2026-11-01."}]` |

## scheduler-2026-11-29  ·  fire_followups  ·  2026-11-29T18:00:00Z

### follow-up session `followup-F-b34f219d-1`

**Scheduler:** [scheduled follow-up F-b34f219d] action=customer_reminder resume={"note": "Set up a travel notice for your Porto trip"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `search_policy({"question": "How does a customer set up a travel notice, and what does it cover?"})` → `{"documents": [{"document": "travel-notices", "score": 0.764, "text": "# Travel notices\n\nA travel notice tells Kestrel's fraud systems that card use in another country is expected, which reduces false declines while you travel. Give the destination and the date you return. Kestrel keeps a travel notice only until the return date and deletes it automatically afterwards; a new trip needs a new not …`
- `list_my_followups({})` → `{"scheduled": []}`
- `notify_customer({"message": "Reminder: set up a travel notice for your Porto trip. A travel notice tells Kestrel's fraud systems to expect card use abroad, reducing false declines; give the destination and return dat …)` → `{"channel": "sms", "message_id": 3, "status": "sent"}`

**Assistant:** Sent the reminder by SMS: it asks you to set up a travel notice for your Porto trip, with the destination and return date, and notes that your Lisbon notice (until 2026-11-30) doesn't cover Porto. To add it, message the card-care chat - replies to this message aren't received.

_Episode written:_ Scheduled follow-up on 2026-11-29 (customer not present): The scheduled follow-up F-b34f219d wanted the customer reminded to set up a Porto travel notice. Assistant sent one SMS (message_id 3, sent) with destination/return-date instructions and directed them to card-care chat; it stated an unverified Lisbon notice until 2026-11-30. No transaction ID, promise, preference, reply, or setup confirmed. Case outcomes: no case touched. Lesson: Verify account-specific details, such as an existing travel notice, before including them in a customer message.

_outcomes:_ `[{"followup_id": "F-b34f219d", "user_id": "priya", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | Priya's reminder fires on the date she chose | `[{"followup_id": "F-b34f219d", "user_id": "priya", "outcome": "fired_done", "error": null}]` |
| PASS | prospective | the reminder carries its resume note to her current channel | `{"message_id": 3, "user_id": "priya", "channel": "sms", "body": "Reminder: set up a travel notice for your Porto trip. A travel notice tells Kestrel's fraud systems to expect card use abroad, reducing false declines; giv …` |

## s6a-priya-staleness  ·  session  ·  priya  ·  2026-12-03T10:00:00Z

**Customer:** I'm in Porto now and just saw a charge from Livraria Porto. Is my travel notice still active?

- `load_memory({"query": "travel notice Porto"})` → `{"memories": [{"at": "2026-11-29T18:00:00Z", "text": "Scheduled follow-up on 2026-11-29 (customer not present): The scheduled follow-up F-b34f219d wanted the customer reminded to set up a Porto travel notice. Assistant sent one SMS (message_id 3, sent) with destination/return-date instructions and directed them to card-care chat; it stated an unverified Lisbon notice until 2026-11-30. No transacti …`

**Assistant:** No - there's no travel notice on your account right now. The only one I have any record of was a Lisbon notice, and that ran through 2026-11-30, so it's expired as well as not being on file.

If you want a Porto notice set up, tell me your return date and I'll add it. I can also pull up the Livraria Porto charge if you'd like to check it.

_Episode written:_ Conversation on 2026-12-03: The customer said they were in Porto and saw a Livraria Porto charge (not verified), asking if their travel notice was active. Assistant said no active notice; only an expired/unverified Lisbon notice through 2026-11-30. Assistant offered to add a Porto notice if given return date and to pull up the charge. No case touched; no transaction ID; no setup completed. Case outcomes: no case touched. Lesson: Next time, verify the account's current travel-notice status before stating that no active notice exists, since the memory was unverified.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | staleness: the Lisbon notice expired on 2026-11-30 and is deleted at turn start, not by any tool | `null` |
| PASS | semantic | ...the agent did not delete it itself | `"not called"` |
| PASS | semantic | staleness: the reply says no notice is active | `No - there's no travel notice on your account right now. The only one I have any record of was a Lisbon notice, and that ran through 2026-11-30, so it's expired as well as not being on file.  If you want a Porto notice s …` |
| PASS | semantic | staleness: the expired Lisbon notice is not presented as current | `No - there's no travel notice on your account right now. The only one I have any record of was a Lisbon notice, and that ran through 2026-11-30, so it's expired as well as not being on file.  If you want a Porto notice s …` |

## s6b-priya-forgetting-and-secrets  ·  session  ·  priya  ·  2026-12-03T10:30:00Z

**Customer:** Please set a travel notice for Porto until December 10.

- `remember_customer_fact({"key": "travel_notice", "value": "Porto", "valid_until": "2026-12-10"})` → `{"stored": {"travel_notice": {"value": "Porto", "as_of": "2026-12-03T10:30:00Z", "valid_until": "2026-12-10", "expires_at": "2026-12-11T00:00:00Z"}}, "replaced": null}`
- `search_policy({"question": "travel notice how it works, what it covers, destinations and dates"})` → `{"documents": [{"document": "travel-notices", "score": 0.816, "text": "# Travel notices\n\nA travel notice tells Kestrel's fraud systems that card use in another country is expected, which reduces false declines while you travel. Give the destination and the date you return. Kestrel keeps a travel notice only until the return date and deletes it automatically afterwards; a new trip needs a new not …`

**Assistant:** Done - travel notice set for Porto through December 10. Kestrel's fraud systems will expect card use there, which reduces false declines, and the notice is deleted automatically after your return date.

**Customer:** Actually, on second thought, delete that travel notice. I'd rather you didn't keep my travel plans.

- `forget_customer_fact({"key": "travel_notice"})` → `{"forgotten": "travel_notice", "had_value": true, "note": "deleted from memory now; conversation transcripts are deleted after 30 days, or at once if the customer asks to erase everything"}`

**Assistant:** Deleted - the Porto travel notice is gone and I'm not keeping your travel plans.

Note that with no travel notice on file, card use in Portugal may be more likely to trigger a fraud decline. If you change your mind, just tell me and I'll set it again.

**Customer:** In case you need it, my full card number is [REDACTED CARD NUMBER].

**Assistant:** That part of your message was removed before it reached me, and I don't need it - please don't send your full card number. For anything that requires verification I only need the last 4 digits and your billing ZIP, which you can type when I ask.

_Episode written:_ Conversation on 2026-12-03: Customer asked to set a Porto travel notice until Dec 10, then delete it because they didn’t want travel plans kept. It was stored and forgotten; no case/transaction IDs appeared. Customer sent a full card number, which was removed; assistant advised not to send it and said last 4 digits plus billing ZIP suffice when asked. Case outcomes: no case touched. Lesson: When a customer deletes stored travel data for privacy, confirm deletion and explain transcript retention and the option to erase everything.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | a new fact can be written | `[{"key": "travel_notice", "value": "Porto", "valid_until": "2026-12-10"}]` |
| PASS | semantic | deletion on request: forget_customer_fact runs | `[{"key": "travel_notice"}]` |
| PASS | semantic | ...and the fact is gone from the store | `null` |
| PASS | guard | a pasted card number is masked before it enters the session | `In case you need it, my full card number is [REDACTED CARD NUMBER].` |
| PASS | guard | the card number is in no store: sessions, memory, bank, scheduler | `found in: nowhere` |

## s7-parametric-prevented  ·  session  ·  priya  ·  2026-12-03T11:00:00Z

**Customer:** What is Kestrel's late payment fee?

- `search_policy({"question": "What is the late payment fee?"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.681, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "cancelled-subscri …`
- `search_policy({"question": "late payment fee amount charged when payment is late"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.669, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`

**Assistant:** I don't have that figure - our policy documents don't cover a late payment fee, so I can't quote one. If you'd like, I can help with something else, like a fee that does appear in policy (the foreign transaction fee is 1.25% of the USD amount), or check a specific charge on your account.

_Episode written:_ Conversation on 2026-12-03: Customer asked for Kestrel’s late payment fee. Policy searches returned no late-fee document, so the assistant said it could not quote a fee and offered help with other policy-covered fees or a specific charge. No case or transaction IDs were provided, and no promises or preferences were stated. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the agent looks the figure up instead of answering from its weights | `[{"question": "What is the late payment fee?"}, {"question": "late payment fee amount charged when payment is late"}]` |
| PASS | parametric | prevented: the KB has no late fee, so the agent states no dollar figure | `I don't have that figure - our policy documents don't cover a late payment fee, so I can't quote one. If you'd like, I can help with something else, like a fee that does appear in policy (the foreign transaction fee is 1 …` |

## s7b-bare-weights-probe  ·  parametric_probe  ·  2026-12-03T11:10:00Z

**Customer:** What is Kestrel Card's late payment fee? Answer with a dollar amount.

**Assistant:** $25

| | memory type | check | evidence |
|---|---|---|---|
| PASS | parametric | observed: the same question to the bare model (no instruction, no tools) gets an invented figure | `$25` |

## retention-2027-06-15  ·  maintenance  ·  2027-06-15T00:00:00Z

_maintenance:_ `{"erased_customers": [], "closed_idle_sessions": [], "purged_episodes": ["E-s1-priya-first-contact-1", "E-s2-priya-returns-1", "E-s3-marco-other-customer-1", "E-followup-F-c5d1d732-1-1", "E-s4-priya-after-rejection-1", "E-followup-F-0f1ccfc7-1-1", "E-s4m-marco-after-rejection-1", "E-s5-dana-under-v2-1", "E-s5c-eli-control-under-v1-1", "E-followup-F-b34f219d-1-1", "E-s6a-priya-staleness-1", "E-s6b-priya-forgetting-and-secrets-1", "E-s7-parametric-prevented-1"], "deleted_transcripts": ["s5-dana-under-v2", "s5c-eli-control-under-v1", "followup-F-0f1ccfc7-1", "s3-marco-other-customer", "s4m-marco- …`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | forgetting on purpose: episodes past their 180-day retention are deleted | `0 episodes; purged 0` |
| PASS | working | ...and transcripts past their 30-day retention are deleted too | `0 transcripts: []` |

## s8-priya-after-retention  ·  session  ·  priya  ·  2027-06-15T10:00:00Z

**Customer:** Hi! What did we talk about last time?

- `load_memory({"query": "previous conversation with customer"})` → `{"memories": []}`

**Assistant:** I checked, and I don't have any record of a previous conversation with you - so I can't say what we talked about last time.

What I can see right now: your contact channel is set to SMS, and there's no travel notice on file.

Is there something I can help you with today?

_Episode written:_ Conversation on 2027-06-15: The customer asked what they discussed last time. The assistant loaded memory, found no previous conversation records, and said it could not say. The assistant also noted the contact channel is SMS and no travel notice is on file. No case or transaction IDs, promises, or customer-stated preferences were present. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | recall after retention finds nothing, because nothing is kept | `{"memories": []}` |
