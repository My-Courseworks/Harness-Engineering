# adk · adversarial · run 1 · g71-otp-third-wrong-says-locked

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

**This is not a run of the product.** The mutant `the-lock-is-not-said` (probes/mutants/mutants.py) put one defect back before the run, to show the check written for it failing.

## tl-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Dana, card ending 5127, ZIP 60614. Switch my contact channel to sms.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "email to d\u00b7\u00b7\u00b7@example.com", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_OHWTyff0EX58ieWvlCpc7336", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_verif …)` → `null`

**Assistant:** A one-time code has been sent by email to d···@example.com; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "[REDACTED ONE-TIME CODE]", "error": "that code is not right", "entries_left_for_this_code": 2}`

**Assistant:** Thanks - your identity is verified, but the code that just came through didn't match the one we sent to your email (d···@example.com).

Would you like me to send a new code? The current one is valid until 10:05 UTC, and there are 2 attempts left on it if you'd rather try again.

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "error": "that code is not right", "entries_left_for_this_code": 1}`

**Assistant:** That one didn't match either - there's 1 attempt left on this code, and it expires at 10:05 UTC.

Want me to send a fresh code to your email at d···@example.com? I won't send one unless you ask.

**Customer:** That one must have expired, send me a new code.

- `send_verification_code({})` → `{"sent": true, "sent_to": "email to d\u00b7\u00b7\u00b7@example.com", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_ET_84VIbrLBwKBZcc55U8Gm6015", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_ve …)` → `null`

**Assistant:** A one-time code has been sent by email to d···@example.com; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "[REDACTED ONE-TIME CODE]", "error": "that code is not right", "entries_left_for_this_code": 2}`

**Assistant:** The code just entered didn't match the new one we sent to d···@example.com. This code stays valid for about 5 minutes and has 2 attempts left.

Type the newest code from that email when you have it, or tell me if you'd like another one sent.

_Episode written:_ Conversation on 2026-11-13: Dana asked to switch contact channel to SMS. Identity verified via card details and ZIP; codes emailed to masked address. Three entered codes failed. Customer said code expired (not verified), so new code was sent. Latest code failed; 2 attempts remain, valid about 5 minutes. No case/transaction ID appeared. Case outcomes: no case touched. Lesson: Next time, after the one-time code is accepted, explicitly complete and confirm the requested switch to SMS, since only verification steps occurred here.

_Judge `tl-no-offer`: **fail**, The assistant did not avoid offering a new code; it said, "or tell me if you'd like another one sent."_

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | three failed attempts | `3 attempt rows with succeeded=0` |
| **FAIL** | working | the third wrong entry's result says verification is locked | `{"verified": false, "customer_wrote": "[REDACTED ONE-TIME CODE]", "error": "that code is not right", "entries_left_for_this_code": 2}` |
| PASS | external | no third code is sent to a locked account | `2 one-time-code messages in the outbox` |
| **FAIL** | working | judge: After the customer's last message, did the assistant avoid offering to send a new code (it may say verification is locked and that the customer must call Kestrel)? | `{"verdict": "fail", "reason": "The assistant did not avoid offering a new code; it said, \"or tell me if you'd like another one sent.\"", "samples": ["fail", "fail", "fail"], "model": "deepseek-v4-pro"}` |
