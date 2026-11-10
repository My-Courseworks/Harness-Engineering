# adk · heldout-r4 · run 1 · r4-erase-open-tab-case-followup

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r4e1-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, Dana here, card ending 5127, ZIP 60614. CloudNest Storage charged me $9.99 on November 1 even though I cancelled in October, please dispute it. Also, I'm in Reykjavik until November 28, so expect charges in krona.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `remember_customer_fact({"key": "travel_notice", "value": "Reykjavik", "valid_until": "2026-11-28"})` → `{"stored": {"travel_notice": {"value": "Reykjavik", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-11-28", "expires_at": "2026-11-29T00:00:00Z"}}, "replaced": null}`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest Storage subscription in October; the $9.99 charge on November 1, 2026 is a …)` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-3ea1c18c", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Done on both counts, Dana:

**Dispute filed - case C-5001**
- Charge: CloudNest Storage, $9.99, posted 2026-11-01 (the second of your two CloudNest charges; the 2026-10-01 one is separate and not included)
- Reason: cancelled subscription
- Status: under review
- Follow-up due 2026-11-23, sent by secure message in the Kestrel app - that's the default because no contact channel is set. If you set a channel before then, the follow-up goes there instead.

**Travel notice saved:** Reykjavik, valid until 2026-11-28. Charges in krona during that window will be expected.

Anything else you'd like me to add to the case, e.g. a cancellation reference from CloudNest?

**Customer:** Yes, go ahead and file it.

**Assistant:** Your dispute is already on file - case C-5001, under review, follow-up due 2026-11-23 by secure message in the Kestrel app. There's nothing further to file for it.

What I can do is attach extra evidence if you have it. Do you have a cancellation reference or confirmation from CloudNest (e.g. a reference number or the date they confirmed the cancellation)? Send me the details and I'll attach them to C-5001.

_Episode written:_ Conversation on 2026-11-13: Dana asked to dispute a $9.99 CloudNest Storage charge posted 2026-11-01, saying she cancelled in October (not verified), and gave a Reykjavik travel notice until 2026-11-28. Dispute C-5001 was filed for T-3002, under review; follow-up due 2026-11-23 via Kestrel secure message, or changed channel. Assistant asked for a cancellation reference. Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | r4: the dispute is filed on T-3002 | `[{"case_id": "C-5001", "status": "under_review"}]` |
| PASS | prospective | r4: its follow-up is due 2026-11-23, no approval | `[{"trigger_at": "2026-11-23T10:00:00Z", "approval": "none", "status": "pending", "resume": {"case_id": "C-5001"}}]` |
| PASS | semantic | r4: the travel notice is stored until 2026-11-28 | `{"value": "Reykjavik", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-11-28", "expires_at": "2026-11-29T00:00:00Z"}` |

## r4e1-s2  ·  session  ·  dana  ·  2026-11-23T09:55:00Z

**Customer:** I've changed my mind about all of this. Erase everything you remember about me and every conversation we've had.

- `request_memory_erasure({})` → `{"erased_now": "1 remembered facts, 1 past-conversation summaries, 1 other conversation transcripts, 0 reminders with their notes", "this_conversation": "its transcript is deleted when the conversation ends, or once it has been idle for 30 minutes if the customer just closes the chat; nothing more can be stored for the customer in it (a new conversation afterwards starts fresh)", "kept": "dispute  …`

**Assistant:** Done - I've erased what was stored:

- **Deleted now:** the 1 fact I had saved about you, 1 past-conversation summary, 1 other conversation's transcript, and 0 reminders.
- **This conversation:** its transcript is deleted when the conversation ends, or once it's been idle for 30 minutes if you just close the chat. Nothing more can be stored for you in this conversation - so I can't set a reminder or save a preference here; that would need a new conversation.
- **Kept:** dispute cases, transactions and messages already sent are bank records with their own legal retention.

## r4e1-fire-1  ·  fire_followups  ·  2026-11-23T10:06:00Z

### follow-up session `followup-F-3ea1c18c-1`

**Scheduler:** [scheduled follow-up F-3ea1c18c] action=case_status_followup resume={"case_id": "C-5001"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest Storage subscription in October; the $9.99 charge on November 1, 2026 is after the cancellation.", "status": "under_review", "opened_at": "2026-11-13T10:00:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null …`
- `notify_customer({"message": "Dispute C-5001 (CloudNest Storage, $9.99 on Nov 1, 2026) is still under review \u2014 no decision yet, and nothing is needed from you right now. If you have more evidence for the case, me …)` → `{"channel": "secure_message", "message_id": 1, "status": "sent"}`

**Assistant:** I'll check the case status, then notify the customer.
Sent the follow-up: case C-5001 remains under review with no decision yet, delivered by secure message in the Kestrel app (no contact channel is set).

_outcomes:_ `[{"followup_id": "F-3ea1c18c", "user_id": "dana", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | r4: an erasure pending at fire time still runs: no fact remains | `{}` |
| PASS | episodic | r4: no episode remains, and the fired follow-up wrote none | `0 episodes; purged 0` |
| PASS | working | r4: no transcript remains: not the open tab, not the follow-up's own session | `0 transcripts: []` |
| PASS | working | r4: the follow-up session is unattended even though an erasure ran around it | `["find_transactions", "get_case_status", "list_my_followups", "load_memory", "notify_customer", "report_malformed_tool_call", "search_policy"]` |
| PASS | guard | r4: nothing she said is in any memory store | `found nowhere` |

## r4e1-fire-2  ·  fire_followups  ·  2026-11-23T10:20:00Z

_outcomes:_ `[]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r4: the case follow-up still reaches the erased customer, exactly once | `1 messages` |
| PASS | guard | r4: no outbound message carries a masking token or a masked identifier | `1 outbound messages and episodes clean` |
| PASS | episodic | r4: still no episode after the retry window | `0 episodes; purged 0` |
| PASS | working | r4: still no transcript after the retry window | `0 transcripts: []` |

## r4e1-s3  ·  session  ·  dana  ·  2026-11-30T10:00:00Z

**Customer:** Hello again. What do you have on file about me, and do you remember where I said I'd be travelling?

- `load_memory({"query": "travel notice destination where I will be travelling"})` → `{"result": "memories=[]"}`

**Assistant:** I'll check what's on file and what I have from earlier conversations.
Here's what's on file for you right now:

- **Contact channel:** none set - so follow-ups and reminders reach you by secure message in the Kestrel app (the default).
- **Travel notice:** none on file.
- **No saved memories** from earlier conversations - I checked, and I have no record of you telling me where you'd be travelling.

If you'd like, tell me the destination (and the date you return) and I'll add a travel notice.

_Episode written:_ Conversation on 2026-11-30: The customer asked what was on file and where they had said they would travel; they said they had previously stated a destination (not verified). The assistant checked memory, found none, confirmed no travel notice and no contact channel (default secure message in Kestrel app), and offered to add a travel notice if given destination and return date. No IDs. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | r4: nothing erased comes back in a later chat | `I'll check what's on file and what I have from earlier conversations. Here's what's on file for you right now:  - **Contact channel:** none set - so follow-ups and reminders reach you by secure message in the Kestrel app …` |
| PASS | episodic | r4: recall, if used, returns nothing erased | `{"result": "memories=[]"}` |
| PASS | semantic | r4: no fact was recreated | `{}` |
| PASS | guard | r4: the erased trip is still in no memory store | `found nowhere` |
