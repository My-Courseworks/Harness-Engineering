# adk · adversarial · run 1 · g72-two-waits-in-one-response

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## tw-batch  ·  forced_calls  ·  marco  ·  2026-11-12T10:00:00Z

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the response sends one code | `{"error": null, "attempts_in_batch": 1, "failed_attempts": 0, "tool_results": ["verify_identity -> {\"verified\": true, \"valid_for_minutes\": 15}", "send_verification_code -> {\"sent\": true, \"sent_to\": \"text message …` |

## tw-entry  ·  session  ·  marco  ·  2026-11-12T10:02:00Z

_Resumes session `forced-tw-batch`._

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "customer_wrote": "[REDACTED ONE-TIME CODE]", "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "customer_wrote": "[REDACTED ONE-TIME CODE]", "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-12T10:02:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Your contact channel is now email - the one-time code went to the text message number on file (···0133) and checked out, so no earlier email address was replaced (none was set).

Anything else, Marco?

**Customer:** Thanks. Which contact channel do you have for me now?

**Assistant:** Email - that's what's on file for you now.

**Customer:** And what is the dispute window?

- `search_policy({"question": "dispute filing window deadline"})` → `{"documents": [{"document": "dispute-window", "score": 0.705, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** You can dispute a posted transaction within **75 days of its posting date**. After that, the case can't be opened through this chat and has to go in as a written claim.

_Episode written:_ Conversation on 2026-11-12: Customer wanted contact channel set to email. After one-time-code verification, assistant stored contact_channel=email and confirmed no prior email was replaced. Asked current channel (email) and dispute window; assistant cited 75 days from posting, otherwise written claim. No case/transaction IDs or promises. Preference: email contact. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | no turn of the conversation fails after two waits were opened at once | `"no errors"` |
| PASS | semantic | the code is accepted and the channel changed | `{"value": "email", "as_of": "2026-11-12T10:02:00Z", "expires_at": null}` |
| PASS | working | the conversation still answers: the third turn has a reply | `You can dispute a posted transaction within **75 days of its posting date**. After that, the case can't be opened through this chat and has to go in as a written claim.` |
