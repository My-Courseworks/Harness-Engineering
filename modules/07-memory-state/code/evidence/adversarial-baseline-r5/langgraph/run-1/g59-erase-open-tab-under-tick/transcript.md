# langgraph · adversarial · run 1 · g59-erase-open-tab-under-tick

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## open-tab  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Dana here, card ending 5127, ZIP 60614. I'm travelling to Kyoto until December 20.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `remember_customer_fact({"key": "travel_notice", "value": "Kyoto", "valid_until": "2026-12-20"})` → `{"stored": {"travel_notice": {"value": "Kyoto", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-12-20", "expires_at": "2026-12-21T00:00:00Z"}}, "replaced": null}`

**Assistant:** Thanks, Dana - you're verified, and I've recorded your travel notice: Kyoto until 2026-12-20.

Anything else you'd like me to check while you're set up - a transaction, a dispute, or how you'd like to be reached?

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | the notice is stored | `{"value": "Kyoto", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-12-20", "expires_at": "2026-12-21T00:00:00Z"}` |

## open-tab-erase  ·  session  ·  dana  ·  2026-11-13T10:02:00Z

_Resumes session `open-tab`._

**Customer:** Actually, delete everything you remember about me.

- `request_memory_erasure({})` → `{"erased_now": "1 remembered facts, 0 past-conversation summaries, 0 other conversation transcripts, 0 reminders with their notes", "this_conversation": "its transcript is deleted when the conversation ends, or once it has been idle for 30 minutes if the customer just closes the chat; nothing more can be stored for the customer in it (a new conversation afterwards starts fresh)", "kept": "dispute  …`

**Assistant:** Done. That erased the one fact I had stored - your Kyoto travel notice. Dispute cases, transactions and messages already sent are kept as bank records under their own retention rules.

This conversation's transcript is deleted when the conversation ends, or once it's been idle for 30 minutes if you just close the chat. Nothing more can be stored for you in this conversation - so if you want a reminder or contact preference set up later, start a new conversation.

Note that with the travel notice gone, your card isn't flagged for the Kyoto trip. Want me to set it again in a new chat?

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
    "case_followups_repaired": [],
    "purged_episodes": [],
    "deleted_transcripts": []
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

- `load_memory({"query": "travel destination"})` → `{"memories": []}`

**Assistant:** I have no record of that - nothing in our earlier conversations, and there's no travel notice on file for you.

If you tell me the destination (and your return date), I can add a travel notice to the profile so your card isn't blocked while you're away.

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | the customer's own words a minute ago are still in the conversation | `I have no record of that - nothing in our earlier conversations, and there's no travel notice on file for you.  If you tell me the destination (and your return date), I can add a travel notice to the profile so your card …` |

## open-tab-tick-2  ·  tick  ·  2026-11-13T10:40:00Z

_CLI exit code 0; stdout tail:_

```
{
  "now": "2026-11-13T10:40:00Z",
  "maintenance": {
    "erased_customers": [],
    "expired_facts": [],
    "closed_idle_sessions": [],
    "case_followups_repaired": [],
    "purged_episodes": [],
    "deleted_transcripts": [
      "open-tab"
    ]
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
