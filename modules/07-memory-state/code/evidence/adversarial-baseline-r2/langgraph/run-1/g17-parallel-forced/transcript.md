# langgraph · adversarial · run 1 · g17-parallel-forced

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## pp-notify  ·  parallel_probe  ·  priya  ·  2026-11-19T10:00:00Z

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | prospective | three parallel notify_customer calls for one follow-up record exactly one message | `{"error": null, "messages_for_followup": 3}` |

## pp-verify  ·  parallel_probe  ·  eli  ·  2026-11-24T10:00:00Z

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | three parallel wrong verifications do not crash | `{"error": "InvalidUpdateError: At key 'identity_failed_attempts': Can receive only one value per step. Use an Annotated key to handle multiple values.\nFor troubleshooting, visit: https://docs.langchain.com/oss/python/la …` |
| **FAIL** | working | and all three are counted | `{"error": "InvalidUpdateError: At key 'identity_failed_attempts': Can receive only one value per step. Use an Annotated key to handle multiple values.\nFor troubleshooting, visit: https://docs.langchain.com/oss/python/la …` |
