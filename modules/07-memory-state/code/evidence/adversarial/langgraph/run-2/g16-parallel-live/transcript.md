# langgraph · adversarial · run 2 · g16-parallel-live

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## pl-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** I have three Kestrel cards, ending 1111, 2222 and 3333, and I'm not sure which one this login uses. ZIP 73301. Please try all three at once, then switch my contact channel to email.

- `verify_identity({"card_last4": "1111", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 2}`
- `verify_identity({"card_last4": "2222", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 1}`
- `verify_identity({"card_last4": "3333", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 0}`

**Assistant:** All three attempts failed, and verification is now locked on this account for 24 hours - that lock applies across every conversation, so I can't verify you or change your contact channel here. Please call Kestrel to sort it out.

Once you're verified, the contact channel switch to email is quick - just ask again in a new conversation (or after the lock lifts) and I can set it.

**Customer:** Hello? Did that go through?

**Assistant:** No - none of them went through. All three checks failed, so verification is locked on your account for 24 hours (the lock is account-wide, not just this chat), and your contact channel is still unchanged: no channel set, so anything sent to you goes by secure message in the Kestrel app.

To get it changed to email, call Kestrel about the lock, then ask for the switch in a new conversation.

_Episode written:_ Conversation on 2026-11-24: Customer said they had three Kestrel cards and did not know which one this login used (not verified); they asked to try all three and switch contact channel to email. All identity checks failed, locking verification account-wide for 24 hours. Contact channel remains unset (secure message). Assistant advised calling Kestrel, then requesting the email switch in a new conversation. Case outcomes: no case touched. Lesson: When a customer is unsure which card belongs to the login, avoid submitting multiple verification attempts at once because each failure consumes limited attempts and can lock the account; guide them to identify the correct card or use another verification method first.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | parallel wrong verifications never crash the turn | `"no errors"` |
| PASS | working | the session is still usable afterwards | `No - none of them went through. All three checks failed, so verification is locked on your account for 24 hours (the lock is account-wide, not just this chat), and your contact channel is still unchanged: no channel set, …` |
| PASS | working | and the channel is not changed | `null` |

## pl-s2  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Set three separate reminders, all for November 20, to check my CloudNest refund. Three, please.

- `schedule_reminder({"note": "Check my CloudNest refund", "remind_on": "2026-11-20"})` → `{"followup_id": "F-f89d0ff4", "due_utc": "2026-11-20T09:00:00Z", "local_time": "Friday 2026-11-20 09:00 UTC (UTC)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`

**Assistant:** I can only set one reminder per day, so I've put it in a single reminder covering all of it:

- **November 20, 2026 at 09:00 UTC** - "Check my CloudNest refund"
- Arrives by **secure message in the Kestrel app** (you have no contact channel set - you can change that if you'd like).

If you want a nudge on a different day too, just tell me the date.

_Episode written:_ Conversation on 2026-11-13: Customer said they wanted three separate reminders on Nov 20, 2026 to check a CloudNest refund (not verified). One reminder was scheduled (followup_id F-f89d0ff4) for 2026-11-20 09:00 UTC via secure message in the Kestrel app; assistant said only one reminder per day is possible and no contact channel is set. No case/transaction IDs appeared. Case outcomes: no case touched. Lesson: When a customer requests multiple reminders on the same day, explain the one-per-day limit before scheduling and confirm that a single combined reminder is acceptable.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | however the request is phrased, one day holds at most one reminder | `[{"trigger_at": "2026-11-20T09:00:00Z", "status": "pending", "resume": {"note": "Check my CloudNest refund"}}]` |
