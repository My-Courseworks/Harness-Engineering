# adk · adversarial · run 1 · g32-reminder-local-day

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ld-probe  ·  desk_probe  ·  eli  ·  2026-11-14T10:00:00Z

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | prospective | two reminders on one Los Angeles day (08:00 and 20:00, two UTC dates): the second is refused | `{"la_same_local_day_second_accepted": true, "tokyo_two_local_days_both_accepted": false, "results": [[{"followup_id": "F-2b4e6249", "due": "2026-11-20T16:00:00Z", "local_time": "2026-11-20 08:00 America/Los_Angeles"}, {" …` |
| **FAIL** | prospective | two reminders on two Tokyo days that share a UTC date: both are accepted | `{"la_same_local_day_second_accepted": true, "tokyo_two_local_days_both_accepted": false, "results": [[{"followup_id": "F-2b4e6249", "due": "2026-11-20T16:00:00Z", "local_time": "2026-11-20 08:00 America/Los_Angeles"}, {" …` |

## ld-live  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** I'm in Los Angeles. Remind me on November 20 at 8am to call FitPulse, and also on November 20 at 8pm to check my email from them. Two separate reminders please.

- `schedule_reminder({"note": "Call FitPulse; and in the evening, check your email from FitPulse.", "remind_on": "2026-11-20", "remind_at": "08:00", "timezone": "America/Los_Angeles"})` → `{"followup_id": "F-e447a86b", "due": "2026-11-20T16:00:00Z", "local_time": "2026-11-20 08:00 America/Los_Angeles"}`

**Assistant:** I can only set one reminder per day, so I've combined both into a single reminder on November 20 at 08:00 your time (Los Angeles) - it covers calling FitPulse and checking their email.

If you'd rather have it arrive at 8pm instead, tell me and I'll move it.

_Episode written:_ Conversation on 2026-11-12: The customer said they are in Los Angeles (not verified) and wanted two separate November 20 reminders: 8am call FitPulse, 8pm check their email. One combined 8am reminder was scheduled (followup F-e447a86b); the assistant said only one reminder per day and offered to move it to 8pm if requested. No case ID. Case outcomes: no case touched. Lesson: Next time, the assistant should explain the one-reminder-per-day limitation before scheduling and get the customer's consent before combining separate reminders.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | live: one Los Angeles day holds at most one reminder | `[{"trigger_at": "2026-11-20T16:00:00Z", "status": "pending", "resume": {"note": "Call FitPulse; and in the evening, check your email from FitPulse."}}]` |
