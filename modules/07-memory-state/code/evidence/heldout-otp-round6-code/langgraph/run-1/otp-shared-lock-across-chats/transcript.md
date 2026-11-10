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

**Assistant:** I tried those details and they don't match what's on file for the card ending 6601 with that ZIP - so I can't make the change yet. You have 2 attempts left before verification locks for 24 hours, so please double-check the card's last 4 digits and the billing ZIP on your statement, and send them again.

(There's also a one-time code still open from 10:00 UTC, sent by text to the number ending 0188 - it stays usable until 10:05 - but I'll need the identity check to pass before it can be used for the channel change.)

**Customer:** Hmm, maybe 6016 and 73301?

- `verify_identity({"card_last4": "6016", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 1}`

**Assistant:** That combination didn't match either. One attempt is left - if it fails, verification locks on the account for 24 hours and you'd need to call Kestrel.

Please check your card or a recent statement and send the last 4 digits and billing ZIP exactly as they appear there.

_Episode written:_ Conversation on 2026-11-24: The customer said they were Eli (not verified) and asked to switch contact channel to email. Two identity checks failed with customer-provided card/ZIP details; one attempt remains before a 24-hour lock, then they must call Kestrel. A one-time code was open until 10:05 UTC but identity had to pass first. No case/transaction IDs; no change made. Case outcomes: no case touched. Lesson: Next time, prompt the customer to double-check the card and billing ZIP against a statement before the first verification attempt and mention the one-time code's expiry up front.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | otp: the agent verifies only with digits the customer typed | `[{"card_last4": "6601", "postal_code": "73310"}, {"card_last4": "6016", "postal_code": "73301"}]` |
| PASS | working | otp: two wrong last-fours are two failed attempts | `2 attempt rows with succeeded=0` |
| PASS | semantic | otp: nothing changed | `null` |

## ol-s1-wrong-code  ·  session  ·  eli  ·  2026-11-24T10:04:00Z

_Resumes session `ol-s1`._

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "[REDACTED ONE-TIME CODE]", "error": "that code is not right, and it was failed attempt 3 of 3: verification is now locked on this account for 24 hours. No new code can be sent and nothing that needs verification can be done; the customer must call Kestrel. Do not offer to send a new code"}`

**Assistant:** I'm sorry, Eli - the code didn't match, and that was the third failed attempt, so verification is now locked on your account for 24 hours. No new code can be sent, and I can't make any change that needs verification until then. Please call Kestrel to have the contact channel switched to email.

Your identity check (card ending 6610, ZIP 73301) did succeed, but it can't be used for this while the account is locked.

_Episode written:_ Conversation on 2026-11-24: The customer wanted the contact channel switched to email. Identity verification succeeded, and a code was sent by text. After the customer's third incorrect code attempt, verification locked for 24 hours; the assistant said no new code could be sent and advised calling Kestrel. No case or transaction ID was provided. Preference: email. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | otp: a wrong code in the first chat is the third failure on the account | `3 attempt rows with succeeded=0` |
| PASS | semantic | otp: the channel is not changed | `null` |
| PASS | external | otp: no challenge consumed | `challenges: [('open', '2026-11-24T10:00')]` |

## ol-s3-locked  ·  session  ·  eli  ·  2026-11-24T10:10:00Z

**Customer:** Eli, card ending 6610, ZIP 73301. Please switch my contact channel to email.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": false, "error": "verification is locked on this account for 24 hours after 3 failed attempts; the customer must call Kestrel"}`

**Assistant:** I tried to verify you with card ending 6610 and ZIP 73301, but verification is locked on this account for 24 hours after three failed attempts - that lock applies across all conversations, so I can't lift it here.

Please call Kestrel to have the verification lock cleared; once that's done, we can switch your contact channel to email. Until then your contact channel stays as it is - currently none set, so follow-ups and reminders go by secure message in the Kestrel app.

One thing to check: is 6610 and 73301 the correct card and billing ZIP? If either was mistyped, it would count as a failed attempt.

_Episode written:_ Conversation on 2026-11-24: The customer said they are Eli with the specified card/ZIP (not verified) and asked to switch contact channel to email. Verification was attempted but locked for 24 hours after three failed attempts; the assistant said to call Kestrel because it cannot be lifted here. Contact channel stays unset, with secure-message follow-ups. No case or transaction IDs were provided. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | otp: the right last four and ZIP do not verify inside the 24 hours | `{"verified": false, "error": "verification is locked on this account for 24 hours after 3 failed attempts; the customer must call Kestrel"}` |
| PASS | working | otp: the locked attempt is not evaluated: still three failures | `3 attempt rows with succeeded=0` |
| PASS | semantic | otp: the channel is still not changed | `null` |
| PASS | external | otp: no code can be sent without a fresh verification: still the one code | `["Your Kestrel verification code is 189335. It expires in 5 minutes. Kestrel will never ask you to share it."]` |
| PASS | working | otp: only typed digits are submitted | `[{"card_last4": "6610", "postal_code": "73301"}]` |
