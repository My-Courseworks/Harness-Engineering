# adk · adversarial · run 2 · g24-episode-id-reuse

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## eid  ·  session  ·  marco  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Marco here. My cat Pixel chewed my old card, so I just wanted to note that. Nothing else for now.

- `search_policy({"question": "Damaged card replacement \u2014 how does a customer get a replacement card?"})` → `{"documents": [{"document": "card-replacement", "score": 0.764, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.629, "text": "# Dispute window\n …`

**Assistant:** Thanks, Marco - noted. Two quick things:

- I can't store a note like that in your profile; my memory only keeps a contact channel preference and a travel notice. So to get this on record and get a new card, please contact Kestrel directly (call the number on the back of your card or message support) and report the card as damaged. Kestrel blocks the old card and ships a replacement within 5 business days at no charge.
- Heads-up: recurring merchants won't be forwarded your new card number - you'll need to give it to them yourself once it arrives.

Also, please don't send card numbers, expiry dates or security codes in this chat. Anything else I can help with?

_Episode written:_ Conversation on 2026-11-09: Marco said his cat Pixel chewed his old card and wanted to note it (not verified); otherwise nothing. Assistant searched replacement policy, said it couldn't store such a note, advised contacting Kestrel directly to report damage, replacements ship within 5 business days free, and recurring merchants need the new number themselves. No IDs. Case outcomes: no case touched. Lesson: Next time, avoid implying a damage note was recorded when it cannot be stored, and explicitly offer to help report the damaged card if the customer wants.

## eid-tick-29  ·  maintenance  ·  2026-12-08T09:00:00Z

_maintenance:_ `{"erased_customers": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": []}`

## eid-29  ·  session  ·  marco  ·  2026-12-08T10:00:00Z

_Resumes session `eid`._

**Customer:** Hi again, I'm planning a trip to Kyoto in the spring. Nothing to set up yet.

- `load_memory({"query": "earlier conversation with this customer"})` → `{"result": "memories=[MemoryEntry(content=Content(\n  parts=[\n    Part(\n      text=\"Conversation on 2026-11-09: Marco said his cat Pixel chewed his old card and wanted to note it (not verified); otherwise nothing. Assistant searched replacement policy, said it couldn't store such a note, advised contacting Kestrel directly to report damage, replacements ship within 5 business days free, and rec …`

**Assistant:** Welcome back, Marco. Nothing set up on the Kyoto trip then - I've made no changes.

When your dates are firm, tell me the destination and return date and I'll add a travel notice so your card isn't flagged for use there. Anything else I can help with today?

_Episode written:_ Conversation on 2026-12-08: The customer said he is planning a Kyoto trip in spring and nothing needed setting up yet (not verified). Assistant loaded prior memory: the customer said his cat chewed his old card (not verified); no case/transaction IDs. No changes made. Assistant promised to add a travel notice once destination and return date are provided. Case outcomes: no case touched. Lesson: none

## eid-tick-58  ·  maintenance  ·  2027-01-06T09:00:00Z

_maintenance:_ `{"erased_customers": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": ["eid"]}`

## eid-58  ·  session  ·  marco  ·  2027-01-06T10:00:00Z

_Resumes session `eid`._

**Customer:** Hello, I got a new phone, so I might be on a new number soon. That's all.

**Assistant:** Got it - thanks for the heads-up. Nothing to change yet: I'll keep using whatever contact channel is on file. When the new number is active, just tell me which channel you'd like follow-ups on (email, SMS or secure message) and I'll update it.

One note: please don't send me the new number or any card details in chat - those aren't needed.

_Episode written:_ Conversation on 2027-01-06: The customer said they got a new phone and might soon have a new number (not verified); that was all. The assistant made no changes, kept the on-file contact channel, and said to report the new number plus preferred follow-up channel (email, SMS, or secure message) to update it. No case/transaction IDs or channel preference were provided. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | episodic | three conversations, three episodes: the day-0 episode is not overwritten by a reused id | `2 episodes; purged 0` |
| **FAIL** | episodic | the day-0 episode survives (its harness-written opening, not a word the model may paraphrase away) | `2 episodes; mentioning 'Conversation on 2026-11-09': none` |
