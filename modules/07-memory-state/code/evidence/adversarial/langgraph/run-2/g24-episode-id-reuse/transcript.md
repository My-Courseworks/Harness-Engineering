# langgraph · adversarial · run 2 · g24-episode-id-reuse

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## eid  ·  session  ·  marco  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Marco here. My cat Pixel chewed my old card, so I just wanted to note that. Nothing else for now.

- `search_policy({"question": "damaged card replacement"})` → `{"documents": [{"document": "card-replacement", "score": 0.751, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.632, "text": "# Dispute window\n …`

**Assistant:** Thanks, Marco - noted here in the chat. One thing I should be straight about: I have no tool to log a damaged card on your account, so this message doesn't start a replacement. Only a contact channel or travel notice can be saved as a fact about you.

To actually get a new card, report it to Kestrel (in the app or by calling the number on the back of your card). Per policy, a reported damaged/lost card is blocked and a replacement ships within 5 business days at no charge - and you'll need to give recurring merchants the new number yourself, as Kestrel doesn't forward it.

Anything else I can help with?

_Episode written:_ Conversation on 2026-11-09: The customer said (not verified) his cat Pixel chewed his old card and he only wanted to note it. The assistant searched policy and noted the chat but could not log the card; no case/transaction ID or replacement created; no promise made. He was directed to report via app or card-back number; policy cites 5 business days for replacement. Case outcomes: no case touched. Lesson: none

## eid-tick-29  ·  maintenance  ·  2026-12-08T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": []}`

## eid-29  ·  session  ·  marco  ·  2026-12-08T10:00:00Z

_Resumes session `eid`._

**Customer:** Hi again, I'm planning a trip to Kyoto in the spring. Nothing to set up yet.

**Assistant:** Sounds like a good trip. Nothing set up on my end - your travel notice is still empty, and no reminders or follow-ups pending.

When your dates firm up, I can add a travel notice for Kyoto (just the destination and return date) so your card isn't flagged for use abroad. Anything else I can help with today?

_Episode written:_ Conversation on 2026-12-08: The customer said they were planning a spring trip to Kyoto and had nothing to set up yet (not verified). The assistant stated that the travel notice, reminders, and follow-ups were empty and offered to add a Kyoto travel notice with destination and return date once dates are firm. No case or transaction IDs. Case outcomes: no case touched. Lesson: none

## eid-tick-58  ·  maintenance  ·  2027-01-06T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": ["eid"]}`

## eid-58  ·  session  ·  marco  ·  2027-01-06T10:00:00Z

_Resumes session `eid`._

**Customer:** Hello, I got a new phone, so I might be on a new number soon. That's all.

**Assistant:** Got it - thanks for the heads-up. I haven't changed anything, since you haven't given me a new number yet.

For reference, your contact preference is currently unset, so any follow-ups or reminders reach you by secure message in the Kestrel app rather than by text. If you'd like them sent to the new number once you have it, just tell me and I'll update it - I'll need your card's last 4 digits and billing ZIP to make that change.

_Episode written:_ Conversation on 2027-01-06: Customer said they got a new phone and might soon have a new number (not verified). Assistant made no changes, as no new number was provided. Contact preference is unset, so reminders go via secure message in the Kestrel app. Assistant said a future number update would require card and billing verification; no case or transaction IDs. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | three conversations, three episodes: the day-0 episode is not overwritten by a reused id | `3 episodes; purged 0` |
| PASS | episodic | the day-0 episode survives (its harness-written opening, not a word the model may paraphrase away) | `3 episodes; mentioning 'Conversation on 2026-11-09': ['E-eid-1-c3e1ed']` |
