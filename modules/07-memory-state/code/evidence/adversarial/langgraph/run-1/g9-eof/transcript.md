# langgraph · adversarial · run 1 · g9-eof

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## eof-s1  ·  cli_eof_session  ·  eli  ·  2026-11-24T10:00:00Z

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (LangGraph) | customer=eli session=eof-s1 | 'exit' or end-of-input ends the session

[you]:   [tool] search_policy({"question": "contact channels available"})

[assistant]: Kestrel can reach you by **email**, **SMS** (text), or **secure message** (the inbox in the Kestrel app). If no channel is chosen, secure message is the default - which is your current setting. Changing your channel requires identity verification (card last 4 digits and billing ZIP).

[you]: 
[memory] episode E-eof-s1-1-df4b5b: Conversation on 2026-11-24: Customer asked what contact channels are available. Assistant searched policy and explained Kestrel can contact by email, SMS, or secure message; secure message is the default, and the assistant said it is the customer's current setting. Changing contact channel requires identity verification. No case or transaction IDs were involved and no promises were made. Case outcomes: no case touched. Lesson: none
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | a chat that ends without 'exit' (EOF) still writes its episode | `1 episodes; purged 0` |

## eof-idle-close  ·  maintenance  ·  2026-11-24T12:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | the idle-session sweep does not write the episode twice | `1 episodes; purged 0` |
