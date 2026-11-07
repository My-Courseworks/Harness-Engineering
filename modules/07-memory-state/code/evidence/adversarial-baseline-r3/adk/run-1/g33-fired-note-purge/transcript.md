# adk · adversarial · run 1 · g33-fired-note-purge

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## fn-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Please remind me on November 15 to phone CloudNest about the refund for my storage plan.

- `schedule_reminder({"note": "Phone CloudNest about the refund for my storage plan", "remind_on": "2026-11-15"})` → `{"followup_id": "F-248b4253", "due": "2026-11-15T09:00:00Z", "local_time": "2026-11-15 09:00 UTC"}`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-248b4253", "action": "customer_reminder", "due": "2026-11-15T09:00:00Z", "status": "pending", "sent_on": "the contact channel on file when it is sent (currently secure_message)", "note": "Phone CloudNest about the refund for my storage plan"}]}`

**Assistant:** Reminder set for **15 November at 09:00 UTC**: "Phone CloudNest about the refund for my storage plan."

It will be sent on the contact channel on file when it goes out - currently secure message (in-app).

_Episode written:_ Conversation on 2026-11-13: Customer wanted a reminder on November 15 to phone CloudNest about a refund for their storage plan. The assistant scheduled reminder F-248b4253 for 2026-11-15 at 09:00 UTC; list_my_followups showed it pending via secure message. The customer said a refund is due for the storage plan (not verified). No other preference stated. Case outcomes: no case touched. Lesson: none

## fn-fire  ·  fire_followups  ·  2026-11-15T10:00:00Z

### follow-up session `followup-F-248b4253-1`

**Scheduler:** [scheduled follow-up F-248b4253] action=customer_reminder resume={"note": "Phone CloudNest about the refund for my storage plan"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `list_my_followups({})` → `{"scheduled": []}`
- `notify_customer({"message": "Reminder: call CloudNest about the refund for your storage plan. (No other follow-ups are currently scheduled. If you need anything else, message the card-care chat.)"})` → `{"channel": "secure_message", "message_id": 1, "status": "sent"}`

**Assistant:** Sent the reminder to the customer: "Reminder: call CloudNest about the refund for your storage plan." It went out on secure message (no other follow-ups are scheduled).

_Episode written:_ Scheduled follow-up on 2026-11-15 (customer not present): The customer said to phone CloudNest about a refund for their storage plan (not verified). The assistant checked scheduled follow-ups, found none, and sent one secure-message reminder (message_id 1; status sent), noting no other follow-ups are scheduled. No case or transaction ids are present. Case outcomes: no case touched. Lesson: none

_outcomes:_ `[{"followup_id": "F-248b4253", "user_id": "dana", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | the reminder is sent | `[{"followup_id": "F-248b4253", "user_id": "dana", "outcome": "fired_done", "error": null}]` |
| **FAIL** | prospective | and its note, the customer's words, is purged from the scheduler once it is done | `{"storage plan": ["scheduler.db"]}` |
