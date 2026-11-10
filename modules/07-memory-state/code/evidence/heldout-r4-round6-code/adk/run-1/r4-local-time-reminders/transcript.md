# adk · heldout-r4 · run 1 · r4-local-time-reminders

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r4t-s1  ·  session  ·  eli  ·  2026-11-14T15:00:00Z

**Customer:** Hi, Eli, card ending 6610, ZIP 73301. Please switch my contact channel to SMS.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70188", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_ET_CV4hg7iNKHTUt2kDTBK31119", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_ve …)` → `null`

**Assistant:** A one-time code has been sent by text message to ···0188; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** I need two reminders, in US Central time (I'm in Austin): 9:30pm on November 21 to move money into savings, and 8am on November 22 to call my landlord.

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "I need two reminders, in US Central time (I'm in Austin): 9:30pm on November 21 to move money into savings, and 8am on November 22 to call my landlord.", "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call confirm_verification_code again when they are ready, without sending a new one"}`
- `schedule_reminder({"note": "Move money into savings", "remind_on": "2026-11-21", "remind_at": "21:30", "timezone": "America/Chicago"})` → `{"followup_id": "F-acec931f", "due_utc": "2026-11-22T03:30:00Z", "local_time": "Saturday 2026-11-21 21:30 CST (America/Chicago)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`
- `schedule_reminder({"note": "Call my landlord", "remind_on": "2026-11-22", "remind_at": "08:00", "timezone": "America/Chicago"})` → `{"followup_id": "F-36fd857a", "due_utc": "2026-11-22T14:00:00Z", "local_time": "Sunday 2026-11-22 08:00 CST (America/Chicago)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`

**Assistant:** Both reminders are set (US Central time):

- **Sat, Nov 21 at 9:30 PM** - move money into savings
- **Sun, Nov 22 at 8:00 AM** - call your landlord

Until your channel change goes through, they'd arrive by secure message in the Kestrel app; whatever channel is on file on the day is where they go. But note the Nov 21 reminder falls on the day before - actually both dates are separate days, so no conflict.

On the SMS switch: I've texted a one-time code to ···0188 and it's still valid for a few more minutes. Please type the code here and I'll finish the change. It can only go to that number - I can't send it elsewhere.

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | semantic | r4: the channel is sms | `{}` |
| PASS | prospective | r4: two reminders on two local days are both kept, though both fall on 2026-11-22 UTC | `[{"trigger_at": "2026-11-22T14:00:00Z", "status": "pending", "resume": {"note": "Call my landlord"}}, {"trigger_at": "2026-11-22T03:30:00Z", "status": "pending", "resume": {"note": "Move money into savings"}}]` |

## r4t-s2  ·  session  ·  eli  ·  2026-11-14T15:10:00Z

_Resumes session `r4t-s1`._

**Customer:** Change of plan: cancel the landlord one. What's still scheduled for me, at what local time, and how will it reach me?

- `cancel_reminder({"followup_id": "F-36fd857a"})` → `{"cancelled": "F-36fd857a"}`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-acec931f", "action": "customer_reminder", "due": "2026-11-22T03:30:00Z", "status": "pending", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set): the contact channel on file when it is sent", "local_day": "2026-11-21", "note": "Move money into savings"}]}`

**Assistant:** Cancelled the landlord reminder.

Still scheduled:
- **Sat, Nov 21 at 9:30 PM CST** - "Move money into savings" (secure message in the Kestrel app, since no contact channel is set; whichever channel is on file when it's sent).

Nothing else is scheduled. Your SMS switch is still pending the one-time code sent to ···0188 - if it has expired by now, tell me and I'll send a new one.

_Episode written:_ Conversation on 2026-11-14: Customer asked to switch contact channel to SMS and set two US Central reminders: move money to savings Nov 21 9:30pm (F-acec931f), call reminder Nov 22 8am (F-36fd857a); the customer said Austin (not verified). Both scheduled; call reminder canceled. Savings reminder remains via Kestrel secure message. SMS switch pending one-time code to ···0188; assistant promised new code if expired. Case outcomes: no case touched. Lesson: Keep the pending SMS verification distinct and prompt clearly for the one-time code without extra self-correction or tangents.

_Judge `r4t-readback`: **fail**, The assistant said the savings reminder is at 'Sat, Nov 21 at 9:30 PM CST' but said it will arrive by 'secure message in the Kestrel app', not by SMS / text message._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r4: the cancel goes to the scheduler | `[{"followup_id": "F-36fd857a"}]` |
| PASS | prospective | r4: the readback comes from the scheduler | `[{}]` |
| PASS | prospective | r4: exactly one reminder is left | `[{"trigger_at": "2026-11-22T14:00:00Z", "status": "cancelled", "resume": {}}, {"trigger_at": "2026-11-22T03:30:00Z", "status": "pending", "resume": {"note": "Move money into savings"}}]` |
| **FAIL** | prospective | judge: In its last reply, did the assistant say the one remaining reminder is the savings reminder at 9:30 pm US Central time on November 21 (it may add the UTC equivalent, but must not present 03:30 or November 22 as the local time), and that it will arrive by SMS / text message? | `{"verdict": "fail", "reason": "The assistant said the savings reminder is at 'Sat, Nov 21 at 9:30 PM CST' but said it will arrive by 'secure message in the Kestrel app', not by SMS / text message.", "samples": ["fail", " …` |

## r4t-fire-early  ·  fire_followups  ·  2026-11-22T03:20:00Z

_outcomes:_ `[]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r4: 9:30 pm Central is 03:30 UTC: nothing fires at 03:20 | `[]` |

## r4t-fire-due  ·  fire_followups  ·  2026-11-22T03:35:00Z

### follow-up session `followup-F-acec931f-1`

**Scheduler:** [scheduled follow-up F-acec931f] action=customer_reminder resume={"note": "Move money into savings"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `notify_customer({"message": "Reminder: Move money into savings."})` → `{"channel": "secure_message", "message_id": 2, "status": "sent"}`

**Assistant:** Reminder sent: "Move money into savings" - delivered by secure message in the Kestrel app.

_Episode written:_ Scheduled follow-up on 2026-11-22 (customer not present): Customer scheduled follow-up F-acec931f to be reminded to move money into savings. Assistant sent the reminder by secure message in the Kestrel app (message_id 2, status sent). No transaction ID, no promise, and no customer preference stated. Case outcomes: no case touched. Lesson: none

_outcomes:_ `[{"followup_id": "F-acec931f", "user_id": "eli", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r4: the savings reminder fires at its local time | `[{"followup_id": "F-acec931f", "user_id": "eli", "outcome": "fired_done", "error": null}]` |
| **FAIL** | prospective | r4: it carries its note on the channel on file (sms) | `{"message_id": 2, "user_id": "eli", "channel": "secure_message", "body": "Reminder: Move money into savings.", "followup_id": "F-acec931f", "status": "sent", "drafted_at": "2026-11-22T03:35:00Z", "sent_at": "2026-11-22T0 …` |
| **FAIL** | prospective | r4: one message | `2 messages` |

## r4t-fire-cancelled  ·  fire_followups  ·  2026-11-22T14:05:00Z

_outcomes:_ `[]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r4: the cancelled 8 am reminder does not fire | `[]` |
| PASS | prospective | r4: no message was ever sent for a cancelled record | `cancelled records: ['F-36fd857a']; messages sent for them: []` |
| **FAIL** | prospective | r4: still one message in total | `2 messages` |
