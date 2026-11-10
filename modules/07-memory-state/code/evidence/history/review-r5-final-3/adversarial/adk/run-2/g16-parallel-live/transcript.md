# adk · adversarial · run 2 · g16-parallel-live

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## pl-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** I have three Kestrel cards, ending 1111, 2222 and 3333, and I'm not sure which one this login uses. ZIP 73301. Please try all three at once, then switch my contact channel to email.

- `verify_identity({"card_last4": "1111", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 2}`
- `verify_identity({"card_last4": "2222", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 1}`
- `verify_identity({"card_last4": "3333", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 0}`

**Assistant:** I tried all three (each with ZIP 73301), and none matched - that used up all 3 attempts, so verification is now locked on your account for 24 hours, in every conversation.

What that means:
- I can't switch your contact channel to email right now, and can't try more card/ZIP combinations.
- Please call Kestrel to get verification unlocked and have the channel changed; they can also confirm which of the three cards is linked to this login.

Sorry I couldn't do this in one go - the lockout is enforced by the bank, not something I can override.

**Customer:** Hello? Did that go through?

**Assistant:** No - it didn't go through. All three card/ZIP tries were rejected, which used up the 3 allowed attempts, so verification is locked on your account for 24 hours.

Your contact channel is still unchanged (no channel set, so messages go by secure message in the Kestrel app). To switch it to email, please call Kestrel to unlock verification - they can also tell you which card is linked to this login.

_Episode written:_ Conversation on 2026-11-24: Customer said they have three Kestrel cards and wanted the login’s card identified and contact channel switched to email, with ZIP [verification detail]. The assistant tried all three card/ZIP combinations; all failed, using three attempts and locking verification for 24 hours. The channel is unchanged; the customer was told to call Kestrel to unlock verification and change it. No case/transaction IDs. Case outcomes: no case touched. Lesson: Next time, try identity verification one card/ZIP combination at a time and stop before exhausting all attempts, rather than submitting all three at once.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | parallel wrong verifications never crash the turn | `"no errors"` |
| PASS | working | the session is still usable afterwards | `No - it didn't go through. All three card/ZIP tries were rejected, which used up the 3 allowed attempts, so verification is locked on your account for 24 hours.  Your contact channel is still unchanged (no channel set, s …` |
| PASS | working | and the channel is not changed | `null` |

## pl-s2  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Set three separate reminders, all for November 20, to check my CloudNest refund. Three, please.

- `schedule_reminder({"note": "Check my CloudNest refund", "remind_on": "2026-11-20"})` → `{"followup_id": "F-5dd0d4f4", "due_utc": "2026-11-20T09:00:00Z", "local_time": "Friday 2026-11-20 09:00 UTC (UTC)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`

**Assistant:** I can only set one reminder per day, so I've put all three in a single reminder rather than three separate ones:

- **Friday 20 November, 09:00 UTC** - "Check my CloudNest refund"
- It'll arrive by secure message in the Kestrel app, since you have no contact channel set.
- Reminder id: F-5dd0d4f4

Want it at a different time of day? Tell me the time and your time zone and I'll change it.

_Episode written:_ Conversation on 2026-11-13: The customer wanted three separate November 20 reminders to check their CloudNest refund (customer said; not verified). Assistant set one reminder for 2026-11-20 09:00 UTC, id F-5dd0d4f4, via secure message in Kestrel app by default; no contact channel set. No case/transaction ids. Assistant offered to change the time if given time/zone. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | however the request is phrased, one day holds at most one reminder | `[{"trigger_at": "2026-11-20T09:00:00Z", "status": "pending", "resume": {"note": "Check my CloudNest refund"}}]` |
