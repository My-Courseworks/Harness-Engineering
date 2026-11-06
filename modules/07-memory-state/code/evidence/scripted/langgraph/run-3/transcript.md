# langgraph · scripted · run 3

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## s1-priya-first-contact  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Hi, it's Priya (card ending 4427, billing ZIP 94107). I'm in Lisbon until November 30, so you'll see euro charges. Also, please contact me by email from now on, not text.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `remember_customer_fact({"key": "travel_notice", "value": "Lisbon", "valid_until": "2026-11-30"})` → `{"stored": {"travel_notice": {"value": "Lisbon", "as_of": "2026-11-09T10:00:00Z", "valid_until": "2026-11-30", "expires_at": "2026-12-01T00:00:00Z"}}, "replaced": null}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-09T10:00:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** You're all set, Priya. I've verified your identity (card ending 4427) and noted:

- **Travel notice:** Lisbon until 2026-11-30 — euro charges from there won't be flagged.
- **Contact channel:** email from now on, so any case updates and follow-ups will go to your email instead of text.

Anything else I can help with?

**Customer:** Can you show me my StreamMax charges?

- `find_transactions({"merchant": "StreamMax"})` → `{"transactions": [{"transaction_id": "T-1001", "posted_on": "2026-09-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-1002", "posted_on": "2026-10-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription …`

**Assistant:** Here are your StreamMax charges:

| Date | Description | Amount |
|---|---|---|
| 2026-09-28 | StreamMax Premium monthly | $15.99 |
| 2026-10-28 | StreamMax Premium monthly | $15.99 |

Both are $15.99 USD monthly subscription charges. Let me know if you'd like to dispute either one or need anything else.

**Customer:** Please dispute the later one. I'd cancelled the subscription before it was charged.

- `file_dispute({"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer states the StreamMax subscription was cancelled before the 2026-10-28 charge was posted."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-ee4663f2", "due": "2026-11-19", "approval": "none", "sent_on": "the contact channel on file when it is sent"}}`

**Assistant:** Dispute filed for the 2026-10-28 StreamMax charge of $15.99.

- **Case ID:** C-5001
- **Status:** Under review
- **Follow-up due:** 2026-11-19 — it will be sent to your email on file.

If you find a cancellation confirmation or reference from StreamMax, send it over and I can attach it to the case.

**Customer:** Quick one: what is a chargeback, in two sentences?

**Assistant:** A chargeback is a process where your card issuer reverses a disputed charge and pulls the funds back from the merchant's bank, which is then required to respond. It's typically used when a merchant won't resolve an issue like a duplicate charge, a cancelled subscription still billing you, or goods you never received.

**Customer:** What foreign transaction fee will I pay on my Lisbon purchases?

- `search_policy({"question": "foreign transaction fee for purchases abroad"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.848, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "travel-notices",  …`

**Assistant:** **1.25% of the US-dollar amount** on each purchase made in a currency other than USD. It posts as a separate line on the same day as the purchase — and note that your travel notice doesn't waive or change it.

_Episode written:_ Conversation on 2026-11-09: Customer wanted a Lisbon travel notice until 2026-11-30, email contact, StreamMax charges, and a dispute of the later charge. Identity verified; travel notice and email preference stored. Dispute T-1002 became case C-5001, under review, follow-up due 2026-11-19 by email. Customer said subscription was cancelled before charge (not verified). Assistant explained chargebacks and the 1.25% foreign fee. Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | travel notice written as a user-scoped fact (Lisbon, valid until 2026-11-30) | `{"value": "Lisbon", "as_of": "2026-11-09T10:00:00Z", "valid_until": "2026-11-30", "expires_at": "2026-12-01T00:00:00Z"}` |
| PASS | semantic | contact channel written as a user-scoped fact (email) | `{"value": "email", "as_of": "2026-11-09T10:00:00Z", "expires_at": null}` |
| PASS | external | transactions come from an exact ledger lookup | `[{"merchant": "StreamMax"}]` |
| PASS | working | session scope: identity_verified_at persists with this session's state | `persisted session keys: ['episodes_written', 'identity_verified_at', 'last_active_at', 'messages', 'reflected_turns']` |
| PASS | working | temp scope: the per-invocation clock (ADK temp:now, LangGraph TurnContext.now) is never persisted | `clock keys found in persisted state: none` |
| PASS | working | 'the later one' resolved from the previous turn's tool result in the session: disputes T-1002 | `[{"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer states the StreamMax subscription was cancelled before the 2026-10-28 charge was posted."}]` |
| PASS | prospective | filing wrote a scheduler record: case follow-up due 2026-11-19, no approval needed | `[{"trigger_at": "2026-11-19T10:04:00Z", "approval": "none", "status": "pending", "resume": {"case_id": "C-5001"}}]` |
| PASS | parametric | a general concept is answered from the weights, with no tool call | `tools: []` |
| PASS | parametric | ...and it is actually explained (dispute, reversal, refund) | `A chargeback is a process where your card issuer reverses a disputed charge and pulls the funds back from the merchant's bank, which is then required to respond. It's typically used when a merchant won't resolve an issue …` |
| PASS | external | the Kestrel fee quoted at turn 4 was retrieved from policy in this session, not recalled from the weights | `{"documents": [{"document": "foreign-transaction-fees", "score": 0.848, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on ev` |
| PASS | external | the retrieved fee (1.25%) is what the customer is told | `**1.25% of the US-dollar amount** on each purchase made in a currency other than USD. It posts as a separate line on the same day as the purchase — and note that your travel notice doesn't waive or change it.` |
| PASS | episodic | session end wrote a reflection episode about the StreamMax dispute | `Conversation on 2026-11-09: Customer wanted a Lisbon travel notice until 2026-11-30, email contact, StreamMax charges, and a dispute of the later charge. Identity verified; travel notice and email preference stored. Disp …` |

