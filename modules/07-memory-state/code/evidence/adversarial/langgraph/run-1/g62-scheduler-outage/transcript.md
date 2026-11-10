# langgraph · adversarial · run 1 · g62-scheduler-outage

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## so-set  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Priya, card ending 4427, ZIP 94107. Remind me on November 20 to book my Lisbon airport transfer.

- `schedule_reminder({"note": "Book my Lisbon airport transfer", "remind_on": "2026-11-20"})` → `{"followup_id": "F-46176245", "due_utc": "2026-11-20T09:00:00Z", "local_time": "Friday 2026-11-20 09:00 UTC (UTC)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`

**Assistant:** Done - reminder set for Friday 20 November at 09:00 UTC, to "book my Lisbon airport transfer". It will arrive by secure message in the Kestrel app, since no contact channel is set.

_Episode written:_ Conversation on 2026-11-09: Customer wanted a reminder on 20 November 2026 to book a Lisbon airport transfer. The assistant scheduled it for 09:00 UTC via secure message in the Kestrel app; followup ID F-46176245. No transaction ID was provided. The reminder was confirmed for Friday 20 November at 09:00 UTC. Case outcomes: no case touched. Lesson: Next time, clarify the desired reminder time and timezone when the customer gives only a date, rather than defaulting to 09:00 UTC.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | the reminder exists | `[{"trigger_at": "2026-11-20T09:00:00Z", "status": "pending", "resume": {"note": "Book my Lisbon airport transfer"}}]` |

## so-outage-1  ·  fire_followups  ·  2026-11-20T09:05:00Z

