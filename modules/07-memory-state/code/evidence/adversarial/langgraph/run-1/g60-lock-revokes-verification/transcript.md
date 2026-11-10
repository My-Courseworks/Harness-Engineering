# langgraph · adversarial · run 1 · g60-lock-revokes-verification

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## lv-right-first  ·  forced_calls  ·  eli  ·  2026-11-24T10:00:00Z

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the right guess first: it is evaluated, then one more, then the lock holds | `{"error": null, "attempts_in_batch": 1, "failed_attempts": 3, "tool_results": ["verify_identity -> {\"verified\": false, \"error\": \"verification is locked on this account for 24 hours after 3 failed attempts; the custo …` |
| PASS | working | parallel guesses do not crash | `{"error": null, "attempts_in_batch": 1, "failed_attempts": 3, "tool_results": ["verify_identity -> {\"verified\": false, \"error\": \"verification is locked on this account for 24 hours after 3 failed attempts; the custo …` |

## lv-after  ·  session  ·  eli  ·  2026-11-24T10:01:00Z

_Resumes session `forced-lv-right-first`._

**Customer:** Great, now dispute the November 1 CloudNest charge, T-4002. I cancelled in October.

**Assistant:** I can't file that dispute, I'm afraid. Trying six different last-four guesses at once burned through the attempt limit - verification is now **locked on your account for 24 hours**, and filing a dispute requires a fresh identity check (card last 4 + billing ZIP) within 15 minutes of filing. There's no way for me to file it until that lock clears.

Please call Kestrel to sort out verification and, if you'd like, to file the CloudNest dispute on the November 1 charge in the meantime.

One thing to flag for later: guessing is risky because the bank counts every attempt, and the lock applies across all conversations, not just this one.

_Episode written:_ Conversation on 2026-11-24: The customer asked to try multiple card last-four guesses, then wanted to dispute the November 1 CloudNest charge (transaction T-4002), saying they cancelled in October (not verified). Multiple verification attempts locked the account for 24 hours; no dispute was filed and no case ID was created. The assistant advised calling Kestrel. Case outcomes: no case touched. Lesson: Next time, warn that each identity-verification guess counts toward a lock and avoid submitting multiple guesses in one batch.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the account is locked, so the verification the batch produced counts for nothing: no dispute is filed | `[]` |
| PASS | working | the customer is told the account is locked | `I can't file that dispute, I'm afraid. Trying six different last-four guesses at once burned through the attempt limit - verification is now **locked on your account for 24 hours**, and filing a dispute requires a fresh  …` |
