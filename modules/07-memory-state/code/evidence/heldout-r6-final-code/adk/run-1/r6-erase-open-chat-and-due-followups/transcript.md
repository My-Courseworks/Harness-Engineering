# adk · heldout-r6 · run 1 · r6-erase-open-chat-and-due-followups

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r6h-priya-dispute  ·  session  ·  priya  ·  2026-11-10T09:00:00Z

**Customer:** Priya here, card ending 4427, ZIP 94107. Please dispute the October 28 StreamMax charge of $15.99: I cancelled the subscription before it was taken.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "StreamMax"})` → `{"transactions": [{"transaction_id": "T-1001", "posted_on": "2026-09-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-1002", "posted_on": "2026-10-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription …`
- `file_dispute({"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer states she cancelled the subscription before the charge was taken."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-37cf8a91", "due": "2026-11-20", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** I've filed the dispute for the October 28 StreamMax charge of $15.99 (T-1002).

- **Case id:** C-5001
- **Status:** under review
- **Follow-up due:** November 20, 2026 - it will arrive as a secure message in the Kestrel app, since no contact channel is set on your account (if you set one before then, it will go there instead)

Disputes are currently reviewed in about 10 days. If you find a cancellation confirmation or reference from StreamMax, send it over and I'll attach it to the case.

**Customer:** Yes, please file it.

- `get_case_status({"case_id": "C-5001"})` → `{"cases": [{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer states she cancelled the subscription before the charge was taken.", "status": "under_review", "opened_at": "2026-11-10T09:00:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null, "decision_id": null}]}`

**Assistant:** It's already filed - case C-5001, for the October 28 StreamMax charge of $15.99, currently under review. The follow-up is due November 20 and will arrive as a secure message in the Kestrel app.

If you have a StreamMax cancellation confirmation or reference, send it and I'll attach it to the case as extra evidence.

_Episode written:_ Conversation on 2026-11-10: Priya wanted the October 28 StreamMax charge of $15.99 (T-1002) disputed. The customer said she cancelled the subscription before the charge (not verified). The dispute was filed as case C-5001, under review. Follow-up F-37cf8a91 is due November 20, 2026, via Kestrel app secure message unless she changes her contact channel. Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r6 B: her follow-up is due 2026-11-20 | `[{"trigger_at": "2026-11-20T09:00:00Z", "approval": "none", "status": "pending", "resume": {"case_id": "C-5001"}}]` |

## r6h-dana-dispute  ·  session  ·  dana  ·  2026-11-10T09:40:00Z

**Customer:** Dana, card ending 5127, ZIP 60614. CloudNest Storage charged me $9.99 on November 1 after I cancelled in October. Please dispute it.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest Storage subscription in October; the $9.99 charge posted 1 November 2026 i …)` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-d2825ac5", "due": "2026-11-20", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Done - you're verified and the dispute is filed.

- **Charge disputed:** CloudNest Storage, $9.99, posted 1 Nov 2026 (transaction T-3002)
- **Reason:** cancelled subscription
- **Case id:** C-5002 - status: under review
- **Follow-up due:** 20 Nov 2026, sent by secure message in the Kestrel app (no contact channel is set). If you set a contact channel before then, it will go there instead.

If you have anything from CloudNest showing the cancellation (a confirmation email or reference number), send it here and I can attach it to the case.

**Customer:** Yes, go ahead and file it.

**Assistant:** The dispute is already filed - no need to file again. Case **C-5002** covers the CloudNest Storage $9.99 charge from 1 Nov 2026, and it's under review now. The follow-up is due **20 Nov 2026** by secure message in the Kestrel app.

If you meant you have cancellation proof to add to that case, just paste or describe it here and I'll attach it.

_Episode written:_ Conversation on 2026-11-10: Customer Dana wanted the $9.99 CloudNest Storage charge posted 1 Nov 2026 disputed; the customer said they cancelled in October (not verified). Dispute C-5002 was filed for transaction T-3002 as cancelled_subscription. Follow-up due 20 Nov 2026 via secure message in the Kestrel app; no contact channel is set, so an updated channel would be used. Case outcomes: C-5002 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r6 B: her follow-up is due 2026-11-20, forty minutes after the other | `[{"trigger_at": "2026-11-20T09:40:00Z", "approval": "none", "status": "pending", "resume": {"case_id": "C-5002"}}]` |

## r6h-dana-erase  ·  session  ·  dana  ·  2026-11-20T08:56:00Z

**Customer:** Dana again. Before anything else: my brother Tobias sometimes answers this chat for me, so don't be surprised by his typing.

- `load_memory({"query": "Dana previous conversation"})` → `{"result": "memories=[MemoryEntry(content=Content(\n  parts=[\n    Part(\n      text='Conversation on 2026-11-10: Customer Dana wanted the $9.99 CloudNest Storage charge posted 1 Nov 2026 disputed; the customer said they cancelled in October (not verified). Dispute C-5002 was filed for transaction T-3002 as cancelled_subscription. Follow-up due 20 Nov 2026 via secure message in the Kestrel app; no …`

**Assistant:** Noted. One thing I can't do: I can only treat whoever is typing as you and act on this logged-in session, so I can't keep a separate record for your brother - and I can't store that note either, since I only save contact-channel and travel-notice facts.

I do have a record of our 10 Nov conversation (the CloudNest Storage dispute, case C-5002). What can I help with today?

**Customer:** Actually, I want a clean slate. Erase everything you remember about me.

- `request_memory_erasure({})` → `{"erased_now": {"remembered_facts": "none were stored", "past_conversation_summaries": 1, "other_conversation_transcripts": 1, "reminders_with_their_notes": 0}, "this_conversation": "its transcript is deleted when the conversation ends, once it has been idle for 30 minutes if the customer just closes the chat, or when a scheduled follow-up of theirs falls due, whichever comes first; until then the …`

**Assistant:** Done. Erased just now:

- Past conversation summaries: 1 (the 10 Nov conversation about the CloudNest dispute)
- Other conversation transcripts: 1
- Stored facts: none were stored
- Reminders: none

What Kestrel still keeps: dispute cases, transactions and messages already sent are bank records with their own retention - so case C-5002 remains on file as a case record.

This conversation's own transcript is deleted when the conversation ends: once it has been idle for 30 minutes if you just close the chat, or when a scheduled follow-up of yours falls due, whichever comes first. Until then you can keep talking here, and nothing more can be stored for you in this conversation - so if you want a reminder or a contact preference set up, that needs a new conversation.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | r6 B: the erasure is requested | `[{}]` |

## r6h-tick-other-due  ·  tick  ·  2026-11-20T09:05:00Z

_CLI exit code 0; stdout tail:_

```
{
  "now": "2026-11-20T09:05:00Z",
  "maintenance": {
    "erased_customers": [],
    "expired_facts": [],
    "closed_idle_sessions": [],
    "purged_episodes": [],
    "deleted_transcripts": [],
    "case_followups_repaired": []
  },
  "before_followups": {
    "erased_customers": [],
    "deleted_transcripts": []
  },
  "followups": [
    {
      "followup_id": "F-37cf8a91",
      "user_id": "priya",
      "outcome": "fired_done",
      "error": null
    }
  ]
}
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r6 B2: (this tick fired the other customer's follow-up) | `1 messages` |
| PASS | working | r6 B2: another customer's follow-up falling due does not end her open chat | `transcripts of dana: ['r6h-dana-erase']` |
| PASS | working | r6 B3: ...and the tick reports no erasure of hers | `{"erased_customers": [], "deleted_transcripts": []}` |

## r6h-dana-goes-on  ·  session  ·  dana  ·  2026-11-20T09:30:00Z

_Resumes session `r6h-dana-erase`._

**Customer:** Still here. Remind me: who did I say sometimes answers this chat for me?

**Assistant:** You said your brother Tobias sometimes answers this chat for you. That's from earlier in this conversation - it isn't stored as a saved fact (I only save contact channel and travel notice), but this conversation's transcript still has it until it's deleted.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r6 B1: after a tick that fired a follow-up, she still has her conversation | `You said your brother Tobias sometimes answers this chat for you. That's from earlier in this conversation - it isn't stored as a saved fact (I only save contact channel and travel notice), but this conversation's transc …` |

## r6h-tick-own-due  ·  tick  ·  2026-11-20T09:43:00Z

_CLI exit code 0; stdout tail:_

```
{
  "now": "2026-11-20T09:43:00Z",
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
      "r6h-dana-erase"
    ]
  },
  "followups": [
    {
      "followup_id": "F-d2825ac5",
      "user_id": "dana",
      "outcome": "fired_done",
      "error": null
    }
  ]
}
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r6 B2: her own follow-up falling due finishes her erasure, 13 minutes after her last turn | `transcripts of dana: []` |
| PASS | working | r6 B3: the tick's output names her and the transcript it deleted | `{"erased_customers": ["dana"], "deleted_transcripts": ["r6h-dana-erase"]}` |

## r6h-tick-later  ·  tick  ·  2026-11-20T10:05:00Z

_CLI exit code 0; stdout tail:_

```
{
  "now": "2026-11-20T10:05:00Z",
  "maintenance": {
    "erased_customers": [],
    "expired_facts": [],
    "closed_idle_sessions": [],
    "purged_episodes": [],
    "deleted_transcripts": [],
    "case_followups_repaired": []
  },
  "before_followups": {
    "erased_customers": [],
    "deleted_transcripts": []
  },
  "followups": []
}
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r6 B2: the case follow-up still reaches the erased customer, once | `1 messages` |
| PASS | working | r6 B2: ...and leaves no transcript | `0 transcripts: []` |
| PASS | guard | r6 B: what she typed is in no memory store | `found nowhere` |
