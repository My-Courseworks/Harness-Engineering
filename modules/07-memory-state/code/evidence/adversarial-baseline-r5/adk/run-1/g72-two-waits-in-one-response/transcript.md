# adk · adversarial · run 1 · g72-two-waits-in-one-response

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## tw-batch  ·  forced_calls  ·  marco  ·  2026-11-12T10:00:00Z

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the response sends one code | `{"error": null, "attempts_in_batch": 1, "failed_attempts": 0, "lock_respected": true, "verified": false, "cases_total": 0, "distinct_case_ids": 0, "case_followups": 0, "evidence": "", "otp_messages": 1, "open_challenges" …` |

## tw-entry  ·  session  ·  marco  ·  2026-11-12T10:02:00Z

_Resumes session `forced-tw-batch`._

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "customer_entered": "[REDACTED ONE-TIME CODE]", "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-12T10:02:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Done - Marco, your contact channel is now **email**. Identity was verified (card ending 8830, ZIP 10011) and the one-time code, sent by text message to the number ending ···0133, checked out.

Nothing was there before, so nothing was replaced. Anything Kestrel sends you from now on will go to your email.

**Customer:** Thanks. Which contact channel do you have for me now?

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "customer_entered": "Thanks. Which contact channel do you have for me now?", "note": "the code was entered correctly before the process stopped; this result is rebuilt from the bank's record of it, so carry out the change or removal the customer asked for before the code was sent; the customer's latest message was not a code: answer it too"}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-12T10:04:00Z", "expires_at": null}}, "replaced": "email"}`
- **error:** `BadRequestError: litellm.BadRequestError: DeepseekException - {"error":{"message":"The `reasoning_content` in the thinking mode must be passed back to the API. (request_id: 490803c6-c459-4f06-886a-cfaeb159e89e)","type":"invalid_request_error","param":null,"code":"invalid_request_error"}} LiteLLM Retried: 2 times`

**Assistant:** (no reply)

**Customer:** And what is the dispute window?

- `search_policy({"question": "dispute filing window / deadline"})` → `{"documents": [{"document": "dispute-window", "score": 0.695, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** Two answers for you:

- **Contact channel:** email - that's what's on file now (the change is done; it was already email, so nothing effectively changed).
- **Dispute window:** you can dispute a posted transaction within **75 days of its posting date**. After that, it can't be opened through the assistant and has to go in as a written claim.

_Episode written:_ Conversation on 2026-11-12: Customer said he was Marco (not verified) and asked to change his contact channel to email. Identity was verified and contact_channel was stored as email; a follow-up confirmed email is on file. Customer also asked the dispute window; assistant said posted transactions can be disputed within 75 days, then require a written claim. No case or transaction IDs. Case outcomes: no case touched. Lesson: Avoid repeating card-ending and ZIP details in confirmation messages; confirm only that identity was verified and the requested change is complete.

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | no turn of the conversation fails after two waits were opened at once | `["BadRequestError: litellm.BadRequestError: DeepseekException - {\"error\":{\"message\":\"The `reasoning_content` in the thinking mode must be passed back to the API. (request_id: 490803c6-c459-4f06-886a-cfaeb159e89e)\", …` |
| PASS | semantic | the code is accepted and the channel changed | `{"value": "email", "as_of": "2026-11-12T10:04:00Z", "expires_at": null}` |
| PASS | working | the conversation still answers: the third turn has a reply | `Two answers for you:  - **Contact channel:** email - that's what's on file now (the change is done; it was already email, so nothing effectively changed). - **Dispute window:** you can dispute a posted transaction within …` |
