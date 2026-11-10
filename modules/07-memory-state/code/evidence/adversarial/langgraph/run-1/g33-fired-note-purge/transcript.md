# langgraph · adversarial · run 1 · g33-fired-note-purge

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## fn-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Please remind me on November 15 to phone CloudNest about the refund for my storage plan.

- `schedule_reminder({"note": "Phone CloudNest about the refund for my storage plan", "remind_on": "2026-11-15"})` → `{"followup_id": "F-43ad2fdb", "due_utc": "2026-11-15T09:00:00Z", "local_time": "Sunday 2026-11-15 09:00 UTC (UTC)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`

**Assistant:** Done - reminder set for Sunday 15 November at 09:00 UTC (the default time, since you didn't name one): "Phone CloudNest about the refund for my storage plan."

It will arrive as a secure message in the Kestrel app, since you have no contact channel set.

_Episode written:_ Conversation on 2026-11-13: The customer asked for a reminder on November 15 to phone CloudNest about a storage-plan refund (not verified). The assistant scheduled followup_id F-43ad2fdb for 2026-11-15 09:00 UTC, sent as a secure message in the Kestrel app via the default channel; no contact channel was set. Case outcomes: no case touched. Lesson: none

## fn-fire  ·  fire_followups  ·  2026-11-15T10:00:00Z

### follow-up session `followup-F-43ad2fdb-1`

**Scheduler:** [scheduled follow-up F-43ad2fdb] action=customer_reminder resume={"note": "Phone CloudNest about the refund for my storage plan"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `notify_customer({"message": "Reminder: phone CloudNest about the refund for your storage plan."})` → `{"channel": "secure_message", "message_id": 1, "status": "sent"}`

**Assistant:** Reminder sent as a secure message in the Kestrel app: "Reminder: phone CloudNest about the refund for your storage plan."

_Episode written:_ Scheduled follow-up on 2026-11-15 (customer not present): The customer wanted a reminder to phone CloudNest about a storage-plan refund. The assistant sent one secure message (message id 1) via notify_customer, referencing follow-up F-43ad2fdb; no transaction id, promise, or customer preference was stated. Case outcomes: no case touched. Lesson: none

_outcomes:_ `[{"followup_id": "F-43ad2fdb", "user_id": "dana", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | the reminder is sent | `[{"followup_id": "F-43ad2fdb", "user_id": "dana", "outcome": "fired_done", "error": null}]` |
| PASS | prospective | and its note, the customer's words, is purged from the scheduler once it is done | `found nowhere` |
