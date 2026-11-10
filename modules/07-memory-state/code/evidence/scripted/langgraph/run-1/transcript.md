# langgraph · scripted · run 1

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## s1-priya-first-contact  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Hi, it's Priya (card ending 4427, billing ZIP 94107). I'm in Lisbon until November 30, so you'll see euro charges. Also, please contact me by email from now on, not text.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `remember_customer_fact({"key": "travel_notice", "value": "Lisbon", "valid_until": "2026-11-30"})` → `{"stored": {"travel_notice": {"value": "Lisbon", "as_of": "2026-11-09T10:00:00Z", "valid_until": "2026-11-30", "expires_at": "2026-12-01T00:00:00Z"}}, "replaced": null}`
- `search_policy({"question": "travel notice"})` → `{"documents": [{"document": "travel-notices", "score": 0.76, "text": "# Travel notices\n\nA travel notice tells Kestrel's fraud systems that card use in another country is expected, which reduces false declines while you travel. Give the destination and the date you return. Kestrel keeps a travel notice only until the return date and deletes it automatically afterwards; a new trip needs a new noti …`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70100", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `null`

**Assistant:** A one-time code has been sent by text message to ···0100; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "customer_wrote": "[REDACTED ONE-TIME CODE]", "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-09T10:02:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** All set, Priya.

- **Travel notice:** Lisbon until November 30, 2026 is recorded, so euro charges in Portugal shouldn't trip fraud alerts. Kestrel deletes it automatically after your return date; a later trip needs a new notice.
- **Contact channel:** changed to **email**. To do that I verified your identity, then sent a one-time code by text message to the mobile number ending **0100** - that's the only place the bank can send it - and it checked out.

Anything else - a charge you'd like to look at, or a reminder?

**Customer:** Can you show me my StreamMax charges?

- `find_transactions({"merchant": "StreamMax"})` → `{"transactions": [{"transaction_id": "T-1001", "posted_on": "2026-09-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-1002", "posted_on": "2026-10-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription …`

**Assistant:** Here are your StreamMax charges:

| Date | Description | Amount |
|---|---|---|
| 2026-09-28 | StreamMax Premium monthly | $15.99 |
| 2026-10-28 | StreamMax Premium monthly | $15.99 |

Both are the same monthly subscription, $15.99 each. Is there something you'd like to do about them - for example, dispute one?

**Customer:** Please dispute the later one. I'd cancelled the subscription before it was charged.

- `file_dispute({"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the StreamMax subscription before the 2026-10-28 charge."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-ddaf94cb", "due": "2026-11-19", "approval": "none", "sent_on": "email; if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Dispute filed.

- **Case:** C-5001, status under review (for the $15.99 StreamMax charge on 2026-10-28)
- **Follow-up:** due 2026-11-19, and it will reach you by **email** - if you change your contact channel before then, it goes to the new one
- Disputes are currently reviewed in about 10 days.

If you have your cancellation confirmation from StreamMax (a reference number or email), send it along and I'll attach it to the case.

**Customer:** Quick one: what is a chargeback, in two sentences?

**Assistant:** A chargeback is when your card issuer reverses a charge and pulls the money back from the merchant's bank, usually after you dispute it and the issuer reviews the evidence from both sides. It differs from a refund, which the merchant issues voluntarily, though a merchant may also choose to refund once a chargeback is filed.

**Customer:** What foreign transaction fee will I pay on my Lisbon purchases?

- `search_policy({"question": "foreign transaction fee"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.858, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "travel-notices",  …`

**Assistant:** **1.25% of the US-dollar amount** on each purchase made in a currency other than USD (so your euro purchases in Lisbon). It posts as a separate line on the same day as the purchase, and your travel notice doesn't change or waive it.

_Episode written:_ Conversation on 2026-11-09: Priya requested a Lisbon travel notice through 2026-11-30, email contact, and dispute of later StreamMax charge T-1002. Assistant recorded travel notice and email preference, filed dispute C-5001 under review with follow-up due 2026-11-19 by email; customer said she cancelled subscription before charge (not verified). Case outcomes: C-5001 under_review. Lesson: Record the email preference and explain before step-up that one-time verification codes may still arrive by text, so the customer is not surprised.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | travel notice written as a user-scoped fact (Lisbon, valid until 2026-11-30) | `{"value": "Lisbon", "as_of": "2026-11-09T10:00:00Z", "valid_until": "2026-11-30", "expires_at": "2026-12-01T00:00:00Z"}` |
| PASS | semantic | contact channel written as a user-scoped fact (email) | `{"value": "email", "as_of": "2026-11-09T10:02:00Z", "expires_at": null}` |
| PASS | external | transactions come from an exact ledger lookup | `[{"merchant": "StreamMax"}]` |
| PASS | working | session scope: identity_verified_at persists with this session's state | `persisted session keys: ['__pregel_tasks', 'episodes_written', 'first_active_at', 'identity_verified_at', 'last_active_at', 'messages', 'possession_verified_at', 'reflected_turns', 'turn_times']` |
| PASS | working | temp scope: the per-invocation clock (ADK temp:now, LangGraph TurnContext.now) is never persisted | `clock keys found in persisted state: none` |
| PASS | working | 'the later one' resolved from the previous turn's tool result in the session: disputes T-1002 | `[{"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the StreamMax subscription before the 2026-10-28 charge."}]` |
| PASS | prospective | filing wrote a scheduler record: case follow-up due 2026-11-19, no approval needed | `[{"trigger_at": "2026-11-19T10:06:00Z", "approval": "none", "status": "pending", "resume": {"case_id": "C-5001"}}]` |
| PASS | parametric | a general concept is answered from the weights, with no tool call | `tools: []` |
| PASS | parametric | ...and it is actually explained (dispute, reversal, refund) | `A chargeback is when your card issuer reverses a charge and pulls the money back from the merchant's bank, usually after you dispute it and the issuer reviews the evidence from both sides. It differs from a refund, which …` |
| PASS | external | the Kestrel fee quoted at turn 5 was retrieved from policy in this session, not recalled from the weights | `{"documents": [{"document": "travel-notices", "score": 0.76, "text": "# Travel notices\n\nA travel notice tells Kestrel's fraud systems that card use in another country is expected, which reduces fals; {"documents": [{"d …` |
| PASS | external | the retrieved fee (1.25%) is what the customer is told | `**1.25% of the US-dollar amount** on each purchase made in a currency other than USD (so your euro purchases in Lisbon). It posts as a separate line on the same day as the purchase, and your travel notice doesn't change  …` |
| PASS | episodic | session end wrote a reflection episode about the StreamMax dispute | `Conversation on 2026-11-09: Priya requested a Lisbon travel notice through 2026-11-30, email contact, and dispute of later StreamMax charge T-1002. Assistant recorded travel notice and email preference, filed dispute C-5 …` |

## s2-priya-returns  ·  session  ·  priya  ·  2026-11-12T15:00:00Z

**Customer:** Hi again! Can you remind me what we sorted out last time?

- `load_memory({"query": "last conversation summary what we sorted out"})` → `{"memories": [{"at": "2026-11-09T10:12:00Z", "text": "Conversation on 2026-11-09: Priya requested a Lisbon travel notice through 2026-11-30, email contact, and dispute of later StreamMax charge T-1002. Assistant recorded travel notice and email preference, filed dispute C-5001 under review with follow-up due 2026-11-19 by email; customer said she cancelled subscription before charge (not verified) …`
- `get_case_status({})` → `{"cases": [{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the StreamMax subscription before the 2026-10-28 charge.", "status": "under_review", "opened_at": "2026-11-09T10:06:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null, "decision_id": null}]}`

**Assistant:** Here's what we covered on 9 November:

- **Travel notice:** Lisbon until 30 November 2026 - still on your profile.
- **Contact channel:** email - still your preference.
- **Dispute:** you disputed the StreamMax charge (T-1002, 28 Oct) as a cancelled subscription, saying you'd cancelled before the charge. That's case **C-5001** - currently **under review** (checked just now).
- **Follow-up:** due 19 November, arriving by email.
- One thing I flagged: one-time verification codes can still go to the mobile number the bank holds, even though email is your contact channel.

Anything you'd like to change or follow up on?

**Customer:** Has that dispute been resolved yet?

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the StreamMax subscription before the 2026-10-28 charge.", "status": "under_review", "opened_at": "2026-11-09T10:06:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null, "decision_id": null}]}`

**Assistant:** Not yet - case C-5001 (StreamMax, T-1002) is still **under review**. Your status update is due 19 November by email. Disputes are currently reviewed in about 10 days, so a decision should be close.

**Customer:** How will you contact me with updates?

**Assistant:** By **email** - that's the contact channel on your profile. Case C-5001's follow-up is also set to reach you by email, due 19 November.

**Customer:** Actually, please switch that to text messages from now on.

**Assistant:** To switch your contact channel to text messages, I first need to verify you. Please send your card's last 4 digits and your billing ZIP code.

Also note: the one-time code I'll then send goes to the mobile number or email the bank holds on your account, and it can't be sent anywhere else.

**Customer:** Sure, card ending 4427, ZIP 94107.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70100", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `null`

**Assistant:** A one-time code has been sent by text message to ···0100; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "customer_wrote": "[REDACTED ONE-TIME CODE]", "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "sms"})` → `{"stored": {"contact_channel": {"value": "sms", "as_of": "2026-11-12T15:10:00Z", "expires_at": null}}, "replaced": "email"}`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-ddaf94cb", "action": "case_status_followup", "due": "2026-11-19T10:06:00Z", "status": "pending", "sent_on": "text message (SMS): the contact channel on file when it is sent", "case_id": "C-5001"}]}`

