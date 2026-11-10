# adk · adversarial · run 1 · g69-otp-what-is-an-entry

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## en-s1  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Priya here, card ending 4427, ZIP 94107. Switch my contact channel to email.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70100", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_P9goerW6WSiCoeZEGERF6306", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_verif …)` → `null`

**Assistant:** A one-time code has been sent by text message to ···0100; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** It hasn't arrived. Is it going to the number ending 0100? I'm in 94

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "It hasn't arrived. Is it going to the number ending 0100? I'm in 94", "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call confirm_verification_code again when they are ready, without sending a new one"}`

**Assistant:** Yes - the code was sent by text message to the mobile number the bank holds, ending 0100. It can only go to that number; I can't send it anywhere else. It's valid for 5 minutes.

If it hasn't arrived, check that number's messages, and type the code here when it comes and I'll check it.

Also - I wasn't sure what "I'm in 94" meant; could you clarify? Your identity check already went through, so you don't need to re-enter anything for that.

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-09T10:04:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Done - your contact channel is now email. Anything Kestrel sends you (like a dispute follow-up) will go by email from here on.

"replaced: null" means there was no previous channel stored to overwrite.

_Episode written:_ Conversation on 2026-11-09: Priya asked to switch her contact channel to email. Verification succeeded and contact channel stored as email. She said the code hadn't arrived and 'I'm in 94' (not verified); the assistant explained it went to the bank-held mobile ending 0100, valid 5 minutes. Kestrel messages, including dispute follow-ups, will go by email from now on. No case/transaction ID was provided. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | a message whose digits happen to total six is not a guess: no failed attempt | `0 attempt rows with succeeded=0` |
| PASS | semantic | the code typed after it is accepted | `{"value": "email", "as_of": "2026-11-09T10:04:00Z", "expires_at": null}` |

## en-other-chat  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

_Resumes session `en-wait`._

**Customer:** Marco, card ending 8830, ZIP 10011. Change my contact channel to email.

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70133", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_ET_VqNWF1LpnXGuB1cLrFHK2793", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_ve …)` → `null`

**Assistant:** A one-time code has been sent by text message to ···0133; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

## en-other-chat-2  ·  session  ·  marco  ·  2026-11-12T10:01:00Z

_Resumes session `en-elsewhere`._

**Customer:** Different question while I wait: is [REDACTED ONE-TIME CODE] one of your reference numbers?

- `confirm_verification_code({})` → `{"verified": false, "note": "a code is open for this customer, but it was sent from another conversation: a six-digit number typed here is removed and not checked. To verify in this conversation, send a new code (send_verification_code)"}`

**Assistant:** The part of your message with the six-digit number was removed before it reached me, so I can't see it and can't tell you anything about it - and it isn't needed. Kestrel reference numbers are case ids (like C-5001) and transaction ids (like T-1002), not six-digit codes.

One thing: the code from earlier can't be used to finish verification in this conversation, so a number typed here won't be checked. If you want to go ahead with the contact-channel change, I can send a fresh code to the mobile ending 0133 - just say the word.

_Episode written:_ Conversation on 2026-11-12: Customer asked if a one-time code was a Kestrel reference number. Assistant clarified it was removed and not needed; reference numbers are case IDs/transaction IDs, not six-digit codes. Tool said the earlier code could not verify this conversation. Assistant offered a fresh code to mobile ending 0133 for the contact-channel change if requested. No case or transaction ID was provided. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | six digits typed in another conversation are not checked against the code: no attempt | `0 attempt rows with succeeded=0` |
| PASS | working | the code stays open for the conversation that asked for it | `challenges: [('open', '2026-11-12T10:00')]` |

## en-back  ·  session  ·  marco  ·  2026-11-12T10:02:00Z

_Resumes session `en-wait`._

**Customer:** [REDACTED ONE-TIME CODE] or maybe [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "[REDACTED ONE-TIME CODE] or maybe [REDACTED ONE-TIME CODE]", "note": "the message held more than one six-digit number: none was checked and nothing was counted. Ask the customer to type only the code, as their whole message"}`

**Assistant:** Your identity is verified. I've sent a one-time code by text message to the mobile number the bank holds, ending ···0133 - it can't be sent anywhere else. It's valid for 5 minutes; a new one can be sent after 60 seconds if needed.

Your last message had more than one six-digit number in it, so none was checked. Please reply with just the code, on its own - nothing else in the message - and I'll complete the switch to email.

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-12T10:04:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Done - your contact channel is now set to email. That's where we'll reach you for things like dispute follow-ups. Let me know if you'd like it changed again.

_Episode written:_ Conversation on 2026-11-12: Customer asked to change contact channel to email. Identity was verified and a one-time code was sent by text; the first code reply contained multiple six-digit numbers and was not checked, then the customer replied with only the code and verification succeeded. The contact channel was stored as email on 2026-11-12T10:04:00Z. No case or transaction IDs appeared. Case outcomes: no case touched. Lesson: Next time, before sending the one-time code, tell the customer to reply with only the code as the whole message so multi-code replies do not delay verification.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | two numbers in one message are not checked, either of them: still no failed attempt | `0 attempt rows with succeeded=0` |
| PASS | semantic | then the code alone is accepted | `{"value": "email", "as_of": "2026-11-12T10:04:00Z", "expires_at": null}` |
| PASS | guard | none of it is stored | `store files holding a sent code: []` |
