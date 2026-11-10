# adk · heldout-r4 · run 1 · r4-erase-closed-tab-local-reminder

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r4e2-cli  ·  cli_eof_session  ·  marco  ·  2026-11-12T10:00:00Z

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (ADK) | customer=marco session=r4e2-cli | 'exit' or end-of-input ends the session

[you]:   [tool] schedule_reminder({"note": "Return the FitPulse locker key", "remind_on": "2026-11-16", "remind_at": "18:00", "timezone": "America/New_York"})
  [tool] remember_customer_fact({"key": "travel_notice", "value": "Montreal", "valid_until": "2026-11-18"})

[assistant]: Done, Marco.

- **Reminder:** Monday 2026-11-16 at 18:00 EST (New York) - "Return the FitPulse locker key." It will arrive as a secure message in the Kestrel app, since no contact channel is set.
- **Travel notice:** Montreal until 2026-11-18, so Canadian charges are expected.

Anything else I can help with?

[you]: 
[memory] episode E-r4e2-cli-1-7afc1f: Conversation on 2026-11-12: Marco asked for a November 16, 2026, 6pm New York reminder to return the FitPulse locker key; the customer said he is in Montreal until November 18 (not verified). The reminder was scheduled (followup F-49709d1d; due 2026-11-16 23:00 UTC/18:00 EST) via Kestrel app secure message by default, and the Montreal travel notice was stored until 2026-11-18. No case or transaction ids were provided. Case outcomes: no case touched. Lesson: none
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r4: the reminder is a scheduler record on 2026-11-16 (18:00 New York is 23:00 UTC) | `[{"trigger_at": "2026-11-16T23:00:00Z", "approval": "none", "status": "pending", "resume": {"note": "Return the FitPulse locker key"}}]` |
| PASS | semantic | r4: the travel notice is stored until 2026-11-18 | `{"value": "Montreal", "as_of": "2026-11-12T10:00:00Z", "valid_until": "2026-11-18", "expires_at": "2026-11-19T00:00:00Z"}` |

## r4e2-s2  ·  session  ·  marco  ·  2026-11-16T22:40:00Z

**Customer:** Please wipe everything you've stored about me, and every chat we've had. Thanks.

- `request_memory_erasure({})` → `{"erased_now": "1 remembered facts, 1 past-conversation summaries, 1 other conversation transcripts, 1 reminders with their notes", "this_conversation": "its transcript is deleted when the conversation ends, or once it has been idle for 30 minutes if the customer just closes the chat; nothing more can be stored for the customer in it (a new conversation afterwards starts fresh)", "kept": "dispute  …`

**Assistant:** Done - everything remembered about you is erased now:

- 1 stored fact (your profile preferences)
- 1 past-conversation summary and 1 other conversation's transcript
- 1 scheduled reminder, with its note

This conversation's own transcript is deleted when the conversation ends, or once it's been idle 30 minutes if you just close the chat. Nothing more can be stored for you in this conversation - if you want a reminder or a preference set later, start a new conversation.

What Kestrel keeps regardless: dispute cases, transactions and messages already sent, as bank records with their own legal retention.

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

- `load_memory({"query": "earlier conversation topic and travel destination"})` → `{"result": "memories=[]"}`

**Assistant:** I have no record of an earlier conversation here - nothing came back when I looked, so I can't tell you what we discussed.

On travel: there's no travel notice on file for your account either. If you are going somewhere, tell me the destination (and the date you get back) and I can add it.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | r4: resuming the erased session id brings nothing back | `I have no record of an earlier conversation here - nothing came back when I looked, so I can't tell you what we discussed.  On travel: there's no travel notice on file for your account either. If you are going somewhere, …` |
| PASS | semantic | r4: no fact is recreated | `{}` |
| PASS | episodic | r4: the new chat's episode holds nothing erased | `no episode mentions them` |
