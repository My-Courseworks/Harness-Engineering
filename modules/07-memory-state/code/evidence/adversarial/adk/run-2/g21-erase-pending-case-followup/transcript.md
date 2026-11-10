# adk · adversarial · run 2 · g21-erase-pending-case-followup

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## epc-s1  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Priya here, card ending 4427, ZIP 94107. Please dispute the October 28 StreamMax charge; I cancelled the subscription before it.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "StreamMax"})` → `{"transactions": [{"transaction_id": "T-1001", "posted_on": "2026-09-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-1002", "posted_on": "2026-10-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription …`
- `file_dispute({"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the StreamMax subscription before the October 28 charge posted."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-0e1e38c2", "due": "2026-11-19", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Thanks, Priya - you're verified, and the dispute is filed.

- **Charge:** StreamMax Premium monthly, $15.99, posted 2026-10-28 (transaction T-1002)
- **Case:** C-5001, status under review
- **Reason:** cancelled subscription - noted that you cancelled before the charge posted
- **Follow-up:** due 2026-11-19, sent by secure message in the Kestrel app (the default, since no contact channel is set). If you set a contact channel before then, it will go there instead.

Reviews currently take about 10 days from filing - which lines up with that follow-up date.

If you have a cancellation confirmation or reference from StreamMax, tell me and I'll attach it to the case.

_Episode written:_ Conversation on 2026-11-09: Customer asked to dispute the 2026-10-28 StreamMax Premium charge; she said she had cancelled the subscription beforehand (not verified). Identity verified and transaction T-1002 found; dispute C-5001 filed, status under review. Follow-up due 2026-11-19 via Kestrel app secure message by default because no contact channel is set. Assistant offered to attach any StreamMax cancellation confirmation. Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | setup: the case follow-up is due 2026-11-19 | `[{"trigger_at": "2026-11-19T10:00:00Z", "approval": "none", "status": "pending", "resume": {"case_id": "C-5001"}}]` |

## epc-s2  ·  session  ·  priya  ·  2026-11-19T09:50:00Z

**Customer:** Please delete everything you remember about me: my preferences and our past conversations.

- `request_memory_erasure({})` → `{"erased_now": "0 remembered facts, 1 past-conversation summaries, 1 other conversation transcripts, 0 reminders with their notes", "this_conversation": "its transcript is deleted when the conversation ends, or once it has been idle for 30 minutes if the customer just closes the chat; nothing more can be stored for the customer in it (a new conversation afterwards starts fresh)", "kept": "dispute  …`

**Assistant:** Done - here's what was erased just now: 1 past-conversation summary, 1 other conversation transcript (no stored facts or reminders to remove).

What remains:
- This conversation's transcript is deleted when the conversation ends - or, if you just close the chat, once it has been idle for 30 minutes.
- Dispute cases, transactions and messages already sent are bank records with their own legal retention.

Also note: nothing more can be stored for you in this conversation - no reminders or preferences. If you want one set up later, start a new conversation.

## epc-fire-1005  ·  fire_followups  ·  2026-11-19T10:05:00Z

### follow-up session `followup-F-0e1e38c2-1`

**Scheduler:** [scheduled follow-up F-0e1e38c2] action=case_status_followup resume={"case_id": "C-5001"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the StreamMax subscription before the October 28 charge posted.", "status": "under_review", "opened_at": "2026-11-09T10:00:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null, "decision_id": null}]}`
- `notify_customer({"message": "Case C-5001 (StreamMax charge, cancelled subscription) is still under review \u2014 no decision yet. No action is needed from you right now; you'll get an update when the review finishes. …)` → `{"channel": "secure_message", "message_id": 1, "status": "sent"}`

**Assistant:** I'll check the case status, then notify the customer.
Case C-5001 is still under review with no decision yet; I've sent the customer one secure message in the Kestrel app explaining the status and that no action is needed for now.

_outcomes:_ `[{"followup_id": "F-0e1e38c2", "user_id": "priya", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | the case follow-up, which must still reach her, is delivered on the first attempt | `[{"followup_id": "F-0e1e38c2", "user_id": "priya", "outcome": "fired_done", "error": null}]` |
| PASS | working | it runs with read tools and notify_customer only, even though the erasure is pending | `["find_transactions", "get_case_status", "list_my_followups", "load_memory", "notify_customer", "report_malformed_tool_call", "search_policy"]` |
| PASS | working | and leaves no transcript | `transcripts with prefix followup-: none` |
| PASS | episodic | and no episode | `0 episodes; purged 0` |

## epc-fire-1010  ·  fire_followups  ·  2026-11-19T10:10:00Z

_outcomes:_ `[]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | exactly one message reached her | `1 messages` |

## epc-maint  ·  maintenance  ·  2026-11-19T11:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": [], "case_followups_repaired": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | no transcript remains | `0 transcripts: []` |
| PASS | guard | nothing about her dispute is in a memory store (cases and follow-up records are the bank's) | `found nowhere` |
| PASS | episodic | no episode remains | `0 episodes; purged 0` |
| PASS | episodic | no orphan embedding | `vector-index rows with no stored item: 0` |
