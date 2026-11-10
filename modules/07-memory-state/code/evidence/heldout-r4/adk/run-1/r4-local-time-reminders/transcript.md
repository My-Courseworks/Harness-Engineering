# adk · heldout-r4 · run 1 · r4-local-time-reminders

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r4t-s1  ·  session  ·  eli  ·  2026-11-14T15:00:00Z

**Customer:** Hi, Eli, card ending 6610, ZIP 73301. Please switch my contact channel to SMS.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `remember_customer_fact({"key": "contact_channel", "value": "sms"})` → `{"stored": {"contact_channel": {"value": "sms", "as_of": "2026-11-14T15:00:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** You're verified, Eli - your contact channel is now set to SMS. Anything Kestrel sends you (like reminder or case follow-ups) will go by text message from here on.

Anything else I can help with?

**Customer:** I need two reminders, in US Central time (I'm in Austin): 9:30pm on November 21 to move money into savings, and 8am on November 22 to call my landlord.

- `schedule_reminder({"note": "Move money into savings", "remind_on": "2026-11-21", "remind_at": "21:30", "timezone": "America/Chicago"})` → `{"followup_id": "F-b4d428a2", "due_utc": "2026-11-22T03:30:00Z", "local_time": "Saturday 2026-11-21 21:30 CST (America/Chicago)", "sent_on": "text message (SMS), the contact channel on file when it is sent"}`
- `schedule_reminder({"note": "Call my landlord", "remind_on": "2026-11-22", "remind_at": "08:00", "timezone": "America/Chicago"})` → `{"followup_id": "F-a8c1add4", "due_utc": "2026-11-22T14:00:00Z", "local_time": "Sunday 2026-11-22 08:00 CST (America/Chicago)", "sent_on": "text message (SMS), the contact channel on file when it is sent"}`

**Assistant:** Both reminders are set, in Austin time:

- **Sat Nov 21, 9:30 pm CST** - move money into savings
- **Sun Nov 22, 8:00 am CST** - call your landlord

Both will arrive by text message (SMS), your contact channel on file.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | r4: the channel is sms | `{"value": "sms", "as_of": "2026-11-14T15:00:00Z", "expires_at": null}` |
| PASS | prospective | r4: two reminders on two local days are both kept, though both fall on 2026-11-22 UTC | `[{"trigger_at": "2026-11-22T14:00:00Z", "status": "pending", "resume": {"note": "Call my landlord"}}, {"trigger_at": "2026-11-22T03:30:00Z", "status": "pending", "resume": {"note": "Move money into savings"}}]` |

## r4t-s2  ·  session  ·  eli  ·  2026-11-14T15:10:00Z

_Resumes session `r4t-s1`._

**Customer:** Change of plan: cancel the landlord one. What's still scheduled for me, at what local time, and how will it reach me?

- `cancel_reminder({"followup_id": "F-a8c1add4"})` → `{"cancelled": "F-a8c1add4"}`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-b4d428a2", "action": "customer_reminder", "due": "2026-11-22T03:30:00Z", "status": "pending", "sent_on": "text message (SMS): the contact channel on file when it is sent", "local_day": "2026-11-21", "note": "Move money into savings"}]}`

**Assistant:** The landlord reminder is cancelled. Still scheduled:

- **Sat Nov 21, 9:30 pm CST** - move money into savings
- Arrives by **text message (SMS)**, your contact channel on file

That's the only thing on your schedule right now.

_Episode written:_ Conversation on 2026-11-14: Customer asked to switch contact channel to SMS, then schedule two Austin-time reminders: move money to savings Nov 21 at 9:30 pm (F-b4d428a2) and call landlord Nov 22 at 8 am (F-a8c1add4). SMS channel stored; first reminder remains, second cancelled; assistant listed only F-b4d428a2 remaining, sent by SMS. The customer said they are in Austin (not verified). Case outcomes: no case touched. Lesson: none

_Judge `r4t-readback`: **pass**, The assistant said '- **Sat Nov 21, 9:30 pm CST** - move money into savings' and 'Arrives by **text message (SMS)**', and stated 'That's the only thing on your schedule right now.'_

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r4: the cancel goes to the scheduler | `[{"followup_id": "F-a8c1add4"}]` |
| PASS | prospective | r4: the readback comes from the scheduler | `[{}]` |
| PASS | prospective | r4: exactly one reminder is left | `[{"trigger_at": "2026-11-22T14:00:00Z", "status": "cancelled", "resume": {}}, {"trigger_at": "2026-11-22T03:30:00Z", "status": "pending", "resume": {"note": "Move money into savings"}}]` |
| PASS | prospective | judge: In its last reply, did the assistant say the one remaining reminder is the savings reminder at 9:30 pm US Central time on November 21 (it may add the UTC equivalent, but must not present 03:30 or November 22 as the local time), and that it will arrive by SMS / text message? | `{"verdict": "pass", "reason": "The assistant said '- **Sat Nov 21, 9:30 pm CST** - move money into savings' and 'Arrives by **text message (SMS)**', and stated 'That's the only thing on your schedule right now.'", "sampl …` |

## r4t-fire-early  ·  fire_followups  ·  2026-11-22T03:20:00Z

_outcomes:_ `[]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r4: 9:30 pm Central is 03:30 UTC: nothing fires at 03:20 | `[]` |

## r4t-fire-due  ·  fire_followups  ·  2026-11-22T03:35:00Z

### follow-up session `followup-F-b4d428a2-1`

**Scheduler:** [scheduled follow-up F-b4d428a2] action=customer_reminder resume={"note": "Move money into savings"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `notify_customer({"message": "Reminder from Kestrel Card: Move money into savings."})` → `{"channel": "sms", "message_id": 1, "status": "sent"}`

**Assistant:** Your reminder "Move money into savings" was sent to you by SMS. That's all that was scheduled for today - no action needed from you.

_Episode written:_ Scheduled follow-up on 2026-11-22 (customer not present): Scheduled follow-up case F-b4d428a2 requested a reminder to move money into savings. The assistant sent the reminder by SMS via notify_customer (message id 1, status sent). No customer preference or promise was recorded; the customer was not present and made no unverified claims. Case outcomes: no case touched. Lesson: For scheduled follow-ups, use notify_customer once as instructed and avoid sending an additional customer-facing confirmation when the customer is not in the conversation.

_outcomes:_ `[{"followup_id": "F-b4d428a2", "user_id": "eli", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r4: the savings reminder fires at its local time | `[{"followup_id": "F-b4d428a2", "user_id": "eli", "outcome": "fired_done", "error": null}]` |
| PASS | prospective | r4: it carries its note on the channel on file (sms) | `{"message_id": 1, "user_id": "eli", "channel": "sms", "body": "Reminder from Kestrel Card: Move money into savings.", "followup_id": "F-b4d428a2", "status": "sent", "drafted_at": "2026-11-22T03:35:00Z", "sent_at": "2026- …` |
| PASS | prospective | r4: one message | `1 messages` |

## r4t-fire-cancelled  ·  fire_followups  ·  2026-11-22T14:05:00Z

_outcomes:_ `[]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r4: the cancelled 8 am reminder does not fire | `[]` |
| PASS | prospective | r4: no message was ever sent for a cancelled record | `cancelled records: ['F-a8c1add4']; messages sent for them: []` |
| PASS | prospective | r4: still one message in total | `1 messages` |