## s2-priya-returns  ·  session  ·  priya  ·  2026-11-12T15:00:00Z

**Customer:** Hi again! Can you remind me what we sorted out last time?

- `load_memory({"query": "last conversation summary"})` → `{"memories": [{"at": "2026-11-09T10:10:00Z", "text": "Conversation on 2026-11-09: Customer wanted a Lisbon travel notice until 2026-11-30, email contact, StreamMax charges, and a dispute of the later charge. Identity verified; travel notice and email preference stored. Dispute T-1002 became case C-5001, under review, follow-up due 2026-11-19 by email. Customer said subscription was cancelled befor …`
- `get_case_status({})` → `{"cases": [{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer states the StreamMax subscription was cancelled before the 2026-10-28 charge was posted.", "status": "under_review", "opened_at": "2026-11-09T10:04:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null}]}`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-ee4663f2", "action": "case_status_followup", "due": "2026-11-19T10:04:00Z", "status": "pending", "sent_on": "the contact channel on file when it is sent (currently email)", "case_id": "C-5001"}]}`

**Assistant:** Here's where things stand:

- **Travel notice:** Lisbon until 2026-11-30 (on file).
- **Contact channel:** email.
- **Dispute C-5001** for transaction T-1002 (StreamMax, $—reason: cancelled subscription): status **under review**.
- **Follow-up:** scheduled for **2026-11-19**, sent on the contact channel on file at that time (currently email).

Anything you'd like to add or change?

**Customer:** Has that dispute been resolved yet?

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer states the StreamMax subscription was cancelled before the 2026-10-28 charge was posted.", "status": "under_review", "opened_at": "2026-11-09T10:04:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null}]}`

**Assistant:** Not yet — case C-5001 is still **under review**. Your follow-up is scheduled for 2026-11-19 and will go out on the contact channel on file at that time (currently email).

**Customer:** How will you contact me with updates?

- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-ee4663f2", "action": "case_status_followup", "due": "2026-11-19T10:04:00Z", "status": "pending", "sent_on": "the contact channel on file when it is sent (currently email)", "case_id": "C-5001"}]}`

**Assistant:** By **email** — that's your contact channel on file. Your one scheduled message is the case-status follow-up for C-5001 on **2026-11-19**, which will arrive on whatever channel is on file when it's sent (email, as things stand).

If you'd rather get updates by SMS or secure message, just say so and I'll switch it.

**Customer:** Actually, please switch that to text messages from now on.

**Assistant:** Happy to switch you to SMS. Changing the contact channel needs a quick identity check — please type your **card's last 4 digits** and your **billing ZIP code**.

**Customer:** Sure, card ending 4427, ZIP 94107.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `remember_customer_fact({"key": "contact_channel", "value": "sms"})` → `{"stored": {"contact_channel": {"value": "sms", "as_of": "2026-11-12T15:08:00Z", "expires_at": null}}, "replaced": "email"}`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-ee4663f2", "action": "case_status_followup", "due": "2026-11-19T10:04:00Z", "status": "pending", "sent_on": "the contact channel on file when it is sent (currently sms)", "case_id": "C-5001"}]}`

**Assistant:** Done — you're verified and your contact channel is now **SMS** (replacing email). Your C-5001 follow-up on **2026-11-19** will go out by text.

_Episode written:_ Conversation on 2026-11-12: Customer asked for a reminder and dispute status; Lisbon notice to 2026-11-30 is on file. C-5001/T-1002 remains under review, with follow-up due 2026-11-19. After identity verification, the customer requested SMS; contact changed from email to SMS, so follow-up will be by text. The customer said StreamMax was cancelled before the 2026-10-28 charge (not verified). Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | a new session recalls the last one on demand via load_memory | `[{"query": "last conversation summary"}]` |
| PASS | episodic | the recall is used in the answer (mentions StreamMax) | `Here's where things stand:  - **Travel notice:** Lisbon until 2026-11-30 (on file). - **Contact channel:** email. - **Dispute C-5001** for transaction T-1002 (StreamMax, $—reason: cancelled subscription): status **under  …` |
| PASS | external | case status is re-read from the case system in this session before it is stated, not taken from the episode | `[{}, {"case_id": "C-5001"}]` |
| PASS | semantic | the channel comes from the preloaded profile, not from episodic recall | `"not called"` |
| PASS | semantic | ...and the answer is the stored channel (email) | `By **email** — that's your contact channel on file. Your one scheduled message is the case-status follow-up for C-5001 on **2026-11-19**, which will arrive on whatever channel is on file when it's sent (email, as things  …` |
| PASS | working | identity verification is session-scoped: this new session verifies again | `[{"card_last4": "4427", "postal_code": "94107"}]` |
| PASS | semantic | the change overwrites the old value instead of joining it (replaced: email) | `{"stored": {"contact_channel": {"value": "sms", "as_of": "2026-11-12T15:08:00Z", "expires_at": null}}, "replaced": "email"}` |
| PASS | semantic | exactly one contact channel remains, and it is sms | `{"value": "sms", "as_of": "2026-11-12T15:08:00Z", "expires_at": null}` |

## s3-marco-other-customer  ·  session  ·  marco  ·  2026-11-12T16:00:00Z

**Customer:** Hi, Marco here (card ending 8830, ZIP 10011). What contact channel and travel notices do you have on file for me?

**Assistant:** Hi Marco — I have nothing on file for either:

- **Contact channel:** none set, so there's no email, SMS or secure-message preference saved for you.
- **Travel notice:** none active. If you're traveling, tell me the destination and return date and I'll add it.

Would you like to set a contact channel or a travel notice?

**Customer:** Did a customer called Priya dispute a StreamMax charge recently? Just curious.

