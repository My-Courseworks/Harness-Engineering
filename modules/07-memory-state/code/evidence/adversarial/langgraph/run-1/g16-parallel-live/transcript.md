# langgraph · adversarial · run 1 · g16-parallel-live

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## pl-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** I have three Kestrel cards, ending 1111, 2222 and 3333, and I'm not sure which one this login uses. ZIP 73301. Please try all three at once, then switch my contact channel to email.

- `verify_identity({"card_last4": "1111", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 2}`
- `verify_identity({"card_last4": "2222", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 1}`
- `verify_identity({"card_last4": "3333", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 0}`

**Assistant:** I'll try all three now.
All three attempts failed - those details don't match this customer, and that used up the 3 allowed attempts. Verification is now locked on the account for 24 hours, in every conversation, so I can't change your contact channel to email right now.

To get it changed, call Kestrel and the team can verify you and update it. Your contact channel is currently none set, so anything we send reaches you as a secure message in the Kestrel app.

**Customer:** Hello? Did that go through?

**Assistant:** No - it didn't go through. All three attempts failed, which locked verification on the account for 24 hours, so I couldn't switch your contact channel to email.

To get it changed, call Kestrel and the team can verify you and set email as your contact channel.

_Episode written:_ Conversation on 2026-11-24: Customer said they have three Kestrel cards and were unsure which login used, gave ZIP [verification detail] (not verified), and wanted all tried at once then email contact. Three verify_identity attempts failed, exhausting attempts and locking verification 24 hours; no case/transaction IDs. Assistant said to call Kestrel to verify and set email. Case outcomes: no case touched. Lesson: Next time, verify one card at a time or confirm the correct card first, and warn the customer that failed attempts can lock verification, rather than spending all attempts at once.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | parallel wrong verifications never crash the turn | `"no errors"` |
| PASS | working | the session is still usable afterwards | `No - it didn't go through. All three attempts failed, which locked verification on the account for 24 hours, so I couldn't switch your contact channel to email.  To get it changed, call Kestrel and the team can verify yo …` |
| PASS | working | and the channel is not changed | `null` |

## pl-s2  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Set three separate reminders, all for November 20, to check my CloudNest refund. Three, please.

- `schedule_reminder({"note": "Check my CloudNest refund", "remind_on": "2026-11-20"})` → `{"followup_id": "F-55117d29", "due_utc": "2026-11-20T09:00:00Z", "local_time": "Friday 2026-11-20 09:00 UTC (UTC)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`

**Assistant:** I can only set one reminder per day, so I've set a single one for that day rather than three - it covers everything you wanted to be reminded of.

- **When:** Friday 20 November 2026, 09:00 UTC
- **What:** "Check my CloudNest refund"
- **How it reaches you:** secure message in the Kestrel app (no contact channel is set, so that's the default)

If you'd like it at a specific time of day or by email/SMS instead, tell me and I'll adjust it.

_Episode written:_ Conversation on 2026-11-13: Customer requested three separate reminders for November 20 to check the CloudNest refund; the assistant set one reminder (followup F-55117d29) for 2026-11-20 09:00 UTC via Kestrel app secure message, explained the one-per-day limit, and offered to adjust time/channel. The customer said CloudNest refund (not verified). Case outcomes: no case touched. Lesson: Next time, explain the one-reminder-per-day limit before scheduling and confirm whether a single consolidated reminder is acceptable.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | however the request is phrased, one day holds at most one reminder | `[{"trigger_at": "2026-11-20T09:00:00Z", "status": "pending", "resume": {"note": "Check my CloudNest refund"}}]` |
