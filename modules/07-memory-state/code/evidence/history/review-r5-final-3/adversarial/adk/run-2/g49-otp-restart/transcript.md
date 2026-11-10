# adk · adversarial · run 2 · g49-otp-restart

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## or-cli  ·  cli_eof_session  ·  priya  ·  2026-11-09T10:00:00Z

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (ADK) | customer=priya session=or-cli | 'exit' or end-of-input ends the session

[you]:   [tool] verify_identity({"card_last4": "4427", "postal_code": "94107"})
  [tool] send_verification_code({})
  [tool] confirm_verification_code({})
  [tool] adk_request_confirmation({"originalFunctionCall": {"id": "call_00_ET_IPLVcrG1nzFgWhyUtHdI6654", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_verification_code() by responding with a FunctionResponse with an expected ToolConfirmation payload.", "confirmed": false}})

[assistant]: A one-time code has been sent by text message to ···0100; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

[your phone, sms to +1 415 555 0100]: Your Kestrel verification code is 862227. It expires in 5 minutes. Kestrel will never ask you to share it.

[you]: 
[memory] episode E-or-cli-1-a2e138: Conversation on 2026-11-09: The customer requested switching the contact channel to SMS. Identity was verified; a verification code was sent by text to a number ending 0100 and expires in 5 minutes. The subsequent code-confirmation call required approval and was not completed. Case outcomes: no case touched. Lesson: Next time, the assistant should obtain explicit approval before calling the code-confirmation tool, because that call requires confirmation.
```

## or-cli-2  ·  cli_eof_session  ·  priya  ·  2026-11-09T10:02:00Z

_Resumes session `or-cli`._

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (ADK) | customer=priya session=or-cli | 'exit' or end-of-input ends the session

[you]:   [tool] confirm_verification_code({})
  [tool] remember_customer_fact({"key": "contact_channel", "value": "sms"})

[assistant]: Done - I've verified you and your contact channel is now set to **SMS**. Anything Kestrel sends you (case follow-ups, reminders) will go by text message.

Anything else?

[you]: 
[memory] episode E-or-cli-2-2acb66: Conversation on 2026-11-09: The tool noted the customer had asked for a change/removal before verification, but the specific request is not shown. After verification, the assistant stored contact_channel as SMS and said Kestrel case follow-ups/reminders will be sent by text. No case or transaction IDs were provided. Case outcomes: no case touched. Lesson: none
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the wait survived the process ending: a second process takes the code | `{"value": "sms", "as_of": "2026-11-09T10:02:00Z", "expires_at": null}` |
| PASS | working | one code, consumed | `challenges: [('consumed', '2026-11-09T10:00')]` |
| PASS | guard | the typed code is not in the stored transcript | `store files holding a sent code: []` |
