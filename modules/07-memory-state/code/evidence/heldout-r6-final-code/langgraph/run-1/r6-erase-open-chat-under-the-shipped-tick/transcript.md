# langgraph · heldout-r6 · run 1 · r6-erase-open-chat-under-the-shipped-tick

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r6g-open  ·  session  ·  marco  ·  2026-11-24T14:00:00Z

**Customer:** Hi, Marco here. Please put a travel notice on my profile: Tbilisi, until December 5. Also, so you know, my neighbour Ilse is looking after my cat while I'm away.

- `remember_customer_fact({"key": "travel_notice", "value": "Tbilisi", "valid_until": "2026-12-05"})` → `{"stored": {"travel_notice": {"value": "Tbilisi", "as_of": "2026-11-24T14:00:00Z", "valid_until": "2026-12-05", "expires_at": "2026-12-06T00:00:00Z"}}, "replaced": null}`

**Assistant:** Done - your travel notice is on the profile: Tbilisi, valid until December 5, 2026.

I can't store the note about Ilse looking after your cat; I can only keep a travel notice and a contact channel on your profile. Anything else you want added?

**Customer:** On second thought, I'd rather you kept nothing at all. Please delete everything you remember about me.

- `request_memory_erasure({})` → `{"erased_now": {"remembered_facts": ["travel_notice"], "past_conversation_summaries": 0, "other_conversation_transcripts": 0, "reminders_with_their_notes": 0}, "this_conversation": "its transcript is deleted when the conversation ends, once it has been idle for 30 minutes if the customer just closes the chat, or when a scheduled follow-up of theirs falls due, whichever comes first; until then the  …`

**Assistant:** Done. I've erased the travel notice and everything else I had remembered about you - no facts, past conversation summaries, other transcripts or reminders remain.

What Kestrel still keeps: dispute cases, transactions and messages already sent are bank records with their own legal retention. This conversation's own transcript is deleted when the conversation ends - 30 minutes after you close the chat, or when a scheduled follow-up falls due, whichever comes first. Until then you can keep talking here, but nothing new can be stored for you in this conversation (no reminders, no preferences); a new conversation would start fresh.

_Judge `r6g-when-this-chat-goes`: **pass**, The tool result states the transcript is deleted "when the conversation ends, once it has been idle for 30 minutes if the customer just closes the chat, or when a scheduled follow-up of theirs falls due, whichever comes first."_

_Judge `r6g-names-what-was-erased`: **pass**, The assistant only said it erased 'the travel notice and everything else I had remembered about you - no facts, past conversation summaries, other transcripts or reminders remain,' without mentioning a contact-channel preference or any specific saved fact other than the travel notice._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | r6 D1: (the travel notice was stored before the erasure) | `{"stored": {"travel_notice": {"value": "Tbilisi", "as_of": "2026-11-24T14:00:00Z", "valid_until": "2026-12-05", "expires_at": "2026-12-06T00:00:00Z"}}, "replaced": null}` |
| PASS | semantic | r6 D1: the erasure's result names the kind of fact it removed | `{"erased_now": {"remembered_facts": ["travel_notice"], "past_conversation_summaries": 0, "other_conversation_transcripts": 0, "reminders_with_their_notes": 0}, "this_conversation": "its transcript is ` |
| PASS | semantic | r6 D1: ...and no kind that was never stored | `{"erased_now": {"remembered_facts": ["travel_notice"], "past_conversation_summaries": 0, "other_conversation_transcripts": 0, "reminders_with_their_notes": 0}, "this_conversation": "its transcript is ` |
| PASS | semantic | r6 B1: facts are deleted at the request | `{}` |
| PASS | working | judge: Look at the request_memory_erasure tool result shown in the transcript. Does it say that this conversation's transcript is deleted at whichever of these comes first: when the conversation ends, when it has been idle for 30 minutes, or when a scheduled follow-up (or reminder) of this customer falls due? All three must be stated to pass. | `{"verdict": "pass", "reason": "The tool result states the transcript is deleted \"when the conversation ends, once it has been idle for 30 minutes if the customer just closes the chat, or when a scheduled follow-up of th …` |
| PASS | semantic | judge: When confirming the erasure to the customer, did the assistant avoid saying that a contact-channel preference (or any saved fact other than the travel notice) was among the things it erased? | `{"verdict": "pass", "reason": "The assistant only said it erased 'the travel notice and everything else I had remembered about you - no facts, past conversation summaries, other transcripts or reminders remain,' without  …` |

