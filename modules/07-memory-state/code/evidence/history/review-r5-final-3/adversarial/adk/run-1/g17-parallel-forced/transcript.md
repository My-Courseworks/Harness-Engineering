# adk · adversarial · run 1 · g17-parallel-forced

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## pp-notify  ·  parallel_probe  ·  priya  ·  2026-11-19T10:00:00Z

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | three parallel notify_customer calls for one follow-up record exactly one message | `{"error": null, "messages_for_followup": 1}` |

## pp-verify  ·  parallel_probe  ·  eli  ·  2026-11-24T10:00:00Z

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | three parallel wrong verifications do not crash | `{"error": null, "failed_attempts": 3}` |
| PASS | working | and all three are counted | `{"error": null, "failed_attempts": 3}` |
