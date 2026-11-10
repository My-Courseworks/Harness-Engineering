# langgraph · heldout-r4 · run 1 · r4-erase-open-tab-case-followup

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r4e1-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, Dana here, card ending 5127, ZIP 60614. CloudNest Storage charged me $9.99 on November 1 even though I cancelled in October, please dispute it. Also, I'm in Reykjavik until November 28, so expect charges in krona.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `remember_customer_fact({"key": "travel_notice", "value": "Reykjavik", "valid_until": "2026-11-28"})` → `{"stored": {"travel_notice": {"value": "Reykjavik", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-11-28", "expires_at": "2026-11-29T00:00:00Z"}}, "replaced": null}`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest Storage subscription in October; the $9.99 charge posted November 1, 2026." …)` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-92b97305", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Thanks, Dana - verified, and here's where things stand:

**Dispute filed: case C-5001** (under review)
- Charge: CloudNest Storage, $9.99, posted 2026-11-01 (transaction T-3002)
- Reason: subscription cancelled in October
- Follow-up due **2026-11-23**, sent by **secure message in the Kestrel app** - that's the default since you have no contact channel set. If you set one (email or SMS) before then, the follow-up goes there instead.
- Disputes are currently reviewed in about 10 days.

**Travel notice saved:** Reykjavik until 2026-11-28, so foreign-currency charges (ISK) on your card won't be flagged as unexpected.

Anything else - like adding a cancellation reference from CloudNest to the case if you have one?

**Customer:** Yes, go ahead and file it.

**Assistant:** The dispute is already filed - no need to file again. Case **C-5001** covers the $9.99 CloudNest charge from 2026-11-01, under review, with the follow-up due 2026-11-23 by secure message in the Kestrel app.

If you meant something else - for example, attaching a cancellation confirmation or reference number from CloudNest - send it to me and I'll add it to the case.

_Episode written:_ Conversation on 2026-11-13: Customer said she cancelled CloudNest Storage in October and disputed the $9.99 2026-11-01 charge (not verified). Dispute C-5001 for T-3002 was filed, under review; follow-up due 2026-11-23 by secure message in Kestrel app. Customer said she's in Reykjavik until 2026-11-28 and expects krona charges (not verified); travel notice saved. She later said “go ahead”; assistant explained it was already filed. Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | r4: the dispute is filed on T-3002 | `[{"case_id": "C-5001", "status": "under_review"}]` |
| PASS | prospective | r4: its follow-up is due 2026-11-23, no approval | `[{"trigger_at": "2026-11-23T10:00:00Z", "approval": "none", "status": "pending", "resume": {"case_id": "C-5001"}}]` |
| PASS | semantic | r4: the travel notice is stored until 2026-11-28 | `{"value": "Reykjavik", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-11-28", "expires_at": "2026-11-29T00:00:00Z"}` |

## r4e1-s2  ·  session  ·  dana  ·  2026-11-23T09:55:00Z

**Customer:** I've changed my mind about all of this. Erase everything you remember about me and every conversation we've had.

- `request_memory_erasure({})` → `{"erased_now": "1 remembered facts, 1 past-conversation summaries, 1 other conversation transcripts, 0 reminders with their notes", "this_conversation": "its transcript is deleted when the conversation ends, or once it has been idle for 30 minutes if the customer just closes the chat; nothing more can be stored for the customer in it (a new conversation afterwards starts fresh)", "kept": "dispute  …`

**Assistant:** Done - that's all erased now:

- The facts stored about you (your contact channel and travel notice entries)
- The summary of your past conversation
- That earlier conversation's transcript
- Reminders with their notes (there were none)

What Kestrel still keeps: dispute cases, transactions and messages already sent are bank records with their own legal retention.

This conversation's own transcript is deleted when the conversation ends - or once the chat has been idle for 30 minutes if you just close it. Nothing more can be stored for you in this conversation, so if you want a reminder or a preference set later, start a new conversation and it will begin fresh.

## r4e1-fire-1  ·  fire_followups  ·  2026-11-23T10:06:00Z

### follow-up session `followup-F-92b97305-1`

**Scheduler:** [scheduled follow-up F-92b97305] action=case_status_followup resume={"case_id": "C-5001"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest Storage subscription in October; the $9.99 charge posted November 1, 2026.", "status": "under_review", "opened_at": "2026-11-13T10:00:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null, "decision_id": null}] …`
- `notify_customer({"message": "Update on your dispute case C-5001 (CloudNest Storage, $9.99 posted November 1, 2026): it is still under review. No decision has been made yet, so no further action is needed from you rig …)` → `{"channel": "secure_message", "message_id": 1, "status": "sent"}`

**Assistant:** I'll check the current status of this case.
Case C-5001 was still under review; I sent the customer one update by secure message in the Kestrel app.

_outcomes:_ `[{"followup_id": "F-92b97305", "user_id": "dana", "outcome": "fired_done", "error": null}]`

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

- `load_memory({"query": "travel plans destination"})` → `{"memories": []}`

**Assistant:** Here's what I have on file for you right now:

- **Contact channel:** none set - so any follow-ups or reminders go by secure message in the Kestrel app (the default).
- **Travel notice:** none on file.

I also checked my records of our earlier conversations and found nothing - so I have no record of you telling me where you'd be travelling. If you tell me the destination (and return date), I can add a travel notice now.

_Episode written:_ Conversation on 2026-11-30: Customer asked what was on file and whether the assistant remembered their travel destination. The assistant loaded memory (no results) and reported no contact channel, no travel notice, and no record of travel plans; no case or transaction IDs appeared. The assistant asked for destination and return date to add a travel notice immediately if provided. No customer preference stated. Case outcomes: no case touched. Lesson: Next time, describe the memory lookup result as no stored travel plans found, rather than implying no earlier conversations occurred, then ask for destination and return date.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | r4: nothing erased comes back in a later chat | `Here's what I have on file for you right now:  - **Contact channel:** none set - so any follow-ups or reminders go by secure message in the Kestrel app (the default). - **Travel notice:** none on file.  I also checked my …` |
| PASS | episodic | r4: recall, if used, returns nothing erased | `{"memories": []}` |
| PASS | semantic | r4: no fact was recreated | `{}` |
| PASS | guard | r4: the erased trip is still in no memory store | `found nowhere` |
