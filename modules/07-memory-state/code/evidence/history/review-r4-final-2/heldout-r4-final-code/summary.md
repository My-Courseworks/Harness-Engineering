# Evidence summary: heldout-r4-final-code

Pass counts per memory type, summed over every recorded live run.

| memory type | adk (1 runs) | langgraph (1 runs) |
|---|---|---|
| working | 16/16 | 16/16 |
| semantic | 15/15 | 14/15 |
| episodic | 12/12 | 12/12 |
| procedural | - | - |
| external | 7/7 | 7/7 |
| parametric | - | - |
| prospective | 20/20 | 20/20 |
| guard | 11/11 | 11/11 |
| **all** | **81/81** | **80/81** |

## Every failed check

| framework | where | step | memory type | check | evidence |
|---|---|---|---|---|---|
| langgraph | run-1/r4-card-shapes-and-overredaction | r4c-s1 | semantic | r4: ...so the channel change goes through | `{}` |
