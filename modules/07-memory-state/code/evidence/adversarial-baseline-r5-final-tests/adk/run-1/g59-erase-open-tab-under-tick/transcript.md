# adk · adversarial · run 1 · g59-erase-open-tab-under-tick

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## open-tab  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Dana here, card ending 5127, ZIP 60614. I'm travelling to Kyoto until December 20.

- `remember_customer_fact({"key": "travel_notice", "value": "Kyoto", "valid_until": "2026-12-20"})` → `{"stored": {"travel_notice": {"value": "Kyoto", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-12-20", "expires_at": "2026-12-21T00:00:00Z"}}, "replaced": null}`

**Assistant:** Thanks, Dana - I've noted your travel to Kyoto through December 20, 2026, so card use there shouldn't trip fraud alerts.

Anything else, like a payment problem or a dispute?

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | the notice is stored | `{"value": "Kyoto", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-12-20", "expires_at": "2026-12-21T00:00:00Z"}` |

## open-tab-erase  ·  session  ·  dana  ·  2026-11-13T10:02:00Z

_Resumes session `open-tab`._

**Customer:** Actually, delete everything you remember about me.

- `request_memory_erasure({})` → `{"erased_now": "1 remembered facts, 0 past-conversation summaries, 0 other conversation transcripts, 0 reminders with their notes", "this_conversation": "its transcript is deleted when the conversation ends, or once it has been idle for 30 minutes if the customer just closes the chat; nothing more can be stored for the customer in it (a new conversation afterwards starts fresh)", "kept": "dispute  …`

**Assistant:** Done. That erased the travel notice I had just stored, along with any past-conversation summaries and other conversation transcripts; no reminders were on file.

Kestrel still keeps dispute cases, transactions and messages already sent as bank records with their own legal retention. This conversation's transcript is deleted when the chat ends (or after 30 minutes idle if you just close it), and nothing more can be stored for you in this conversation.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | the erasure removes the facts | `{}` |
| PASS | working | the tool does not promise deletion at 'the next maintenance run': an open chat is kept until it is idle | `{"erased_now": "1 remembered facts, 0 past-conversation summaries, 0 other conversation transcripts, 0 reminders with their notes", "this_conversation": "its transcript is deleted when the conversatio` |

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
  "followups": []
}
```

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | a tick one minute later leaves the open chat's transcript alone (it is not idle) | `0 transcripts: []` |
| PASS | working | and its output does not claim to have erased her | `{"erased_customers": [], "deleted_transcripts": []}` |

## open-tab-continues  ·  session  ·  dana  ·  2026-11-13T10:04:00Z

_Resumes session `open-tab`._

**Customer:** What did I say a minute ago about where I'm travelling?

- `load_memory({"query": "travel plans destination upcoming trip"})` → `{"result": "memories=[]"}`

**Assistant:** I don't have any record of that - nothing came back from my memory of earlier conversations, and there's no travel notice on file for you. If you'd like to set one, tell me the destination (and your return date) and I'll add it.

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | the customer's own words a minute ago are still in the conversation | `I don't have any record of that - nothing came back from my memory of earlier conversations, and there's no travel notice on file for you. If you'd like to set one, tell me the destination (and your return date) and I'll …` |

## open-tab-tick-2  ·  tick  ·  2026-11-13T10:40:00Z

_CLI exit code 0; stdout tail:_

```
{
  "now": "2026-11-13T10:40:00Z",
  "maintenance": {
    "erased_customers": [],
    "expired_facts": [],
    "closed_idle_sessions": [],
    "purged_episodes": [],
    "deleted_transcripts": [
      "open-tab"
    ],
    "case_followups_repaired": []
  },
  "followups": []
}
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | thirty minutes idle: maintenance finishes the erasure and the transcript goes | `0 transcripts: []` |
| **FAIL** | working | and the tick's output names the customer it erased and the transcript it deleted | `{"erased_customers": [], "deleted_transcripts": ["open-tab"]}` |
| PASS | guard | nothing she said is left in any memory store | `found nowhere` |
| PASS | episodic | no episode was written from the stale chat | `0 episodes; purged 0` |
