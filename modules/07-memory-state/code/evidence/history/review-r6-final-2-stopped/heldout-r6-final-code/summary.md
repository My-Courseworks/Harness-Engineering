# Evidence summary: heldout-r6-final-code

Pass counts per memory type, summed over every recorded live run.

| memory type | adk (1 runs) | langgraph (1 runs) |
|---|---|---|
| working | 40/40 | 23/24 |
| semantic | 15/15 | 7/8 |
| episodic | 6/6 | - |
| procedural | - | - |
| external | 20/20 | 15/16 |
| parametric | - | - |
| prospective | 9/9 | - |
| guard | 40/41 | 18/18 |
| **all** | **130/131** | **63/66** |

## Every failed check

| framework | where | step | memory type | check | evidence |
|---|---|---|---|---|---|
| adk | run-1/r6-card-number-behind-a-date-or-a-word | r6i-paste | guard | r6 C4: the end of a number sent after a code at the seam is masked | `CVC [REDACTED SECURITY CODE] [REDACTED SECURITY CODE]` |
| langgraph | run-1/r6-what-counts-as-an-entry | r6b-new-code | external | r6 A: three codes in all, the third on request | `2 one-time-code messages in the outbox` |
| langgraph | run-1/r6-what-counts-as-an-entry | r6b-new-code | working | r6 A3: the earlier code, typed once a newer one is out, is one wrong entry | `0 attempt rows with succeeded=0` |
| langgraph | run-1/r6-what-counts-as-an-entry | r6b-new-code | semantic | r6 A1: the newest code typed as three pairs removes the channel | `{"value": "email", "as_of": "2026-11-18T14:04:10Z", "expires_at": null}` |
