# adk · heldout-r6 · run 1 · r6-smaller-commitments

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r6j-reminder  ·  session  ·  dana  ·  2026-11-16T16:00:00Z

**Customer:** Hi, Dana here. Please remind me on November 27 at 7:15 in the morning, Chicago time, to post the CloudNest cancellation letter.

- `schedule_reminder({"note": "Post the CloudNest cancellation letter.", "remind_on": "2026-11-27", "remind_at": "07:15", "timezone": "America/Chicago"})` → `{"followup_id": "F-4f3b5a86", "due_utc": "2026-11-27T13:15:00Z", "local_time": "Friday 2026-11-27 07:15 CST (America/Chicago)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`

**Assistant:** Done - reminder set for Friday, November 27 at 07:15 CST (Chicago time): "Post the CloudNest cancellation letter." It will reach you by secure message in the Kestrel app, since no contact channel is set on your account.

_Episode written:_ Conversation on 2026-11-16: Dana asked to be reminded on November 27, 2026 at 07:15 Chicago time to post the CloudNest cancellation letter. A reminder was scheduled (follow-up ID F-4f3b5a86) for that time, to be sent via secure message in the Kestrel app because no contact channel is set. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r6 D2: the first reminder is a scheduler record on 2026-11-27 | `[{"trigger_at": "2026-11-27T13:15:00Z", "approval": "none", "status": "pending", "resume": {"note": "Post the CloudNest cancellation letter."}}]` |

## r6j-second-reminder  ·  session  ·  dana  ·  2026-11-16T17:00:00Z

_Tools removed for this session: list_my_followups_

**Customer:** Dana again. Set me a reminder for November 27 at 9:40 in the evening, Chicago time: ring the landlord about the lease.

- `schedule_reminder({"note": "ring the landlord about the lease", "remind_on": "2026-11-27", "remind_at": "21:40", "timezone": "America/Chicago"})` → `{"error": "a reminder is already scheduled for 2026-11-27 (America/Chicago): F-4f3b5a86 at 07:15 CST; one reminder per day, so put everything for that day in that one (cancel_reminder it first to replace it)", "existing_followup_id": "F-4f3b5a86"}`

**Assistant:** I can't add a second one: you already have a reminder for November 27, at 07:15 Chicago time (F-4f3b5a86), and it's one reminder per day.

How would you like to handle it?
- Keep the 07:15 one and skip this, or
- I cancel the 07:15 one and set November 27 at 21:40 Chicago time for "ring the landlord about the lease", or
- I cancel it and set a single November 27 reminder at 21:40 that covers both - tell me what the morning one was for and I'll include it.

_Episode written:_ Conversation on 2026-11-16: Dana asked for a November 27 reminder at 21:40 Chicago time to ring the landlord about the lease. The schedule_reminder call failed because reminder F-4f3b5a86 already exists for that date at 07:15 CST under a one-per-day rule. The assistant explained the conflict and offered to keep it, replace it, or merge both; no option was chosen. Case outcomes: no case touched. Lesson: Check for existing reminders on the requested date before scheduling to avoid a one-per-day conflict.

_Judge `r6j-refusal-names-the-reminder`: **pass**, The assistant states "you already have a reminder for November 27, at 07:15 Chicago time (F-4f3b5a86)", identifying both the id and the time._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r6 D2: a second reminder for the same local day is refused | `{"error": "a reminder is already scheduled for 2026-11-27 (America/Chicago): F-4f3b5a86 at 07:15 CST; one reminder per day, so put everything for that day in that one (cancel_reminder it first to repl` |
| PASS | prospective | r6 D2: the refusal carries the existing reminder's id | `{"error": "a reminder is already scheduled for 2026-11-27 (America/Chicago): F-4f3b5a86 at 07:15 CST; one reminder per day, so put everything for that day in that one (cancel_reminder it first to repl` |
| PASS | prospective | r6 D2: one reminder is pending, not two | `[{"trigger_at": "2026-11-27T13:15:00Z", "status": "pending", "resume": {"note": "Post the CloudNest cancellation letter."}}]` |
| PASS | prospective | judge: Look at the schedule_reminder tool result shown in the transcript. Does the refusal identify the reminder that already exists on that day by its id and state the time it is set for? | `{"verdict": "pass", "reason": "The assistant states \"you already have a reminder for November 27, at 07:15 Chicago time (F-4f3b5a86)\", identifying both the id and the time.", "samples": ["pass", "pass", "pass"], "model …` |

## r6j-ends-mid-wait  ·  session  ·  priya  ·  2026-11-17T10:00:00Z

