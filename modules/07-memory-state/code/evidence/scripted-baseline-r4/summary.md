# Evidence summary: scripted-baseline-r4

Pass counts per memory type, summed over every recorded live run.

| memory type | adk (1 runs) | langgraph (1 runs) |
|---|---|---|
| working | 5/6 | 5/6 |
| semantic | 16/16 | 16/16 |
| episodic | 11/11 | 11/11 |
| procedural | 10/10 | 10/10 |
| external | 8/9 | 9/9 |
| parametric | 3/4 | 4/4 |
| prospective | 13/13 | 13/13 |
| guard | 3/3 | 3/3 |
| **all** | **69/72** | **71/72** |

## Every failed check

| framework | where | step | memory type | check | evidence |
|---|---|---|---|---|---|
| adk | run-1/scenario | s2-priya-returns | working | a channel change needs the one-time code as well: it is sent and confirmed | `"not called"` |
| adk | run-1/scenario | s7-parametric-prevented | external | the agent looks the figure up instead of answering from its weights | `"not called"` |
| adk | run-1/scenario | s7-parametric-prevented | parametric | prevented: the KB has no late fee, so the agent states no dollar figure | `a selected turn errored, so the absence cannot be shown: ServiceUnavailableError: litellm.ServiceUnavailableError: ServiceUnavailableError: DeepseekException - {"error":{"message":"Service is too busy …` |
| langgraph | run-1/scenario | s2-priya-returns | working | a channel change needs the one-time code as well: it is sent and confirmed | `"not called"` |
