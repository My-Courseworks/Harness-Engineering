# langgraph · adversarial · run 1 · g16-parallel-live

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## pl-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** I have three Kestrel cards, ending 1111, 2222 and 3333, and I'm not sure which one this login uses. ZIP 73301. Please try all three at once, then switch my contact channel to email.

**Assistant:** I can't run all three — that's effectively guessing, and a wrong try still counts: three failed attempts lock verification for this conversation and you'd have to call Kestrel.

So let's do one attempt. Which of the three is the card you used to open or sign in to this account — or the one you have in hand right now? Give me that card's last 4 and I'll verify, then switch your contact channel to email in the same step.

**Customer:** Hello? Did that go through?

**Assistant:** No — nothing went through. I haven't attempted any verification, so none of your three attempts are used up.

To move forward I need the last 4 digits of the one card tied to this login (not all three). Once verified, I'll set your contact channel to email right away.

_Episode written:_ Conversation on 2026-11-24: Customer said they have three Kestrel cards and are unsure which card the login uses (not verified); they asked to try all three and switch contact channel to email. The assistant refused due lock risk, made no verification attempt, asked for the one card tied to the login, and promised email-channel switching right away once verified. No case/transaction IDs. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | parallel wrong verifications never crash the turn | `"no errors"` |
| PASS | working | the session is still usable afterwards | `No — nothing went through. I haven't attempted any verification, so none of your three attempts are used up.  To move forward I need the last 4 digits of the one card tied to this login (not all three). Once verified, I' …` |
| PASS | working | and the channel is not changed | `null` |

## pl-s2  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Set three separate reminders, all for November 20, to check my CloudNest refund. Three, please.

- `schedule_reminder({"note": "Check CloudNest refund", "remind_on": "2026-11-20"})` → `{"followup_id": "F-d92f74e6", "due": "2026-11-20"}`
- `schedule_reminder({"note": "Check CloudNest refund", "remind_on": "2026-11-20"})` → `{"followup_id": "F-35cdca47", "due": "2026-11-20"}`
- `schedule_reminder({"note": "Check CloudNest refund", "remind_on": "2026-11-20"})` → `{"followup_id": "F-cbb138eb", "due": "2026-11-20"}`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-35cdca47", "action": "customer_reminder", "due": "2026-11-20T09:00:00Z", "status": "pending", "sent_on": "the contact channel on file when it is sent (currently secure_message)", "note": "Check CloudNest refund"}, {"followup_id": "F-cbb138eb", "action": "customer_reminder", "due": "2026-11-20T09:00:00Z", "status": "pending", "sent_on": "the contact channel on file …`

**Assistant:** Three reminders set — all for November 20, all reading "Check CloudNest refund":

- F-d92f74e6
- F-35cdca47
- F-cbb138eb

They'll arrive the morning of the 20th on your current contact channel (secure message). Note that they'll go out together, so you'll get the same note three times — say the word if you'd rather keep just one and cancel the other two.

_Episode written:_ Conversation on 2026-11-13: Customer asked for three separate reminders on November 20 to check a CloudNest refund; the customer said they have a CloudNest refund to check (not verified). Three reminders were scheduled for 2026-11-20 on secure_message: F-d92f74e6, F-35cdca47, F-cbb138eb. Assistant promised morning delivery and offered to cancel two. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | prospective | however the request is phrased, one day holds at most one reminder | `[{"trigger_at": "2026-11-20T09:00:00Z", "status": "pending", "resume": {"note": "Check CloudNest refund"}}, {"trigger_at": "2026-11-20T09:00:00Z", "status": "pending", "resume": {"note": "Check CloudNest refund"}}, {"tri …` |
