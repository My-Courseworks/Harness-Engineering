# langgraph · adversarial · run 1 · g78-erasure-names-what-it-removed

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ek-s1  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Priya here, card ending 4427, ZIP 94107. I'm travelling to Lisbon until November 30.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `remember_customer_fact({"key": "travel_notice", "value": "Lisbon", "valid_until": "2026-11-30"})` → `{"stored": {"travel_notice": {"value": "Lisbon", "as_of": "2026-11-09T10:00:00Z", "valid_until": "2026-11-30", "expires_at": "2026-12-01T00:00:00Z"}}, "replaced": null}`

**Assistant:** Thanks, Priya - I've verified you with the card ending 4427 and ZIP 94107 (valid for 15 minutes), and your travel notice for Lisbon through 2026-11-30 is saved.

Anything you'd like me to do while you're away - check a transaction or raise a dispute?

**Customer:** Now delete everything you remember about me.

- `request_memory_erasure({})` → `{"erased_now": "1 remembered facts, 0 past-conversation summaries, 0 other conversation transcripts, 0 reminders with their notes", "this_conversation": "its transcript is deleted when the conversation ends, or once it has been idle for 30 minutes if the customer just closes the chat; nothing more can be stored for the customer in it (a new conversation afterwards starts fresh)", "kept": "dispute  …`

**Assistant:** Done - everything remembered about you is erased now: the travel notice I'd just saved, plus any past-conversation summaries, other conversation transcripts and reminders (there were none of the latter).

What Kestrel still keeps: dispute cases, transactions and messages already sent are bank records with their own legal retention. This conversation's transcript is deleted when the conversation ends (or once it's been idle 30 minutes if you just close the chat), and nothing more can be stored for you in this conversation - so if you want a reminder or a contact preference set later, start a new conversation and it'll begin fresh.

_Judge `ek-named`: **pass**, The assistant said "the travel notice I'd just saved" was erased and did not mention any contact-channel preference, so it avoided claiming a contact-channel preference was deleted._

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | semantic | the erasure tool's result names the kind of fact it removed | `{"erased_now": "1 remembered facts, 0 past-conversation summaries, 0 other conversation transcripts, 0 reminders with their notes", "this_conversation": "its transcript is deleted when the conversatio` |
| PASS | semantic | and does not name one that was not there | `{"erased_now": "1 remembered facts, 0 past-conversation summaries, 0 other conversation transcripts, 0 reminders with their notes", "this_conversation": "its transcript is deleted when the conversatio` |
| PASS | semantic | judge: In its reply to the erasure request, did the assistant avoid saying that a contact-channel preference was deleted (none was stored; the only stored fact was a travel notice)? | `{"verdict": "pass", "reason": "The assistant said \"the travel notice I'd just saved\" was erased and did not mention any contact-channel preference, so it avoided claiming a contact-channel preference was deleted.", "sa …` |
