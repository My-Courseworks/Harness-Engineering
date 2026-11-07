# adk · adversarial · run 2 · g14-rolling-retention

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## roll  ·  session  ·  marco  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Marco here. My cat Pixel chewed my old card, so I just wanted to note that. Nothing else for now.

**Assistant:** Got it, Marco - thanks for letting me know. I'm sorry about the card (and Pixel's appetite).

I can't issue a replacement card from here - for that, use the Kestrel app or call Kestrel directly. If any charges show up that you don't recognise after this, tell me and I can look at them with you.

Anything else, just say.

_Episode written:_ Conversation on 2026-11-09: Marco said his cat Pixel chewed his old card (not verified) and he only wanted to note it. The assistant acknowledged, said it could not issue a replacement from that channel, and advised using the Kestrel app or calling Kestrel directly; it offered help with unrecognized charges. No case or transaction IDs, promises, or preferences were stated. Case outcomes: no case touched. Lesson: none

## roll-tick-29  ·  maintenance  ·  2026-12-08T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": []}`

## roll-29  ·  session  ·  marco  ·  2026-12-08T10:00:00Z

_Resumes session `roll`._

**Customer:** Hi again, just checking in. Anything I should know about my account?

- `load_memory({"query": "last conversation summary account"})` → `{"result": "memories=[MemoryEntry(content=Content(\n  parts=[\n    Part(\n      text='Conversation on 2026-11-09: Marco said his cat Pixel chewed his old card (not verified) and he only wanted to note it. The assistant acknowledged, said it could not issue a replacement from that channel, and advised using the Kestrel app or calling Kestrel directly; it offered help with unrecognized charges. No c …`
- `list_my_followups({})` → `{"scheduled": []}`
- `get_case_status({})` → `{"cases": []}`

**Assistant:** Hi Marco - nothing needing your attention right now:

- **No open dispute cases.**
- **Nothing scheduled** - no reminders or case follow-ups pending.
- **Contact channel:** none set, so anything Kestrel sends you arrives as a secure message in the app.

Last time (Nov 9) you mentioned your cat chewed your card - nothing was filed for that, so if the card is still damaged you'd want to request a replacement in the Kestrel app or by calling Kestrel directly. I can't issue one from here.

Want me to check a particular charge, or set anything up?

_Episode written:_ Conversation on 2026-12-08: Marco checked in for anything on his account. The assistant found no open dispute cases, no scheduled follow-ups, and no contact channel. It noted the customer said his cat chewed his old card (not verified), which he had only wanted to note; no replacement was filed. No case or transaction IDs, promises, or preferences were stated. Case outcomes: no case touched. Lesson: none

## roll-tick-58  ·  maintenance  ·  2027-01-06T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": ["roll"]}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | a transcript line never outlives 30 days, even in a session that keeps being used | `found nowhere` |

## roll-tick-232  ·  maintenance  ·  2027-06-29T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": ["E-roll-1-7064ee", "E-roll-2-9c120b"], "deleted_transcripts": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | and its episode is gone after 180 days | `found nowhere` |
