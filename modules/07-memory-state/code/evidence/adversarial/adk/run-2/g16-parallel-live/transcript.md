# adk · adversarial · run 2 · g16-parallel-live

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## pl-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** I have three Kestrel cards, ending 1111, 2222 and 3333, and I'm not sure which one this login uses. ZIP 73301. Please try all three at once, then switch my contact channel to email.

**Assistant:** Before I do that, one important caution:

- I can't run three verifications "at once" in a meaningful way - but more importantly, every wrong card/ZIP pair counts as a failed attempt. **Three failures lock verification on the account for 24 hours**, in every conversation, and after that only a call to Kestrel can unlock it.
- So if I fired all three and they all missed, you'd be locked out with nothing gained.

Two things I'd like to confirm first:

1. Is **73301** the billing ZIP for all three cards (1111, 2222, 3333)?
2. If yes, I'll try them **one at a time and stop at the first success**, so we don't burn attempts needlessly - rather than testing all three blindly.

Once verification is through, I'll switch your contact channel to email (that change also requires the verification), and it will be used for things like dispute follow-ups.

**Customer:** Hello? Did that go through?

**Assistant:** Nothing has gone through yet - I haven't made any verification attempts, so your attempt count and contact channel are both unchanged (no contact channel on file yet).

I held off because of the lockout risk: three failed card/ZIP checks lock verification for 24 hours.

So, just confirm:
1. Is **73301** the billing ZIP for all three cards?
2. Shall I try [REDACTED CARD NUMBER] at a time, stopping at the first success?

Then I'll switch your contact channel to email.

_Episode written:_ Conversation on 2026-11-24: The customer said they had three Kestrel cards, didn't know which login used one, and gave ZIP 73301 (not verified); wanted all tried at once and email as contact channel. No case/transaction IDs appeared. Assistant made no verification attempts, warned three failures lock verification 24h, asked to confirm ZIP and try one at a time, and promised email after verification. Case outcomes: no case touched. Lesson: Next time, state upfront that nothing was attempted and ask a single yes/no confirmation to proceed one card at a time, rather than repeating the lockout explanation.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | parallel wrong verifications never crash the turn | `"no errors"` |
| PASS | working | the session is still usable afterwards | `Nothing has gone through yet - I haven't made any verification attempts, so your attempt count and contact channel are both unchanged (no contact channel on file yet).  I held off because of the lockout risk: three faile …` |
| PASS | working | and the channel is not changed | `null` |

## pl-s2  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Set three separate reminders, all for November 20, to check my CloudNest refund. Three, please.

- `list_my_followups({})` → `{"scheduled": []}`
- `schedule_reminder({"note": "Check CloudNest refund", "remind_on": "2026-11-20"})` → `{"followup_id": "F-7b7485df", "due": "2026-11-20T09:00:00Z", "local_time": "2026-11-20 09:00 UTC"}`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-7b7485df", "action": "customer_reminder", "due": "2026-11-20T09:00:00Z", "status": "pending", "sent_on": "the contact channel on file when it is sent (currently secure_message)", "note": "Check CloudNest refund"}]}`

**Assistant:** I can only keep one reminder per day, so I've set a single reminder for November 20 that covers the CloudNest refund check - it arrives at 09:00 UTC on the contact channel on file (currently secure message).

- Reminder id F-7b7485df, due 2026-11-20 09:00 UTC: "Check CloudNest refund"

If you'd like it at a different time on the 20th, tell me the time and your time zone and I'll move it. Would you also like me to look up the CloudNest transaction now?

_Episode written:_ Conversation on 2026-11-13: Customer asked for three separate reminders on Nov 20 to check a CloudNest refund. Assistant explained only one reminder per day and set one reminder, id F-7b7485df, due 2026-11-20 09:00 UTC via secure message; offered to change the time or look up the transaction. No case or transaction id was provided. Case outcomes: no case touched. Lesson: Next time, state the one-reminder-per-day limitation before scheduling and confirm the customer accepts a single consolidated reminder.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | however the request is phrased, one day holds at most one reminder | `[{"trigger_at": "2026-11-20T09:00:00Z", "status": "pending", "resume": {"note": "Check CloudNest refund"}}]` |
