# adk · heldout-r4 · run 1 · r4-erase-closed-tab-local-reminder

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r4e2-cli  ·  cli_eof_session  ·  marco  ·  2026-11-12T10:00:00Z

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (ADK) | customer=marco session=r4e2-cli | 'exit' or end-of-input ends the session

[you]:   [tool] schedule_reminder({"note": "Return the FitPulse locker key", "remind_on": "2026-11-16", "remind_at": "18:00", "timezone": "America/New_York"})
  [tool] remember_customer_fact({"key": "travel_notice", "value": "Montreal", "valid_until": "2026-11-18"})

[assistant]: Done, Marco.

- **Reminder:** FitPulse locker key - Monday, November 16 at 18:00 EST (New York time). It'll arrive as a secure message in the Kestrel app, since no contact channel is set.
- **Travel notice:** Montreal, through November 18 - so Canadian charges won't be flagged as unexpected.

[you]: 
[memory] episode E-r4e2-cli-1-b84064: Conversation on 2026-11-12: Marco asked for a reminder on 2026-11-16 at 18:00 New York time to return the FitPulse locker key; reminder F-1637acf8 was set to arrive then as a secure Kestrel app message (no contact channel set). He said he is in Montreal until Nov 18 and Canadian charges should be expected (not verified); travel notice stored through Nov 18. Case outcomes: no case touched. Lesson: none
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r4: the reminder is a scheduler record on 2026-11-16 (18:00 New York is 23:00 UTC) | `[{"trigger_at": "2026-11-16T23:00:00Z", "approval": "none", "status": "pending", "resume": {"note": "Return the FitPulse locker key"}}]` |
| PASS | semantic | r4: the travel notice is stored until 2026-11-18 | `{"value": "Montreal", "as_of": "2026-11-12T10:00:00Z", "valid_until": "2026-11-18", "expires_at": "2026-11-19T00:00:00Z"}` |

## r4e2-s2  ·  session  ·  marco  ·  2026-11-16T22:40:00Z

**Customer:** Please wipe everything you've stored about me, and every chat we've had. Thanks.

**Assistant:** I can do that - but first I need to verify you. Please type your card's last 4 digits and your billing ZIP code.

## r4e2-fire-due  ·  fire_followups  ·  2026-11-16T23:01:00Z

### follow-up session `followup-F-1637acf8-1`

**Scheduler:** [scheduled follow-up F-1637acf8] action=customer_reminder resume={"note": "Return the FitPulse locker key"}. The customer is not in this conversation and cannot reply to the message you send. Carry out the action using your tools, then send the customer exactly one message with notify_customer.

- `notify_customer({"message": "Reminder: return the FitPulse locker key. (Sent by secure message in the Kestrel app \u2014 no reply needed here; message the card-care chat if you need anything else.)"})` → `{"channel": "secure_message", "message_id": 1, "status": "sent"}`

**Assistant:** Reminder sent via secure message in the Kestrel app: "Return the FitPulse locker key."

_Episode written:_ Scheduled follow-up on 2026-11-16 (customer not present): Scheduled follow-up F-1637acf8 required a reminder to return the FitPulse locker key. The assistant sent one secure message in the Kestrel app (message_id 1, status sent) and noted no reply was needed. The customer was not present and stated no preferences. Case outcomes: no case touched. Lesson: none

_outcomes:_ `[{"followup_id": "F-1637acf8", "user_id": "marco", "outcome": "fired_done", "error": null}]`

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | prospective | r4: a reminder falling due while the erasure is pending is never sent | `1 messages` |
| **FAIL** | semantic | r4: no fact remains | `{"travel_notice": {"value": "Montreal", "as_of": "2026-11-12T10:00:00Z", "valid_until": "2026-11-18", "expires_at": "2026-11-19T00:00:00Z"}}` |
| **FAIL** | episodic | r4: no episode remains or is written by the fire | `2 episodes; purged 0` |
| **FAIL** | working | r4: no transcript remains or is written by the fire | `3 transcripts: ['followup-F-1637acf8-1', 'r4e2-cli', 'r4e2-s2']` |
| **FAIL** | guard | r4: the reminder note and the trip are in no memory store | `{"locker key": ["adk_episodes.db", "adk_sessions.db"], "Montreal": ["adk_episodes.db", "adk_sessions.db"]}` |

## r4e2-fire-next  ·  fire_followups  ·  2026-11-17T09:00:00Z

_outcomes:_ `[]`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | r4: nothing retries afterwards | `[]` |
| **FAIL** | prospective | r4: still no message to the erased customer | `1 messages` |

## r4e2-s3  ·  session  ·  marco  ·  2026-11-20T15:00:00Z

_Resumes session `r4e2-s2`._

**Customer:** Picking this chat back up. What were we talking about here, and where did I tell you I was travelling?

- `load_memory({"query": "travel notice destination trip travel plans"})` → `{"result": "memories=[MemoryEntry(content=Content(\n  parts=[\n    Part(\n      text='Conversation on 2026-11-12: Marco asked for a reminder on 2026-11-16 at 18:00 New York time to return the FitPulse locker key; reminder F-1637acf8 was set to arrive then as a secure Kestrel app message (no contact channel set). He said he is in Montreal until Nov 18 and Canadian charges should be expected (not ve …`

**Assistant:** Here in this chat: you asked me to wipe everything I remember about you and delete our past conversations. That's still on hold - I need your card's last 4 digits and billing ZIP to verify you first.

On travel: nothing is on file as a current travel notice. My record of an earlier conversation (12 Nov) has you saying you'd be in Montreal until 18 Nov - that's now past, so no travel notice is active. If you're travelling again, tell me the destination and return date and I'll set a new one.

_Episode written:_ Conversation on 2026-11-20: The customer asked to wipe all data and past chats. Assistant requested verification (card and billing ZIP); none provided, so deletion is on hold. Memory: reminder F-1637acf8 for 2026-11-16 18:00 New York (FitPulse locker key, Kestrel app message). The customer said he was in Montreal until Nov 18 and expected Canadian charges (not verified). No case/transaction IDs; no travel notice. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | episodic | r4: resuming the erased session id brings nothing back | `Here in this chat: you asked me to wipe everything I remember about you and delete our past conversations. That's still on hold - I need your card's last 4 digits and billing ZIP to verify you first.  On travel: nothing  …` |
| PASS | semantic | r4: no fact is recreated | `{}` |
| **FAIL** | episodic | r4: the new chat's episode holds nothing erased | `Conversation on 2026-11-12: Marco asked for a reminder on 2026-11-16 at 18:00 New York time to return the FitPulse locker key; reminder F-1637acf8 was set to arrive then as a secure Kestrel app message (no contact channe …` |
