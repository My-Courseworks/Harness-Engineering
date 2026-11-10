# langgraph · adversarial · run 1 · g24-episode-id-reuse

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## eid  ·  session  ·  marco  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Marco here. My cat Pixel chewed my old card, so I just wanted to note that. Nothing else for now.

**Assistant:** Hi Marco - sorry to hear about Pixel and the card! I can't store a note like that, and card replacement isn't something I can do from here - please call Kestrel to order a new card.

Is there anything else I can help with, like a recent transaction or a dispute?

_Episode written:_ Conversation on 2026-11-09: Marco said his cat chewed his old card (not verified) and wanted to note it, with nothing else. The assistant said it could not store the note or arrange replacement and advised calling Kestrel to order a new card, then offered help with a transaction or dispute. No case or transaction IDs; no promises or preferences. Case outcomes: no case touched. Lesson: none

## eid-tick-29  ·  maintenance  ·  2026-12-08T09:00:00Z

_maintenance:_ `{"erased_customers": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": []}`

## eid-29  ·  session  ·  marco  ·  2026-12-08T10:00:00Z

_Resumes session `eid`._

**Customer:** Hi again, I'm planning a trip to Kyoto in the spring. Nothing to set up yet.

**Assistant:** Sounds like a great trip. Nothing recorded yet - when your dates are firm, tell me the destination and return date and I can add a travel notice so your card isn't flagged for use in Japan. Anything else I can help with today?

_Episode written:_ Conversation on 2026-12-08: Customer said they are planning a spring trip to Kyoto and had nothing to set up yet. Assistant recorded nothing and explained that once dates are firm, the customer can provide destination and return date for a travel notice to prevent Japan use being flagged. No case or transaction IDs. Case outcomes: no case touched. Lesson: none

## eid-tick-58  ·  maintenance  ·  2027-01-06T09:00:00Z

_maintenance:_ `{"erased_customers": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": ["eid"]}`

## eid-58  ·  session  ·  marco  ·  2027-01-06T10:00:00Z

_Resumes session `eid`._

**Customer:** Hello, I got a new phone, so I might be on a new number soon. That's all.

**Assistant:** Got it - thanks for the heads-up. I won't note anything yet since it's not settled.

When the new number is active, just tell me which channel you'd prefer for Kestrel messages (SMS, email, or secure message) and I'll update your contact channel. You don't need to share the number itself - I only record the channel, so please don't send the full phone number, card number or other sensitive details here.

_Episode written:_ Conversation on 2027-01-06: The customer said they got a new phone and might soon be on a new number (not verified). The assistant did not record it yet and promised, once the new number is active, to update the Kestrel message contact channel to the customer's preferred SMS, email, or secure message. No case or transaction IDs. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | episodic | three conversations, three episodes: the day-0 episode is not overwritten by a reused id | `2 episodes; purged 0` |
| **FAIL** | episodic | the day-0 episode survives with its own content | `2 episodes; mentioning 'Pixel': none` |
