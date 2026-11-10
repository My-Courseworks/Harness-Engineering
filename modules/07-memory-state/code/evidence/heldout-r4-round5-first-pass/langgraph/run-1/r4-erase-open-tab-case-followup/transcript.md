# langgraph · heldout-r4 · run 1 · r4-erase-open-tab-case-followup

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r4e1-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, Dana here, card ending 5127, ZIP 60614. CloudNest Storage charged me $9.99 on November 1 even though I cancelled in October, please dispute it. Also, I'm in Reykjavik until November 28, so expect charges in krona.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `remember_customer_fact({"key": "travel_notice", "value": "Reykjavik", "valid_until": "2026-11-28"})` → `{"stored": {"travel_notice": {"value": "Reykjavik", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-11-28", "expires_at": "2026-11-29T00:00:00Z"}}, "replaced": null}`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest Storage subscription in October; the $9.99 charge posted 2026-11-01."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-87ef4ce2", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Hi Dana - all set:

- **Dispute filed:** case **C-5001** for the $9.99 CloudNest Storage charge on **Nov 1** (T-3002), reason: subscription cancelled. Status: under review. Disputes are currently reviewed in about 10 days.
- **Follow-up:** due **Nov 23**, sent by **secure message in the Kestrel app** (the default since you have no contact channel set - if you set one before then, it will go there instead).
- **Travel notice:** recorded - Reykjavik until **Nov 28**, 2026. Charges in krona are expected.

If you have a cancellation confirmation or reference from CloudNest, I can attach it to the case - that helps the review. Anything else?

**Customer:** Yes, go ahead and file it.

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest Storage subscription in October; the $9.99 charge posted 2026-11-01.", "status": "under_review", "opened_at": "2026-11-13T10:00:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null, "decision_id": null}]}`

**Assistant:** No need - it's already filed. Case **C-5001** is open and under review for the Nov 1 $9.99 CloudNest charge, with the follow-up due **Nov 23** by secure message in the Kestrel app. Filing it again would just create a duplicate.

If you meant the CloudNest cancellation confirmation, send it over and I'll attach it to C-5001.

_Episode written:_ Conversation on 2026-11-13: Customer said she cancelled CloudNest Storage in October (not verified) and wanted the Nov 1 $9.99 charge disputed. Dispute filed for T-3002 as case C-5001, under review; follow-up due Nov 23, 2026 via Kestrel app secure message. Travel notice recorded: Reykjavik until Nov 28, 2026; krona charges expected. Customer then said go ahead; assistant clarified already filed. Case outcomes: C-5001 under_review. Lesson: When a customer says 'go ahead and file it' immediately after an offer to attach evidence, clarify whether they mean attaching the evidence or filing a new dispute before taking action.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | r4: the dispute is filed on T-3002 | `[{"case_id": "C-5001", "status": "under_review"}]` |
| PASS | prospective | r4: its follow-up is due 2026-11-23, no approval | `[{"trigger_at": "2026-11-23T10:00:00Z", "approval": "none", "status": "pending", "resume": {"case_id": "C-5001"}}]` |
| PASS | semantic | r4: the travel notice is stored until 2026-11-28 | `{"value": "Reykjavik", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-11-28", "expires_at": "2026-11-29T00:00:00Z"}` |

## r4e1-s2  ·  session  ·  dana  ·  2026-11-23T09:55:00Z

**Customer:** I've changed my mind about all of this. Erase everything you remember about me and every conversation we've had.

- `request_memory_erasure({})` → `{"erased_now": "1 remembered facts, 1 past-conversation summaries, 1 other conversation transcripts, 0 reminders with their notes", "this_conversation": "its transcript is deleted when the conversation ends, or once it has been idle for 30 minutes if the customer just closes the chat; nothing more can be stored for the customer in it (a new conversation afterwards starts fresh)", "kept": "dispute  …`

**Assistant:** Done. I erased everything stored about you: the remembered facts, the summary of your past conversations, and the other conversations' transcripts (no reminders were affected).

What Kestrel keeps: dispute cases, transactions and messages already sent are bank records with their own legal retention. This conversation's transcript is deleted when it ends - or if you just close the chat, once it has been idle for 30 minutes.

Nothing more can be stored for you in this conversation - not a reminder or a preference. If you want to set either up later, start a new conversation and it will begin fresh.

## r4e1-fire-1  ·  fire_followups  ·  2026-11-23T10:06:00Z

### follow-up session `followup-F-87ef4ce2-1`

**Scheduler:** [scheduled follow-up F-87ef4ce2] action=case_status_followup resume={"case_id": "C-5001"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest Storage subscription in October; the $9.99 charge posted 2026-11-01.", "status": "under_review", "opened_at": "2026-11-13T10:00:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null, "decision_id": null}]}`
- `notify_customer({"message": "Update on your dispute C-5001 (CloudNest Storage, $9.99 posted 2026-11-01): it is still under review with the bank \u2014 no decision yet. Disputes are currently reviewed in about 10 days …)` → `{"channel": "secure_message", "message_id": 1, "status": "sent"}`

**Assistant:** I'll check the case status for this follow-up.
Follow-up sent via secure message in the Kestrel app: case C-5001 (CloudNest Storage, $9.99) remains under review with no decision yet, and no action is needed from the customer right now.

_outcomes:_ `[{"followup_id": "F-87ef4ce2", "user_id": "dana", "outcome": "fired_done", "error": null}]`

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

**Assistant:** Here's what's on file for you right now:

- **Contact channel:** none set - so any follow-ups or reminders would reach you as a secure message in the Kestrel app.
- **Travel notice:** none on file.

As for where you said you'd be travelling - I have no record of any earlier conversation about that, so I can't tell you a destination. If you tell me the place and your return date, I can add a travel notice now.

_Episode written:_ Conversation on 2026-11-30: The customer wanted to know what was on file and whether an earlier travel destination was remembered. The assistant checked memory and found none. No contact channel or travel notice was on file; the assistant said there was no record of an earlier travel discussion and offered to add a travel notice if given place and return date. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | r4: nothing erased comes back in a later chat | `Here's what's on file for you right now:  - **Contact channel:** none set - so any follow-ups or reminders would reach you as a secure message in the Kestrel app. - **Travel notice:** none on file.  As for where you said …` |
| PASS | episodic | r4: recall, if used, returns nothing erased | `{"memories": []}` |
| PASS | semantic | r4: no fact was recreated | `{}` |
| PASS | guard | r4: the erased trip is still in no memory store | `found nowhere` |
