# langgraph · adversarial · run 1 · g71-otp-third-wrong-says-locked

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

**This is not a run of the product.** The mutant `the-lock-is-not-said` (probes/mutants/mutants.py) put one defect back before the run, to show the check written for it failing.

## tl-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Dana, card ending 5127, ZIP 60614. Switch my contact channel to sms.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "email to d\u00b7\u00b7\u00b7@example.com", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `null`

**Assistant:** A one-time code has been sent by email to d···@example.com; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "[REDACTED ONE-TIME CODE]", "error": "that code is not right", "entries_left_for_this_code": 2}`

**Assistant:** That code didn't match - you have 2 tries left on it. Do you want me to send a new one, or would you like to try again with the code from the email?

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "error": "that code is not right", "entries_left_for_this_code": 1}`

**Assistant:** That one didn't match either - 1 try left on this code. Want me to send a fresh code, or try once more with what's in the email?

**Customer:** That one must have expired, send me a new code.

- `send_verification_code({})` → `{"sent": true, "sent_to": "email to d\u00b7\u00b7\u00b7@example.com", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `null`

**Assistant:** A one-time code has been sent by email to d···@example.com; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "[REDACTED ONE-TIME CODE]", "error": "that code is not right", "entries_left_for_this_code": 2}`

**Assistant:** The new code didn't match either - 2 tries left on it. Want me to send another one, or try again with the latest email (it's valid for 5 minutes from when it was sent)?

_Episode written:_ Conversation on 2026-11-13: Customer asked to switch contact channel to SMS; identity was verified and verification codes were emailed. Multiple customer-entered codes were rejected. A fresh code was sent and also rejected, leaving 2 tries. No case or transaction ID was provided. Customer said an earlier code must have expired (not verified). Assistant said latest email code was valid 5 minutes. Case outcomes: no case touched. Lesson: none

_Judge `tl-no-offer`: **fail**, The assistant offered to send another code: "Want me to send another one, or try again with the latest email..."_

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | three failed attempts | `3 attempt rows with succeeded=0` |
| **FAIL** | working | the third wrong entry's result says verification is locked | `{"verified": false, "customer_wrote": "[REDACTED ONE-TIME CODE]", "error": "that code is not right", "entries_left_for_this_code": 2}` |
| PASS | external | no third code is sent to a locked account | `2 one-time-code messages in the outbox` |
| **FAIL** | working | judge: After the customer's last message, did the assistant avoid offering to send a new code (it may say verification is locked and that the customer must call Kestrel)? | `{"verdict": "fail", "reason": "The assistant offered to send another code: \"Want me to send another one, or try again with the latest email...\"", "samples": ["fail", "pass", "fail"], "model": "deepseek-v4-pro"}` |
