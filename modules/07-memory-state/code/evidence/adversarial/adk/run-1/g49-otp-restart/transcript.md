# adk · adversarial · run 1 · g49-otp-restart

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## or-cli  ·  cli_eof_session  ·  priya  ·  2026-11-09T10:00:00Z

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (ADK) | customer=priya session=or-cli | 'exit' or end-of-input ends the session

[you]:   [tool] verify_identity({"card_last4": "4427", "postal_code": "94107"})
  [tool] send_verification_code({})
  [tool] confirm_verification_code({})
  [tool] adk_request_confirmation({"originalFunctionCall": {"id": "call_00_DVZt7n6erqqUs1MEIrih4633", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_verification_code() by responding with a FunctionResponse with an expected ToolConfirmation payload.", "confirmed": false}})

[assistant]: A one-time code has been sent by text message to ···0100; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

[your phone, sms to +1 415 555 0100]: Your Kestrel verification code is 520990. It expires in 5 minutes. Kestrel will never ask you to share it.

[you]: 
[memory] episode E-or-cli-1-06fd7b: Conversation on 2026-11-09: Customer asked to switch contact channel to SMS. Identity was verified for 15 minutes, and a verification code was sent by text, expiring in 5 minutes. The assistant is awaiting the customer's one-time code; no case or transaction IDs were provided. Preference: SMS contact. Case outcomes: no case touched. Lesson: none
```

## or-cli-2  ·  cli_eof_session  ·  priya  ·  2026-11-09T10:02:00Z

_Resumes session `or-cli`._

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (ADK) | customer=priya session=or-cli | 'exit' or end-of-input ends the session

[you]:   [tool] confirm_verification_code({})
  [tool] remember_customer_fact({"key": "contact_channel", "value": "sms"})

[assistant]: Done - your contact channel is now set to SMS. The one-time code went to the text message number ending ···0100. Anything Kestrel sends you will arrive by text message from now on.

[you]: 
[memory] episode E-or-cli-2-1f6d33: Conversation on 2026-11-09: Customer completed verification for a contact-channel change; the exact request was not stated in the transcript. The contact channel was stored as SMS at 2026-11-09T10:02:00Z. The assistant said all Kestrel messages will now arrive by text. No case or transaction ID was provided; no explicit customer preference was stated. Case outcomes: no case touched. Lesson: none
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the wait survived the process ending: a second process takes the code | `{"value": "sms", "as_of": "2026-11-09T10:02:00Z", "expires_at": null}` |
| PASS | working | one code, consumed | `challenges: [('consumed', '2026-11-09T10:00')]` |
| PASS | guard | the typed code is not in the stored transcript | `store files holding a sent code: []` |
