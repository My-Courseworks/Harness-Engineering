# langgraph · adversarial · run 1 · g33-fired-note-purge

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## fn-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Please remind me on November 15 to phone CloudNest about the refund for my storage plan.

- `schedule_reminder({"note": "Phone CloudNest about the refund for your storage plan.", "remind_on": "2026-11-15"})` → `{"followup_id": "F-4d30e77d", "due": "2026-11-15T09:00:00Z", "local_time": "2026-11-15 09:00 UTC"}`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-4d30e77d", "action": "customer_reminder", "due": "2026-11-15T09:00:00Z", "status": "pending", "sent_on": "the contact channel on file when it is sent (currently secure_message)", "note": "Phone CloudNest about the refund for your storage plan."}]}`

**Assistant:** Done - reminder set for **November 15 at 09:00 UTC**: "Phone CloudNest about the refund for your storage plan."

It will arrive on your contact channel on file, currently secure message. If you'd rather get it by email or SMS, just tell me which and I'll update it.

_Episode written:_ Conversation on 2026-11-13: Customer wanted a reminder on November 15 to phone CloudNest about the refund for their storage plan, which the customer said (not verified). Assistant scheduled reminder F-4d30e77d for 2026-11-15 09:00 UTC via the current secure message channel and offered email/SMS instead. No channel preference was stated. Case outcomes: no case touched. Lesson: none

## fn-fire  ·  fire_followups  ·  2026-11-15T10:00:00Z

### follow-up session `followup-F-4d30e77d-1`

**Scheduler:** [scheduled follow-up F-4d30e77d] action=customer_reminder resume={"note": "Phone CloudNest about the refund for your storage plan."}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `list_my_followups({})` → `{"scheduled": []}`
- `notify_customer({"message": "Reminder: phone CloudNest about the refund for your storage plan. If you need help from us (or want to set another reminder), message the card-care chat."})` → `{"channel": "secure_message", "message_id": 1, "status": "sent"}`

**Assistant:** Sent your reminder via secure message: **phone CloudNest about the refund for your storage plan.** If you need anything else, message the card-care chat.

_Episode written:_ Scheduled follow-up on 2026-11-15 (customer not present): The customer's scheduled follow-up F-4d30e77d requested a reminder to phone CloudNest about a storage-plan refund; the customer said a refund is involved (not verified). The assistant checked follow-ups (none listed) and sent one secure message, message_id 1. No transaction id was provided and no promise was stated. Case outcomes: no case touched. Lesson: none

_outcomes:_ `[{"followup_id": "F-4d30e77d", "user_id": "dana", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | the reminder is sent | `[{"followup_id": "F-4d30e77d", "user_id": "dana", "outcome": "fired_done", "error": null}]` |
| **FAIL** | prospective | and its note, the customer's words, is purged from the scheduler once it is done | `{"storage plan": ["scheduler.db"]}` |
