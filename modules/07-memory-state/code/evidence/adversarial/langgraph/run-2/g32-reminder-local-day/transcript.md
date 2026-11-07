# langgraph · adversarial · run 2 · g32-reminder-local-day

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ld-probe  ·  desk_probe  ·  eli  ·  2026-11-14T10:00:00Z

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | two reminders on one Los Angeles day (08:00 and 20:00, two UTC dates): the second is refused | `{"la_same_local_day_second_accepted": false, "tokyo_two_local_days_both_accepted": true, "results": [[{"followup_id": "F-fca92417", "due_utc": "2026-11-20T16:00:00Z", "local_time": "Friday 2026-11-20 08:00 PST (America/L …` |
| PASS | prospective | two reminders on two Tokyo days that share a UTC date: both are accepted | `{"la_same_local_day_second_accepted": false, "tokyo_two_local_days_both_accepted": true, "results": [[{"followup_id": "F-fca92417", "due_utc": "2026-11-20T16:00:00Z", "local_time": "Friday 2026-11-20 08:00 PST (America/L …` |

## ld-live  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** I'm in Los Angeles. Remind me on November 20 at 8am to call FitPulse, and also on November 20 at 8pm to check my email from them. Two separate reminders please.

- `schedule_reminder({"note": "Call FitPulse, and check your email from FitPulse", "remind_on": "2026-11-20", "remind_at": "08:00", "timezone": "America/Los_Angeles"})` → `{"followup_id": "F-3e3ee381", "due_utc": "2026-11-20T16:00:00Z", "local_time": "Friday 2026-11-20 08:00 PST (America/Los_Angeles)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`

**Assistant:** I can only set one reminder per day, so I've combined both into one for November 20:

- **Reminder F-3e3ee381** - Friday, November 20 at 08:00 PST: "Call FitPulse, and check your email from FitPulse"
- It will arrive as a secure message in the Kestrel app (the default, since no contact channel is set).

Since it comes in the morning, you'll want to handle the 8pm email check on your own - or tell me if you'd rather the single reminder fire in the evening instead.

_Episode written:_ Conversation on 2026-11-12: The customer said they are in Los Angeles (not verified) and requested two separate reminders for Nov 20: 8am call FitPulse and 8pm check FitPulse email. Assistant scheduled one combined reminder, F-3e3ee381, for 2026-11-20 08:00 PST as a Kestrel app secure message, explained only one reminder per day is allowed, and asked if the customer preferred evening. Case outcomes: no case touched. Lesson: Next time, the assistant should explain any one-reminder-per-day limitation before scheduling and get confirmation before combining two separately requested reminders.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | live: one Los Angeles day holds at most one reminder | `[{"trigger_at": "2026-11-20T16:00:00Z", "status": "pending", "resume": {"note": "Call FitPulse, and check your email from FitPulse"}}]` |
