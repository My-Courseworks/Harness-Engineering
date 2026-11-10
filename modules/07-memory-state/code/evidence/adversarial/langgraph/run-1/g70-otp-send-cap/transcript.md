# langgraph · adversarial · run 1 · g70-otp-send-cap

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## cap-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Eli, card ending 6610, ZIP 73301. Change my contact channel to email.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70188", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `null`

**Assistant:** A one-time code has been sent by text message to ···0188; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** I didn't get it. Send me a new code.

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "I didn't get it. Send me a new code.", "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call confirm_verification_code again when they are ready, without sending a new one"}`

**Assistant:** I've sent a one-time code by text message to the mobile number the bank holds on your account, ending ···0188 - it can only go there, not to another number or email. It's valid for 5 minutes.

If you'd rather have a fresh one, I can resend it - just say so. Otherwise, type the code into the chat when it arrives and I'll finish the change to email.

**Customer:** Still nothing. Send another one.

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

**Assistant:** A one-time code has been sent by text message to ···0188; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** And again, please send a new code.

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "And again, please send a new code.", "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call confirm_verification_code again when they are ready, without sending a new one"}`
- `send_verification_code({})` → `{"error": "5 codes were sent to this account in the last 24 hours, which is the limit; no code is sent and none can be until 2026-11-25T10:00:00Z. A code already sent stays valid for its 5 minutes; otherwise the customer must call Kestrel"}`

**Assistant:** I've hit the limit: five one-time codes have already gone to this account in the last 24 hours, so I can't send another until 2026-11-25 at 10:00 UTC. The most recent one is still valid for about 5 minutes - if it turns up, just type it here and I'll complete the change to email. If nothing arrives, please call Kestrel so they can sort out the delivery to ···0188.

_Episode written:_ Conversation on 2026-11-24: Eli requested changing contact channel to email. Identity was verified for 15 minutes; multiple verification codes were sent by text to a number ending 0188. The customer said no code arrived (not verified). After five codes in 24 hours, no more can be sent until 2026-11-25 10:00 UTC. Latest valid about 5 minutes; otherwise call Kestrel. No case/transaction ID. Case outcomes: no case touched. Lesson: Next time, after repeated reports of non-receipt, stop resending and escalate or offer an alternative earlier so the five-code limit is not exhausted.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | at most five codes are sent to one account in 24 hours | `5 one-time-code messages in the outbox` |
| PASS | working | asking for codes is not a failed attempt | `0 attempt rows with succeeded=0` |

## cap-forced-1  ·  forced_calls  ·  eli  ·  2026-11-24T10:30:00Z

## cap-forced-2  ·  forced_calls  ·  eli  ·  2026-11-24T10:32:00Z

## cap-forced-3  ·  forced_calls  ·  eli  ·  2026-11-24T10:34:00Z

## cap-forced-4  ·  forced_calls  ·  eli  ·  2026-11-24T10:36:00Z

## cap-forced-5  ·  forced_calls  ·  eli  ·  2026-11-24T10:38:00Z

## cap-forced-6  ·  forced_calls  ·  eli  ·  2026-11-24T10:40:00Z

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | asked at least six times, the bank sent five codes | `{"error": null, "attempts_in_batch": 0, "failed_attempts": 0, "tool_results": ["send_verification_code -> {\"error\": \"5 codes were sent to this account in the last 24 hours, which is the limit; no code is sent and none …` |
| PASS | working | the refusal says why | `['send_verification_code -> {"error": "5 codes were sent to this account in the last 24 hours, which is the limit; no code is sent and none can be until 2026-11-25T10:00:00Z. A code already sent stays valid for its 5 min …` |
| PASS | working | a refused send is not a failed attempt | `0 attempt rows with succeeded=0` |
