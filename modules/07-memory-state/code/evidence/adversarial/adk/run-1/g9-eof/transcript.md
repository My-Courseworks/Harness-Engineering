# adk · adversarial · run 1 · g9-eof

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## eof-s1  ·  cli_eof_session  ·  eli  ·  2026-11-24T10:00:00Z

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (ADK) | customer=eli session=eof-s1 | 'exit' or end-of-input ends the session

[you]:   [tool] search_policy({"question": "Which contact channels can Kestrel use to reach a customer (email, SMS, secure message)?"})

[assistant]: Kestrel can reach you by **email**, **SMS (text message)**, or **secure message** (the inbox in the Kestrel app).

You don't currently have a channel chosen, so anything sent to you would go by secure message. If you'd like to switch to email or SMS, tell me which one — changing it requires identity verification (card last 4 digits and billing ZIP).

[you]: 
[memory] episode E-eof-s1-1: Conversation on 2026-11-24: The customer asked which contact channels Kestrel can use. The assistant said email, SMS, or secure message, with secure message as the default if no channel is chosen. The assistant said changing the channel requires identity verification. No case or transaction ID, promise, or customer channel preference was stated. Case outcomes: no case touched. Lesson: none
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | a chat that ends without 'exit' (EOF) still writes its episode | `1 episodes; purged 0` |

## eof-idle-close  ·  maintenance  ·  2026-11-24T12:00:00Z

_maintenance:_ `{"closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | the idle-session sweep does not write the episode twice | `1 episodes; purged 0` |