**Assistant:** Done - your contact channel is now **text message (SMS)**, replacing email, and verified with the one-time code.

Your pending update for case C-5001 is due 19 November and will arrive by text message too, since that's the channel on file when it's sent.

_Episode written:_ Conversation on 2026-11-12: Customer asked for a recap and whether dispute C-5001 (StreamMax, T-1002) was resolved, then requested SMS contact instead of email. Assistant confirmed C-5001/T-1002 remains under review, follow-up F-ddaf94cb due 19 November, verified identity, and switched contact channel to SMS; the update will arrive by SMS. Lisbon travel notice active. The customer said she cancelled StreamMax before the 2026-10-28 charge (not verified). Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | a new session recalls the last one on demand via load_memory | `[{"query": "last conversation summary what we sorted out"}]` |
| PASS | episodic | the recall is used in the answer (mentions StreamMax) | `Here's what we covered on 9 November:  - **Travel notice:** Lisbon until 30 November 2026 - still on your profile. - **Contact channel:** email - still your preference. - **Dispute:** you disputed the StreamMax charge (T …` |
| PASS | external | case status is re-read from the case system in this session before it is stated, not taken from the episode | `[{}, {"case_id": "C-5001"}]` |
| PASS | semantic | the channel comes from the preloaded profile, not from episodic recall | `"not called"` |
| PASS | semantic | ...and the answer is the stored channel (email) | `By **email** - that's the contact channel on your profile. Case C-5001's follow-up is also set to reach you by email, due 19 November.` |
| PASS | working | identity verification is session-scoped: this new session verifies again | `[{"card_last4": "4427", "postal_code": "94107"}]` |
| PASS | working | a channel change needs the one-time code as well: it is sent and confirmed | `[{}, {}]` |
| PASS | semantic | the change overwrites the old value instead of joining it (replaced: email) | `{"stored": {"contact_channel": {"value": "sms", "as_of": "2026-11-12T15:10:00Z", "expires_at": null}}, "replaced": "email"}` |
| PASS | semantic | exactly one contact channel remains, and it is sms | `{"value": "sms", "as_of": "2026-11-12T15:10:00Z", "expires_at": null}` |

## s3-marco-other-customer  ·  session  ·  marco  ·  2026-11-12T16:00:00Z

**Customer:** Hi, Marco here (card ending 8830, ZIP 10011). What contact channel and travel notices do you have on file for me?

**Assistant:** Hi Marco - here's what's on file:

