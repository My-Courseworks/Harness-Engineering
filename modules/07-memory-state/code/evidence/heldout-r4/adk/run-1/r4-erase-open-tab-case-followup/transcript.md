# adk · heldout-r4 · run 1 · r4-erase-open-tab-case-followup

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r4e1-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, Dana here, card ending 5127, ZIP 60614. CloudNest Storage charged me $9.99 on November 1 even though I cancelled in October, please dispute it. Also, I'm in Reykjavik until November 28, so expect charges in krona.

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states she cancelled the CloudNest Storage subscription in October; the $9.99 charge on 2026-11-01 is after  …)` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-3a3301dc", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`
- `remember_customer_fact({"key": "travel_notice", "value": "Reykjavik", "valid_until": "2026-11-28"})` → `{"stored": {"travel_notice": {"value": "Reykjavik", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-11-28", "expires_at": "2026-11-29T00:00:00Z"}}, "replaced": null}`

**Assistant:** Done, Dana.

**Dispute filed** - CloudNest Storage, $9.99, posted 2026-11-01 (transaction T-3002), reason: cancelled subscription.
- Case id: **C-5001** - status: under review (currently about 10 days)
- Follow-up due **2026-11-23**, sent by **secure message in the Kestrel app** (no contact channel is set on your account; if you add one before then, it'll go there instead)

**Travel notice saved** - Reykjavik until 2026-11-28, so krona charges from there shouldn't trip fraud checks.

If you have a cancellation confirmation or reference number from CloudNest, send it over and I'll attach it to case C-5001.

**Customer:** Yes, go ahead and file it.

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states she cancelled the CloudNest Storage subscription in October; the $9.99 charge on 2026-11-01 is after cancellation.", "status": "under_review", "opened_at": "2026-11-13T10:00:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null, "decisi …`

**Assistant:** It's already filed - no need to do it again. Case **C-5001** is open for the $9.99 CloudNest Storage charge from 2026-11-01, currently **under review**.

- Follow-up due **2026-11-23** via **secure message in the Kestrel app**

If you'd like, send me the CloudNest cancellation confirmation or reference number and I'll attach it to the case as extra evidence.

_Episode written:_ Conversation on 2026-11-13: Customer wanted the $9.99 CloudNest Storage charge posted 2026-11-01 disputed; the customer said she cancelled in October (not verified). Assistant verified identity, filed dispute for transaction T-3002 as case C-5001 (under review), with follow-up due 2026-11-23 by secure message in the Kestrel app, and saved a Reykjavik travel notice valid until 2026-11-28. Assistant offered to attach cancellation confirmation if provided. Case outcomes: C-5001 under_review. Lesson: Next time, make clear that the dispute is already filed before asking for supporting evidence, so the customer does not think another filing action is needed.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | r4: the dispute is filed on T-3002 | `[{"case_id": "C-5001", "status": "under_review"}]` |
| PASS | prospective | r4: its follow-up is due 2026-11-23, no approval | `[{"trigger_at": "2026-11-23T10:00:00Z", "approval": "none", "status": "pending", "resume": {"case_id": "C-5001"}}]` |
| PASS | semantic | r4: the travel notice is stored until 2026-11-28 | `{"value": "Reykjavik", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-11-28", "expires_at": "2026-11-29T00:00:00Z"}` |

## r4e1-s2  ·  session  ·  dana  ·  2026-11-23T09:55:00Z

**Customer:** I've changed my mind about all of this. Erase everything you remember about me and every conversation we've had.

**Assistant:** I can do that. First I need to verify you: please type your card's last 4 digits and your billing ZIP code.

Also, since a card number could be masked once it reaches me, please don't send the full card number, security code or expiry date - just the last 4 digits and ZIP.

## r4e1-fire-1  ·  fire_followups  ·  2026-11-23T10:06:00Z

### follow-up session `followup-F-3a3301dc-1`

**Scheduler:** [scheduled follow-up F-3a3301dc] action=case_status_followup resume={"case_id": "C-5001"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states she cancelled the CloudNest Storage subscription in October; the $9.99 charge on 2026-11-01 is after cancellation.", "status": "under_review", "opened_at": "2026-11-13T10:00:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null, "decisi …`
- `notify_customer({"message": "Update on your dispute C-5001 (CloudNest Storage, $9.99 charge on 2026-11-01): it is still under review \u2014 no decision yet. Disputes are currently reviewed in about 10 days, so the ne …)` → `{"channel": "secure_message", "message_id": 1, "status": "sent"}`

**Assistant:** Case C-5001 is still under review, so I sent the customer a secure-message update noting that and pointing them to the card-care chat if they have more evidence.

_Episode written:_ Scheduled follow-up on 2026-11-23 (customer not present): Customer disputed a $9.99 CloudNest Storage charge on 2026-11-01 (case C-5001, txn T-3002), saying she cancelled the subscription in October (not verified). Assistant checked status: under_review; sent secure message 1 saying no decision yet, reviews take about 10 days, next update soon, and no action needed unless more evidence is sent via card-care chat. Case outcomes: C-5001 under_review. Lesson: none

_outcomes:_ `[{"followup_id": "F-3a3301dc", "user_id": "dana", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | semantic | r4: an erasure pending at fire time still runs: no fact remains | `{"travel_notice": {"value": "Reykjavik", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-11-28", "expires_at": "2026-11-29T00:00:00Z"}}` |
| **FAIL** | episodic | r4: no episode remains, and the fired follow-up wrote none | `2 episodes; purged 0` |
| **FAIL** | working | r4: no transcript remains: not the open tab, not the follow-up's own session | `3 transcripts: ['followup-F-3a3301dc-1', 'r4e1-s1', 'r4e1-s2']` |
| PASS | working | r4: the follow-up session is unattended even though an erasure ran around it | `["find_transactions", "get_case_status", "list_my_followups", "load_memory", "notify_customer", "report_malformed_tool_call", "search_policy"]` |
| **FAIL** | guard | r4: nothing she said is in any memory store | `{"Reykjavik": ["adk_episodes.db", "adk_sessions.db"], "krona": ["adk_sessions.db"]}` |

## r4e1-fire-2  ·  fire_followups  ·  2026-11-23T10:20:00Z

_outcomes:_ `[]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r4: the case follow-up still reaches the erased customer, exactly once | `1 messages` |
| PASS | guard | r4: no outbound message carries a masking token or a masked identifier | `3 outbound messages and episodes clean` |
| **FAIL** | episodic | r4: still no episode after the retry window | `2 episodes; purged 0` |
| **FAIL** | working | r4: still no transcript after the retry window | `3 transcripts: ['followup-F-3a3301dc-1', 'r4e1-s1', 'r4e1-s2']` |

## r4e1-s3  ·  session  ·  dana  ·  2026-11-30T10:00:00Z

**Customer:** Hello again. What do you have on file about me, and do you remember where I said I'd be travelling?

- `load_memory({"query": "travel notice destination trip return date"})` → `{"result": "memories=[MemoryEntry(content=Content(\n  parts=[\n    Part(\n      text='Conversation on 2026-11-13: Customer wanted the $9.99 CloudNest Storage charge posted 2026-11-01 disputed; the customer said she cancelled in October (not verified). Assistant verified identity, filed dispute for transaction T-3002 as case C-5001 (under review), with follow-up due 2026-11-23 by secure message in  …`

**Assistant:** I'll check both the current profile and any earlier conversation.
Here's what's on file right now:

- **Contact channel:** none set - so any follow-ups or reminders go by secure message in the Kestrel app (the default).
- **Travel notice:** none on file.

On the earlier conversation: yes, I have a record from 13 November where you had me save a **Reykjavik** travel notice, valid until **28 November 2026**. That has now expired, which is why nothing is showing as active today. If you have another trip coming up, tell me the destination and return date and I'll set a new one.

Also from that conversation: dispute **C-5001** for the $9.99 CloudNest Storage charge (transaction T-3002) was filed and is still under review. Say the word if you'd like me to check its current status.

_Episode written:_ Conversation on 2026-11-30: Customer asked what was on file and where she had said she was travelling. Assistant checked profile/memory: no active travel notice; an earlier Reykjavik notice had expired 2026-11-28. Earlier, dispute C-5001 for transaction T-3002 ($9.99 CloudNest Storage) was filed and remains under review, with follow-up due 2026-11-23 by Kestrel app secure message. Customer said she cancelled in October (not verified). Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | episodic | r4: nothing erased comes back in a later chat | `I'll check both the current profile and any earlier conversation. Here's what's on file right now:  - **Contact channel:** none set - so any follow-ups or reminders go by secure message in the Kestrel app (the default).  …` |
| **FAIL** | episodic | r4: recall, if used, returns nothing erased | `{"result": "memories=[MemoryEntry(content=Content(\n  parts=[\n    Part(\n      text='Conversation on 2026-11-13: Customer wanted the $9.99 CloudNest Storage charge posted 2026-11-01 disputed; the cus` |
| PASS | semantic | r4: no fact was recreated | `{}` |
| **FAIL** | guard | r4: the erased trip is still in no memory store | `{"Reykjavik": ["adk_episodes.db", "adk_sessions.db"], "krona": ["adk_sessions.db"]}` |
