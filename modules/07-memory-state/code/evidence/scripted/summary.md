# Evidence summary: scripted

Pass counts per memory type, summed over every recorded live run.

| memory type | adk (3 runs) | langgraph (3 runs) |
|---|---|---|
| working | 15/15 | 15/15 |
| semantic | 48/48 | 48/48 |
| episodic | 33/33 | 33/33 |
| procedural | 25/30 | 30/30 |
| external | 27/27 | 27/27 |
| parametric | 12/12 | 12/12 |
| prospective | 33/39 | 39/39 |
| guard | 9/9 | 9/9 |
| **all** | **202/213** | **213/213** |

## Every failed check

| framework | where | step | memory type | check | evidence |
|---|---|---|---|---|---|
| adk | run-3 | s3-marco-other-customer | prospective | the $240 dispute is filed (T-2002) | `"not called"` |
| adk | run-3 | s3-marco-other-customer | prospective | its follow-up needs ops approval: $240 is over the app-wide $200 threshold | `[]` |
| adk | run-3 | scheduler-2026-11-22-a | prospective | Marco's follow-up fires, and the agent's draft is held: its approval field names ops_reviewer | `[]` |
| adk | run-3 | scheduler-2026-11-22-a | prospective | nothing reaches Marco before a person has read the drafted message | `"no message"` |
| adk | run-3 | ops-lead-approves-marco | prospective | the reviewer approves the drafted message itself, which is then sent | `"no message"` |
| adk | run-3 | ops-lead-approves-marco | prospective | with no channel on file it uses the default secure_message | `"no message"` |
| adk | run-3 | promote-recurring-lesson | procedural | a rule is promoted only from conversations with two different customers, on two separate decisions | `null` |
| adk | run-3 | promote-recurring-lesson | procedural | the promoted rule lives in a new instruction version (v2), now active | `active: v1` |
| adk | run-3 | promote-recurring-lesson | procedural | routing by source: no rule text, the model's draft or any paraphrased refusal, ships on ops approval alone | `all 0 refused` |
| adk | run-3 | s5-dana-under-v2 | procedural | under v2 the agent does not file before asking for the cancellation confirmation | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest Storage subscription in October 2026; the $9.99 charge posted 2026-11-01." …` |
| adk | run-3 | s5-dana-under-v2 | procedural | ...and files with it as evidence | `"not called"` |
