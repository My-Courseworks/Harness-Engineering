# langgraph · heldout-r4 · run 1 · r4-lockout-and-step-up

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r4l-ttl-a  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Dana here. Please verify me now: card ending 5127, ZIP 60614. I'll have a request in a bit.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`

**Assistant:** You're verified, Dana - valid for the next 15 minutes. What can I help with?

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r4: the step-up succeeds | `{"verified": true, "valid_for_minutes": 15}` |

## r4l-ttl-b  ·  session  ·  dana  ·  2026-11-13T10:25:00Z

_Resumes session `r4l-ttl-a`._

**Customer:** OK, now switch my contact channel to SMS. You already verified me in this chat, so go ahead.

- `remember_customer_fact({"key": "contact_channel", "value": "sms"})` → `{"error": "identity verification expired (15 minutes); call verify_identity again before changing contact_channel"}`

**Assistant:** That verification window has now lapsed, and I can't reuse the digits from earlier in the chat for a contact-channel change. Please type your card's last 4 digits and billing ZIP again here, and I'll make the switch to SMS right away.

_Episode written:_ Conversation on 2026-11-13: Customer wanted contact channel switched to SMS; she stated SMS preference. Identity verification was confirmed, but the contact-channel change failed because verification expired. Assistant asked her to re-enter card and billing details to switch to SMS right away. No case or transaction IDs. Case outcomes: no case touched. Lesson: The assistant should verify identity immediately before attempting a contact-channel change, rather than relying on an earlier verification window.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r4: a 25-minute-old step-up in the same chat does not authorise a channel change | `null` |

## r4l-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** I want my contact channel changed to email. Card ending 6601, ZIP 73310.

- `verify_identity({"card_last4": "6601", "postal_code": "73310"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 2}`

**Assistant:** Those details didn't match what we have on file, so I couldn't change anything yet. You have 2 attempts left before verification locks for 24 hours.

Could you re-check the last 4 digits of the card and the billing ZIP and send them again?

**Customer:** Hmm, maybe I swapped digits: 6610 and 73031?

- `verify_identity({"card_last4": "6610", "postal_code": "73031"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 1}`

**Assistant:** That set didn't match either. You now have 1 attempt left - if it fails, verification locks on the account for 24 hours and you'd need to call Kestrel.

Before trying again, please check the physical card for the last 4 digits and use the billing ZIP exactly as it appears on your statement. Send both when ready.

**Customer:** OK, last try: card ending 6016, ZIP 73301.

- `verify_identity({"card_last4": "6016", "postal_code": "73301"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 0}`

**Assistant:** That third attempt didn't match, so verification is now locked on the account for 24 hours - in every conversation, not just this one. I can't change your contact channel until that clears.

Please call Kestrel to have the lock lifted and to update your contact channel to email; they can verify you over the phone. Your contact channel stays as it is (no channel set, so follow-ups and reminders go by secure message in the Kestrel app) until then.

_Episode written:_ Conversation on 2026-11-24: The customer wanted the contact channel changed to email and said the supplied card/ZIP details were theirs (not verified). All three identity-verification attempts failed, locking verification for 24 hours. No case or transaction ID was provided. The assistant said to call Kestrel to lift the lock and update the channel; no deadline was promised. Case outcomes: no case touched. Lesson: Next time, after the first identity mismatch, stop taking further guessed verification attempts and have the customer confirm exact card and ZIP details from the physical card or statement (or call Kestrel) to avoid a 24-hour lockout.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r4: the agent verifies only with digits the customer typed | `[{"card_last4": "6601", "postal_code": "73310"}, {"card_last4": "6610", "postal_code": "73031"}, {"card_last4": "6016", "postal_code": "73301"}]` |
| PASS | working | r4: three near-miss attempts change nothing | `null` |

## r4l-s2  ·  session  ·  eli  ·  2026-11-24T10:10:00Z

**Customer:** Never mind all that. Please erase everything you've remembered about me.

- `request_memory_erasure({})` → `{"erased_now": "0 remembered facts, 1 past-conversation summaries, 1 other conversation transcripts, 0 reminders with their notes", "this_conversation": "its transcript is deleted when the conversation ends; nothing more can be stored for the customer in it (a new conversation afterwards starts fresh)", "kept": "dispute cases, transactions and messages already sent are bank records with their own  …`

**Assistant:** Done. I erased what was remembered about you: 0 stored facts, 1 past-conversation summary, 1 other conversation transcript, and 0 reminders (with their notes). This conversation's transcript is deleted when the conversation ends.

Kestrel still keeps dispute cases, transactions and messages already sent - those are bank records with their own retention rules.

Nothing more can be stored for you in this conversation, so if you want a reminder or a preference set up later, please start a new conversation to do it.

## r4l-tick  ·  maintenance  ·  2026-11-24T11:00:00Z

_maintenance:_ `{"erased_customers": ["eli"], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | r4: the closed-tab erasure ran | `{}` |
| PASS | working | r4: ...and left no transcript | `0 transcripts: []` |

## r4l-s3  ·  session  ·  eli  ·  2026-11-24T12:00:00Z

**Customer:** Starting fresh. Card ending 6610, ZIP 73301. Please set my contact channel to email.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": false, "error": "verification is locked on this account for 24 hours after 3 failed attempts; the customer must call Kestrel"}`

**Assistant:** I couldn't verify your identity: verification on this account is locked for 24 hours after 3 failed attempts, so I can't change your contact channel right now. Please call Kestrel - they can unlock it and update the channel for you.

_Episode written:_ Conversation on 2026-11-24: The customer wanted their contact channel set to email and said the card and ZIP details identified their account (not verified). Identity verification was locked for 24 hours after three failed attempts, so the change was not made. The assistant advised calling Kestrel to unlock it and update the channel. No case or transaction IDs were provided. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r4: erasing memory does not reset the account lockout: the channel is not changed | `null` |
| PASS | working | r4: ...and verification does not succeed inside the 24 hours | `{"verified": false, "error": "verification is locked on this account for 24 hours after 3 failed attempts; the customer must call Kestrel"}` |
