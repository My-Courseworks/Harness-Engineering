# adk · adversarial · run 2 · g21-erase-pending-case-followup

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## epc-s1  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Priya here, card ending 4427, ZIP 94107. Please dispute the October 28 StreamMax charge; I cancelled the subscription before it.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "StreamMax"})` → `{"transactions": [{"transaction_id": "T-1001", "posted_on": "2026-09-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-1002", "posted_on": "2026-10-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription …`
- `file_dispute({"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the StreamMax subscription before the October 28 charge."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-31331cd4", "due": "2026-11-19", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Done - dispute filed for the October 28 StreamMax charge of $15.99 (T-1002).

- **Case id:** C-5001 - status: under review
- **Follow-up due:** November 19, 2026, sent by secure message in the Kestrel app (no contact channel set; if you add one before then, it goes there instead)

If you find a cancellation confirmation from StreamMax - a reference number or email - send it here and I'll attach it to the case as evidence.

_Episode written:_ Conversation on 2026-11-09: Priya asked to dispute the October 28 StreamMax charge. The customer said she cancelled the subscription before it (not verified). Dispute filed for T-1002 as case C-5001, under review. Follow-up due November 19, 2026 via Kestrel secure message; if contact channel changes before then, it uses the new one. Assistant requested cancellation confirmation to attach as evidence. Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | setup: the case follow-up is due 2026-11-19 | `[{"trigger_at": "2026-11-19T10:00:00Z", "approval": "none", "status": "pending", "resume": {"case_id": "C-5001"}}]` |

## epc-s2  ·  session  ·  priya  ·  2026-11-19T09:50:00Z

**Customer:** Please delete everything you remember about me: my preferences and our past conversations.

- `request_memory_erasure({})` → `{"erased_now": "0 remembered facts, 1 past-conversation summaries, 1 other conversation transcripts, 0 reminders with their notes", "this_conversation": "its transcript is deleted when the conversation ends; nothing more can be stored for the customer in it (a new conversation afterwards starts fresh)", "kept": "dispute cases, transactions and messages already sent are bank records with their own  …`

**Assistant:** Done - I've erased what was stored about you: 1 past-conversation summary, 1 other conversation transcript, and 0 stored facts or reminders (you had no contact channel or travel notice saved).

What's kept: this conversation's transcript, until this conversation ends - then it's deleted too. Dispute cases, transactions and messages already sent remain bank records with their own retention.

Nothing more can be stored for you in this conversation - so if you'd like a reminder or a saved preference, please set it up in a new conversation. Anything else I can help with right now?

## epc-fire-1005  ·  fire_followups  ·  2026-11-19T10:05:00Z

### follow-up session `followup-F-31331cd4-1`

**Scheduler:** [scheduled follow-up F-31331cd4] action=case_status_followup resume={"case_id": "C-5001"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the StreamMax subscription before the October 28 charge.", "status": "under_review", "opened_at": "2026-11-09T10:00:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null, "decision_id": null}]}`
- `notify_customer({"message": "Update on case C-5001 (StreamMax charge of Oct 28): it is still under review and no decision has been made yet. No action is needed from you right now; if you have extra evidence, such as …)` → `{"channel": "secure_message", "message_id": 1, "status": "sent"}`

**Assistant:** I'll check the case status first.
Sent the follow-up: case C-5001 is still under review with no decision yet, and the customer was told to send any extra evidence (like a cancellation confirmation) via the card-care chat. The message went out as a secure message in the Kestrel app, since no contact channel is set.

_outcomes:_ `[{"followup_id": "F-31331cd4", "user_id": "priya", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | the case follow-up, which must still reach her, is delivered on the first attempt | `[{"followup_id": "F-31331cd4", "user_id": "priya", "outcome": "fired_done", "error": null}]` |
| PASS | working | it runs with read tools and notify_customer only, even though the erasure is pending | `["find_transactions", "get_case_status", "list_my_followups", "load_memory", "notify_customer", "report_malformed_tool_call", "search_policy"]` |
| PASS | working | and leaves no transcript | `transcripts with prefix followup-: none` |
| PASS | episodic | and no episode | `0 episodes; purged 0` |

## epc-fire-1010  ·  fire_followups  ·  2026-11-19T10:10:00Z

_outcomes:_ `[]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | exactly one message reached her | `1 messages` |

## epc-maint  ·  maintenance  ·  2026-11-19T11:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | no transcript remains | `0 transcripts: []` |
| PASS | guard | nothing about her dispute is in a memory store (cases and follow-up records are the bank's) | `found nowhere` |
| PASS | episodic | no episode remains | `0 episodes; purged 0` |
| PASS | episodic | no orphan embedding | `vector-index rows with no stored item: 0` |
