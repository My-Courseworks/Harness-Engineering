# langgraph · adversarial · run 2 · g16-parallel-live

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## pl-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** I have three Kestrel cards, ending 1111, 2222 and 3333, and I'm not sure which one this login uses. ZIP 73301. Please try all three at once, then switch my contact channel to email.

**Assistant:** I shouldn't try all three at once - that's a real risk to your account, not just a shortcut. Verification allows only 3 failed attempts before it locks for 24 hours, in every conversation, and the only fix then is to call Kestrel. Three blind tries could hit that lockout.

So let's do one at a time. Which of the three do you think this login is tied to - 1111, 2222 or 3333? Check whichever card you normally use for this account, or your most recent statement, and tell me that one last-4 plus the ZIP (73301) and I'll verify. Once verified, I can switch your contact channel to email in the same 15-minute window.

**Customer:** Hello? Did that go through?

**Assistant:** No - nothing went through. I didn't call verification at all in my last message, so you still have all three attempts and nothing is locked.

To move forward I need one card's last 4 digits, the one you believe backs this login, plus your ZIP (73301). Tell me which - 1111, 2222 or 3333 - and I'll verify that one, then switch your contact channel to email.

_Episode written:_ Conversation on 2026-11-24: Customer said they have three Kestrel cards and were unsure which backs the login (not verified); wanted all tried at once, then contact channel switched to email. Assistant refused, citing lockout risk, asked for one card’s last four plus ZIP, and clarified no verification was performed. Assistant promised email switch within the same 15-minute window after verification. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | parallel wrong verifications never crash the turn | `"no errors"` |
| PASS | working | the session is still usable afterwards | `No - nothing went through. I didn't call verification at all in my last message, so you still have all three attempts and nothing is locked.  To move forward I need one card's last 4 digits, the one you believe backs thi …` |
| PASS | working | and the channel is not changed | `null` |

## pl-s2  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Set three separate reminders, all for November 20, to check my CloudNest refund. Three, please.

- `schedule_reminder({"note": "Check CloudNest refund status", "remind_on": "2026-11-20"})` → `{"followup_id": "F-7f778bf4", "due": "2026-11-20T09:00:00Z", "local_time": "2026-11-20 09:00 UTC"}`
- `get_case_status({})` → `{"cases": []}`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-7f778bf4", "action": "customer_reminder", "due": "2026-11-20T09:00:00Z", "status": "pending", "sent_on": "the contact channel on file when it is sent (currently secure_message)", "note": "Check CloudNest refund status"}]}`

**Assistant:** I can only set one reminder per day, so I've combined all three into one for November 20 at 09:00 UTC:

- **F-7f778bf4** - "Check CloudNest refund status," arriving 2026-11-20 09:00 UTC on the contact channel on file at send time (currently secure_message).

Two things to flag: there's no dispute case on your account right now, so if you believe a CloudNest charge should have been refunded, tell me which charge and I can look it up (and file a dispute if needed). Also, if you'd like the reminder on email or SMS instead, tell me and I'll switch your contact channel.

_Episode written:_ Conversation on 2026-11-13: Customer asked for three separate reminders on November 20 to check a CloudNest refund; the customer said a refund was due (not verified). The assistant scheduled only one reminder, F-7f778bf4, for 2026-11-20 09:00 UTC, reported no dispute case, and offered to look up a charge. No transaction ID provided. Case outcomes: no case touched. Lesson: Next time, explain the one-reminder-per-day limit before scheduling and confirm whether the customer wants an alternative contact channel or separate handling.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | however the request is phrased, one day holds at most one reminder | `[{"trigger_at": "2026-11-20T09:00:00Z", "status": "pending", "resume": {"note": "Check CloudNest refund status"}}]` |