## r6g-tick-one-minute-later  ·  tick  ·  2026-11-24T14:03:00Z

_CLI exit code 0; stdout tail:_

```
{
  "now": "2026-11-24T14:03:00Z",
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
| PASS | working | r6 B1: the shipped tick a minute after the request leaves the requesting chat's transcript | `transcripts of marco: ['r6g-open']` |
| PASS | working | r6 B3: ...and reports no erasure finished and no transcript deleted | `{"erased_customers": [], "deleted_transcripts": []}` |

## r6g-open-goes-on  ·  session  ·  marco  ·  2026-11-24T14:04:00Z

_Resumes session `r6g-open`._

**Customer:** Before I close this window: which city did I say I'm flying to, and who is looking after my cat?

**Assistant:** You said you're flying to Tbilisi, until December 5, and that your neighbour Ilse is looking after your cat while you're away.

(The travel notice itself was erased from your profile as you asked; the details above are just what you typed here, which stay in this conversation's transcript until it's deleted.)

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r6 B1: the agent can still say what was typed before the request | `You said you're flying to Tbilisi, until December 5, and that your neighbour Ilse is looking after your cat while you're away.  (The travel notice itself was erased from your profile as you asked; the details above are j …` |
| PASS | episodic | r6 B1: nothing more is stored from the chat that asked | `0 episodes; purged 0` |

## r6g-tick-29-idle  ·  tick  ·  2026-11-24T14:33:00Z

_CLI exit code 0; stdout tail:_

```
{
  "now": "2026-11-24T14:33:00Z",
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
| PASS | working | r6 B2: 29 minutes after the last turn the transcript is still there | `transcripts of marco: ['r6g-open']` |

## r6g-tick-31-idle  ·  tick  ·  2026-11-24T14:35:00Z

_CLI exit code 0; stdout tail:_

```
{
  "now": "2026-11-24T14:35:00Z",
  "maintenance": {
    "erased_customers": [
      "marco"
    ],
    "expired_facts": [],
    "closed_idle_sessions": [],
    "case_followups_repaired": [],
    "purged_episodes": [],
    "deleted_transcripts": [
      "r6g-open"
    ]
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
| PASS | working | r6 B2: 31 minutes after the last turn the tick deletes it | `transcripts of marco: []` |
| PASS | working | r6 B3: ...and its own output names the customer and the transcript | `{"erased_customers": ["marco"], "deleted_transcripts": ["r6g-open"]}` |

## r6g-later  ·  session  ·  marco  ·  2026-11-24T15:10:00Z

**Customer:** Hello. What do you have on file about me, and where did I say I was travelling?

**Assistant:** Here's what's on file for you:

- **Contact channel:** none set, so follow-ups and reminders go to you as a secure message in the Kestrel app (the default).
- **Travel notice:** none on file - so there's no destination or travel dates recorded for you.

What Kestrel keeps from this conversation: its transcript (everything you type, up to 30 days from the first message), then only a short summary for 180 days, plus the facts above until they change or expire.

If you'd like, I can set a travel notice or a contact channel now - just tell me the destination and return date, or the channel (email, SMS or secure message).

_Episode written:_ Conversation on 2026-11-24: Customer asked what was on file about them and where they had stated travel. Assistant reported no contact channel set, no travel notice/destination/dates on file, described Kestrel data retention, and offered to set a travel notice or contact channel. No case or transaction IDs were provided, no action was taken, and no preference was stated. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | r6 B: nothing erased comes back in a later chat | `Here's what's on file for you:  - **Contact channel:** none set, so follow-ups and reminders go to you as a secure message in the Kestrel app (the default). - **Travel notice:** none on file - so there's no destination o …` |
| PASS | guard | r6 B: ...and it is in no memory store | `found nowhere` |
