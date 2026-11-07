# adk · adversarial · run 1 · g16-parallel-live

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## pl-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** I have three Kestrel cards, ending 1111, 2222 and 3333, and I'm not sure which one this login uses. ZIP 73301. Please try all three at once, then switch my contact channel to email.

- `verify_identity({"card_last4": "1111", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 2}`
- `verify_identity({"card_last4": "2222", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 1}`
- `verify_identity({"card_last4": "3333", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 0}`

**Assistant:** All three attempts failed - the combination of each card's last four with ZIP 73301 didn't match the card on this login, and that used up the 3 allowed attempts. Verification is now locked on the account for 24 hours, in every conversation, so I can't switch your contact channel to email right now.

Please call Kestrel to sort out which card is on this login and to change your contact channel - they can do it while the lock is in place. You can try the email change here again after 24 hours.

**Customer:** Hello? Did that go through?

**Assistant:** No - nothing went through. All three verification attempts failed, so:

- Your contact channel is still unchanged (no email set; follow-ups and reminders still go by secure message in the Kestrel app).
- Verification is locked on the account for 24 hours, so I can't make that change here until the lock clears.

To get the email set now, call Kestrel and they can do it for you. Otherwise, come back to this chat after 24 hours and I'll retry - double-checking the billing ZIP on the account first would help, since 73301 didn't match any of the three cards.

_Episode written:_ Conversation on 2026-11-24: Customer wanted contact channel changed to email and said they had three Kestrel cards, unsure which was on login (not verified). Assistant tried three identity checks with ZIP [verification detail]; all failed, exhausting attempts and locking verification for 24 hours. Email was not changed. No case/transaction IDs. Assistant advised calling Kestrel or returning after 24 hours to retry. Case outcomes: no case touched. Lesson: Next time, do not run all possible card verification attempts at once when attempts are limited; confirm the correct card or use an alternate verified route before consuming the lockout threshold.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | parallel wrong verifications never crash the turn | `"no errors"` |
| PASS | working | the session is still usable afterwards | `No - nothing went through. All three verification attempts failed, so:  - Your contact channel is still unchanged (no email set; follow-ups and reminders still go by secure message in the Kestrel app). - Verification is  …` |
| PASS | working | and the channel is not changed | `null` |

## pl-s2  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Set three separate reminders, all for November 20, to check my CloudNest refund. Three, please.

- `schedule_reminder({"note": "Check CloudNest refund", "remind_on": "2026-11-20"})` → `{"followup_id": "F-052518ed", "due_utc": "2026-11-20T09:00:00Z", "local_time": "Friday 2026-11-20 09:00 UTC (UTC)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`

**Assistant:** I can only set one reminder per day, so I set a single reminder for November 20 rather than three separate ones:

- **When:** Friday, 2026-11-20 at 09:00 UTC
- **Where:** secure message in the Kestrel app (the default, since no contact channel is set)
- **Note:** Check CloudNest refund
- **Id:** F-052518ed

If you'd like it moved to a particular time of day, tell me the time and your time zone and I'll reschedule it.

_Episode written:_ Conversation on 2026-11-13: The customer asked for three separate reminders on November 20 to check a CloudNest refund. The assistant set one reminder for 2026-11-20 at 09:00 UTC via secure message in the Kestrel app (follow-up ID F-052518ed), explained only one reminder per day is possible, and offered to reschedule if given a time and time zone. Case outcomes: no case touched. Lesson: Next time, explain the one-reminder-per-day limitation before scheduling so the customer understands why only one of the three requested reminders was created.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | however the request is phrased, one day holds at most one reminder | `[{"trigger_at": "2026-11-20T09:00:00Z", "status": "pending", "resume": {"note": "Check CloudNest refund"}}]` |