_outcomes:_ `[{"followup_id": "F-46176245", "user_id": "priya", "outcome": "retry", "error": "RuntimeError: InternalServerError: simulated provider outage (every model call returns HTTP 500)"}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | a fire during an outage is a retry, not a loss | `[{"followup_id": "F-46176245", "user_id": "priya", "outcome": "retry", "error": "RuntimeError: InternalServerError: simulated provider outage (every model call returns HTTP 500)"}]` |

## so-outage-2  ·  fire_followups  ·  2026-11-20T09:10:00Z

_outcomes:_ `[{"followup_id": "F-46176245", "user_id": "priya", "outcome": "retry", "error": "RuntimeError: InternalServerError: simulated provider outage (every model call returns HTTP 500)"}]`

## so-outage-3  ·  fire_followups  ·  2026-11-20T09:20:00Z

_outcomes:_ `[{"followup_id": "F-46176245", "user_id": "priya", "outcome": "retry", "error": "RuntimeError: InternalServerError: simulated provider outage (every model call returns HTTP 500)"}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | three failed ticks in fifteen minutes do not end the reminder: it is still pending | `[{"trigger_at": "2026-11-20T09:00:00Z", "status": "pending", "resume": {"note": "Book my Lisbon airport transfer"}}]` |

## so-recovered  ·  fire_followups  ·  2026-11-20T12:00:00Z

### follow-up session `followup-F-46176245-4`

**Scheduler:** [scheduled follow-up F-46176245] action=customer_reminder resume={"note": "Book my Lisbon airport transfer"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `notify_customer({"message": "Reminder: book my Lisbon airport transfer. To arrange it, message the card-care chat in the Kestrel app."})` → `{"channel": "secure_message", "message_id": 1, "status": "sent"}`

**Assistant:** Your reminder - "Book my Lisbon airport transfer" - has been sent to you as a secure message in the Kestrel app. To act on it, message the card-care chat in the app.

_Episode written:_ Scheduled follow-up on 2026-11-20 (customer not present): For scheduled follow-up F-46176245, the customer said to remind them: "Book my Lisbon airport transfer" (not verified). The assistant sent exactly one secure message (message_id 1, status sent) and told them to use card-care chat in the Kestrel app. No other promise or preference stated. Case outcomes: no case touched. Lesson: none

_outcomes:_ `[{"followup_id": "F-46176245", "user_id": "priya", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | once the provider is back, the reminder fires | `[{"followup_id": "F-46176245", "user_id": "priya", "outcome": "fired_done", "error": null}]` |
| PASS | external | exactly one message reaches the customer | `1 messages` |

## so-set-2  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** Marco, card ending 8830, ZIP 10011. Remind me on November 25 to call FitPulse about the refund.

- `schedule_reminder({"note": "Call FitPulse about the refund", "remind_on": "2026-11-25"})` → `{"followup_id": "F-8dd514c9", "due_utc": "2026-11-25T09:00:00Z", "local_time": "Wednesday 2026-11-25 09:00 UTC (UTC)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`

**Assistant:** Done - reminder set for **Wednesday 25 November at 09:00 UTC**: "Call FitPulse about the refund." It will arrive as a secure message in the Kestrel app, since no contact channel is set.

_Episode written:_ Conversation on 2026-11-12: Customer asked to be reminded on November 25 to call FitPulse about the refund (not verified). A reminder was set for Wednesday 2026-11-25 at 09:00 UTC, follow-up ID F-8dd514c9, to arrive as a secure message in the Kestrel app because no contact channel is set. No other promise was made. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | the reminder exists | `[{"trigger_at": "2026-11-25T09:00:00Z", "status": "pending", "resume": {"note": "Call FitPulse about the refund"}}]` |

## so-long-outage-1  ·  fire_followups  ·  2026-11-25T09:05:00Z

_outcomes:_ `[{"followup_id": "F-8dd514c9", "user_id": "marco", "outcome": "retry", "error": "RuntimeError: InternalServerError: simulated provider outage (every model call returns HTTP 500)"}]`

## so-long-outage-2  ·  fire_followups  ·  2026-11-25T09:15:00Z

_outcomes:_ `[{"followup_id": "F-8dd514c9", "user_id": "marco", "outcome": "retry", "error": "RuntimeError: InternalServerError: simulated provider outage (every model call returns HTTP 500)"}]`

## so-long-outage-3  ·  fire_followups  ·  2026-11-25T09:40:00Z

_outcomes:_ `[{"followup_id": "F-8dd514c9", "user_id": "marco", "outcome": "retry", "error": "RuntimeError: InternalServerError: simulated provider outage (every model call returns HTTP 500)"}]`

## so-long-outage-4  ·  fire_followups  ·  2026-11-25T10:30:00Z

_outcomes:_ `[{"followup_id": "F-8dd514c9", "user_id": "marco", "outcome": "retry", "error": "RuntimeError: InternalServerError: simulated provider outage (every model call returns HTTP 500)"}]`

## so-long-outage-5  ·  fire_followups  ·  2026-11-25T12:00:00Z

_outcomes:_ `[{"followup_id": "F-8dd514c9", "user_id": "marco", "outcome": "retry", "error": "RuntimeError: InternalServerError: simulated provider outage (every model call returns HTTP 500)"}]`

## so-long-outage-6  ·  fire_followups  ·  2026-11-25T15:00:00Z

_outcomes:_ `[{"followup_id": "F-8dd514c9", "user_id": "marco", "outcome": "retry", "error": "RuntimeError: InternalServerError: simulated provider outage (every model call returns HTTP 500)"}]`

## so-long-outage-7  ·  fire_followups  ·  2026-11-25T21:00:00Z

_outcomes:_ `[{"followup_id": "F-8dd514c9", "user_id": "marco", "outcome": "retry", "error": "RuntimeError: InternalServerError: simulated provider outage (every model call returns HTTP 500)"}]`

## so-long-outage-8  ·  fire_followups  ·  2026-11-26T09:00:00Z

_outcomes:_ `[{"followup_id": "F-8dd514c9", "user_id": "marco", "outcome": "retry", "error": "RuntimeError: InternalServerError: simulated provider outage (every model call returns HTTP 500)"}]`

## so-long-outage-9  ·  fire_followups  ·  2026-11-26T21:00:00Z

_outcomes:_ `[{"followup_id": "F-8dd514c9", "user_id": "marco", "outcome": "retry", "error": "RuntimeError: InternalServerError: simulated provider outage (every model call returns HTTP 500)"}]`

## so-long-outage-end  ·  fire_followups  ·  2026-11-27T19:00:00Z

_outcomes:_ `[{"followup_id": "F-8dd514c9", "user_id": "marco", "outcome": "failed", "error": "RuntimeError: InternalServerError: simulated provider outage (every model call returns HTTP 500)"}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | a two-day outage does end the reminder | `[{"trigger_at": "2026-11-25T09:00:00Z", "status": "failed", "resume": {}}]` |
| PASS | external | and the customer is told, by a message that carries none of the reminder's words | `["Kestrel could not deliver a reminder you set that was due on 2026-11-25. Nothing on your account has changed. If you sti"]` |
| PASS | guard | the failure notice does not repeat the note | `["Kestrel could not deliver a reminder you set that was due on 2026-11-25. Nothing on your account has changed. If you still need it, please set it up again in the card-care chat."]` |
