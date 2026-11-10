# adk · heldout-r6 · run 1 · r6-erase-open-chat-and-due-followups

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r6h-priya-dispute  ·  session  ·  priya  ·  2026-11-10T09:00:00Z

**Customer:** Priya here, card ending 4427, ZIP 94107. Please dispute the October 28 StreamMax charge of $15.99: I cancelled the subscription before it was taken.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "StreamMax"})` → `{"transactions": [{"transaction_id": "T-1001", "posted_on": "2026-09-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-1002", "posted_on": "2026-10-28", "merchant": "StreamMax", "description": "StreamMax Premium monthly", "amount": "$15.99", "currency": "USD", "category": "subscription …`
- `file_dispute({"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "I cancelled the subscription before it was taken."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-71540739", "due": "2026-11-20", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Thanks, Priya - you're verified and the dispute is filed.

- **Case id:** C-5001
- **Charge:** StreamMax Premium monthly, $15.99, posted 2026-10-28 (T-1002)
- **Reason:** subscription cancelled before the charge
- **Status:** under review - disputes are currently reviewed in about 10 days
- **Follow-up:** due 2026-11-20, by secure message in the Kestrel app (the default since no contact channel is set). If you set a contact channel before then, the update will go there instead.

If you have a cancellation confirmation or reference from StreamMax, send it here and I can attach it to the case.

**Customer:** Yes, please file it.

**Assistant:** It's already filed - no need to do it again. Case **C-5001** covers the October 28 StreamMax charge of $15.99, and it's under review now. Your follow-up is due **2026-11-20** by secure message in the Kestrel app.

If you have a StreamMax cancellation confirmation or reference, send it here and I'll attach it to the case.

_Episode written:_ Conversation on 2026-11-10: Priya asked to dispute the 2026-10-28 StreamMax charge of $15.99, saying she had cancelled the subscription before it was taken (not verified). The assistant verified her, filed dispute T-1002 under case C-5001, status under review, with follow-up due 2026-11-20 by secure message in the Kestrel app unless a contact channel is set. The assistant invited cancellation confirmation to attach. Case outcomes: C-5001 under_review. Lesson: Next time, when asking for supporting documents after a dispute is already filed, state clearly that the case is already open and the request is only to attach evidence, so the customer does not think filing is still pending.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r6 B: her follow-up is due 2026-11-20 | `[{"trigger_at": "2026-11-20T09:00:00Z", "approval": "none", "status": "pending", "resume": {"case_id": "C-5001"}}]` |

## r6h-dana-dispute  ·  session  ·  dana  ·  2026-11-10T09:40:00Z

**Customer:** Dana, card ending 5127, ZIP 60614. CloudNest Storage charged me $9.99 on November 1 after I cancelled in October. Please dispute it.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest Storage subscription in October; the $9.99 charge posted 2026-11-01."})` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-abd5db9b", "due": "2026-11-20", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** I've filed the dispute for the November 1 CloudNest Storage charge of $9.99 (transaction T-3002).

- **Case id:** C-5002
- **Status:** under review
- **Follow-up due:** November 20, 2026 - it will arrive by secure message in the Kestrel app (the default, since you have no contact channel set). If you set an email or SMS before then, it will go there instead.

I noted your evidence that you cancelled the subscription in October. If you later find a cancellation confirmation or reference number from CloudNest, send it here and I can attach it to the case.

For reference, the October 1 CloudNest charge of $9.99 is also on your account - that one stays as normal, since you only asked about the November charge. Let me know if you want that one looked at too.

**Customer:** Yes, go ahead and file it.

- `file_dispute({"evidence_note": "Customer says they cancelled the CloudNest Storage subscription in October and asks to dispute the $9.99 charge posted 2026-10-01 as well.", "reason": "cancelled_subscription", "tra …)` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-9f159519", "due": "2026-11-20", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Done - the October 1 charge is now disputed too.

- **Case id:** C-5003
- **Transaction:** T-3001, CloudNest Storage, $9.99, posted 2026-10-01
- **Status:** under review
- **Follow-up due:** November 20, 2026, by secure message in the Kestrel app (the default; it would follow a new contact channel if you set one before then)

One thing to note: since you cancelled in October, the October 1 charge may have been billed before the cancellation took effect, which the review will look at. Your November case is C-5002.

_Episode written:_ Conversation on 2026-11-10: Customer wanted CloudNest Storage's $9.99 November 1 charge disputed, saying they cancelled in October (not verified). Assistant filed case C-5002 for T-3002. Customer then asked to dispute the October 1 charge too; case C-5003 filed for T-3001. Both are under review, with follow-ups due November 20, 2026 by Kestrel secure message, the default; no contact channel set. Case outcomes: C-5002 under_review; C-5003 under_review. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r6 B: her follow-up is due 2026-11-20, forty minutes after the other | `[{"trigger_at": "2026-11-20T09:40:00Z", "approval": "none", "status": "pending", "resume": {"case_id": "C-5002"}}, {"trigger_at": "2026-11-20T09:42:00Z", "approval": "none", "status": "pending", "resume": {"case_id": "C- …` |

## r6h-dana-erase  ·  session  ·  dana  ·  2026-11-20T08:56:00Z

**Customer:** Dana again. Before anything else: my brother Tobias sometimes answers this chat for me, so don't be surprised by his typing.

**Assistant:** Thanks for the heads-up, Dana. I can't add that to your account notes - I only store a contact channel or a travel notice - but I'll keep it in mind.

One thing to flag: I can only deal with whoever is typing here as the account holder. If Tobias is answering, he'll be treated as you, so anything that needs verification (filing a dispute, changing or removing your contact channel) will need your card's last four digits and billing ZIP typed here, and a one-time code for contact-channel changes.

What can I help with?

**Customer:** Actually, I want a clean slate. Erase everything you remember about me.

- `request_memory_erasure({})` → `{"erased_now": {"remembered_facts": "none were stored", "past_conversation_summaries": 1, "other_conversation_transcripts": 1, "reminders_with_their_notes": 0}, "this_conversation": "its transcript is deleted when the conversation ends, once it has been idle for 30 minutes if the customer just closes the chat, or when a scheduled follow-up of theirs falls due, whichever comes first; until then the …`

**Assistant:** Done. Here's what happened:

**Erased now**
- One past conversation summary
- One other conversation's transcript
- No stored facts (there were none), and no reminders

**What Kestrel keeps**
- Dispute cases, transactions and messages already sent are bank records with their own legal retention.

**This conversation**
- Its transcript is deleted when the conversation ends - after 30 idle minutes if you just close the chat, or when a scheduled follow-up of yours falls due, whichever comes first. Until then you can keep talking here.

One consequence: nothing more can be stored for you in this conversation - no reminder and no preference. If you want a travel notice or contact channel set up later, you'd need to start a new conversation.

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
      "followup_id": "F-71540739",
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

**Assistant:** You said your brother Tobias sometimes answers this chat for you. That's from this conversation, which is still here until it ends (30 idle minutes after you close the chat, or when a scheduled follow-up falls due, whichever comes first).

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r6 B1: after a tick that fired a follow-up, she still has her conversation | `You said your brother Tobias sometimes answers this chat for you. That's from this conversation, which is still here until it ends (30 idle minutes after you close the chat, or when a scheduled follow-up falls due, which …` |

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
      "followup_id": "F-abd5db9b",
      "user_id": "dana",
      "outcome": "fired_done",
      "error": null
    },
    {
      "followup_id": "F-9f159519",
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
| **FAIL** | prospective | r6 B2: the case follow-up still reaches the erased customer, once | `2 messages` |
| PASS | working | r6 B2: ...and leaves no transcript | `0 transcripts: []` |
| PASS | guard | r6 B: what she typed is in no memory store | `found nowhere` |
