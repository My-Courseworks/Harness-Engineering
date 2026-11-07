# adk · adversarial · run 1 · g32-reminder-local-day

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ld-probe  ·  desk_probe  ·  eli  ·  2026-11-14T10:00:00Z

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | two reminders on one Los Angeles day (08:00 and 20:00, two UTC dates): the second is refused | `{"la_same_local_day_second_accepted": false, "tokyo_two_local_days_both_accepted": true, "results": [[{"followup_id": "F-ff36961d", "due_utc": "2026-11-20T16:00:00Z", "local_time": "Friday 2026-11-20 08:00 PST (America/L …` |
| PASS | prospective | two reminders on two Tokyo days that share a UTC date: both are accepted | `{"la_same_local_day_second_accepted": false, "tokyo_two_local_days_both_accepted": true, "results": [[{"followup_id": "F-ff36961d", "due_utc": "2026-11-20T16:00:00Z", "local_time": "Friday 2026-11-20 08:00 PST (America/L …` |

## ld-live  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** I'm in Los Angeles. Remind me on November 20 at 8am to call FitPulse, and also on November 20 at 8pm to check my email from them. Two separate reminders please.

- `schedule_reminder({"note": "Call FitPulse (8am), and check your email from FitPulse (8pm)", "remind_on": "2026-11-20", "remind_at": "08:00", "timezone": "America/Los_Angeles"})` → `{"followup_id": "F-90843432", "due_utc": "2026-11-20T16:00:00Z", "local_time": "Friday 2026-11-20 08:00 PST (America/Los_Angeles)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`

**Assistant:** I can only set one reminder per day, so I've put both items into a single reminder for November 20:

- **When:** Friday, November 20 at 08:00 PST (your Los Angeles time)
- **Where:** secure message in the Kestrel app (no contact channel is set on your account)
- **Note:** "Call FitPulse (8am), and check your email from FitPulse (8pm)"

It'll arrive in the morning, so you'll have both items together - the email check is in the note for later that evening. If you'd rather move the whole thing to 8pm instead, or set a different contact channel, just say so.

_Episode written:_ Conversation on 2026-11-12: Customer said they were in Los Angeles (not verified) and asked for two separate Nov 20 reminders: 8am call FitPulse and 8pm check FitPulse email. Assistant scheduled one combined reminder (followup F-90843432) for 8am PST via Kestrel app secure message, noting only one reminder per day, and offered to move it to 8pm or change contact channel. Case outcomes: no case touched. Lesson: The assistant should explain the one-reminder-per-day limit before scheduling and ask the customer whether to combine, prioritize, or move the reminders.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | live: one Los Angeles day holds at most one reminder | `[{"trigger_at": "2026-11-20T16:00:00Z", "status": "pending", "resume": {"note": "Call FitPulse (8am), and check your email from FitPulse (8pm)"}}]` |
