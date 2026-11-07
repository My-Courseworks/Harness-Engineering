# adk · adversarial · run 1 · g33-fired-note-purge

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## fn-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Please remind me on November 15 to phone CloudNest about the refund for my storage plan.

- `schedule_reminder({"note": "Phone CloudNest about the refund for my storage plan", "remind_on": "2026-11-15"})` → `{"followup_id": "F-b9b6510d", "due_utc": "2026-11-15T09:00:00Z", "local_time": "Sunday 2026-11-15 09:00 UTC (UTC)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`

**Assistant:** Reminder set for Sunday 2026-11-15 at 09:00 UTC (the default time, since you didn't name one) - id F-b9b6510d. It will arrive as a secure message in the Kestrel app, since no contact channel is set on your account.

_Episode written:_ Conversation on 2026-11-13: Customer wanted a reminder on November 15 to phone CloudNest about the refund for their storage plan (not verified). Assistant scheduled reminder F-b9b6510d for 2026-11-15 09:00 UTC, the default time, to arrive by secure message in the Kestrel app because no contact channel is set. No other preference stated. Case outcomes: no case touched. Lesson: none

## fn-fire  ·  fire_followups  ·  2026-11-15T10:00:00Z

### follow-up session `followup-F-b9b6510d-1`

**Scheduler:** [scheduled follow-up F-b9b6510d] action=customer_reminder resume={"note": "Phone CloudNest about the refund for my storage plan"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `notify_customer({"message": "Reminder: phone CloudNest about the refund for your storage plan. If you need anything from Kestrel, message the card-care chat in the Kestrel app."})` → `{"channel": "secure_message", "message_id": 1, "status": "sent"}`

**Assistant:** Reminder sent by secure message in the Kestrel app: phone CloudNest about the refund for your storage plan.

_Episode written:_ Scheduled follow-up on 2026-11-15 (customer not present): Customer scheduled follow-up F-b9b6510d for a reminder to phone CloudNest about the refund for their storage plan (customer said, not verified). The assistant sent exactly one secure message reminder via notify_customer; message ID 1, status sent. No transaction ID or promise was recorded; no preference stated. Case outcomes: no case touched. Lesson: none

_outcomes:_ `[{"followup_id": "F-b9b6510d", "user_id": "dana", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | the reminder is sent | `[{"followup_id": "F-b9b6510d", "user_id": "dana", "outcome": "fired_done", "error": null}]` |
| PASS | prospective | and its note, the customer's words, is purged from the scheduler once it is done | `found nowhere` |
