# langgraph · adversarial · run 1 · g52-otp-parallel

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## op-sends  ·  forced_calls  ·  eli  ·  2026-11-24T10:00:00Z

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | three parallel sends open one challenge | `{"error": null, "attempts_in_batch": 0, "failed_attempts": 0, "tool_results": ["send_verification_code -> {\"error\": \"a code was sent 0 seconds ago and is still valid; ask the customer to enter it (a new one can be sen …` |
| PASS | prospective | and send one message | `{"error": null, "attempts_in_batch": 0, "failed_attempts": 0, "tool_results": ["send_verification_code -> {\"error\": \"a code was sent 0 seconds ago and is still valid; ask the customer to enter it (a new one can be sen …` |
| PASS | working | without an exception | `{"error": null, "attempts_in_batch": 0, "failed_attempts": 0, "tool_results": ["send_verification_code -> {\"error\": \"a code was sent 0 seconds ago and is still valid; ask the customer to enter it (a new one can be sen …` |
