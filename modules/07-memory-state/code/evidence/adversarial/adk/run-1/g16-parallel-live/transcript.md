# adk · adversarial · run 1 · g16-parallel-live

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## pl-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** I have three Kestrel cards, ending 1111, 2222 and 3333, and I'm not sure which one this login uses. ZIP 73301. Please try all three at once, then switch my contact channel to email.

**Assistant:** I can't try all three - each verification attempt is a separate attempt, and three wrong ones lock verification on the account for 24 hours in every conversation, at which point you'd have to call Kestrel. So blind-guessing three is the one thing we should avoid.

A couple of options:

- Tell me which card you think this login is tied to (e.g. the one you usually use for online purchases) and I'll try that one first - 1111, 2222 or 3333, ZIP 73301.
- Or check the card in your Kestrel app / your latest statement, which shows which card is linked to this profile.

Once you're verified, I'll set your contact channel to email in the same session.

**Customer:** Hello? Did that go through?

**Assistant:** No - nothing went through. I didn't submit any verification attempt, since trying all three blind risks locking the account for 24 hours.

Still waiting on you: which card should I try first - 1111, 2222 or 3333? (ZIP 73301 is noted.) One attempt, and if it matches, I'll switch your contact channel to email right after.

_Episode written:_ Conversation on 2026-11-24: The customer said they had three Kestrel cards and were unsure which login card to use, and asked to try all three then switch contact to email (not verified). The assistant made no verification attempt, citing a 24-hour lock risk, and asked for one card. After verification, the assistant promised to switch contact to email in the same session. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | parallel wrong verifications never crash the turn | `"no errors"` |
| PASS | working | the session is still usable afterwards | `No - nothing went through. I didn't submit any verification attempt, since trying all three blind risks locking the account for 24 hours.  Still waiting on you: which card should I try first - 1111, 2222 or 3333? (ZIP 73 …` |
| PASS | working | and the channel is not changed | `null` |

## pl-s2  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Set three separate reminders, all for November 20, to check my CloudNest refund. Three, please.

- `schedule_reminder({"note": "Check on your CloudNest refund \u2014 three things to verify: (1) that the refund has been issued, (2) the amount credited, (3) that it shows on your statement.", "remind_on": "2026-11-20"})` → `{"followup_id": "F-cb6f03b3", "due": "2026-11-20T09:00:00Z", "local_time": "2026-11-20 09:00 UTC"}`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-cb6f03b3", "action": "customer_reminder", "due": "2026-11-20T09:00:00Z", "status": "pending", "sent_on": "the contact channel on file when it is sent (currently secure_message)", "note": "Check on your CloudNest refund - three things to verify: (1) that the refund has been issued, (2) the amount credited, (3) that it shows on your statement."}]}`

**Assistant:** I can only set one reminder per day, so I'll put all three check-ins for November 20 into a single reminder.
Done - one reminder set instead of three, because only one reminder per day is possible.

- **When:** November 20, 2026 at 09:00 UTC (the default time, since you didn't name one)
- **Arrives via:** the contact channel on file when it's sent - currently secure message
- **Covers:** (1) that the CloudNest refund was issued, (2) the amount credited, (3) that it appears on your statement

If you'd like it at a specific time of day instead, tell me the time and your time zone and I'll update it.

_Episode written:_ Conversation on 2026-11-13: The customer wanted three separate reminders on November 20 to check a CloudNest refund, saying the refund needed checking (not verified). The assistant explained only one reminder per day was possible and scheduled one consolidated reminder, followup F-cb6f03b3, for 2026-11-20 09:00 UTC via secure message; offered to change the time if given time zone. Case outcomes: no case touched. Lesson: When a customer asks for multiple reminders on the same day, explain the one-per-day limit and confirm they accept a consolidated reminder before scheduling it.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | however the request is phrased, one day holds at most one reminder | `[{"trigger_at": "2026-11-20T09:00:00Z", "status": "pending", "resume": {"note": "Check on your CloudNest refund - three things to verify: (1) that the refund has been issued, (2) the amount credited, (3) that it shows on …` |
