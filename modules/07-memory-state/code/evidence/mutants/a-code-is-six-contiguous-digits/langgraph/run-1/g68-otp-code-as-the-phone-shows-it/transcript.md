# langgraph · adversarial · run 1 · g68-otp-code-as-the-phone-shows-it

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

**This is not a run of the product.** The mutant `a-code-is-six-contiguous-digits` (probes/mutants/mutants.py) put one defect back before the run, to show the check written for it failing.

## ph-spaced  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Priya here, card ending 4427, ZIP 94107. Switch my contact channel to email.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70100", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `null`

**Assistant:** A one-time code has been sent by text message to ···0100; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "[REDACTED ONE-TIME CODE]", "error": "the customer wrote the code in a form the bank does not take (for example with a comma, or grouped four and two). It was removed from their message, and that code is now cancelled because it was written into the conversation. Send a new code (send_verification_code) and ask them to type only its six digits"}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70100", "expires_in_minutes": 5, "resent": false}`

**Assistant:** Your identity is verified. I sent a new one-time code by text message to the mobile number the bank holds on your account, ending ···0100 - it can't be sent anywhere else. It's valid for 5 minutes.

The first code didn't go through because it was typed in a form the bank doesn't accept (for example with a comma or split into groups), so please type only its six digits, nothing else. I'll check it as soon as you send it.

_Episode written:_ Conversation on 2026-11-09: Priya (card ending [verification detail], ZIP [verification detail]) asked to switch contact channel to email. Identity verified. A code sent by text to number ending 0100 was rejected for formatting and cancelled; a new code was sent, valid 5 minutes, and the assistant will check it once six digits are typed. No case/transaction ID provided. Case outcomes: no case touched. Lesson: Next time, tell the customer up front to type only the six-digit code, then resend promptly if a code is cancelled for formatting.

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | semantic | "123 456" is accepted: the channel is email | `{}` |
| PASS | guard | and the code is in no session store, in any spelling | `store files holding a sent code: []` |

## ph-dashed  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** Marco, card ending 8830, ZIP 10011. Change my contact channel to email.

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70133", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `null`

**Assistant:** A one-time code has been sent by text message to ···0133; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** ok it says [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "ok it says [REDACTED ONE-TIME CODE]", "error": "the customer wrote the code in a form the bank does not take (for example with a comma, or grouped four and two). It was removed from their message, and that code is now cancelled because it was written into the conversation. Send a new code (send_verification_code) and ask them to type only its six digits"}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70133", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `null`

**Assistant:** I've sent a fresh code by text message to ···0133 - it can only go to the number the bank holds on the account. That one has to be typed as six digits only, with nothing else around it.

_Episode written:_ Conversation on 2026-11-12: Customer asked to change contact channel to email. Identity was verified for 15 minutes; a verification code was sent by text to ending 0133, but the customer’s first code was invalid/cancelled because it was written into chat. A fresh code was sent, expires in 5 minutes, and the assistant asked for six digits only; no case or transaction IDs were provided. Case outcomes: no case touched. Lesson: Next time, tell the customer before sending a verification code to type only the six digits and nothing else, so the code is not cancelled and resent.

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | semantic | "ok it says 123-456" is accepted | `{}` |
| PASS | guard | and the code is in no session store | `store files holding a sent code: []` |

## ph-digits  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Eli, card ending 6610, ZIP 73301. Change my contact channel to email.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70188", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `null`

**Assistant:** I'll verify you first.

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "[REDACTED ONE-TIME CODE]", "error": "the customer wrote the code in a form the bank does not take (for example with a comma, or grouped four and two). It was removed from their message, and that code is now cancelled because it was written into the conversation. Send a new code (send_verification_code) and ask them to type only its six digits"}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70188", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `null`

**Assistant:** The code you typed came through in a form the bank can't accept (for example with a comma or split into groups), so that code was cancelled. I've sent a new one by text message to ···0188 - please type just its six digits, nothing else.

_Episode written:_ Conversation on 2026-11-24: Customer wanted contact channel changed to email. Identity was verified for 15 minutes. A code was texted to ···0188; the first was rejected/cancelled due to unsupported format, so a new code was sent (expires in 5 minutes) and the customer was asked to type only six digits. No case or transaction IDs appeared. Case outcomes: no case touched. Lesson: Next time, before asking for a one-time code, the assistant should tell the customer to type only the six digits with no punctuation or grouping, to avoid the first code being cancelled.

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | semantic | "1 2 3 4 5 6" is accepted | `{}` |
| PASS | guard | and the code is in no session store | `store files holding a sent code: []` |

## ph-maintenance  ·  maintenance  ·  2026-11-24T10:40:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "case_followups_repaired": [], "purged_episodes": [], "deleted_transcripts": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | guard | after the sessions ended and maintenance ran, still none of the three codes is stored | `store files holding a sent code: []` |
| PASS | guard | every run record names the code it ran on and when | `{"code_sha256": "c1534120b95fb32fc56496964249031c30725afa99275a30ef10fa9654498612", "recorded_at": "2026-11-10T19:14:08Z", "mutant": "a-code-is-six-contiguous-digits"}` |
