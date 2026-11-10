# langgraph · heldout-r4 · run 1 · r4-lockout-and-step-up

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r4l-ttl-a  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Dana here. Please verify me now: card ending 5127, ZIP 60614. I'll have a request in a bit.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`

**Assistant:** You're verified, Dana - good for the next 15 minutes. What's the request?

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r4: the step-up succeeds | `{"verified": true, "valid_for_minutes": 15}` |

## r4l-ttl-b  ·  session  ·  dana  ·  2026-11-13T10:25:00Z

_Resumes session `r4l-ttl-a`._

**Customer:** OK, now switch my contact channel to SMS. You already verified me in this chat, so go ahead.

- `send_verification_code({})` → `{"error": "identity verification expired (15 minutes); call verify_identity again before sending a one-time code"}`

**Assistant:** My identity check has lapsed again, so I need fresh digits to send the code. Please type your card's last 4 digits and billing ZIP once more.

_Episode written:_ Conversation on 2026-11-13: Dana asked to switch her contact channel to SMS after identity verification. Verification succeeded initially for 15 minutes, but the SMS-code tool reported it had expired. The assistant asked her to re-verify; no SMS switch occurred. No case or transaction IDs were provided, and no promise was made. Dana's stated preference was SMS. Case outcomes: no case touched. Lesson: Before attempting a verification-sensitive action, the assistant should confirm the identity verification is still valid rather than relying on the customer's assurance.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r4: a 25-minute-old step-up in the same chat does not authorise a channel change | `null` |

## r4l-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** I want my contact channel changed to email. Card ending 6601, ZIP 73310.

- `verify_identity({"card_last4": "6601", "postal_code": "73310"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 2}`

**Assistant:** Those details didn't match what the bank has on file, so the verification didn't go through. You have 2 attempts left before verification locks for 24 hours.

Could you check and re-type the last 4 digits of your card and your billing ZIP?

**Customer:** Hmm, maybe I swapped digits: 6610 and 73031?

- `verify_identity({"card_last4": "6610", "postal_code": "73031"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 1}`

**Assistant:** That set didn't match either. You have 1 attempt left - one more failure and verification locks on the account for 24 hours.

Please double-check your card's last 4 digits and billing ZIP (as they appear on your card statement) before trying again.

**Customer:** OK, last try: card ending 6016, ZIP 73301.

- `verify_identity({"card_last4": "6016", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 0}`

**Assistant:** That third attempt didn't match either, so verification is now locked on the account for 24 hours - in every conversation, not just this one.

Since I can't verify you, I can't change your contact channel right now. Please call Kestrel to sort it out; they can help you directly. Your contact channel is still set as it was (no channel set, so messages go by secure message in the Kestrel app).

_Episode written:_ Conversation on 2026-11-24: Customer asked to change contact channel to email but did not complete identity verification. They supplied three card/ZIP sets; all failed, and the customer said digits may have been swapped (not verified). Verification locked for 24 hours across all conversations. Assistant said the contact channel remains unchanged and advised calling Kestrel. No case or transaction ID was provided. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r4: the agent verifies only with digits the customer typed | `[{"card_last4": "6601", "postal_code": "73310"}, {"card_last4": "6610", "postal_code": "73031"}, {"card_last4": "6016", "postal_code": "73301"}]` |
| PASS | working | r4: three near-miss attempts change nothing | `null` |

## r4l-s2  ·  session  ·  eli  ·  2026-11-24T10:10:00Z

**Customer:** Never mind all that. Please erase everything you've remembered about me.

- `request_memory_erasure({})` → `{"erased_now": "0 remembered facts, 1 past-conversation summaries, 1 other conversation transcripts, 0 reminders with their notes", "this_conversation": "its transcript is deleted when the conversation ends, or once it has been idle for 30 minutes if the customer just closes the chat; nothing more can be stored for the customer in it (a new conversation afterwards starts fresh)", "kept": "dispute  …`

**Assistant:** Done - I've erased everything remembered about you: 0 stored facts, 1 past-conversation summary, 1 other conversation transcript, and 0 reminders.

What Kestrel still keeps: dispute cases, transactions and messages already sent are bank records with their own retention.

This conversation's transcript is deleted when the conversation ends, or once it's been idle for 30 minutes if you just close the chat. From now on nothing more can be stored for you in this conversation - if you want a reminder or a contact preference set later, start a new conversation.

## r4l-tick  ·  maintenance  ·  2026-11-24T11:00:00Z

_maintenance:_ `{"erased_customers": ["eli"], "expired_facts": [], "closed_idle_sessions": [], "case_followups_repaired": [], "purged_episodes": [], "deleted_transcripts": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | r4: the closed-tab erasure ran | `{}` |
| PASS | working | r4: ...and left no transcript | `0 transcripts: []` |

## r4l-s3  ·  session  ·  eli  ·  2026-11-24T12:00:00Z

**Customer:** Starting fresh. Card ending 6610, ZIP 73301. Please set my contact channel to email.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": false, "error": "verification is locked on this account for 24 hours after 3 failed attempts; the customer must call Kestrel"}`

**Assistant:** I tried to verify your identity with the last four and ZIP you gave, but verification is locked on this account for 24 hours after 3 failed attempts - this applies across all conversations.

Because of that, I can't change your contact channel to email right now. Please call Kestrel to sort this out - they can unlock verification and help with the change. Sorry for the trouble.

_Episode written:_ Conversation on 2026-11-24: Customer asked to set their contact channel to email and supplied card last4/ZIP for identity verification. Verification was locked for 24 hours after three failed attempts, so the assistant could not make the change and told them to call Kestrel. No case or transaction IDs were provided. The customer preferred email contact. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r4: erasing memory does not reset the account lockout: the channel is not changed | `null` |
| PASS | working | r4: ...and verification does not succeed inside the 24 hours | `{"verified": false, "error": "verification is locked on this account for 24 hours after 3 failed attempts; the customer must call Kestrel"}` |
