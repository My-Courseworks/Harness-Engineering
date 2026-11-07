# adk · adversarial · run 2 · g9-eof

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## eof-s1  ·  cli_eof_session  ·  eli  ·  2026-11-24T10:00:00Z

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (ADK) | customer=eli session=eof-s1 | 'exit' or end-of-input ends the session

[you]:   [tool] search_policy({"question": "What contact channels can Kestrel use to reach customers?"})

[assistant]: Kestrel can reach you by:

- **email**
- **sms** (text message)
- **secure_message** (the inbox in the Kestrel app)

If you haven't chosen a channel, Kestrel uses **secure_message** by default. Note that changing your contact channel requires identity verification (card last 4 digits and billing ZIP), since it's a common step in account takeover.

[you]: 
[memory] episode E-eof-s1-1: Conversation on 2026-11-24: The customer asked which contact channels Kestrel can use. The assistant searched the contact-preferences policy and answered: email, SMS, and secure_message; secure_message is the default if no channel is chosen; changing the channel requires identity verification. No case or transaction IDs were provided, and no promises or channel preference were stated. Case outcomes: no case touched. Lesson: none
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | a chat that ends without 'exit' (EOF) still writes its episode | `1 episodes; purged 0` |

## eof-idle-close  ·  maintenance  ·  2026-11-24T12:00:00Z

_maintenance:_ `{"erased_customers": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | the idle-session sweep does not write the episode twice | `1 episodes; purged 0` |
