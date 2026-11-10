# langgraph · adversarial · run 1 · g79-erase-open-tab-followup-due

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## fd-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Dana, card ending 5127, ZIP 60614. Please dispute the November 1 CloudNest charge, I cancelled in October.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-79db240e", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Verified - and I've filed the dispute.

- **Case:** C-5001
- **Charge:** CloudNest Storage, $9.99, posted 2026-11-01 (transaction T-3002)
- **Reason:** subscription cancelled in October
- **Status:** under review (currently about 10 days)
- **Follow-up:** due 2026-11-23, sent by secure message in the Kestrel app since no contact channel is set

If you have a cancellation confirmation or reference from CloudNest, send it over and I'll attach it to the case.

_Episode written:_ Conversation on 2026-11-13: The customer wanted the November 1 CloudNest Storage charge disputed; the customer said they cancelled the subscription in October (not verified). The assistant verified identity, filed dispute for transaction T-3002 as case C-5001 (under review), and noted follow-up due 2026-11-23 via secure message in the Kestrel app because no contact channel is set; the assistant requested cancellation confirmation. Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | setup: the dispute is filed | `[{"case_id": "C-5001", "status": "under_review"}]` |

## fd-open  ·  session  ·  dana  ·  2026-11-23T09:58:00Z

**Customer:** Delete everything you remember about me.

- `request_memory_erasure({})` → `{"erased_now": "0 remembered facts, 1 past-conversation summaries, 1 other conversation transcripts, 0 reminders with their notes", "this_conversation": "its transcript is deleted when the conversation ends, or once it has been idle for 30 minutes if the customer just closes the chat; nothing more can be stored for the customer in it (a new conversation afterwards starts fresh)", "kept": "dispute  …`

**Assistant:** Done. I erased:

- 0 stored facts (you had no contact channel or travel notice on file)
- 1 past-conversation summary
- 1 other conversation's transcript
- 0 reminders

This conversation's transcript is deleted when the conversation ends - or after 30 minutes idle if you just close the chat. Nothing more can be stored for you in this conversation; a new conversation starts fresh.

What Kestrel still keeps: dispute cases, transactions and messages already sent are bank records with their own legal retention.

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
    "case_followups_repaired": [],
    "purged_episodes": [],
    "deleted_transcripts": []
  },
  "followups": [
    {
      "followup_id": "F-79db240e",
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
| PASS | prospective | the case follow-up still reaches her, once | `1 follow_up messages: ['Your dispute C-5001 (CloudNest subscription, canceled in Oct']` |
