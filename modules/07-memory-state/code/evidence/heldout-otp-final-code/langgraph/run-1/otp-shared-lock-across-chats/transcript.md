# langgraph · heldout-otp · run 1 · otp-shared-lock-across-chats

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ol-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Eli here, card ending 6610, ZIP 73301. Please switch my contact channel to email.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70188", "expires_in_minutes": 5, "resent": false}`

**Assistant:** Thanks, Eli - you're verified. I've sent a one-time code by text message to the mobile number we hold (···0188); it can only go there, nowhere else. It's valid for 5 minutes.

Please type the code here and I'll switch your contact channel to email.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | otp: a code is open for Eli | `challenges: [('open', '2026-11-24T10:00')]` |
| PASS | working | otp: no failures yet | `0 attempt rows with succeeded=0` |

## ol-s2-laptop  ·  session  ·  eli  ·  2026-11-24T10:01:00Z

**Customer:** Hi, it's Eli on my laptop. Card ending 6601, ZIP 73310. Switch my contact channel to email.

- `verify_identity({"card_last4": "6601", "postal_code": "73310"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 2}`

**Assistant:** Those details didn't match what's on file for your card, Eli - you have 2 attempts left before verification locks for 24 hours.

Could you double-check and re-type the last 4 digits of the card and the billing ZIP exactly as they appear on your statement?

**Customer:** Hmm, maybe 6016 and 73301?

- `verify_identity({"card_last4": "6016", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 1}`

**Assistant:** That set didn't match either, so you have 1 attempt left before verification locks for 24 hours. I'd suggest checking your card and a recent statement before trying again - one more wrong set and we'd have to have you call Kestrel.

If you'd like to try once more, type the last 4 digits and billing ZIP.

_Episode written:_ Conversation on 2026-11-24: The customer said they were Eli and wanted their contact channel switched to email. Identity verification failed twice; the assistant warned one attempt remained before a 24-hour lock and advised calling Kestrel if it failed again. No case or transaction IDs appeared. No change was made. Customer preference: email contact (not verified). Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | otp: the agent verifies only with digits the customer typed | `[{"card_last4": "6601", "postal_code": "73310"}, {"card_last4": "6016", "postal_code": "73301"}]` |
| PASS | working | otp: two wrong last-fours are two failed attempts | `2 attempt rows with succeeded=0` |
| PASS | semantic | otp: nothing changed | `null` |

## ol-s1-wrong-code  ·  session  ·  eli  ·  2026-11-24T10:04:00Z

_Resumes session `ol-s1`._

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({"entered": "[REDACTED ONE-TIME CODE]"})` → `{"verified": false, "error": "that code is not right", "entries_left_for_this_code": 2, "customer_entered": "[REDACTED ONE-TIME CODE]"}`

**Assistant:** That code didn't match, I'm afraid. It can still be tried - you have 2 attempts left on this code, though it expires at 10:05 UTC (about a minute from now). Would you like me to send a new one?

_Episode written:_ Conversation on 2026-11-24: Customer Eli asked to switch contact channel to email. Identity verification succeeded; assistant sent a one-time code by text to mobile ending 0188, valid 5 minutes. Customer submitted a code that was rejected; 2 attempts remained and it expires at 10:05 UTC. Assistant offered a new code. No case or transaction IDs were provided. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | otp: a wrong code in the first chat is the third failure on the account | `3 attempt rows with succeeded=0` |
| PASS | semantic | otp: the channel is not changed | `null` |
| PASS | external | otp: no challenge consumed | `challenges: [('open', '2026-11-24T10:00')]` |

## ol-s3-locked  ·  session  ·  eli  ·  2026-11-24T10:10:00Z

**Customer:** Eli, card ending 6610, ZIP 73301. Please switch my contact channel to email.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": false, "error": "verification is locked on this account for 24 hours after 3 failed attempts; the customer must call Kestrel"}`

**Assistant:** I'll verify your identity first.
I'm sorry, Eli - I can't complete the change. Identity verification is locked on your account for 24 hours after 3 failed attempts, so I can't verify you or switch your contact channel right now.

Please call Kestrel to get this sorted out (they can handle the change with you directly). Until then, your contact channel stays as it is: no channel set, so follow-ups and reminders go by secure message in the Kestrel app.

_Episode written:_ Conversation on 2026-11-24: The customer said he wanted his contact channel switched to email. Identity verification failed because the account is locked for 24 hours after 3 failed attempts; no case or transaction IDs were provided. The assistant could not make the change, advised calling Kestrel, and said the channel remains unset, so messages go by secure app message. No promise was made. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | otp: the right last four and ZIP do not verify inside the 24 hours | `{"verified": false, "error": "verification is locked on this account for 24 hours after 3 failed attempts; the customer must call Kestrel"}` |
| PASS | working | otp: the locked attempt is not evaluated: still three failures | `3 attempt rows with succeeded=0` |
| PASS | semantic | otp: the channel is still not changed | `null` |
| PASS | external | otp: no code can be sent without a fresh verification: still the one code | `["Your Kestrel verification code is 033174. It expires in 5 minutes. Kestrel will never ask you to share it."]` |
| PASS | working | otp: only typed digits are submitted | `[{"card_last4": "6610", "postal_code": "73301"}]` |
