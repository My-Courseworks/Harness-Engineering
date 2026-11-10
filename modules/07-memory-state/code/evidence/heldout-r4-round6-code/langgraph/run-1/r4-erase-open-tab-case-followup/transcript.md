# langgraph · heldout-r4 · run 1 · r4-erase-open-tab-case-followup

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r4e1-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, Dana here, card ending 5127, ZIP 60614. CloudNest Storage charged me $9.99 on November 1 even though I cancelled in October, please dispute it. Also, I'm in Reykjavik until November 28, so expect charges in krona.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `remember_customer_fact({"key": "travel_notice", "value": "Reykjavik", "valid_until": "2026-11-28"})` → `{"stored": {"travel_notice": {"value": "Reykjavik", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-11-28", "expires_at": "2026-11-29T00:00:00Z"}}, "replaced": null}`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the $9.99 charge posted 2026-11-01."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-0a6dd405", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`
- `search_policy({"question": "foreign transaction fee on purchases abroad"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.844, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "travel-notices",  …`

**Assistant:** Hi Dana - thanks, identity verified.

- **Dispute filed:** CloudNest Storage, $9.99 on 2026-11-01 (case **C-5001**, under review). Your follow-up is due **2026-11-23** and will reach you as a secure message in the Kestrel app, since no contact channel is set. If you'd like it emailed or texted instead, I can change that.
- **Travel notice:** recorded for Reykjavik until 2026-11-28. That helps prevent false declines on your krona charges, and it's deleted automatically after your return date.
- **Heads up on fees:** a travel notice doesn't waive Kestrel's foreign transaction fee - 1.25% of the US-dollar amount on any purchase made in a non-USD currency, posted as a separate line the same day.

**Customer:** Yes, go ahead and file it.

**Assistant:** Already done - the dispute was filed when I verified you a moment ago. Case **C-5001**, CloudNest Storage $9.99 posted 2026-11-01, status: under review. No further action is needed from you.

Your status follow-up is due **2026-11-23** and will arrive as a secure message in the Kestrel app. Anything else I can help with?

_Episode written:_ Conversation on 2026-11-13: Customer asked to dispute a $9.99 CloudNest Storage charge posted 2026-11-01; she said she cancelled in October (not verified). Dispute filed on transaction T-3002, case C-5001, under review, follow-up due 2026-11-23 via Kestrel app secure message. Customer said she is in Reykjavik until 2026-11-28 and expects krona charges; travel notice recorded. Assistant explained 1.25% foreign transaction fee applies. Case outcomes: C-5001 under_review. Lesson: Next time, when the customer has already requested a dispute, clearly state that it has been filed instead of prompting them to approve filing again.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | r4: the dispute is filed on T-3002 | `[{"case_id": "C-5001", "status": "under_review"}]` |
| PASS | prospective | r4: its follow-up is due 2026-11-23, no approval | `[{"trigger_at": "2026-11-23T10:00:00Z", "approval": "none", "status": "pending", "resume": {"case_id": "C-5001"}}]` |
| PASS | semantic | r4: the travel notice is stored until 2026-11-28 | `{"value": "Reykjavik", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-11-28", "expires_at": "2026-11-29T00:00:00Z"}` |

## r4e1-s2  ·  session  ·  dana  ·  2026-11-23T09:55:00Z

**Customer:** I've changed my mind about all of this. Erase everything you remember about me and every conversation we've had.

- `request_memory_erasure({})` → `{"erased_now": {"remembered_facts": ["travel_notice"], "past_conversation_summaries": 1, "other_conversation_transcripts": 1, "reminders_with_their_notes": 0}, "this_conversation": "its transcript is deleted when the conversation ends, once it has been idle for 30 minutes if the customer just closes the chat, or when a scheduled follow-up of theirs falls due, whichever comes first; until then the  …`

**Assistant:** Done. What was erased just now:

- The fact I had stored about you (a travel notice)
- 1 past conversation summary
- 1 other conversation transcript
- No reminders were stored, so none were deleted

What Kestrel keeps: dispute cases, transactions and messages already sent are bank records with their own legal retention.

This conversation's own transcript is deleted when the conversation ends - after 30 minutes idle if you just close the chat, or sooner if a scheduled follow-up of yours falls due, whichever comes first. Until then you can keep talking here, though nothing more can be stored for you in this conversation (no reminders, no preferences). If you want something set up later, start a new conversation and it will begin fresh.

## r4e1-fire-1  ·  fire_followups  ·  2026-11-23T10:06:00Z

### follow-up session `followup-F-0a6dd405-1`

**Scheduler:** [scheduled follow-up F-0a6dd405] action=case_status_followup resume={"case_id": "C-5001"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the $9.99 charge posted 2026-11-01.", "status": "under_review", "opened_at": "2026-11-13T10:00:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null, "decision_id": null}]}`
- `notify_customer({"message": "Your dispute case C-5001 (CloudNest, $9.99 charge posted 2026-11-01) is still under review. No action is needed from you right now; we'll update you again as the review proceeds. If you w …)` → `{"channel": "secure_message", "message_id": 1, "status": "sent"}`

**Assistant:** Case C-5001 is still under review; I've sent the customer one secure message in the Kestrel app with that status and the next step.

_outcomes:_ `[{"followup_id": "F-0a6dd405", "user_id": "dana", "outcome": "fired_done", "error": null}]`

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

- `load_memory({"query": "travel plans destination trip"})` → `{"memories": []}`

**Assistant:** I have no record of an earlier conversation, so I can't tell you where you said you'd be travelling - and nothing about a trip is on file for you.

Here's what's stored about you right now:
- **Contact channel:** none set, so any follow-ups or reminders go by secure message in the Kestrel app (the default).
- **Travel notice:** none on file.

If you tell me your destination (and return date, if you want one), I can add a travel notice.

_Episode written:_ Conversation on 2026-11-30: Customer asked what was on file and whether an earlier travel destination was remembered; they said they had previously stated one (not verified). Memory lookup returned no records. The assistant said no travel notice or contact channel was stored, defaulting to secure message in the Kestrel app, and offered to add a travel notice if given destination and return date. Case outcomes: no case touched. Lesson: Next time, use an appropriate profile lookup to confirm contact-channel details before stating them, rather than relying on a travel-plans memory query alone.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | r4: nothing erased comes back in a later chat | `I have no record of an earlier conversation, so I can't tell you where you said you'd be travelling - and nothing about a trip is on file for you.  Here's what's stored about you right now: - **Contact channel:** none se …` |
| PASS | episodic | r4: recall, if used, returns nothing erased | `{"memories": []}` |
| PASS | semantic | r4: no fact was recreated | `{}` |
| PASS | guard | r4: the erased trip is still in no memory store | `found nowhere` |