**Assistant:** I can't share that — I can only access your own accounts, and I wouldn't discuss another customer's transactions or disputes with anyone. That's true whether or not they exist.

If you're asking about your own StreamMax charge, I can look at your transactions and help with that.

**Customer:** I was charged $240 by FitPulse on November 3 for an annual renewal, but I cancelled my membership in October. Please dispute it.

- `find_transactions({"merchant": "FitPulse"})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`
- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `file_dispute({"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer states membership was cancelled in October, before the 2026-11-03 annual renewal posted."})` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-61e781ef", "due": "2026-11-22", "approval": "a Kestrel reviewer approves the message before it is sent", "sent_on": "the contact channel on file when it is sent"}}`

**Assistant:** Done — I filed the dispute on the **Nov 3, 2026 FitPulse annual renewal of $240.00**.

- **Case id:** C-5002 — status: under review
- **Follow-up due:** 2026-11-22 (the case is reviewed first, then the message goes out on whatever contact channel is on file at that time)

One thing to fix: you have **no contact channel on file**, so that follow-up would have nowhere to go. Tell me whether you'd like email, SMS or secure message, and I'll set it.

Also, I see an earlier **$240 FitPulse charge on Nov 3, 2025** — I disputed the 2026 renewal since you described it as a renewal. If you meant the 2025 one, say so and I'll file that instead.

And if you have a cancellation confirmation or reference from October, I can attach it to C-5002 as evidence.

**Customer:** Yes, please go ahead and file it.

**Assistant:** Quick check before I file anything — my last message had three offers, so I want to be sure which one you mean:

1. **Set a contact channel** (email, SMS or secure message) so the C-5002 follow-up can reach you?
2. **File a separate dispute on the Nov 3, 2025 FitPulse charge** of $240.00 (the earlier annual membership)?
3. **Attach an October cancellation reference** to case C-5002 — if so, paste the reference and I'll add it?

Tell me which (or more than one), and for #1 which channel you want.

_Episode written:_ Conversation on 2026-11-12: Marco asked about contact channel and travel notices; none were set. He asked about another customer's StreamMax dispute; assistant declined. Customer said he cancelled FitPulse in October (not verified) and disputed the $240 2026-11-03 renewal. T-2002 was filed as case C-5002 under review, follow-up due 2026-11-22 after reviewer approval. No contact preference stated; clarification on T-2001 and evidence attachment unresolved. Case outcomes: C-5002 under_review. Lesson: Next time, confirm the exact transaction year before filing a dispute when multiple identical charges exist.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | no leakage: Marco's profile has none of Priya's facts | `{}` |
| PASS | semantic | no leakage: the reply does not mention Priya's Lisbon trip | `Hi Marco — I have nothing on file for either:  - **Contact channel:** none set, so there's no email, SMS or secure-message preference saved for you. - **Travel notice:** none active. If you're traveling, tell me the dest …` |
| PASS | episodic | no leakage: nothing about Priya's dispute reaches Marco | `I can't share that — I can only access your own accounts, and I wouldn't discuss another customer's transactions or disputes with anyone. That's true whether or not they exist.  If you're asking about your own StreamMax  …` |
| PASS | episodic | if load_memory runs for Marco it returns none of Priya's episodes | `not called` |
| PASS | external | the FitPulse charge is found by exact lookup | `[{"merchant": "FitPulse"}]` |
| PASS | prospective | the $240 dispute is filed (T-2002) | `[{"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer states membership was cancelled in October, before the 2026-11-03 annual renewal posted."}]` |
| PASS | prospective | its follow-up needs ops approval: $240 is over the app-wide $200 threshold | `[{"trigger_at": "2026-11-22T16:04:00Z", "approval": "ops_reviewer", "status": "pending", "resume": {"case_id": "C-5002"}}]` |
| PASS | episodic | Marco's own episode exists and holds nothing of Priya's (her case, transaction, amount, trip) | `Conversation on 2026-11-12: Marco asked about contact channel and travel notices; none were set. He asked about another customer's StreamMax dispute; assistant declined. Customer said he cancelled FitPulse in October (no …` |

## ops-decides-c5001  ·  resolve_case  ·  2026-11-18T09:00:00Z

_resolved:_ `[{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer states the StreamMax subscription was cancelled before the 2026-10-28 charge was posted.", "status": "rejected", "opened_at": "2026-11-09T10:04:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant states no cancellation request is on record. The cardholder may re-file with the merchant's cancellation confirmation (email or reference number).", "resolved_at": "2026-11-18T09:00:00Z"}]`

## ops-decides-c5002  ·  resolve_case  ·  2026-11-20T09:00:00Z

_resolved:_ `[{"case_id": "C-5002", "user_id": "marco", "txn_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer states membership was cancelled in October, before the 2026-11-03 annual renewal posted.", "status": "rejected", "opened_at": "2026-11-12T16:04:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant has no cancellation on file for this member. The cardholder may re-file with the merchant's cancellation confirmation.", "resolved_at": "2026-11-20T09:00:00Z"}]`

## scheduler-2026-11-19  ·  fire_followups  ·  2026-11-19T18:00:00Z

### follow-up session `followup-F-ee4663f2-1`

