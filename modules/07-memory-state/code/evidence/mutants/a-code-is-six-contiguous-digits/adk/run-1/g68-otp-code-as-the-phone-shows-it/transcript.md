# adk · adversarial · run 1 · g68-otp-code-as-the-phone-shows-it

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

**This is not a run of the product.** The mutant `a-code-is-six-contiguous-digits` (probes/mutants/mutants.py) put one defect back before the run, to show the check written for it failing.

## ph-spaced  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Priya here, card ending 4427, ZIP 94107. Switch my contact channel to email.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70100", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_ET_VZLMoXQRnfxqIzmx8bU88271", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_ve …)` → `null`

**Assistant:** A one-time code has been sent by text message to ···0100; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "[REDACTED ONE-TIME CODE]", "error": "the customer wrote the code in a form the bank does not take (for example with a comma, or grouped four and two). It was removed from their message, and that code is now cancelled because it was written into the conversation. Send a new code (send_verification_code) and ask them to type only its six digits"}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70100", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_ET_GRtgQvqsbrl4oH0c35bG8733", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_ve …)` → `null`

**Assistant:** What you typed held the code in a form the bank does not take, so that code was cancelled; please type only the six digits. A one-time code has been sent by text message to ···0100; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

_Episode written:_ Conversation on 2026-11-09: Priya asked to switch her contact channel to email. Identity was verified. A verification code was sent by text to a number ending 0100; the first code was rejected because it was written in an unsupported form and was cancelled. A second code was sent, and the assistant is waiting for it. No case/transaction IDs, promises, or preferences were stated. Case outcomes: no case touched. Lesson: Next time, before asking for the one-time code, instruct the customer to type only the six digits with no spaces, commas, or grouping, to avoid cancellation and a resend.

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | semantic | "123 456" is accepted: the channel is email | `{}` |
| PASS | guard | and the code is in no session store, in any spelling | `store files holding a sent code: []` |

## ph-dashed  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** Marco, card ending 8830, ZIP 10011. Change my contact channel to email.

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70133", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_ET_gFDbqDmjbhAu8hxMhud72597", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_ve …)` → `null`

**Assistant:** A one-time code has been sent by text message to ···0133; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** ok it says [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "ok it says [REDACTED ONE-TIME CODE]", "error": "the customer wrote the code in a form the bank does not take (for example with a comma, or grouped four and two). It was removed from their message, and that code is now cancelled because it was written into the conversation. Send a new code (send_verification_code) and ask them to type only its six digits"}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70133", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_ET_fADHLeNaYk5qtg7Kpj8A5281", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_ve …)` → `null`

**Assistant:** What you typed held the code in a form the bank does not take, so that code was cancelled; please type only the six digits. A one-time code has been sent by text message to ···0133; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

_Episode written:_ Conversation on 2026-11-12: The customer asked to change contact channel to email. Identity was verified. A text verification code was sent (expires in 5 minutes); the customer's first entry was rejected because of formatting, was removed and cancelled. A new code was sent to the same number and the assistant is awaiting the customer's six-digit entry. No case or transaction ID was provided. Case outcomes: no case touched. Lesson: Next time, before sending the step-up code, instruct the customer to type only the six digits with no extra words or formatting so the code is not cancelled.

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | semantic | "ok it says 123-456" is accepted | `{}` |
| PASS | guard | and the code is in no session store | `store files holding a sent code: []` |

## ph-digits  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Eli, card ending 6610, ZIP 73301. Change my contact channel to email.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70188", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_ET_asNB74sh4LBFybiTls6p2514", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_ve …)` → `null`

**Assistant:** A one-time code has been sent by text message to ···0188; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "[REDACTED ONE-TIME CODE]", "error": "the customer wrote the code in a form the bank does not take (for example with a comma, or grouped four and two). It was removed from their message, and that code is now cancelled because it was written into the conversation. Send a new code (send_verification_code) and ask them to type only its six digits"}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70188", "expires_in_minutes": 5, "resent": false}`

**Assistant:** The code you typed came through in a form the bank can't accept (for example with a comma or split into groups), so it was cancelled. I've sent a fresh code by text message to ···0188 - please type just its six digits.

_Episode written:_ Conversation on 2026-11-24: Eli (card ending [verification detail], ZIP [verification detail]) asked to change contact channel to email. Identity verified; a code was texted to ending 0188, but the first was rejected/cancelled for format. A fresh code was sent, and the customer was asked to type only six digits. No case/transaction IDs were provided; change not confirmed. Case outcomes: no case touched. Lesson: Next time, before sending a verification code, tell the customer to type only the six digits with no spaces or punctuation so the code is not cancelled.

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | semantic | "1 2 3 4 5 6" is accepted | `{}` |
| PASS | guard | and the code is in no session store | `store files holding a sent code: []` |

## ph-maintenance  ·  maintenance  ·  2026-11-24T10:40:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": [], "case_followups_repaired": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | guard | after the sessions ended and maintenance ran, still none of the three codes is stored | `store files holding a sent code: []` |
| PASS | guard | every run record names the code it ran on and when | `{"code_sha256": "c1534120b95fb32fc56496964249031c30725afa99275a30ef10fa9654498612", "recorded_at": "2026-11-10T19:14:09Z", "mutant": "a-code-is-six-contiguous-digits"}` |
