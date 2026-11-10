# langgraph · adversarial · run 1 · g25-lockout-race

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## lr-two-prior  ·  forced_calls  ·  eli  ·  2026-11-24T10:00:00Z

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | with two failures on the account, at most one more guess is evaluated | `{"error": null, "attempts_in_batch": 1, "failed_attempts": 3, "tool_results": ["verify_identity -> {\"verified\": false, \"error\": \"verification is locked on this account for 24 hours after 3 failed attempts; the custo …` |
| PASS | working | no guess is evaluated once the account holds three failures | `{"error": null, "attempts_in_batch": 1, "failed_attempts": 3, "tool_results": ["verify_identity -> {\"verified\": false, \"error\": \"verification is locked on this account for 24 hours after 3 failed attempts; the custo …` |
| PASS | working | parallel guesses do not crash | `{"error": null, "attempts_in_batch": 1, "failed_attempts": 3, "tool_results": ["verify_identity -> {\"verified\": false, \"error\": \"verification is locked on this account for 24 hours after 3 failed attempts; the custo …` |

## lr-none-prior  ·  forced_calls  ·  eli  ·  2026-11-25T11:00:00Z

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | six parallel wrong guesses: exactly three are evaluated | `{"error": null, "attempts_in_batch": 3, "failed_attempts": 3, "tool_results": ["verify_identity -> {\"verified\": false, \"error\": \"those details do not match this customer\", \"attempts_left\": 2}", "verify_identity - …` |
| PASS | working | and the account is locked | `{"error": null, "attempts_in_batch": 3, "failed_attempts": 3, "tool_results": ["verify_identity -> {\"verified\": false, \"error\": \"those details do not match this customer\", \"attempts_left\": 2}", "verify_identity - …` |
