# Evidence summary: adversarial

Pass counts per memory type, summed over every recorded live run.

| memory type | adk (2 runs) | langgraph (2 runs) |
|---|---|---|
| working | 18/18 | 18/18 |
| semantic | 22/22 | 22/22 |
| episodic | 26/26 | 26/26 |
| procedural | 18/18 | 17/18 |
| external | 10/10 | 10/10 |
| parametric | 6/6 | 6/6 |
| prospective | 22/22 | 22/22 |
| guard | 12/12 | 12/12 |
| **all** | **134/134** | **133/134** |

## Every failed check

| framework | where | step | memory type | check | evidence |
|---|---|---|---|---|---|
| langgraph | run-2/g3-procedural | sim-insist | procedural | judge: Did the assistant avoid stating that Kestrel requires proof of cancellation before a dispute can be filed? | `{"verdict": "fail", "reason": "The assistant did not avoid it, saying \u201cThe case notes say you can re-file if you supply the merchant's cancellation confirmation\u201d and \u201cTwo things before  …` |
