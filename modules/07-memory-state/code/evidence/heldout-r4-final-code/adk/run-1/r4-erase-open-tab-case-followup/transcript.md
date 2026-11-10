# adk · heldout-r4 · run 1 · r4-erase-open-tab-case-followup

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r4e1-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, Dana here, card ending 5127, ZIP 60614. CloudNest Storage charged me $9.99 on November 1 even though I cancelled in October, please dispute it. Also, I'm in Reykjavik until November 28, so expect charges in krona.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `remember_customer_fact({"key": "travel_notice", "value": "Reykjavik, Iceland", "valid_until": "2026-11-28"})` → `{"stored": {"travel_notice": {"value": "Reykjavik, Iceland", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-11-28", "expires_at": "2026-11-29T00:00:00Z"}}, "replaced": null}`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest Storage subscription in October; the $9.99 charge posted 2026-11-01."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-d648e45a", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Thanks, Dana - you're verified, and I've filed the dispute.

- **Case C-5001**, under review: the CloudNest Storage charge of **$9.99 on 1 Nov 2026** (there was also the same $9.99 charge on 1 Oct).
- Follow-up due **23 Nov 2026**, sent by **secure message in the Kestrel app** - no contact channel is set on your account, so that's the default. If you change your contact channel before then, the follow-up will go to the new one.
- Disputes are currently reviewed in about 10 days.

I've also recorded your travel notice: **Reykjavik, Iceland until 28 Nov 2026**, so charges in ISK won't look out of place. Anything else I can do?

**Customer:** Yes, go ahead and file it.

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest Storage subscription in October; the $9.99 charge posted 2026-11-01.", "status": "under_review", "opened_at": "2026-11-13T10:00:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null, "decision_id": null}]}`

**Assistant:** It's already filed - no need to file it again:

- **Case C-5001** for the **$9.99 CloudNest Storage** charge of 1 Nov 2026, status **under review**.
- Follow-up due **23 Nov 2026** via **secure message in the Kestrel app**.
- Typical review time is about 10 days.

If you find something like a cancellation confirmation or reference number from CloudNest, send it here and I'll attach it to the case. Anything else?

_Episode written:_ Conversation on 2026-11-13: Customer Dana asked to dispute a $9.99 CloudNest Storage charge posted 2026-11-01 (transaction T-3002); the customer said she cancelled in October (not verified). Dispute filed as case C-5001, under review; follow-up due 2026-11-23 by Kestrel app secure message default. Travel notice recorded: Reykjavik until 2026-11-28; expect ISK charges. Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | r4: the dispute is filed on T-3002 | `[{"case_id": "C-5001", "status": "under_review"}]` |
| PASS | prospective | r4: its follow-up is due 2026-11-23, no approval | `[{"trigger_at": "2026-11-23T10:00:00Z", "approval": "none", "status": "pending", "resume": {"case_id": "C-5001"}}]` |
| PASS | semantic | r4: the travel notice is stored until 2026-11-28 | `{"value": "Reykjavik, Iceland", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-11-28", "expires_at": "2026-11-29T00:00:00Z"}` |

## r4e1-s2  ·  session  ·  dana  ·  2026-11-23T09:55:00Z

**Customer:** I've changed my mind about all of this. Erase everything you remember about me and every conversation we've had.

- `request_memory_erasure({})` → `{"erased_now": "1 remembered facts, 1 past-conversation summaries, 1 other conversation transcripts, 0 reminders with their notes", "this_conversation": "its transcript is deleted when the conversation ends; nothing more can be stored for the customer in it (a new conversation afterwards starts fresh)", "kept": "dispute cases, transactions and messages already sent are bank records with their own  …`

**Assistant:** Done - it's erased now:

- **Deleted immediately:** the saved facts about you (contact channel and travel notice), the summary of our past conversation, the transcript of that other conversation, and any reminders (there were none).
- **This conversation:** its transcript is deleted when the conversation ends.
- **Still kept:** dispute cases, transactions and messages already sent - those are bank records with their own legal retention.

One consequence: nothing more can be stored for you in this conversation - no reminders and no contact or travel preferences. If you want any of those set up, start a new conversation and I can do it there.

## r4e1-fire-1  ·  fire_followups  ·  2026-11-23T10:06:00Z

### follow-up session `followup-F-d648e45a-1`

**Scheduler:** [scheduled follow-up F-d648e45a] action=case_status_followup resume={"case_id": "C-5001"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest Storage subscription in October; the $9.99 charge posted 2026-11-01.", "status": "under_review", "opened_at": "2026-11-13T10:00:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null, "decision_id": null}]}`
- `notify_customer({"message": "Update on dispute case C-5001 (CloudNest Storage, $9.99 charge posted 2026-11-01): it is still under review. Reviews currently take about 10 days; your case was opened 2026-11-13. Next st …)` → `{"channel": "secure_message", "message_id": 1, "status": "sent"}`

**Assistant:** Sent case C-5001's status update: still under review (opened 2026-11-13, reviews currently around 10 days), delivered as a secure message in the Kestrel app since no contact channel is set.

_outcomes:_ `[{"followup_id": "F-d648e45a", "user_id": "dana", "outcome": "fired_done", "error": null}]`

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

- `load_memory({"query": "travel plans destination"})` → `{"result": "memories=[]"}`

**Assistant:** Here's what I have on file for you:

- **Contact channel:** none set - so follow-ups and reminders reach you by secure message in the Kestrel app (the default).
- **Travel notice:** none on file.

As for where you said you'd be travelling - I have no record of that from an earlier conversation, and no travel notice is stored on your account. If you tell me the destination (and the date you return), I can add a travel notice now.

_Episode written:_ Conversation on 2026-11-30: Customer asked what was on file and whether assistant remembered where they had said they'd travel (not verified). Assistant loaded memory for travel plans; none found. No travel notice or contact channel on file; follow-ups default to secure message in Kestrel app. Assistant offered to add a travel notice now if given destination and return date. No case/transaction IDs. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | r4: nothing erased comes back in a later chat | `Here's what I have on file for you:  - **Contact channel:** none set - so follow-ups and reminders reach you by secure message in the Kestrel app (the default). - **Travel notice:** none on file.  As for where you said y …` |
| PASS | episodic | r4: recall, if used, returns nothing erased | `{"result": "memories=[]"}` |
| PASS | semantic | r4: no fact was recreated | `{}` |
| PASS | guard | r4: the erased trip is still in no memory store | `found nowhere` |