- **Contact channel:** none set, so follow-ups and reminders go by secure message in the Kestrel app (the default).
- **Travel notice:** none on file.

Want to add an email or SMS channel, or set up a travel notice for an upcoming trip?

**Customer:** Did a customer called Priya dispute a StreamMax charge recently? Just curious.

**Assistant:** I can't share anything about another customer's account or disputes - I can only discuss your own transactions and cases. If you're wondering about one of your own charges, I'm happy to look that up.

**Customer:** I was charged $240 by FitPulse on November 3 for an annual renewal, but I cancelled my membership in October. Please dispute it.

- `find_transactions({"merchant": "FitPulse"})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`
- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `file_dispute({"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled their FitPulse membership in October, before the annual renewal posted on November 3, 20 …)` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-4b78ea73", "due": "2026-11-22", "approval": "a Kestrel reviewer approves the message before it is sent", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Done - I filed the dispute for the FitPulse annual renewal:

- **Transaction:** FitPulse Gym, $240.00, posted 2026-11-03 (T-2002)
- **Reason:** cancelled subscription - you cancelled in October, before the renewal
- **Case ID:** C-5002 (status: under review)
- **Follow-up:** due 2026-11-22, sent by secure message in the Kestrel app (the default, since no contact channel is set - if you set one before then, it will go there instead)

Note there's also an earlier FitPulse charge of $240 from 2025-11-03, in case that one matters too. If you have a cancellation confirmation or reference from FitPulse, I can attach it to the case.

**Customer:** Yes, please go ahead and file it.

- `search_policy({"question": "time limit to dispute a charge"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.744, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`

**Assistant:** Just to be clear on what's already done and what I can't do:

- **The November 3, 2026 charge ($240) is already filed** - that's case C-5002, under review, follow-up due 2026-11-22 by secure message in the Kestrel app. Nothing more needed there.
- **The November 3, 2025 charge ($240) I can't file through the assistant.** Two reasons:
  - It's outside the dispute window: posted transactions can be disputed within 75 days of the posting date, and that one is over a year old, so it would have to go as a written claim.
  - It was charged before you cancelled in October, and earlier charges made before cancellation can't be disputed on the cancelled-subscription ground.

If you think the 2025 charge is wrong for a different reason, tell me and I'll see what's possible; otherwise, for that older charge you'd need to submit a written claim to Kestrel.

_Episode written:_ Conversation on 2026-11-12: Marco asked what contact channel and travel notices were on file; none were set, so secure-message default. He asked about another customer's dispute, which the assistant declined to discuss. He disputed a $240 FitPulse renewal posted 2026-11-03 (T-2002), saying he cancelled in October (not verified); dispute C-5002 filed under review, follow-up due 2026-11-22 by secure message. Case outcomes: C-5002 under_review. Lesson: When multiple similar transactions exist and the customer gives an ambiguous approval, confirm which specific charge or action they mean before proceeding.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | no leakage: Marco's profile has none of Priya's facts | `{}` |
| PASS | semantic | no leakage: the reply does not mention Priya's Lisbon trip | `Hi Marco - here's what's on file:  - **Contact channel:** none set, so follow-ups and reminders go by secure message in the Kestrel app (the default). - **Travel notice:** none on file.  Want to add an email or SMS chann …` |
| PASS | episodic | no leakage: nothing about Priya's dispute reaches Marco | `I can't share anything about another customer's account or disputes - I can only discuss your own transactions and cases. If you're wondering about one of your own charges, I'm happy to look that up.` |
| PASS | episodic | if load_memory runs for Marco it returns none of Priya's episodes | `not called` |
| PASS | external | the FitPulse charge is found by exact lookup | `[{"merchant": "FitPulse"}]` |
| PASS | prospective | the $240 dispute is filed (T-2002) | `[{"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled their FitPulse membership in October, before the annual renewal posted on November 3, 2026."}]` |
| PASS | prospective | its follow-up needs ops approval: $240 is over the app-wide $200 threshold | `[{"trigger_at": "2026-11-22T16:04:00Z", "approval": "ops_reviewer", "status": "pending", "resume": {"case_id": "C-5002"}}]` |
| PASS | episodic | Marco's own episode exists and holds nothing of Priya's (her case, transaction, amount, trip) | `Conversation on 2026-11-12: Marco asked what contact channel and travel notices were on file; none were set, so secure-message default. He asked about another customer's dispute, which the assistant declined to discuss.  …` |

## ops-decides-c5001  ·  resolve_case  ·  2026-11-18T09:00:00Z

_resolved:_ `[{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the StreamMax subscription before the 2026-10-28 charge.", "status": "rejected", "opened_at": "2026-11-09T10:06:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant states no cancellation request is on record. The cardholder may re-file with the merchant's cancellation confirmation (email or reference number).", "resolved_at": "2026-11-18T09:00:00Z", "decision_id": "D-ops-decides-c5001"}]`

## ops-decides-c5002  ·  resolve_case  ·  2026-11-20T09:00:00Z

_resolved:_ `[{"case_id": "C-5002", "user_id": "marco", "txn_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled their FitPulse membership in October, before the annual renewal posted on November 3, 2026.", "status": "rejected", "opened_at": "2026-11-12T16:04:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant has no cancellation on file for this member. The cardholder may re-file with the merchant's cancellation confirmation.", "resolved_at": "2026-11-20T09:00:00Z", "decision_id": "D-ops-decides-c5002"}]`

## scheduler-2026-11-19  ·  fire_followups  ·  2026-11-19T18:00:00Z

### follow-up session `followup-F-ddaf94cb-1`

