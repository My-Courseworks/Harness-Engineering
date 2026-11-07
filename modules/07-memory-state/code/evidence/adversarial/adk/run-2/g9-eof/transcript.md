# adk · adversarial · run 2 · g9-eof

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## eof-s1  ·  cli_eof_session  ·  eli  ·  2026-11-24T10:00:00Z

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (ADK) | customer=eli session=eof-s1 | 'exit' or end-of-input ends the session

[you]:   [tool] search_policy({"question": "contact channels available"})

[assistant]: Kestrel can reach you by **email**, **SMS (text)**, or **secure message** (the inbox in the Kestrel app). Right now you have no channel set, so anything sent to you goes by secure message in the app.

Changing your channel takes identity verification - your card's last 4 digits and billing ZIP. Want to set one?

[you]: 
[memory] episode E-eof-s1-1-873053: Conversation on 2026-11-24: Customer asked which contact channels are available. The assistant explained that Kestrel can use email, SMS, or secure message, and that secure message is the default. The assistant said the customer had no channel set (not verified) and that changing channels requires identity verification, then offered to set one. No case or transaction IDs; nothing was promised. Case outcomes: no case touched. Lesson: none
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | a chat that ends without 'exit' (EOF) still writes its episode | `1 episodes; purged 0` |

## eof-idle-close  ·  maintenance  ·  2026-11-24T12:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | the idle-session sweep does not write the episode twice | `1 episodes; purged 0` |
