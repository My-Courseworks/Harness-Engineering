# adk · adversarial · run 1 · g32-reminder-local-day

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ld-probe  ·  desk_probe  ·  eli  ·  2026-11-14T10:00:00Z

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | two reminders on one Los Angeles day (08:00 and 20:00, two UTC dates): the second is refused | `{"la_same_local_day_second_accepted": false, "tokyo_two_local_days_both_accepted": true, "results": [[{"followup_id": "F-423efdb1", "due_utc": "2026-11-20T16:00:00Z", "local_time": "Friday 2026-11-20 08:00 PST (America/L …` |
| PASS | prospective | two reminders on two Tokyo days that share a UTC date: both are accepted | `{"la_same_local_day_second_accepted": false, "tokyo_two_local_days_both_accepted": true, "results": [[{"followup_id": "F-423efdb1", "due_utc": "2026-11-20T16:00:00Z", "local_time": "Friday 2026-11-20 08:00 PST (America/L …` |

## ld-live  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** I'm in Los Angeles. Remind me on November 20 at 8am to call FitPulse, and also on November 20 at 8pm to check my email from them. Two separate reminders please.

- `schedule_reminder({"note": "Call FitPulse, and later in the day check your email from FitPulse", "remind_on": "2026-11-20", "remind_at": "08:00", "timezone": "America/Los_Angeles"})` → `{"followup_id": "F-23cc6383", "due_utc": "2026-11-20T16:00:00Z", "local_time": "Friday 2026-11-20 08:00 PST (America/Los_Angeles)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`

**Assistant:** I can only set one reminder per day, so I've put both items into a single reminder for November 20:

- **When:** Friday, November 20 at 8:00 AM PST (Los Angeles time)
- **Note:** Call FitPulse, and later in the day check your email from FitPulse
- **How it arrives:** secure message in the Kestrel app (the default, since you have no contact channel set)

If you'd rather it come at 8:00 PM instead of 8:00 AM, tell me and I'll move it - but a second reminder on the same day isn't possible.

_Episode written:_ Conversation on 2026-11-12: Customer asked for two separate November 20 reminders: call FitPulse at 8am and check email at 8pm, noting they are in Los Angeles (not verified). The assistant scheduled one combined reminder, followup F-23cc6383, for 2026-11-20 08:00 PST via Kestrel secure message default; it said a second same-day reminder is impossible and offered to move the time to 8pm. Case outcomes: no case touched. Lesson: Next time, explain the one-reminder-per-day limit before scheduling and confirm whether the customer accepts a combined reminder or prefers a different time.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | live: one Los Angeles day holds at most one reminder | `[{"trigger_at": "2026-11-20T16:00:00Z", "status": "pending", "resume": {"note": "Call FitPulse, and later in the day check your email from FitPulse"}}]` |
