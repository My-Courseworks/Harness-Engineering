# Evidence summary: adversarial

Pass counts per memory type, summed over every recorded live run.

| memory type | adk (2 runs) | langgraph (2 runs) |
|---|---|---|
| working | 192/192 | 192/192 |
| semantic | 90/90 | 90/90 |
| episodic | 58/58 | 58/58 |
| procedural | 24/24 | 24/24 |
| external | 75/78 | 78/78 |
| parametric | 6/6 | 6/6 |
| prospective | 113/114 | 114/114 |
| guard | 98/98 | 98/98 |
| **all** | **656/660** | **660/660** |

## Every failed check

| framework | where | step | memory type | check | evidence |
|---|---|---|---|---|---|
| adk | run-2/g61-lost-tool-result | lr-dispute | external | the process was killed after the case was opened | `exit code 0; stderr: ` |
| adk | run-2/g61-lost-tool-result | lr-dispute-resume | external | one case, not two | `[]` |
| adk | run-2/g61-lost-tool-result | lr-dispute-resume | prospective | the follow-up the crash skipped is scheduled by the repeated filing (a $240 dispute: reviewed) | `[]` |
| adk | run-2/g61-lost-tool-result | lr-dispute-resume | external | the customer is given the case id | `ed no cases, so the assistant said no dispute was filed and no case number exists. The assistant asked them to choose T-2002 (2026 renewal, 3 Nov 2026) or T-2001 (2025 charge, 3 Nov 2025), promising t …` |
