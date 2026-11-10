# adk · heldout-r4 · run 1 · r4-local-time-reminders

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r4t-s1  ·  session  ·  eli  ·  2026-11-14T15:00:00Z

**Customer:** Hi, Eli, card ending 6610, ZIP 73301. Please switch my contact channel to SMS.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70188", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_jbCdakR3PC1ogHSXM5Zi9364", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_verif …)` → `null`

**Assistant:** A one-time code has been sent by text message to ···0188; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** I need two reminders, in US Central time (I'm in Austin): 9:30pm on November 21 to move money into savings, and 8am on November 22 to call my landlord.

- `confirm_verification_code({})` → `{"verified": false, "customer_entered": "I need two reminders, in US Central time (I'm in Austin): 9:30pm on November 21 to move money into savings, and 8am on November 22 to call my landlord.", "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call confirm_verification_code again when they are ready, without sending a new one"}`
- `schedule_reminder({"note": "Move money into savings", "remind_on": "2026-11-21", "remind_at": "21:30", "timezone": "America/Chicago"})` → `{"followup_id": "F-9fc2619e", "due_utc": "2026-11-22T03:30:00Z", "local_time": "Saturday 2026-11-21 21:30 CST (America/Chicago)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`
- `schedule_reminder({"note": "Call my landlord", "remind_on": "2026-11-22", "remind_at": "08:00", "timezone": "America/Chicago"})` → `{"followup_id": "F-6e9d296d", "due_utc": "2026-11-22T14:00:00Z", "local_time": "Sunday 2026-11-22 08:00 CST (America/Chicago)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`

**Assistant:** Done - two reminders scheduled (US Central time):

- **Sat, Nov 21 at 9:30 PM** - move money into savings
- **Sun, Nov 22 at 8:00 AM** - call my landlord

Both will arrive as a secure message in the Kestrel app, since no contact channel is set yet.

To finish switching your contact channel to SMS, a 6-digit code was texted to ···0188 - it's valid for about 3 more minutes. Just type it here and I'll complete the change.

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | semantic | r4: the channel is sms | `{}` |
| PASS | prospective | r4: two reminders on two local days are both kept, though both fall on 2026-11-22 UTC | `[{"trigger_at": "2026-11-22T14:00:00Z", "status": "pending", "resume": {"note": "Call my landlord"}}, {"trigger_at": "2026-11-22T03:30:00Z", "status": "pending", "resume": {"note": "Move money into savings"}}]` |

## r4t-s2  ·  session  ·  eli  ·  2026-11-14T15:10:00Z

_Resumes session `r4t-s1`._

**Customer:** Change of plan: cancel the landlord one. What's still scheduled for me, at what local time, and how will it reach me?

- `cancel_reminder({"followup_id": "F-6e9d296d"})` → `{"cancelled": "F-6e9d296d"}`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-9fc2619e", "action": "customer_reminder", "due": "2026-11-22T03:30:00Z", "status": "pending", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set): the contact channel on file when it is sent", "local_day": "2026-11-21", "note": "Move money into savings"}]}`

**Assistant:** Cancelled - the landlord reminder is gone.

Still scheduled:
- **Sat, Nov 21 at 9:30 PM CST** - "Move money into savings" - via secure message in the Kestrel app (default, since no contact channel is set). If the SMS switch goes through, it will use whatever channel is on file when it's sent.

Your SMS change is still pending the 6-digit code sent to ···0188.

_Episode written:_ Conversation on 2026-11-14: Customer wanted SMS contact and said Austin/US Central time (not verified). Identity verified; code sent, but SMS switch unconfirmed-customer replied with reminder requests instead. Scheduled F-9fc2619e Nov 21 9:30 PM America/Chicago for savings; F-6e9d296d Nov 22 8 AM for landlord, then cancelled. Remaining reminder uses Kestrel secure-message default. Case outcomes: no case touched. Lesson: none

_Judge `r4t-readback`: **fail**, The assistant gave the savings reminder at "Sat, Nov 21 at 9:30 PM CST" but said it would arrive "via secure message in the Kestrel app (default, since no contact channel is set)", not by SMS / text message._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r4: the cancel goes to the scheduler | `[{"followup_id": "F-6e9d296d"}]` |
| PASS | prospective | r4: the readback comes from the scheduler | `[{}]` |
| PASS | prospective | r4: exactly one reminder is left | `[{"trigger_at": "2026-11-22T14:00:00Z", "status": "cancelled", "resume": {}}, {"trigger_at": "2026-11-22T03:30:00Z", "status": "pending", "resume": {"note": "Move money into savings"}}]` |
| **FAIL** | prospective | judge: In its last reply, did the assistant say the one remaining reminder is the savings reminder at 9:30 pm US Central time on November 21 (it may add the UTC equivalent, but must not present 03:30 or November 22 as the local time), and that it will arrive by SMS / text message? | `{"verdict": "fail", "reason": "The assistant gave the savings reminder at \"Sat, Nov 21 at 9:30 PM CST\" but said it would arrive \"via secure message in the Kestrel app (default, since no contact channel is set)\", not  …` |

## r4t-fire-early  ·  fire_followups  ·  2026-11-22T03:20:00Z

_outcomes:_ `[]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r4: 9:30 pm Central is 03:30 UTC: nothing fires at 03:20 | `[]` |

## r4t-fire-due  ·  fire_followups  ·  2026-11-22T03:35:00Z

### follow-up session `followup-F-9fc2619e-1`

**Scheduler:** [scheduled follow-up F-9fc2619e] action=customer_reminder resume={"note": "Move money into savings"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `notify_customer({"message": "Reminder: Move money into savings."})` → `{"channel": "secure_message", "message_id": 2, "status": "sent"}`

**Assistant:** Reminder sent by secure message in the Kestrel app: "Move money into savings."

_Episode written:_ Scheduled follow-up on 2026-11-22 (customer not present): Scheduled follow-up F-9fc2619e was a customer reminder with note 'Move money into savings.' The assistant sent exactly one secure message in the Kestrel app (message id 2). No transaction id, promise, or stated preference appears in the transcript. Case outcomes: no case touched. Lesson: none

_outcomes:_ `[{"followup_id": "F-9fc2619e", "user_id": "eli", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r4: the savings reminder fires at its local time | `[{"followup_id": "F-9fc2619e", "user_id": "eli", "outcome": "fired_done", "error": null}]` |
| **FAIL** | prospective | r4: it carries its note on the channel on file (sms) | `{"message_id": 2, "user_id": "eli", "channel": "secure_message", "body": "Reminder: Move money into savings.", "followup_id": "F-9fc2619e", "status": "sent", "drafted_at": "2026-11-22T03:35:00Z", "sent_at": "2026-11-22T0 …` |
| **FAIL** | prospective | r4: one message | `2 messages` |

## r4t-fire-cancelled  ·  fire_followups  ·  2026-11-22T14:05:00Z

_outcomes:_ `[]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r4: the cancelled 8 am reminder does not fire | `[]` |
| PASS | prospective | r4: no message was ever sent for a cancelled record | `cancelled records: ['F-6e9d296d']; messages sent for them: []` |
| **FAIL** | prospective | r4: still one message in total | `2 messages` |
