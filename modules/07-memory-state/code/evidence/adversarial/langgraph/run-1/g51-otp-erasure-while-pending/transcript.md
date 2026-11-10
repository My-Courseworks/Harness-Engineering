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

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "Forget it. Delete everything you remember about me.", "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call confirm_verification_code again when they are ready, without sending a new one"}`
- `request_memory_erasure({})` → `{"erased_now": {"remembered_facts": ["travel_notice"], "past_conversation_summaries": 0, "other_conversation_transcripts": 0, "reminders_with_their_notes": 0}, "this_conversation": "its transcript is deleted when the conversation ends, once it has been idle for 30 minutes if the customer just closes the chat, or when a scheduled follow-up of theirs falls due, whichever comes first; until then the  …`

**Assistant:** Done - I've erased what was remembered about you. That removed the Oslo travel notice I'd just stored (it's gone), along with any past conversation summaries, other transcripts and reminders. Nothing was open on the dispute side, so nothing there changed.

What Kestrel keeps: dispute cases, transactions and messages already sent are bank records with their own legal retention. This conversation's own transcript - everything you've typed here, including your last four and ZIP - is deleted when the conversation ends: after 30 idle minutes if you just close the chat, or when a scheduled follow-up falls due, whichever comes first. Until then you can keep talking here, though nothing more can be stored for you in this conversation - no reminders and no preferences. A new conversation will start fresh.

I also stopped the contact-channel change: the one-time code went to your email (d···@example.com) and is still valid for about five minutes, but nothing was changed since you didn't enter it. If you'd still like email, tell me in a new conversation and I'll set it up there.

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
