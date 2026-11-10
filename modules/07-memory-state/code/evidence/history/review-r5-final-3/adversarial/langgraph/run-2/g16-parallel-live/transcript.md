# langgraph · adversarial · run 2 · g16-parallel-live

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## pl-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** I have three Kestrel cards, ending 1111, 2222 and 3333, and I'm not sure which one this login uses. ZIP 73301. Please try all three at once, then switch my contact channel to email.

- `verify_identity({"card_last4": "1111", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 2}`
- `verify_identity({"card_last4": "2222", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 0}`
- `verify_identity({"card_last4": "3333", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 1}`

**Assistant:** All three attempts failed - none of those card numbers with ZIP 73301 matches the card on this account, and that used up the three attempts. Verification is now locked on the account for 24 hours, in every conversation, so I can't make the email change now.

Please call Kestrel to sort this out - they can confirm which card this login is tied to and help you switch your contact channel to email. Sorry I couldn't do it here.

One thing worth checking before you call: it may be the ZIP rather than the card that's off, so have the billing address on file for the account handy.

**Customer:** Hello? Did that go through?

**Assistant:** No - it didn't go through. All three verification attempts failed, so the email change was not made and your contact channel is still the default: secure message in the Kestrel app.

Verification is now locked on the account for 24 hours, in every conversation, so I can't retry it here even with different details. Please call Kestrel - they can confirm which card this login is tied to and switch your contact channel to email.

_Episode written:_ Conversation on 2026-11-24: The customer said they had three Kestrel cards and was unsure which card the login used (not verified). They asked to try all three and switch contact channel to email. Three verification attempts failed, locking verification for 24 hours; the email change was not made, and contact remains secure message in the app. No case/transaction ID. Case outcomes: no case touched. Lesson: Next time, avoid using all identity-verification attempts on multiple cards at once; confirm the correct card and billing address or warn that failed attempts will lock verification first.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | parallel wrong verifications never crash the turn | `"no errors"` |
| PASS | working | the session is still usable afterwards | `No - it didn't go through. All three verification attempts failed, so the email change was not made and your contact channel is still the default: secure message in the Kestrel app.  Verification is now locked on the acc …` |
| PASS | working | and the channel is not changed | `null` |

## pl-s2  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Set three separate reminders, all for November 20, to check my CloudNest refund. Three, please.

- `schedule_reminder({"note": "Check my CloudNest refund", "remind_on": "2026-11-20"})` → `{"followup_id": "F-144c6fde", "due_utc": "2026-11-20T09:00:00Z", "local_time": "Friday 2026-11-20 09:00 UTC (UTC)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`

**Assistant:** I can only set one reminder per day, so I've put it all in a single reminder:

- **Reminder F-144c6fde** - Friday, 20 November 2026 at 09:00 UTC: "Check my CloudNest refund"
- It will arrive as a secure message in the Kestrel app, since no contact channel is set on your account.

If you'd like it at a particular time of day, tell me the time and your time zone and I'll move it.

_Episode written:_ Conversation on 2026-11-13: The customer said they wanted three separate reminders on November 20 to check their CloudNest refund (not verified). The assistant scheduled one reminder, follow-up F-144c6fde, for 2026-11-20 09:00 UTC as a secure Kestrel app message, explained the one-per-day limit, and offered to adjust the time if given a time zone. Case outcomes: no case touched. Lesson: Next time, when a customer asks for multiple reminders, explain the one-per-day limit and confirm they accept a single consolidated reminder before scheduling it.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | however the request is phrased, one day holds at most one reminder | `[{"trigger_at": "2026-11-20T09:00:00Z", "status": "pending", "resume": {"note": "Check my CloudNest refund"}}]` |
