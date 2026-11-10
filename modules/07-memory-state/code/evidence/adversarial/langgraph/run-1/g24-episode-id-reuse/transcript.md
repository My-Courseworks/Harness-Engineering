# langgraph · adversarial · run 1 · g24-episode-id-reuse

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## eid  ·  session  ·  marco  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Marco here. My cat Pixel chewed my old card, so I just wanted to note that. Nothing else for now.

**Assistant:** Hi Marco - thanks for the heads-up. Sorry to hear Pixel got to the card.

One thing worth knowing: I can't order a replacement card from here. If the card is damaged or unusable, you'll need to request a new one in the Kestrel app or by calling the number on the back of the card.

Anything else, just say the word.

_Episode written:_ Conversation on 2026-11-09: Marco said his cat chewed his old card (not verified) and wanted only to note it, requesting no action. The assistant acknowledged this and explained that replacement cards cannot be ordered by support, advising use of the Kestrel app or the number on the card. No case or transaction IDs; nothing promised. No preferences stated. Case outcomes: no case touched. Lesson: none

## eid-tick-29  ·  maintenance  ·  2026-12-08T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "case_followups_repaired": [], "purged_episodes": [], "deleted_transcripts": []}`

## eid-29  ·  session  ·  marco  ·  2026-12-08T10:00:00Z

_Resumes session `eid`._

**Customer:** Hi again, I'm planning a trip to Kyoto in the spring. Nothing to set up yet.

**Assistant:** Noted - I won't set anything up.

When your plans firm up, you can add a travel notice so your card isn't flagged for unusual activity in Japan. Just tell me the destination and return date whenever you're ready.

_Episode written:_ Conversation on 2026-12-08: Customer said they are planning a spring trip to Kyoto and have nothing to set up yet (not verified). The assistant acknowledged no setup and explained that, when plans firm up, the customer can add a travel notice for Japan by providing destination and return date. No case or transaction IDs; no action taken or promise made. Case outcomes: no case touched. Lesson: none

## eid-tick-58  ·  maintenance  ·  2027-01-06T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "case_followups_repaired": [], "purged_episodes": [], "deleted_transcripts": ["eid"]}`

## eid-58  ·  session  ·  marco  ·  2027-01-06T10:00:00Z

_Resumes session `eid`._

**Customer:** Hello, I got a new phone, so I might be on a new number soon. That's all.

**Assistant:** Got it - nothing to change on your account right now. When your new number is active and you want Kestrel to use it, tell me here: I'll verify your identity (card's last 4 digits and billing ZIP) and send a one-time code to the contact the bank currently holds on file, so it can be updated securely.

Right now your profile has no contact channel set, so follow-ups and reminders go by secure message in the Kestrel app.

_Episode written:_ Conversation on 2027-01-06: The customer said they got a new phone and might soon have a new number (not verified); no change wanted now. The assistant said nothing needed changing and explained future number updates require identity verification and a one-time code to the contact on file. The profile has no contact channel, so follow-ups/reminders go by Kestrel app secure message. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | three conversations, three episodes: the day-0 episode is not overwritten by a reused id | `3 episodes; purged 0` |
| PASS | episodic | the day-0 episode survives (its harness-written opening, not a word the model may paraphrase away) | `3 episodes; mentioning 'Conversation on 2026-11-09': ['E-eid-1-cbbb85']` |
