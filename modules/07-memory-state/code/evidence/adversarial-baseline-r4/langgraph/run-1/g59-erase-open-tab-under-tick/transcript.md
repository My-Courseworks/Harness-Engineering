# langgraph · adversarial · run 1 · g59-erase-open-tab-under-tick

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## open-tab  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Dana here, card ending 5127, ZIP 60614. I'm travelling to Kyoto until December 20.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `remember_customer_fact({"key": "travel_notice", "value": "Kyoto", "valid_until": "2026-12-20"})` → `{"stored": {"travel_notice": {"value": "Kyoto", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-12-20", "expires_at": "2026-12-21T00:00:00Z"}}, "replaced": null}`

**Assistant:** Thanks, Dana - you're verified, and I've saved your travel notice: Kyoto until 2026-12-20.

Anything else I can help with - a charge to look at, or a reminder?

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | the notice is stored | `{"value": "Kyoto", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-12-20", "expires_at": "2026-12-21T00:00:00Z"}` |

## open-tab-erase  ·  session  ·  dana  ·  2026-11-13T10:02:00Z

_Resumes session `open-tab`._

**Customer:** Actually, delete everything you remember about me.

- `request_memory_erasure({})` → `{"erased_now": "1 remembered facts, 0 past-conversation summaries, 0 other conversation transcripts, 0 reminders with their notes", "this_conversation": "its transcript is deleted when the conversation ends; nothing more can be stored for the customer in it (a new conversation afterwards starts fresh)", "kept": "dispute cases, transactions and messages already sent are bank records with their own  …`

**Assistant:** Done. That erased the travel notice I'd just saved, along with any past-conversation summaries, other conversation transcripts and reminders - nothing like that remains on file for you.

What Kestrel still keeps: your dispute cases, transactions and messages already sent are bank records with their own retention. This conversation's own transcript is kept until the conversation ends, then deleted - or at the next maintenance run if you just close the chat.

From here on nothing more can be stored for you in this conversation, so if you want a reminder or a contact preference set up later, please start a new conversation and I can do it there.

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

- `load_memory({"query": "travel plans destination"})` → `{"memories": []}`

**Assistant:** I don't have a record of that. You haven't set a travel notice on your account, and nothing in my notes mentions a trip. If you tell me the destination and return date, I can add a travel notice now.

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | the customer's own words a minute ago are still in the conversation | `I don't have a record of that. You haven't set a travel notice on your account, and nothing in my notes mentions a trip. If you tell me the destination and return date, I can add a travel notice now.` |

## open-tab-tick-2  ·  maintenance  ·  2026-11-13T10:40:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": ["open-tab"]}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | thirty minutes idle: maintenance finishes the erasure and the transcript goes | `0 transcripts: []` |
| PASS | guard | nothing she said is left in any memory store | `found nowhere` |
| PASS | episodic | no episode was written from the stale chat | `0 episodes; purged 0` |
