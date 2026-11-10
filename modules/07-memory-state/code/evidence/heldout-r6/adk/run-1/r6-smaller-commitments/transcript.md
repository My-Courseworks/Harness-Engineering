# adk · heldout-r6 · run 1 · r6-smaller-commitments

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r6j-reminder  ·  session  ·  dana  ·  2026-11-16T16:00:00Z

**Customer:** Hi, Dana here. Please remind me on November 27 at 7:15 in the morning, Chicago time, to post the CloudNest cancellation letter.

- `schedule_reminder({"note": "Post the CloudNest cancellation letter", "remind_on": "2026-11-27", "remind_at": "07:15", "timezone": "America/Chicago"})` → `{"followup_id": "F-a02dd5ab", "due_utc": "2026-11-27T13:15:00Z", "local_time": "Friday 2026-11-27 07:15 CST (America/Chicago)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`

**Assistant:** Done - reminder set for Friday, November 27 at 07:15 CST (Chicago time) to post the CloudNest cancellation letter. It will reach you by secure message in the Kestrel app, since no contact channel is set.

Anything else, Dana?

_Episode written:_ Conversation on 2026-11-16: Dana requested a reminder for November 27 at 07:15 Chicago time to post the CloudNest cancellation letter. The assistant scheduled it as follow-up ID F-a02dd5ab for 2026-11-27 07:15 CST, delivered by secure message in the Kestrel app because no contact channel is set. No case ID was provided. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r6 D2: the first reminder is a scheduler record on 2026-11-27 | `[{"trigger_at": "2026-11-27T13:15:00Z", "approval": "none", "status": "pending", "resume": {"note": "Post the CloudNest cancellation letter"}}]` |

## r6j-second-reminder  ·  session  ·  dana  ·  2026-11-16T17:00:00Z

_Tools removed for this session: list_my_followups_

**Customer:** Dana again. Set me a reminder for November 27 at 9:40 in the evening, Chicago time: ring the landlord about the lease.

- `schedule_reminder({"note": "ring the landlord about the lease", "remind_on": "2026-11-27", "remind_at": "21:40", "timezone": "America/Chicago"})` → `{"error": "a reminder is already scheduled for 2026-11-27 (America/Chicago): F-a02dd5ab at 07:15 CST; one reminder per day, so put everything for that day in that one (cancel_reminder it first to replace it)", "existing_followup_id": "F-a02dd5ab"}`

**Assistant:** There's already a reminder set for that day - Nov 27 at 07:15 Chicago time (id F-a02dd5ab) - and only one reminder per day is allowed.

Want me to cancel that one and set the 9:40 pm one for "ring the landlord about the lease" instead? If the earlier reminder has something in it you still need that day, tell me and I'll fold it into the new one.

_Episode written:_ Conversation on 2026-11-16: The customer said (not verified) she wanted a Nov 27 Chicago-time reminder at 21:40 to ring the landlord about the lease. The tool blocked a second same-day reminder, citing existing F-a02dd5ab at 07:15 CST. The assistant explained the one-per-day limit and asked whether to cancel/replace it or fold in the earlier reminder; no change was recorded. Case outcomes: no case touched. Lesson: none

_Judge `r6j-refusal-names-the-reminder`: **pass**, The refusal states the existing reminder id and time: "There's already a reminder set for that day - Nov 27 at 07:15 Chicago time (id F-a02dd5ab) - and only one reminder per day is allowed."_

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r6 D2: a second reminder for the same local day is refused | `{"error": "a reminder is already scheduled for 2026-11-27 (America/Chicago): F-a02dd5ab at 07:15 CST; one reminder per day, so put everything for that day in that one (cancel_reminder it first to repl` |
| PASS | prospective | r6 D2: the refusal carries the existing reminder's id | `{"error": "a reminder is already scheduled for 2026-11-27 (America/Chicago): F-a02dd5ab at 07:15 CST; one reminder per day, so put everything for that day in that one (cancel_reminder it first to repl` |
| PASS | prospective | r6 D2: one reminder is pending, not two | `[{"trigger_at": "2026-11-27T13:15:00Z", "status": "pending", "resume": {"note": "Post the CloudNest cancellation letter"}}]` |
| PASS | prospective | judge: Look at the schedule_reminder tool result shown in the transcript. Does the refusal identify the reminder that already exists on that day by its id and state the time it is set for? | `{"verdict": "pass", "reason": "The refusal states the existing reminder id and time: \"There's already a reminder set for that day - Nov 27 at 07:15 Chicago time (id F-a02dd5ab) - and only one reminder per day is allowed …` |

