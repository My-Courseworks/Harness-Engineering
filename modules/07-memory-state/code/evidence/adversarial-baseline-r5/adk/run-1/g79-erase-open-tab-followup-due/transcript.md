# adk · adversarial · run 1 · g79-erase-open-tab-followup-due

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## fd-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Dana, card ending 5127, ZIP 60614. Please dispute the November 1 CloudNest charge, I cancelled in October.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-54990765", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Thanks, Dana - you're verified, and the dispute is filed.

- **Charge:** CloudNest Storage, $9.99, posted 2026-11-01 (Nov 1) - transaction T-3002
- **Reason:** cancelled subscription
- **Case id:** C-5001 - status: under review
- **Follow-up:** due 2026-11-23, sent by secure message in the Kestrel app (the default, since no contact channel is set). If you set a contact channel before then, it will go there instead.

Disputes are currently reviewed in about 10 days. If you have a cancellation confirmation or reference from CloudNest, send it over and I can attach it to the case.

_Episode written:_ Conversation on 2026-11-13: Dana wanted the 2026-11-01 CloudNest Storage $9.99 charge (T-3002) disputed; the customer said they cancelled in October (not verified). The dispute was filed under case C-5001, status under_review. Follow-up F-54990765 is due 2026-11-23 by Kestrel app secure message, the default since no contact channel is set. Reviews take about 10 days. Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | setup: the dispute is filed | `[{"case_id": "C-5001", "status": "under_review"}]` |

## fd-open  ·  session  ·  dana  ·  2026-11-23T09:58:00Z

**Customer:** Delete everything you remember about me.

- `request_memory_erasure({})` → `{"erased_now": "0 remembered facts, 1 past-conversation summaries, 1 other conversation transcripts, 0 reminders with their notes", "this_conversation": "its transcript is deleted when the conversation ends, or once it has been idle for 30 minutes if the customer just closes the chat; nothing more can be stored for the customer in it (a new conversation afterwards starts fresh)", "kept": "dispute  …`

**Assistant:** Done - erased now: 0 saved facts, 1 past-conversation summary, 1 other conversation transcript, and 0 reminders.

What Kestrel still keeps: dispute cases, transactions and messages already sent are bank records with their own legal retention. This conversation's transcript is deleted when the conversation ends, or once it has been idle for 30 minutes if you just close the chat.

One thing to know: nothing more can be stored for you in this conversation - not a reminder or a preference. If you want one of those later, set it up in a new conversation.

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | the tool says the transcript also goes when a scheduled follow-up falls due | `{"erased_now": "0 remembered facts, 1 past-conversation summaries, 1 other conversation transcripts, 0 reminders with their notes", "this_conversation": "its transcript is deleted when the conversatio` |

## fd-tick  ·  tick  ·  2026-11-23T10:05:00Z

_CLI exit code 0; stdout tail:_

```
{
  "now": "2026-11-23T10:05:00Z",
  "maintenance": {
    "erased_customers": [],
    "expired_facts": [],
    "closed_idle_sessions": [],
    "purged_episodes": [],
    "deleted_transcripts": [],
    "case_followups_repaired": []
  },
  "followups": [
    {
      "followup_id": "F-54990765",
      "user_id": "dana",
      "outcome": "fired_done",
      "error": null
    }
  ]
}
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | a follow-up of hers is due: the scheduler finishes her erasure before it fires, and the transcript goes | `transcripts of dana: []` |
| **FAIL** | working | and the tick's output names it | `{"erased_customers": [], "deleted_transcripts": []}` |
| PASS | prospective | the case follow-up still reaches her, once | `1 follow_up messages: ['Update on your dispute case C-5001 (CloudNest cancelled subs']` |
