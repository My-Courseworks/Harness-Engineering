# langgraph · adversarial · run 1 · g70-otp-send-cap

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

**This is not a run of the product.** The mutant `no-cap-on-codes` (probes/mutants/mutants.py) put one defect back before the run, to show the check written for it failing.

## cap-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Eli, card ending 6610, ZIP 73301. Change my contact channel to email.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70188", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `null`

**Assistant:** A one-time code has been sent by text message to ···0188; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** I didn't get it. Send me a new code.

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "I didn't get it. Send me a new code.", "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call confirm_verification_code again when they are ready, without sending a new one"}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70188", "expires_in_minutes": 5, "resent": true}`
- `confirm_verification_code({})` → `null`

**Assistant:** A one-time code has been sent by text message to ···0188; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** Still nothing. Send another one.

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "Still nothing. Send another one.", "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call confirm_verification_code again when they are ready, without sending a new one"}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70188", "expires_in_minutes": 5, "resent": true}`
- `confirm_verification_code({})` → `null`

**Assistant:** A one-time code has been sent by text message to ···0188; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** Nope. Again please.

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "Nope. Again please.", "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call confirm_verification_code again when they are ready, without sending a new one"}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70188", "expires_in_minutes": 5, "resent": true}`
- `confirm_verification_code({})` → `null`

**Assistant:** A one-time code has been sent by text message to ···0188; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** Send it again.

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "Send it again.", "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call confirm_verification_code again when they are ready, without sending a new one"}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70188", "expires_in_minutes": 5, "resent": true}`
- `confirm_verification_code({})` → `null`

**Assistant:** A one-time code has been sent by text message to ···0188; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** One more time, send a new code.

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "One more time, send a new code.", "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call confirm_verification_code again when they are ready, without sending a new one"}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70188", "expires_in_minutes": 5, "resent": true}`
- `confirm_verification_code({})` → `null`

**Assistant:** A new code has just been texted to the mobile number Kestrel holds for you - ···0188. That's the only place it can go: it can't be sent to your email or any other number, even though the change you're asking for is to email.

**Customer:** And again, please send a new code.

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "And again, please send a new code.", "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call confirm_verification_code again when they are ready, without sending a new one"}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70188", "expires_in_minutes": 5, "resent": true}`
- `confirm_verification_code({})` → `null`

**Assistant:** A one-time code has been sent by text message to ···0188; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

_Episode written:_ Conversation on 2026-11-24: Customer asked to change contact channel to email. Identity was verified; multiple codes were texted to the mobile on file, valid five minutes. The customer repeatedly said no code arrived (not verified) and requested resends. The assistant said codes can only go to that mobile, not email. No case/transaction IDs or completed change. Case outcomes: no case touched. Lesson: Next time, stop repeatedly resending when the customer reports not receiving the SMS; explain that the code is only sent to the mobile on file and remains valid for five minutes, then guide them on next steps.

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | external | at most five codes are sent to one account in 24 hours | `7 one-time-code messages in the outbox` |
| PASS | working | asking for codes is not a failed attempt | `0 attempt rows with succeeded=0` |

## cap-forced-1  ·  forced_calls  ·  eli  ·  2026-11-24T10:30:00Z

## cap-forced-2  ·  forced_calls  ·  eli  ·  2026-11-24T10:32:00Z

## cap-forced-3  ·  forced_calls  ·  eli  ·  2026-11-24T10:34:00Z

## cap-forced-4  ·  forced_calls  ·  eli  ·  2026-11-24T10:36:00Z

## cap-forced-5  ·  forced_calls  ·  eli  ·  2026-11-24T10:38:00Z

## cap-forced-6  ·  forced_calls  ·  eli  ·  2026-11-24T10:40:00Z

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | external | asked at least six times, the bank sent five codes | `{"error": null, "attempts_in_batch": 0, "failed_attempts": 0, "tool_results": ["send_verification_code -> {\"sent\": true, \"sent_to\": \"text message to \\u00b7\\u00b7\\u00b70188\", \"expires_in_minutes\": 5, \"resent\" …` |
| **FAIL** | working | the refusal says why | `missing: ['24 hours']; ['send_verification_code -> {"sent": true, "sent_to": "text message to \\u00b7\\u00b7\\u00b70188", "expires_in_minutes": 5, "resent": true}']` |
| PASS | working | a refused send is not a failed attempt | `0 attempt rows with succeeded=0` |
