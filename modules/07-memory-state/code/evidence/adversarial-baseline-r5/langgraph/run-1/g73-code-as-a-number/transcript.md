# langgraph · adversarial · run 1 · g73-code-as-a-number

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## num-wait  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Eli, card ending 6610, ZIP 73301. Change my contact channel to email.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70188", "expires_in_minutes": 5, "resent": false}`

**Assistant:** Verified - thanks. I've sent a one-time code by text message to the mobile number ending ···0188; it's valid for 5 minutes. It can only go there, not to another number or email.

Please type the code in your next message and I'll switch your contact channel to email.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | setup: a code is open | `challenges: [('open', '2026-11-24T10:00')]` |

## num-batch  ·  forced_calls  ·  eli  ·  2026-11-24T10:01:00Z

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | guard | a code a model response carries as a number is in no session store afterwards | `store files holding a sent code: ['lg_checkpoints.db', 'lg_checkpoints.db-wal']` |

## num-after  ·  session  ·  eli  ·  2026-11-24T10:02:00Z

_Resumes session `forced-num-batch`._

**Customer:** Did that go through?

- `confirm_verification_code({})` → `null`

**Assistant:** A one-time code has been sent by text message to ···0188; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

_Episode written:_ Conversation on 2026-11-24: The customer wanted their contact channel changed to email. A verification-code confirmation failed because the entered value was not valid as a string; a follow-up call submitted no code, and no success was confirmed. No case or transaction IDs were provided. No promise was made. Customer preference: contact by email. Case outcomes: no case touched. Lesson: Next time, correct the invalid code input by collecting a valid string before retrying, rather than calling the verification tool with an empty payload.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the conversation goes on without a failed turn | `"no errors"` |
| **FAIL** | guard | and still holds no code | `store files holding a sent code: ['lg_checkpoints.db']` |
