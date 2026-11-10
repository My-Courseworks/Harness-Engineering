# Evidence summary: heldout-otp

Pass counts per memory type, summed over every recorded live run.

| memory type | adk (1 runs) | langgraph (1 runs) |
|---|---|---|
| working | 22/22 | 22/22 |
| semantic | 26/27 | 27/27 |
| episodic | 2/2 | 2/2 |
| procedural | - | - |
| external | 39/40 | 40/40 |
| parametric | - | - |
| prospective | 3/3 | 3/3 |
| guard | 14/14 | 14/14 |
| **all** | **106/108** | **108/108** |

## Every failed check

| framework | where | step | memory type | check | evidence |
|---|---|---|---|---|---|
| adk | run-1/otp-impatient-unscripted | ou-sim | semantic | otp unscripted: the change goes through once the code her phone shows is typed | `{}` |
| adk | run-1/otp-impatient-unscripted | ou-sim | external | otp unscripted: one challenge consumed | `challenges: [('open', '2026-11-13T10:00')]` |
