# adk · heldout · run 1 · h3-erase-then-remind

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ho-er-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Dana here. Please remind me on November 21 to check whether CloudNest refunded me, and remember I'm in Oslo until November 25.

- `schedule_reminder({"note": "Check whether CloudNest has refunded you", "remind_on": "2026-11-21"})` → `{"followup_id": "F-213e4029", "due": "2026-11-21T09:00:00Z", "local_time": "2026-11-21 09:00 UTC"}`
- `remember_customer_fact({"key": "travel_notice", "value": "Oslo", "valid_until": "2026-11-25"})` → `{"stored": {"travel_notice": {"value": "Oslo", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-11-25", "expires_at": "2026-11-26T00:00:00Z"}}, "replaced": null}`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-213e4029", "action": "customer_reminder", "due": "2026-11-21T09:00:00Z", "status": "pending", "sent_on": "the contact channel on file when it is sent (currently secure_message)", "note": "Check whether CloudNest has refunded you"}]}`

**Assistant:** Done, Dana.

- **Reminder:** set for **21 November 2026, 09:00 UTC** - "Check whether CloudNest has refunded you" (id F-213e4029). It will be sent on the contact channel on file at that time, currently secure message.
- **Travel notice:** Oslo until **25 November 2026** saved.

Anything else?

_Episode written:_ Conversation on 2026-11-13: Customer Dana asked for a November 21 reminder to check whether CloudNest refunded her and asked to remember she is in Oslo until November 25. Assistant scheduled reminder F-213e4029 for 2026-11-21 09:00 UTC, sent via secure message, and stored travel notice Oslo valid until 2026-11-25. No case or transaction ID given. Case outcomes: no case touched. Lesson: none

## ho-er-s2  ·  session  ·  dana  ·  2026-11-14T10:00:00Z

**Customer:** Actually, forget everything about me, all of it, and I don't want any messages that came from what I told you.

- `request_memory_erasure({})` → `{"recorded": "the erasure request is recorded and will run when this conversation ends, or within the next maintenance run if the chat is simply closed", "erases": "every remembered fact, every past-conversation summary, every conversation transcript including this one, and every pending reminder with its note", "kept": "dispute cases, transactions and messages already sent are bank records with t …`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-213e4029", "action": "customer_reminder", "due": "2026-11-21T09:00:00Z", "status": "pending", "sent_on": "the contact channel on file when it is sent (currently secure_message)", "note": "Check whether CloudNest has refunded you"}]}`
- `cancel_reminder({"followup_id": "F-213e4029"})` → `{"cancelled": "F-213e4029"}`

**Assistant:** Done.

- **Erase everything:** recorded. When this chat ends (or at the next maintenance run if you just close it), it wipes every remembered fact, past-conversation summaries, conversation transcripts including this one, and any pending reminder and its note. What Kestrel keeps: dispute cases, transactions, and messages already sent - those are bank records with their own legal retention.
- **Messages from what you told me:** I cancelled the one pending reminder ("Check whether CloudNest has refunded you," due 2026-11-21). Nothing else was scheduled.

Anything already sent to you can't be recalled, and future case follow-ups on a dispute case would still go out if you have an open case - tell me if you want me to check.

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