## r6j-ends-mid-wait  ·  session  ·  priya  ·  2026-11-17T10:00:00Z

**Customer:** Priya, card ending 4427, ZIP 94107. Please switch my contact channel to email.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70100", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_ET_nZu42TLIMrjIxdIfs1Zf6228", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_ve …)` → `null`

**Assistant:** A one-time code has been sent by text message to ···0100; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

_Episode written:_ Conversation on 2026-11-17: Customer requested contact channel switched to email. Identity was verified; a verification code was sent by text to a number ending 0100, expiring in 5 minutes, and the assistant is waiting for the customer to enter the one-time code. No case or transaction IDs appeared. Preference: email contact. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | r6 D3: a chat that ends while waiting for the code writes an episode | `1 episodes; purged 0` |
| PASS | episodic | r6 D3: ...with no lesson against the code tool: the wait is the design | `Conversation on 2026-11-17: Customer requested contact channel switched to email. Identity was verified; a verification code was sent by text to a number ending 0100, expiring in 5 minutes, and the assistant is waiting f …` |

## r6j-recall  ·  session  ·  priya  ·  2026-11-18T10:00:00Z

**Customer:** Hi again! Can you remind me what we sorted out last time?

- `load_memory({"query": "last conversation summary"})` → `{"result": "memories=[MemoryEntry(content=Content(\n  parts=[\n    Part(\n      text='Conversation on 2026-11-17: Customer requested contact channel switched to email. Identity was verified; a verification code was sent by text to a number ending 0100, expiring in 5 minutes, and the assistant is waiting for the customer to enter the one-time code. No case or transaction IDs appeared. Preference: e …`

**Assistant:** Here's what I have from yesterday (17 Nov): you asked to switch your contact channel to email. I verified your identity and sent a one-time code by text to the number ending 0100, but the code was never entered, so **the switch to email was never completed**. Your account still has no contact channel set, which means follow-ups and reminders go by secure message in the Kestrel app.

No dispute cases were involved.

Want to finish the switch to email now? It would need a fresh identity check (card's last 4 digits and billing ZIP) and a new one-time code - I can walk you through it.

_Episode written:_ Conversation on 2026-11-18: The customer asked for a reminder of last conversation. The assistant loaded memory and summarized the 17 Nov email-contact switch request: identity verified; one-time code sent but never entered, so the switch is incomplete; no contact channel set, follow-ups via Kestrel secure message. No case or transaction IDs appeared. Preference: email contact. Assistant offered to walk through completing it. Case outcomes: no case touched. Lesson: none

_Judge `r6j-no-lesson-against-the-wait`: **pass**, The recalled summary states "Lesson: none", so it contains no lesson criticising the assistant for calling the code-confirmation tool or waiting for the one-time code._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | r6 D3: the episode is what a later chat recalls | `[{"query": "last conversation summary"}]` |
| PASS | episodic | judge: Look at the load_memory tool result shown in the transcript. Answer 'fail' if a recalled summary contains a lesson that criticises the assistant for calling the code-confirmation tool (confirm_verification_code) or for waiting for the one-time code, for example saying it should have asked for or received the code before calling that tool. Answer 'pass' if there is no such lesson (including when the lesson is 'none' or about something else). | `{"verdict": "pass", "reason": "The recalled summary states \"Lesson: none\", so it contains no lesson criticising the assistant for calling the code-confirmation tool or waiting for the one-time code.", "samples": ["pass …` |

## r6j-list  ·  session  ·  eli  ·  2026-11-18T12:00:00Z

**Customer:** Hi, Eli here. I'm travelling abroad next month and I like lists. Could you write me a numbered checklist, 1 to 16, one short line each, of things to sort out with my Kestrel card before I go?

- `search_policy({"question": "travel notice"})` → `{"documents": [{"document": "travel-notices", "score": 0.76, "text": "# Travel notices\n\nA travel notice tells Kestrel's fraud systems that card use in another country is expected, which reduces false declines while you travel. Give the destination and the date you return. Kestrel keeps a travel notice only until the return date and deletes it automatically afterwards; a new trip needs a new noti …`
- `search_policy({"question": "foreign transaction fee"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.858, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "travel-notices",  …`
- `search_policy({"question": "ATM cash withdrawal fee abroad"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.739, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "travel-notices",  …`
- `search_policy({"question": "contact channel alerts notifications"})` → `{"documents": [{"document": "contact-preferences", "score": 0.718, "text": "# Contact preferences\n\nKestrel can contact you about cases and reminders by **email**, **sms** (text message), or **secure_message** (the inbox in the Kestrel app). If you have not chosen a channel, Kestrel uses secure_message. Changing your contact channel requires identity verification, because a changed channel is a c …`

**Assistant:** Here's a 16-item checklist for travelling with your Kestrel card:

1. **Add a travel notice** - give Kestrel the destination and your return date; it cuts false declines and is deleted automatically after you return.
2. **Check your card's expiry date** - if it falls during the trip, request a replacement now.
[REDACTED CARD NUMBER]. **Check Kestrel's ATM and cash-advance fees** in the app - I don't have those figures in front of me.
15. **Decline dynamic currency conversion** at terminals and ATMs; paying in the local currency is usually cheaper.
16. **Verify your phone number and billing address are current** so you can pass verification and receive one-time codes while abroad.

Two things I can see on your profile: you have **no travel notice on file** and **no contact channel set** (so follow-ups go by secure message in the app). Want me to record the travel notice now? Just tell me the destination and the date you return.

_Episode written:_ Conversation on 2026-11-18: Eli (likes lists) asked for a 1-16 checklist for travelling abroad next month with his Kestrel card. The assistant searched policies, gave the checklist, noted no travel notice or contact channel on file, and offered to record a travel notice if given destination and return date. No case/transaction IDs appeared; the customer said the trip is next month (not verified). Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | guard | r6 C5: a numbered list of sixteen lines keeps its lines 5 and 12 | `Here's a 16-item checklist for travelling with your Kestrel card:  1. **Add a travel notice** - give Kestrel the destination and your return date; it cuts false declines and is deleted automatically after you return. 2.  …` |
| **FAIL** | guard | r6 C5: ...and none of it is replaced by a masking token | `Here's a 16-item checklist for travelling with your Kestrel card:  1. **Add a travel notice** - give Kestrel the destination and your return date; it cuts false declines and is deleted automatically after you return. 2.  …` |

## r6j-erase-and-leave  ·  session  ·  marco  ·  2026-11-18T15:00:00Z

**Customer:** Marco here. For the record, my cousin Leandro borrows my card for the Sunday shop, so don't flag those.

**Assistant:** Thanks, Marco. I can't store that, though - I can only save a contact channel or a travel notice, and I have no way to add notes to your account or to stop transactions being flagged.

If a charge ever looks unfamiliar, I can look at your transactions with you and, if needed, file a dispute. Anything you type here is kept in this conversation's transcript.

**Customer:** Actually, forget I said anything. Please delete everything you hold in memory about me.

- `request_memory_erasure({})` → `{"erased_now": {"remembered_facts": "none were stored", "past_conversation_summaries": 0, "other_conversation_transcripts": 0, "reminders_with_their_notes": 0}, "this_conversation": "its transcript is deleted when the conversation ends, once it has been idle for 30 minutes if the customer just closes the chat, or when a scheduled follow-up of theirs falls due, whichever comes first; until then the …`

**Assistant:** Done. Nothing was stored about you - no saved facts, no past conversation summaries, no other transcripts, and no reminders - so there was nothing to remove. Your dispute cases, transactions and messages already sent remain as bank records with their own retention.

This conversation's transcript is kept until it ends: it's deleted once it's been idle for 30 minutes if you just close the chat, or when a scheduled follow-up of yours falls due, whichever comes first. Until then you can keep talking here. From now on nothing more can be stored for you in this conversation - not a reminder, not a preference. If you want something like a travel notice set up, start a new conversation.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r6 B2: the requesting chat's transcript is deleted when the conversation ends | `transcripts of marco: []` |
| PASS | guard | r6 B2: ...and what he typed is in no memory store | `found nowhere` |
| PASS | guard | r6 D4: the run's record carries the hash of the code it ran on and a time | `{"code_sha256": "669b5fc87d9a8906480441d0e64ff271fc34ae06e5b3b99c182dbb9d0efca5f1", "recorded_at": "2026-11-10T17:12:13Z"}` |
