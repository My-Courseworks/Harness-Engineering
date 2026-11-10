# adk · adversarial · run 1 · g16-parallel-live

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## pl-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** I have three Kestrel cards, ending 1111, 2222 and 3333, and I'm not sure which one this login uses. ZIP 73301. Please try all three at once, then switch my contact channel to email.

- `verify_identity({"card_last4": "1111", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 2}`
- `verify_identity({"card_last4": "2222", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 1}`
- `verify_identity({"card_last4": "3333", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 0}`

**Assistant:** I'll run all three now.
None of the three matched: all three attempts failed, and verification is now locked on the account for 24 hours - in every conversation, not just this one. I can't try again or switch your contact channel until that clears.

Please call Kestrel to sort out verification and the contact-channel change. A likely cause is that the billing ZIP on file for this card isn't 73301, or this login's card isn't one of those three.

Once verification is available again, here's what the change will need: the correct last 4 and billing ZIP, then a one-time code sent to the mobile number or email the bank holds on the account, which I'd then confirm.

**Customer:** Hello? Did that go through?

**Assistant:** No - it didn't go through. All three attempts failed (last 4s 1111, 2222 and 3333 with ZIP 73301), and that used up the three allowed attempts, so verification is locked on the account for 24 hours.

I can't retry, and I can't change your contact channel to email until that lock clears. Please call Kestrel to get verification sorted. When it's available again, we'll need the correct last 4 and billing ZIP, plus a one-time code to the mobile number or email the bank holds on the account.

_Episode written:_ Conversation on 2026-11-24: Customer said they had three Kestrel cards and ZIP [verification detail], unsure which login uses (not verified); wanted all three verified at once, then contact channel switched to email. Assistant attempted them; all failed, exhausting attempts and locking verification for 24 hours across conversations. No case/transaction IDs. Customer was told to call Kestrel; retry and email change need lock cleared. Case outcomes: no case touched. Lesson: Before attempting multiple card verifications, explain that each failed try consumes limited attempts and can lock verification, and confirm the correct card and ZIP first.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | parallel wrong verifications never crash the turn | `"no errors"` |
| PASS | working | the session is still usable afterwards | `No - it didn't go through. All three attempts failed (last 4s 1111, 2222 and 3333 with ZIP 73301), and that used up the three allowed attempts, so verification is locked on the account for 24 hours.  I can't retry, and I …` |
| PASS | working | and the channel is not changed | `null` |

## pl-s2  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Set three separate reminders, all for November 20, to check my CloudNest refund. Three, please.

- `schedule_reminder({"note": "Check my CloudNest refund", "remind_on": "2026-11-20"})` → `{"followup_id": "F-c358861d", "due_utc": "2026-11-20T09:00:00Z", "local_time": "Friday 2026-11-20 09:00 UTC (UTC)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`

**Assistant:** I can only set one reminder per day, so I put everything for November 20 into a single reminder rather than three.

- **Reminder:** check your CloudNest refund
- **When:** Friday, 2026-11-20 at 09:00 UTC (the default time, since you didn't give one - tell me if you'd prefer another time and your time zone)
- **Where:** secure message in the Kestrel app (the default, since no contact channel is set)
- **Id:** F-c358861d

Want me to change the time, or look up the CloudNest charge on your account now?

_Episode written:_ Conversation on 2026-11-13: Customer asked for three separate reminders on 2026-11-20 to check a CloudNest refund the customer said existed (not verified). The assistant scheduled one reminder for 2026-11-20 09:00 UTC via Kestrel app secure message (followup F-c358861d), explaining only one reminder per day is possible, and offered to change the time or look up the charge. Case outcomes: no case touched. Lesson: Next time, explain the one-reminder-per-day limit before scheduling and confirm the customer's preferred time, time zone, and contact channel.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | however the request is phrased, one day holds at most one reminder | `[{"trigger_at": "2026-11-20T09:00:00Z", "status": "pending", "resume": {"note": "Check my CloudNest refund"}}]` |
