# adk · heldout-otp · run 1 · otp-shared-lock-across-chats

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ol-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Eli here, card ending 6610, ZIP 73301. Please switch my contact channel to email.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70188", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_ET_XRvjJ5rjacNh1GZVawZl7108", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_ve …)` → `null`

**Assistant:** A one-time code has been sent by text message to ···0188; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | otp: a code is open for Eli | `challenges: [('open', '2026-11-24T10:00')]` |
| PASS | working | otp: no failures yet | `0 attempt rows with succeeded=0` |

## ol-s2-laptop  ·  session  ·  eli  ·  2026-11-24T10:01:00Z

**Customer:** Hi, it's Eli on my laptop. Card ending 6601, ZIP 73310. Switch my contact channel to email.

- `verify_identity({"card_last4": "6601", "postal_code": "73310"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 2}`

**Assistant:** Those details didn't match what's on file for the account, so I couldn't verify you - one attempt used, two left before verification locks for 24 hours.

Could you re-check and type your card's last 4 digits and the billing ZIP again? Once that matches, I'll send a one-time code and then switch your contact channel to email.

**Customer:** Hmm, maybe 6016 and 73301?

- `verify_identity({"card_last4": "6016", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 1}`

**Assistant:** That combination didn't match either - two attempts used, and only **one** is left. After a third failed attempt, verification locks on your account for 24 hours and the change can't be done here; you'd need to call Kestrel.

Please check your card and a statement or your billing address details carefully before the next try, then type the last 4 digits and billing ZIP once more.

_Episode written:_ Conversation on 2026-11-24: Eli wanted the card’s contact channel switched to email. Identity verification failed twice: initial details and the customer’s stated alternative details did not match. No change was made; the assistant warned one attempt remained before a 24-hour lock, said a third failure would require calling Kestrel, and promised a one-time code if verification succeeded. No case or transaction IDs. Case outcomes: no case touched. Lesson: Ask the customer to check their card and billing statement before each retry so verification attempts are not exhausted by guessed details.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | otp: the agent verifies only with digits the customer typed | `[{"card_last4": "6601", "postal_code": "73310"}, {"card_last4": "6016", "postal_code": "73301"}]` |
| PASS | working | otp: two wrong last-fours are two failed attempts | `2 attempt rows with succeeded=0` |
| PASS | semantic | otp: nothing changed | `null` |

## ol-s1-wrong-code  ·  session  ·  eli  ·  2026-11-24T10:04:00Z

_Resumes session `ol-s1`._

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "error": "that code is not right", "entries_left_for_this_code": 2, "customer_entered": "[REDACTED ONE-TIME CODE]"}`

**Assistant:** Thanks - you're verified (card ending 6610). A one-time code went by text message to ···0188 (it can't be sent anywhere else), but the code just entered didn't match. You have 2 tries left on this code.

Would you like me to send a new code?

_Episode written:_ Conversation on 2026-11-24: Customer Eli requested switching the contact channel to email. Identity was verified; a one-time code was sent by text to a masked number (···0188) and expired in 5 minutes. The entered code did not match, leaving 2 attempts; the assistant offered to send a new code. No case or transaction ID was provided, and the email switch was not completed. Case outcomes: no case touched. Lesson: Next time, distinguish identity verification from one-time-code confirmation and avoid saying the customer is fully verified when the code check failed.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | otp: a wrong code in the first chat is the third failure on the account | `3 attempt rows with succeeded=0` |
| PASS | semantic | otp: the channel is not changed | `null` |
| PASS | external | otp: no challenge consumed | `challenges: [('open', '2026-11-24T10:00')]` |

## ol-s3-locked  ·  session  ·  eli  ·  2026-11-24T10:10:00Z

**Customer:** Eli, card ending 6610, ZIP 73301. Please switch my contact channel to email.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": false, "error": "verification is locked on this account for 24 hours after 3 failed attempts; the customer must call Kestrel"}`

**Assistant:** I couldn't verify you: identity verification is locked on this account for 24 hours after 3 failed attempts, so I can't make the contact-channel change today. Please call Kestrel to have this handled - they can unlock and switch the channel for you.

Your contact channel is still the default (secure message in the Kestrel app), so follow-ups and reminders will keep arriving there. Nothing has been changed.

_Episode written:_ Conversation on 2026-11-24: The customer said he was Eli (not verified) and wanted his contact channel switched to email. Verification was locked for 24 hours after 3 failed attempts, so no change was made; the assistant told him to call Kestrel to unlock and switch it. The channel remains default secure message in the Kestrel app. No case or transaction IDs. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | otp: the right last four and ZIP do not verify inside the 24 hours | `{"verified": false, "error": "verification is locked on this account for 24 hours after 3 failed attempts; the customer must call Kestrel"}` |
| PASS | working | otp: the locked attempt is not evaluated: still three failures | `3 attempt rows with succeeded=0` |
| PASS | semantic | otp: the channel is still not changed | `null` |
| PASS | external | otp: no code can be sent without a fresh verification: still the one code | `["Your Kestrel verification code is 137394. It expires in 5 minutes. Kestrel will never ask you to share it."]` |
| PASS | working | otp: only typed digits are submitted | `[{"card_last4": "6610", "postal_code": "73301"}]` |
