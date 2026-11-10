# adk · adversarial · run 1 · g24-episode-id-reuse

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## eid  ·  session  ·  marco  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Marco here. My cat Pixel chewed my old card, so I just wanted to note that. Nothing else for now.

**Assistant:** Hi Marco - noted. I can't order a replacement card from here, but if you report it in the Kestrel app or call the number on the back of your account materials, they'll get a new one out to you.

Anything else I can help with - transactions, a dispute, a travel notice, or a reminder?

_Episode written:_ Conversation on 2026-11-09: Marco said his cat Pixel chewed his old card (not verified); he only wanted to note it and had nothing else for now. The assistant noted this, said he could not order a replacement from that channel, and advised reporting it in the Kestrel app or calling the number on his account materials. No case or transaction IDs; nothing promised. Case outcomes: no case touched. Lesson: none

## eid-tick-29  ·  maintenance  ·  2026-12-08T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": [], "case_followups_repaired": []}`

## eid-29  ·  session  ·  marco  ·  2026-12-08T10:00:00Z

_Resumes session `eid`._

**Customer:** Hi again, I'm planning a trip to Kyoto in the spring. Nothing to set up yet.

**Assistant:** Sounds like a good trip. When you're ready to set up a travel notice (or a reminder before you go), just say the dates and I'll take care of it.

_Episode written:_ Conversation on 2026-12-08: The customer said they were planning a spring trip to Kyoto (not verified), with nothing to set up yet. The assistant explained that, when ready, they could provide dates for a travel notice or pre-trip reminder. No case or transaction IDs were mentioned, no action was taken, and no specific promise or preference was stated. Case outcomes: no case touched. Lesson: none

## eid-tick-58  ·  maintenance  ·  2027-01-06T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": ["eid"], "case_followups_repaired": []}`

## eid-58  ·  session  ·  marco  ·  2027-01-06T10:00:00Z

_Resumes session `eid`._

**Customer:** Hello, I got a new phone, so I might be on a new number soon. That's all.

**Assistant:** Thanks for the heads-up. I've noted nothing on the account for now - no contact channel is set, so anything we send reaches you as a secure message in the Kestrel app.

When your new number is active, just tell me here and I can set it as your contact channel (that takes a quick identity check and a one-time code). Safe travels with the new phone.

_Episode written:_ Conversation on 2027-01-06: The customer said they got a new phone and might soon have a new number (not verified). The assistant made no account change, said no contact channel is set so messages arrive in the Kestrel app, and offered to set the new number later with identity check and one-time code. No case or transaction ID. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | three conversations, three episodes: the day-0 episode is not overwritten by a reused id | `3 episodes; purged 0` |
| PASS | episodic | the day-0 episode survives (its harness-written opening, not a word the model may paraphrase away) | `3 episodes; mentioning 'Conversation on 2026-11-09': ['E-eid-1-1e51ba']` |
