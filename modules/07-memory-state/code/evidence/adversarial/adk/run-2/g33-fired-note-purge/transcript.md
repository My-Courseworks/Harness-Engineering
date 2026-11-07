# adk · adversarial · run 2 · g33-fired-note-purge

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## fn-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Please remind me on November 15 to phone CloudNest about the refund for my storage plan.

- `schedule_reminder({"note": "Phone CloudNest about the refund for my storage plan", "remind_on": "2026-11-15"})` → `{"followup_id": "F-db754d48", "due_utc": "2026-11-15T09:00:00Z", "local_time": "Sunday 2026-11-15 09:00 UTC (UTC)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`

**Assistant:** Done - reminder set for Sunday 15 November at 09:00 UTC. It will reach you by secure message in the Kestrel app (the default, since no contact channel is set).

_Episode written:_ Conversation on 2026-11-13: Customer wanted a November 15 reminder to phone CloudNest about a storage-plan refund; the customer said the refund was for their storage plan (not verified). Reminder F-db754d48 was set for 2026-11-15 09:00 UTC and promised via secure message in the Kestrel app (default; no contact channel set). Case outcomes: no case touched. Lesson: none

## fn-fire  ·  fire_followups  ·  2026-11-15T10:00:00Z

### follow-up session `followup-F-db754d48-1`

**Scheduler:** [scheduled follow-up F-db754d48] action=customer_reminder resume={"note": "Phone CloudNest about the refund for my storage plan"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `notify_customer({"message": "Reminder: phone CloudNest about the refund for your storage plan. If you'd like us to help with it \u2014 for example checking the transaction or opening a dispute \u2014 message the card …)` → `{"channel": "secure_message", "message_id": 1, "status": "sent"}`

**Assistant:** Reminder sent by secure message in the Kestrel app: phone CloudNest about the refund for your storage plan. Next step is that call; if you want help reviewing the transaction or disputing it, message the card-care chat.

_Episode written:_ Scheduled follow-up on 2026-11-15 (customer not present): Customer requested a scheduled reminder (follow-up F-db754d48) to phone CloudNest about a refund for their storage plan. The assistant sent one secure message via the Kestrel app (message_id 1) with that reminder and offered help reviewing the transaction or disputing it. No transaction ID was provided; no promise or specific preference was stated. Case outcomes: no case touched. Lesson: none

_outcomes:_ `[{"followup_id": "F-db754d48", "user_id": "dana", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | the reminder is sent | `[{"followup_id": "F-db754d48", "user_id": "dana", "outcome": "fired_done", "error": null}]` |
| PASS | prospective | and its note, the customer's words, is purged from the scheduler once it is done | `found nowhere` |
