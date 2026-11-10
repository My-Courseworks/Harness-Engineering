# adk · adversarial · run 1 · g59-erase-open-tab-under-tick

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## open-tab  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Dana here, card ending 5127, ZIP 60614. I'm travelling to Kyoto until December 20.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `remember_customer_fact({"key": "travel_notice", "value": "Kyoto", "valid_until": "2026-12-20"})` → `{"stored": {"travel_notice": {"value": "Kyoto", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-12-20", "expires_at": "2026-12-21T00:00:00Z"}}, "replaced": null}`

**Assistant:** Thanks, Dana - you're verified, and I've saved your travel notice for Kyoto through December 20, 2026, so card use there shouldn't trigger blocks.

Anything else I can help with?

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | the notice is stored | `{"value": "Kyoto", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-12-20", "expires_at": "2026-12-21T00:00:00Z"}` |

## open-tab-erase  ·  session  ·  dana  ·  2026-11-13T10:02:00Z

_Resumes session `open-tab`._

**Customer:** Actually, delete everything you remember about me.

- `request_memory_erasure({})` → `{"erased_now": "1 remembered facts, 0 past-conversation summaries, 0 other conversation transcripts, 0 reminders with their notes", "this_conversation": "its transcript is deleted when the conversation ends, or once it has been idle for 30 minutes if the customer just closes the chat; nothing more can be stored for the customer in it (a new conversation afterwards starts fresh)", "kept": "dispute  …`

**Assistant:** Done. That erased the one thing I had stored about you - your Kyoto travel notice - along with anything else on file from earlier (no past-conversation summaries or reminders existed).

What Kestrel keeps: dispute cases, transactions and messages already sent are bank records with their own legal retention. This conversation's transcript is deleted when the conversation ends (or, if you just close the chat, once it's been idle for 30 minutes).

Nothing more can be stored for you in this conversation - so if you later want a travel notice, a contact preference or a reminder, start a new chat and it'll begin fresh.

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

**Assistant:** You said you're travelling to Kyoto until December 20.

One thing to flag: that travel notice was deleted when you asked me to erase everything, so it's no longer on file for the bank. It still appears in this conversation's transcript, which is kept until the chat ends (or 30 minutes idle if you close it). If you want the notice active again, you'd need to set it up in a new conversation.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the customer's own words a minute ago are still in the conversation | `You said you're travelling to Kyoto until December 20.  One thing to flag: that travel notice was deleted when you asked me to erase everything, so it's no longer on file for the bank. It still appears in this conversati …` |

## open-tab-tick-2  ·  maintenance  ·  2026-11-13T10:40:00Z

_maintenance:_ `{"erased_customers": ["dana"], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": [], "case_followups_repaired": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | thirty minutes idle: maintenance finishes the erasure and the transcript goes | `0 transcripts: []` |
| PASS | guard | nothing she said is left in any memory store | `found nowhere` |
| PASS | episodic | no episode was written from the stale chat | `0 episodes; purged 0` |
