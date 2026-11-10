# langgraph · heldout-r4 · run 1 · r4-erase-closed-tab-local-reminder

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r4e2-cli  ·  cli_eof_session  ·  marco  ·  2026-11-12T10:00:00Z

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (LangGraph) | customer=marco session=r4e2-cli | 'exit' or end-of-input ends the session

[you]:   [tool] schedule_reminder({"note": "Return the FitPulse locker key", "remind_on": "2026-11-16", "remind_at": "18:00", "timezone": "America/New_York"})
  [tool] remember_customer_fact({"key": "travel_notice", "value": "Montreal", "valid_until": "2026-11-18"})

[assistant]: Done, Marco.

- **Reminder:** "Return the FitPulse locker key" - Monday November 16 at 18:00 EST (New York time). It will reach you by secure message in the Kestrel app, since no contact channel is set on your account.
- **Travel notice:** Montreal until November 18 - recorded, so Canadian charges on your card during that period are expected.

Anything else?

[you]: 
[memory] episode E-r4e2-cli-1-76aa8f: Conversation on 2026-11-12: Marco asked for a reminder on Nov 16 at 6pm New York time to return the FitPulse locker key, and said he is in Montreal until Nov 18 (not verified), so Canadian charges should be expected. Reminder scheduled (follow-up F-859fd07f) via secure Kestrel app message; travel notice stored until Nov 18. No contact channel is set. Case outcomes: no case touched. Lesson: none
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r4: the reminder is a scheduler record on 2026-11-16 (18:00 New York is 23:00 UTC) | `[{"trigger_at": "2026-11-16T23:00:00Z", "approval": "none", "status": "pending", "resume": {"note": "Return the FitPulse locker key"}}]` |
| PASS | semantic | r4: the travel notice is stored until 2026-11-18 | `{"value": "Montreal", "as_of": "2026-11-12T10:00:00Z", "valid_until": "2026-11-18", "expires_at": "2026-11-19T00:00:00Z"}` |

## r4e2-s2  ·  session  ·  marco  ·  2026-11-16T22:40:00Z

**Customer:** Please wipe everything you've stored about me, and every chat we've had. Thanks.

- `request_memory_erasure({})` → `{"erased_now": "1 remembered facts, 1 past-conversation summaries, 1 other conversation transcripts, 1 reminders with their notes", "this_conversation": "its transcript is deleted when the conversation ends, or once it has been idle for 30 minutes if the customer just closes the chat; nothing more can be stored for the customer in it (a new conversation afterwards starts fresh)", "kept": "dispute  …`

**Assistant:** Done. I erased everything stored about you: your saved facts, past-conversation summaries, other conversation transcripts, and your reminder with its note.

What remains: this conversation's transcript is deleted when the conversation ends (or after 30 minutes idle if you just close the chat). Dispute cases, transactions and messages already sent are bank records with their own retention.

Nothing more can be stored for you in this conversation - reminders or preferences would need a new conversation.

## r4e2-fire-due  ·  fire_followups  ·  2026-11-16T23:01:00Z

_outcomes:_ `[]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r4: a reminder falling due while the erasure is pending is never sent | `0 messages` |
| PASS | semantic | r4: no fact remains | `{}` |
| PASS | episodic | r4: no episode remains or is written by the fire | `0 episodes; purged 0` |
| PASS | working | r4: no transcript remains or is written by the fire | `0 transcripts: []` |
| PASS | guard | r4: the reminder note and the trip are in no memory store | `found nowhere` |

## r4e2-fire-next  ·  fire_followups  ·  2026-11-17T09:00:00Z

_outcomes:_ `[]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r4: nothing retries afterwards | `[]` |
| PASS | prospective | r4: still no message to the erased customer | `0 messages` |

## r4e2-s3  ·  session  ·  marco  ·  2026-11-20T15:00:00Z

_Resumes session `r4e2-s2`._

**Customer:** Picking this chat back up. What were we talking about here, and where did I tell you I was travelling?

- `load_memory({"query": "earlier conversation topics and travel destination"})` → `{"memories": []}`

**Assistant:** I don't have any record of an earlier conversation here - nothing from past chats came back.

And on travel: there's no travel notice on file for your account, so you haven't told me a destination that's been stored.

If you're travelling and want a notice added, just tell me the destination (and your return date), and I'll set it.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | r4: resuming the erased session id brings nothing back | `I don't have any record of an earlier conversation here - nothing from past chats came back.  And on travel: there's no travel notice on file for your account, so you haven't told me a destination that's been stored.  If …` |
| PASS | semantic | r4: no fact is recreated | `{}` |
| PASS | episodic | r4: the new chat's episode holds nothing erased | `no episode mentions them` |
