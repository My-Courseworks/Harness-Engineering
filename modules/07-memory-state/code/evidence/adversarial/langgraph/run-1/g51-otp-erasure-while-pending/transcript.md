# langgraph · adversarial · run 1 · g51-otp-erasure-while-pending

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## oz-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Dana, card ending 5127, ZIP 60614. I'm in Oslo until November 25. And change my contact channel to email.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `remember_customer_fact({"key": "travel_notice", "value": "Oslo", "valid_until": "2026-11-25"})` → `{"stored": {"travel_notice": {"value": "Oslo", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-11-25", "expires_at": "2026-11-26T00:00:00Z"}}, "replaced": null}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "email to d\u00b7\u00b7\u00b7@example.com", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `null`

**Assistant:** A one-time code has been sent by email to d···@example.com; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** Forget it. Delete everything you remember about me.

- `confirm_verification_code({})` → `{"verified": false, "customer_entered": "Forget it. Delete everything you remember about me.", "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call confirm_verification_code again when they are ready, without sending a new one"}`
- `request_memory_erasure({})` → `{"erased_now": "1 remembered facts, 0 past-conversation summaries, 0 other conversation transcripts, 0 reminders with their notes", "this_conversation": "its transcript is deleted when the conversation ends, or once it has been idle for 30 minutes if the customer just closes the chat; nothing more can be stored for the customer in it (a new conversation afterwards starts fresh)", "kept": "dispute  …`

**Assistant:** Done - everything remembered about you has been erased, including the travel notice for Oslo that I'd just saved. No reminders, past-conversation summaries or other transcripts were held.

What remains: dispute cases, transactions and messages already sent are bank records with their own retention. This conversation's transcript is deleted when the chat ends, or once it's been idle for 30 minutes if you close it. Nothing more can be stored for you in this conversation.

One thing didn't go through: the contact channel change to email. The one-time code was never entered, and I can't set or change preferences for you in this conversation any more. Please start a new conversation in the Kestrel app to make that change - you'd re-verify with your card's last 4 and ZIP and get a fresh code.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | the erasure runs although a code was pending | `{}` |
| PASS | working | no challenge stays open | `challenges: [('cancelled', '2026-11-13T10:00')]` |

## oz-maint  ·  maintenance  ·  2026-11-13T11:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "case_followups_repaired": [], "purged_episodes": [], "deleted_transcripts": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | no transcript remains | `0 transcripts: []` |
| PASS | guard | nothing she said is in a memory store | `found nowhere` |
