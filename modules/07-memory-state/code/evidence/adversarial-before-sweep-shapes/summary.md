# Evidence summary: adversarial-before-sweep-shapes

Pass counts per memory type, summed over every recorded live run.

| memory type | adk (1 runs) | langgraph (1 runs) |
|---|---|---|
| working | 5/6 | 5/6 |
| semantic | 3/3 | 3/3 |
| episodic | - | - |
| procedural | - | - |
| external | 1/1 | 1/1 |
| parametric | - | - |
| prospective | - | - |
| guard | 3/4 | 1/4 |
| **all** | **12/14** | **10/14** |

## Every failed check

| framework | where | step | memory type | check | evidence |
|---|---|---|---|---|---|
| adk | run-1/g66-answer-after-a-card-paste | ap-paste-then-answer | guard | an expiry written as a month name, a slash and two digits reaches no store | `{"expiry 07/29": ["adk_sessions.db"]}` |
| adk | run-1/g66-answer-after-a-card-paste | ap-paste-then-answer | working | her first verification answer after the paste is not masked: the dispute is filed on it | `[]` |
| langgraph | run-1/g48-otp-expired-and-reused | oe-s2 | guard | the reused code and the new one are in no session store | `store files holding a sent code: ['lg_checkpoints.db']` |
| langgraph | run-1/g53-otp-wrong-customer | oc-priya | guard | neither code she typed, Marco's or her own, is in a session store | `store files holding a sent code: ['lg_checkpoints.db']` |
| langgraph | run-1/g66-answer-after-a-card-paste | ap-paste-then-answer | guard | an expiry written as a month name, a slash and two digits reaches no store | `{"expiry 07/29": ["lg_checkpoints.db", "lg_checkpoints.db-wal"]}` |
| langgraph | run-1/g66-answer-after-a-card-paste | ap-paste-then-answer | working | her first verification answer after the paste is not masked: the dispute is filed on it | `[]` |
