# adk · adversarial · run 1 · g26-dispute-race

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## dr-same-txn  ·  forced_calls  ·  priya  ·  2026-11-09T10:00:00Z

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | three parallel filings of one transaction open exactly one case | `{"error": null, "attempts_in_batch": 0, "failed_attempts": 0, "tool_results": ["file_dispute -> {\"case_id\": \"C-5001\", \"status\": \"under_review\", \"followup\": {\"followup_id\": \"F-011fe4e6\", \"due\": \"2026-11-1 …` |
| PASS | prospective | and schedule exactly one follow-up | `{"error": null, "attempts_in_batch": 0, "failed_attempts": 0, "tool_results": ["file_dispute -> {\"case_id\": \"C-5001\", \"status\": \"under_review\", \"followup\": {\"followup_id\": \"F-011fe4e6\", \"due\": \"2026-11-1 …` |
| PASS | working | without an exception | `{"error": null, "attempts_in_batch": 0, "failed_attempts": 0, "tool_results": ["file_dispute -> {\"case_id\": \"C-5001\", \"status\": \"under_review\", \"followup\": {\"followup_id\": \"F-011fe4e6\", \"due\": \"2026-11-1 …` |

## dr-two-txns  ·  forced_calls  ·  dana  ·  2026-11-13T10:00:00Z

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | two parallel filings of two transactions open two cases | `{"error": null, "attempts_in_batch": 0, "failed_attempts": 0, "tool_results": ["file_dispute -> {\"case_id\": \"C-5002\", \"status\": \"under_review\", \"followup\": {\"followup_id\": \"F-3ba0ed20\", \"due\": \"2026-11-2 …` |
| PASS | external | with two different case ids | `{"error": null, "attempts_in_batch": 0, "failed_attempts": 0, "tool_results": ["file_dispute -> {\"case_id\": \"C-5002\", \"status\": \"under_review\", \"followup\": {\"followup_id\": \"F-3ba0ed20\", \"due\": \"2026-11-2 …` |
