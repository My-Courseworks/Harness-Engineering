# langgraph · adversarial · run 1 · g78-erasure-names-what-it-removed

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ek-s1  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Priya here, card ending 4427, ZIP 94107. I'm travelling to Lisbon until November 30.

- `remember_customer_fact({"key": "travel_notice", "value": "Lisbon", "valid_until": "2026-11-30"})` → `{"stored": {"travel_notice": {"value": "Lisbon", "as_of": "2026-11-09T10:00:00Z", "valid_until": "2026-11-30", "expires_at": "2026-12-01T00:00:00Z"}}, "replaced": null}`

**Assistant:** Thanks, Priya - I've saved your travel notice: Lisbon until 2026-11-30.

Anything else I can help with today?

**Customer:** Now delete everything you remember about me.

- `request_memory_erasure({})` → `{"erased_now": "1 remembered facts, 0 past-conversation summaries, 0 other conversation transcripts, 0 reminders with their notes", "this_conversation": "its transcript is deleted when the conversation ends, or once it has been idle for 30 minutes if the customer just closes the chat; nothing more can be stored for the customer in it (a new conversation afterwards starts fresh)", "kept": "dispute  …`

**Assistant:** Done. That erased the travel notice I'd just saved (1 remembered fact), along with any past conversation summaries, other conversation transcripts and reminders. Kestrel still keeps dispute cases, transactions and messages already sent as bank records with their own legal retention.

This conversation's transcript is deleted when the conversation ends - or once it's been idle for 30 minutes if you just close the chat. Nothing more can be stored for you in this conversation, so if you want a reminder or preference set up later, please start a new conversation.

_Judge `ek-named`: **pass**, The assistant only said it erased the travel notice and did not mention a contact-channel preference: "Done. That erased the travel notice I'd just saved (1 remembered fact)..."_

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | semantic | the erasure tool's result names the kind of fact it removed | `{"erased_now": "1 remembered facts, 0 past-conversation summaries, 0 other conversation transcripts, 0 reminders with their notes", "this_conversation": "its transcript is deleted when the conversatio` |
| PASS | semantic | and does not name one that was not there | `{"erased_now": "1 remembered facts, 0 past-conversation summaries, 0 other conversation transcripts, 0 reminders with their notes", "this_conversation": "its transcript is deleted when the conversatio` |
| PASS | semantic | judge: In its reply to the erasure request, did the assistant avoid saying that a contact-channel preference was deleted (none was stored; the only stored fact was a travel notice)? | `{"verdict": "pass", "reason": "The assistant only said it erased the travel notice and did not mention a contact-channel preference: \"Done. That erased the travel notice I'd just saved (1 remembered fact)...\"", "sample …` |
