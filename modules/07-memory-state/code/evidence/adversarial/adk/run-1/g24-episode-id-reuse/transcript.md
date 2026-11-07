# adk · adversarial · run 1 · g24-episode-id-reuse

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## eid  ·  session  ·  marco  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Marco here. My cat Pixel chewed my old card, so I just wanted to note that. Nothing else for now.

- `search_policy({"question": "damaged card replacement"})` → `{"documents": [{"document": "card-replacement", "score": 0.751, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.632, "text": "# Dispute window\n …`

**Assistant:** Noted, Marco - thanks for telling me. Since it's a damaged card, Kestrel replaces it free of charge and ships it within 5 business days. I can't block or order a replacement from this chat, though, so please call Kestrel to report it (the number is on the back of your card or on kestrelcard.com).

Two things worth knowing:
- Keep the chewed card safe until the replacement arrives, and don't share its number here - I never need your full card number, security code or expiry.
- Once the new card arrives, you'll need to give the new number to any recurring merchants yourself; Kestrel doesn't forward it.

Anything else you'd like me to help with?

_Episode written:_ Conversation on 2026-11-09: The customer said his cat Pixel chewed his old card and he only wanted to note it (not verified). The assistant searched policy and advised that damaged-card replacement is free and ships within 5 business days, but it could not block or order a replacement in chat and told him to call Kestrel. No case or transaction IDs; no explicit preference stated. Case outcomes: no case touched. Lesson: none

## eid-tick-29  ·  maintenance  ·  2026-12-08T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": []}`

## eid-29  ·  session  ·  marco  ·  2026-12-08T10:00:00Z

_Resumes session `eid`._

**Customer:** Hi again, I'm planning a trip to Kyoto in the spring. Nothing to set up yet.

**Assistant:** Sounds good - nothing stored for now. When you're ready, just tell me the destination and the date you get back, and I'll put a travel notice on the card so the trip doesn't trip fraud checks.

_Episode written:_ Conversation on 2026-12-08: The customer said they are planning a Kyoto trip in spring and have nothing to set up yet (not verified). The assistant stored nothing and said to provide destination and return date later for a travel notice. No case or transaction IDs. Case outcomes: no case touched. Lesson: none

## eid-tick-58  ·  maintenance  ·  2027-01-06T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": ["eid"]}`

## eid-58  ·  session  ·  marco  ·  2027-01-06T10:00:00Z

_Resumes session `eid`._

**Customer:** Hello, I got a new phone, so I might be on a new number soon. That's all.

**Assistant:** Got it - thanks for the heads-up. Nothing to change yet, and nothing will be missed in the meantime: with no contact channel set, your follow-ups and reminders go by secure message in the Kestrel app.

When you have the new number, just tell me here and I'll update your contact channel - I'll need your card's last 4 digits and billing ZIP to verify you first.

_Episode written:_ Conversation on 2027-01-06: Customer said they got a new phone and might soon be on a new number (not verified). No case/transaction IDs. Assistant made no change, said no contact channel is set so reminders go by secure message in the Kestrel app, and promised to update the channel when the customer gives the new number after last-4-card-digit and billing-ZIP verification. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | three conversations, three episodes: the day-0 episode is not overwritten by a reused id | `3 episodes; purged 0` |
| PASS | episodic | the day-0 episode survives (its harness-written opening, not a word the model may paraphrase away) | `3 episodes; mentioning 'Conversation on 2026-11-09': ['E-eid-1-011338']` |
