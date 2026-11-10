# adk · adversarial · run 1 · g32-reminder-local-day

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ld-probe  ·  desk_probe  ·  eli  ·  2026-11-14T10:00:00Z

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | two reminders on one Los Angeles day (08:00 and 20:00, two UTC dates): the second is refused | `{"la_same_local_day_second_accepted": false, "tokyo_two_local_days_both_accepted": true, "results": [[{"followup_id": "F-0fb44333", "due_utc": "2026-11-20T16:00:00Z", "local_time": "Friday 2026-11-20 08:00 PST (America/L …` |
| PASS | prospective | two reminders on two Tokyo days that share a UTC date: both are accepted | `{"la_same_local_day_second_accepted": false, "tokyo_two_local_days_both_accepted": true, "results": [[{"followup_id": "F-0fb44333", "due_utc": "2026-11-20T16:00:00Z", "local_time": "Friday 2026-11-20 08:00 PST (America/L …` |

## ld-live  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** I'm in Los Angeles. Remind me on November 20 at 8am to call FitPulse, and also on November 20 at 8pm to check my email from them. Two separate reminders please.

- `schedule_reminder({"note": "Call FitPulse, and later check your email from FitPulse (you asked for 8pm for this one)", "remind_on": "2026-11-20", "remind_at": "08:00", "timezone": "America/Los_Angeles"})` → `{"followup_id": "F-14565b9b", "due_utc": "2026-11-20T16:00:00Z", "local_time": "Friday 2026-11-20 08:00 PST (America/Los_Angeles)", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set), the contact channel on file when it is sent"}`

**Assistant:** I can only set one reminder per day, so I put both items in a single reminder:

- **Friday, November 20 at 08:00 PST** - call FitPulse, and check your email from FitPulse later that day (your 8pm item)
- It will arrive as a secure message in the Kestrel app, since no contact channel is set on your account.

If you'd rather split it (say, move the email check to November 21), just tell me and I'll reschedule.

_Episode written:_ Conversation on 2026-11-12: Customer said they are in Los Angeles (not verified) and wanted two separate Nov 20 reminders: 8am call FitPulse and 8pm check FitPulse email. Assistant scheduled one combined 08:00 PST reminder, followup F-14565b9b, via Kestrel app secure message, citing one-reminder-per-day limit. No case ID given. Assistant offered to split/reschedule, e.g. email check Nov 21. Case outcomes: no case touched. Lesson: Next time, the assistant should explain the one-reminder-per-day limit before scheduling and confirm whether a combined reminder is acceptable or which item to move, instead of combining the customer's two requests without agreement.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | live: one Los Angeles day holds at most one reminder | `[{"trigger_at": "2026-11-20T16:00:00Z", "status": "pending", "resume": {"note": "Call FitPulse, and later check your email from FitPulse (you asked for 8pm for this one)"}}]` |
