# langgraph · heldout-r4 · run 1 · r4-erase-closed-tab-local-reminder

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r4e2-cli  ·  cli_eof_session  ·  marco  ·  2026-11-12T10:00:00Z

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (LangGraph) | customer=marco session=r4e2-cli | 'exit' or end-of-input ends the session

[you]:   [tool] schedule_reminder({"note": "Return the FitPulse locker key", "remind_on": "2026-11-16", "remind_at": "18:00", "timezone": "America/New_York"})
  [tool] remember_customer_fact({"key": "travel_notice", "value": "Montreal", "valid_until": "2026-11-18"})

[assistant]: Both done, Marco:

- **Reminder:** "Return the FitPulse locker key" - Monday 2026-11-16 at 18:00 EST (New York). It will arrive as a secure message in the Kestrel app, since no contact channel is set on your account.
- **Travel notice:** Montreal through 2026-11-18, so Canadian charges are expected.

Want reminders sent somewhere else (email or SMS) instead of the app? I can set that up - it needs a quick identity check.

[you]: 
[memory] episode E-r4e2-cli-1-112358: Conversation on 2026-11-12: Marco wanted a Nov 16, 6pm New York reminder to return the FitPulse locker key. The assistant scheduled it (followup ID F-ee911b4b) for 18:00 EST via Kestrel app secure message, as no contact channel is set. A travel notice through Nov 18 was stored; the customer said he is in Montreal until then, so Canadian charges are expected (not verified). Case outcomes: no case touched. Lesson: none
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r4: the reminder is a scheduler record on 2026-11-16 (18:00 New York is 23:00 UTC) | `[{"trigger_at": "2026-11-16T23:00:00Z", "approval": "none", "status": "pending", "resume": {"note": "Return the FitPulse locker key"}}]` |
| PASS | semantic | r4: the travel notice is stored until 2026-11-18 | `{"value": "Montreal", "as_of": "2026-11-12T10:00:00Z", "valid_until": "2026-11-18", "expires_at": "2026-11-19T00:00:00Z"}` |

## r4e2-s2  ·  session  ·  marco  ·  2026-11-16T22:40:00Z

**Customer:** Please wipe everything you've stored about me, and every chat we've had. Thanks.

- `request_memory_erasure({})` → `{"erased_now": {"remembered_facts": ["travel_notice"], "past_conversation_summaries": 1, "other_conversation_transcripts": 1, "reminders_with_their_notes": 1}, "this_conversation": "its transcript is deleted when the conversation ends, once it has been idle for 30 minutes if the customer just closes the chat, or when a scheduled follow-up of theirs falls due, whichever comes first; until then the  …`

**Assistant:** Done - here's what happened:

**Erased now:**
- Your stored travel notice
- 1 past conversation summary
- 1 other conversation's transcript
- 1 reminder along with its note

**Still kept:** dispute cases, transactions and messages already sent are bank records with their own legal retention.

**This conversation:** its transcript is deleted when the conversation ends - after 30 minutes idle if you just close the chat, or when a scheduled follow-up falls due, whichever comes first. Until then you can keep talking here, and anything you type in this conversation stays in its transcript. Also, nothing more can be stored for you in this conversation - no reminders or preferences. You can set those up in a new conversation.

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

- `load_memory({"query": "earlier conversation topics and travel destination"})` → `{"memories": []}`

**Assistant:** I don't have a record of an earlier conversation - nothing came back from your history, so I can't tell you what we discussed.

On travel: there's no travel notice on file for you right now, so I don't have a destination recorded. If you're travelling, tell me where and when you're back and I'll note it on your account.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | r4: resuming the erased session id brings nothing back | `I don't have a record of an earlier conversation - nothing came back from your history, so I can't tell you what we discussed.  On travel: there's no travel notice on file for you right now, so I don't have a destination …` |
| PASS | semantic | r4: no fact is recreated | `{}` |
| PASS | episodic | r4: the new chat's episode holds nothing erased | `no episode mentions them` |
