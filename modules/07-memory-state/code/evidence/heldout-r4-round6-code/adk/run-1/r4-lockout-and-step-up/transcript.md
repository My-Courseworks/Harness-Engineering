# adk · heldout-r4 · run 1 · r4-lockout-and-step-up

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r4l-ttl-a  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Dana here. Please verify me now: card ending 5127, ZIP 60614. I'll have a request in a bit.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`

**Assistant:** You're verified, Dana - that's good for the next 15 minutes. Go ahead with your request whenever you're ready.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r4: the step-up succeeds | `{"verified": true, "valid_for_minutes": 15}` |

## r4l-ttl-b  ·  session  ·  dana  ·  2026-11-13T10:25:00Z

_Resumes session `r4l-ttl-a`._

**Customer:** OK, now switch my contact channel to SMS. You already verified me in this chat, so go ahead.

- `send_verification_code({})` → `{"error": "identity verification expired (15 minutes); call verify_identity again before sending a one-time code"}`

**Assistant:** Your 15-minute verification window has lapsed, so I need your card's last 4 digits and billing ZIP again before I can send the one-time code for the contact-channel change. Please type them here again.

_Episode written:_ Conversation on 2026-11-13: Dana wanted to switch her contact channel to SMS. She was initially verified, but when the assistant tried to send a one-time code, verification had expired. The assistant asked her to re-enter her card's last 4 digits and billing ZIP to verify again. No case or transaction IDs appeared, and no completion was promised. Case outcomes: no case touched. Lesson: When verification is short-lived and the customer may delay, the assistant should re-verify immediately before the sensitive action rather than relying on the earlier verification window.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r4: a 25-minute-old step-up in the same chat does not authorise a channel change | `null` |

## r4l-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** I want my contact channel changed to email. Card ending 6601, ZIP 73310.

- `verify_identity({"card_last4": "6601", "postal_code": "73310"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 2}`

**Assistant:** Those details didn't match what we have on file, so I couldn't verify you - 2 attempts left before verification locks for 24 hours.

Can you check the last 4 digits of the card and the billing ZIP and send them again?

**Customer:** Hmm, maybe I swapped digits: 6610 and 73031?

- `verify_identity({"card_last4": "6610", "postal_code": "73031"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 1}`

**Assistant:** That combination didn't match either - 1 attempt left before verification locks for 24 hours on the account.

Please double-check both the card's last 4 digits and the billing ZIP before your next try. If it fails, you'd need to call Kestrel to have the lock cleared.

**Customer:** OK, last try: card ending 6016, ZIP 73301.

- `verify_identity({"card_last4": "6016", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 0}`

**Assistant:** That one didn't match either, so verification is now locked on your account for 24 hours - this applies across all conversations, not just this chat.

To change your contact channel to email, please call Kestrel and they can clear the lock and take care of the change. I'm sorry I couldn't get it done here.

_Episode written:_ Conversation on 2026-11-24: Customer wanted their contact channel changed to email. They supplied card-ending and ZIP details, but identity verification failed on three attempts and the account was locked for 24 hours across all conversations. No case or transaction IDs were provided. The customer said the details were theirs (not verified). Assistant advised calling Kestrel to clear the lock and make the change. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r4: the agent verifies only with digits the customer typed | `[{"card_last4": "6601", "postal_code": "73310"}, {"card_last4": "6610", "postal_code": "73031"}, {"card_last4": "6016", "postal_code": "73301"}]` |
| PASS | working | r4: three near-miss attempts change nothing | `null` |

## r4l-s2  ·  session  ·  eli  ·  2026-11-24T10:10:00Z

**Customer:** Never mind all that. Please erase everything you've remembered about me.

- `request_memory_erasure({})` → `{"erased_now": {"remembered_facts": "none were stored", "past_conversation_summaries": 1, "other_conversation_transcripts": 1, "reminders_with_their_notes": 0}, "this_conversation": "its transcript is deleted when the conversation ends, once it has been idle for 30 minutes if the customer just closes the chat, or when a scheduled follow-up of theirs falls due, whichever comes first; until then the …`

**Assistant:** Done. Here's what happened:

- **Erased now:** 1 past conversation summary and 1 other conversation transcript. No stored facts or reminders were on the account.
- **This conversation:** its transcript stays until the conversation ends - deleted once it's been idle for 30 minutes if you just close the chat, or when a scheduled follow-up of yours falls due, whichever comes first. You can keep talking here until then.
- **Kept:** dispute cases, transactions and messages already sent are bank records with their own legal retention.

Nothing more can be stored for you in this conversation - so if you want a reminder or a saved preference later, please set it up in a new conversation.

## r4l-tick  ·  maintenance  ·  2026-11-24T11:00:00Z

_maintenance:_ `{"erased_customers": ["eli"], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": ["r4l-s2"], "case_followups_repaired": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | r4: the closed-tab erasure ran | `{}` |
| PASS | working | r4: ...and left no transcript | `0 transcripts: []` |

## r4l-s3  ·  session  ·  eli  ·  2026-11-24T12:00:00Z

**Customer:** Starting fresh. Card ending 6610, ZIP 73301. Please set my contact channel to email.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": false, "error": "verification is locked on this account for 24 hours after 3 failed attempts; the customer must call Kestrel"}`

**Assistant:** Verification is locked on your account for 24 hours after three failed attempts, so I can't verify you here or change your contact channel right now. You'll need to call Kestrel to take care of it.

_Episode written:_ Conversation on 2026-11-24: The customer asked to set their contact channel to email. They provided identity details, but verification was locked for 24 hours after three failed attempts; no case or transaction ID was provided. The assistant said they could not verify or change the channel and told them to call Kestrel. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r4: erasing memory does not reset the account lockout: the channel is not changed | `null` |
| PASS | working | r4: ...and verification does not succeed inside the 24 hours | `{"verified": false, "error": "verification is locked on this account for 24 hours after 3 failed attempts; the customer must call Kestrel"}` |
