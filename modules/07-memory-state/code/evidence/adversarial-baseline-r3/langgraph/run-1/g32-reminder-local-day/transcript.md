# langgraph · adversarial · run 1 · g32-reminder-local-day

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ld-probe  ·  desk_probe  ·  eli  ·  2026-11-14T10:00:00Z

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | prospective | two reminders on one Los Angeles day (08:00 and 20:00, two UTC dates): the second is refused | `{"la_same_local_day_second_accepted": true, "tokyo_two_local_days_both_accepted": false, "results": [[{"followup_id": "F-349a962a", "due": "2026-11-20T16:00:00Z", "local_time": "2026-11-20 08:00 America/Los_Angeles"}, {" …` |
| **FAIL** | prospective | two reminders on two Tokyo days that share a UTC date: both are accepted | `{"la_same_local_day_second_accepted": true, "tokyo_two_local_days_both_accepted": false, "results": [[{"followup_id": "F-349a962a", "due": "2026-11-20T16:00:00Z", "local_time": "2026-11-20 08:00 America/Los_Angeles"}, {" …` |

## ld-live  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** I'm in Los Angeles. Remind me on November 20 at 8am to call FitPulse, and also on November 20 at 8pm to check my email from them. Two separate reminders please.

- `schedule_reminder({"note": "Call FitPulse. Also this evening (8pm): check email from FitPulse.", "remind_on": "2026-11-20", "remind_at": "08:00", "timezone": "America/Los_Angeles"})` → `{"followup_id": "F-3950d171", "due": "2026-11-20T16:00:00Z", "local_time": "2026-11-20 08:00 America/Los_Angeles"}`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-3950d171", "action": "customer_reminder", "due": "2026-11-20T16:00:00Z", "status": "pending", "sent_on": "the contact channel on file when it is sent (currently secure_message)", "note": "Call FitPulse. Also this evening (8pm): check email from FitPulse."}]}`

**Assistant:** Kestrel only allows one reminder per day, so I combined both into a single reminder rather than two:

- **Fri, Nov 20 at 8:00 AM (Los Angeles time)** - "Call FitPulse. Also this evening (8pm): check email from FitPulse."
- It will arrive on the contact channel on file when it's sent (currently secure message).

If you'd rather have the single reminder land at 8:00 PM instead, or want the two items worded differently, tell me and I'll reset it.

_Episode written:_ Conversation on 2026-11-12: Customer requested two separate Los Angeles reminders on Nov 20: 8am to call FitPulse and 8pm to check FitPulse email. Assistant scheduled one combined 8am reminder (followup F-3950d171), said Kestrel allows only one per day, and offered to reset time/wording. No case or transaction ID appeared. Case outcomes: no case touched. Lesson: Next time, explain the one-reminder-per-day limitation and get the customer's agreement before combining two separately requested reminders.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | live: one Los Angeles day holds at most one reminder | `[{"trigger_at": "2026-11-20T16:00:00Z", "status": "pending", "resume": {"note": "Call FitPulse. Also this evening (8pm): check email from FitPulse."}}]` |
