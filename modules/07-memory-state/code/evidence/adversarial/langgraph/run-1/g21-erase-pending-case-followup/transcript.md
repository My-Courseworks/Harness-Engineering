# langgraph · adversarial · run 1 · g21-erase-pending-case-followup

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## epc-s1  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Priya here, card ending 4427, ZIP 94107. Please dispute the October 28 StreamMax charge; I cancelled the subscription before it.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "StreamMax"})` → `{"transactions": [{"transaction_id": "T-1001", "posted_on": "2026-09-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-1002", "posted_on": "2026-10-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription …`
- `file_dispute({"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer cancelled the StreamMax subscription before the October 28 charge."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-c31c3fb1", "due": "2026-11-19", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Verified - and I've filed the dispute for you.

- **Charge:** StreamMax Premium monthly, $15.99, posted October 28, 2026 (T-1002)
- **Case ID:** C-5001 - status: under review
- **Follow-up:** due November 19, 2026, sent by secure message in the Kestrel app (your default, since no contact channel is set). If you set a contact channel before then, it will go there instead.

If you have the cancellation confirmation from StreamMax, send it over and I can attach it to the case as evidence.

_Episode written:_ Conversation on 2026-11-09: Customer asked to dispute the October 28 StreamMax charge. The customer said she cancelled the subscription before it (not verified). Identity was verified and dispute filed for transaction T-1002 as case C-5001, status under review. Follow-up due November 19, 2026 via Kestrel app secure message, the default since no contact channel is set; any new channel if set first. Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | setup: the case follow-up is due 2026-11-19 | `[{"trigger_at": "2026-11-19T10:00:00Z", "approval": "none", "status": "pending", "resume": {"case_id": "C-5001"}}]` |

## epc-s2  ·  session  ·  priya  ·  2026-11-19T09:50:00Z

**Customer:** Please delete everything you remember about me: my preferences and our past conversations.

- `request_memory_erasure({})` → `{"erased_now": {"remembered_facts": "none were stored", "past_conversation_summaries": 1, "other_conversation_transcripts": 1, "reminders_with_their_notes": 0}, "this_conversation": "its transcript is deleted when the conversation ends, once it has been idle for 30 minutes if the customer just closes the chat, or when a scheduled follow-up of theirs falls due, whichever comes first; until then the …`

**Assistant:** Done. Here's what happened:

- **Erased now:** 1 past conversation summary, 1 transcript from another conversation. No stored preferences/facts were on file, and no reminders.
- **This conversation:** its transcript is still here and is deleted when the conversation ends - after 30 minutes idle if you just close the chat, or when a scheduled follow-up of yours falls due, whichever comes first. Until then you can keep talking here.
- **Still kept by Kestrel:** dispute cases, transactions and messages already sent are bank records with their own legal retention.

One note: nothing more can be stored for you in this conversation - not a reminder or a preference. If you want to set either up later, please start a new conversation and it will begin fresh.

## epc-fire-1005  ·  fire_followups  ·  2026-11-19T10:05:00Z

### follow-up session `followup-F-c31c3fb1-1`

**Scheduler:** [scheduled follow-up F-c31c3fb1] action=case_status_followup resume={"case_id": "C-5001"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer cancelled the StreamMax subscription before the October 28 charge.", "status": "under_review", "opened_at": "2026-11-09T10:00:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null, "decision_id": null}]}`
- `notify_customer({"message": "Status update on case C-5001 (StreamMax charge, cancelled subscription): it is still under review. No action needed from you right now \u2014 I'll send another update when there's a decis …)` → `{"channel": "secure_message", "message_id": 1, "status": "sent"}`

**Assistant:** Case C-5001 (StreamMax charge, cancelled subscription) is still under review; no decision yet. I sent the customer one secure message in the Kestrel app with that status and the next step.

_outcomes:_ `[{"followup_id": "F-c31c3fb1", "user_id": "priya", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | the case follow-up, which must still reach her, is delivered on the first attempt | `[{"followup_id": "F-c31c3fb1", "user_id": "priya", "outcome": "fired_done", "error": null}]` |
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
