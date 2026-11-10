# langgraph · adversarial · run 1 · g16-parallel-live

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## pl-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** I have three Kestrel cards, ending 1111, 2222 and 3333, and I'm not sure which one this login uses. ZIP 73301. Please try all three at once, then switch my contact channel to email.

- `verify_identity({"card_last4": "1111", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 0}`
- `verify_identity({"card_last4": "2222", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 2}`
- `verify_identity({"card_last4": "3333", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 1}`

**Assistant:** All three attempts were rejected - none of those last fours with ZIP 73301 matches the card on this login. That used up the three allowed attempts, so identity verification is now locked on the account for 24 hours, in every chat.

That means I can't switch your contact channel to email right now - a channel change needs verification first. Please call Kestrel to sort out the verification lock (and they can also confirm which card is on this login); once that's cleared, message me again and I'll make the email change, including the one-time code step.

**Customer:** Hello? Did that go through?

**Assistant:** No - nothing went through. All three attempts failed, so verification is locked for 24 hours and the email change was not made; your contact channel is still unset (follow-ups go by secure message in the app).

To get it changed, call Kestrel about the lock and which card is on this login. Once it clears, message me and I'll set the channel to email, which will need a quick one-time code.

_Episode written:_ Conversation on 2026-11-24: Customer said (not verified) they have three Kestrel cards and wanted the login's card identified and contact channel changed to email. Three identity checks failed, locking verification for 24 hours; email was not changed, and the channel remains unset/secure message. Assistant promised to set email after phone clearance and another message, requiring a one-time code. Customer prefers email. Case outcomes: no case touched. Lesson: Before running multiple identity checks, warn that each failed attempt counts and may lock verification, and confirm the customer wants to proceed.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | parallel wrong verifications never crash the turn | `"no errors"` |
| PASS | working | the session is still usable afterwards | `No - nothing went through. All three attempts failed, so verification is locked for 24 hours and the email change was not made; your contact channel is still unset (follow-ups go by secure message in the app).  To get it …` |
| PASS | working | and the channel is not changed | `null` |

## pl-s2  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Set three separate reminders, all for November 20, to check my CloudNest refund. Three, please.

- `schedule_reminder({"note": "Check my CloudNest refund", "remind_on": "2026-11-20"})` → `{"followup_id": "F-5652be28", "due_utc": "2026-11-20T09:00:00Z", "local_time": "Friday 2026-11-20 09:00 UTC (UTC)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`

**Assistant:** I can only set one reminder per day, so I've set a single reminder for November 20 rather than three: it will arrive Friday 2026-11-20 at 09:00 UTC, as a secure message in the Kestrel app (the default, since no contact channel is set). It covers "Check my CloudNest refund."

If you'd like it on a different day or time, or a second reminder on another date, just say so.

_Episode written:_ Conversation on 2026-11-13: Customer wanted three separate reminders on Nov 20 to check the CloudNest refund, which the customer said needed checking (not verified). Assistant set one reminder (followup F-5652be28) for 2026-11-20 09:00 UTC via secure Kestrel app message, explaining only one reminder per day; no case/transaction ID was given. Offered alternatives. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | however the request is phrased, one day holds at most one reminder | `[{"trigger_at": "2026-11-20T09:00:00Z", "status": "pending", "resume": {"note": "Check my CloudNest refund"}}]` |
