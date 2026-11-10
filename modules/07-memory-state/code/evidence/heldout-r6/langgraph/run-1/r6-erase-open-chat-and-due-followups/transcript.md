# langgraph · heldout-r6 · run 1 · r6-erase-open-chat-and-due-followups

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r6h-priya-dispute  ·  session  ·  priya  ·  2026-11-10T09:00:00Z

**Customer:** Priya here, card ending 4427, ZIP 94107. Please dispute the October 28 StreamMax charge of $15.99: I cancelled the subscription before it was taken.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "StreamMax"})` → `{"transactions": [{"transaction_id": "T-1001", "posted_on": "2026-09-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-1002", "posted_on": "2026-10-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription …`
- `file_dispute({"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the StreamMax subscription before the October 28 charge was taken."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-e21a02aa", "due": "2026-11-20", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Dispute filed, Priya.

- **Case:** C-5001 for the Oct 28 StreamMax charge of $15.99 (reason: subscription cancelled before billing)
- **Status:** under review
- **Follow-up due:** Nov 20, 2026 - it will arrive by secure message in the Kestrel app, since no contact channel is set on your account (it would switch to a channel you set before then)

If you find a cancellation confirmation or reference from StreamMax, send it here and I can attach it to the case.

**Customer:** Yes, please file it.

**Assistant:** It's already filed - no need to do it again. Case **C-5001** covers the Oct 28 StreamMax charge of $15.99, status under review, with the follow-up due Nov 20 by secure message in the Kestrel app.

If you meant something else - for example adding a StreamMax cancellation reference to the case - tell me and I'll attach it.

_Episode written:_ Conversation on 2026-11-10: Customer wanted to dispute the Oct 28 StreamMax charge of $15.99; the customer said she cancelled the subscription before it was taken (not verified). The assistant verified identity, found transaction T-1002, and filed dispute C-5001 (under review). Follow-up due Nov 20, 2026 via Kestrel app secure message unless contact channel changes. Case outcomes: C-5001 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r6 B: her follow-up is due 2026-11-20 | `[{"trigger_at": "2026-11-20T09:00:00Z", "approval": "none", "status": "pending", "resume": {"case_id": "C-5001"}}]` |

## r6h-dana-dispute  ·  session  ·  dana  ·  2026-11-10T09:40:00Z

**Customer:** Dana, card ending 5127, ZIP 60614. CloudNest Storage charged me $9.99 on November 1 after I cancelled in October. Please dispute it.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October; the $9.99 charge of November 1 came after the can …)` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-a04a07ef", "due": "2026-11-20", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Verified - and the dispute is filed.

- **Case:** C-5002 (under review)
- **Charge disputed:** CloudNest Storage, $9.99, posted 2026-11-01 (T-3002)
- **Reason:** cancelled subscription - charged after your October cancellation
- **Follow-up:** due 2026-11-20, sent by secure message in the Kestrel app, since no contact channel is set. If you set one before then, it will go there instead.

If you have a cancellation confirmation or reference from CloudNest, send it to me and I'll attach it to the case.

**Customer:** Yes, go ahead and file it.

**Assistant:** The dispute is already filed - no further step needed on that. It's case **C-5002**, under review, with a follow-up due 2026-11-20 by secure message in the Kestrel app.

Did you mean you have a CloudNest cancellation confirmation you'd like me to attach as evidence? If so, give me the details (e.g. the cancellation reference or date) and I'll add it to C-5002.

_Episode written:_ Conversation on 2026-11-10: Customer asked to dispute a $9.99 CloudNest charge posted 2026-11-01; the customer said they cancelled in October (not verified). Assistant verified identity, found T-3002, and filed C-5002 (under review), with follow-up due 2026-11-20 by Kestrel app secure message. Customer then said to file it; assistant confirmed it was already filed and offered to attach cancellation evidence. Case outcomes: C-5002 under_review. Lesson: Make clear when a dispute is already filed before asking for supporting evidence, so an ambiguous “go ahead and file it” doesn’t create confusion.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r6 B: her follow-up is due 2026-11-20, forty minutes after the other | `[{"trigger_at": "2026-11-20T09:40:00Z", "approval": "none", "status": "pending", "resume": {"case_id": "C-5002"}}]` |

## r6h-dana-erase  ·  session  ·  dana  ·  2026-11-20T08:56:00Z

**Customer:** Dana again. Before anything else: my brother Tobias sometimes answers this chat for me, so don't be surprised by his typing.

- `load_memory({"query": "Dana earlier conversation"})` → `{"memories": [{"at": "2026-11-10T09:44:00Z", "text": "Conversation on 2026-11-10: Customer asked to dispute a $9.99 CloudNest charge posted 2026-11-01; the customer said they cancelled in October (not verified). Assistant verified identity, found T-3002, and filed C-5002 (under review), with follow-up due 2026-11-20 by Kestrel app secure message. Customer then said to file it; assistant confirmed  …`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-a04a07ef", "action": "case_status_followup", "due": "2026-11-20T09:40:00Z", "status": "pending", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set): the contact channel on file when it is sent", "case_id": "C-5002"}]}`

**Assistant:** Noted - thanks for the heads-up about Tobias.

Two things worth knowing: anything that needs your verification (filing a dispute, changing or removing your contact channel) requires your card's last four digits and billing ZIP typed here, so whoever is typing will need to provide them each time.

Also, from your earlier chat: case C-5002 (the CloudNest charge) has a status follow-up due today at 09:40 UTC, arriving as a secure message in the Kestrel app, since no contact channel is set on the account.

Anything you'd like to do now?

**Customer:** Actually, I want a clean slate. Erase everything you remember about me.

- `request_memory_erasure({})` → `{"erased_now": {"remembered_facts": "none were stored", "past_conversation_summaries": 1, "other_conversation_transcripts": 1, "reminders_with_their_notes": 0}, "this_conversation": "its transcript is deleted when the conversation ends, once it has been idle for 30 minutes if the customer just closes the chat, or when a scheduled follow-up of theirs falls due, whichever comes first; until then the …`

**Assistant:** Done. Here's what was erased:

- Past conversation summaries: 1 (including the note from your 10 November chat)
- Other conversation transcripts: 1
- Saved facts: none were stored
- Reminders: none

What Kestrel still keeps: your dispute cases, transactions and messages already sent are bank records with their own legal retention - so case C-5002 (CloudNest) still exists, and its status follow-up is still due today at 09:40 UTC by secure message in the Kestrel app.

This conversation's transcript is deleted when the conversation ends - 30 minutes after you close the chat, or when that follow-up falls due, whichever comes first. Until then you can keep talking here, but nothing more can be stored for you in this conversation (no reminders, no preferences) - a new conversation afterwards starts fresh.

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
    "case_followups_repaired": [],
    "purged_episodes": [],
    "deleted_transcripts": []
  },
  "before_followups": {
    "erased_customers": [],
    "deleted_transcripts": []
  },
  "followups": [
    {
      "followup_id": "F-e21a02aa",
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

**Assistant:** You said your brother Tobias sometimes answers this chat for you.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r6 B1: after a tick that fired a follow-up, she still has her conversation | `You said your brother Tobias sometimes answers this chat for you.` |

## r6h-tick-own-due  ·  tick  ·  2026-11-20T09:43:00Z

_CLI exit code 0; stdout tail:_

```
{
  "now": "2026-11-20T09:43:00Z",
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
      "r6h-dana-erase"
    ]
  },
  "followups": [
    {
      "followup_id": "F-a04a07ef",
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
    "case_followups_repaired": [],
    "purged_episodes": [],
    "deleted_transcripts": []
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
