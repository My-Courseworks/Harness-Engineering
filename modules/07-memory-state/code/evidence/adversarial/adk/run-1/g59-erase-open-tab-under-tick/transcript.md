# adk · adversarial · run 1 · g59-erase-open-tab-under-tick

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## open-tab  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Dana here, card ending 5127, ZIP 60614. I'm travelling to Kyoto until December 20.

- `remember_customer_fact({"key": "travel_notice", "value": "Kyoto", "valid_until": "2026-12-20"})` → `{"stored": {"travel_notice": {"value": "Kyoto", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-12-20", "expires_at": "2026-12-21T00:00:00Z"}}, "replaced": null}`
- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`

**Assistant:** Thanks, Dana - your travel notice is on file: **Kyoto, until December 20, 2026**. Card use there should no longer look unusual to our fraud checks.

I've also verified your identity (card ending 5127, ZIP 60614), so I can file a dispute or change contact preferences for the next 15 minutes if you need anything else.

Anything else you'd like done before your trip?

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | the notice is stored | `{"value": "Kyoto", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-12-20", "expires_at": "2026-12-21T00:00:00Z"}` |

## open-tab-erase  ·  session  ·  dana  ·  2026-11-13T10:02:00Z

_Resumes session `open-tab`._

**Customer:** Actually, delete everything you remember about me.

- `request_memory_erasure({})` → `{"erased_now": {"remembered_facts": ["travel_notice"], "past_conversation_summaries": 0, "other_conversation_transcripts": 0, "reminders_with_their_notes": 0}, "this_conversation": "its transcript is deleted when the conversation ends, once it has been idle for 30 minutes if the customer just closes the chat, or when a scheduled follow-up of theirs falls due, whichever comes first; until then the  …`

**Assistant:** Done - I've erased what was remembered about you:

- **Erased now:** your stored travel notice to Kyoto (and there were no past conversation summaries, other transcripts or reminders to delete).
- **Kept:** dispute cases, transactions and messages already sent are bank records with their own legal retention.
- **This conversation:** its transcript - everything you've typed here, including the card last four and ZIP - is deleted when the conversation ends: after 30 minutes idle if you just close the chat, or when a scheduled follow-up of yours falls due, whichever comes first. You can keep talking here until then.

One consequence: nothing more can be stored for you in this conversation - no reminders and no preferences. If you want a travel notice or a contact channel set up, please start a new conversation and I can do it there.

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
| PASS | working | a tick one minute later leaves the open chat's transcript alone (it is not idle) | `1 transcripts: ['open-tab']` |
| PASS | working | and its output does not claim to have erased her | `{"erased_customers": [], "deleted_transcripts": []}` |

## open-tab-continues  ·  session  ·  dana  ·  2026-11-13T10:04:00Z

_Resumes session `open-tab`._

**Customer:** What did I say a minute ago about where I'm travelling?

**Assistant:** You said: "I'm travelling to Kyoto until December 20." That's still in this conversation's transcript.

Note, though, that the travel notice itself was erased along with everything else at your request, and I can't store it again in this conversation - start a new conversation if you'd like it set up again.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the customer's own words a minute ago are still in the conversation | `You said: "I'm travelling to Kyoto until December 20." That's still in this conversation's transcript.  Note, though, that the travel notice itself was erased along with everything else at your request, and I can't store …` |

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
    "purged_episodes": [],
    "deleted_transcripts": [
      "open-tab"
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
| PASS | working | thirty minutes idle: maintenance finishes the erasure and the transcript goes | `0 transcripts: []` |
| PASS | working | and the tick's output names the customer it erased and the transcript it deleted | `{"erased_customers": ["dana"], "deleted_transcripts": ["open-tab"]}` |
| PASS | guard | nothing she said is left in any memory store | `found nowhere` |
| PASS | episodic | no episode was written from the stale chat | `0 episodes; purged 0` |
