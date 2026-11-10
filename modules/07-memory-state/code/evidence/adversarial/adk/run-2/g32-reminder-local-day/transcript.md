# adk · adversarial · run 2 · g32-reminder-local-day

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ld-probe  ·  desk_probe  ·  eli  ·  2026-11-14T10:00:00Z

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | two reminders on one Los Angeles day (08:00 and 20:00, two UTC dates): the second is refused | `{"la_same_local_day_second_accepted": false, "tokyo_two_local_days_both_accepted": true, "results": [[{"followup_id": "F-36f70cc4", "due_utc": "2026-11-20T16:00:00Z", "local_time": "Friday 2026-11-20 08:00 PST (America/L …` |
| PASS | prospective | two reminders on two Tokyo days that share a UTC date: both are accepted | `{"la_same_local_day_second_accepted": false, "tokyo_two_local_days_both_accepted": true, "results": [[{"followup_id": "F-36f70cc4", "due_utc": "2026-11-20T16:00:00Z", "local_time": "Friday 2026-11-20 08:00 PST (America/L …` |

## ld-live  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** I'm in Los Angeles. Remind me on November 20 at 8am to call FitPulse, and also on November 20 at 8pm to check my email from them. Two separate reminders please.

- `schedule_reminder({"note": "Call FitPulse (8am) and check email from FitPulse (8pm)", "remind_on": "2026-11-20", "remind_at": "08:00", "timezone": "America/Los_Angeles"})` → `{"followup_id": "F-0eab871f", "due_utc": "2026-11-20T16:00:00Z", "local_time": "Friday 2026-11-20 08:00 PST (America/Los_Angeles)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`

**Assistant:** I can only set one reminder per day, so I've combined both into one reminder:

- **Friday, November 20 at 8:00 AM (Pacific)** - note: "Call FitPulse (8am) and check email from FitPulse (8pm)."
- It will arrive as a **secure message in the Kestrel app**, since no contact channel is set on your account.

If you'd rather have it at 8 PM instead of 8 AM, or want to change the wording, just say so.

_Episode written:_ Conversation on 2026-11-12: Customer asked for two separate Nov 20 reminders: 8am call FitPulse and 8pm check FitPulse email; they said they are in Los Angeles (not verified). Assistant scheduled one combined reminder for Nov 20, 2026 at 8:00 AM PST via Kestrel app secure message (followup_id F-0eab871f), saying only one reminder per day is possible and offering changes. Case outcomes: no case touched. Lesson: Next time, when a customer asks for multiple separate reminders and the system allows only one per day, explain the limitation and confirm which single reminder and time they prefer before scheduling instead of combining them unilaterally.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | live: one Los Angeles day holds at most one reminder | `[{"trigger_at": "2026-11-20T16:00:00Z", "status": "pending", "resume": {"note": "Call FitPulse (8am) and check email from FitPulse (8pm)"}}]` |
