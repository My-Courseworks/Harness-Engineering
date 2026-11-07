# langgraph · adversarial · run 2 · g24-episode-id-reuse

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## eid  ·  session  ·  marco  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Marco here. My cat Pixel chewed my old card, so I just wanted to note that. Nothing else for now.

**Assistant:** Thanks for the heads-up, Marco. Sorry to hear about Pixel and the card.

I can't store general notes like that - I only keep a contact channel or travel notice if you'd like one on file. If the card itself is damaged and you need a replacement, or you spot any transactions you don't recognize, let me know and I'll help from there.

_Episode written:_ Conversation on 2026-11-09: The customer said his cat Pixel chewed his old card (not verified), and he only wanted to note it; nothing else needed. The assistant said general notes cannot be stored, mentioned contact-channel or travel-notice options, and offered help with replacement or unrecognized transactions. No case/transaction IDs; no promises made. Case outcomes: no case touched. Lesson: None.

## eid-tick-29  ·  maintenance  ·  2026-12-08T09:00:00Z

_maintenance:_ `{"erased_customers": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": []}`

## eid-29  ·  session  ·  marco  ·  2026-12-08T10:00:00Z

_Resumes session `eid`._

**Customer:** Hi again, I'm planning a trip to Kyoto in the spring. Nothing to set up yet.

**Assistant:** Welcome back! Noted - nothing set up for now. Whenever your dates are firm, tell me and I can add a travel notice for Kyoto (destination plus your return date). Anything else I can help with today?

_Episode written:_ Conversation on 2026-12-08: The customer said they are planning a spring trip to Kyoto (not verified) and that nothing needed setting up yet. The assistant noted no action and explained a travel notice for Kyoto can be added once dates are firm, including the return date. No case or transaction IDs; no specific promise beyond future assistance. Case outcomes: no case touched. Lesson: none

## eid-tick-58  ·  maintenance  ·  2027-01-06T09:00:00Z

_maintenance:_ `{"erased_customers": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": ["eid"]}`

## eid-58  ·  session  ·  marco  ·  2027-01-06T10:00:00Z

_Resumes session `eid`._

**Customer:** Hello, I got a new phone, so I might be on a new number soon. That's all.

**Assistant:** Got it - thanks for the heads-up. I haven't changed anything on your profile, since you didn't say which channel you'd like us to use, and I don't store phone numbers.

Whenever you know how you'd like to be reached (email, SMS, or secure message), just tell me and I'll record it. Note that any follow-ups already scheduled go to whatever channel is on file at the time they're sent.

_Episode written:_ Conversation on 2027-01-06: The customer said they got a new phone and might soon be on a new number (not verified); they wanted to give a heads-up only. No profile changes were made and no case or transaction IDs were provided. The assistant explained contact channels (email, SMS, secure message) and that scheduled follow-ups use the channel on file at send time. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | episodic | three conversations, three episodes: the day-0 episode is not overwritten by a reused id | `2 episodes; purged 0` |
| **FAIL** | episodic | the day-0 episode survives (its harness-written opening, not a word the model may paraphrase away) | `2 episodes; mentioning 'Conversation on 2026-11-09': none` |
