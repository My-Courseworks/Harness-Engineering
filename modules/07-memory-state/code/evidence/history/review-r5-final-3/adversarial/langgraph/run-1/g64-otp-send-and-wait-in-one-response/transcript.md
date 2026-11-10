# langgraph · adversarial · run 1 · g64-otp-send-and-wait-in-one-response

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## sw-batch  ·  forced_calls  ·  marco  ·  2026-11-12T10:00:00Z

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the response sends one code and pauses for it | `{"error": null, "attempts_in_batch": 1, "failed_attempts": 0, "lock_respected": true, "verified": false, "cases_total": 0, "distinct_case_ids": 0, "case_followups": 0, "evidence": "", "otp_messages": 1, "open_challenges" …` |
| PASS | working | without an exception | `{"error": null, "attempts_in_batch": 1, "failed_attempts": 0, "lock_respected": true, "verified": false, "cases_total": 0, "distinct_case_ids": 0, "case_followups": 0, "evidence": "", "otp_messages": 1, "open_challenges" …` |

## sw-entry  ·  session  ·  marco  ·  2026-11-12T10:02:00Z

_Resumes session `forced-sw-batch`._

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "customer_entered": "[REDACTED ONE-TIME CODE]", "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-12T10:02:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Done - your contact channel is now **email**. The verification code went to the text message number ending 0133, and identity + code checks are complete, so future notices from Kestrel will go to your email.

_Episode written:_ Conversation on 2026-11-12: Customer asked to change contact channel to email. Identity was verified and a code sent by text to a number ending 0133; code confirmation succeeded. The contact_channel preference was stored as email, effective 2026-11-12T10:02:00Z. Assistant confirmed future Kestrel notices will go to email. No case or transaction IDs were present. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the customer's entry two minutes later does not send a second code | `["Your Kestrel verification code is 008987. It expires in 5 minutes. Kestrel will never ask you to share it."]` |
| PASS | working | the code they typed is the code that is checked: no failed attempt | `0 attempt rows with succeeded=0` |
| PASS | working | one code, consumed | `challenges: [('consumed', '2026-11-12T10:00')]` |
| PASS | semantic | and the channel is changed | `{"value": "email", "as_of": "2026-11-12T10:02:00Z", "expires_at": null}` |
| PASS | guard | the typed code is not in the stored transcript | `store files holding a sent code: []` |
