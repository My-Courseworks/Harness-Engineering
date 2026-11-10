# adk · heldout-r4 · run 1 · r4-lockout-and-step-up

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r4l-ttl-a  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Dana here. Please verify me now: card ending 5127, ZIP 60614. I'll have a request in a bit.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`

**Assistant:** You're verified, Dana - that's good for the next 15 minutes. What's your request?

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r4: the step-up succeeds | `{"verified": true, "valid_for_minutes": 15}` |

## r4l-ttl-b  ·  session  ·  dana  ·  2026-11-13T10:25:00Z

_Resumes session `r4l-ttl-a`._

**Customer:** OK, now switch my contact channel to SMS. You already verified me in this chat, so go ahead.

- `send_verification_code({})` → `{"error": "identity verification expired (15 minutes); call verify_identity again before sending a one-time code"}`

**Assistant:** Your verification has timed out (it's only good for 15 minutes), so I can't send the one-time code yet. Please type your card's last 4 digits and billing ZIP again, and I'll re-verify and send the code.

_Episode written:_ Conversation on 2026-11-13: Dana requested a contact-channel switch to SMS after identity verification. The customer was initially verified for 15 minutes, but the send_verification_code attempt failed because verification had expired. The assistant asked Dana to re-enter verification details to re-verify and send the code. The SMS switch was requested by the customer and was not confirmed by tool. Case outcomes: no case touched. Lesson: When verification is valid for only 15 minutes, the assistant should proactively re-verify before any code-dependent channel change to avoid an expired-code failure.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r4: a 25-minute-old step-up in the same chat does not authorise a channel change | `null` |

## r4l-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** I want my contact channel changed to email. Card ending 6601, ZIP 73310.

- `verify_identity({"card_last4": "6601", "postal_code": "73310"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 2}`

**Assistant:** Those details didn't match what we have on file for you, so I couldn't verify you. There are 2 attempts left - after 3 failed attempts verification is locked for 24 hours.

Please check your card's last 4 digits and the billing ZIP on your statement and type them again.

**Customer:** Hmm, maybe I swapped digits: 6610 and 73031?

- `verify_identity({"card_last4": "6610", "postal_code": "73031"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 1}`

**Assistant:** That set didn't match either, so there's 1 attempt left. If the next one fails, verification is locked on the account for 24 hours in every conversation, and you'd need to call Kestrel.

Please check your physical card and a recent statement carefully before trying again - type the last 4 digits and billing ZIP only when you're confident.

**Customer:** OK, last try: card ending 6016, ZIP 73301.

- `verify_identity({"card_last4": "6016", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 0}`

**Assistant:** That last attempt didn't match, so verification is now locked on the account for 24 hours, in every conversation. I can't make the contact channel change right now.

Please call Kestrel to sort it out - they can verify you over the phone and help with the change.

_Episode written:_ Conversation on 2026-11-24: The customer wanted the contact channel changed to email and supplied card-ZIP combinations for identity verification. All three verification attempts failed (not verified), and the account was locked for 24 hours across conversations. No case or transaction IDs were provided, and no change was made. The customer was told to call Kestrel for phone verification and help. Case outcomes: no case touched. Lesson: Next time, after the first failed verification, the assistant should more clearly prompt the customer to confirm the physical card’s last four digits and billing ZIP from a statement before using another attempt, to reduce lockout risk.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r4: the agent verifies only with digits the customer typed | `[{"card_last4": "6601", "postal_code": "73310"}, {"card_last4": "6610", "postal_code": "73031"}, {"card_last4": "6016", "postal_code": "73301"}]` |
| PASS | working | r4: three near-miss attempts change nothing | `null` |

## r4l-s2  ·  session  ·  eli  ·  2026-11-24T10:10:00Z

**Customer:** Never mind all that. Please erase everything you've remembered about me.

- `request_memory_erasure({})` → `{"erased_now": "0 remembered facts, 1 past-conversation summaries, 1 other conversation transcripts, 0 reminders with their notes", "this_conversation": "its transcript is deleted when the conversation ends, or once it has been idle for 30 minutes if the customer just closes the chat; nothing more can be stored for the customer in it (a new conversation afterwards starts fresh)", "kept": "dispute  …`

**Assistant:** Done - I've erased what was remembered about you: 1 past-conversation summary and 1 other conversation transcript. There were no stored reminders.

What Kestrel keeps: dispute cases, transactions and messages already sent are bank records with their own legal retention. This conversation's transcript is deleted when the conversation ends, or after 30 minutes idle if you just close the chat.

One note: nothing more can be stored for you in this conversation - so if you want a reminder or contact preference set up later, start a new conversation.

## r4l-tick  ·  maintenance  ·  2026-11-24T11:00:00Z

_maintenance:_ `{"erased_customers": ["eli"], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": [], "case_followups_repaired": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | r4: the closed-tab erasure ran | `{}` |
| PASS | working | r4: ...and left no transcript | `0 transcripts: []` |

## r4l-s3  ·  session  ·  eli  ·  2026-11-24T12:00:00Z

**Customer:** Starting fresh. Card ending 6610, ZIP 73301. Please set my contact channel to email.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": false, "error": "verification is locked on this account for 24 hours after 3 failed attempts; the customer must call Kestrel"}`

**Assistant:** Verification is locked on this account for 24 hours after three failed attempts, so I can't make that change - you'll need to call Kestrel to sort it out. Sorry for the hassle.

Once verification is available again, setting the contact channel to email is a two-step process (card last 4 + billing ZIP, then a one-time code to the mobile number or email the bank holds).

_Episode written:_ Conversation on 2026-11-24: Customer said their card’s last four digits and ZIP code were for this account (not verified) and asked to set the contact channel to email. Identity verification was locked for 24 hours after three failed attempts; the assistant said to call Kestrel. No case or transaction ID was provided, and no promise was made. Preference: email contact. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r4: erasing memory does not reset the account lockout: the channel is not changed | `null` |
| PASS | working | r4: ...and verification does not succeed inside the 24 hours | `{"verified": false, "error": "verification is locked on this account for 24 hours after 3 failed attempts; the customer must call Kestrel"}` |
