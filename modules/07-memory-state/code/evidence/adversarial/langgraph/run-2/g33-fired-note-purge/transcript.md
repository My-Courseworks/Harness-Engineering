# langgraph · adversarial · run 2 · g33-fired-note-purge

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## fn-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Please remind me on November 15 to phone CloudNest about the refund for my storage plan.

- `schedule_reminder({"note": "Phone CloudNest about the refund for my storage plan", "remind_on": "2026-11-15"})` → `{"followup_id": "F-89a6641b", "due_utc": "2026-11-15T09:00:00Z", "local_time": "Sunday 2026-11-15 09:00 UTC (UTC)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`

**Assistant:** Reminder set: Sunday 15 November at 09:00 UTC, to phone CloudNest about your storage plan refund. It will arrive by secure message in the Kestrel app, since you have no contact channel set.

_Episode written:_ Conversation on 2026-11-13: Customer asked for a reminder on November 15 to phone CloudNest about a storage plan refund. Reminder scheduled (followup_id F-89a6641b) for 2026-11-15 09:00 UTC, to be sent by secure message in the Kestrel app because no contact channel was set. Case outcomes: no case touched. Lesson: none

## fn-fire  ·  fire_followups  ·  2026-11-15T10:00:00Z

### follow-up session `followup-F-89a6641b-1`

**Scheduler:** [scheduled follow-up F-89a6641b] action=customer_reminder resume={"note": "Phone CloudNest about the refund for my storage plan"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `list_my_followups({})` → `{"scheduled": []}`
- `notify_customer({"message": "Reminder: phone CloudNest about the refund for your storage plan."})` → `{"channel": "secure_message", "message_id": 1, "status": "sent"}`

**Assistant:** Your reminder - phone CloudNest about the refund for your storage plan - has been sent as a secure message in the Kestrel app.

_Episode written:_ Scheduled follow-up on 2026-11-15 (customer not present): Customer scheduled follow-up F-89a6641b wanted a reminder to phone CloudNest about a storage-plan refund; the customer said this refund matter needed a call (not verified). Assistant checked follow-ups (none scheduled) and sent one secure-message reminder in the Kestrel app, message_id 1. No transaction ID or stated preference. Case outcomes: no case touched. Lesson: When a scheduled follow-up is provided but list_my_followups returns none, the assistant should note or verify the discrepancy before sending the reminder.

_outcomes:_ `[{"followup_id": "F-89a6641b", "user_id": "dana", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | the reminder is sent | `[{"followup_id": "F-89a6641b", "user_id": "dana", "outcome": "fired_done", "error": null}]` |
| PASS | prospective | and its note, the customer's words, is purged from the scheduler once it is done | `found nowhere` |
