# langgraph · heldout-r4 · run 1 · r4-erase-closed-tab-local-reminder

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r4e2-cli  ·  cli_eof_session  ·  marco  ·  2026-11-12T10:00:00Z

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (LangGraph) | customer=marco session=r4e2-cli | 'exit' or end-of-input ends the session

[you]:   [tool] schedule_reminder({"note": "Return the FitPulse locker key", "remind_on": "2026-11-16", "remind_at": "18:00", "timezone": "America/New_York"})
  [tool] remember_customer_fact({"key": "travel_notice", "value": "Montreal", "valid_until": "2026-11-18"})

[assistant]: Both done, Marco:

- **Reminder:** "Return the FitPulse locker key" - Monday, November 16 at 6:00 PM EST (New York), arriving by secure message in the Kestrel app since no contact channel is set on your account.
- **Travel notice:** Montreal until November 18, so Canadian charges won't be flagged as unexpected.

If you'd rather get the reminder by email or SMS, let me know and I can set that up.

[you]: 
[memory] episode E-r4e2-cli-1-0dc202: Conversation on 2026-11-12: Marco asked for a Nov 16, 2026, 6 PM New York reminder to return the FitPulse locker key; scheduled as followup F-40df99ac via Kestrel secure message because no contact channel is set. The customer said they are in Montreal until Nov 18 and expect Canadian charges (not verified); a travel notice was stored. Assistant offered email/SMS instead. Case outcomes: no case touched. Lesson: none
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r4: the reminder is a scheduler record on 2026-11-16 (18:00 New York is 23:00 UTC) | `[{"trigger_at": "2026-11-16T23:00:00Z", "approval": "none", "status": "pending", "resume": {"note": "Return the FitPulse locker key"}}]` |
| PASS | semantic | r4: the travel notice is stored until 2026-11-18 | `{"value": "Montreal", "as_of": "2026-11-12T10:00:00Z", "valid_until": "2026-11-18", "expires_at": "2026-11-19T00:00:00Z"}` |

## r4e2-s2  ·  session  ·  marco  ·  2026-11-16T22:40:00Z

**Customer:** Please wipe everything you've stored about me, and every chat we've had. Thanks.

- `request_memory_erasure({})` → `{"erased_now": "1 remembered facts, 1 past-conversation summaries, 1 other conversation transcripts, 1 reminders with their notes", "this_conversation": "its transcript is deleted when the conversation ends, or once it has been idle for 30 minutes if the customer just closes the chat; nothing more can be stored for the customer in it (a new conversation afterwards starts fresh)", "kept": "dispute  …`

**Assistant:** Done. I've erased what was stored about you: your saved facts, the summaries of past conversations, the earlier conversation transcripts and a reminder with its note. Your contact preferences and travel notice are gone too.

This conversation's own transcript is deleted when the conversation ends (or once it's been idle for 30 minutes if you just close the chat), and nothing more can be stored for you in it, so a reminder or preference would need a new conversation.

Kept as bank records with their own retention: your dispute cases, transactions, and messages already sent.

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

- `load_memory({"query": "earlier conversation topic and travel destination"})` → `{"memories": []}`

**Assistant:** I have no record of an earlier conversation here, so I can't tell you what we discussed.

On travel: there's no travel notice on file for you - you haven't told me a destination in a conversation I can see. If you're going somewhere, tell me where and when you'll be back and I'll add it.

One note: the profile is the current source, so if you set a travel notice in the past it either expired or was never saved.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | r4: resuming the erased session id brings nothing back | `I have no record of an earlier conversation here, so I can't tell you what we discussed.  On travel: there's no travel notice on file for you - you haven't told me a destination in a conversation I can see. If you're goi …` |
| PASS | semantic | r4: no fact is recreated | `{}` |
| PASS | episodic | r4: the new chat's episode holds nothing erased | `no episode mentions them` |
