# adk · adversarial · run 1 · g49-otp-restart

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## or-cli  ·  cli_eof_session  ·  priya  ·  2026-11-09T10:00:00Z

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (ADK) | customer=priya session=or-cli | 'exit' or end-of-input ends the session

[you]:   [tool] verify_identity({"card_last4": "4427", "postal_code": "94107"})
  [tool] send_verification_code({})
  [tool] confirm_verification_code({})
  [tool] adk_request_confirmation({"originalFunctionCall": {"id": "call_00_mJFrZEteJRI65jMHG5Ur9316", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_verification_code() by responding with a FunctionResponse with an expected ToolConfirmation payload.", "confirmed": false}})

[assistant]: I'll verify you first.

[your phone, sms to +1 415 555 0100]: Your Kestrel verification code is 543015. It expires in 5 minutes. Kestrel will never ask you to share it.

[you]: 
[memory] episode E-or-cli-1-0b60a6: Conversation on 2026-11-09: Priya asked to switch her contact channel to SMS. Identity was verified, a verification code was sent by text message, and the code-confirmation step required approval; the transcript ends before completion. No case or transaction ID was provided. Customer preference: SMS contact. No promise was recorded. Case outcomes: no case touched. Lesson: Next time, obtain explicit confirmation before invoking the code-confirmation tool so the required approval is handled rather than the call returning an error.
```

## or-cli-2  ·  cli_eof_session  ·  priya  ·  2026-11-09T10:02:00Z

_Resumes session `or-cli`._

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (ADK) | customer=priya session=or-cli | 'exit' or end-of-input ends the session

[you]:   [tool] confirm_verification_code({})
  [tool] remember_customer_fact({"key": "contact_channel", "value": "sms"})

[assistant]: Done - your contact channel is now set to SMS. The one-time code went to your mobile ending ···0100, and it checked out.

[you]: 
[memory] episode E-or-cli-2-1cf0f1: Conversation on 2026-11-09: The customer completed step-up verification for a contact-channel change. The assistant set the contact channel to SMS and stored that preference as of 2026-11-09T10:02:00Z; the verification code to mobile ending ···0100 was confirmed. No case or transaction IDs, promises, or unverified claims were present. Case outcomes: no case touched. Lesson: none
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the wait survived the process ending: a second process takes the code | `{"value": "sms", "as_of": "2026-11-09T10:02:00Z", "expires_at": null}` |
| PASS | working | one code, consumed | `challenges: [('consumed', '2026-11-09T10:00')]` |
| PASS | guard | the typed code is not in the stored transcript | `store files holding a sent code: []` |
