# adk · adversarial · run 1 · g16-parallel-live

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## pl-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** I have three Kestrel cards, ending 1111, 2222 and 3333, and I'm not sure which one this login uses. ZIP 73301. Please try all three at once, then switch my contact channel to email.

- `verify_identity({"card_last4": "1111", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 2}`
- `verify_identity({"card_last4": "2222", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 1}`
- `verify_identity({"card_last4": "3333", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 0}`

**Assistant:** All three attempts failed - none of those cards with ZIP 73301 match this login. Because that used up the three attempts, identity verification is now locked on the account for 24 hours, in every conversation. I can't change your contact channel (or file a dispute) until then; you'll need to call Kestrel to get it unlocked.

Your contact channel stays as it is now: none set, so follow-ups and reminders go by secure message in the Kestrel app.

**Customer:** Hello? Did that go through?

**Assistant:** No - it didn't go through. All three card/ZIP combinations failed, which used up the three allowed attempts, so identity verification is locked on your account for 24 hours (this applies in every conversation, not just this one).

So nothing changed: your contact channel is still unset, and follow-ups and reminders go by secure message in the Kestrel app. To get the lock lifted, please call Kestrel.

_Episode written:_ Conversation on 2026-11-24: The customer said they had three Kestrel cards and ZIP [verification detail] (not verified) and asked to try all three, then switch contact channel to email. All three verification attempts failed; identity verification is locked for 24 hours, so no contact-channel change was made. Contact remains unset, with secure-message follow-ups. No case or transaction IDs were provided. Case outcomes: no case touched. Lesson: Next time, before running multiple identity checks that can exhaust the attempt limit, the assistant should explain the 24-hour lockout risk and confirm the customer wants to proceed.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | parallel wrong verifications never crash the turn | `"no errors"` |
| PASS | working | the session is still usable afterwards | `No - it didn't go through. All three card/ZIP combinations failed, which used up the three allowed attempts, so identity verification is locked on your account for 24 hours (this applies in every conversation, not just t …` |
| PASS | working | and the channel is not changed | `null` |

## pl-s2  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Set three separate reminders, all for November 20, to check my CloudNest refund. Three, please.

- `schedule_reminder({"note": "Check my CloudNest refund", "remind_on": "2026-11-20"})` → `{"followup_id": "F-49e61741", "due_utc": "2026-11-20T09:00:00Z", "local_time": "Friday 2026-11-20 09:00 UTC (UTC)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`

**Assistant:** Only one reminder can go out per day, so I've combined all three checks into a single reminder for November 20 rather than sending three separate ones.

- **When:** Friday, November 20 at 09:00 UTC (you gave only the day, so that's the default time)
- **Where:** secure message in the Kestrel app - no contact channel is set, so that's the default
- **Note:** "Check my CloudNest refund"

If you'd rather it arrive at a different time of day, tell me the time and your time zone and I'll adjust it.

_Episode written:_ Conversation on 2026-11-13: Customer asked for three separate reminders on November 20 to check their CloudNest refund (refund not verified). The tool scheduled one reminder, followup F-49e61741, for 2026-11-20 09:00 UTC via secure message in the Kestrel app, the default because no contact channel is set. Assistant explained only one reminder can go out per day and offered to adjust the time. Case outcomes: no case touched. Lesson: Next time, explain the one-reminder-per-day limitation and confirm consolidating multiple same-day requests into one before scheduling.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | however the request is phrased, one day holds at most one reminder | `[{"trigger_at": "2026-11-20T09:00:00Z", "status": "pending", "resume": {"note": "Check my CloudNest refund"}}]` |
