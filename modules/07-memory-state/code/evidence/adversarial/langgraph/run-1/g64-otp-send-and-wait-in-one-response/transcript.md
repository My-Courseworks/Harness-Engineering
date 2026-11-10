# langgraph · adversarial · run 1 · g64-otp-send-and-wait-in-one-response

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## sw-batch  ·  forced_calls  ·  marco  ·  2026-11-12T10:00:00Z

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the response sends one code and pauses for it | `{"error": null, "attempts_in_batch": 1, "failed_attempts": 0, "tool_results": ["verify_identity -> {\"verified\": true, \"valid_for_minutes\": 15}", "send_verification_code -> {\"sent\": true, \"sent_to\": \"text message …` |
| PASS | working | without an exception | `{"error": null, "attempts_in_batch": 1, "failed_attempts": 0, "tool_results": ["verify_identity -> {\"verified\": true, \"valid_for_minutes\": 15}", "send_verification_code -> {\"sent\": true, \"sent_to\": \"text message …` |

## sw-entry  ·  session  ·  marco  ·  2026-11-12T10:02:00Z

_Resumes session `forced-sw-batch`._

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-12T10:02:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Done - your contact channel is now set to email. The one-time code went to the mobile number ending ··0133. Anything Kestrel sends you will reach you by email from now on.

_Episode written:_ Conversation on 2026-11-12: Customer asked to change his contact channel to email. Identity was verified; a one-time code sent to mobile ending ··0133 was confirmed. The contact_channel=email fact was stored as of 2026-11-12T10:02:00Z. No case or transaction IDs were provided. Future Kestrel messages were promised to go by email. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the customer's entry two minutes later does not send a second code | `["Your Kestrel verification code is 922342. It expires in 5 minutes. Kestrel will never ask you to share it."]` |
| PASS | working | the code they typed is the code that is checked: no failed attempt | `0 attempt rows with succeeded=0` |
| PASS | working | one code, consumed | `challenges: [('consumed', '2026-11-12T10:00')]` |
| PASS | semantic | and the channel is changed | `{"value": "email", "as_of": "2026-11-12T10:02:00Z", "expires_at": null}` |
| PASS | guard | the typed code is not in the stored transcript | `store files holding a sent code: []` |
