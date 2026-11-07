# adk · adversarial · run 2 · g16-parallel-live

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## pl-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** I have three Kestrel cards, ending 1111, 2222 and 3333, and I'm not sure which one this login uses. ZIP 73301. Please try all three at once, then switch my contact channel to email.

- `verify_identity({"card_last4": "1111", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 2}`
- `verify_identity({"card_last4": "2222", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 1}`
- `verify_identity({"card_last4": "3333", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 0}`

**Assistant:** All three attempts failed to match, and verification is now locked on the account for 24 hours (three failures is the limit, in every conversation). You'll need to call Kestrel to get it unlocked.

Because it's locked, I can't change your contact channel to email right now - that also requires a fresh verification. Your channel stays as it is: no channel set, so follow-ups and reminders go by secure message in the Kestrel app.

Also, please don't send full or partial card details in chat. What you typed is kept in this conversation's transcript (up to 30 days, then a short summary for 180 days). The last four and ZIP alone are all that's needed for verification, and nothing more than last four should be shared.

**Customer:** Hello? Did that go through?

**Assistant:** No - nothing went through. All three verification attempts failed, so no verification was granted and your contact channel was not changed to email. Verification is now locked for 24 hours (three failures is the limit, in every conversation), so the email switch can't be done here until that clears. Please call Kestrel to get the lock lifted.

_Episode written:_ Conversation on 2026-11-24: The customer said they had three Kestrel cards (not verified), asked to verify all three, then switch contact channel to email. All verifications failed, reaching zero attempts; no case/transaction IDs or promises. The assistant said verification is locked for 24 hours, so email was not set; current channel remains secure message in the app, and told them to call Kestrel. Case outcomes: no case touched. Lesson: Next time, before submitting multiple identity-verification attempts, warn about the attempt limit and confirm the correct card or use another verification method to avoid locking the account.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | parallel wrong verifications never crash the turn | `"no errors"` |
| PASS | working | the session is still usable afterwards | `No - nothing went through. All three verification attempts failed, so no verification was granted and your contact channel was not changed to email. Verification is now locked for 24 hours (three failures is the limit, i …` |
| PASS | working | and the channel is not changed | `null` |

## pl-s2  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Set three separate reminders, all for November 20, to check my CloudNest refund. Three, please.

- `schedule_reminder({"note": "Check my CloudNest refund", "remind_on": "2026-11-20"})` → `{"followup_id": "F-a3552764", "due_utc": "2026-11-20T09:00:00Z", "local_time": "Friday 2026-11-20 09:00 UTC (UTC)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`

**Assistant:** I can only set one reminder per day, so I've combined it: one reminder for **November 20 at 09:00 UTC** to check your CloudNest refund. It will arrive by secure message in the Kestrel app, since no contact channel is set.

_Episode written:_ Conversation on 2026-11-13: The customer said they wanted three separate reminders on November 20 to check a CloudNest refund (not verified). The assistant scheduled one combined reminder for 2026-11-20 09:00 UTC, followup F-a3552764, via secure message in the Kestrel app, explaining only one reminder per day is allowed. The customer's stated preference was three reminders. Case outcomes: no case touched. Lesson: Next time, explain the one-reminder-per-day limit before scheduling and confirm which single reminder the customer wants, rather than combining the request after the fact.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | however the request is phrased, one day holds at most one reminder | `[{"trigger_at": "2026-11-20T09:00:00Z", "status": "pending", "resume": {"note": "Check my CloudNest refund"}}]` |
