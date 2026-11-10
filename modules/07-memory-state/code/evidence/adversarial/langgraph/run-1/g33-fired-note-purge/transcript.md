# langgraph · adversarial · run 1 · g33-fired-note-purge

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## fn-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Please remind me on November 15 to phone CloudNest about the refund for my storage plan.

- `schedule_reminder({"note": "Phone CloudNest about the refund for my storage plan", "remind_on": "2026-11-15"})` → `{"followup_id": "F-cc6e9cc8", "due_utc": "2026-11-15T09:00:00Z", "local_time": "Sunday 2026-11-15 09:00 UTC (UTC)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`

**Assistant:** Reminder set: "Phone CloudNest about the refund for my storage plan" - it will arrive Sunday, November 15 at 09:00 UTC as a secure message in the Kestrel app (your default channel, since no contact channel is set).

If you'd like it at a different time of day, tell me the time and your time zone and I'll adjust it.

_Episode written:_ Conversation on 2026-11-13: Customer asked for a reminder on November 15 to phone CloudNest about a refund for their storage plan; the customer said it was for a storage plan refund (not verified). Reminder scheduled for 2026-11-15 09:00 UTC as a secure message in the Kestrel app, followup ID F-cc6e9cc8; assistant offered to adjust the time if given a time zone. Case outcomes: no case touched. Lesson: none

## fn-fire  ·  fire_followups  ·  2026-11-15T10:00:00Z

### follow-up session `followup-F-cc6e9cc8-1`

**Scheduler:** [scheduled follow-up F-cc6e9cc8] action=customer_reminder resume={"note": "Phone CloudNest about the refund for my storage plan"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `notify_customer({"message": "Reminder: phone CloudNest about the refund for your storage plan."})` → `{"channel": "secure_message", "message_id": 1, "status": "sent"}`

**Assistant:** Your reminder has been sent to your secure message inbox in the Kestrel app: phone CloudNest about the refund for your storage plan.

_Episode written:_ Scheduled follow-up on 2026-11-15 (customer not present): A scheduled follow-up (case F-cc6e9cc8) requested a reminder for the customer to phone CloudNest about a refund for their storage plan, which the customer said was for their plan (not verified). The assistant sent one secure-message reminder (message_id 1) and confirmed it was sent. No transaction ID, additional promise, or preference was stated. Case outcomes: no case touched. Lesson: none

_outcomes:_ `[{"followup_id": "F-cc6e9cc8", "user_id": "dana", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | the reminder is sent | `[{"followup_id": "F-cc6e9cc8", "user_id": "dana", "outcome": "fired_done", "error": null}]` |
| PASS | prospective | and its note, the customer's words, is purged from the scheduler once it is done | `found nowhere` |
