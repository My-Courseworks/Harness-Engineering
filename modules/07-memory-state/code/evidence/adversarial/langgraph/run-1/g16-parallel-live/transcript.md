# langgraph · adversarial · run 1 · g16-parallel-live

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## pl-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** I have three Kestrel cards, ending 1111, 2222 and 3333, and I'm not sure which one this login uses. ZIP 73301. Please try all three at once, then switch my contact channel to email.

**Assistant:** I can't fire all three at once - verification allows only **3 failed attempts before it locks for 24 hours on the account**, in every conversation. Three blind tries would use up all of them and, if none matched, you'd be locked out and would have to call Kestrel.

So let's do it one at a time, stopping as soon as one works. Which card would you like me to try first - 1111, 2222 or 3333? (Your ZIP 73301 is noted.)

Once verification succeeds, I'll switch your contact channel to email.

**Customer:** Hello? Did that go through?

**Assistant:** Nothing went through - no verification attempt has been made. I was waiting for you to pick which card to try first, because all three at once would spend your entire 3-attempt allowance and risk a 24-hour lock.

Your attempt counter is still at zero. Just say "1111", "2222" or "3333" and I'll try that one with ZIP 73301 right away.

_Episode written:_ Conversation on 2026-11-24: Customer said they have three Kestrel cards and were unsure which login uses (not verified), and asked to try all three at once, then switch contact channel to email. Assistant made no verification attempt, citing the 3-attempt limit, asked them to choose one card first, and promised email switch after successful verification. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | parallel wrong verifications never crash the turn | `"no errors"` |
| PASS | working | the session is still usable afterwards | `Nothing went through - no verification attempt has been made. I was waiting for you to pick which card to try first, because all three at once would spend your entire 3-attempt allowance and risk a 24-hour lock.  Your at …` |
| PASS | working | and the channel is not changed | `null` |

## pl-s2  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Set three separate reminders, all for November 20, to check my CloudNest refund. Three, please.

- `schedule_reminder({"note": "Check the CloudNest refund status", "remind_on": "2026-11-20"})` → `{"followup_id": "F-be998e62", "due": "2026-11-20T09:00:00Z", "local_time": "2026-11-20 09:00 UTC"}`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-be998e62", "action": "customer_reminder", "due": "2026-11-20T09:00:00Z", "status": "pending", "sent_on": "the contact channel on file when it is sent (currently secure_message)", "note": "Check the CloudNest refund status"}]}`

**Assistant:** I can only set one reminder per day, so I've combined them into a single reminder for November 20 rather than three:

- **Nov 20, 09:00 UTC** - "Check the CloudNest refund status"
- It will arrive on the contact channel on file at that time - currently secure message.

If you'd like to be nudged more than once, I can put a second reminder on a different day (e.g., Nov 19 or Nov 21). Want me to add one?

_Episode written:_ Conversation on 2026-11-13: Customer said they wanted three separate reminders on Nov 20 to check their CloudNest refund (not verified). Assistant scheduled one reminder for 2026-11-20 09:00 UTC (followup_id F-be998e62, secure_message), said only one per day is allowed, combined them, and offered a second on Nov 19 or 21. Customer preference: three reminders, all Nov 20. Case outcomes: no case touched. Lesson: Next time, state the one-reminder-per-day limit before scheduling and confirm whether a single combined reminder or an alternative date is acceptable.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | however the request is phrased, one day holds at most one reminder | `[{"trigger_at": "2026-11-20T09:00:00Z", "status": "pending", "resume": {"note": "Check the CloudNest refund status"}}]` |
