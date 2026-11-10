# adk · heldout-r4 · run 1 · r4-erase-closed-tab-local-reminder

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r4e2-cli  ·  cli_eof_session  ·  marco  ·  2026-11-12T10:00:00Z

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (ADK) | customer=marco session=r4e2-cli | 'exit' or end-of-input ends the session

[you]:   [tool] schedule_reminder({"note": "Return the FitPulse locker key", "remind_on": "2026-11-16", "remind_at": "18:00", "timezone": "America/New_York"})
  [tool] remember_customer_fact({"key": "travel_notice", "value": "Montreal", "valid_until": "2026-11-18"})

[assistant]: Done, Marco:

- **Reminder set:** Monday 2026-11-16 at 18:00 EST (New York) - "Return the FitPulse locker key." It will arrive by secure message in the Kestrel app, since no contact channel is set.
- **Travel notice saved:** Montreal until 2026-11-18, so Canadian charges won't be flagged as unusual.

Anything else?

[you]: 
[memory] episode E-r4e2-cli-1-f9b06d: Conversation on 2026-11-12: Marco asked for a reminder on 2026-11-16 at 18:00 New York time to return the FitPulse locker key, and said he would be in Montreal until 2026-11-18 expecting Canadian charges (not verified). Reminder scheduled (follow-up ID F-fc6131e6) by secure Kestrel app message; Montreal travel notice saved until 2026-11-18. No transaction ID. Case outcomes: no case touched. Lesson: none
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r4: the reminder is a scheduler record on 2026-11-16 (18:00 New York is 23:00 UTC) | `[{"trigger_at": "2026-11-16T23:00:00Z", "approval": "none", "status": "pending", "resume": {"note": "Return the FitPulse locker key"}}]` |
| PASS | semantic | r4: the travel notice is stored until 2026-11-18 | `{"value": "Montreal", "as_of": "2026-11-12T10:00:00Z", "valid_until": "2026-11-18", "expires_at": "2026-11-19T00:00:00Z"}` |

## r4e2-s2  ·  session  ·  marco  ·  2026-11-16T22:40:00Z

**Customer:** Please wipe everything you've stored about me, and every chat we've had. Thanks.

- `request_memory_erasure({})` → `{"erased_now": "1 remembered facts, 1 past-conversation summaries, 1 other conversation transcripts, 1 reminders with their notes", "this_conversation": "its transcript is deleted when the conversation ends, or once it has been idle for 30 minutes if the customer just closes the chat; nothing more can be stored for the customer in it (a new conversation afterwards starts fresh)", "kept": "dispute  …`

**Assistant:** Done. That erased, immediately:

- 1 stored fact about you (your contact channel/travel notice)
- 1 past-conversation summary
- 1 other conversation's transcript
- 1 reminder, including its note

This conversation's own transcript is deleted when the conversation ends - or, if you just close the chat, once it's been idle for 30 minutes.

Kestrel still keeps dispute cases, transactions and messages already sent, as bank records with their own legal retention.

One thing to know: nothing more can be stored for you in this conversation - not a reminder, not a contact preference. If you want either set up later, start a new conversation.

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

- `load_memory({"query": "previous conversation, travel destination"})` → `{"result": "memories=[]"}`

**Assistant:** I don't have any record of an earlier conversation with you here - nothing comes up on my side.

As for travel, there's no travel notice on file for your account right now. If you told me about a trip before, it isn't recorded. Would you like to set one now? If so, just tell me the destination and the date you return, and I'll add it.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | r4: resuming the erased session id brings nothing back | `I don't have any record of an earlier conversation with you here - nothing comes up on my side.  As for travel, there's no travel notice on file for your account right now. If you told me about a trip before, it isn't re …` |
| PASS | semantic | r4: no fact is recreated | `{}` |
| PASS | episodic | r4: the new chat's episode holds nothing erased | `no episode mentions them` |
