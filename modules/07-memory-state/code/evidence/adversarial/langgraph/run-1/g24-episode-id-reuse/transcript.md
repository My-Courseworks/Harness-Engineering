# langgraph · adversarial · run 1 · g24-episode-id-reuse

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## eid  ·  session  ·  marco  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Marco here. My cat Pixel chewed my old card, so I just wanted to note that. Nothing else for now.

- `search_policy({"question": "damaged card replacement"})` → `{"documents": [{"document": "card-replacement", "score": 0.751, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.632, "text": "# Dispute window\n …`

**Assistant:** Hi Marco - noted, though I should be straight with you: I can't file a general note on the account, and I have no tool here to order a replacement card. What Kestrel's policy says: report a damaged card and Kestrel blocks it and ships a replacement within 5 business days at no charge - so it's worth reporting it through the app or by calling Kestrel rather than leaving it for later. One thing to remember: recurring merchants will need the new card number from you; Kestrel doesn't forward it.

Anything you'd like me to look up or do while you're here?

_Episode written:_ Conversation on 2026-11-09: Marco said his cat Pixel chewed his old card (not verified); he wanted to note it, nothing else. Assistant searched damaged-card policy, said it couldn't add a general note or order a replacement, and advised reporting via app/phone. Policy: replacement within 5 business days, no charge; recurring merchants need new number. No case/transaction IDs. Case outcomes: no case touched. Lesson: none

## eid-tick-29  ·  maintenance  ·  2026-12-08T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": []}`

## eid-29  ·  session  ·  marco  ·  2026-12-08T10:00:00Z

_Resumes session `eid`._

**Customer:** Hi again, I'm planning a trip to Kyoto in the spring. Nothing to set up yet.

**Assistant:** Hi! Sounds like a good trip. Nothing set up then - when your dates are settled, just tell me the destination and return date and I can add a travel notice to your profile (optional, but it helps avoid card interruptions while you're away).

For now, nothing is scheduled and no travel notice is on file. Anything else I can help with?

_Episode written:_ Conversation on 2026-12-08: Customer said they are planning a trip to Kyoto in spring (not verified) and nothing to set up yet. Assistant noted no travel notice on file and explained an optional travel notice can be added once dates are settled; no case or transaction IDs. Case outcomes: no case touched. Lesson: none

## eid-tick-58  ·  maintenance  ·  2027-01-06T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": ["eid"]}`

## eid-58  ·  session  ·  marco  ·  2027-01-06T10:00:00Z

_Resumes session `eid`._

**Customer:** Hello, I got a new phone, so I might be on a new number soon. That's all.

**Assistant:** Got it - noted for whenever it happens.

For now your contact channel isn't set, so anything we send (dispute follow-ups, reminders) goes as a secure message in the Kestrel app, so a new number won't cut anything off. If you'd like to switch to SMS once the new number is active, just tell me then - I'll need your card's last 4 digits and billing ZIP to verify before I can change the channel.

_Episode written:_ Conversation on 2027-01-06: Customer said new phone and possible new number soon (not verified); no clear request. Assistant promised to note it for whenever it happens and explained messages go as secure Kestrel-app messages since contact channel is unset. If customer later wants SMS, assistant said to ask then and provide verification details. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | three conversations, three episodes: the day-0 episode is not overwritten by a reused id | `3 episodes; purged 0` |
| PASS | episodic | the day-0 episode survives (its harness-written opening, not a word the model may paraphrase away) | `3 episodes; mentioning 'Conversation on 2026-11-09': ['E-eid-1-f74570']` |
