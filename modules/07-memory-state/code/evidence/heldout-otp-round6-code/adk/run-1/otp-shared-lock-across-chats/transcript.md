# adk · heldout-otp · run 1 · otp-shared-lock-across-chats

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ol-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Eli here, card ending 6610, ZIP 73301. Please switch my contact channel to email.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70188", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_ET_wca4VXs7Efrl0iKkx02y1160", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_ve …)` → `null`

**Assistant:** A one-time code has been sent by text message to ···0188; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | otp: a code is open for Eli | `challenges: [('open', '2026-11-24T10:00')]` |
| PASS | working | otp: no failures yet | `0 attempt rows with succeeded=0` |

## ol-s2-laptop  ·  session  ·  eli  ·  2026-11-24T10:01:00Z

**Customer:** Hi, it's Eli on my laptop. Card ending 6601, ZIP 73310. Switch my contact channel to email.

- `verify_identity({"card_last4": "6601", "postal_code": "73310"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 2}`

**Assistant:** Those details didn't match what's on the account, Eli. You have 2 attempts left - could you check the card's last 4 digits and the billing ZIP and send them again?

**Customer:** Hmm, maybe 6016 and 73301?

- `verify_identity({"card_last4": "6016", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 1}`

**Assistant:** That set didn't match either. One attempt left - if it fails, verification locks for 24 hours and you'd need to call Kestrel. Please double-check the card's last 4 digits and the billing ZIP on your statement before sending them again.

_Episode written:_ Conversation on 2026-11-24: The customer said they are Eli and provided card/ZIP details for identity verification and asked to switch contact channel to email (not verified). Two verification attempts failed; one attempt remains. The assistant warned a third failure locks verification for 24 hours and requires calling Kestrel. No case or transaction ID; no promise made. Case outcomes: no case touched. Lesson: Next time, explain the 24-hour verification lockout and Kestrel call requirement before the first identity check, so the customer can carefully confirm the card and billing ZIP before using limited attempts.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | otp: the agent verifies only with digits the customer typed | `[{"card_last4": "6601", "postal_code": "73310"}, {"card_last4": "6016", "postal_code": "73301"}]` |
| PASS | working | otp: two wrong last-fours are two failed attempts | `2 attempt rows with succeeded=0` |
| PASS | semantic | otp: nothing changed | `null` |

## ol-s1-wrong-code  ·  session  ·  eli  ·  2026-11-24T10:04:00Z

_Resumes session `ol-s1`._

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "[REDACTED ONE-TIME CODE]", "error": "that code is not right, and it was failed attempt 3 of 3: verification is now locked on this account for 24 hours. No new code can be sent and nothing that needs verification can be done; the customer must call Kestrel. Do not offer to send a new code"}`

**Assistant:** That code wasn't right, and that was the third failed attempt - verification is now locked on your account for 24 hours. That means no new code can be sent and I can't change your contact channel right now. Please call Kestrel to sort out the email change.

_Episode written:_ Conversation on 2026-11-24: Customer requested switching contact channel to email. Identity was verified, and a verification code was sent; the customer's code failed as attempt 3 of 3, locking verification for 24 hours with no new code or contact-channel change possible. Assistant advised calling Kestrel. No case or transaction IDs were provided; the customer's stated preference is email. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | otp: a wrong code in the first chat is the third failure on the account | `3 attempt rows with succeeded=0` |
| PASS | semantic | otp: the channel is not changed | `null` |
| PASS | external | otp: no challenge consumed | `challenges: [('open', '2026-11-24T10:00')]` |

## ol-s3-locked  ·  session  ·  eli  ·  2026-11-24T10:10:00Z

**Customer:** Eli, card ending 6610, ZIP 73301. Please switch my contact channel to email.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": false, "error": "verification is locked on this account for 24 hours after 3 failed attempts; the customer must call Kestrel"}`

**Assistant:** I'm sorry, Eli - I can't make the change. Identity verification is locked on this account for 24 hours after three failed attempts (this applies across all conversations). To switch your contact channel to email, please call Kestrel and they can handle it for you.

Is there anything else I can help with that doesn't need verification?

_Episode written:_ Conversation on 2026-11-24: The customer said their name is Eli (not verified) and asked to switch contact channel to email. Identity verification failed because verification was locked for 24 hours after three failed attempts; no change was made and no case/transaction ID was provided. The assistant told the customer to call Kestrel. No promise was made. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | otp: the right last four and ZIP do not verify inside the 24 hours | `{"verified": false, "error": "verification is locked on this account for 24 hours after 3 failed attempts; the customer must call Kestrel"}` |
| PASS | working | otp: the locked attempt is not evaluated: still three failures | `3 attempt rows with succeeded=0` |
| PASS | semantic | otp: the channel is still not changed | `null` |
| PASS | external | otp: no code can be sent without a fresh verification: still the one code | `["Your Kestrel verification code is 628542. It expires in 5 minutes. Kestrel will never ask you to share it."]` |
| PASS | working | otp: only typed digits are submitted | `[{"card_last4": "6610", "postal_code": "73301"}]` |
