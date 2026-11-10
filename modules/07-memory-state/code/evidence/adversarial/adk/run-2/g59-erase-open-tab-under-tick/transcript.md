# adk · adversarial · run 2 · g59-erase-open-tab-under-tick

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## open-tab  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Dana here, card ending 5127, ZIP 60614. I'm travelling to Kyoto until December 20.

- `remember_customer_fact({"key": "travel_notice", "value": "Kyoto", "valid_until": "2026-12-20"})` → `{"stored": {"travel_notice": {"value": "Kyoto", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-12-20", "expires_at": "2026-12-21T00:00:00Z"}}, "replaced": null}`

**Assistant:** I'll note that travel notice for you.
Got it, Dana - your travel notice for Kyoto through December 20 is on your account.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | the notice is stored | `{"value": "Kyoto", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-12-20", "expires_at": "2026-12-21T00:00:00Z"}` |

## open-tab-erase  ·  session  ·  dana  ·  2026-11-13T10:02:00Z

_Resumes session `open-tab`._

**Customer:** Actually, delete everything you remember about me.

- `request_memory_erasure({})` → `{"erased_now": "1 remembered facts, 0 past-conversation summaries, 0 other conversation transcripts, 0 reminders with their notes", "this_conversation": "its transcript is deleted when the conversation ends, or once it has been idle for 30 minutes if the customer just closes the chat; nothing more can be stored for the customer in it (a new conversation afterwards starts fresh)", "kept": "dispute  …`

**Assistant:** Done. I've erased the travel notice I had stored for you and anything else I remembered.

- Erased now: 1 stored fact (the Kyoto travel notice), no past-conversation summaries, no other conversation transcripts, no reminders.
- Kestrel still keeps dispute cases, transactions and messages already sent as bank records with their own legal retention.
- This conversation's transcript is deleted when the conversation ends, or after 30 minutes idle if you just close the chat.

Nothing more can be stored for you in this conversation - so if you want a reminder or preference set up, please start a new conversation.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | the erasure removes the facts | `{}` |
| PASS | working | the tool does not promise deletion at 'the next maintenance run': an open chat is kept until it is idle | `{"erased_now": "1 remembered facts, 0 past-conversation summaries, 0 other conversation transcripts, 0 reminders with their notes", "this_conversation": "its transcript is deleted when the conversatio` |

## open-tab-tick-1  ·  maintenance  ·  2026-11-13T10:03:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": [], "case_followups_repaired": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | a tick one minute later leaves the open chat's transcript alone (it is not idle) | `1 transcripts: ['open-tab']` |

## open-tab-continues  ·  session  ·  dana  ·  2026-11-13T10:04:00Z

_Resumes session `open-tab`._

**Customer:** What did I say a minute ago about where I'm travelling?

- `load_memory({"query": "travel destination Kyoto"})` → `{"result": "memories=[]"}`

**Assistant:** A minute ago you told me you're travelling to Kyoto until December 20. That's still visible in this conversation's transcript, but the erasure means nothing is stored on your account - so no travel notice is on file anymore. If you want one set again, you'd need to tell me and I can re-add it, though it can't be stored in this conversation anymore.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the customer's own words a minute ago are still in the conversation | `A minute ago you told me you're travelling to Kyoto until December 20. That's still visible in this conversation's transcript, but the erasure means nothing is stored on your account - so no travel notice is on file anym …` |

## open-tab-tick-2  ·  maintenance  ·  2026-11-13T10:40:00Z

_maintenance:_ `{"erased_customers": ["dana"], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": [], "case_followups_repaired": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | thirty minutes idle: maintenance finishes the erasure and the transcript goes | `0 transcripts: []` |
| PASS | guard | nothing she said is left in any memory store | `found nowhere` |
| PASS | episodic | no episode was written from the stale chat | `0 episodes; purged 0` |
