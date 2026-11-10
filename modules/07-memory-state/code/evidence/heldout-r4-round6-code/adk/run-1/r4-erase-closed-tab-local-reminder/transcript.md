# adk · heldout-r4 · run 1 · r4-erase-closed-tab-local-reminder

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r4e2-cli  ·  cli_eof_session  ·  marco  ·  2026-11-12T10:00:00Z

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (ADK) | customer=marco session=r4e2-cli | 'exit' or end-of-input ends the session

[you]:   [tool] schedule_reminder({"note": "Return the FitPulse locker key", "remind_on": "2026-11-16", "remind_at": "18:00", "timezone": "America/New_York"})
  [tool] remember_customer_fact({"key": "travel_notice", "value": "Montreal", "valid_until": "2026-11-18"})

[assistant]: Both done, Marco.

- **Reminder:** Monday 2026-11-16 at 18:00 EST (New York) - to return the FitPulse locker key. It will arrive by secure message in the Kestrel app, since no contact channel is set.
- **Travel notice:** Montreal through 2026-11-18, so Canadian charges won't be flagged as unexpected.

Anything else?

[you]: 
[memory] episode E-r4e2-cli-1-38e9b9: Conversation on 2026-11-12: Marco requested a reminder for 2026-11-16 at 18:00 New York to return the FitPulse locker key; scheduled with followup ID F-b63f9eee via Kestrel app secure message (default channel). He said he is in Montreal until 2026-11-18 (not verified) for Canadian charges; a travel notice was stored. No stated preference. Case outcomes: no case touched. Lesson: none
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r4: the reminder is a scheduler record on 2026-11-16 (18:00 New York is 23:00 UTC) | `[{"trigger_at": "2026-11-16T23:00:00Z", "approval": "none", "status": "pending", "resume": {"note": "Return the FitPulse locker key"}}]` |
| PASS | semantic | r4: the travel notice is stored until 2026-11-18 | `{"value": "Montreal", "as_of": "2026-11-12T10:00:00Z", "valid_until": "2026-11-18", "expires_at": "2026-11-19T00:00:00Z"}` |

## r4e2-s2  ·  session  ·  marco  ·  2026-11-16T22:40:00Z

**Customer:** Please wipe everything you've stored about me, and every chat we've had. Thanks.

- `request_memory_erasure({})` → `{"erased_now": {"remembered_facts": ["travel_notice"], "past_conversation_summaries": 1, "other_conversation_transcripts": 1, "reminders_with_their_notes": 1}, "this_conversation": "its transcript is deleted when the conversation ends, once it has been idle for 30 minutes if the customer just closes the chat, or when a scheduled follow-up of theirs falls due, whichever comes first; until then the  …`

**Assistant:** Done. Here's what was erased just now:

- The facts I had stored about you (your travel notice)
- 1 past conversation summary
- 1 other conversation transcript
- 1 reminder, along with its note

What Kestrel keeps: dispute cases, transactions and messages already sent are bank records with their own legal retention.

This conversation's own transcript is deleted when the conversation ends - 30 minutes after you close the chat, or when a scheduled follow-up of yours falls due, whichever comes first. Until then you can keep talking here.

From now on, nothing more can be stored about you in this conversation (no reminders, no preferences). If you want to set any of that up later, start a new conversation and it will begin fresh.

## r4e2-fire-due  ·  fire_followups  ·  2026-11-16T23:01:00Z

_outcomes:_ `[]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r4: a reminder falling due while the erasure is pending is never sent | `0 messages` |
| PASS | semantic | r4: no fact remains | `{}` |
| PASS | episodic | r4: no episode remains or is written by the fire | `0 episodes; purged 0` |
| **FAIL** | working | r4: no transcript remains or is written by the fire | `1 transcripts: ['r4e2-s2']` |
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

**Assistant:** I don't have any record of an earlier conversation - nothing came back when I looked, so I can't tell you what we discussed. And there's no travel notice on file for you right now.

If you'd like to set one, just tell me the destination (and your return date), and I'll add it.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | r4: resuming the erased session id brings nothing back | `I don't have any record of an earlier conversation - nothing came back when I looked, so I can't tell you what we discussed. And there's no travel notice on file for you right now.  If you'd like to set one, just tell me …` |
| PASS | semantic | r4: no fact is recreated | `{}` |
| PASS | episodic | r4: the new chat's episode holds nothing erased | `no episode mentions them` |
