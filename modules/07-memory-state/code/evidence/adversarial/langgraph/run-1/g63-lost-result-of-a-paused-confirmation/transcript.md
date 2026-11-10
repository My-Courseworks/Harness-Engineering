# langgraph · adversarial · run 1 · g63-lost-result-of-a-paused-confirmation

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## lp-pause  ·  forced_calls  ·  eli  ·  2026-11-24T10:00:00Z

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | setup: the turn is paused on one open code | `{"error": null, "attempts_in_batch": 1, "failed_attempts": 0, "tool_results": ["verify_identity -> {\"verified\": true, \"valid_for_minutes\": 15}", "send_verification_code -> {\"sent\": true, \"sent_to\": \"text message …` |
| PASS | working | without an exception | `{"error": null, "attempts_in_batch": 1, "failed_attempts": 0, "tool_results": ["verify_identity -> {\"verified\": true, \"valid_for_minutes\": 15}", "send_verification_code -> {\"sent\": true, \"sent_to\": \"text message …` |

## lp-entry  ·  crash_session  ·  eli  ·  2026-11-24T10:01:00Z

_Resumes session `forced-lp-pause`._

_CLI exit code 137; stdout tail:_

```
Kestrel card-care (LangGraph) | customer=eli session=forced-lp-pause | 'exit' or end-of-input ends the session

[you]:
```

_stderr tail:_

```
[crash hook] attempt_code done; exiting before its result is recorded
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the process was killed after the customer's entry resumed the paused tool | `exit code 137; stderr: [crash hook] attempt_code done; exiting before its result is recorded ` |
| PASS | working | and after the code was consumed | `challenges: [('consumed', '2026-11-24T10:00')]` |

## lp-resume  ·  cli_eof_session  ·  eli  ·  2026-11-24T10:02:00Z

_Resumes session `forced-lp-pause`._

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (LangGraph) | customer=eli session=forced-lp-pause | 'exit' or end-of-input ends the session

[you]:   [tool] confirm_verification_code({})
  [tool] remember_customer_fact({"key": "contact_channel", "value": "sms"})

[assistant]: Yes - it went through. Your contact channel is now SMS, so future updates and case follow-ups will reach you by text.

[you]: 
[memory] episode E-forced-lp-pause-1-c253e6: Conversation on 2026-11-24: Customer Eli asked to switch contact channel to SMS. Identity and one-time-code verification succeeded; the assistant stored contact_channel=sms as of 2026-11-24T10:02:00Z and confirmed future updates will arrive by text. No case or transaction IDs were present. Preference: SMS contact. Case outcomes: no case touched. Lesson: Next time, explicitly tell the customer that a one-time SMS code was sent and must be entered before the contact-channel change is finalized, rather than leaving them to ask whether it went through.
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | no second code is sent | `["Your Kestrel verification code is 762754. It expires in 5 minutes. Kestrel will never ask you to share it."]` |
| PASS | semantic | the change asked for before the code is made from the bank's record of the proof | `{"value": "sms", "as_of": "2026-11-24T10:02:00Z", "expires_at": null}` |
| PASS | guard | the code typed before the crash is not left in the transcript | `store files holding a sent code: []` |
