# Evidence summary

Pass counts per memory type, summed over every recorded live run.

| memory type | adk (3 runs) | langgraph (3 runs) |
|---|---|---|
| working | 12/12 | 12/12 |
| semantic | 48/48 | 48/48 |
| episodic | 31/33 | 33/33 |
| procedural | 21/21 | 21/21 |
| external | 21/21 | 21/21 |
| parametric | 18/18 | 18/18 |
| prospective | 39/39 | 39/39 |
| guard | 6/6 | 6/6 |

## Every failed check

| framework | run | step | memory type | check | evidence |
|---|---|---|---|---|---|
| adk | run-1 | s3-marco-other-customer | episodic | no leakage: nothing about Priya's dispute reaches Marco | `a selected turn errored, so the absence cannot be shown: InternalServerError: litellm.InternalServerError: InternalServerError: DeepseekException - Response payload is not completed: <TransferEncoding …` |
| adk | run-1 | s3-marco-other-customer | episodic | if load_memory runs for Marco it returns none of Priya's episodes | `a selected turn errored, so the absence cannot be shown: InternalServerError: litellm.InternalServerError: InternalServerError: DeepseekException - Response payload is not completed: <TransferEncoding …` |
