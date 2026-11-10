# langgraph · adversarial · run 2 · g32-reminder-local-day

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ld-probe  ·  desk_probe  ·  eli  ·  2026-11-14T10:00:00Z

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | two reminders on one Los Angeles day (08:00 and 20:00, two UTC dates): the second is refused | `{"la_same_local_day_second_accepted": false, "tokyo_two_local_days_both_accepted": true, "results": [[{"followup_id": "F-2bcbd376", "due_utc": "2026-11-20T16:00:00Z", "local_time": "Friday 2026-11-20 08:00 PST (America/L …` |
| PASS | prospective | two reminders on two Tokyo days that share a UTC date: both are accepted | `{"la_same_local_day_second_accepted": false, "tokyo_two_local_days_both_accepted": true, "results": [[{"followup_id": "F-2bcbd376", "due_utc": "2026-11-20T16:00:00Z", "local_time": "Friday 2026-11-20 08:00 PST (America/L …` |

## ld-live  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** I'm in Los Angeles. Remind me on November 20 at 8am to call FitPulse, and also on November 20 at 8pm to check my email from them. Two separate reminders please.

- `schedule_reminder({"note": "Call FitPulse (planned for 8:00 AM), and later check your email from FitPulse (planned for 8:00 PM)", "remind_on": "2026-11-20", "remind_at": "08:00", "timezone": "America/Los_Angeles"})` → `{"followup_id": "F-f0881d59", "due_utc": "2026-11-20T16:00:00Z", "local_time": "Friday 2026-11-20 08:00 PST (America/Los_Angeles)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`

**Assistant:** I've scheduled it - but Kestrel allows only one reminder per day, so both items are in a single reminder rather than two:

- **When:** Friday 2026-11-20 at 08:00 PST (Los Angeles time)
- **Note:** Call FitPulse (planned for 8:00 AM), and later check your email from FitPulse (planned for 8:00 PM)
- **Where:** secure message in the Kestrel app (the default, since you have no contact channel set)

If you'd rather have reminders by email or SMS, I can set that up as your contact channel - it needs a quick identity check.

_Episode written:_ Conversation on 2026-11-12: Customer said they were in Los Angeles (not verified) and asked for two separate reminders on 2026-11-20: call FitPulse at 8am and check FitPulse email at 8pm. Only one combined 8am reminder was scheduled (followup_id F-f0881d59) because of a one-per-day limit; the assistant offered email/SMS setup with identity check. Case outcomes: no case touched. Lesson: Next time, confirm the one-reminder-per-day limit before combining requests and ask which single reminder the customer prefers or whether to set a contact channel.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | live: one Los Angeles day holds at most one reminder | `[{"trigger_at": "2026-11-20T16:00:00Z", "status": "pending", "resume": {"note": "Call FitPulse (planned for 8:00 AM), and later check your email from FitPulse (planned for 8:00 PM)"}}]` |
