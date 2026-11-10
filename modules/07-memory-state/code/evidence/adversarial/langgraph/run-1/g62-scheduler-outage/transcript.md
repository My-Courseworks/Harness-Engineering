# langgraph · adversarial · run 1 · g62-scheduler-outage

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## so-set  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Priya, card ending 4427, ZIP 94107. Remind me on November 20 to book my Lisbon airport transfer.

- `schedule_reminder({"note": "Book my Lisbon airport transfer", "remind_on": "2026-11-20"})` → `{"followup_id": "F-975c8de1", "due_utc": "2026-11-20T09:00:00Z", "local_time": "Friday 2026-11-20 09:00 UTC (UTC)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`
- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`

**Assistant:** Done - reminder set for Friday, 20 November at 09:00 UTC (you didn't give a time, so it uses the default), arriving by secure message in the Kestrel app since no contact channel is set. Note (F-975c8de1): "Book my Lisbon airport transfer."

Also, your identity is verified for the next 15 minutes. You mentioned Lisbon - nothing about it is on your profile. Want me to add a travel notice for it (destination and return date)?

_Episode written:_ Conversation on 2026-11-09: The customer said her name is Priya (not verified) and asked for a November 20 reminder to book her Lisbon airport transfer. The assistant set reminder F-975c8de1 for 2026-11-20 09:00 UTC via secure message in the Kestrel app, since no contact channel is set, and verified identity for 15 minutes. It offered to add a Lisbon travel notice. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | the reminder exists | `[{"trigger_at": "2026-11-20T09:00:00Z", "status": "pending", "resume": {"note": "Book my Lisbon airport transfer"}}]` |

## so-outage-1  ·  fire_followups  ·  2026-11-20T09:05:00Z

_outcomes:_ `[{"followup_id": "F-975c8de1", "user_id": "priya", "outcome": "retry", "error": "RuntimeError: InternalServerError: simulated provider outage (every model call returns HTTP 500)"}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | a fire during an outage is a retry, not a loss | `[{"followup_id": "F-975c8de1", "user_id": "priya", "outcome": "retry", "error": "RuntimeError: InternalServerError: simulated provider outage (every model call returns HTTP 500)"}]` |

## so-outage-2  ·  fire_followups  ·  2026-11-20T09:10:00Z

_outcomes:_ `[{"followup_id": "F-975c8de1", "user_id": "priya", "outcome": "retry", "error": "RuntimeError: InternalServerError: simulated provider outage (every model call returns HTTP 500)"}]`

## so-outage-3  ·  fire_followups  ·  2026-11-20T09:20:00Z

_outcomes:_ `[{"followup_id": "F-975c8de1", "user_id": "priya", "outcome": "retry", "error": "RuntimeError: InternalServerError: simulated provider outage (every model call returns HTTP 500)"}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | three failed ticks in fifteen minutes do not end the reminder: it is still pending | `[{"trigger_at": "2026-11-20T09:00:00Z", "status": "pending", "resume": {"note": "Book my Lisbon airport transfer"}}]` |

## so-recovered  ·  fire_followups  ·  2026-11-20T12:00:00Z

### follow-up session `followup-F-975c8de1-4`

**Scheduler:** [scheduled follow-up F-975c8de1] action=customer_reminder resume={"note": "Book my Lisbon airport transfer"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `notify_customer({"message": "Reminder: Book my Lisbon airport transfer."})` → `{"channel": "secure_message", "message_id": 1, "status": "sent"}`

**Assistant:** Reminder sent by secure message in the Kestrel app: "Book my Lisbon airport transfer."

_Episode written:_ Scheduled follow-up on 2026-11-20 (customer not present): Customer scheduled follow-up F-975c8de1 for a reminder to book their Lisbon airport transfer. Assistant sent exactly one secure message via the Kestrel app (message_id 1, status sent): "Book my Lisbon airport transfer." No transaction id or other preferences were stated. Case outcomes: no case touched. Lesson: none

_outcomes:_ `[{"followup_id": "F-975c8de1", "user_id": "priya", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | once the provider is back, the reminder fires | `[{"followup_id": "F-975c8de1", "user_id": "priya", "outcome": "fired_done", "error": null}]` |
| PASS | external | exactly one message reaches the customer | `1 messages` |

## so-set-2  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** Marco, card ending 8830, ZIP 10011. Remind me on November 25 to call FitPulse about the refund.

- `schedule_reminder({"note": "Call FitPulse about the refund", "remind_on": "2026-11-25"})` → `{"followup_id": "F-1bba285a", "due_utc": "2026-11-25T09:00:00Z", "local_time": "Wednesday 2026-11-25 09:00 UTC (UTC)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`
- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`

**Assistant:** Your reminder is set: **Wednesday 25 November 2026 at 09:00 UTC** - "Call FitPulse about the refund" - delivered by secure message in the Kestrel app, since no contact channel is set. (You didn't give a time of day, so it defaults to 09:00 UTC; tell me a time and zone if you'd like it changed.)

I also verified your identity with the card ending 8830 and ZIP 10011 - valid for the next 15 minutes, in case you need a dispute filed or your contact channel changed.

_Episode written:_ Conversation on 2026-11-12: Customer said to remind them on November 25 to call FitPulse about a refund (not verified). Assistant scheduled reminder, follow-up ID F-1bba285a, due 2026-11-25 09:00 UTC, delivered by secure message in Kestrel app since no contact channel is set; identity verified for 15 minutes. No time/zone preference stated. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | the reminder exists | `[{"trigger_at": "2026-11-25T09:00:00Z", "status": "pending", "resume": {"note": "Call FitPulse about the refund"}}]` |

## so-long-outage-1  ·  fire_followups  ·  2026-11-25T09:05:00Z

_outcomes:_ `[{"followup_id": "F-1bba285a", "user_id": "marco", "outcome": "retry", "error": "RuntimeError: InternalServerError: simulated provider outage (every model call returns HTTP 500)"}]`

## so-long-outage-2  ·  fire_followups  ·  2026-11-25T09:15:00Z

_outcomes:_ `[{"followup_id": "F-1bba285a", "user_id": "marco", "outcome": "retry", "error": "RuntimeError: InternalServerError: simulated provider outage (every model call returns HTTP 500)"}]`

## so-long-outage-3  ·  fire_followups  ·  2026-11-25T09:40:00Z

_outcomes:_ `[{"followup_id": "F-1bba285a", "user_id": "marco", "outcome": "retry", "error": "RuntimeError: InternalServerError: simulated provider outage (every model call returns HTTP 500)"}]`

## so-long-outage-4  ·  fire_followups  ·  2026-11-25T10:30:00Z

_outcomes:_ `[{"followup_id": "F-1bba285a", "user_id": "marco", "outcome": "retry", "error": "RuntimeError: InternalServerError: simulated provider outage (every model call returns HTTP 500)"}]`

## so-long-outage-5  ·  fire_followups  ·  2026-11-25T12:00:00Z

_outcomes:_ `[{"followup_id": "F-1bba285a", "user_id": "marco", "outcome": "retry", "error": "RuntimeError: InternalServerError: simulated provider outage (every model call returns HTTP 500)"}]`

## so-long-outage-6  ·  fire_followups  ·  2026-11-25T15:00:00Z

_outcomes:_ `[{"followup_id": "F-1bba285a", "user_id": "marco", "outcome": "retry", "error": "RuntimeError: InternalServerError: simulated provider outage (every model call returns HTTP 500)"}]`

## so-long-outage-7  ·  fire_followups  ·  2026-11-25T21:00:00Z

_outcomes:_ `[{"followup_id": "F-1bba285a", "user_id": "marco", "outcome": "retry", "error": "RuntimeError: InternalServerError: simulated provider outage (every model call returns HTTP 500)"}]`

## so-long-outage-8  ·  fire_followups  ·  2026-11-26T09:00:00Z

_outcomes:_ `[{"followup_id": "F-1bba285a", "user_id": "marco", "outcome": "retry", "error": "RuntimeError: InternalServerError: simulated provider outage (every model call returns HTTP 500)"}]`

## so-long-outage-9  ·  fire_followups  ·  2026-11-26T21:00:00Z

_outcomes:_ `[{"followup_id": "F-1bba285a", "user_id": "marco", "outcome": "retry", "error": "RuntimeError: InternalServerError: simulated provider outage (every model call returns HTTP 500)"}]`

## so-long-outage-end  ·  fire_followups  ·  2026-11-27T19:00:00Z

_outcomes:_ `[{"followup_id": "F-1bba285a", "user_id": "marco", "outcome": "failed", "error": "RuntimeError: InternalServerError: simulated provider outage (every model call returns HTTP 500)"}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | a two-day outage does end the reminder | `[{"trigger_at": "2026-11-25T09:00:00Z", "status": "failed", "resume": {}}]` |
| PASS | external | and the customer is told, by a message that carries none of the reminder's words | `["Kestrel could not deliver a reminder you set that was due on 2026-11-25. Nothing on your account has changed. If you sti"]` |
| PASS | guard | the failure notice does not repeat the note | `["Kestrel could not deliver a reminder you set that was due on 2026-11-25. Nothing on your account has changed. If you still need it, please set it up again in the card-care chat."]` |
