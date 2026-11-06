# adk · adversarial · run 2 · g9-eof

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## eof-s1  ·  cli_eof_session  ·  eli  ·  2026-11-24T10:00:00Z

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (ADK) | customer=eli session=eof-s1 | 'exit' or end-of-input ends the session

[you]:   [tool] search_policy({"question": "What contact channels can Kestrel use to reach customers?"})

[assistant]: You can be reached by **email**, **SMS (text)**, or **secure_message** (the inbox in the Kestrel app).

Right now you have no channel chosen, so anything Kestrel sends you — case updates and reminders — goes to **secure_message** by default. If you'd like to switch to email or SMS, I can do that, but changing the channel requires identity verification (card's last 4 digits and billing ZIP).

[you]: 
[memory] episode E-eof-s1-1: Conversation on 2026-11-24: Customer asked what contact channels Kestrel can use. Assistant searched policy and explained email, SMS, or secure_message; with no channel chosen, messages default to secure_message. Assistant said switching channels requires identity verification. No case or transaction IDs; no customer preference stated. Case outcomes: no case touched. Lesson: none
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | a chat that ends without 'exit' (EOF) still writes its episode | `1 episodes; purged 0` |

## eof-idle-close  ·  maintenance  ·  2026-11-24T12:00:00Z

_maintenance:_ `{"closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | the idle-session sweep does not write the episode twice | `1 episodes; purged 0` |
