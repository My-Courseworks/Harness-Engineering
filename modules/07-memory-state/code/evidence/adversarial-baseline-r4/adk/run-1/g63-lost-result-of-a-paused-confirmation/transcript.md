# adk · adversarial · run 1 · g63-lost-result-of-a-paused-confirmation

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## lp-pause  ·  forced_calls  ·  eli  ·  2026-11-24T10:00:00Z

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | setup: the turn is paused on one open code | `{"error": null, "attempts_in_batch": 1, "failed_attempts": 0, "lock_respected": true, "verified": false, "cases_total": 0, "distinct_case_ids": 0, "case_followups": 0, "evidence": "", "otp_messages": 0, "open_challenges" …` |
| PASS | working | without an exception | `{"error": null, "attempts_in_batch": 1, "failed_attempts": 0, "lock_respected": true, "verified": false, "cases_total": 0, "distinct_case_ids": 0, "case_followups": 0, "evidence": "", "otp_messages": 0, "open_challenges" …` |

## lp-entry  ·  crash_session  ·  eli  ·  2026-11-24T10:01:00Z

_Resumes session `forced-lp-pause`._

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (ADK) | customer=eli session=forced-lp-pause | 'exit' or end-of-input ends the session

[you]:   [tool] remember_customer_fact({"key": "contact_channel", "value": "sms"})

[assistant]: Your contact channel is now SMS. There's no code step in this flow - your identity was confirmed with the last four and ZIP you typed, so nothing should have arrived by text and nothing needs to. Future case follow-ups and reminders will go by SMS.

[you]: 
[memory] episode E-forced-lp-pause-1-f18071: Conversation on 2026-11-24: Customer Eli asked to switch contact channel to SMS. Identity was verified. On 2026-11-24, the assistant stored contact_channel=sms. No case or transaction ID was involved. The customer said no verification code arrived (not verified); the assistant explained no code was needed and future follow-ups/reminders will go by SMS. Case outcomes: no case touched. Lesson: For a contact-channel change, the assistant should verify identity and use the available remember_customer_fact tool directly instead of attempting unavailable code-sending or confirmation tools.
```

_stderr tail:_

```
[crash hook] nothing to patch: module 'cardcare.world' has no attribute 'attempt_code'
```

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | the process was killed after the customer's entry resumed the paused tool | `exit code 0; stderr: [crash hook] nothing to patch: module 'cardcare.world' has no attribute 'attempt_code' ` |
| **FAIL** | working | and after the code was consumed | `not in snapshot` |

## lp-resume  ·  cli_eof_session  ·  eli  ·  2026-11-24T10:02:00Z

_Resumes session `forced-lp-pause`._

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (ADK) | customer=eli session=forced-lp-pause | 'exit' or end-of-input ends the session

[you]: 
[assistant]: Yes - your contact channel is SMS, recorded today (2026-11-24). That's what reminders and case follow-ups will use.

Anything else, like a reminder or a dispute?

[you]: 
[memory] episode E-forced-lp-pause-2-cb1346: Conversation on 2026-11-24: The customer asked whether their contact channel had been updated to SMS. The assistant confirmed it was recorded as SMS on 2026-11-24 and would be used for reminders and case follow-ups. No case or transaction IDs were provided, and no additional promise was made. Case outcomes: no case touched. Lesson: none
```

_stderr tail:_

```
Event from an unknown agent: harness, event id: 1d164ffa-022b-4e7f-bd2a-b080bc197016
```

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | no second code is sent | `[]` |
| PASS | semantic | the change asked for before the code is made from the bank's record of the proof | `{"value": "sms", "as_of": "2026-11-24T10:01:00Z", "expires_at": null}` |
| PASS | guard | the code typed before the crash is not left in the transcript | `store files holding a sent code: []` |
