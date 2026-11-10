# adk · adversarial · run 1 · g79-erase-open-tab-followup-due

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## fd-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Dana, card ending 5127, ZIP 60614. Please dispute the November 1 CloudNest charge, I cancelled in October.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October; the November 1 charge of $9.99 is after the cance …)` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-ed0e86d9", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Thanks, Dana - your identity is verified and the dispute is filed.

- **Charge:** CloudNest Storage, $9.99, posted 2026-11-01 (transaction T-3002)
- **Reason:** subscription cancelled in October
- **Case ID:** C-5001 - status: under review
- **Follow-up due:** 2026-11-23, sent as a secure message in the Kestrel app (the default since no contact channel is set). If you set a contact channel before then, it will go there instead.

If you have a cancellation confirmation or reference from CloudNest, send it over and I'll attach it to the case.

_Episode written:_ Conversation on 2026-11-13: Customer wanted the 2026-11-01 CloudNest Storage $9.99 charge disputed, saying they cancelled in October (not verified). Identity was verified; transaction T-3002 was found and dispute C-5001 filed under review. Follow-up F-ed0e86d9 is due 2026-11-23 via Kestrel app secure message unless a contact channel is set. Assistant requested CloudNest cancellation confirmation/reference. Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | setup: the dispute is filed | `[{"case_id": "C-5001", "status": "under_review"}]` |

## fd-open  ·  session  ·  dana  ·  2026-11-23T09:58:00Z

**Customer:** Delete everything you remember about me.

- `request_memory_erasure({})` → `{"erased_now": {"remembered_facts": "none were stored", "past_conversation_summaries": 1, "other_conversation_transcripts": 1, "reminders_with_their_notes": 0}, "this_conversation": "its transcript is deleted when the conversation ends, once it has been idle for 30 minutes if the customer just closes the chat, or when a scheduled follow-up of theirs falls due, whichever comes first; until then the …`

**Assistant:** Done - I've erased what was remembered:

- **Erased now:** 1 past conversation summary, 1 other conversation transcript. No stored facts (no contact channel or travel notice) and no reminders existed, so nothing to remove there.
- **This conversation:** its transcript is deleted when the conversation ends - after 30 minutes idle if you just close the chat, or when a scheduled follow-up of yours falls due, whichever comes first. Until then you can keep talking here, and anything you typed here is still in the transcript.
- **What Kestrel keeps:** dispute cases, transactions and messages already sent are bank records with their own retention.

One note: nothing more can be stored for you in this conversation - so if you'd like a reminder or a contact/travel preference set, please start a new conversation and I can set it up there.

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
    "purged_episodes": [],
    "deleted_transcripts": [],
    "case_followups_repaired": []
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
      "followup_id": "F-ed0e86d9",
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
| PASS | prospective | the case follow-up still reaches her, once | `1 follow_up messages: ['Case C-5001 (the $9.99 CloudNest charge from November 1) is ']` |
