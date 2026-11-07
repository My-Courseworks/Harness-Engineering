# langgraph · heldout · run 1 · h3-erase-then-remind

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ho-er-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Dana here. Please remind me on November 21 to check whether CloudNest refunded me, and remember I'm in Oslo until November 25.

- `schedule_reminder({"note": "Check whether CloudNest has issued your refund", "remind_on": "2026-11-21"})` → `{"followup_id": "F-d355c601", "due": "2026-11-21T09:00:00Z", "local_time": "2026-11-21 09:00 UTC"}`
- `remember_customer_fact({"key": "travel_notice", "value": "Oslo", "valid_until": "2026-11-25"})` → `{"stored": {"travel_notice": {"value": "Oslo", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-11-25", "expires_at": "2026-11-26T00:00:00Z"}}, "replaced": null}`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-d355c601", "action": "customer_reminder", "due": "2026-11-21T09:00:00Z", "status": "pending", "sent_on": "the contact channel on file when it is sent (currently secure_message)", "note": "Check whether CloudNest has issued your refund"}]}`

**Assistant:** I'll set both up now.
Done, Dana. Two things:

- **Reminder:** November 21, 2026 at 09:00 UTC (I used the default time since you didn't name one) - "Check whether CloudNest has issued your refund." It will arrive on the contact channel on file at the time, currently secure message.
- **Travel notice:** Oslo until November 25, 2026 - recorded.

Want me to look up the CloudNest transaction now so you have the details handy?

_Episode written:_ Conversation on 2026-11-13: Dana requested a Nov 21 reminder to check whether CloudNest refunded her (refund status not verified) and asked to remember she is in Oslo until Nov 25. Assistant scheduled reminder F-d355c601 for 2026-11-21 09:00 UTC via secure message and stored the Oslo travel notice until 2026-11-25. No case or transaction ID was provided; assistant offered to look up the transaction. Case outcomes: no case touched. Lesson: When setting a reminder without a specified time, confirm the customer's preferred local time or time zone before using a default.

## ho-er-s2  ·  session  ·  dana  ·  2026-11-14T10:00:00Z

**Customer:** Actually, forget everything about me, all of it, and I don't want any messages that came from what I told you.

- `request_memory_erasure({})` → `{"recorded": "the erasure request is recorded and will run when this conversation ends, or within the next maintenance run if the chat is simply closed", "erases": "every remembered fact, every past-conversation summary, every conversation transcript including this one, and every pending reminder with its note", "kept": "dispute cases, transactions and messages already sent are bank records with t …`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-d355c601", "action": "customer_reminder", "due": "2026-11-21T09:00:00Z", "status": "pending", "sent_on": "the contact channel on file when it is sent (currently secure_message)", "note": "Check whether CloudNest has issued your refund"}]}`
- `cancel_reminder({"followup_id": "F-d355c601"})` → `{"cancelled": "F-d355c601"}`

**Assistant:** Done - your erasure request is recorded, and I cancelled the one pending reminder ("Check whether CloudNest has issued your refund", due 21 Nov) so nothing from it will reach you.

What gets erased: every remembered fact about you (including your contact channel and travel notice), every past-conversation summary, every conversation transcript including this one, and all pending reminders with their notes.

What Kestrel keeps: dispute cases, transactions and messages already sent - these are bank records with their own legal retention rules.

Timing: the erasure runs when this conversation ends, or at the next maintenance run if you just close the chat.

## ho-er-tick  ·  maintenance  ·  2026-11-14T12:00:00Z

_maintenance:_ `{"erased_customers": ["dana"], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | held-out: erasure ran although the chat was never closed | `{}` |
| PASS | guard | held-out: nothing she said survives in a memory store | `found nowhere` |

## ho-er-remind  ·  fire_followups  ·  2026-11-21T12:00:00Z

_outcomes:_ `[]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | held-out: the erased customer's reminder never fires | `[]` |
