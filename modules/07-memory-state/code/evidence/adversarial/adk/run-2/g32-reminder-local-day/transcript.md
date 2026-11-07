# adk · adversarial · run 2 · g32-reminder-local-day

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ld-probe  ·  desk_probe  ·  eli  ·  2026-11-14T10:00:00Z

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | two reminders on one Los Angeles day (08:00 and 20:00, two UTC dates): the second is refused | `{"la_same_local_day_second_accepted": false, "tokyo_two_local_days_both_accepted": true, "results": [[{"followup_id": "F-ccd9838a", "due_utc": "2026-11-20T16:00:00Z", "local_time": "Friday 2026-11-20 08:00 PST (America/L …` |
| PASS | prospective | two reminders on two Tokyo days that share a UTC date: both are accepted | `{"la_same_local_day_second_accepted": false, "tokyo_two_local_days_both_accepted": true, "results": [[{"followup_id": "F-ccd9838a", "due_utc": "2026-11-20T16:00:00Z", "local_time": "Friday 2026-11-20 08:00 PST (America/L …` |

## ld-live  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** I'm in Los Angeles. Remind me on November 20 at 8am to call FitPulse, and also on November 20 at 8pm to check my email from them. Two separate reminders please.

- `schedule_reminder({"note": "Call FitPulse at 8:00am, and check my email from FitPulse at 8:00pm", "remind_on": "2026-11-20", "remind_at": "08:00", "timezone": "America/Los_Angeles"})` → `{"followup_id": "F-52d80245", "due_utc": "2026-11-20T16:00:00Z", "local_time": "Friday 2026-11-20 08:00 PST (America/Los_Angeles)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`

**Assistant:** I can only send one reminder per day, so I've combined both into a single reminder for November 20:

- **When:** Friday, November 20 at 8:00am PST (Los Angeles time)
- **What it says:** "Call FitPulse at 8:00am, and check my email from FitPulse at 8:00pm"
- **Where:** secure message in the Kestrel app (no contact channel is set on your account)
- Reminder id: F-52d80245

If you'd rather have the email check at 8pm instead of 8am, I can move the reminder - but it has to be one per day.

_Episode written:_ Conversation on 2026-11-12: Customer wanted two separate Los Angeles reminders on November 20: 8am call FitPulse and 8pm check their email. Assistant scheduled one combined reminder for 8am (id F-52d80245) via Kestrel app, citing one reminder per day and offering to move it; no contact channel set. Case outcomes: no case touched. Lesson: Next time, confirm any one-reminder-per-day limitation and get customer agreement before combining separately requested reminders.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | live: one Los Angeles day holds at most one reminder | `[{"trigger_at": "2026-11-20T16:00:00Z", "status": "pending", "resume": {"note": "Call FitPulse at 8:00am, and check my email from FitPulse at 8:00pm"}}]` |
