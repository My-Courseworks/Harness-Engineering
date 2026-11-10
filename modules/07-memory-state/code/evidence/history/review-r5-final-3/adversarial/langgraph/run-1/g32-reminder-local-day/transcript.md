# langgraph · adversarial · run 1 · g32-reminder-local-day

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ld-probe  ·  desk_probe  ·  eli  ·  2026-11-14T10:00:00Z

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | two reminders on one Los Angeles day (08:00 and 20:00, two UTC dates): the second is refused | `{"la_same_local_day_second_accepted": false, "tokyo_two_local_days_both_accepted": true, "results": [[{"followup_id": "F-2385100b", "due_utc": "2026-11-20T16:00:00Z", "local_time": "Friday 2026-11-20 08:00 PST (America/L …` |
| PASS | prospective | two reminders on two Tokyo days that share a UTC date: both are accepted | `{"la_same_local_day_second_accepted": false, "tokyo_two_local_days_both_accepted": true, "results": [[{"followup_id": "F-2385100b", "due_utc": "2026-11-20T16:00:00Z", "local_time": "Friday 2026-11-20 08:00 PST (America/L …` |

## ld-live  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** I'm in Los Angeles. Remind me on November 20 at 8am to call FitPulse, and also on November 20 at 8pm to check my email from them. Two separate reminders please.

- `schedule_reminder({"note": "Call FitPulse, and in the evening (around 8pm) check your email from them", "remind_on": "2026-11-20", "remind_at": "08:00", "timezone": "America/Los_Angeles"})` → `{"followup_id": "F-59ad0e46", "due_utc": "2026-11-20T16:00:00Z", "local_time": "Friday 2026-11-20 08:00 PST (America/Los_Angeles)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`

**Assistant:** I can only set one reminder per day, so I've combined both into a single reminder:

- **Friday, November 20 at 8:00 AM PST** - reminder to call FitPulse, and to check your email from them in the evening (8pm).
- It will arrive as a secure message in the Kestrel app, since no contact channel is set on your account.

If you'd rather it arrive at 8pm instead of 8am, or want it on email or SMS, tell me and I'll adjust.

_Episode written:_ Conversation on 2026-11-12: Customer said they were in Los Angeles (not verified) and asked for two separate Nov 20 reminders: 8am to call FitPulse and 8pm to check email from them. Assistant said only one reminder per day was possible and scheduled one combined 8:00am PST reminder (followup F-59ad0e46), sent via Kestrel app secure message. No case ID provided. Case outcomes: no case touched. Lesson: The assistant should clarify reminder limits before combining requests and either set separate reminders or confirm the customer accepts a single combined reminder.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | live: one Los Angeles day holds at most one reminder | `[{"trigger_at": "2026-11-20T16:00:00Z", "status": "pending", "resume": {"note": "Call FitPulse, and in the evening (around 8pm) check your email from them"}}]` |
