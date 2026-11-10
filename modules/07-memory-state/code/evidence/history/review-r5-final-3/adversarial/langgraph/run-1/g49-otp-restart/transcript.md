# langgraph · adversarial · run 1 · g49-otp-restart

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## or-cli  ·  cli_eof_session  ·  priya  ·  2026-11-09T10:00:00Z

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (LangGraph) | customer=priya session=or-cli | 'exit' or end-of-input ends the session

[you]:   [tool] verify_identity({"card_last4": "4427", "postal_code": "94107"})
  [tool] send_verification_code({})

[assistant]: I've sent a one-time code by text message to the number ending ···0100 - it can only go to the number the bank holds on file. Please type the 6-digit code here and I'll complete the switch to SMS.

[your phone, sms to +1 415 555 0100]: Your Kestrel verification code is 976669. It expires in 5 minutes. Kestrel will never ask you to share it.

[you]: 
[memory] episode E-or-cli-1-280f76: Conversation on 2026-11-09: The customer asked to switch their contact channel to SMS. The assistant verified identity, sent a one-time code by text to the bank-held number ending ···0100, and asked the customer to enter the 6-digit code to complete the switch. No case or transaction IDs were provided. Case outcomes: no case touched. Lesson: none
```

## or-cli-2  ·  cli_eof_session  ·  priya  ·  2026-11-09T10:02:00Z

_Resumes session `or-cli`._

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (LangGraph) | customer=priya session=or-cli | 'exit' or end-of-input ends the session

[you]:   [tool] confirm_verification_code({"entered": "[REDACTED ONE-TIME CODE]"})
  [tool] remember_customer_fact({"key": "contact_channel", "value": "sms"})

[assistant]: Done - your contact channel is now SMS, so Kestrel will reach you by text at the number ending ···0100. Anything else I can help with?

[you]: 
[memory] episode E-or-cli-2-b3ad6e: Conversation on 2026-11-09: The customer wanted their contact channel changed to SMS and completed step-up verification with a one-time code; verification succeeded for 15 minutes. The assistant stored contact_channel as SMS (as of 2026-11-09T10:02:00Z, no expiry) and said Kestrel would reach them by text. No case or transaction IDs were present. Case outcomes: no case touched. Lesson: none
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the wait survived the process ending: a second process takes the code | `{"value": "sms", "as_of": "2026-11-09T10:02:00Z", "expires_at": null}` |
| PASS | working | one code, consumed | `challenges: [('consumed', '2026-11-09T10:00')]` |
| PASS | guard | the typed code is not in the stored transcript | `store files holding a sent code: []` |
