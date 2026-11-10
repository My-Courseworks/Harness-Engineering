# langgraph · adversarial · run 1 · g62-scheduler-outage

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## so-set  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Priya, card ending 4427, ZIP 94107. Remind me on November 20 to book my Lisbon airport transfer.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `schedule_reminder({"note": "Book my Lisbon airport transfer", "remind_on": "2026-11-20"})` → `{"followup_id": "F-a8ccf014", "due_utc": "2026-11-20T09:00:00Z", "local_time": "Friday 2026-11-20 09:00 UTC (UTC)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`

**Assistant:** Your reminder is set: "Book my Lisbon airport transfer" - it will arrive on Friday, November 20 at 09:00 UTC, as a secure message in the Kestrel app (that's the default since no contact channel is set).

If you'd like it by email or SMS instead, say which and I can change it. Your identity check also succeeded just now.

_Episode written:_ Conversation on 2026-11-09: The customer said her name is Priya (not verified) and asked for a November 20 reminder to book her Lisbon airport transfer. Identity was verified; reminder F-a8ccf014 was scheduled for 2026-11-20 09:00 UTC via secure message in the Kestrel app, the default because no contact channel is set. Assistant offered changing to email/SMS. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | the reminder exists | `[{"trigger_at": "2026-11-20T09:00:00Z", "status": "pending", "resume": {"note": "Book my Lisbon airport transfer"}}]` |

## so-outage-1  ·  fire_followups  ·  2026-11-20T09:05:00Z

_outcomes:_ `[{"followup_id": "F-a8ccf014", "user_id": "priya", "outcome": "retry", "error": "RuntimeError: InternalServerError: simulated provider outage (every model call returns HTTP 500)"}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | a fire during an outage is a retry, not a loss | `[{"followup_id": "F-a8ccf014", "user_id": "priya", "outcome": "retry", "error": "RuntimeError: InternalServerError: simulated provider outage (every model call returns HTTP 500)"}]` |

## so-outage-2  ·  fire_followups  ·  2026-11-20T09:10:00Z

_outcomes:_ `[{"followup_id": "F-a8ccf014", "user_id": "priya", "outcome": "retry", "error": "RuntimeError: InternalServerError: simulated provider outage (every model call returns HTTP 500)"}]`

## so-outage-3  ·  fire_followups  ·  2026-11-20T09:20:00Z

_outcomes:_ `[{"followup_id": "F-a8ccf014", "user_id": "priya", "outcome": "failed", "error": "RuntimeError: InternalServerError: simulated provider outage (every model call returns HTTP 500)"}]`

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | prospective | three failed ticks in fifteen minutes do not end the reminder: it is still pending | `[{"trigger_at": "2026-11-20T09:00:00Z", "status": "failed", "resume": {}}]` |

## so-recovered  ·  fire_followups  ·  2026-11-20T12:00:00Z

_outcomes:_ `[]`

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | prospective | once the provider is back, the reminder fires | `[]` |
| **FAIL** | external | exactly one message reaches the customer | `0 messages` |

## so-set-2  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** Marco, card ending 8830, ZIP 10011. Remind me on November 25 to call FitPulse about the refund.

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `schedule_reminder({"note": "Call FitPulse about the refund", "remind_on": "2026-11-25"})` → `{"followup_id": "F-89766ddb", "due_utc": "2026-11-25T09:00:00Z", "local_time": "Wednesday 2026-11-25 09:00 UTC (UTC)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`

**Assistant:** Done - and your identity is verified for the next 15 minutes, in case you need anything like a dispute.

Reminder set for **Wednesday, November 25 at 09:00 UTC** (id F-89766ddb): "Call FitPulse about the refund." It will arrive as a secure message in the Kestrel app, since no contact channel is set on your profile.

_Episode written:_ Conversation on 2026-11-12: The customer asked for a reminder on November 25 to call FitPulse about a refund (not verified). Identity was verified for 15 minutes, and reminder F-89766ddb was scheduled for 2026-11-25 09:00 UTC. It will arrive as a secure message in the Kestrel app; no contact channel is set. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | the reminder exists | `[{"trigger_at": "2026-11-25T09:00:00Z", "status": "pending", "resume": {"note": "Call FitPulse about the refund"}}]` |

## so-long-outage-1  ·  fire_followups  ·  2026-11-25T09:05:00Z

_outcomes:_ `[{"followup_id": "F-89766ddb", "user_id": "marco", "outcome": "retry", "error": "RuntimeError: InternalServerError: simulated provider outage (every model call returns HTTP 500)"}]`

## so-long-outage-2  ·  fire_followups  ·  2026-11-25T09:15:00Z

_outcomes:_ `[{"followup_id": "F-89766ddb", "user_id": "marco", "outcome": "retry", "error": "RuntimeError: InternalServerError: simulated provider outage (every model call returns HTTP 500)"}]`

## so-long-outage-3  ·  fire_followups  ·  2026-11-25T09:40:00Z

_outcomes:_ `[{"followup_id": "F-89766ddb", "user_id": "marco", "outcome": "failed", "error": "RuntimeError: InternalServerError: simulated provider outage (every model call returns HTTP 500)"}]`

## so-long-outage-4  ·  fire_followups  ·  2026-11-25T10:30:00Z

_outcomes:_ `[]`

## so-long-outage-5  ·  fire_followups  ·  2026-11-25T12:00:00Z

_outcomes:_ `[]`

## so-long-outage-6  ·  fire_followups  ·  2026-11-25T15:00:00Z

_outcomes:_ `[]`

## so-long-outage-7  ·  fire_followups  ·  2026-11-25T21:00:00Z

_outcomes:_ `[]`

## so-long-outage-8  ·  fire_followups  ·  2026-11-26T09:00:00Z

_outcomes:_ `[]`

## so-long-outage-9  ·  fire_followups  ·  2026-11-26T21:00:00Z

_outcomes:_ `[]`

## so-long-outage-end  ·  fire_followups  ·  2026-11-27T09:00:00Z

_outcomes:_ `[]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | a two-day outage does end the reminder | `[{"trigger_at": "2026-11-25T09:00:00Z", "status": "failed", "resume": {}}]` |
| **FAIL** | external | and the customer is told, by a message that carries none of the reminder's words | `[]` |
| **FAIL** | guard | the failure notice does not repeat the note | `[]` |
