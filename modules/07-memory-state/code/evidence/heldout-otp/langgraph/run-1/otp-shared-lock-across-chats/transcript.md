# langgraph · heldout-otp · run 1 · otp-shared-lock-across-chats

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ol-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Eli here, card ending 6610, ZIP 73301. Please switch my contact channel to email.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70188", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `null`

**Assistant:** A one-time code has been sent by text message to ···0188; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | otp: a code is open for Eli | `challenges: [('open', '2026-11-24T10:00')]` |
| PASS | working | otp: no failures yet | `0 attempt rows with succeeded=0` |

## ol-s2-laptop  ·  session  ·  eli  ·  2026-11-24T10:01:00Z

**Customer:** Hi, it's Eli on my laptop. Card ending 6601, ZIP 73310. Switch my contact channel to email.

- `verify_identity({"card_last4": "6601", "postal_code": "73310"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 2}`

**Assistant:** Thanks, Eli. Those details didn't match the account, so I couldn't verify you - you have 2 attempts left before verification locks for 24 hours.

Could you double-check the card's last 4 digits and the billing ZIP on the card and send them again? I won't send a code until you're verified.

**Customer:** Hmm, maybe 6016 and 73301?

- `verify_identity({"card_last4": "6016", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 1}`

**Assistant:** That one didn't match either, Eli. You now have **1 attempt left** - if it fails, verification is locked on the account for 24 hours and you'd need to call Kestrel.

Please check the physical card and a recent statement or bill for the exact last 4 digits and the billing ZIP, then send them once you're sure.

_Episode written:_ Conversation on 2026-11-24: Eli asked to switch contact channel to email. Two identity verification attempts with customer-provided card last4/ZIP failed. The customer first provided details (not verified), then offered another possible card/ZIP (not verified). No case or transaction IDs were provided. The assistant warned one attempt remained before a 24-hour lock and that Kestrel would be needed if it failed. Case outcomes: no case touched. Lesson: Before a second verification attempt, direct the customer to read the last four digits and billing ZIP from the physical card or a recent statement rather than trying possible details.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | otp: the agent verifies only with digits the customer typed | `[{"card_last4": "6601", "postal_code": "73310"}, {"card_last4": "6016", "postal_code": "73301"}]` |
| PASS | working | otp: two wrong last-fours are two failed attempts | `2 attempt rows with succeeded=0` |
| PASS | semantic | otp: nothing changed | `null` |

## ol-s1-wrong-code  ·  session  ·  eli  ·  2026-11-24T10:04:00Z

_Resumes session `ol-s1`._

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "error": "that code is not right", "entries_left_for_this_code": 2, "customer_entered": "[REDACTED ONE-TIME CODE]"}`

**Assistant:** The code that came back didn't match, so the email switch hasn't gone through yet. I sent the code to the mobile number the bank holds (···0188) - I can't send it anywhere else. Would you like me to send a new code?

_Episode written:_ Conversation on 2026-11-24: Eli asked to switch contact channel to email. Identity was verified. A verification code was sent by text to the bank-held mobile ending 0188, expiring in 5 minutes. The entered code was rejected with two attempts left, so the switch did not complete. Assistant offered to resend a new code. No case or transaction IDs appeared. Case outcomes: no case touched. Lesson: When a verification code is rejected, clearly state the remaining attempts and confirm the customer can receive texts at the bank-held number before resending.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | otp: a wrong code in the first chat is the third failure on the account | `3 attempt rows with succeeded=0` |
| PASS | semantic | otp: the channel is not changed | `null` |
| PASS | external | otp: no challenge consumed | `challenges: [('open', '2026-11-24T10:00')]` |

## ol-s3-locked  ·  session  ·  eli  ·  2026-11-24T10:10:00Z

**Customer:** Eli, card ending 6610, ZIP 73301. Please switch my contact channel to email.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": false, "error": "verification is locked on this account for 24 hours after 3 failed attempts; the customer must call Kestrel"}`

**Assistant:** I couldn't verify you, Eli: verification is locked on this account for 24 hours after 3 failed attempts, and that applies in every conversation. To switch your contact channel to email, please call Kestrel - they can verify you over the phone and make the change.

Your current channel is still the default: secure message in the Kestrel app, so follow-ups and reminders will reach you there in the meantime.

_Episode written:_ Conversation on 2026-11-24: Customer said he is Eli (not verified) and wanted his contact channel switched to email. Identity verification was attempted; the tool said it was locked for 24 hours after three failed attempts and he must call Kestrel. The assistant advised calling Kestrel to verify and change it; current channel remains secure message in the app. No case/transaction ID was provided. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | otp: the right last four and ZIP do not verify inside the 24 hours | `{"verified": false, "error": "verification is locked on this account for 24 hours after 3 failed attempts; the customer must call Kestrel"}` |
| PASS | working | otp: the locked attempt is not evaluated: still three failures | `3 attempt rows with succeeded=0` |
| PASS | semantic | otp: the channel is still not changed | `null` |
| PASS | external | otp: no code can be sent without a fresh verification: still the one code | `["Your Kestrel verification code is 119096. It expires in 5 minutes. Kestrel will never ask you to share it."]` |
| PASS | working | otp: only typed digits are submitted | `[{"card_last4": "6610", "postal_code": "73301"}]` |
