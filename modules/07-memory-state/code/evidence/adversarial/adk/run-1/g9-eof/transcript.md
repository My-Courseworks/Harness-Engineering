# adk · adversarial · run 1 · g9-eof

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## eof-s1  ·  cli_eof_session  ·  eli  ·  2026-11-24T10:00:00Z

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (ADK) | customer=eli session=eof-s1 | 'exit' or end-of-input ends the session

[you]:   [tool] search_policy({"question": "contact channels available"})

[assistant]: I'll check our policy on contact channels.
There are three: **email**, **SMS (text message)**, and **secure message** - the inbox in the Kestrel app.

You currently have no channel set, so anything we send (case follow-ups, reminders) goes by secure message in the app. You can switch to email or SMS any time; that requires a quick identity check (card's last 4 digits and billing ZIP).

[you]: 
[memory] episode E-eof-s1-1-3d8deb: Conversation on 2026-11-24: The customer asked what contact channels are available. The assistant checked the contact-preferences policy and explained that Kestrel can use email, SMS, or secure app message; with no channel chosen, secure message is the default. The assistant said switching channels requires identity verification. Case outcomes: no case touched. Lesson: none
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | a chat that ends without 'exit' (EOF) still writes its episode | `1 episodes; purged 0` |

## eof-idle-close  ·  maintenance  ·  2026-11-24T12:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | the idle-session sweep does not write the episode twice | `1 episodes; purged 0` |
