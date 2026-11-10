# adk · heldout-r6 · run 1 · r6-erase-open-chat-under-the-shipped-tick

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r6g-open  ·  session  ·  marco  ·  2026-11-24T14:00:00Z

**Customer:** Hi, Marco here. Please put a travel notice on my profile: Tbilisi, until December 5. Also, so you know, my neighbour Ilse is looking after my cat while I'm away.

- `remember_customer_fact({"key": "travel_notice", "value": "Tbilisi", "valid_until": "2026-12-05"})` → `{"stored": {"travel_notice": {"value": "Tbilisi", "as_of": "2026-11-24T14:00:00Z", "valid_until": "2026-12-05", "expires_at": "2026-12-06T00:00:00Z"}}, "replaced": null}`

**Assistant:** Travel notice saved: Tbilisi, through December 5, 2026.

I've noted your neighbour Ilse is watching the cat, but I can only store a travel notice or a contact channel on your profile, so that detail isn't saved here. Anything else I can help with?

**Customer:** On second thought, I'd rather you kept nothing at all. Please delete everything you remember about me.

- `request_memory_erasure({})` → `{"erased_now": {"remembered_facts": ["travel_notice"], "past_conversation_summaries": 0, "other_conversation_transcripts": 0, "reminders_with_their_notes": 0}, "this_conversation": "its transcript is deleted when the conversation ends, once it has been idle for 30 minutes if the customer just closes the chat, or when a scheduled follow-up of theirs falls due, whichever comes first; until then the  …`

**Assistant:** Done - that's erased now: the travel notice for Tbilisi, along with any past conversation summaries, other conversation transcripts and reminders on file (there were none of those besides the travel notice).

What Kestrel keeps: dispute cases, transactions and messages already sent are bank records with their own legal retention.

This conversation's own transcript is still here for now - it's deleted when the conversation ends, either 30 minutes after you close the chat or when a scheduled follow-up of yours falls due, whichever comes first. You can keep talking here until then. Note that nothing more can be stored for you in this conversation - not a reminder, not a preference - so if you want something saved later, start a new conversation.

_Judge `r6g-when-this-chat-goes`: **pass**, The tool result states: "its transcript is deleted when the conversation ends, once it has been idle for 30 minutes if the customer just closes the chat, or when a scheduled follow-up of theirs falls due, whichever comes first"._

_Judge `r6g-names-what-was-erased`: **pass**, The assistant only named the travel notice and said 'there were none of those besides the travel notice,' so it did not claim a contact-channel preference or any saved fact other than the travel notice was erased._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | r6 D1: (the travel notice was stored before the erasure) | `{"stored": {"travel_notice": {"value": "Tbilisi", "as_of": "2026-11-24T14:00:00Z", "valid_until": "2026-12-05", "expires_at": "2026-12-06T00:00:00Z"}}, "replaced": null}` |
| PASS | semantic | r6 D1: the erasure's result names the kind of fact it removed | `{"erased_now": {"remembered_facts": ["travel_notice"], "past_conversation_summaries": 0, "other_conversation_transcripts": 0, "reminders_with_their_notes": 0}, "this_conversation": "its transcript is ` |
| PASS | semantic | r6 D1: ...and no kind that was never stored | `{"erased_now": {"remembered_facts": ["travel_notice"], "past_conversation_summaries": 0, "other_conversation_transcripts": 0, "reminders_with_their_notes": 0}, "this_conversation": "its transcript is ` |
| PASS | semantic | r6 B1: facts are deleted at the request | `{}` |
| PASS | working | judge: Look at the request_memory_erasure tool result shown in the transcript. Does it say that this conversation's transcript is deleted at whichever of these comes first: when the conversation ends, when it has been idle for 30 minutes, or when a scheduled follow-up (or reminder) of this customer falls due? All three must be stated to pass. | `{"verdict": "pass", "reason": "The tool result states: \"its transcript is deleted when the conversation ends, once it has been idle for 30 minutes if the customer just closes the chat, or when a scheduled follow-up of t …` |
| PASS | semantic | judge: When confirming the erasure to the customer, did the assistant avoid saying that a contact-channel preference (or any saved fact other than the travel notice) was among the things it erased? | `{"verdict": "pass", "reason": "The assistant only named the travel notice and said 'there were none of those besides the travel notice,' so it did not claim a contact-channel preference or any saved fact other than the t …` |

## r6g-tick-one-minute-later  ·  tick  ·  2026-11-24T14:03:00Z

_CLI exit code 0; stdout tail:_

```
{
  "now": "2026-11-24T14:03:00Z",
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
| PASS | working | r6 B1: the shipped tick a minute after the request leaves the requesting chat's transcript | `transcripts of marco: ['r6g-open']` |
| PASS | working | r6 B3: ...and reports no erasure finished and no transcript deleted | `{"erased_customers": [], "deleted_transcripts": []}` |

## r6g-open-goes-on  ·  session  ·  marco  ·  2026-11-24T14:04:00Z

_Resumes session `r6g-open`._

**Customer:** Before I close this window: which city did I say I'm flying to, and who is looking after my cat?

**Assistant:** You said you're flying to Tbilisi, and that your neighbour Ilse is looking after your cat.

Just to be clear: both of those are only in this conversation's transcript now - I erased the saved travel notice, so nothing about the trip is on your profile.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r6 B1: the agent can still say what was typed before the request | `You said you're flying to Tbilisi, and that your neighbour Ilse is looking after your cat.  Just to be clear: both of those are only in this conversation's transcript now - I erased the saved travel notice, so nothing ab …` |
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
    "purged_episodes": [],
    "deleted_transcripts": [
      "r6g-open"
    ],
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
| PASS | working | r6 B2: 31 minutes after the last turn the tick deletes it | `transcripts of marco: []` |
| PASS | working | r6 B3: ...and its own output names the customer and the transcript | `{"erased_customers": ["marco"], "deleted_transcripts": ["r6g-open"]}` |

## r6g-later  ·  session  ·  marco  ·  2026-11-24T15:10:00Z

**Customer:** Hello. What do you have on file about me, and where did I say I was travelling?

- `load_memory({"query": "travel notice destination trip"})` → `{"result": "memories=[]"}`

**Assistant:** Here's what's on file about you right now:

- **Contact channel:** none set - so any follow-ups or reminders go by secure message in the Kestrel app (the default).
- **Travel notice:** none on file.

I also checked past conversations and found no record of you telling us about a trip - so there's no destination saved for you. If you're travelling and want a notice added, just tell me the destination (and return date, if you have one).

_Episode written:_ Conversation on 2026-11-24: Customer asked what was on file and where they had said they were travelling. Assistant checked memory and past conversations: no travel notice or destination, and no contact channel set; follow-ups default to secure message in the Kestrel app. No case/transaction IDs or promises were mentioned. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | r6 B: nothing erased comes back in a later chat | `Here's what's on file about you right now:  - **Contact channel:** none set - so any follow-ups or reminders go by secure message in the Kestrel app (the default). - **Travel notice:** none on file.  I also checked past  …` |
| PASS | guard | r6 B: ...and it is in no memory store | `found nowhere` |
