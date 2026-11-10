# Evidence summary: adversarial

Pass counts per memory type, summed over every recorded live run.

| memory type | adk (2 runs) | langgraph (2 runs) |
|---|---|---|
| working | 194/194 | 194/194 |
| semantic | 90/90 | 89/90 |
| episodic | 58/58 | 58/58 |
| procedural | 24/24 | 24/24 |
| external | 78/78 | 77/78 |
| parametric | 6/6 | 4/6 |
| prospective | 114/114 | 114/114 |
| guard | 116/116 | 116/116 |
| **all** | **680/680** | **676/680** |

## Every failed check

| framework | where | step | memory type | check | evidence |
|---|---|---|---|---|---|
| langgraph | run-1/g1-priya-month | p1-followups-11-19 | parametric | no outbound message invites a reply or promises to 'add it to your case' | `["Case C-5001 (StreamMax charge, cancelled subscription) was rejected: the merchant says no cancellation request is on record. If you have proof of cancellation, you can message the card-care chat in  …` |
| langgraph | run-2/g1-priya-month | p1-followups-11-19 | parametric | no outbound message invites a reply or promises to 'add it to your case' | `["Update on your dispute C-5001 (subscription charge): it was rejected because the merchant states no cancellation request is on record. If you have proof the subscription was cancelled before the cha …` |
| langgraph | run-2/g4-kb-gaps | p7 | external | the 75-day window and 5-day replacement come from retrieval | `not called` |
| langgraph | run-2/g54-otp-destination-is-not-memory | od-s1 | semantic | the channel is email | `{}` |
