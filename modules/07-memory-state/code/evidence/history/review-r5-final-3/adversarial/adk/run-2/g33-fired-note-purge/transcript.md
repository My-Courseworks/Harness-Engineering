# adk · adversarial · run 2 · g33-fired-note-purge

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## fn-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Please remind me on November 15 to phone CloudNest about the refund for my storage plan.

- `schedule_reminder({"note": "Phone CloudNest about the refund for my storage plan", "remind_on": "2026-11-15"})` → `{"followup_id": "F-29c8f2e9", "due_utc": "2026-11-15T09:00:00Z", "local_time": "Sunday 2026-11-15 09:00 UTC (UTC)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`

**Assistant:** Reminder set for Sunday, November 15 at 09:00 UTC: "Phone CloudNest about the refund for my storage plan."

It will arrive as a secure message in the Kestrel app, since no contact channel is set on your account. If you'd like it by email or SMS instead, just say so.

_Episode written:_ Conversation on 2026-11-13: Customer requested a Nov 15 reminder to phone CloudNest about a storage-plan refund (not verified). Reminder scheduled for 2026-11-15 09:00 UTC, followup F-29c8f2e9, via secure message in the Kestrel app because no contact channel is set. Assistant offered email/SMS alternatives. No stated preference. Case outcomes: no case touched. Lesson: none

## fn-fire  ·  fire_followups  ·  2026-11-15T10:00:00Z

### follow-up session `followup-F-29c8f2e9-1`

**Scheduler:** [scheduled follow-up F-29c8f2e9] action=customer_reminder resume={"note": "Phone CloudNest about the refund for my storage plan"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `notify_customer({"message": "Reminder: phone CloudNest about the refund for your storage plan."})` → `{"channel": "secure_message", "message_id": 1, "status": "sent"}`

**Assistant:** Reminder sent by secure message in the Kestrel app: "Phone CloudNest about the refund for my storage plan."

_Episode written:_ Scheduled follow-up on 2026-11-15 (customer not present): Follow-up/case F-29c8f2e9 requested a reminder for the customer to phone CloudNest about a storage-plan refund; the customer said a refund was due (not verified). The assistant sent one secure message via Kestrel (message_id 1, status sent); no transaction id or promise recorded. No other preference stated. Case outcomes: no case touched. Lesson: none

_outcomes:_ `[{"followup_id": "F-29c8f2e9", "user_id": "dana", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | the reminder is sent | `[{"followup_id": "F-29c8f2e9", "user_id": "dana", "outcome": "fired_done", "error": null}]` |
| PASS | prospective | and its note, the customer's words, is purged from the scheduler once it is done | `found nowhere` |
