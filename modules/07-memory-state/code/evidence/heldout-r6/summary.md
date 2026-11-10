# Evidence summary: heldout-r6

Pass counts per memory type, summed over every recorded live run.

| memory type | adk (1 runs) | langgraph (1 runs) |
|---|---|---|
| working | 38/40 | 40/40 |
| semantic | 15/15 | 15/15 |
| episodic | 6/6 | 6/6 |
| procedural | - | - |
| external | 20/20 | 20/20 |
| parametric | - | - |
| prospective | 8/9 | 9/9 |
| guard | 37/41 | 38/41 |
| **all** | **124/131** | **128/131** |

## Every failed check

| framework | where | step | memory type | check | evidence |
|---|---|---|---|---|---|
| adk | run-1/r6-candidate-list-in-a-second-chat | r6a-notes-more | working | r6 A4: ...and nothing typed there is a failed attempt | `1 attempt rows with succeeded=0` |
| adk | run-1/r6-candidate-list-in-a-second-chat | r6a-main-entry | working | r6 A4: the detour through the other chat cost no failed attempt | `1 attempt rows with succeeded=0` |
| adk | run-1/r6-card-number-behind-a-date-or-a-word | r6i-paste | guard | r6 C: none of the seven numbers, the code or the expiry reaches any store | `{"security code 047": ["adk_sessions.db"]}` |
| adk | run-1/r6-card-number-behind-a-date-or-a-word | r6i-paste | guard | r6 C4: the end of a number sent after a code at the seam is masked | `CVC 047 1111` |
| adk | run-1/r6-erase-open-chat-and-due-followups | r6h-tick-later | prospective | r6 B2: the case follow-up still reaches the erased customer, once | `2 messages` |
| adk | run-1/r6-smaller-commitments | r6j-list | guard | r6 C5: a numbered list of sixteen lines keeps its lines 5 and 12 | `Here's a 16-item checklist for travelling with your Kestrel card:  1. **Add a travel notice** - give Kestrel the destination and your return date; it cuts false declines and is deleted automatically a …` |
| adk | run-1/r6-smaller-commitments | r6j-list | guard | r6 C5: ...and none of it is replaced by a masking token | `Here's a 16-item checklist for travelling with your Kestrel card:  1. **Add a travel notice** - give Kestrel the destination and your return date; it cuts false declines and is deleted automatically a …` |
| langgraph | run-1/r6-card-number-behind-a-date-or-a-word | r6i-paste | guard | r6 C: none of the seven numbers, the code or the expiry reaches any store | `{"security code 047": ["lg_checkpoints.db", "lg_checkpoints.db-wal"]}` |
| langgraph | run-1/r6-card-number-behind-a-date-or-a-word | r6i-paste | guard | r6 C4: the end of a number sent after a code at the seam is masked | `CVC 047 1111` |
| langgraph | run-1/r6-card-number-behind-a-date-or-a-word | r6i-sim | guard | r6 unscripted C1: no card number, code or expiry of the pasted note reaches any store | `{"expiry 09/27": ["lg_checkpoints.db", "lg_checkpoints.db-wal"]}` |
