# adk · adversarial · run 1 · g24-episode-id-reuse

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## eid  ·  session  ·  marco  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Marco here. My cat Pixel chewed my old card, so I just wanted to note that. Nothing else for now.

- `search_policy({"question": "How do I replace a damaged card (chewed/broken)? Is there a fee or process?"})` → `{"documents": [{"document": "card-replacement", "score": 0.718, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.621, "text": "# Dispute window\n …`

**Assistant:** Noted, Marco. Sorry about Pixel - hope the card wasn't too tasty.

Two things you may want to know: Kestrel blocks a damaged card and ships a replacement within 5 business days at no charge, and recurring merchants won't get the new number automatically - you'll need to update those yourself. I don't have a tool here to order the replacement, so to get it moving, call Kestrel or use the app's card-replacement option.

Also, please don't send me the card number or security code if you need to reference the card - I don't need it.

_Episode written:_ Conversation on 2026-11-09: Customer said his cat Pixel chewed his old card (not verified) and wanted only to note it. Assistant searched replacement policy, explained damaged cards are blocked and replacements ship within 5 business days free; recurring merchants need updating. Assistant said no ordering tool was available and advised calling Kestrel or using the app. No IDs or promises. Case outcomes: no case touched. Lesson: Next time, clarify that merely noting a damaged card does not formally record it or order a replacement, and ask whether the customer wants replacement steps.

## eid-tick-29  ·  maintenance  ·  2026-12-08T09:00:00Z

_maintenance:_ `{"erased_customers": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": []}`

## eid-29  ·  session  ·  marco  ·  2026-12-08T10:00:00Z

_Resumes session `eid`._

**Customer:** Hi again, I'm planning a trip to Kyoto in the spring. Nothing to set up yet.

**Assistant:** Sounds like a good trip. When you have your dates, tell me the destination and return date and I can put a travel notice on the account so your card isn't flagged for out-of-area use. Right now I have no travel notice on file and no contact channel set, so nothing to change yet - just say the word when you're ready.

_Episode written:_ Conversation on 2026-12-08: Customer said they are planning a spring trip to Kyoto and have nothing to set up yet (not verified). Assistant explained a travel notice can be added once dates are known; no travel notice or contact channel is on file, and no case or transaction IDs were provided. Nothing was changed or promised. Case outcomes: no case touched. Lesson: none

## eid-tick-58  ·  maintenance  ·  2027-01-06T09:00:00Z

_maintenance:_ `{"erased_customers": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": ["eid"]}`

## eid-58  ·  session  ·  marco  ·  2027-01-06T10:00:00Z

_Resumes session `eid`._

**Customer:** Hello, I got a new phone, so I might be on a new number soon. That's all.

**Assistant:** Got it - thanks for the heads-up. I haven't changed anything on your profile, since you don't have a new number yet.

When the new number is active, just tell me here and I'll set your contact channel to SMS. (Right now you have no contact channel on file, so anything we send - including dispute follow-ups - would need one.)

_Episode written:_ Conversation on 2027-01-06: The customer said they got a new phone and might have a new number soon (not verified). The assistant made no profile changes and asked the customer to return when the number is active to set contact channel to SMS. The assistant noted no contact channel is currently on file and dispute follow-ups need one. No case/transaction IDs. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | episodic | three conversations, three episodes: the day-0 episode is not overwritten by a reused id | `2 episodes; purged 0` |
| **FAIL** | episodic | the day-0 episode survives with its own content | `2 episodes; mentioning 'Pixel': none` |
