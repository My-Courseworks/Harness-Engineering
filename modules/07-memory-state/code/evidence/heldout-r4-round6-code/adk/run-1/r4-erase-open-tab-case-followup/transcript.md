# adk · heldout-r4 · run 1 · r4-erase-open-tab-case-followup

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r4e1-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, Dana here, card ending 5127, ZIP 60614. CloudNest Storage charged me $9.99 on November 1 even though I cancelled in October, please dispute it. Also, I'm in Reykjavik until November 28, so expect charges in krona.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `remember_customer_fact({"key": "travel_notice", "value": "Reykjavik", "valid_until": "2026-11-28"})` → `{"stored": {"travel_notice": {"value": "Reykjavik", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-11-28", "expires_at": "2026-11-29T00:00:00Z"}}, "replaced": null}`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the $9.99 charge posted 2026-11-01."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-2785ad22", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** I'll verify your identity, look up the charge, and note your travel plans.
Thanks, Dana - you're verified.

**Dispute filed: case C-5001**
- Charge: CloudNest Storage, $9.99, posted 2026-11-01
- Reason: subscription cancelled in October
- Status: under review
- Follow-up due: **2026-11-23** (about 10 days out, Kestrel's current review time), sent as a **secure message in the Kestrel app**, since you don't have a contact channel set. If you set one before then, the update goes there instead.

**Travel notice saved:** Reykjavik until 2026-11-28, so krona charges during that period won't be flagged as unusual.

If you find a cancellation confirmation or reference from CloudNest, send it over and I'll attach it to the case.

**Customer:** Yes, go ahead and file it.

**Assistant:** The dispute is already filed - no need to do it again. Here's where it stands:

- **Case C-5001** - CloudNest Storage, $9.99 posted 2026-11-01, reason: subscription cancelled in October
- Status: **under review**
- Follow-up due **2026-11-23**, delivered as a secure message in the Kestrel app (no contact channel is set on your account)

If you meant something else - for example attaching a CloudNest cancellation confirmation - just send it and I'll add it to case C-5001.

_Episode written:_ Conversation on 2026-11-13: Customer wanted a $9.99 CloudNest Storage charge posted 2026-11-01 disputed; the customer said she cancelled in October (not verified). Reykjavik travel notice saved until 2026-11-28. Identity verified; transactions T-3001/T-3002 found. Dispute filed on T-3002 as case C-5001, under review; follow-up due 2026-11-23 by Kestrel secure message, or a new contact channel if set. Offered to attach cancellation confirmation. Case outcomes: C-5001 under_review. Lesson: Next time, explicitly confirm the customer's intent before filing a dispute, so the customer does not later ask to file it after it has already been submitted.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | r4: the dispute is filed on T-3002 | `[{"case_id": "C-5001", "status": "under_review"}]` |
| PASS | prospective | r4: its follow-up is due 2026-11-23, no approval | `[{"trigger_at": "2026-11-23T10:00:00Z", "approval": "none", "status": "pending", "resume": {"case_id": "C-5001"}}]` |
| PASS | semantic | r4: the travel notice is stored until 2026-11-28 | `{"value": "Reykjavik", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-11-28", "expires_at": "2026-11-29T00:00:00Z"}` |

## r4e1-s2  ·  session  ·  dana  ·  2026-11-23T09:55:00Z

**Customer:** I've changed my mind about all of this. Erase everything you remember about me and every conversation we've had.

- `request_memory_erasure({})` → `{"erased_now": {"remembered_facts": ["travel_notice"], "past_conversation_summaries": 1, "other_conversation_transcripts": 1, "reminders_with_their_notes": 0}, "this_conversation": "its transcript is deleted when the conversation ends, once it has been idle for 30 minutes if the customer just closes the chat, or when a scheduled follow-up of theirs falls due, whichever comes first; until then the  …`

**Assistant:** Done - erased now:

- Your stored facts (the travel notice on file; no contact channel was set)
- 1 past conversation summary
- 1 other conversation transcript
- 0 reminders

Kestrel still keeps dispute cases, transactions and messages already sent - those are bank records with their own legal retention.

This conversation's own transcript is deleted when the conversation ends: once it's been idle for 30 minutes if you just close the chat, or when a scheduled follow-up of yours falls due, whichever comes first. Until then you can keep talking here - but nothing more can be stored for you in this conversation (no reminders, no preferences). A new conversation afterwards starts fresh.

## r4e1-fire-1  ·  fire_followups  ·  2026-11-23T10:06:00Z

### follow-up session `followup-F-2785ad22-1`

**Scheduler:** [scheduled follow-up F-2785ad22] action=case_status_followup resume={"case_id": "C-5001"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the $9.99 charge posted 2026-11-01.", "status": "under_review", "opened_at": "2026-11-13T10:00:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null, "decision_id": null}]}`
- `notify_customer({"message": "Update on dispute case C-5001 (CloudNest charge of $9.99 posted 2026-11-01): it is still under review. No decision has been made yet. If you have new evidence, such as proof of the cancel …)` → `{"channel": "secure_message", "message_id": 1, "status": "sent"}`

**Assistant:** I'll check the case status and then notify the customer.
Case C-5001 (CloudNest, $9.99) is still **under review** - no decision yet. I sent the customer an update by secure message in the Kestrel app, including the next step: message the card-care chat to attach any new evidence, such as proof of the subscription cancellation.

_outcomes:_ `[{"followup_id": "F-2785ad22", "user_id": "dana", "outcome": "fired_done", "error": null}]`

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

- `load_memory({"query": "travel plans destination dates"})` → `{"result": "memories=[]"}`

**Assistant:** I'll check my records and our earlier conversation.
Here's what I have on file for you right now:

- **Contact channel:** none set - so any follow-ups or reminders go to you as a secure message in the Kestrel app by default.
- **Travel notice:** none on file.

I also checked our earlier conversations and found no record of a travel destination or dates - so I can't tell you where you said you'd be travelling. It may be that the detail wasn't stored, or that the earlier conversation is no longer available to me.

If you'd like, tell me the destination and your return date and I'll add a travel notice now.

_Episode written:_ Conversation on 2026-11-30: Customer asked what was on file and where they'd said they would travel. Assistant checked memory/earlier chats: no travel notice, destination or dates; contact channel unset, so follow-ups default to Kestrel app secure messages. Assistant offered to add a travel notice now if given destination and return date. Customer said they had previously stated travel plans (not verified). Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | r4: nothing erased comes back in a later chat | `I'll check my records and our earlier conversation. Here's what I have on file for you right now:  - **Contact channel:** none set - so any follow-ups or reminders go to you as a secure message in the Kestrel app by defa …` |
| PASS | episodic | r4: recall, if used, returns nothing erased | `{"result": "memories=[]"}` |
| PASS | semantic | r4: no fact was recreated | `{}` |
| PASS | guard | r4: the erased trip is still in no memory store | `found nowhere` |
