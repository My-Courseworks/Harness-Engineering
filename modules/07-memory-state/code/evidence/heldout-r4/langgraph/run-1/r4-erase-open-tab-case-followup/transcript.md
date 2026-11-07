# langgraph · heldout-r4 · run 1 · r4-erase-open-tab-case-followup

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r4e1-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, Dana here, card ending 5127, ZIP 60614. CloudNest Storage charged me $9.99 on November 1 even though I cancelled in October, please dispute it. Also, I'm in Reykjavik until November 28, so expect charges in krona.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `remember_customer_fact({"key": "travel_notice", "value": "Reykjavik", "valid_until": "2026-11-28"})` → `{"stored": {"travel_notice": {"value": "Reykjavik", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-11-28", "expires_at": "2026-11-29T00:00:00Z"}}, "replaced": null}`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says subscription was cancelled in October; the November 1 charge is after cancellation."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-66ec5dae", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** All set, Dana.

**Dispute filed** - CloudNest Storage, $9.99, posted November 1 (case **C-5001**). It's now under review; these are currently taking about 10 days.

**Follow-up:** due **November 23**, sent by secure message in the Kestrel app, since you have no contact channel set. If you set an email or SMS before then, it will go there instead.

**Travel notice:** Reykjavik until November 28 is on file, so krona charges from your trip should be expected.

One thing that would help the case: if you have the cancellation confirmation (an email, reference number, or date), send it over and I'll attach it to C-5001.

**Customer:** Yes, go ahead and file it.

**Assistant:** It's already filed - no need to do it again. Case **C-5001** covers the November 1 CloudNest charge of $9.99, and it's under review now.

Your follow-up is due **November 23**, by secure message in the Kestrel app (or email/SMS if you set one before then).

If you find your October cancellation confirmation, send it here and I'll attach it to the case.

_Episode written:_ Conversation on 2026-11-13: Customer asked to dispute a Nov 1 CloudNest Storage $9.99 charge (T-3002), saying the subscription was cancelled in October (not verified). Dispute filed as case C-5001, under review; assistant said about 10 days. Follow-up due Nov 23 via Kestrel app secure message unless contact channel changes. Travel notice stored for Reykjavik until Nov 28; customer expects krona charges. Case outcomes: C-5001 under_review. Lesson: Next time, explicitly say the dispute is already filed before requesting cancellation evidence, so the customer does not think filing is still pending.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | r4: the dispute is filed on T-3002 | `[{"case_id": "C-5001", "status": "under_review"}]` |
| PASS | prospective | r4: its follow-up is due 2026-11-23, no approval | `[{"trigger_at": "2026-11-23T10:00:00Z", "approval": "none", "status": "pending", "resume": {"case_id": "C-5001"}}]` |
| PASS | semantic | r4: the travel notice is stored until 2026-11-28 | `{"value": "Reykjavik", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-11-28", "expires_at": "2026-11-29T00:00:00Z"}` |

## r4e1-s2  ·  session  ·  dana  ·  2026-11-23T09:55:00Z

**Customer:** I've changed my mind about all of this. Erase everything you remember about me and every conversation we've had.

**Assistant:** I can do that. To verify, please type your card's last 4 digits and your billing ZIP code.

## r4e1-fire-1  ·  fire_followups  ·  2026-11-23T10:06:00Z

### follow-up session `followup-F-66ec5dae-1`

