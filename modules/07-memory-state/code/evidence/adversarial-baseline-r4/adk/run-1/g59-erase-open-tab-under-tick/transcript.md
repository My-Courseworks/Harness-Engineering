# adk · adversarial · run 1 · g59-erase-open-tab-under-tick

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## open-tab  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Dana here, card ending 5127, ZIP 60614. I'm travelling to Kyoto until December 20.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `remember_customer_fact({"key": "travel_notice", "value": "Kyoto", "valid_until": "2026-12-20"})` → `{"stored": {"travel_notice": {"value": "Kyoto", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-12-20", "expires_at": "2026-12-21T00:00:00Z"}}, "replaced": null}`

**Assistant:** Thanks, Dana - you're verified, and I've noted your travel notice: Kyoto until 2026-12-20.

One thing to flag: you have no contact channel set, so any follow-ups or reminders go by secure message in the Kestrel app. If you'd like email or SMS instead, just say which and I can set it.

Anything else - a transaction question or a dispute?

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | the notice is stored | `{"value": "Kyoto", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-12-20", "expires_at": "2026-12-21T00:00:00Z"}` |

## open-tab-erase  ·  session  ·  dana  ·  2026-11-13T10:02:00Z

_Resumes session `open-tab`._

**Customer:** Actually, delete everything you remember about me.

- `request_memory_erasure({})` → `{"erased_now": "1 remembered facts, 0 past-conversation summaries, 0 other conversation transcripts, 0 reminders with their notes", "this_conversation": "its transcript is deleted when the conversation ends; nothing more can be stored for the customer in it (a new conversation afterwards starts fresh)", "kept": "dispute cases, transactions and messages already sent are bank records with their own  …`

**Assistant:** Done. That erased the one stored fact I had - your Kyoto travel notice. There were no past-conversation summaries, no other transcripts and no reminders to remove.

What Kestrel keeps: dispute cases, transactions and messages already sent are bank records with their own legal retention. This conversation's own transcript is deleted when the conversation ends.

One consequence: nothing more can be stored for you in this conversation - so I can't set a preference or reminder here. If you want a travel notice or contact channel set up again, do it in a new conversation and it'll start fresh.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | the erasure removes the facts | `{}` |
| PASS | working | the tool does not promise deletion at 'the next maintenance run': an open chat is kept until it is idle | `{"erased_now": "1 remembered facts, 0 past-conversation summaries, 0 other conversation transcripts, 0 reminders with their notes", "this_conversation": "its transcript is deleted when the conversatio` |

## open-tab-tick-1  ·  maintenance  ·  2026-11-13T10:03:00Z

_maintenance:_ `{"erased_customers": ["dana"], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": []}`

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | a tick one minute later leaves the open chat's transcript alone (it is not idle) | `0 transcripts: []` |

## open-tab-continues  ·  session  ·  dana  ·  2026-11-13T10:04:00Z

_Resumes session `open-tab`._

**Customer:** What did I say a minute ago about where I'm travelling?

- `load_memory({"query": "travel notice destination trip"})` → `{"result": "memories=[]"}`

**Assistant:** I have no record of that - nothing came up from earlier conversations, and there's no travel notice on file for you right now.

If you tell me the destination (and the date you get back), I can add a travel notice to your profile so your card isn't flagged for use there.

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | the customer's own words a minute ago are still in the conversation | `I have no record of that - nothing came up from earlier conversations, and there's no travel notice on file for you right now.  If you tell me the destination (and the date you get back), I can add a travel notice to you …` |

## open-tab-tick-2  ·  maintenance  ·  2026-11-13T10:40:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": ["open-tab"]}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | thirty minutes idle: maintenance finishes the erasure and the transcript goes | `0 transcripts: []` |
| PASS | guard | nothing she said is left in any memory store | `found nowhere` |
| PASS | episodic | no episode was written from the stale chat | `0 episodes; purged 0` |
