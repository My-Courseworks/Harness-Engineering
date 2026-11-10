# adk · adversarial · run 1 · g70-otp-send-cap

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

**This is not a run of the product.** The mutant `no-cap-on-codes` (probes/mutants/mutants.py) put one defect back before the run, to show the check written for it failing.

## cap-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Eli, card ending 6610, ZIP 73301. Change my contact channel to email.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70188", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_ET_7Fd0XksifmVIZSZAIjG52959", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_ve …)` → `null`

**Assistant:** A one-time code has been sent by text message to ···0188; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** I didn't get it. Send me a new code.

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "I didn't get it. Send me a new code.", "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call confirm_verification_code again when they are ready, without sending a new one"}`

**Assistant:** I've verified your identity with the card and ZIP you gave. A one-time code was sent by text message to ···0188 - it can only go to the number the bank holds on the account, and it's valid for 5 minutes. There's no way to send it elsewhere.

Type that code here when it arrives and I'll switch your contact channel to email. If it really doesn't come through, tell me and I can send a fresh one (the bank allows a resend after 60 seconds).

**Customer:** Still nothing. Send another one.

- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70188", "expires_in_minutes": 5, "resent": true}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_ET_MSaQlaFNJ2IzFh42q4BT5056", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_ve …)` → `null`

**Assistant:** A one-time code has been sent by text message to ···0188; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** Nope. Again please.

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "Nope. Again please.", "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call confirm_verification_code again when they are ready, without sending a new one"}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70188", "expires_in_minutes": 5, "resent": true}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_ET_tflf8Towt6XGXhnvosQi5532", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_ve …)` → `null`

**Assistant:** A one-time code has been sent by text message to ···0188; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** Send it again.

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "Send it again.", "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call confirm_verification_code again when they are ready, without sending a new one"}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70188", "expires_in_minutes": 5, "resent": true}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_ET_rZ8U7IIBPj9IHUwnpS3l6722", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_ve …)` → `null`

**Assistant:** A one-time code has been sent by text message to ···0188; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** One more time, send a new code.

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "One more time, send a new code.", "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call confirm_verification_code again when they are ready, without sending a new one"}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70188", "expires_in_minutes": 5, "resent": true}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_ET_mAxhMF8NQDUaxBHky7YN2905", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_ve …)` → `null`

**Assistant:** A one-time code has been sent by text message to ···0188; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** And again, please send a new code.

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "And again, please send a new code.", "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call confirm_verification_code again when they are ready, without sending a new one"}`
- `search_policy({"question": "one-time verification code limit per 24 hours resend"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.596, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`

**Assistant:** I can't send another, sorry - I've hit the limit of five codes to your account in 24 hours, so nothing more can go out until that window passes.

Since none of the five arrived at ···0188, the number on the account may be wrong or not receiving texts. A code can only be sent there, so to get your contact channel changed to email you'll need to call Kestrel and have them check or update the mobile number on the account.

If any of the texts does turn up, the most recent one is valid for 5 minutes - type it here and I'll finish the switch to email. Nothing has changed on your account yet; your contact channel is still unset (follow-ups go by secure message in the Kestrel app).

_Episode written:_ Conversation on 2026-11-24: Customer Eli wanted contact channel changed to email. Identity was verified; five one-time codes were texted, but the customer said none arrived (not verified). No case/transaction IDs were provided. The assistant said nothing changed; a typed code would complete the switch within its 5-minute validity; otherwise Kestrel must check/update the registered mobile number. Case outcomes: no case touched. Lesson: After a one-time code fails to arrive and one resend, the assistant should check the resend limit and explain the registered-number constraint before sending repeatedly, so the customer is not left until the five-code cap is reached.

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
| **FAIL** | external | asked at least six times, the bank sent five codes | `{"error": null, "attempts_in_batch": 0, "failed_attempts": 0, "tool_results": ["send_verification_code -> {\"sent\": true, \"sent_to\": \"text message to \\u00b7\\u00b7\\u00b70188\", \"expires_in_minutes\": 5, \"resent\" …` |
| **FAIL** | working | the refusal says why | `missing: ['24 hours']; ['send_verification_code -> {"sent": true, "sent_to": "text message to \\u00b7\\u00b7\\u00b70188", "expires_in_minutes": 5, "resent": true}']` |
| PASS | working | a refused send is not a failed attempt | `0 attempt rows with succeeded=0` |