**Scheduler:** [scheduled follow-up F-ddaf94cb] action=case_status_followup resume={"case_id": "C-5001"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the StreamMax subscription before the 2026-10-28 charge.", "status": "rejected", "opened_at": "2026-11-09T10:06:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant states no cancellation request is on record. The cardh …`
- `notify_customer({"message": "Update on case C-5001 (StreamMax charge of 2026-10-28): the dispute was rejected and the case is now closed, because the merchant says no cancellation request is on record. Nothing can be …)` → `{"channel": "sms", "message_id": 3, "status": "sent"}`

**Assistant:** Case C-5001 was rejected and is closed (reason: no cancellation proof). I've sent the customer an SMS explaining the outcome and that with the merchant's cancellation confirmation she can open a new dispute of the same charge via the card-care chat.

_Episode written:_ Scheduled follow-up on 2026-11-19 (customer not present): Customer wanted an update on case C-5001 about a StreamMax charge (txn T-1002, 2026-10-28). The customer said she canceled before the charge (not verified). The case was rejected and closed for no cancellation proof; an SMS (message_id 3) was sent explaining this and advising a new dispute via card-care chat with the merchant’s cancellation confirmation. No preference or promise stated. Case outcomes: C-5001 rejected (NO_CANCELLATION_PROOF). Lesson: none

_outcomes:_ `[{"followup_id": "F-ddaf94cb", "user_id": "priya", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | Priya's follow-up fires on its trigger date and is marked done on evidence | `[{"followup_id": "F-ddaf94cb", "user_id": "priya", "outcome": "fired_done", "error": null}]` |
| PASS | prospective | Marco's follow-up is not due yet and does not fire | `[]` |
| PASS | semantic | the channel is read at fire time, so Priya's later change to sms is honoured | `[{"message_id": 3, "user_id": "priya", "channel": "sms", "body": "Update on case C-5001 (StreamMax charge of 2026-10-28): the dispute was rejected and the case is now closed, because the merchant says no cancellation req …` |
| PASS | episodic | the follow-up session's episode carries the case system's outcome code | `latest episode outcome codes: ['NO_CANCELLATION_PROOF']` |

## s4-priya-after-rejection  ·  session  ·  priya  ·  2026-11-20T11:00:00Z

**Customer:** I got your text. Why was the StreamMax dispute rejected, and what can I do now?

- `get_case_status({})` → `{"cases": [{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the StreamMax subscription before the 2026-10-28 charge.", "status": "rejected", "opened_at": "2026-11-09T10:06:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant states no cancellation request is on record. The cardh …`
- `search_policy({"question": "dispute rejected what can I do next"})` → `{"documents": [{"document": "dispute-window", "score": 0.679, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** Here's what the case record shows for the StreamMax charge:

- **Case C-5001** (transaction T-1002, reason: cancelled subscription) - **rejected** on 2026-11-18.
- **Why:** resolution code **NO_CANCELLATION_PROOF** - the merchant states no cancellation request is on record for the subscription.
- **Status:** the case is decided and closed, so nothing more can be attached to it.

What you can do now: if you have the merchant's cancellation confirmation - an email or a reference number from when you cancelled - I can file a **new dispute on the same charge** with that proof. That's the route the record points to; without proof of cancellation, a re-file would likely meet the same answer.

If you'd like me to file it, send me the cancellation reference (or tell me you have the email), and I'll need your card's last 4 digits and billing ZIP to verify you first - the case can only be filed within 75 days of the charge posting, and this one is still inside that window. The new follow-up would reach you by text, as your contact channel is set to SMS.

**Customer:** OK. Please send me a reminder on November 29 to set up a travel notice for my Porto trip.

- `schedule_reminder({"note": "Set up a travel notice for my Porto trip", "remind_on": "2026-11-29"})` → `{"followup_id": "F-879ffe4e", "due_utc": "2026-11-29T09:00:00Z", "local_time": "Sunday 2026-11-29 09:00 UTC (UTC)", "sent_on": "text message (SMS), the contact channel on file when it is sent"}`

**Assistant:** Done - reminder set for **Sunday 29 November at 09:00 UTC** ("Set up a travel notice for my Porto trip"), arriving by **text message (SMS)** to your number on file.

One thing to note: your profile currently has a travel notice for **Lisbon until 30 November**. If you want the Porto trip recorded now rather than waiting for the reminder, just tell me the dates and I'll record it.

**Customer:** Before I go, give me a quick recap of everything we've discussed across our conversations.

- `load_memory({"query": "StreamMax dispute, travel notice, contact channel, past conversations summary"})` → `{"memories": [{"at": "2026-11-12T15:12:00Z", "text": "Conversation on 2026-11-12: Customer asked for a recap and whether dispute C-5001 (StreamMax, T-1002) was resolved, then requested SMS contact instead of email. Assistant confirmed C-5001/T-1002 remains under review, follow-up F-ddaf94cb due 19 November, verified identity, and switched contact channel to SMS; the update will arrive by SMS. Lisb …`

**Assistant:** Here's the recap, combining what's on record from your earlier conversations and this one:

**StreamMax charge (C-5001, txn T-1002, posted 2026-10-28)**
- 9 Nov: you asked me to dispute it as a cancelled subscription; case filed and put under review, with a follow-up due 19 Nov. You also set email contact and a Lisbon travel notice through 30 Nov.
- 12 Nov: you switched your contact channel to SMS (identity verified in that conversation), and the case was still under review at that point.
- 19 Nov: the scheduled follow-up went out by SMS - the case had been **rejected** (no cancellation proof: the merchant says no cancellation request is on record) and closed.
- Today: you asked why, and I explained it was rejected for lack of cancellation proof and that a decided case can't take more evidence. The route now is a **new dispute of the same charge** if you can supply the merchant's cancellation confirmation (email or reference number). You haven't filed it yet.

**Travel**
- Lisbon travel notice is active until 30 Nov.
- Today we set a reminder for **Sunday 29 November, 09:00 UTC, by SMS** to set up a travel notice for your Porto trip.

**Contact channel:** SMS, as it stands now.

We haven't recorded anything about the Porto trip's dates yet, and no new StreamMax dispute has been filed - just say the word if you want either done.

_Episode written:_ Conversation on 2026-11-20: Customer asked why StreamMax dispute C-5001 (txn T-1002) was rejected and next steps. Assistant explained NO_CANCELLATION_PROOF and that a new dispute could be filed with merchant cancellation confirmation; none filed. Customer said she cancelled before the 2026-10-28 charge (not verified). Assistant scheduled reminder F-879ffe4e for 2026-11-29 09:00 UTC by SMS for Porto travel notice; SMS preference. Case outcomes: C-5001 rejected (NO_CANCELLATION_PROOF). Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the rejection reason comes from the case system | `[{}]` |
| PASS | external | ...and is relayed (cancellation confirmation) | `Here's what the case record shows for the StreamMax charge:  - **Case C-5001** (transaction T-1002, reason: cancelled subscription) - **rejected** on 2026-11-18. - **Why:** resolution code **NO_CANCELLATION_PROOF** - the …` |
| PASS | prospective | a customer-requested reminder becomes a scheduler record for 2026-11-29 | `[{"trigger_at": "2026-11-29T09:00:00Z", "approval": "none", "status": "pending", "resume": {"note": "Set up a travel notice for my Porto trip"}}]` |
| PASS | episodic | a cross-session recap is built from load_memory run in this session | `[{"query": "StreamMax dispute, travel notice, contact channel, past conversations summary"}]` |
| PASS | episodic | ...and uses more than one past episode (StreamMax and the switch to text) | `Here's the recap, combining what's on record from your earlier conversations and this one:  **StreamMax charge (C-5001, txn T-1002, posted 2026-10-28)** - 9 Nov: you asked me to dispute it as a cancelled subscription; ca …` |

## scheduler-2026-11-22-a  ·  fire_followups  ·  2026-11-22T18:00:00Z

### follow-up session `followup-F-4b78ea73-1`

**Scheduler:** [scheduled follow-up F-4b78ea73] action=case_status_followup resume={"case_id": "C-5002"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `get_case_status({"case_id": "C-5002"})` → `{"cases": [{"case_id": "C-5002", "user_id": "marco", "txn_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled their FitPulse membership in October, before the annual renewal posted on November 3, 2026.", "status": "rejected", "opened_at": "2026-11-12T16:04:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant has no cancellatio …`
- `notify_customer({"message": "Your dispute C-5002 (FitPulse annual renewal, Nov 3, 2026) was decided and closed on Nov 20: it was rejected because the merchant has no cancellation on record for your membership. Nothin …)` → `{"channel": "secure_message", "message_id": 4, "status": "held for a Kestrel reviewer to approve before it is sent"}`

**Assistant:** I'll check the case status for C-5002, then notify the customer.
Case C-5002 was decided and rejected - the merchant has no cancellation on record for the FitPulse membership. A secure message with the outcome and next step (re-file the same charge with FitPulse's cancellation confirmation via the card-care chat) has been sent to the customer; it is currently held for Kestrel reviewer approval before delivery.

_Episode written:_ Scheduled follow-up on 2026-11-22 (customer not present): Scheduled follow-up for case C-5002 (txn T-2002): checked status. The FitPulse renewal dispute was rejected and closed Nov 20 for no cancellation proof; the customer said they cancelled in October before the Nov 3, 2026 renewal (not verified). A secure-message notice advised re-filing with FitPulse cancellation confirmation via Kestrel card-care chat; it is held for reviewer approval. Case outcomes: C-5002 rejected (NO_CANCELLATION_PROOF). Lesson: Next time, report a secure message as pending reviewer approval until delivery is confirmed, rather than saying it was sent.

_outcomes:_ `[{"followup_id": "F-4b78ea73", "user_id": "marco", "outcome": "awaiting_approval", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | Marco's follow-up fires, and the agent's draft is held: its approval field names ops_reviewer | `[{"followup_id": "F-4b78ea73", "user_id": "marco", "outcome": "awaiting_approval", "error": null}]` |
| PASS | prospective | nothing reaches Marco before a person has read the drafted message | `[{"message_id": 4, "user_id": "marco", "channel": "secure_message", "body": "Your dispute C-5002 (FitPulse annual renewal, Nov 3, 2026) was decided and closed on Nov 20: it was rejected because the merchant has no cancel …` |

## ops-lead-approves-marco  ·  approve_followups  ·  marco  ·  2026-11-22T18:10:00Z

_approved:_ `[{"followup_id": "F-4b78ea73", "user_id": "marco", "action": "case_status_followup", "trigger_at": "2026-11-22T16:04:00Z", "approval": "ops_reviewer", "status": "done", "attempts": 1, "approved_by": "ops-lead", "created_at": "2026-11-12T16:04:00Z", "fired_at": "2026-11-22T18:00:00Z", "done_at": "2026-11-22T18:10:00Z", "cancelled_at": null, "last_error": null, "generation": 0, "local_day": null, "not_before": null, "resume": {"case_id": "C-5002"}}]`

_rejected:_ `[]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | the reviewer approves the drafted message itself, which is then sent | `[{"message_id": 4, "user_id": "marco", "channel": "secure_message", "body": "Your dispute C-5002 (FitPulse annual renewal, Nov 3, 2026) was decided and closed on Nov 20: it was rejected because the merchant has no cancel …` |
| PASS | prospective | with no channel on file it uses the default secure_message | `[{"message_id": 4, "user_id": "marco", "channel": "secure_message", "body": "Your dispute C-5002 (FitPulse annual renewal, Nov 3, 2026) was decided and closed on Nov 20: it was rejected because the merchant has no cancel …` |
| PASS | guard | no outbound message or episode so far carries a masking token or a masked identifier | `10 outbound messages and episodes clean` |

## scheduler-2026-11-22-b  ·  fire_followups  ·  2026-11-22T18:30:00Z

_outcomes:_ `[]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | done flag: a later run fires nothing | `[]` |

## s4m-marco-after-rejection  ·  session  ·  marco  ·  2026-11-23T10:00:00Z

**Customer:** I got your message. Why was my FitPulse dispute rejected?

- `get_case_status({})` → `{"cases": [{"case_id": "C-5002", "user_id": "marco", "txn_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled their FitPulse membership in October, before the annual renewal posted on November 3, 2026.", "status": "rejected", "opened_at": "2026-11-12T16:04:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant has no cancellatio …`
- `find_transactions({"merchant": "FitPulse"})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`

**Assistant:** Your FitPulse dispute (case C-5002, the $240.00 renewal posted November 3, 2026) was rejected on November 20. The reason given: the merchant has no cancellation on file for your membership, so the case closed with "no cancellation proof."

That case is decided and closed, so nothing more can be added to it. If you have the merchant's cancellation confirmation (or a cancellation reference), you can start a new dispute of the same charge from this chat - just send it over. Do you have that proof?

_Episode written:_ Conversation on 2026-11-23: Customer asked why their FitPulse dispute was rejected. Assistant explained case C-5002/transaction T-2002 ($240 renewal posted 2026-11-03) was rejected on 2026-11-20 because the merchant had no cancellation on file. The case record notes the customer said they cancelled in October (not verified). Assistant said a new dispute can be started with the merchant’s cancellation confirmation/reference. No customer preference stated. Case outcomes: C-5002 rejected (NO_CANCELLATION_PROOF). Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | Marco's rejection reason is read from the case system | `[{}]` |

## promote-recurring-lesson  ·  promote  ·  2026-11-23T12:00:00Z

_Model draft:_ Before calling file_dispute for a cancellation-related dispute, ask the cardholder for the merchant’s cancellation confirmation (email or reference number) and pass that confirmation as evidence_note; if the cardholder cannot provide it, do not call file_dispute and advise them to obtain it before re-filing.

_Routing probe (ops-only approval):_ REFUSED: Before calling file_dispute for a cancellation-related dispute, ask th; REFUSED: File a cancelled_subscription dispute only after the customer provides; REFUSED: Require the merchant's cancellation confirmation before calling file_d; REFUSED: Decline to file a cancelled_subscription dispute until the customer su; REFUSED: Refuse cancelled_subscription disputes that lack a cancellation confir; REFUSED: Hold off on filing a cancelled_subscription dispute until a cancellati; REFUSED: A cancelled_subscription dispute must include the merchant's cancellat; REFUSED: Without a cancellation confirmation, a cancelled_subscription dispute ; REFUSED: Ask whether the customer has the merchant's cancellation confirmation,

_Reviewer-approved rule, promoted to v2:_ Before filing a cancelled_subscription dispute, ask whether the customer has the merchant's cancellation confirmation (an email or a reference number). If they have it, pass it as evidence_note. If they do not, tell them disputes without it have been rejected before, and file the dispute anyway if they still want it filed.

_Evidence (registry only, never in the prompt):_ episodes ['E-s4-priya-after-rejection-1-51d3b3', 'E-s4m-marco-after-rejection-1-86467d'] from customers ['marco', 'priya'], decisions ['D-ops-decides-c5001', 'D-ops-decides-c5002']

| | memory type | check | evidence |
|---|---|---|---|
| PASS | procedural | a rule is promoted only from conversations with two different customers, on two separate decisions | `{"resolution_code": "NO_CANCELLATION_PROOF", "users": ["marco", "priya"], "decisions": ["D-ops-decides-c5001", "D-ops-decides-c5002"], "episodes": ["E-s4-priya-after-rejection-1-51d3b3", "E-s4m-marco-after-rejection-1-86 …` |
| PASS | procedural | the promoted rule lives in a new instruction version (v2), now active | `active: v2` |
| PASS | procedural | the instruction every customer sees names no customer | `no customer identifier in the active procedure` |
| PASS | procedural | routing by source: no rule text, the model's draft or any paraphrased refusal, ships on ops approval alone | `all 9 refused` |

## s5-dana-under-v2  ·  session  ·  dana  ·  2026-11-24T10:00:00Z

**Customer:** Hi, I'm Dana (card ending 5127, ZIP 60614). I cancelled CloudNest Storage in October but they still charged me $9.99 on November 1. Please dispute it.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`

**Assistant:** I found it: the $9.99 CloudNest Storage charge posted on 2026-11-01 (transaction T-3002).

Since this is a cancelled-subscription dispute, one question before I file: do you have the merchant's cancellation confirmation - an email or a reference number from CloudNest? If so, I'll attach it as evidence. If not, I can still file, but I should tell you that disputes without cancellation proof have been rejected before. Let me know and I'll proceed either way.

**Customer:** Sure, the cancellation reference CloudNest gave me is CN-77812.

- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "CloudNest cancellation reference CN-77812 (subscription cancelled in October, still charged on November 1)."})` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-664048db", "due": "2026-12-04", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Filed. Here are the details:

- **Case id:** C-5003 (status: under review)
- **Charge:** $9.99, CloudNest Storage, posted 2026-11-01
- **Evidence attached:** cancellation reference CN-77812
- **Follow-up due:** 2026-12-04, sent by secure message in the Kestrel app (the default, since no contact channel is set on your account)

You don't need to do anything else for now. If you find more evidence before the case is decided, send it here and I can attach it.

_Episode written:_ Conversation on 2026-11-24: The customer wanted a $9.99 CloudNest Storage charge posted 2026-11-01 disputed. The customer said the subscription was cancelled in October and gave cancellation reference CN-77812 (not verified). Dispute filed on transaction T-3002 as case C-5003, status under review. Follow-up due 2026-12-04 by secure message in the Kestrel app; customer should send further evidence if found. Case outcomes: C-5003 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | procedural | under v2 the agent does not file before asking for the cancellation confirmation | `"not called"` |
| PASS | procedural | ...it asks for it | `I found it: the $9.99 CloudNest Storage charge posted on 2026-11-01 (transaction T-3002).  Since this is a cancelled-subscription dispute, one question before I file: do you have the merchant's cancellation confirmation  …` |
| PASS | procedural | ...and files with it as evidence | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "CloudNest cancellation reference CN-77812 (subscription cancelled in October, still charged on November 1)."}]` |

## retraction-drill  ·  retract  ·  2026-11-24T12:00:00Z

_affected:_ `[{"user_id": "dana", "episode_id": "E-s5-dana-under-v2-1-d60e7d", "at": "2026-11-24T10:04:00Z", "outcomes": [{"case_id": "C-5003", "txn_id": "T-3002", "reason": "cancelled_subscription", "status": "under_review", "resolution_code": null, "resolution_note": null, "resolved_at": null, "decision_id": null}]}]`

_Registry history:_ `[{"event": "baseline", "version": "v1"}, {"event": "promoted", "version": "v2", "based_on": "v1", "by": ["ops-lead (scripted reviewer)", "disputes-policy-owner (scripted reviewer)"], "at": "2026-11-23T12:00:00Z"}, {"event": "retracted", "version": "v2", "active_now": "v1", "by": "ops-lead (scripted reviewer)", "roles": ["ops_lead"], "reason": "retraction drill: prove a promoted rule can be removed", "at": "2026-11-24T12:00:00Z"}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | procedural | the retraction path restores v1 | `active: v1` |
| PASS | procedural | the retraction lists the conversations held under v2, for review (Dana's) | `[["dana", "E-s5-dana-under-v2-1-d60e7d"]]` |

## s5c-eli-control-under-v1  ·  session  ·  eli  ·  2026-11-24T13:00:00Z

**Customer:** Hi, I'm Eli (card ending 6610, ZIP 73301). I cancelled CloudNest Storage in October but they still charged me $9.99 on November 1. Please dispute it.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled CloudNest Storage in October, but was still charged $9.99 on November 1."})` → `{"case_id": "C-5004", "status": "under_review", "followup": {"followup_id": "F-8101a9d7", "due": "2026-12-04", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Verified you, Eli - thanks. I found the November 1 charge and filed the dispute.

- **Case:** C-5004 (CloudNest Storage, $9.99 on 2026-11-01, cancelled subscription)
- **Status:** under review
- **Follow-up:** due 2026-12-04, sent as a secure message in the Kestrel app (no contact channel is set, so that's the default)

Disputes are currently reviewed in about 10 days. If you have anything like a cancellation confirmation or reference number from CloudNest, send it along and I'll attach it to the case.

_Episode written:_ Conversation on 2026-11-24: The customer said they cancelled CloudNest Storage in October (not verified) and asked to dispute a $9.99 charge posted 2026-11-01. The assistant verified identity, found transaction T-4002, and filed dispute C-5004 (under review). Follow-up F-8101a9d7 is due 2026-12-04 via Kestrel app secure message; review takes about 10 days and cancellation proof can be attached if provided. Case outcomes: C-5004 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | procedural | control: the same request under v1 is filed straight away, without the promoted check | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled CloudNest Storage in October, but was still charged $9.99 on November 1."}]` |

## scheduler-2026-11-29  ·  fire_followups  ·  2026-11-29T18:00:00Z

### follow-up session `followup-F-879ffe4e-1`

**Scheduler:** [scheduled follow-up F-879ffe4e] action=customer_reminder resume={"note": "Set up a travel notice for my Porto trip"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `search_policy({"question": "how to set up a travel notice"})` → `{"documents": [{"document": "travel-notices", "score": 0.742, "text": "# Travel notices\n\nA travel notice tells Kestrel's fraud systems that card use in another country is expected, which reduces false declines while you travel. Give the destination and the date you return. Kestrel keeps a travel notice only until the return date and deletes it automatically afterwards; a new trip needs a new not …`
- `notify_customer({"message": "Reminder: you wanted to set up a travel notice for your Porto trip. A travel notice needs the destination and your return date, and it is deleted automatically after that date, so a new t …)` → `{"channel": "sms", "message_id": 5, "status": "sent"}`

**Assistant:** Sent the reminder by SMS: the note to set up a travel notice for the Porto trip, plus the next step of messaging the card-care chat in the Kestrel app to add it (destination and return date).

_Episode written:_ Scheduled follow-up on 2026-11-29 (customer not present): For follow-up F-879ffe4e, the customer said they wanted a travel notice for a Porto trip (not verified). The assistant searched policy and sent an SMS reminder, message_id 5, explaining a notice needs destination and return date, expires after return, and can be added via card-care chat. No travel notice was confirmed created. Case outcomes: no case touched. Lesson: Next time, for a travel-notice reminder without a return date, clearly state that no notice was created and give the customer the exact next step to add it.

_outcomes:_ `[{"followup_id": "F-879ffe4e", "user_id": "priya", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | Priya's reminder fires on the date she chose | `[{"followup_id": "F-879ffe4e", "user_id": "priya", "outcome": "fired_done", "error": null}]` |
| PASS | prospective | the reminder carries its resume note to her current channel | `{"message_id": 5, "user_id": "priya", "channel": "sms", "body": "Reminder: you wanted to set up a travel notice for your Porto trip. A travel notice needs the destination and your return date, and it is deleted automatic …` |

## s6a-priya-staleness  ·  session  ·  priya  ·  2026-12-03T10:00:00Z

**Customer:** I'm in Porto now and just saw a charge from Livraria Porto. Is my travel notice still active?

- `load_memory({"query": "travel notice Porto"})` → `{"memories": [{"at": "2026-11-29T18:00:00Z", "text": "Scheduled follow-up on 2026-11-29 (customer not present): For follow-up F-879ffe4e, the customer said they wanted a travel notice for a Porto trip (not verified). The assistant searched policy and sent an SMS reminder, message_id 5, explaining a notice needs destination and return date, expires after return, and can be added via card-care chat. …`
- `find_transactions({"merchant": "Livraria Porto"})` → `{"transactions": [{"transaction_id": "T-1005", "posted_on": "2026-12-01", "merchant": "Livraria Porto", "description": "Bookshop, Porto", "amount": "\u20ac22.00", "currency": "EUR", "category": "retail"}]}`

**Assistant:** No - there's no travel notice on your account right now. It looks like the Porto notice requested back in late November never got created (it needed a destination and return date to be set up), and nothing is on file now.

I can add it now: just tell me the destination (Porto is fine) and the date you return, and I'll record it.

One note on the charge you mentioned: the €22.00 Livraria Porto charge (posted 2026-12-01) is on your account. If you want to dispute it, say the word.

_Episode written:_ Conversation on 2026-12-03: The customer said they were in Porto now (not verified) and asked if their travel notice was active after seeing a Livraria Porto charge. Memory for follow-up F-879ffe4e showed no travel notice confirmed created; transaction T-1005, €22.00 posted 2026-12-01, was found. Assistant said no notice is active, offered to add one if given return date, and offered a dispute. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | staleness: the Lisbon notice expired on 2026-11-30 and is deleted at turn start, not by any tool | `null` |
| PASS | semantic | ...the agent did not delete it itself | `"not called"` |
| PASS | semantic | staleness: the reply says no notice is active | `No - there's no travel notice on your account right now. It looks like the Porto notice requested back in late November never got created (it needed a destination and return date to be set up), and nothing is on file now …` |
| PASS | semantic | staleness: the expired Lisbon notice is not presented as current | `No - there's no travel notice on your account right now. It looks like the Porto notice requested back in late November never got created (it needed a destination and return date to be set up), and nothing is on file now …` |

## s6b-priya-forgetting-and-secrets  ·  session  ·  priya  ·  2026-12-03T10:30:00Z

**Customer:** Please set a travel notice for Porto until December 10.

- `remember_customer_fact({"key": "travel_notice", "value": "Porto", "valid_until": "2026-12-10"})` → `{"stored": {"travel_notice": {"value": "Porto", "as_of": "2026-12-03T10:30:00Z", "valid_until": "2026-12-10", "expires_at": "2026-12-11T00:00:00Z"}}, "replaced": null}`

**Assistant:** Your travel notice for Porto is set, covering through December 10, 2026 (it runs until 00:00 UTC on December 11). Anything else I can help with?

**Customer:** Actually, on second thought, delete that travel notice. I'd rather you didn't keep my travel plans.

- `forget_customer_fact({"key": "travel_notice"})` → `{"forgotten": "travel_notice", "had_value": true, "note": "deleted from memory now; conversation transcripts are deleted 30 days after their first message, or at once if the customer asks to erase everything"}`

**Assistant:** Done - the travel notice is deleted. You now have none on file.

**Customer:** In case you need it, my full card number is [REDACTED CARD NUMBER].

**Assistant:** That card number was removed before it reached me or any record, and it isn't needed - please don't send full card details. If you ever need a dispute or a contact-channel change, I only need your card's last 4 digits and billing ZIP.

_Episode written:_ Conversation on 2026-12-03: Customer asked to set a Porto travel notice through Dec 10, 2026, then asked to delete it, preferring travel plans not be kept. The notice was stored then deleted; no case or transaction IDs appeared and no promises were made. The customer said they had a full card number (not verified); the assistant said it was removed. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | a new fact can be written | `[{"key": "travel_notice", "value": "Porto", "valid_until": "2026-12-10"}]` |
| PASS | semantic | deletion on request: forget_customer_fact runs | `[{"key": "travel_notice"}]` |
| PASS | semantic | ...and the fact is gone from the store | `null` |
| PASS | guard | a pasted card number is masked before it enters the session | `In case you need it, my full card number is [REDACTED CARD NUMBER].` |
| PASS | guard | the card number is in no store: sessions, memory, bank, scheduler | `found in: nowhere` |

## s7-parametric-prevented  ·  session  ·  priya  ·  2026-12-03T11:00:00Z

**Customer:** What is Kestrel's late payment fee?

- `search_policy({"question": "late payment fee"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.664, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "cancelled-subscri …`

**Assistant:** I don't have a Kestrel figure for a late payment fee - that isn't in the policy documents I can access. You may want to check your cardholder agreement or call Kestrel directly to confirm it.

_Episode written:_ Conversation on 2026-12-03: The customer wanted Kestrel's late payment fee. A policy search returned no relevant Kestrel fee document, so the assistant said it had no accessible figure and advised checking the cardholder agreement or calling Kestrel. No case or transaction IDs, promises, or preferences were stated. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the agent looks the figure up instead of answering from its weights | `[{"question": "late payment fee"}]` |
| PASS | parametric | prevented: the KB has no late fee, so the agent states no dollar figure | `I don't have a Kestrel figure for a late payment fee - that isn't in the policy documents I can access. You may want to check your cardholder agreement or call Kestrel directly to confirm it.` |

## s7b-bare-weights-probe  ·  parametric_probe  ·  2026-12-03T11:10:00Z

**Customer:** What is Kestrel Card's late payment fee? Answer with a dollar amount.

**Assistant:** $0

| | memory type | check | evidence |
|---|---|---|---|
| PASS | parametric | observed: the same question to the bare model (no instruction, no tools) gets an invented figure | `$0` |

## retention-2027-06-15  ·  maintenance  ·  2027-06-15T00:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "case_followups_repaired": [], "purged_episodes": ["E-s1-priya-first-contact-1-c88d64", "E-s2-priya-returns-1-8fc91d", "E-s3-marco-other-customer-1-1b5726", "E-followup-F-ddaf94cb-1-1-56bbcc", "E-s4-priya-after-rejection-1-51d3b3", "E-followup-F-4b78ea73-1-1-5d3e1e", "E-s4m-marco-after-rejection-1-86467d", "E-s5-dana-under-v2-1-d60e7d", "E-s5c-eli-control-under-v1-1-2140a5", "E-followup-F-879ffe4e-1-1-5a6722", "E-s6a-priya-staleness-1-37a4f8", "E-s6b-priya-forgetting-and-secrets-1-b2eba5", "E-s7-parametric-prevented-1-62 …`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | forgetting on purpose: episodes past their 180-day retention are deleted | `0 episodes; purged 0` |
| PASS | working | ...and transcripts past their 30-day retention are deleted too | `0 transcripts: []` |

## s8-priya-after-retention  ·  session  ·  priya  ·  2027-06-15T10:00:00Z

**Customer:** Hi! What did we talk about last time?

- `load_memory({"query": "last conversation topics"})` → `{"memories": []}`

**Assistant:** I have no record of an earlier conversation with you, so I can't say what we talked about.

What I can see right now: your contact channel is set to SMS, and you have no travel notice on file. Happy to help with anything - transactions, a dispute, travel notices or reminders.

_Episode written:_ Conversation on 2027-06-15: The customer asked what they discussed last time. The assistant ran a memory lookup, which returned no records, then said there was no prior conversation record. No case or transaction IDs, promises, or preferences were stated. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | recall after retention finds nothing, because nothing is kept | `{"memories": []}` |
