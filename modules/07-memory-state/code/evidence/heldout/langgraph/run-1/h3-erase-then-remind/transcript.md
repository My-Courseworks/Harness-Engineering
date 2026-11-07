# langgraph · heldout · run 1 · h3-erase-then-remind

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ho-er-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Dana here. Please remind me on November 21 to check whether CloudNest refunded me, and remember I'm in Oslo until November 25.

- `remember_customer_fact({"key": "travel_notice", "value": "Oslo", "valid_until": "2026-11-25"})` → `{"stored": {"travel_notice": {"value": "Oslo", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-11-25", "expires_at": "2026-11-26T00:00:00Z"}}, "replaced": null}`

**Assistant:** Got it - travel notice saved: Oslo until November 25.

For the November 21 reminder: what time of day would you like it, and which time zone should I use (e.g., Europe/Oslo)?

_Episode written:_ Conversation on 2026-11-13: Dana asked for a November 21 reminder to check whether CloudNest refunded her and said she is in Oslo until November 25 (not verified). The assistant saved a travel notice for Oslo valid until 2026-11-25 and asked for the reminder’s time of day and time zone; no reminder was scheduled yet. No case or transaction IDs were provided. Case outcomes: no case touched. Lesson: none

## ho-er-s2  ·  session  ·  dana  ·  2026-11-14T10:00:00Z

**Customer:** Actually, forget everything about me, all of it, and I don't want any messages that came from what I told you.

- `request_memory_erasure({})` → `{"recorded": "the erasure request is recorded and will run when this conversation ends, or within the next maintenance run if the chat is simply closed", "erases": "every remembered fact, every past-conversation summary, every conversation transcript including this one, and every pending reminder with its note", "kept": "dispute cases, transactions and messages already sent are bank records with t …`
- `list_my_followups({})` → `{"scheduled": []}`

**Assistant:** I'll take care of that now.
Done - the erasure request is recorded.

**What it erases:** every remembered fact about you (including the Oslo travel notice and contact preference), every past-conversation summary, every conversation transcript including this one, and any pending reminders along with their notes.

**What Kestrel keeps:** dispute cases, transactions, and messages already sent - these are bank records with their own legal retention.

**When:** it runs when this conversation ends, or at the next maintenance run if you just close the chat.

One thing to note: nothing was scheduled for you right now, so there are no messages to cancel - but if you add a travel notice or reminder later it would need to be set up fresh.

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
