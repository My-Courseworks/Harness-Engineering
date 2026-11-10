# Evidence summary: adversarial

Pass counts per memory type, summed over every recorded live run.

| memory type | adk (1 runs) | langgraph (1 runs) |
|---|---|---|
| working | 134/134 | 134/134 |
| semantic | 58/58 | 58/58 |
| episodic | 30/30 | 29/30 |
| procedural | 12/12 | 12/12 |
| external | 45/45 | 45/45 |
| parametric | 3/3 | 3/3 |
| prospective | 58/58 | 58/58 |
| guard | 81/81 | 81/81 |
| **all** | **421/421** | **420/421** |

## Every failed check

| framework | where | step | memory type | check | evidence |
|---|---|---|---|---|---|
| langgraph | run-1/g8-overflow | long-s1 | episodic | ...and answered correctly | `I have no record of a dog's name - nothing about that in your past conversations or your profile.  For March: one earlier conversation mentions a trip to **Oslo**, but that was never confirmed and the …` |
