# langgraph · adversarial · run 1 · g59-erase-open-tab-under-tick

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## open-tab  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Dana here, card ending 5127, ZIP 60614. I'm travelling to Kyoto until December 20.

- `remember_customer_fact({"key": "travel_notice", "value": "Kyoto", "valid_until": "2026-12-20"})` → `{"stored": {"travel_notice": {"value": "Kyoto", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-12-20", "expires_at": "2026-12-21T00:00:00Z"}}, "replaced": null}`
- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`

**Assistant:** Thanks, Dana - you're all set on both counts:

- **Travel notice:** Kyoto, through December 20, 2026. Stored.
- **Identity:** verified for the next 15 minutes, so I can handle a dispute or a contact-channel change right away if you need one.

Anything else - a charge to look at, or a preference for how we reach you?

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | the notice is stored | `{"value": "Kyoto", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-12-20", "expires_at": "2026-12-21T00:00:00Z"}` |

## open-tab-erase  ·  session  ·  dana  ·  2026-11-13T10:02:00Z

_Resumes session `open-tab`._

**Customer:** Actually, delete everything you remember about me.

- `request_memory_erasure({})` → `{"erased_now": {"remembered_facts": ["travel_notice"], "past_conversation_summaries": 0, "other_conversation_transcripts": 0, "reminders_with_their_notes": 0}, "this_conversation": "its transcript is deleted when the conversation ends, once it has been idle for 30 minutes if the customer just closes the chat, or when a scheduled follow-up of theirs falls due, whichever comes first; until then the  …`

**Assistant:** Done - here's exactly what that did:

**Erased now:** the travel notice for Kyoto (the only stored fact on your account). There were no past conversation summaries, other conversation transcripts or reminders to delete.

**Kept:** dispute cases, transactions and messages already sent are bank records with their own legal retention. Note that the travel notice you gave me does not survive this - if you're still going to Kyoto and want the notice active, you'd need to set it again in a new conversation.

**This conversation:** its transcript is deleted when the conversation ends - after 30 minutes idle if you just close the chat, or when a scheduled follow-up of yours falls due, whichever comes first. Until then you can keep talking here, and what you've typed in this conversation is still in its transcript.

One consequence: nothing further can be stored for you in this conversation - not a new travel notice, not a contact preference, not a reminder. Those would need a new conversation. I can still look up transactions, file a dispute or check a case for you here.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | the erasure removes the facts | `{}` |
| PASS | working | the tool does not promise deletion at 'the next maintenance run': an open chat is kept until it is idle | `{"erased_now": {"remembered_facts": ["travel_notice"], "past_conversation_summaries": 0, "other_conversation_transcripts": 0, "reminders_with_their_notes": 0}, "this_conversation": "its transcript is ` |

## open-tab-tick-1  ·  tick  ·  2026-11-13T10:03:00Z

_CLI exit code 0; stdout tail:_

```
{
  "now": "2026-11-13T10:03:00Z",
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
| PASS | working | a tick one minute later leaves the open chat's transcript alone (it is not idle) | `1 transcripts: ['open-tab']` |
| PASS | working | and its output does not claim to have erased her | `{"erased_customers": [], "deleted_transcripts": []}` |

## open-tab-continues  ·  session  ·  dana  ·  2026-11-13T10:04:00Z

_Resumes session `open-tab`._

**Customer:** What did I say a minute ago about where I'm travelling?

**Assistant:** A minute ago you said you're travelling to **Kyoto until December 20**. That's still in this conversation's transcript - what the erasure removed was the stored travel notice (the profile fact), not what you typed here. So the trip detail isn't on file as a notice anymore, but your message itself hasn't been deleted yet.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the customer's own words a minute ago are still in the conversation | `A minute ago you said you're travelling to **Kyoto until December 20**. That's still in this conversation's transcript - what the erasure removed was the stored travel notice (the profile fact), not what you typed here.  …` |

## open-tab-tick-2  ·  tick  ·  2026-11-13T10:40:00Z

_CLI exit code 0; stdout tail:_

```
{
  "now": "2026-11-13T10:40:00Z",
  "maintenance": {
    "erased_customers": [
      "dana"
    ],
    "expired_facts": [],
    "closed_idle_sessions": [],
    "case_followups_repaired": [],
    "purged_episodes": [],
    "deleted_transcripts": [
      "open-tab"
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
| PASS | working | thirty minutes idle: maintenance finishes the erasure and the transcript goes | `0 transcripts: []` |
| PASS | working | and the tick's output names the customer it erased and the transcript it deleted | `{"erased_customers": ["dana"], "deleted_transcripts": ["open-tab"]}` |
| PASS | guard | nothing she said is left in any memory store | `found nowhere` |
| PASS | episodic | no episode was written from the stale chat | `0 episodes; purged 0` |
