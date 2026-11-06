# langgraph · adversarial · run 1 · g9-eof

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## eof-s1  ·  cli_eof_session  ·  eli  ·  2026-11-24T10:00:00Z

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (LangGraph) | customer=eli session=eof-s1 | 'exit' or end-of-input ends the session

[you]:   [tool] search_policy({"question": "What contact channels can Kestrel use to reach a customer?"})

[assistant]: Kestrel can reach you by **email**, **SMS (text message)**, or **secure_message** (the Kestrel app inbox).

You currently have no channel on file, so anything we send — case follow-ups, reminders — would go to **secure_message** by default. If you'd like to switch to email or SMS, I can do that; it requires quick identity verification (card's last 4 digits and billing ZIP).

[you]: 
[memory] episode E-eof-s1-1: Conversation on 2026-11-24: Customer asked which contact channels Kestrel can use. Assistant said email, SMS, or secure_message; with no channel on file, secure_message is default. Assistant offered to switch after identity verification; no case or transaction ID, promise, or preference stated. Case outcomes: no case touched. Lesson: none
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | a chat that ends without 'exit' (EOF) still writes its episode | `1 episodes; purged 0` |

## eof-idle-close  ·  maintenance  ·  2026-11-24T12:00:00Z

_maintenance:_ `{"closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | the idle-session sweep does not write the episode twice | `1 episodes; purged 0` |