**Scheduler:** [scheduled follow-up F-66ec5dae] action=case_status_followup resume={"case_id": "C-5001"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says subscription was cancelled in October; the November 1 charge is after cancellation.", "status": "under_review", "opened_at": "2026-11-13T10:00:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null, "decision_id": null}]}`
- `notify_customer({"message": "Case C-5001 (November 1 subscription charge) is still under review \u2014 no decision yet. Disputes are currently reviewed in about 10 days from filing. We'll message you when the status  …)` → `{"channel": "secure_message", "message_id": 1, "status": "sent"}`

**Assistant:** Done - the customer was sent one secure message: case C-5001 (the November 1 subscription charge) is still under review, disputes currently take about 10 days, and they can add evidence or reply via the card-care chat.

_Episode written:_ Scheduled follow-up on 2026-11-23 (customer not present): Customer wanted a status update on case C-5001 (txn T-3002); they said the subscription was cancelled in October and the November 1 charge came after cancellation (not verified). Assistant found status under_review, no decision, and sent one secure message saying disputes take about 10 days from filing and they will be messaged when status changes. Case outcomes: C-5001 under_review. Lesson: none

_outcomes:_ `[{"followup_id": "F-66ec5dae", "user_id": "dana", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | semantic | r4: an erasure pending at fire time still runs: no fact remains | `{"travel_notice": {"value": "Reykjavik", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-11-28", "expires_at": "2026-11-29T00:00:00Z"}}` |
| **FAIL** | episodic | r4: no episode remains, and the fired follow-up wrote none | `2 episodes; purged 0` |
| **FAIL** | working | r4: no transcript remains: not the open tab, not the follow-up's own session | `3 transcripts: ['followup-F-66ec5dae-1', 'r4e1-s1', 'r4e1-s2']` |
| PASS | working | r4: the follow-up session is unattended even though an erasure ran around it | `["find_transactions", "get_case_status", "list_my_followups", "load_memory", "notify_customer", "report_malformed_tool_call", "search_policy"]` |
| **FAIL** | guard | r4: nothing she said is in any memory store | `{"Reykjavik": ["lg_store.db", "lg_checkpoints.db-wal"], "krona": ["lg_store.db", "lg_checkpoints.db-wal"]}` |

## r4e1-fire-2  ·  fire_followups  ·  2026-11-23T10:20:00Z

_outcomes:_ `[]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r4: the case follow-up still reaches the erased customer, exactly once | `1 messages` |
| PASS | guard | r4: no outbound message carries a masking token or a masked identifier | `3 outbound messages and episodes clean` |
| **FAIL** | episodic | r4: still no episode after the retry window | `2 episodes; purged 0` |
| **FAIL** | working | r4: still no transcript after the retry window | `3 transcripts: ['followup-F-66ec5dae-1', 'r4e1-s1', 'r4e1-s2']` |

## r4e1-s3  ·  session  ·  dana  ·  2026-11-30T10:00:00Z

**Customer:** Hello again. What do you have on file about me, and do you remember where I said I'd be travelling?

- `load_memory({"query": "travel plans destination dates"})` → `{"memories": [{"at": "2026-11-13T10:04:00Z", "text": "Conversation on 2026-11-13: Customer asked to dispute a Nov 1 CloudNest Storage $9.99 charge (T-3002), saying the subscription was cancelled in October (not verified). Dispute filed as case C-5001, under review; assistant said about 10 days. Follow-up due Nov 23 via Kestrel app secure message unless contact channel changes. Travel notice stored …`
- `get_case_status({})` → `{"cases": [{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says subscription was cancelled in October; the November 1 charge is after cancellation.", "status": "under_review", "opened_at": "2026-11-13T10:00:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null, "decision_id": null}]}`

**Assistant:** Here's what's on file for you right now:

- **Contact channel:** none set - so anything Kestrel sends you (case follow-ups, reminders) goes by secure message in the Kestrel app.
- **Travel notice:** none on file. I do see from our 13 Nov conversation that you had a notice for **Reykjavik** (expecting krona charges), but it ran until 28 Nov, so it's now expired and no longer active.
- **Dispute case:** C-5001, opened 13 Nov on the 1 Nov CloudNest Storage $9.99 charge (cancelled subscription). Status is still **under review** - no decision yet.

If you're travelling again, tell me the destination and return date and I'll set a new travel notice.

_Episode written:_ Conversation on 2026-11-30: Customer asked what was on file and where they'd said they'd travel. Assistant checked memory/status: C-5001 (txn T-3002) remains under review; prior Reykjavik notice expired Nov 28, no active notice. No contact channel set; Kestrel app secure messages. Prior follow-up due Nov 23; the customer said subscription cancelled in October (not verified). Assistant offered new travel notice if details provided. Case outcomes: C-5001 under_review. Lesson: When summarizing what is on file, include any scheduled follow-up date or prior promise as well as the case status.

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | episodic | r4: nothing erased comes back in a later chat | `Here's what's on file for you right now:  - **Contact channel:** none set - so anything Kestrel sends you (case follow-ups, reminders) goes by secure message in the Kestrel app. - **Travel notice:** none on file. I do se …` |
| **FAIL** | episodic | r4: recall, if used, returns nothing erased | `{"memories": [{"at": "2026-11-13T10:04:00Z", "text": "Conversation on 2026-11-13: Customer asked to dispute a Nov 1 CloudNest Storage $9.99 charge (T-3002), saying the subscription was cancelled in Oc` |
| PASS | semantic | r4: no fact was recreated | `{}` |
| **FAIL** | guard | r4: the erased trip is still in no memory store | `{"Reykjavik": ["lg_store.db", "lg_checkpoints.db-wal"], "krona": ["lg_store.db", "lg_checkpoints.db-wal"]}` |