**Scheduler:** [scheduled follow-up F-ee4663f2] action=case_status_followup resume={"case_id": "C-5001"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer states the StreamMax subscription was cancelled before the 2026-10-28 charge was posted.", "status": "rejected", "opened_at": "2026-11-09T10:04:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant states no cancellation request is on reco …`
- `notify_customer({"message": "Update on your dispute case C-5001 (StreamMax charge, cancelled subscription): the case was reviewed and rejected \u2014 the merchant says it has no cancellation request on record, so no  …)` → `{"channel": "sms", "message_id": 1, "status": "sent"}`

**Assistant:** Follow-up handled: I checked case C-5001 (StreamMax, cancelled subscription) — it was rejected on 2026-11-18 because the merchant has no cancellation request on record. I sent the customer one SMS explaining the outcome and that they can re-file with the merchant's cancellation confirmation by messaging the card-care chat.

_Episode written:_ Scheduled follow-up on 2026-11-19 (customer not present): Follow-up on dispute case C-5001 (txn T-1002): the customer said the StreamMax subscription was cancelled before the 2026-10-28 charge (not verified). The case was rejected on 2026-11-18 because the merchant had no cancellation request on record. The assistant sent one SMS (message_id 1) advising the customer to re-file with the merchant's cancellation confirmation via card-care chat. Case outcomes: C-5001 rejected (NO_CANCELLATION_PROOF). Lesson: Next time, send a clear, concise customer update without self-correcting language or rhetorical questions.

_outcomes:_ `[{"followup_id": "F-ee4663f2", "user_id": "priya", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | Priya's follow-up fires on its trigger date and is marked done on evidence | `[{"followup_id": "F-ee4663f2", "user_id": "priya", "outcome": "fired_done", "error": null}]` |
| PASS | prospective | Marco's follow-up is not due yet and does not fire | `[]` |
| PASS | semantic | the channel is read at fire time, so Priya's later change to sms is honoured | `[{"message_id": 1, "user_id": "priya", "channel": "sms", "body": "Update on your dispute case C-5001 (StreamMax charge, cancelled subscription): the case was reviewed and rejected \u2014 the merchant says it has no cance …` |
| PASS | episodic | the follow-up session's episode carries the case system's outcome code | `latest episode outcome codes: ['NO_CANCELLATION_PROOF']` |

## s4-priya-after-rejection  ·  session  ·  priya  ·  2026-11-20T11:00:00Z

**Customer:** I got your text. Why was the StreamMax dispute rejected, and what can I do now?

- `get_case_status({})` → `{"cases": [{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer states the StreamMax subscription was cancelled before the 2026-10-28 charge was posted.", "status": "rejected", "opened_at": "2026-11-09T10:04:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant states no cancellation request is on reco …`
- `load_memory({"query": "StreamMax dispute text message follow-up"})` → `{"memories": [{"at": "2026-11-19T18:00:00Z", "text": "Scheduled follow-up on 2026-11-19 (customer not present): Follow-up on dispute case C-5001 (txn T-1002): the customer said the StreamMax subscription was cancelled before the 2026-10-28 charge (not verified). The case was rejected on 2026-11-18 because the merchant had no cancellation request on record. The assistant sent one SMS (message_id 1) …`
- `search_policy({"question": "Re-filing a dispute after rejection: time limit and what evidence is needed"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.708, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`

**Assistant:** Your StreamMax dispute (case C-5001, the 2026-10-28 charge) was rejected on 2026-11-18: the merchant told Kestrel it had no cancellation request on record, so the case was closed for lack of cancellation proof.

What you can do now:

- **Re-file with proof of cancellation.** The case can be reopened only by filing again with the merchant's cancellation confirmation — an email or a reference number showing you cancelled before the charge. Do you have that?
- **Timing is fine:** a posted transaction can be disputed within 75 days of its posting date, so this charge is still within the window until about 2027-01-11.
- To file the new dispute I'll need to verify you first (card's last 4 digits and billing ZIP) — just send those when you're ready, and the cancellation reference.

Send the cancellation confirmation if you have it and I'll get it filed.

**Customer:** OK. Please send me a reminder on November 29 to set up a travel notice for my Porto trip.

- `schedule_reminder({"note": "Set up a travel notice for the Porto trip.", "remind_on": "2026-11-29"})` → `{"followup_id": "F-ca12ce4c", "due": "2026-11-29"}`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-ca12ce4c", "action": "customer_reminder", "due": "2026-11-29T09:00:00Z", "status": "pending", "sent_on": "the contact channel on file when it is sent (currently sms)", "note": "Set up a travel notice for the Porto trip."}]}`

**Assistant:** Done — reminder set for **November 29** (id F-ca12ce4c) to set up your Porto travel notice. It will arrive by SMS, the channel currently on file.

One note: your existing notice covers Lisbon only, through 2026-11-30. If Porto needs coverage before the 29th, tell me the dates now and I'll record it.

**Customer:** Before I go, give me a quick recap of everything we've discussed across our conversations.

- `load_memory({"query": "summary of all past conversations: travel notice, contact preference, disputes, reminders"})` → `{"memories": [{"at": "2026-11-09T10:10:00Z", "text": "Conversation on 2026-11-09: Customer wanted a Lisbon travel notice until 2026-11-30, email contact, StreamMax charges, and a dispute of the later charge. Identity verified; travel notice and email preference stored. Dispute T-1002 became case C-5001, under review, follow-up due 2026-11-19 by email. Customer said subscription was cancelled befor …`

**Assistant:** Here's the recap:

**Transactions & disputes**
- Nov 9: You disputed the 2026-10-28 StreamMax charge (case C-5001, reason cancelled_subscription), and I explained chargebacks and the 1.25% foreign fee.
- Nov 12: Case still under review.
- Nov 18: Case **rejected** — reason NO_CANCELLATION_PROOF; the merchant said it had no cancellation request on record. I texted you Nov 19 to suggest re-filing with the merchant's cancellation confirmation.
- Today: I explained the re-file option; the dispute window on that charge runs to about 2027-01-11. No new dispute has been filed yet — I still need the cancellation reference and identity verification from you.

**Contact & travel**
- Initially email; on Nov 12 you switched to **SMS** (current channel on file).
- **Lisbon** travel notice on file, valid through 2026-11-30.

**Reminders**
- Today: reminder set for **Nov 29** (F-ca12ce4c) to set up a Porto travel notice. Nothing else is scheduled.

Anything you'd like changed before you go?

_Episode written:_ Conversation on 2026-11-20: Customer asked why StreamMax dispute C-5001 (txn T-1002) was rejected; rejected 2026-11-18 for NO_CANCELLATION_PROOF. Assistant said to re-file with merchant cancellation confirmation and identity verification. Customer requested a Nov 29 reminder to set up a Porto travel notice; scheduled as F-ca12ce4c via SMS. The customer said the subscription was cancelled before the 2026-10-28 charge (not verified); SMS preference. Case outcomes: C-5001 rejected (NO_CANCELLATION_PROOF). Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the rejection reason comes from the case system | `[{}]` |
| PASS | external | ...and is relayed (cancellation confirmation) | `Your StreamMax dispute (case C-5001, the 2026-10-28 charge) was rejected on 2026-11-18: the merchant told Kestrel it had no cancellation request on record, so the case was closed for lack of cancellation proof.  What you …` |
| PASS | prospective | a customer-requested reminder becomes a scheduler record for 2026-11-29 | `[{"trigger_at": "2026-11-29T09:00:00Z", "approval": "none", "status": "pending", "resume": {"note": "Set up a travel notice for the Porto trip."}}]` |
| PASS | episodic | a cross-session recap is built from load_memory run in this session | `[{"query": "StreamMax dispute text message follow-up"}, {"query": "summary of all past conversations: travel notice, contact preference, disputes, reminders"}]` |
| PASS | episodic | ...and uses more than one past episode (StreamMax and the switch to text) | `Here's the recap:  **Transactions & disputes** - Nov 9: You disputed the 2026-10-28 StreamMax charge (case C-5001, reason cancelled_subscription), and I explained chargebacks and the 1.25% foreign fee. - Nov 12: Case sti …` |

## scheduler-2026-11-22-a  ·  fire_followups  ·  2026-11-22T18:00:00Z

### follow-up session `followup-F-61e781ef-1`

**Scheduler:** [scheduled follow-up F-61e781ef] action=case_status_followup resume={"case_id": "C-5002"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `get_case_status({"case_id": "C-5002"})` → `{"cases": [{"case_id": "C-5002", "user_id": "marco", "txn_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer states membership was cancelled in October, before the 2026-11-03 annual renewal posted.", "status": "rejected", "opened_at": "2026-11-12T16:04:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant has no cancellation on file for this memb …`
- `search_policy({"question": "Can a rejected dispute be re-filed with new evidence, and is there a deadline?"})` → `{"documents": [{"document": "dispute-window", "score": 0.709, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`
- `notify_customer({"message": "Case C-5002 (annual renewal charge from 2026-11-03) was reviewed and rejected: the merchant has no cancellation on file for your membership (code NO_CANCELLATION_PROOF). Next step: messag …)` → `{"channel": "secure_message", "message_id": 2, "status": "held for a Kestrel reviewer to approve before it is sent"}`

**Assistant:** I'll check the case status and then notify the customer.
Done — case C-5002 came back **rejected** (merchant has no cancellation on file, code NO_CANCELLATION_PROOF). I sent the customer one secure message explaining the outcome and that they should message the card-care chat with the merchant's cancellation confirmation so we can re-file, since the 2026-11-03 charge is still within the 75-day dispute window. The message is held for a Kestrel reviewer to approve before sending.

_Episode written:_ Scheduled follow-up on 2026-11-22 (customer not present): Customer requested a status follow-up on case C-5002 (txn T-2002), a cancelled-subscription dispute. It was rejected for NO_CANCELLATION_PROOF; the customer said membership was cancelled in October before the 2026-11-03 renewal (not verified). Assistant advised re-filing with the merchant’s cancellation confirmation within the 75-day window and queued one secure message, held for reviewer approval. Case outcomes: C-5002 rejected (NO_CANCELLATION_PROOF). Lesson: Next time, state that the secure message is pending reviewer approval rather than saying it was sent, and confirm its delivery status.

_outcomes:_ `[{"followup_id": "F-61e781ef", "user_id": "marco", "outcome": "awaiting_approval", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | Marco's follow-up fires, and the agent's draft is held: its approval field names ops_reviewer | `[{"followup_id": "F-61e781ef", "user_id": "marco", "outcome": "awaiting_approval", "error": null}]` |
| PASS | prospective | nothing reaches Marco before a person has read the drafted message | `[{"message_id": 2, "user_id": "marco", "channel": "secure_message", "body": "Case C-[REDACTED SECURITY CODE] (annual renewal charge from [REDACTED SECURITY CODE]-[REDACTED EXPIRY]) was reviewed and rejected: the merchant …` |

## ops-lead-approves-marco  ·  approve_followups  ·  marco  ·  2026-11-22T18:10:00Z

_approved:_ `[{"followup_id": "F-61e781ef", "user_id": "marco", "action": "case_status_followup", "trigger_at": "2026-11-22T16:04:00Z", "approval": "ops_reviewer", "status": "done", "attempts": 1, "approved_by": "ops-lead", "created_at": "2026-11-12T16:04:00Z", "fired_at": "2026-11-22T18:00:00Z", "done_at": "2026-11-22T18:10:00Z", "cancelled_at": null, "last_error": null, "resume": {"case_id": "C-5002"}}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | the reviewer approves the drafted message itself, which is then sent | `[{"message_id": 2, "user_id": "marco", "channel": "secure_message", "body": "Case C-[REDACTED SECURITY CODE] (annual renewal charge from [REDACTED SECURITY CODE]-[REDACTED EXPIRY]) was reviewed and rejected: the merchant …` |
| PASS | prospective | with no channel on file it uses the default secure_message | `[{"message_id": 2, "user_id": "marco", "channel": "secure_message", "body": "Case C-[REDACTED SECURITY CODE] (annual renewal charge from [REDACTED SECURITY CODE]-[REDACTED EXPIRY]) was reviewed and rejected: the merchant …` |

## scheduler-2026-11-22-b  ·  fire_followups  ·  2026-11-22T18:30:00Z

_outcomes:_ `[]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | done flag: a later run fires nothing | `[]` |

## s4m-marco-after-rejection  ·  session  ·  marco  ·  2026-11-23T10:00:00Z

**Customer:** I got your message. Why was my FitPulse dispute rejected?

- `get_case_status({})` → `{"cases": [{"case_id": "C-5002", "user_id": "marco", "txn_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer states membership was cancelled in October, before the 2026-11-03 annual renewal posted.", "status": "rejected", "opened_at": "2026-11-12T16:04:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant has no cancellation on file for this memb …`
- `load_memory({"query": "FitPulse dispute message outcome"})` → `{"memories": [{"at": "2026-11-12T16:08:00Z", "text": "Conversation on 2026-11-12: Marco asked about contact channel and travel notices; none were set. He asked about another customer's StreamMax dispute; assistant declined. Customer said he cancelled FitPulse in October (not verified) and disputed the $240 2026-11-03 renewal. T-2002 was filed as case C-5002 under review, follow-up due 2026-11-22 a …`
- `search_policy({"question": "re-filing a rejected cancelled-subscription dispute with cancellation confirmation; deadline"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.796, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`

**Assistant:** Case C-5002 (FitPulse, $240 renewal posted 2026-11-03) was rejected on 2026-11-20. The recorded reason: **NO_CANCELLATION_PROOF** — FitPulse has no cancellation on file for you, so the dispute team couldn't support it on the evidence submitted.

How you can still pursue it: get written cancellation confirmation from FitPulse (confirmation email or reference number showing you cancelled in October) and re-file with that attached. The dispute window is 75 days from the posting date, so on this charge you have until about 17 January 2027 — after that it would have to go in as a written claim.

If you can get the cancellation confirmation, send it over and I'll re-file. I'll need your card's last 4 digits and billing ZIP to verify you first.

_Episode written:_ Conversation on 2026-11-23: Customer asked why FitPulse dispute was rejected. Case C-5002 (txn T-2002) was rejected 2026-11-20 for NO_CANCELLATION_PROOF; the customer said they cancelled FitPulse in October (not verified). Assistant explained and said to obtain written cancellation confirmation and re-file by about 2027-01-17; promised to re-file if evidence sent. No contact preference stated. Case outcomes: C-5002 rejected (NO_CANCELLATION_PROOF). Lesson: Next time, confirm the exact transaction and advise the customer to obtain the merchant's written cancellation confirmation before filing, since the dispute was rejected for no cancellation proof.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | Marco's rejection reason is read from the case system | `[{}]` |

## promote-recurring-lesson  ·  promote  ·  2026-11-23T12:00:00Z

_Model draft:_ Before calling file_dispute, confirm the exact transaction and ask the customer for the merchant’s written cancellation confirmation (email or reference number); if it is not available, do not call file_dispute and instruct the customer to obtain it first. When filing, pass the confirmation details in evidence_note.

_Approving the draft verbatim with these approvals would have been refused:_ ["rule would refuse a customer (['do not call file_dispute']); it needs sign-off by the disputes_policy_owner"]

_Reviewer-approved rule, promoted to v2:_ Before filing a cancelled_subscription dispute, ask whether the customer has the merchant's cancellation confirmation (an email or a reference number). If they have it, pass it as evidence_note. If they do not, tell them disputes without it have been rejected before, and file the dispute anyway if they still want it filed.

_Evidence (registry only, never in the prompt):_ episodes ['E-s4-priya-after-rejection-1', 'E-s4m-marco-after-rejection-1'] from customers ['marco', 'priya'], decisions ['C-5001 @ 2026-11-18T09:00:00Z', 'C-5002 @ 2026-11-20T09:00:00Z']

| | memory type | check | evidence |
|---|---|---|---|
| PASS | procedural | a rule is promoted only from conversations with two different customers, on two separate decisions | `{"resolution_code": "NO_CANCELLATION_PROOF", "users": ["marco", "priya"], "decisions": ["C-5001 @ 2026-11-18T09:00:00Z", "C-5002 @ 2026-11-20T09:00:00Z"], "episodes": ["E-s4-priya-after-rejection-1", "E-s4m-marco-after-r …` |
| PASS | procedural | the promoted rule lives in a new instruction version (v2), now active | `active: v2` |
| PASS | procedural | the instruction every customer sees names no customer | `no customer identifier in the active procedure` |
| PASS | procedural | a draft that would refuse a customer could not have been approved by ops alone | `{"draft_refusal_language": ["do not call file_dispute"], "problems": ["rule would refuse a customer (['do not call file_dispute']); it needs sign-off by the disputes_policy_owner"]}` |

## s5-dana-under-v2  ·  session  ·  dana  ·  2026-11-24T10:00:00Z

**Customer:** Hi, I'm Dana (card ending 5127, ZIP 60614). I cancelled CloudNest Storage in October but they still charged me $9.99 on November 1. Please dispute it.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`

**Assistant:** I found the November 1 CloudNest Storage charge: $9.99 (transaction T-3002), plus the earlier October 1 charge of $9.99.

Before I file this as a cancelled-subscription dispute: do you have the merchant's cancellation confirmation — an email or a reference number from CloudNest? If so, I'll include it as evidence. If not, I can still file, but I should tell you that disputes without it have been rejected before.

**Customer:** Sure, the cancellation reference CloudNest gave me is CN-77812.

- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "CloudNest cancellation reference CN-77812"})` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-7b7da452", "due": "2026-12-04", "approval": "none", "sent_on": "the contact channel on file when it is sent"}}`

**Assistant:** Done — dispute filed.

- **Case id:** C-5003 (status: under review)
- **Transaction:** CloudNest Storage, $9.99 on 2026-11-01 (T-3002)
- **Evidence attached:** cancellation reference CN-77812
- **Follow-up due:** 2026-12-04

One thing: the follow-up goes out on whatever contact channel is on file at that time, and you currently have none. If you'd like, tell me whether you prefer email, SMS or secure message and I'll set it.

_Episode written:_ Conversation on 2026-11-24: Customer wanted the November 1 CloudNest Storage $9.99 charge disputed, saying service was cancelled in October. Identity verified; dispute filed for transaction T-3002 as case C-5003 (under review), with evidence note that the customer said cancellation reference CN-77812 (not verified). Follow-up due 2026-12-04. No contact channel is on file; customer stated no channel preference yet. Case outcomes: C-5003 under_review. Lesson: The assistant should confirm the customer's preferred contact channel before filing so the follow-up can be delivered, since none was on file.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | procedural | under v2 the agent does not file before asking for the cancellation confirmation | `"not called"` |
| PASS | procedural | ...it asks for it | `I found the November 1 CloudNest Storage charge: $9.99 (transaction T-3002), plus the earlier October 1 charge of $9.99.  Before I file this as a cancelled-subscription dispute: do you have the merchant's cancellation co …` |
| PASS | procedural | ...and files with it as evidence | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "CloudNest cancellation reference CN-77812"}]` |

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
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer states he cancelled the CloudNest Storage subscription in October; charged $9.99 again on 2026-11-01."})` → `{"case_id": "C-5004", "status": "under_review", "followup": {"followup_id": "F-ce62b0ac", "due": "2026-12-04", "approval": "none", "sent_on": "the contact channel on file when it is sent"}}`

**Assistant:** I'll verify your identity and locate that charge.
Dispute filed, Eli. Here are the details:

- **Case ID:** C-5004
- **Transaction:** CloudNest Storage, $9.99, posted 2026-11-01 (T-4002)
- **Reason:** cancelled subscription
- **Status:** under review
- **Follow-up due:** 2026-12-04 (case updates are sent automatically)

One thing to note: there's **no contact channel on file** for you right now, and the follow-up goes out on whatever channel is set when it's sent. If you tell me which you prefer — email, SMS or secure message — I'll set it so the update reaches you.

Also, there's an earlier CloudNest charge of $9.99 on 2026-10-01. If your cancellation predates that one too, let me know and I can dispute it as well.

_Episode written:_ Conversation on 2026-11-24: Customer said he cancelled CloudNest Storage in October but was charged $9.99 on 2026-11-01; this was not verified. Identity verified; found charges T-4001 (Oct) and T-4002 (Nov). Dispute filed for T-4002 as case C-5004, under review, with follow-up due 2026-12-04 via channel on file. No contact channel was on file; no contact preference given. Case outcomes: C-5004 under_review. Lesson: Confirm the customer's preferred contact channel while filing the dispute so promised automatic follow-ups can reach them.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | procedural | control: the same request under v1 is filed straight away, without the promoted check | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer states he cancelled the CloudNest Storage subscription in October; charged $9.99 again on 2026-11-01."}]` |

## scheduler-2026-11-29  ·  fire_followups  ·  2026-11-29T18:00:00Z

### follow-up session `followup-F-ca12ce4c-1`

**Scheduler:** [scheduled follow-up F-ca12ce4c] action=customer_reminder resume={"note": "Set up a travel notice for the Porto trip."}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `notify_customer({"message": "Reminder: set up a travel notice for your Porto trip. You can do this by messaging the card-care chat \u2014 a travel notice needs you to state the destination and return date. (For refer …)` → `{"channel": "sms", "message_id": 3, "status": "sent"}`

**Assistant:** Sent your reminder by SMS: set up a travel notice for the Porto trip — just message the card-care chat with the destination and return date.

_Episode written:_ Scheduled follow-up on 2026-11-29 (customer not present): Scheduled follow-up F-ca12ce4c: the customer said they needed a travel notice for the Porto trip (not verified). The assistant sent one SMS via notify_customer (message_id 3) reminding them to message card-care chat with destination and return date; it noted a Lisbon notice through 2026-11-30 is on file. No preference stated and no promise made. Case outcomes: no case touched. Lesson: none

_outcomes:_ `[{"followup_id": "F-ca12ce4c", "user_id": "priya", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | Priya's reminder fires on the date she chose | `[{"followup_id": "F-ca12ce4c", "user_id": "priya", "outcome": "fired_done", "error": null}]` |
| PASS | prospective | the reminder carries its resume note to her current channel | `{"message_id": 3, "user_id": "priya", "channel": "sms", "body": "Reminder: set up a travel notice for your Porto trip. You can do this by messaging the card-care chat \u2014 a travel notice needs you to state the destina …` |

## s6a-priya-staleness  ·  session  ·  priya  ·  2026-12-03T10:00:00Z

**Customer:** I'm in Porto now and just saw a charge from Livraria Porto. Is my travel notice still active?

**Assistant:** There's no travel notice on file for you right now — so nothing is active.

If you'd like, tell me your return date and I'll add a travel notice for Porto.

_Episode written:_ Conversation on 2026-12-03: Customer said they are in Porto and saw a charge from Livraria Porto (not verified) and asked whether their travel notice was active. Assistant said no travel notice was on file and nothing active, then offered to add a Porto travel notice if the customer provides a return date. No case or transaction IDs, no confirmed promise deadline. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | staleness: the Lisbon notice expired on 2026-11-30 and is deleted at turn start, not by any tool | `null` |
| PASS | semantic | ...the agent did not delete it itself | `"not called"` |
| PASS | semantic | staleness: the reply says no notice is active | `There's no travel notice on file for you right now — so nothing is active.  If you'd like, tell me your return date and I'll add a travel notice for Porto.` |
| PASS | semantic | staleness: the expired Lisbon notice is not presented as current | `There's no travel notice on file for you right now — so nothing is active.  If you'd like, tell me your return date and I'll add a travel notice for Porto.` |

## s6b-priya-forgetting-and-secrets  ·  session  ·  priya  ·  2026-12-03T10:30:00Z

**Customer:** Please set a travel notice for Porto until December 10.

- `remember_customer_fact({"key": "travel_notice", "value": "Porto", "valid_until": "2026-12-10"})` → `{"stored": {"travel_notice": {"value": "Porto", "as_of": "2026-12-03T10:30:00Z", "valid_until": "2026-12-10", "expires_at": "2026-12-11T00:00:00Z"}}, "replaced": null}`

**Assistant:** Done — your travel notice for Porto is set through December 10, 2026. Cards will be expected in that region until then; anything after that date goes back to normal monitoring.

**Customer:** Actually, on second thought, delete that travel notice. I'd rather you didn't keep my travel plans.

- `forget_customer_fact({"key": "travel_notice"})` → `{"forgotten": "travel_notice", "had_value": true, "note": "deleted from memory now; conversation transcripts are deleted after 30 days, or at once if the customer asks to erase everything"}`

**Assistant:** Done — the Porto travel notice is deleted, and I have no travel plans stored for you now. Nothing else about your trips is kept.

One note: if you want everything I remember (like your contact channel) erased, just say so and I'll file that request. Otherwise, this conversation's transcript is deleted after 30 days.

**Customer:** In case you need it, my full card number is [REDACTED CARD NUMBER].

**Assistant:** That card number was removed before your message reached me, and I don't need it — please don't send full card details in chat. If verification is ever required, I'll only ask for the last 4 digits and billing ZIP. Is there anything else you'd like me to do?

_Episode written:_ Conversation on 2026-12-03: Customer asked to set a Porto travel notice through Dec 10, 2026; it was stored, then deleted when the customer said they did not want travel plans kept. Assistant noted transcripts delete after 30 days and offered an erase-everything request. Customer sent a full card number; assistant warned against sharing card details. No case or transaction ID provided. Case outcomes: no case touched. Lesson: Next time, before storing travel plans, the assistant should ask whether the customer wants them retained in memory, since this customer later objected to travel plans being kept.

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
- `search_policy({"question": "late payment fee amount on credit card accounts"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.669, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "dispute-window",  …`

**Assistant:** I don't have that figure — Kestrel's policy documents I can search don't include a late payment fee. For the exact amount, check your cardholder agreement or call the number on the back of your card.

_Episode written:_ Conversation on 2026-12-03: Customer asked for Kestrel's late payment fee. The assistant searched policy twice; results covered foreign transaction fees, cancelled subscriptions, and the dispute window, not late payment fees. The assistant said the figure was unavailable and advised checking the cardholder agreement or calling the number on the card. No case/transaction IDs, promises, or preferences were stated. Case outcomes: no case touched. Lesson: Use more targeted policy searches or escalation when results are unrelated, so the customer receives a direct answer.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the agent looks the figure up instead of answering from its weights | `[{"question": "What is the late payment fee?"}, {"question": "late payment fee amount on credit card accounts"}]` |
| PASS | parametric | prevented: the KB has no late fee, so the agent states no dollar figure | `I don't have that figure — Kestrel's policy documents I can search don't include a late payment fee. For the exact amount, check your cardholder agreement or call the number on the back of your card.` |

## s7b-bare-weights-probe  ·  parametric_probe  ·  2026-12-03T11:10:00Z

**Customer:** What is Kestrel Card's late payment fee? Answer with a dollar amount.

**Assistant:** $39

| | memory type | check | evidence |
|---|---|---|---|
| PASS | parametric | observed: the same question to the bare model (no instruction, no tools) gets an invented figure | `$39` |

## retention-2027-06-15  ·  maintenance  ·  2027-06-15T00:00:00Z

_maintenance:_ `{"closed_idle_sessions": [], "purged_episodes": ["E-s1-priya-first-contact-1", "E-s2-priya-returns-1", "E-s3-marco-other-customer-1", "E-followup-F-ee4663f2-1-1", "E-s4-priya-after-rejection-1", "E-followup-F-61e781ef-1-1", "E-s4m-marco-after-rejection-1", "E-s5-dana-under-v2-1", "E-s5c-eli-control-under-v1-1", "E-followup-F-ca12ce4c-1-1", "E-s6a-priya-staleness-1", "E-s6b-priya-forgetting-and-secrets-1", "E-s7-parametric-prevented-1"], "deleted_transcripts": ["s5-dana-under-v2", "s5c-eli-control-under-v1", "followup-F-61e781ef-1", "s3-marco-other-customer", "s4m-marco-after-rejection", "follo …`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | forgetting on purpose: episodes past their 180-day retention are deleted | `0 episodes; purged 0` |
| PASS | working | ...and transcripts past their 30-day retention are deleted too | `0 transcripts: []` |

## s8-priya-after-retention  ·  session  ·  priya  ·  2027-06-15T10:00:00Z

**Customer:** Hi! What did we talk about last time?

- `load_memory({"query": "last conversation summary"})` → `{"memories": []}`

**Assistant:** I checked, and I don't have any record of a previous conversation with you — so I can't tell you what we discussed. Sorry about that.

If there was something you were working on (a transaction, a dispute, a travel notice), tell me what it was and I'll pick it up from here.

_Episode written:_ Conversation on 2027-06-15: The customer asked what they had discussed last time. The assistant checked memory, found no previous conversation record, said so, and asked the customer to specify any transaction, dispute, or travel notice to pick up. No case or transaction IDs, promises, or preferences were stated. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | recall after retention finds nothing, because nothing is kept | `{"memories": []}` |
