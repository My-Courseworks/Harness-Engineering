# adk · adversarial · run 2 · g63-lost-result-of-a-paused-confirmation

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## lp-pause  ·  forced_calls  ·  eli  ·  2026-11-24T10:00:00Z

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | setup: the turn is paused on one open code | `{"error": null, "attempts_in_batch": 1, "failed_attempts": 0, "lock_respected": true, "verified": false, "cases_total": 0, "distinct_case_ids": 0, "case_followups": 0, "evidence": "", "otp_messages": 1, "open_challenges" …` |
| PASS | working | without an exception | `{"error": null, "attempts_in_batch": 1, "failed_attempts": 0, "lock_respected": true, "verified": false, "cases_total": 0, "distinct_case_ids": 0, "case_followups": 0, "evidence": "", "otp_messages": 1, "open_challenges" …` |

## lp-entry  ·  crash_session  ·  eli  ·  2026-11-24T10:01:00Z

_Resumes session `forced-lp-pause`._

_CLI exit code 137; stdout tail:_

```
Kestrel card-care (ADK) | customer=eli session=forced-lp-pause | 'exit' or end-of-input ends the session

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
Kestrel card-care (ADK) | customer=eli session=forced-lp-pause | 'exit' or end-of-input ends the session

[you]:   [tool] confirm_verification_code({})
  [tool] remember_customer_fact({"key": "contact_channel", "value": "sms"})

[assistant]: Yes - the code checked out and your contact channel is now SMS. Anything else I can help with?

[you]: 
[memory] episode E-forced-lp-pause-1-cdaead: Conversation on 2026-11-24: The customer said he was Eli (not verified) and asked to switch contact channel to SMS; he then asked if it went through. Identity and a one-time code verified. The assistant stored contact_channel=sms as of 2026-11-24T10:02:00Z and said the contact channel was now SMS. No case/transaction IDs appeared; no promises were made. Case outcomes: no case touched. Lesson: Storing a contact-channel preference in memory is not proof that the account setting was changed; next time use the appropriate account-update tool or clearly say only the preference was recorded before confirming.
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | no second code is sent | `["Your Kestrel verification code is 087269. It expires in 5 minutes. Kestrel will never ask you to share it."]` |
| PASS | semantic | the change asked for before the code is made from the bank's record of the proof | `{"value": "sms", "as_of": "2026-11-24T10:02:00Z", "expires_at": null}` |
| PASS | guard | the code typed before the crash is not left in the transcript | `store files holding a sent code: []` |
