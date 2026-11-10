# langgraph · adversarial · run 1 · g16-parallel-live

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## pl-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** I have three Kestrel cards, ending 1111, 2222 and 3333, and I'm not sure which one this login uses. ZIP 73301. Please try all three at once, then switch my contact channel to email.

- `verify_identity({"card_last4": "1111", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 1}`
- `verify_identity({"card_last4": "2222", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 0}`
- `verify_identity({"card_last4": "3333", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 2}`

**Assistant:** I'll try all three now.
None of the three combinations matched, and the attempt limit has been used up - verification is now locked on the account for 24 hours, in every conversation. I can't switch your contact channel until that clears, so you'll need to call Kestrel to get it changed (or to sort out the card on file) - they can help you today.

For the record, your contact channel is currently not set, so follow-ups and reminders go by secure message in the Kestrel app.

**Customer:** Hello? Did that go through?

**Assistant:** No - it didn't go through. All three card endings failed to match with ZIP 73301, and that used up the attempt limit, so verification is locked on your account for 24 hours in every conversation.

Your contact channel is still unset (follow-ups go by secure message in the Kestrel app). To get it switched to email before the lock lifts, please call Kestrel and they can handle it for you.

_Episode written:_ Conversation on 2026-11-24: The customer said they had three Kestrel cards and was unsure which login used (not verified); wanted all tried at once, channel switched to email. Verification failed and exhausted attempts; assistant said verification is locked 24 hours in every conversation, cannot change channel, and advised calling Kestrel today. No case/transaction IDs provided; asked if it went through; assistant confirmed no. Case outcomes: no case touched. Lesson: Before trying multiple cards at once, the assistant should warn that each verification attempt counts toward the limit and check whether the customer wants to risk a 24-hour lockout.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | parallel wrong verifications never crash the turn | `"no errors"` |
| PASS | working | the session is still usable afterwards | `No - it didn't go through. All three card endings failed to match with ZIP 73301, and that used up the attempt limit, so verification is locked on your account for 24 hours in every conversation.  Your contact channel is …` |
| PASS | working | and the channel is not changed | `null` |

## pl-s2  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Set three separate reminders, all for November 20, to check my CloudNest refund. Three, please.

- `schedule_reminder({"note": "Check my CloudNest refund", "remind_on": "2026-11-20"})` → `{"followup_id": "F-15664ace", "due_utc": "2026-11-20T09:00:00Z", "local_time": "Friday 2026-11-20 09:00 UTC (UTC)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`

**Assistant:** I can only set one reminder per day, so I've bundled it into a single reminder for November 20 rather than three:

- **One reminder**, id F-15664ace, arriving **Friday 2026-11-20 at 09:00 UTC**, by **secure message in the Kestrel app** (the default, since you have no contact channel set).
- Note: "Check my CloudNest refund."

Want me to look up the CloudNest charge now, or add anything else to that reminder?

_Episode written:_ Conversation on 2026-11-13: The customer said they wanted three separate reminders on November 20 to check their CloudNest refund (not verified). The assistant set one bundled reminder, followup_id F-15664ace, due 2026-11-20 09:00 UTC, by secure message in the Kestrel app (default; no contact channel set), and offered to look up the charge. No case or transaction id was provided. Case outcomes: no case touched. Lesson: Next time, explain the one-reminder-per-day limit before scheduling and confirm that a single bundled reminder is acceptable.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | however the request is phrased, one day holds at most one reminder | `[{"trigger_at": "2026-11-20T09:00:00Z", "status": "pending", "resume": {"note": "Check my CloudNest refund"}}]` |
