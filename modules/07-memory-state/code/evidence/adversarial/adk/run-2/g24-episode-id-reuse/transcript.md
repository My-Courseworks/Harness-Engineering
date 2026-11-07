# adk · adversarial · run 2 · g24-episode-id-reuse

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## eid  ·  session  ·  marco  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Marco here. My cat Pixel chewed my old card, so I just wanted to note that. Nothing else for now.

**Assistant:** Thanks for the heads-up, Marco. Just so you know: the only things I can save on your profile are a contact channel and a travel notice - I don't have a way to keep a general note, so nothing about the chewed card is stored.

For a damaged card, you'd want a replacement issued - that's done by Kestrel's card services (the number on the back of your card, or the app). If any charges show up on it that you don't recognise, come back here and I can look them up and dispute them.

_Episode written:_ Conversation on 2026-11-09: Marco said his cat Pixel chewed his old card (not verified) and wanted to note it; he had nothing else for now. The assistant said general notes cannot be stored, advised contacting Kestrel card services via the number on the card/app for a replacement, and offered to look up/dispute unrecognised charges. No case/transaction IDs or promise. Case outcomes: no case touched. Lesson: none

## eid-tick-29  ·  maintenance  ·  2026-12-08T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": []}`

## eid-29  ·  session  ·  marco  ·  2026-12-08T10:00:00Z

_Resumes session `eid`._

**Customer:** Hi again, I'm planning a trip to Kyoto in the spring. Nothing to set up yet.

- `load_memory({"query": "Kyoto trip travel notice"})` → `{"result": "memories=[MemoryEntry(content=Content(\n  parts=[\n    Part(\n      text='Conversation on 2026-11-09: Marco said his cat Pixel chewed his old card (not verified) and wanted to note it; he had nothing else for now. The assistant said general notes cannot be stored, advised contacting Kestrel card services via the number on the card/app for a replacement, and offered to look up/dispute u …`

**Assistant:** Hi Marco - good to hear from you. I don't have anything on record about a Kyoto trip, and I've not set anything up: no travel notice is on file, and nothing was stored from this message.

When your plans firm up, just tell me the destination and return date and I'll add the travel notice then. Anything else I can help with today?

_Episode written:_ Conversation on 2026-12-08: The customer said he is planning a Kyoto trip in spring (not verified) and had nothing to set up yet. The assistant confirmed no Kyoto record or travel notice was on file and nothing was stored. The assistant promised to add a travel notice later when given destination and return date. No case/transaction IDs. Case outcomes: no case touched. Lesson: none

## eid-tick-58  ·  maintenance  ·  2027-01-06T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": ["eid"]}`

## eid-58  ·  session  ·  marco  ·  2027-01-06T10:00:00Z

_Resumes session `eid`._

**Customer:** Hello, I got a new phone, so I might be on a new number soon. That's all.

**Assistant:** Got it - thanks for the heads-up. Nothing's changed on your profile yet: your contact channel is still unset, so follow-ups and reminders go by secure message in the Kestrel app.

When the new number is active, just tell me here and I'll update your contact channel to SMS. I'll need your card's last 4 digits and billing ZIP at that point to make the change. Don't send a full card number or any security codes.

_Episode written:_ Conversation on 2027-01-06: Customer said they got a new phone and might soon have a new number (not verified), only as a heads-up. No case or transaction IDs. Assistant made no profile change, noting contact channel still unset, and promised to update to SMS when the new number is active after verification. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | three conversations, three episodes: the day-0 episode is not overwritten by a reused id | `3 episodes; purged 0` |
| PASS | episodic | the day-0 episode survives (its harness-written opening, not a word the model may paraphrase away) | `3 episodes; mentioning 'Conversation on 2026-11-09': ['E-eid-1-462f94']` |
