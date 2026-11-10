# adk · adversarial · run 1 · g9-eof

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## eof-s1  ·  cli_eof_session  ·  eli  ·  2026-11-24T10:00:00Z

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (ADK) | customer=eli session=eof-s1 | 'exit' or end-of-input ends the session

[you]:   [tool] search_policy({"question": "contact channels for follow-ups and reminders"})

[assistant]: Three options:

- **Email**
- **SMS** (text message)
- **Secure message** - the inbox in the Kestrel app

You currently have no channel set, so anything Kestrel sends you (case follow-ups and reminders) goes by secure message in the app. I can change it to email or SMS if you like - that requires verifying your identity first (card's last 4 digits and billing ZIP).

[you]: 
[memory] episode E-eof-s1-1-571928: Conversation on 2026-11-24: Customer asked which contact channels are available. Assistant explained email, SMS, and secure message; with no channel set, case follow-ups and reminders default to secure message. Assistant offered to change to email or SMS after identity verification. No case or transaction IDs, promises, or customer preferences were stated. Case outcomes: no case touched. Lesson: none
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | a chat that ends without 'exit' (EOF) still writes its episode | `1 episodes; purged 0` |

## eof-idle-close  ·  maintenance  ·  2026-11-24T12:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": [], "case_followups_repaired": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | the idle-session sweep does not write the episode twice | `1 episodes; purged 0` |