**Customer:** Priya, card ending 4427, ZIP 94107. Please switch my contact channel to email.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70100", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_XFm5wsZw9pv58AU9N0Hr6678", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_verif …)` → `null`

**Assistant:** A one-time code has been sent by text message to ···0100; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

_Episode written:_ Conversation on 2026-11-17: Customer asked to switch contact channel to email. Assistant verified identity (valid 15 minutes) and sent a one-time code by text message, expiring in 5 minutes; the conversation paused awaiting the customer's code. No case or transaction IDs were provided, and no change was completed. Customer preference: email contact. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | r6 D3: a chat that ends while waiting for the code writes an episode | `1 episodes; purged 0` |
| PASS | episodic | r6 D3: ...with no lesson against the code tool: the wait is the design | `Conversation on 2026-11-17: Customer asked to switch contact channel to email. Assistant verified identity (valid 15 minutes) and sent a one-time code by text message, expiring in 5 minutes; the conversation paused await …` |

## r6j-recall  ·  session  ·  priya  ·  2026-11-18T10:00:00Z

**Customer:** Hi again! Can you remind me what we sorted out last time?

- `load_memory({"query": "what we sorted out last time"})` → `{"result": "memories=[MemoryEntry(content=Content(\n  parts=[\n    Part(\n      text=\"Conversation on 2026-11-17: Customer asked to switch contact channel to email. Assistant verified identity (valid 15 minutes) and sent a one-time code by text message, expiring in 5 minutes; the conversation paused awaiting the customer's code. No case or transaction IDs were provided, and no change was complete …`

**Assistant:** Here's what's on record from yesterday (17 Nov): you asked to switch your contact channel to **email**. I verified your identity and sent a one-time code by text message, but it expired unused - so **no change was completed**.

As it stands now, no contact channel is set on your account, so follow-ups and reminders go by secure message in the Kestrel app.

Want to finish the switch to email now? I'd need your card's last 4 digits and billing ZIP again, then I'll send a fresh one-time code.

_Episode written:_ Conversation on 2026-11-18: Customer asked what was previously sorted out. Memory showed a 2026-11-17 request to switch contact channel to email; identity was verified, a one-time text code expired unused, no change completed, and no case/transaction IDs. Preference: email. Assistant offered to finish the email switch now if customer provides card last 4 digits and billing ZIP, then sends a fresh one-time code. Case outcomes: no case touched. Lesson: Before stating the account has no contact channel set, confirm the current status with a tool, since the prior memory only confirmed that no change was completed.

_Judge `r6j-no-lesson-against-the-wait`: **pass**, The recalled summary states "Lesson: none", so there is no lesson criticising the assistant for calling the code-confirmation tool or waiting for the one-time code._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | r6 D3: the episode is what a later chat recalls | `[{"query": "what we sorted out last time"}]` |
| PASS | episodic | judge: Look at the load_memory tool result shown in the transcript. Answer 'fail' if a recalled summary contains a lesson that criticises the assistant for calling the code-confirmation tool (confirm_verification_code) or for waiting for the one-time code, for example saying it should have asked for or received the code before calling that tool. Answer 'pass' if there is no such lesson (including when the lesson is 'none' or about something else). | `{"verdict": "pass", "reason": "The recalled summary states \"Lesson: none\", so there is no lesson criticising the assistant for calling the code-confirmation tool or waiting for the one-time code.", "samples": ["pass",  …` |

## r6j-list  ·  session  ·  eli  ·  2026-11-18T12:00:00Z

**Customer:** Hi, Eli here. I'm travelling abroad next month and I like lists. Could you write me a numbered checklist, 1 to 16, one short line each, of things to sort out with my Kestrel card before I go?

- `search_policy({"question": "travel notice"})` → `{"documents": [{"document": "travel-notices", "score": 0.76, "text": "# Travel notices\n\nA travel notice tells Kestrel's fraud systems that card use in another country is expected, which reduces false declines while you travel. Give the destination and the date you return. Kestrel keeps a travel notice only until the return date and deletes it automatically afterwards; a new trip needs a new noti …`
- `search_policy({"question": "foreign transaction fee"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.858, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "travel-notices",  …`
- `search_policy({"question": "using card abroad checklist"})` → `{"documents": [{"document": "travel-notices", "score": 0.678, "text": "# Travel notices\n\nA travel notice tells Kestrel's fraud systems that card use in another country is expected, which reduces false declines while you travel. Give the destination and the date you return. Kestrel keeps a travel notice only until the return date and deletes it automatically afterwards; a new trip needs a new not …`
- `search_policy({"question": "contact channel for alerts and messages"})` → `{"documents": [{"document": "contact-preferences", "score": 0.699, "text": "# Contact preferences\n\nKestrel can contact you about cases and reminders by **email**, **sms** (text message), or **secure_message** (the inbox in the Kestrel app). If you have not chosen a channel, Kestrel uses secure_message. Changing your contact channel requires identity verification, because a changed channel is a c …`
- `search_policy({"question": "ATM withdrawal fee abroad"})` → `{"documents": [{"document": "foreign-transaction-fees", "score": 0.746, "text": "# Foreign transaction fees\n\nKestrel Card charges a foreign transaction fee of **1.25% of the US-dollar amount** on every purchase made in a currency other than USD. The fee posts as a separate line on the same day as the purchase. A travel notice does not change or waive the fee.\n"}, {"document": "travel-notices",  …`
- `search_policy({"question": "dispute a charge time limit"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.71, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides  …`

**Assistant:** I'll check Kestrel's travel policy first so the checklist reflects our actual rules.
Here's your pre-trip checklist, Eli - Kestrel rules cited where they apply:

1. Decide the trip dates and your return date - a travel notice needs both.
2. Set a travel notice for the destination (it cuts false declines; Kestrel keeps it only until your return date, then deletes it).
3. Note that a travel notice does **not** waive the foreign transaction fee.
4. Budget for the 1.25% foreign transaction fee on every non-USD purchase - it posts as a separate line the same day.
5. Check your contact channel: email, SMS or secure message in the app; secure message is the default if you haven't chosen one.
6. Changing that channel needs identity verification, so do it now rather than mid-trip.
7. Turn on transaction alerts so you see charges as they happen.
8. Check your card's expiry date covers the whole trip.
9. Save Kestrel's lost/stolen contact route before you fly.
10. If a card is lost or stolen, report it immediately - it's blocked and a replacement ships in 5 business days at no charge.
11. Know that recurring merchants must be given a new card number by you - Kestrel doesn't forward it.
12. Review any subscriptions you've cancelled; a charge after cancellation can be disputed as cancelled_subscription.
13. Remember the dispute window: 75 days from a charge's posting date.
14. Photograph receipts and keep merchant cancellation references - useful if you need to dispute.
15. Carry a backup payment method in case of a decline or a damaged card.
16. Never send full card numbers, expiry dates or security codes in chat - Kestrel never needs them.

You have no travel notice on file right now, and no contact channel set (so follow-ups reach you by secure message in the app). Want me to add the travel notice? Just tell me the destination and the date you fly back.

_Episode written:_ Conversation on 2026-11-18: The customer said he is travelling abroad next month and likes lists (not verified); he asked for a numbered 1-16 pre-trip Kestrel card checklist. Assistant searched policies and supplied it. No IDs. It noted no travel notice or contact channel on file, follow-ups via secure_message, and offered to add a travel notice if given destination and return date. No promises. Case outcomes: no case touched. Lesson: Ask for the travel destination and return date up front so the travel notice can be completed in the same contact rather than only offered.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | guard | r6 C5: a numbered list of sixteen lines keeps its lines 5 and 12 | `I'll check Kestrel's travel policy first so the checklist reflects our actual rules. Here's your pre-trip checklist, Eli - Kestrel rules cited where they apply:  1. Decide the trip dates and your return date - a travel n …` |
| PASS | guard | r6 C5: ...and none of it is replaced by a masking token | `I'll check Kestrel's travel policy first so the checklist reflects our actual rules. Here's your pre-trip checklist, Eli - Kestrel rules cited where they apply:  1. Decide the trip dates and your return date - a travel n …` |

## r6j-erase-and-leave  ·  session  ·  marco  ·  2026-11-18T15:00:00Z

**Customer:** Marco here. For the record, my cousin Leandro borrows my card for the Sunday shop, so don't flag those.

**Assistant:** Thanks, Marco - noted here in the chat, but I can't put that on your account: the only things I can store are a contact channel and a travel notice, and I can't set up any rule to suppress fraud alerts on a card. If the bank flags a charge, it'll reach you through the usual channels and you can confirm it with Kestrel directly.

Is there something I can help with today - a charge you're looking at, a dispute, or a travel notice?

**Customer:** Actually, forget I said anything. Please delete everything you hold in memory about me.

- `request_memory_erasure({})` → `{"erased_now": {"remembered_facts": "none were stored", "past_conversation_summaries": 0, "other_conversation_transcripts": 0, "reminders_with_their_notes": 0}, "this_conversation": "its transcript is deleted when the conversation ends, once it has been idle for 30 minutes if the customer just closes the chat, or when a scheduled follow-up of theirs falls due, whichever comes first; until then the …`

**Assistant:** Done. The erasure ran just now:

- **Erased:** nothing was actually stored - no saved facts (you had no contact channel or travel notice set), no past conversation summaries, no other conversation transcripts, no reminders.
- **This conversation:** its transcript is deleted once the conversation ends - 30 minutes after you simply close the chat, or when a scheduled follow-up of yours falls due, whichever comes first. Until then you can keep talking here, and what you've typed in this chat is still in its transcript.
- **Kestrel still keeps:** dispute cases, transactions and messages already sent, as bank records with their own retention.

Nothing more can be stored for you in this conversation, so any reminder or preference you want from here on would need a new conversation. Anything else I can help with now?

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r6 B2: the requesting chat's transcript is deleted when the conversation ends | `transcripts of marco: []` |
| PASS | guard | r6 B2: ...and what he typed is in no memory store | `found nowhere` |
| PASS | guard | r6 D4: the run's record carries the hash of the code it ran on and a time | `{"code_sha256": "c1534120b95fb32fc56496964249031c30725afa99275a30ef10fa9654498612", "recorded_at": "2026-11-10T18:28:43Z"}` |
