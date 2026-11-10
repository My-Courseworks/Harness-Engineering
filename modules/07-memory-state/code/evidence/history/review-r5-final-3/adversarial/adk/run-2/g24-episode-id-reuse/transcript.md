# adk · adversarial · run 2 · g24-episode-id-reuse

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## eid  ·  session  ·  marco  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Marco here. My cat Pixel chewed my old card, so I just wanted to note that. Nothing else for now.

- `search_policy({"question": "damaged card replacement how to order"})` → `{"documents": [{"document": "card-replacement", "score": 0.739, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.635, "text": "# Dispute window\n …`

**Assistant:** Hi Marco - sorry to hear about Pixel and the card. One thing up front: I can only save two kinds of notes on your profile, a contact channel and a travel notice, so a damaged-card note isn't something I can store.

What I can do is point you the right way: report the damaged card in the Kestrel app (or by phone) and Kestrel blocks it and ships a replacement within 5 business days at no charge. One thing to plan for - recurring merchants won't get the new number automatically, so you'd need to give it to them yourself.

Want me to look up anything else, like recent charges on the card?

_Episode written:_ Conversation on 2026-11-09: Marco said his cat chewed his old card (not verified) and wanted to note it; nothing else. Assistant could not store that note, only contact-channel/travel-notice preferences, and advised reporting the card in-app/by phone: replacement ships within 5 business days free, but recurring merchants need the new number. No case/transaction IDs. Case outcomes: no case touched. Lesson: none

## eid-tick-29  ·  maintenance  ·  2026-12-08T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": [], "case_followups_repaired": []}`

## eid-29  ·  session  ·  marco  ·  2026-12-08T10:00:00Z

_Resumes session `eid`._

**Customer:** Hi again, I'm planning a trip to Kyoto in the spring. Nothing to set up yet.

**Assistant:** Got it - I've not set anything up, since you said nothing's needed yet. When your dates firm up, tell me the destination and your return date and I can add a travel notice to your profile, which helps keep card use abroad from being flagged as unusual. Enjoy the planning - Kyoto in spring is a good pick.

_Episode written:_ Conversation on 2026-12-08: The customer said they are planning a trip to Kyoto in spring (not verified) and that nothing needs setting up yet. No case or transaction IDs were mentioned. The assistant did not set anything up and explained a travel notice can be added later once the customer provides destination and return date. Case outcomes: no case touched. Lesson: none

## eid-tick-58  ·  maintenance  ·  2027-01-06T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": ["eid"], "case_followups_repaired": []}`

## eid-58  ·  session  ·  marco  ·  2027-01-06T10:00:00Z

_Resumes session `eid`._

**Customer:** Hello, I got a new phone, so I might be on a new number soon. That's all.

**Assistant:** Got it - thanks for the heads-up. Nothing on your account changes until you tell me, and your contact channel is currently unset, so follow-ups and reminders go by secure message in the Kestrel app.

If you do want to switch to a new number later, just say so here and I'll walk you through it (it takes a quick identity check and a one-time code).

_Episode written:_ Conversation on 2027-01-06: The customer said they got a new phone and may soon use a new number (not verified). The assistant acknowledged it, said nothing changes until requested, and noted the contact channel is unset so follow-ups/reminders go by secure message in the Kestrel app. They offered to walk through a number change later. No case/transaction IDs appeared. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | three conversations, three episodes: the day-0 episode is not overwritten by a reused id | `3 episodes; purged 0` |
| PASS | episodic | the day-0 episode survives (its harness-written opening, not a word the model may paraphrase away) | `3 episodes; mentioning 'Conversation on 2026-11-09': ['E-eid-1-44cc09']` |
