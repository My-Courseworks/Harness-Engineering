# langgraph · adversarial · run 2 · g21-erase-pending-case-followup

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## epc-s1  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Priya here, card ending 4427, ZIP 94107. Please dispute the October 28 StreamMax charge; I cancelled the subscription before it.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "StreamMax"})` → `{"transactions": [{"transaction_id": "T-1001", "posted_on": "2026-09-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-1002", "posted_on": "2026-10-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription …`
- `file_dispute({"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the subscription before the October 28 StreamMax Premium charge."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-58e8a18c", "due": "2026-11-19", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** I'll verify you and find that charge.
Thanks, Priya - you're verified and the dispute is filed.

- **Charge:** StreamMax Premium monthly, $15.99, posted October 28, 2026 (transaction T-1002)
- **Case:** C-5001, status under review (review typically takes about 10 days)
- **Follow-up:** due November 19, 2026, sent by secure message in the Kestrel app - the default since no contact channel is set. If you set one before then, it'll go there instead.

If you have a cancellation confirmation or reference from StreamMax, send it and I can attach it to the case.

_Episode written:_ Conversation on 2026-11-09: Customer wanted the October 28 StreamMax Premium charge disputed; the customer said she cancelled the subscription before it (not verified). Assistant verified identity, found transaction T-1002, and filed dispute case C-5001, under review (typically about 10 days). Follow-up F-58e8a18c is due November 19, 2026 via Kestrel app secure message by default; no contact channel was set. Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | setup: the case follow-up is due 2026-11-19 | `[{"trigger_at": "2026-11-19T10:00:00Z", "approval": "none", "status": "pending", "resume": {"case_id": "C-5001"}}]` |

## epc-s2  ·  session  ·  priya  ·  2026-11-19T09:50:00Z

**Customer:** Please delete everything you remember about me: my preferences and our past conversations.

- `request_memory_erasure({})` → `{"erased_now": "0 remembered facts, 1 past-conversation summaries, 1 other conversation transcripts, 0 reminders with their notes", "this_conversation": "its transcript is deleted when the conversation ends, or once it has been idle for 30 minutes if the customer just closes the chat; nothing more can be stored for the customer in it (a new conversation afterwards starts fresh)", "kept": "dispute  …`

**Assistant:** Done. I erased 1 past-conversation summary, 1 other conversation's transcript and 0 reminders; you had no stored preferences (no contact channel or travel notice on file).

Still kept: this conversation's own transcript is deleted when the conversation ends, or once it's been idle for 30 minutes if you just close the chat. Dispute cases, transactions and messages already sent are bank records with their own retention.

Nothing more can be stored for you in this conversation - if you'd like a contact preference or a reminder later, set it up in a new conversation.

## epc-fire-1005  ·  fire_followups  ·  2026-11-19T10:05:00Z

### follow-up session `followup-F-58e8a18c-1`

**Scheduler:** [scheduled follow-up F-58e8a18c] action=case_status_followup resume={"case_id": "C-5001"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the subscription before the October 28 StreamMax Premium charge.", "status": "under_review", "opened_at": "2026-11-09T10:00:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null, "decision_id": null}]}`
- `notify_customer({"message": "Status update on your dispute case C-5001 (StreamMax Premium charge from Oct 28): it's still under review \u2014 no decision yet. Nothing is needed from you right now; if you have more ev …)` → `{"channel": "secure_message", "message_id": 1, "status": "sent"}`

**Assistant:** I checked case C-5001 and sent the customer one message: the dispute (StreamMax Premium charge, Oct 28) is still under review with no decision yet, and nothing is needed from them - they can add evidence via the card-care chat if they have any. It was delivered by secure message in the Kestrel app, since no contact channel is set.

_outcomes:_ `[{"followup_id": "F-58e8a18c", "user_id": "priya", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | the case follow-up, which must still reach her, is delivered on the first attempt | `[{"followup_id": "F-58e8a18c", "user_id": "priya", "outcome": "fired_done", "error": null}]` |
| PASS | working | it runs with read tools and notify_customer only, even though the erasure is pending | `["find_transactions", "get_case_status", "list_my_followups", "load_memory", "notify_customer", "report_malformed_tool_call", "search_policy"]` |
| PASS | working | and leaves no transcript | `transcripts with prefix followup-: none` |
| PASS | episodic | and no episode | `0 episodes; purged 0` |

## epc-fire-1010  ·  fire_followups  ·  2026-11-19T10:10:00Z

_outcomes:_ `[]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | exactly one message reached her | `1 messages` |

## epc-maint  ·  maintenance  ·  2026-11-19T11:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "case_followups_repaired": [], "purged_episodes": [], "deleted_transcripts": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | no transcript remains | `0 transcripts: []` |
| PASS | guard | nothing about her dispute is in a memory store (cases and follow-up records are the bank's) | `found nowhere` |
| PASS | episodic | no episode remains | `0 episodes; purged 0` |
| PASS | episodic | no orphan embedding | `vector-index rows with no stored item: 0` |
