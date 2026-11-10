# langgraph · adversarial · run 2 · g49-otp-restart

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## or-cli  ·  cli_eof_session  ·  priya  ·  2026-11-09T10:00:00Z

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (LangGraph) | customer=priya session=or-cli | 'exit' or end-of-input ends the session

[you]:   [tool] verify_identity({"card_last4": "4427", "postal_code": "94107"})
  [tool] send_verification_code({})
  [tool] confirm_verification_code({})

[assistant]: A one-time code has been sent by text message to ···0100; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

[your phone, sms to +1 415 555 0100]: Your Kestrel verification code is 781044. It expires in 5 minutes. Kestrel will never ask you to share it.

[you]: 
[memory] episode E-or-cli-1-b57649: Conversation on 2026-11-09: Customer Priya wanted the contact channel switched to SMS. Identity was verified; a verification code was sent by text message ending 0100 and expires in 5 minutes. The assistant then called confirm_verification_code, but no result was shown. No case or transaction IDs were provided, and no completion was promised. Case outcomes: no case touched. Lesson: Wait for and report the verification-code confirmation result before treating the SMS contact-channel change as complete.
```

## or-cli-2  ·  cli_eof_session  ·  priya  ·  2026-11-09T10:02:00Z

_Resumes session `or-cli`._

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (LangGraph) | customer=priya session=or-cli | 'exit' or end-of-input ends the session

[you]:   [tool] confirm_verification_code({})
  [tool] remember_customer_fact({"key": "contact_channel", "value": "sms"})

[assistant]: Your contact channel is now set to SMS. Future follow-ups and reminders will go to ····0100 by text.

[you]: 
[memory] episode E-or-cli-2-8403e8: Conversation on 2026-11-09: After verification, the assistant stored the customer’s contact channel as SMS and confirmed future follow-ups/reminders would be sent by text to the stored contact. No case or transaction IDs were mentioned, and no deadline was promised. The transcript does not show the customer’s original request or any unverified claims. Case outcomes: no case touched. Lesson: none
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the wait survived the process ending: a second process takes the code | `{"value": "sms", "as_of": "2026-11-09T10:02:00Z", "expires_at": null}` |
| PASS | working | one code, consumed | `challenges: [('consumed', '2026-11-09T10:00')]` |
| PASS | guard | the typed code is not in the stored transcript | `store files holding a sent code: []` |
