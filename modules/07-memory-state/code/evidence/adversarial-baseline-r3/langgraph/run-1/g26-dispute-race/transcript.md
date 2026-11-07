# langgraph · adversarial · run 1 · g26-dispute-race

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## dr-same-txn  ·  forced_calls  ·  priya  ·  2026-11-09T10:00:00Z

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | external | three parallel filings of one transaction open exactly one case | `{"error": "IntegrityError: UNIQUE constraint failed: cases.case_id", "attempts_in_batch": 0, "failed_attempts": 0, "lock_respected": true, "verified": false, "cases_total": 2, "distinct_case_ids": 2, "case_followups": 2, …` |
| **FAIL** | prospective | and schedule exactly one follow-up | `{"error": "IntegrityError: UNIQUE constraint failed: cases.case_id", "attempts_in_batch": 0, "failed_attempts": 0, "lock_respected": true, "verified": false, "cases_total": 2, "distinct_case_ids": 2, "case_followups": 2, …` |
| **FAIL** | working | without an exception | `{"error": "IntegrityError: UNIQUE constraint failed: cases.case_id", "attempts_in_batch": 0, "failed_attempts": 0, "lock_respected": true, "verified": false, "cases_total": 2, "distinct_case_ids": 2, "case_followups": 2, …` |

## dr-two-txns  ·  forced_calls  ·  dana  ·  2026-11-13T10:00:00Z

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | external | two parallel filings of two transactions open two cases | `{"error": "IntegrityError: UNIQUE constraint failed: cases.case_id", "attempts_in_batch": 0, "failed_attempts": 0, "lock_respected": true, "verified": false, "cases_total": 1, "distinct_case_ids": 1, "case_followups": 1, …` |
| **FAIL** | external | with two different case ids | `{"error": "IntegrityError: UNIQUE constraint failed: cases.case_id", "attempts_in_batch": 0, "failed_attempts": 0, "lock_respected": true, "verified": false, "cases_total": 1, "distinct_case_ids": 1, "case_followups": 1, …` |
