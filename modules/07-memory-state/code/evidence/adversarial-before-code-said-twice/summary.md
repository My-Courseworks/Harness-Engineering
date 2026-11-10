# Evidence summary: adversarial-before-code-said-twice

Pass counts per memory type, summed over every recorded live run.

| memory type | adk (1 runs) | langgraph (1 runs) |
|---|---|---|
| working | - | - |
| semantic | - | - |
| episodic | - | - |
| procedural | - | - |
| external | - | - |
| parametric | - | - |
| prospective | - | - |
| guard | 1/5 | 1/5 |
| **all** | **1/5** | **1/5** |

## Every failed check

| framework | where | step | memory type | check | evidence |
|---|---|---|---|---|---|
| adk | run-1/g65-code-said-twice | st-notes-paste | guard | the final pass's own line: a code in words and again in brackets reaches no store | `{"security code 386": ["adk_sessions.db"]}` |
| adk | run-1/g65-code-said-twice | st-typed-twice | guard | no card number nearby: the code between dashes and again in digits, then typed twice, reaches no store | `{"security code 914": ["adk_sessions.db"]}` |
| adk | run-1/g65-code-said-twice | st-expiry-with-a-space | guard | an expiry typed with a space after its cue reaches no store (found while checking the fix) | `{"expiry 08/27": ["adk_sessions.db"]}` |
| adk | run-1/g65-code-said-twice | st-digits-then-words | guard | digits first, then the same code in words in brackets, before a card number: nothing reaches a store | `{"security code 737": ["adk_sessions.db"]}` |
| langgraph | run-1/g65-code-said-twice | st-notes-paste | guard | the final pass's own line: a code in words and again in brackets reaches no store | `{"security code 386": ["lg_checkpoints.db-wal"]}` |
| langgraph | run-1/g65-code-said-twice | st-typed-twice | guard | no card number nearby: the code between dashes and again in digits, then typed twice, reaches no store | `{"security code 914": ["lg_checkpoints.db-wal"]}` |
| langgraph | run-1/g65-code-said-twice | st-expiry-with-a-space | guard | an expiry typed with a space after its cue reaches no store (found while checking the fix) | `{"expiry 08/27": ["lg_checkpoints.db-wal"]}` |
| langgraph | run-1/g65-code-said-twice | st-digits-then-words | guard | digits first, then the same code in words in brackets, before a card number: nothing reaches a store | `{"security code 737": ["lg_checkpoints.db-wal"]}` |
