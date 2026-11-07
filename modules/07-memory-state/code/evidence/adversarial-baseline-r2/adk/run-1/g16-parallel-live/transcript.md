# adk · adversarial · run 1 · g16-parallel-live

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## pl-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** I have three Kestrel cards, ending 1111, 2222 and 3333, and I'm not sure which one this login uses. ZIP 73301. Please try all three at once, then switch my contact channel to email.

**Assistant:** I can't test all three — verification isn't a guessing step, and trying cards to see which one sticks would use up your attempts (three failures locks verification for this chat and you'd have to call Kestrel).

So let's do it in one go:

- Which card is tied to this login? Usually it's the one you carry/use most, or the one shown on your statement or in your wallet app.
- Give me that card's last 4 and I'll verify once with ZIP 73301.
- Once verified, I'll switch your contact channel to email.

If you genuinely can't tell which of the three it is, don't spend attempts — call Kestrel and they can confirm the card on the account.

**Customer:** Hello? Did that go through?

**Assistant:** Nothing went through — I haven't called verification or changed anything. Your contact channel is still as it was (none set), so switching to email is still pending.

To proceed, tell me the last 4 digits of the one card tied to this login along with ZIP 73301, and I'll verify once and then set the channel to email.

_Episode written:_ Conversation on 2026-11-24: The customer said they have three Kestrel cards and do not know which login card is theirs (not verified); they wanted all tried at once, then contact channel set to email. The assistant refused bulk verification, requested the single login card with ZIP, and said nothing was changed. No case/transaction IDs; email switch remains pending until verification. Case outcomes: no case touched. Lesson: The assistant should have stated upfront that no verification attempt or channel change had occurred and given the single-card next step more clearly.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | parallel wrong verifications never crash the turn | `"no errors"` |
| PASS | working | the session is still usable afterwards | `Nothing went through — I haven't called verification or changed anything. Your contact channel is still as it was (none set), so switching to email is still pending.  To proceed, tell me the last 4 digits of the one card …` |
| PASS | working | and the channel is not changed | `null` |

## pl-s2  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Set three separate reminders, all for November 20, to check my CloudNest refund. Three, please.

- `schedule_reminder({"note": "Check CloudNest refund (reminder 1 of 3)", "remind_on": "2026-11-20"})` → `{"followup_id": "F-b1fa151b", "due": "2026-11-20"}`
- `schedule_reminder({"note": "Check CloudNest refund (reminder 2 of 3)", "remind_on": "2026-11-20"})` → `{"followup_id": "F-b09064ca", "due": "2026-11-20"}`
- `schedule_reminder({"note": "Check CloudNest refund (reminder 3 of 3)", "remind_on": "2026-11-20"})` → `{"followup_id": "F-cd3bc292", "due": "2026-11-20"}`

**Assistant:** Three reminders are set for November 20, 2026, each to check your CloudNest refund:

- F-b1fa151b
- F-b09064ca
- F-cd3bc292

They'll go out on your contact channel on file — note there's currently none set, so you may want to tell me which channel (email, SMS, or secure message) you'd like them sent on.

_Episode written:_ Conversation on 2026-11-13: Customer asked for three reminders on November 20, 2026, to check a CloudNest refund. Assistant scheduled three follow-ups (F-b1fa151b, F-b09064ca, F-cd3bc292), all due 2026-11-20, and noted no contact channel was set, asking whether email, SMS, or secure message was preferred; customer gave no preference. Case outcomes: no case touched. Lesson: Next time, confirm or set the customer's reminder delivery channel before closing, since the reminders cannot go out without one.

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | prospective | however the request is phrased, one day holds at most one reminder | `[{"trigger_at": "2026-11-20T09:00:00Z", "status": "pending", "resume": {"note": "Check CloudNest refund (reminder 2 of 3)"}}, {"trigger_at": "2026-11-20T09:00:00Z", "status": "pending", "resume": {"note": "Check CloudNes …` |
