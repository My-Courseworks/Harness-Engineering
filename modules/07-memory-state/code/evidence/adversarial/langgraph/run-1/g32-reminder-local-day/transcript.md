# langgraph · adversarial · run 1 · g32-reminder-local-day

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ld-probe  ·  desk_probe  ·  eli  ·  2026-11-14T10:00:00Z

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | two reminders on one Los Angeles day (08:00 and 20:00, two UTC dates): the second is refused | `{"la_same_local_day_second_accepted": false, "tokyo_two_local_days_both_accepted": true, "results": [[{"followup_id": "F-8dcbd102", "due_utc": "2026-11-20T16:00:00Z", "local_time": "Friday 2026-11-20 08:00 PST (America/L …` |
| PASS | prospective | two reminders on two Tokyo days that share a UTC date: both are accepted | `{"la_same_local_day_second_accepted": false, "tokyo_two_local_days_both_accepted": true, "results": [[{"followup_id": "F-8dcbd102", "due_utc": "2026-11-20T16:00:00Z", "local_time": "Friday 2026-11-20 08:00 PST (America/L …` |

## ld-live  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** I'm in Los Angeles. Remind me on November 20 at 8am to call FitPulse, and also on November 20 at 8pm to check my email from them. Two separate reminders please.

- `schedule_reminder({"note": "Call FitPulse (8am), and check email from FitPulse (8pm)", "remind_on": "2026-11-20", "remind_at": "08:00", "timezone": "America/Los_Angeles"})` → `{"followup_id": "F-481049ca", "due_utc": "2026-11-20T16:00:00Z", "local_time": "Friday 2026-11-20 08:00 PST (America/Los_Angeles)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`

**Assistant:** I can only send one reminder per day, so I've combined both into a single reminder:

- **When:** Friday, November 20, 2026 at 8:00 AM PST (Los Angeles time)
- **Note:** Call FitPulse (8am), and check email from FitPulse (8pm)
- **Where:** secure message in the Kestrel app - the default, since you have no contact channel set

If you'd rather have it arrive at 8:00 PM instead so it's closer to the email check, say the word and I'll move it. You can also change where reminders go by setting a contact channel - just let me know.

_Episode written:_ Conversation on 2026-11-12: Customer said they are in Los Angeles (not verified) and asked for two separate Nov 20, 2026 reminders: 8am call FitPulse, 8pm check their email. Assistant scheduled one combined reminder at 8am (followup F-481049ca; no case/transaction id given), citing a one-reminder-per-day limit, and offered to move it to 8pm if requested. No firm promise. Case outcomes: no case touched. Lesson: Next time, confirm the one-reminder-per-day limitation and obtain agreement to combine or choose a time before scheduling, since the customer explicitly requested two separate reminders.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | live: one Los Angeles day holds at most one reminder | `[{"trigger_at": "2026-11-20T16:00:00Z", "status": "pending", "resume": {"note": "Call FitPulse (8am), and check email from FitPulse (8pm)"}}]` |
