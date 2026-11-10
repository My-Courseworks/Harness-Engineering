# langgraph · adversarial · run 1 · g9-eof

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## eof-s1  ·  cli_eof_session  ·  eli  ·  2026-11-24T10:00:00Z

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (LangGraph) | customer=eli session=eof-s1 | 'exit' or end-of-input ends the session

[you]:   [tool] search_policy({"question": "contact channels available"})

[assistant]: You can be reached by **email**, **SMS (text message)**, or **secure message** in the Kestrel app.

Right now you have no channel chosen, so anything Kestrel sends you (like dispute follow-ups or reminders) goes by secure message in the Kestrel app. If you'd like to switch to email or SMS, I can set that up - it needs a quick identity check first (card's last 4 digits and billing ZIP).

[you]: 
[memory] episode E-eof-s1-1-79492c: Conversation on 2026-11-24: The customer asked which contact channels the issuer can use. The assistant said Kestrel can contact by email, SMS, or secure message; if no channel is chosen, secure message is default. The assistant offered to switch to email or SMS after identity verification. No case or transaction IDs, promises, or customer preference were stated. Case outcomes: no case touched. Lesson: none
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | a chat that ends without 'exit' (EOF) still writes its episode | `1 episodes; purged 0` |

## eof-idle-close  ·  maintenance  ·  2026-11-24T12:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "case_followups_repaired": [], "purged_episodes": [], "deleted_transcripts": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | the idle-session sweep does not write the episode twice | `1 episodes; purged 0` |
