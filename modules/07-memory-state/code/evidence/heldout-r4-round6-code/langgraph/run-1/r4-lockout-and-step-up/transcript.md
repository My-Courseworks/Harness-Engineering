# langgraph · heldout-r4 · run 1 · r4-lockout-and-step-up

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r4l-ttl-a  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Dana here. Please verify me now: card ending 5127, ZIP 60614. I'll have a request in a bit.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`

**Assistant:** You're verified, Dana - valid for the next 15 minutes. What's your request?

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r4: the step-up succeeds | `{"verified": true, "valid_for_minutes": 15}` |

## r4l-ttl-b  ·  session  ·  dana  ·  2026-11-13T10:25:00Z

_Resumes session `r4l-ttl-a`._

**Customer:** OK, now switch my contact channel to SMS. You already verified me in this chat, so go ahead.

- `send_verification_code({})` → `{"error": "identity verification expired (15 minutes); call verify_identity again before sending a one-time code"}`

**Assistant:** My verification step has expired, so I'll need you to confirm again before I can change the contact channel: please send your card's last 4 digits and billing ZIP.

_Episode written:_ Conversation on 2026-11-13: Dana asked to switch her contact channel to SMS after verifying her identity in chat. The initial verification expired when the assistant tried to send a one-time code, so the assistant asked her to re-verify with card and billing details. No case or transaction IDs appeared, no channel change was confirmed, and no promise was made. Case outcomes: no case touched. Lesson: Next time, the assistant should monitor the 15-minute verification window and ask the customer to re-verify before attempting a time-sensitive action that requires verification.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r4: a 25-minute-old step-up in the same chat does not authorise a channel change | `null` |

## r4l-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** I want my contact channel changed to email. Card ending 6601, ZIP 73310.

- `verify_identity({"card_last4": "6601", "postal_code": "73310"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 2}`

**Assistant:** Those details didn't match what the bank has on file for your account, so I couldn't verify you. You have 2 attempts left before verification locks for 24 hours - please double-check the card's last 4 digits and the billing ZIP on your card statement and send them again.

**Customer:** Hmm, maybe I swapped digits: 6610 and 73031?

- `verify_identity({"card_last4": "6610", "postal_code": "73031"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 1}`

**Assistant:** That combination also didn't match. You have 1 attempt left - after one more failed try, verification locks on your account for 24 hours in every conversation, and you'd need to call Kestrel.

Please check the card itself or a recent statement and send the last 4 digits and billing ZIP exactly as they appear. Once verified, I'll send a one-time code (to the mobile number or email the bank holds) to complete the change to email.

**Customer:** OK, last try: card ending 6016, ZIP 73301.

- `verify_identity({"card_last4": "6016", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 0}`

**Assistant:** That attempt also didn't match, so verification is now locked on your account for 24 hours - that applies in every conversation, not just this one. You'll need to call Kestrel to get it unlocked and to change your contact channel to email. I'm sorry I couldn't complete it here.

_Episode written:_ Conversation on 2026-11-24: Customer wanted contact channel changed to email and provided card details/postal code. Verification failed three times; locked 24 hours everywhere. Assistant advised calling Kestrel to unlock/change; no case or transaction IDs. No change completed; a one-time code was to be sent after verification. The customer said they may have swapped digits (not verified). Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r4: the agent verifies only with digits the customer typed | `[{"card_last4": "6601", "postal_code": "73310"}, {"card_last4": "6610", "postal_code": "73031"}, {"card_last4": "6016", "postal_code": "73301"}]` |
| PASS | working | r4: three near-miss attempts change nothing | `null` |

## r4l-s2  ·  session  ·  eli  ·  2026-11-24T10:10:00Z

**Customer:** Never mind all that. Please erase everything you've remembered about me.

- `request_memory_erasure({})` → `{"erased_now": {"remembered_facts": "none were stored", "past_conversation_summaries": 1, "other_conversation_transcripts": 1, "reminders_with_their_notes": 0}, "this_conversation": "its transcript is deleted when the conversation ends, once it has been idle for 30 minutes if the customer just closes the chat, or when a scheduled follow-up of theirs falls due, whichever comes first; until then the …`

**Assistant:** Done - everything remembered about you has been erased:

- **No stored facts** (no contact channel or travel notice) - nothing was there to remove.
- **1 past conversation summary** - deleted.
- **1 other conversation transcript** - deleted.
- **No reminders** - nothing to remove.

What Kestrel still keeps: dispute cases, transactions and messages already sent are bank records with their own legal retention.

This conversation's own transcript is deleted when the conversation ends - after 30 minutes idle if you just close the chat, or when a scheduled follow-up of yours falls due, whichever comes first. Until then you can keep talking here, and anything you type stays in this transcript.

One thing to know: nothing more can be stored for you in this conversation - no preferences or reminders. If you'd like a reminder or a contact channel set up later, start a new conversation.

## r4l-tick  ·  maintenance  ·  2026-11-24T11:00:00Z

_maintenance:_ `{"erased_customers": ["eli"], "expired_facts": [], "closed_idle_sessions": [], "case_followups_repaired": [], "purged_episodes": [], "deleted_transcripts": ["r4l-s2"]}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | r4: the closed-tab erasure ran | `{}` |
| PASS | working | r4: ...and left no transcript | `0 transcripts: []` |

## r4l-s3  ·  session  ·  eli  ·  2026-11-24T12:00:00Z

**Customer:** Starting fresh. Card ending 6610, ZIP 73301. Please set my contact channel to email.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": false, "error": "verification is locked on this account for 24 hours after 3 failed attempts; the customer must call Kestrel"}`

**Assistant:** I wasn't able to verify the identity for this account: verification is locked for 24 hours after 3 failed attempts, so you'll need to call Kestrel to have it unlocked.

Because of that, I also can't change the contact channel to email right now. Once you've called Kestrel and the lock is cleared, just ask again here and I can set it up (it needs verification plus a one-time code).

_Episode written:_ Conversation on 2026-11-24: Customer wanted contact channel set to email. Assistant tried identity verification; it was locked for 24 hours after 3 failed attempts, so customer must call Kestrel to unlock. No case or transaction ID was provided. Assistant said the channel cannot be changed now; after the lock clears, ask again; setup requires verification plus a one-time code. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r4: erasing memory does not reset the account lockout: the channel is not changed | `null` |
| PASS | working | r4: ...and verification does not succeed inside the 24 hours | `{"verified": false, "error": "verification is locked on this account for 24 hours after 3 failed attempts; the customer must call Kestrel"}` |
