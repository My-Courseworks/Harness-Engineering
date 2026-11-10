# Evidence summary: adversarial-before-blind-findings

Pass counts per memory type, summed over every recorded live run.

| memory type | adk (1 runs) | langgraph (1 runs) |
|---|---|---|
| working | 1/4 | 1/4 |
| semantic | - | - |
| episodic | - | - |
| procedural | - | - |
| external | - | - |
| parametric | - | - |
| prospective | - | - |
| guard | 1/4 | 1/4 |
| **all** | **2/8** | **2/8** |

## Every failed check

| framework | where | step | memory type | check | evidence |
|---|---|---|---|---|---|
| adk | run-1/g81-what-the-blind-run-found | bf-seam | guard | a code at the seam of a number sent in two goes, after an earlier card paste, reaches no store | `{"security code 047": ["adk_sessions.db"]}` |
| adk | run-1/g81-what-the-blind-run-found | bf-seam | guard | the message that completes the number holds a marker, not the code | `CVC 047 1111` |
| adk | run-1/g81-what-the-blind-run-found | bf-month-expiry | guard | a month name and two digits directly before the number are its expiry: nothing of the note reaches a store | `{"expiry 09/27": ["adk_sessions.db"]}` |
| adk | run-1/g81-what-the-blind-run-found | bf-unit-word | working | and the words after it are stored as typed | `I stopped using [REDACTED CARD NUMBER]. Which card do you have on my account?` |
| adk | run-1/g81-what-the-blind-run-found | bf-list | working | a numbered list whose items hold other numbers is stored whole: line 5 | `Unrelated to my card. This is my packing checklist, exactly as I wrote it: 1. Charge 2 power banks 2. Keep 75 euros in cash 3. Verify your phone number [REDACTED CARD NUMBER]. Save the 7-hour helpline …` |
| adk | run-1/g81-what-the-blind-run-found | bf-list | working | and line 13 | `Unrelated to my card. This is my packing checklist, exactly as I wrote it: 1. Charge 2 power banks 2. Keep 75 euros in cash 3. Verify your phone number [REDACTED CARD NUMBER]. Save the 7-hour helpline …` |
| langgraph | run-1/g81-what-the-blind-run-found | bf-seam | guard | a code at the seam of a number sent in two goes, after an earlier card paste, reaches no store | `{"security code 047": ["lg_checkpoints.db", "lg_checkpoints.db-wal"]}` |
| langgraph | run-1/g81-what-the-blind-run-found | bf-seam | guard | the message that completes the number holds a marker, not the code | `CVC 047 1111` |
| langgraph | run-1/g81-what-the-blind-run-found | bf-month-expiry | guard | a month name and two digits directly before the number are its expiry: nothing of the note reaches a store | `{"expiry 09/27": ["lg_checkpoints.db", "lg_checkpoints.db-wal"]}` |
| langgraph | run-1/g81-what-the-blind-run-found | bf-unit-word | working | and the words after it are stored as typed | `I stopped using [REDACTED CARD NUMBER]. Which card do you have on my account?` |
| langgraph | run-1/g81-what-the-blind-run-found | bf-list | working | a numbered list whose items hold other numbers is stored whole: line 5 | `Unrelated to my card. This is my packing checklist, exactly as I wrote it: 1. Charge 2 power banks 2. Keep 75 euros in cash 3. Verify your phone number [REDACTED CARD NUMBER]. Save the 7-hour helpline …` |
| langgraph | run-1/g81-what-the-blind-run-found | bf-list | working | and line 13 | `Unrelated to my card. This is my packing checklist, exactly as I wrote it: 1. Charge 2 power banks 2. Keep 75 euros in cash 3. Verify your phone number [REDACTED CARD NUMBER]. Save the 7-hour helpline …` |
