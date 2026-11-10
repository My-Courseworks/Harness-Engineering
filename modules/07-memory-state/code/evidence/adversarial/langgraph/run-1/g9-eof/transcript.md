# langgraph · adversarial · run 1 · g9-eof

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## eof-s1  ·  cli_eof_session  ·  eli  ·  2026-11-24T10:00:00Z

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (LangGraph) | customer=eli session=eof-s1 | 'exit' or end-of-input ends the session

[you]:   [tool] search_policy({"question": "contact channels available for follow-ups and reminders"})

[assistant]: Three options: **email**, **SMS** (text), or **secure message** (the inbox in the Kestrel app).

Right now you have no channel set, so anything Kestrel sends you - case follow-ups and reminders - goes by secure message in the app. If you'd like to switch to email or SMS, I can do that; changing it requires identity verification (card last 4 digits and billing ZIP, plus a one-time code).

[you]: 
[memory] episode E-eof-s1-1-201478: Conversation on 2026-11-24: The customer asked which contact channels are available. The assistant listed email, SMS, or secure message, noted no channel is set so secure message is the default, and said switching requires identity verification. No case/transaction IDs were provided, no preference was stated, and nothing was promised. Case outcomes: no case touched. Lesson: none
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | a chat that ends without 'exit' (EOF) still writes its episode | `1 episodes; purged 0` |

## eof-idle-close  ·  maintenance  ·  2026-11-24T12:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "case_followups_repaired": [], "purged_episodes": [], "deleted_transcripts": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | the idle-session sweep does not write the episode twice | `1 episodes; purged 0` |
