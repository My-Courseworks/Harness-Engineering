# langgraph · adversarial · run 2 · g9-eof

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## eof-s1  ·  cli_eof_session  ·  eli  ·  2026-11-24T10:00:00Z

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (LangGraph) | customer=eli session=eof-s1 | 'exit' or end-of-input ends the session

[you]:   [tool] search_policy({"question": "contact channels available"})

[assistant]: Kestrel can reach you by **email**, **SMS (text message)**, or **secure message** in the Kestrel app.

You currently have no channel set, so anything sent to you (case follow-ups, reminders) goes by secure message in the app. If you'd like to switch to email or SMS, I can do that - it requires identity verification (card's last 4 digits and billing ZIP). Just let me know.

[you]: 
[memory] episode E-eof-s1-1-cbb3ff: Conversation on 2026-11-24: The customer asked what contact channels the issuer uses. The assistant explained email, SMS, or secure message, noted no channel is set so secure message is the default, and offered to switch after identity verification. No case or transaction IDs; no preference stated. Case outcomes: no case touched. Lesson: none
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | a chat that ends without 'exit' (EOF) still writes its episode | `1 episodes; purged 0` |

## eof-idle-close  ·  maintenance  ·  2026-11-24T12:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | the idle-session sweep does not write the episode twice | `1 episodes; purged 0` |
