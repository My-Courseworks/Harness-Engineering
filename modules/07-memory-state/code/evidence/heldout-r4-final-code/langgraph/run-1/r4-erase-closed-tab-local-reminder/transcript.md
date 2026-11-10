# langgraph · heldout-r4 · run 1 · r4-erase-closed-tab-local-reminder

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r4e2-cli  ·  cli_eof_session  ·  marco  ·  2026-11-12T10:00:00Z

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (LangGraph) | customer=marco session=r4e2-cli | 'exit' or end-of-input ends the session

[you]:   [tool] schedule_reminder({"note": "return the FitPulse locker key", "remind_on": "2026-11-16", "remind_at": "18:00", "timezone": "America/New_York"})
  [tool] remember_customer_fact({"key": "travel_notice", "value": "Montreal", "valid_until": "2026-11-18"})

[assistant]: Both are set, Marco:

- **Reminder:** "return the FitPulse locker key" - Monday, November 16 at 18:00 EST (New York time). It'll arrive as a secure message in the Kestrel app, since no contact channel is set on your account.
- **Travel notice:** Montreal, valid until November 18, so Canadian charges through then will be expected.

Anything else?

[you]: 
[memory] episode E-r4e2-cli-1-97cb9d: Conversation on 2026-11-12: Marco wanted a reminder on Nov 16 at 6pm New York time to return the FitPulse locker key; he said he was in Montreal until Nov 18, so Canadian charges were expected (not verified). Reminder scheduled (followup F-8dff7043) for 2026-11-16 18:00 EST via Kestrel secure message (no contact channel set); travel notice stored until Nov 18. Case outcomes: no case touched. Lesson: none
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r4: the reminder is a scheduler record on 2026-11-16 (18:00 New York is 23:00 UTC) | `[{"trigger_at": "2026-11-16T23:00:00Z", "approval": "none", "status": "pending", "resume": {"note": "return the FitPulse locker key"}}]` |
| PASS | semantic | r4: the travel notice is stored until 2026-11-18 | `{"value": "Montreal", "as_of": "2026-11-12T10:00:00Z", "valid_until": "2026-11-18", "expires_at": "2026-11-19T00:00:00Z"}` |

## r4e2-s2  ·  session  ·  marco  ·  2026-11-16T22:40:00Z

**Customer:** Please wipe everything you've stored about me, and every chat we've had. Thanks.

- `request_memory_erasure({})` → `{"erased_now": "1 remembered facts, 1 past-conversation summaries, 1 other conversation transcripts, 1 reminders with their notes", "this_conversation": "its transcript is deleted when the conversation ends; nothing more can be stored for the customer in it (a new conversation afterwards starts fresh)", "kept": "dispute cases, transactions and messages already sent are bank records with their own  …`

**Assistant:** Done - I've erased what was stored about you: the remembered facts, the summary of your past conversation, that other conversation's transcript, and one reminder with its note.

What Kestrel still keeps: this conversation's transcript, until you end the chat (then it's deleted). Dispute cases, transactions and messages already sent are bank records and stay under their own retention rules.

From here on nothing more can be stored for you in this conversation - if you'd like a reminder or a contact preference set up later, just start a new conversation and it can be done there.

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

- `load_memory({"query": "travel plans destination and recent chat topic"})` → `{"memories": []}`

**Assistant:** I don't have any record of an earlier conversation with you - nothing came back when I checked, so I can't tell you what we discussed.

On travel: there's no travel notice on your account right now, so you haven't told me a destination that's been saved. If you'd like one added, tell me the destination (and your return date) and I'll set it.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | r4: resuming the erased session id brings nothing back | `I don't have any record of an earlier conversation with you - nothing came back when I checked, so I can't tell you what we discussed.  On travel: there's no travel notice on your account right now, so you haven't told m …` |
| PASS | semantic | r4: no fact is recreated | `{}` |
| PASS | episodic | r4: the new chat's episode holds nothing erased | `no episode mentions them` |
