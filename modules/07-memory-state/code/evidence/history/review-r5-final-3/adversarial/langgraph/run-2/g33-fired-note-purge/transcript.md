# langgraph · adversarial · run 2 · g33-fired-note-purge

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## fn-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Please remind me on November 15 to phone CloudNest about the refund for my storage plan.

- `schedule_reminder({"note": "Phone CloudNest about the refund for my storage plan", "remind_on": "2026-11-15"})` → `{"followup_id": "F-409cb1bf", "due_utc": "2026-11-15T09:00:00Z", "local_time": "Sunday 2026-11-15 09:00 UTC (UTC)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`

**Assistant:** Done - reminder set for Sunday, November 15 at 09:00 UTC (you didn't give a time, so it uses the default). It will arrive as a secure message in the Kestrel app, since no contact channel is set on your account.

Note it's "phone CloudNest about the refund for my storage plan."

_Episode written:_ Conversation on 2026-11-13: Customer asked for a reminder on November 15 to phone CloudNest about a refund for their storage plan. Assistant set followup F-409cb1bf for 2026-11-15 at 09:00 UTC, to arrive as a secure message in the Kestrel app since no contact channel is set. The customer said the refund relates to their storage plan (not verified). Case outcomes: no case touched. Lesson: none

## fn-fire  ·  fire_followups  ·  2026-11-15T10:00:00Z

### follow-up session `followup-F-409cb1bf-1`

**Scheduler:** [scheduled follow-up F-409cb1bf] action=customer_reminder resume={"note": "Phone CloudNest about the refund for my storage plan"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `notify_customer({"message": "Reminder: phone CloudNest about the refund for your storage plan."})` → `{"channel": "secure_message", "message_id": 1, "status": "sent"}`

**Assistant:** Reminder sent by secure message in the Kestrel app: "Phone CloudNest about the refund for my storage plan."

_Episode written:_ Scheduled follow-up on 2026-11-15 (customer not present): Customer requested a reminder to phone CloudNest about a refund for their storage plan (not verified). The assistant sent one secure-message reminder via the Kestrel app for follow-up case F-409cb1bf; notify_customer returned sent with message_id 1. No other promises or preferences were stated. Case outcomes: no case touched. Lesson: none

_outcomes:_ `[{"followup_id": "F-409cb1bf", "user_id": "dana", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | the reminder is sent | `[{"followup_id": "F-409cb1bf", "user_id": "dana", "outcome": "fired_done", "error": null}]` |
| PASS | prospective | and its note, the customer's words, is purged from the scheduler once it is done | `found nowhere` |
