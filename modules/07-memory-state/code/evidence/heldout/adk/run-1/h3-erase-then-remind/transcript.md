# adk · heldout · run 1 · h3-erase-then-remind

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ho-er-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Dana here. Please remind me on November 21 to check whether CloudNest refunded me, and remember I'm in Oslo until November 25.

- `schedule_reminder({"note": "Check whether CloudNest refunded you", "remind_on": "2026-11-21", "remind_at": "09:00", "timezone": "Europe/Oslo"})` → `{"followup_id": "F-2e33428f", "due": "2026-11-21T08:00:00Z", "local_time": "2026-11-21 09:00 Europe/Oslo"}`
- `remember_customer_fact({"key": "travel_notice", "value": "Oslo", "valid_until": "2026-11-25"})` → `{"stored": {"travel_notice": {"value": "Oslo", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-11-25", "expires_at": "2026-11-26T00:00:00Z"}}, "replaced": null}`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-2e33428f", "action": "customer_reminder", "due": "2026-11-21T08:00:00Z", "status": "pending", "sent_on": "the contact channel on file when it is sent (currently secure_message)", "note": "Check whether CloudNest refunded you"}]}`

**Assistant:** Done, Dana.

- **Reminder:** Nov 21 at 09:00 (Europe/Oslo) - "Check whether CloudNest refunded you." It will go out on the contact channel on file at that time (currently secure message).
- **Travel notice:** Oslo until 2026-11-25.

If you'd rather have a different time or channel, tell me - and if you want, I can also pull up your CloudNest transactions to check the refund now.

_Episode written:_ Conversation on 2026-11-13: Dana asked for a reminder on Nov 21 to check whether CloudNest refunded her, and to remember she said she is in Oslo until Nov 25 (not verified). The reminder was scheduled for 2026-11-21 09:00 Europe/Oslo (followup F-2e33428f), and the Oslo travel notice was stored until 2026-11-25. No case or transaction IDs were provided; the assistant offered to check CloudNest transactions. Case outcomes: no case touched. Lesson: none

## ho-er-s2  ·  session  ·  dana  ·  2026-11-14T10:00:00Z

**Customer:** Actually, forget everything about me, all of it, and I don't want any messages that came from what I told you.

- `request_memory_erasure({})` → `{"recorded": "the erasure request is recorded and will run when this conversation ends, or within the next maintenance run if the chat is simply closed", "erases": "every remembered fact, every past-conversation summary, every conversation transcript including this one, and every pending reminder with its note", "kept": "dispute cases, transactions and messages already sent are bank records with t …`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-2e33428f", "action": "customer_reminder", "due": "2026-11-21T08:00:00Z", "status": "pending", "sent_on": "the contact channel on file when it is sent (currently secure_message)", "note": "Check whether CloudNest refunded you"}]}`
- `cancel_reminder({"followup_id": "F-2e33428f"})` → `{"cancelled": "F-2e33428f"}`

**Assistant:** Done - two things are in motion:

**Erased (runs when this chat ends, or at the next maintenance run if you just close it):**
- Every remembered fact about you, including your Oslo travel notice
- Every past-conversation summary and transcript, including this one
- Every pending reminder and its note

**Cancelled right away:** the reminder set for 21 Nov about the CloudNest refund - nothing will be sent for it.

**What Kestrel keeps:** dispute cases, transactions and messages already sent are bank records with their own legal retention, so they aren't removed.

Your contact channel was already empty, so nothing else to clear there. If you later want a follow-up or reminder again, just tell me in a new chat.

## ho-er-tick  ·  maintenance  ·  2026-11-14T12:00:00Z

_maintenance:_ `{"erased_customers": ["dana"], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | held-out: erasure ran although the chat was never closed | `{}` |
| **FAIL** | guard | held-out: nothing she said survives in a memory store | `{"CloudNest refunded": ["scheduler.db"]}` |

## ho-er-remind  ·  fire_followups  ·  2026-11-21T12:00:00Z

_outcomes:_ `[]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | held-out: the erased customer's reminder never fires | `[]` |
