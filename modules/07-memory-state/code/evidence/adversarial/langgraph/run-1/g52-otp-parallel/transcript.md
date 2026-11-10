# langgraph · adversarial · run 1 · g52-otp-parallel

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## op-sends  ·  forced_calls  ·  eli  ·  2026-11-24T10:00:00Z

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | three parallel sends open one challenge | `{"error": null, "attempts_in_batch": 0, "failed_attempts": 0, "lock_respected": true, "verified": false, "cases_total": 0, "distinct_case_ids": 0, "case_followups": 0, "evidence": "", "otp_messages": 1, "open_challenges" …` |
| PASS | prospective | and send one message | `{"error": null, "attempts_in_batch": 0, "failed_attempts": 0, "lock_respected": true, "verified": false, "cases_total": 0, "distinct_case_ids": 0, "case_followups": 0, "evidence": "", "otp_messages": 1, "open_challenges" …` |
| PASS | working | without an exception | `{"error": null, "attempts_in_batch": 0, "failed_attempts": 0, "lock_respected": true, "verified": false, "cases_total": 0, "distinct_case_ids": 0, "case_followups": 0, "evidence": "", "otp_messages": 1, "open_challenges" …` |
