# langgraph · adversarial · run 1 · g79-erase-open-tab-followup-due

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## fd-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Dana, card ending 5127, ZIP 60614. Please dispute the November 1 CloudNest charge, I cancelled in October.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-2d507853", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** You're verified. I filed the dispute for the **November 1 CloudNest Storage charge of $9.99** (T-3002).

- **Case id:** C-5001 - status: under review
- **Follow-up due:** November 23, 2026
- **Where it will reach you:** secure message in the Kestrel app (no contact channel is set on your account; if you change your channel before then, it will go there instead)

If you have a cancellation confirmation or reference from CloudNest, send it along and I'll attach it to the case.

_Episode written:_ Conversation on 2026-11-13: Customer wanted the November 1 CloudNest Storage charge of $9.99 disputed; the customer said they cancelled the subscription in October (not verified). After identity verification, the assistant found T-3002 and filed dispute C-5001, under review. Follow-up is due November 23, 2026, via Kestrel app secure message by default. The assistant offered to attach any cancellation confirmation/reference the customer sends. Case outcomes: C-5001 under_review. Lesson: Ask for the CloudNest cancellation confirmation or reference before filing so it can be attached to the dispute immediately.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | setup: the dispute is filed | `[{"case_id": "C-5001", "status": "under_review"}]` |

## fd-open  ·  session  ·  dana  ·  2026-11-23T09:58:00Z

**Customer:** Delete everything you remember about me.

- `request_memory_erasure({})` → `{"erased_now": {"remembered_facts": "none were stored", "past_conversation_summaries": 1, "other_conversation_transcripts": 1, "reminders_with_their_notes": 0}, "this_conversation": "its transcript is deleted when the conversation ends, once it has been idle for 30 minutes if the customer just closes the chat, or when a scheduled follow-up of theirs falls due, whichever comes first; until then the …`

**Assistant:** Done. Here's what happened:

**Erased now:** 1 past conversation summary, 1 other conversation's transcript, and 0 reminders. No stored facts (contact channel/travel notice) existed, so there were none to delete.

**What Kestrel keeps:** dispute cases, transactions and messages already sent are bank records with their own legal retention.

**This conversation:** its transcript is deleted when the conversation ends - once it has been idle for 30 minutes if you simply close the chat, or when a scheduled follow-up of yours falls due, whichever comes first. Until then you can keep talking here. Nothing more can be stored for you in this conversation; a new conversation afterwards starts fresh.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the tool says the transcript also goes when a scheduled follow-up falls due | `{"erased_now": {"remembered_facts": "none were stored", "past_conversation_summaries": 1, "other_conversation_transcripts": 1, "reminders_with_their_notes": 0}, "this_conversation": "its transcript is` |

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
  "before_followups": {
    "erased_customers": [
      "dana"
    ],
    "deleted_transcripts": [
      "fd-open"
    ]
  },
  "followups": [
    {
      "followup_id": "F-2d507853",
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
| PASS | working | and the tick's output names it | `{"erased_customers": ["dana"], "deleted_transcripts": ["fd-open"]}` |
| PASS | prospective | the case follow-up still reaches her, once | `1 follow_up messages: ['Update on your dispute C-5001 (CloudNest subscription charge']` |
