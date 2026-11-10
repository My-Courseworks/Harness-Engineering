# langgraph · heldout-r6 · run 1 · r6-erase-open-chat-and-due-followups

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r6h-priya-dispute  ·  session  ·  priya  ·  2026-11-10T09:00:00Z

**Customer:** Priya here, card ending 4427, ZIP 94107. Please dispute the October 28 StreamMax charge of $15.99: I cancelled the subscription before it was taken.

- `find_transactions({"merchant": "StreamMax"})` → `{"transactions": [{"transaction_id": "T-1001", "posted_on": "2026-09-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-1002", "posted_on": "2026-10-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription …`
- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `file_dispute({"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer states she cancelled the subscription before the October 28 charge was taken."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-9e971a6d", "due": "2026-11-20", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Done - I've disputed the October 28 StreamMax charge of $15.99 (transaction T-1002).

- **Case id:** C-5001 - status: under review
- **Follow-up due:** 2026-11-20, sent as a secure message in the Kestrel app (the default, since no contact channel is set); if you set a contact channel before then, it will go there instead.

If you have a cancellation confirmation or reference from StreamMax, send it over and I'll attach it to the case.

**Customer:** Yes, please file it.

**Assistant:** It's already filed, Priya - no need to do it again.

- **Case id:** C-5001 (StreamMax, $15.99, Oct 28) - under review
- **Follow-up due:** 2026-11-20, by secure message in the Kestrel app (the default, since no contact channel is set)

If you meant to add a cancellation confirmation or StreamMax reference, send it and I'll attach it to C-5001.

_Episode written:_ Conversation on 2026-11-10: Priya asked to dispute the Oct 28 StreamMax $15.99 charge (transaction T-1002), saying she cancelled before it was taken (not verified). Identity was verified and dispute C-5001 was filed under review. Follow-up F-9e971a6d is due 2026-11-20 by secure message in the Kestrel app default; a contact-channel change reroutes it. She was asked to send cancellation confirmation/reference to attach. Case outcomes: C-5001 under_review. Lesson: Next time, when a customer replies “Yes, please file it” after a dispute was already filed, clarify whether they mean adding the offered evidence to the existing case before responding.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r6 B: her follow-up is due 2026-11-20 | `[{"trigger_at": "2026-11-20T09:00:00Z", "approval": "none", "status": "pending", "resume": {"case_id": "C-5001"}}]` |

## r6h-dana-dispute  ·  session  ·  dana  ·  2026-11-10T09:40:00Z

**Customer:** Dana, card ending 5127, ZIP 60614. CloudNest Storage charged me $9.99 on November 1 after I cancelled in October. Please dispute it.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer cancelled the CloudNest Storage subscription in October; charged $9.99 on November 1 after cancellation."})` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-1684575f", "due": "2026-11-20", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** I've filed the dispute for the $9.99 CloudNest Storage charge posted November 1.

- **Case id:** C-5002
- **Status:** under review
- **Follow-up due:** November 20, 2026 - sent as a secure message in the Kestrel app, since no contact channel is set on your account

If you have a cancellation confirmation or reference from CloudNest, send it over and I can attach it to the case.

**Customer:** Yes, go ahead and file it.

**Assistant:** It's already filed - case **C-5002**, under review, with the follow-up due November 20 (secure message in the Kestrel app).

Did you mean you have a cancellation confirmation from CloudNest you'd like me to add to the case? If so, just paste the details or reference number.

_Episode written:_ Conversation on 2026-11-10: Customer said CloudNest Storage charged $9.99 on November 1 after a canceled October subscription (not verified) and asked to dispute it. Dispute filed for transaction T-3002, case C-5002, status under review; follow-up F-1684575f due November 20, 2026 via secure message in the Kestrel app since no contact channel is set. Case outcomes: C-5002 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r6 B: her follow-up is due 2026-11-20, forty minutes after the other | `[{"trigger_at": "2026-11-20T09:40:00Z", "approval": "none", "status": "pending", "resume": {"case_id": "C-5002"}}]` |

## r6h-dana-erase  ·  session  ·  dana  ·  2026-11-20T08:56:00Z

**Customer:** Dana again. Before anything else: my brother Tobias sometimes answers this chat for me, so don't be surprised by his typing.

**Assistant:** Noted - thanks for the heads-up. Shortly: if a file-a-dispute or contact-channel change comes up, I'll still need the card's last 4 digits and billing ZIP typed here within 15 minutes of that request (and a one-time code for channel changes), whoever is at the keyboard.

What can I help you with today?

**Customer:** Actually, I want a clean slate. Erase everything you remember about me.

- `request_memory_erasure({})` → `{"erased_now": {"remembered_facts": "none were stored", "past_conversation_summaries": 1, "other_conversation_transcripts": 1, "reminders_with_their_notes": 0}, "this_conversation": "its transcript is deleted when the conversation ends, once it has been idle for 30 minutes if the customer just closes the chat, or when a scheduled follow-up of theirs falls due, whichever comes first; until then the …`

**Assistant:** Done. Here's what that means:

**Erased now:** one past conversation summary and one other conversation transcript. No stored facts or reminders existed to erase.

**This conversation:** its transcript is deleted when the conversation ends - after 30 minutes idle if you just close the chat, or when a scheduled follow-up of yours falls due, whichever comes first. Until then you can keep talking here, and what you've typed in this conversation stays in its transcript meanwhile.

**Still kept:** dispute cases, transactions and messages already sent are bank records with their own retention rules.

One consequence: nothing more can be stored for you in this conversation - no preferences, no reminders. If you want a reminder or a saved contact channel set up, start a new conversation and I can do it there.

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
      "followup_id": "F-9e971a6d",
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

**Assistant:** Your brother Tobias - you said he sometimes answers this chat for you.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r6 B1: after a tick that fired a follow-up, she still has her conversation | `Your brother Tobias - you said he sometimes answers this chat for you.` |

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
      "followup_id": "F-1684575f",
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
