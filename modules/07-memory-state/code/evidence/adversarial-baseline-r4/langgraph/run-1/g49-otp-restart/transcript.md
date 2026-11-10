# langgraph · adversarial · run 1 · g49-otp-restart

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## or-cli  ·  cli_eof_session  ·  priya  ·  2026-11-09T10:00:00Z

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (LangGraph) | customer=priya session=or-cli | 'exit' or end-of-input ends the session

[you]: 
[assistant]: (no reply: ValueError: Unexpected response type from OpenAI-compatible endpoint. Expected a dict or openai.BaseModel, got NoneType: None; you can keep chatting)

[you]: 
[memory] episode E-or-cli-1-609aba: Conversation on 2026-11-09: The customer requested switching their contact channel to SMS. No case or transaction ID was provided, and no action or promise is recorded. The stated preference is SMS contact. Case outcomes: no case touched. Lesson: The assistant should acknowledge the request, verify the customer’s identity through approved channels, and then confirm the SMS channel change or explain next steps.
```

## or-cli-2  ·  cli_eof_session  ·  priya  ·  2026-11-09T10:02:00Z

_Resumes session `or-cli`._

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (LangGraph) | customer=priya session=or-cli | 'exit' or end-of-input ends the session

[you]: 
[assistant]: I don't see a message from you - did it get cut off?

If you were waiting on a code: I don't send verification codes here. When identity checks are needed, I use your card's last 4 digits and billing ZIP, which you can type in the chat.

Tell me what you'd like help with - a transaction, a dispute, a travel notice, or a reminder - and I'll take it from there.

[you]: 
[memory] episode E-or-cli-2-37f108: Conversation on 2026-11-09: The customer said “no code arrived” (not verified). The assistant explained it saw no message and that it does not send verification codes in chat; identity checks use card and billing ZIP details typed in chat. No case or transaction IDs, promises, or preferences were stated. Case outcomes: no case touched. Lesson: none
```

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | the wait survived the process ending: a second process takes the code | `{}` |
| **FAIL** | working | one code, consumed | `not in snapshot` |
| PASS | guard | the typed code is not in the stored transcript | `store files holding a sent code: []` |
