# langgraph · adversarial · run 2 · g9-eof

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## eof-s1  ·  cli_eof_session  ·  eli  ·  2026-11-24T10:00:00Z

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (LangGraph) | customer=eli session=eof-s1 | 'exit' or end-of-input ends the session

[you]:   [tool] search_policy({"question": "What contact channels can Kestrel use to reach a customer?"})

[assistant]: Kestrel can reach you by **email**, **SMS**, or **secure message** (the inbox in the Kestrel app).

You don't currently have a channel on file, so the default is secure message. If you'd like to switch to email or SMS, let me know — I'll need to verify your identity first (card's last 4 digits and billing ZIP), since channel changes require that.

[you]: 
[memory] episode E-eof-s1-1: Conversation on 2026-11-24: Customer asked which contact channels Kestrel uses. Assistant said email, SMS, or secure message (default secure message); switching to email/SMS requires identity verification using card last four digits and billing ZIP. No case or transaction IDs were given, no promise was made, and the customer stated no channel preference. Case outcomes: no case touched. Lesson: none
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | a chat that ends without 'exit' (EOF) still writes its episode | `1 episodes; purged 0` |

## eof-idle-close  ·  maintenance  ·  2026-11-24T12:00:00Z

_maintenance:_ `{"closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | the idle-session sweep does not write the episode twice | `1 episodes; purged 0` |
