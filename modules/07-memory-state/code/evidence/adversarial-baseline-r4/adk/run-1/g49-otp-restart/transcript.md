# adk · adversarial · run 1 · g49-otp-restart

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## or-cli  ·  cli_eof_session  ·  priya  ·  2026-11-09T10:00:00Z

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (ADK) | customer=priya session=or-cli | 'exit' or end-of-input ends the session

[you]:   [tool] verify_identity({"card_last4": "4427", "postal_code": "94107"})
  [tool] remember_customer_fact({"key": "contact_channel", "value": "sms"})

[assistant]: You're verified, and your contact channel is now set to SMS. Messages from Kestrel - including dispute follow-ups - will go to you by text.

[you]: 
[memory] episode E-or-cli-1-71775b: Conversation on 2026-11-09: Customer Priya requested that contact channel be switched to SMS. Identity was verified, and the contact_channel preference was stored as SMS (as of 2026-11-09T10:00:00Z, no expiry). Assistant confirmed messages, including dispute follow-ups, will be sent by text. No case or transaction IDs were provided. No other promises were made. Case outcomes: no case touched. Lesson: none
```

## or-cli-2  ·  cli_eof_session  ·  priya  ·  2026-11-09T10:02:00Z

_Resumes session `or-cli`._

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (ADK) | customer=priya session=or-cli | 'exit' or end-of-input ends the session

[you]: 
[assistant]: I'm not sure what you're referring to - no verification code was requested in this chat, and I can't send one.

If you were expecting a one-time code from Kestrel (for example by SMS), you can request a new one from the app or the Kestrel website. If you tell me what you're trying to do, I can point you the right way.

[you]: 
[memory] episode E-or-cli-2-dac6b4: Conversation on 2026-11-09: The customer said no code arrived (not verified), apparently seeking help with a verification code. The assistant clarified that no verification code was requested in this chat and could not send one, advised requesting a new Kestrel code via the app or website, and asked what the customer was trying to do. No case or transaction IDs, promises, or preferences were stated. Case outcomes: no case touched. Lesson: Next time, first ask what the customer was trying to do and where they expected the code from before explaining that no code was requested.
```

_stderr tail:_

```
Event from an unknown agent: harness, event id: 3fc6660a-968f-431a-8cca-05ee3312fecb
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the wait survived the process ending: a second process takes the code | `{"value": "sms", "as_of": "2026-11-09T10:00:00Z", "expires_at": null}` |
| **FAIL** | working | one code, consumed | `not in snapshot` |
| PASS | guard | the typed code is not in the stored transcript | `store files holding a sent code: []` |
