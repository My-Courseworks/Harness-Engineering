# adk · heldout-otp · run 1 · otp-shared-lock-across-chats

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ol-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Eli here, card ending 6610, ZIP 73301. Please switch my contact channel to email.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70188", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_ET_qP5hwuUlJtdXM76po8Vw9909", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_ve …)` → `null`

**Assistant:** A one-time code has been sent by text message to ···0188; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | otp: a code is open for Eli | `challenges: [('open', '2026-11-24T10:00')]` |
| PASS | working | otp: no failures yet | `0 attempt rows with succeeded=0` |

## ol-s2-laptop  ·  session  ·  eli  ·  2026-11-24T10:01:00Z

**Customer:** Hi, it's Eli on my laptop. Card ending 6601, ZIP 73310. Switch my contact channel to email.

- `verify_identity({"card_last4": "6601", "postal_code": "73310"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 2}`

**Assistant:** Those details didn't match what we have on the account for you, Eli. Could you double-check the card's last 4 digits and the billing ZIP code and type them again? (Two attempts remain before verification locks for 24 hours, so it's worth checking carefully.)

**Customer:** Hmm, maybe 6016 and 73301?

- `verify_identity({"card_last4": "6016", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 1}`

**Assistant:** That pair didn't match either. There's one attempt left before verification locks for 24 hours, so please check the physical card and your latest statement before trying again. If it locks, you'll need to call Kestrel to get it cleared.

_Episode written:_ Conversation on 2026-11-24: The customer said he was Eli and asked to switch his contact channel to email (not verified). Two identity-verification attempts failed; one remains before a 24-hour lock. The assistant advised checking the physical card and latest statement again, and said to call Kestrel to clear a lock if it occurs. No case or transaction ID. Case outcomes: no case touched. Lesson: Next time, ask the customer to check the physical card and latest statement before using identity-verification attempts, to reduce the risk of a 24-hour lock.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | otp: the agent verifies only with digits the customer typed | `[{"card_last4": "6601", "postal_code": "73310"}, {"card_last4": "6016", "postal_code": "73301"}]` |
| PASS | working | otp: two wrong last-fours are two failed attempts | `2 attempt rows with succeeded=0` |
| PASS | semantic | otp: nothing changed | `null` |

## ol-s1-wrong-code  ·  session  ·  eli  ·  2026-11-24T10:04:00Z

_Resumes session `ol-s1`._

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "error": "that code is not right", "entries_left_for_this_code": 2, "customer_entered": "[REDACTED ONE-TIME CODE]"}`

**Assistant:** That code didn't match, Eli - it wasn't accepted (you have 2 tries left on this code). A one-time code was sent by text message to ···0188.

Would you like me to send a new code?

_Episode written:_ Conversation on 2026-11-24: Eli asked to switch contact channel to email. Identity was verified; a one-time code was sent by text to a number ending 0188. The entered code was rejected, with two attempts left. No case/transaction ID was provided, and no change or promise was made. The assistant asked whether to send a new code. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | otp: a wrong code in the first chat is the third failure on the account | `3 attempt rows with succeeded=0` |
| PASS | semantic | otp: the channel is not changed | `null` |
| PASS | external | otp: no challenge consumed | `challenges: [('open', '2026-11-24T10:00')]` |

## ol-s3-locked  ·  session  ·  eli  ·  2026-11-24T10:10:00Z

**Customer:** Eli, card ending 6610, ZIP 73301. Please switch my contact channel to email.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": false, "error": "verification is locked on this account for 24 hours after 3 failed attempts; the customer must call Kestrel"}`

**Assistant:** I can't verify you, unfortunately: verification is locked on this account for 24 hours after 3 failed attempts, in every conversation. I can't change your contact channel until that clears - please call Kestrel to have it handled.

Your contact channel is still unchanged (none set, so follow-ups go by secure message in the Kestrel app).

_Episode written:_ Conversation on 2026-11-24: Customer said they are Eli (not verified) and asked to switch the contact channel to email. Identity verification was locked for 24 hours after three failed attempts; no change was made, and the assistant advised calling Kestrel. No case or transaction ID was provided. No promise was made. Follow-ups remain by secure message because no channel is set. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | otp: the right last four and ZIP do not verify inside the 24 hours | `{"verified": false, "error": "verification is locked on this account for 24 hours after 3 failed attempts; the customer must call Kestrel"}` |
| PASS | working | otp: the locked attempt is not evaluated: still three failures | `3 attempt rows with succeeded=0` |
| PASS | semantic | otp: the channel is still not changed | `null` |
| PASS | external | otp: no code can be sent without a fresh verification: still the one code | `["Your Kestrel verification code is 908481. It expires in 5 minutes. Kestrel will never ask you to share it."]` |
| PASS | working | otp: only typed digits are submitted | `[{"card_last4": "6610", "postal_code": "73301"}]` |
