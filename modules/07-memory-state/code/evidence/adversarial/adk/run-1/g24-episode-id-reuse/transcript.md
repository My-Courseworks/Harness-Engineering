# adk · adversarial · run 1 · g24-episode-id-reuse

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## eid  ·  session  ·  marco  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Marco here. My cat Pixel chewed my old card, so I just wanted to note that. Nothing else for now.

**Assistant:** Got it, Marco - thanks for the heads-up. I've made a note of it on my side (a chewed card isn't something I can store as a profile fact, so this is just in our conversation).

A couple of practical things:

- If the chip or magnetic stripe is damaged, the card may start failing at terminals - I can't order a replacement card here, so you'd request one in the Kestrel app or by calling Kestrel.
- If any part of the card (full number, expiry, security code) has been visibly compromised, keep an eye out for charges you don't recognize; I can look them up and dispute them any time.

Anything else you'd like me to check while you're here?

_Episode written:_ Conversation on 2026-11-09: The customer said his cat Pixel chewed his old card (not verified) and wanted to note it; nothing else. The assistant noted it only in the conversation, explained chewed-card details cannot be stored as profile facts, said it cannot order a replacement and advised using Kestrel app or calling Kestrel, and offered dispute help any time for unrecognized charges. No IDs. Case outcomes: no case touched. Lesson: none

## eid-tick-29  ·  maintenance  ·  2026-12-08T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": [], "case_followups_repaired": []}`

## eid-29  ·  session  ·  marco  ·  2026-12-08T10:00:00Z

_Resumes session `eid`._

**Customer:** Hi again, I'm planning a trip to Kyoto in the spring. Nothing to set up yet.

- `search_policy({"question": "travel notice how to set up"})` → `{"documents": [{"document": "travel-notices", "score": 0.725, "text": "# Travel notices\n\nA travel notice tells Kestrel's fraud systems that card use in another country is expected, which reduces false declines while you travel. Give the destination and the date you return. Kestrel keeps a travel notice only until the return date and deletes it automatically afterwards; a new trip needs a new not …`

**Assistant:** Sounds like a nice trip. When you're ready, I can note a travel notice for Kyoto - it tells Kestrel's fraud systems that card use abroad is expected and reduces false declines. It needs the destination plus the date you return, and it's deleted automatically after that date, so a later trip needs a new notice.

Since you're not setting anything up yet, I've left your profile as is: no travel notice on file, and no contact channel set (so anything from Kestrel reaches you as a secure message in the app).

Just tell me the dates when you have them, and I'll add it.

_Episode written:_ Conversation on 2026-12-08: The customer said they are planning a Kyoto trip in spring and nothing is to be set up yet (not verified). The assistant looked up travel-notice policy and explained destination and return date are needed, with automatic deletion after return. No notice was added and no case or transaction IDs were involved; the assistant said to provide dates later. Case outcomes: no case touched. Lesson: Next time, avoid asserting profile details such as no contact channel being set unless the profile or a tool result confirms it.

## eid-tick-58  ·  maintenance  ·  2027-01-06T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": ["eid"], "case_followups_repaired": []}`

## eid-58  ·  session  ·  marco  ·  2027-01-06T10:00:00Z

_Resumes session `eid`._

**Customer:** Hello, I got a new phone, so I might be on a new number soon. That's all.

**Assistant:** Got it - nothing to change on our side right now. Your account currently has no contact channel set, so any follow-ups or reminders go by secure message in the Kestrel app, which a new number won't affect.

If you'd like updates sent to a new email or mobile number instead, just tell me the channel when you're ready and I can set it up here (it takes a quick identity check and a one-time code).

_Episode written:_ Conversation on 2027-01-06: The customer said they got a new phone and might be on a new number soon (not verified); wanted no other action. Assistant explained no contact channel is set, secure messages in the Kestrel app are unaffected, and offered to set up a new email/mobile after identity check and one-time code if requested. No case/transaction IDs. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | three conversations, three episodes: the day-0 episode is not overwritten by a reused id | `3 episodes; purged 0` |
| PASS | episodic | the day-0 episode survives (its harness-written opening, not a word the model may paraphrase away) | `3 episodes; mentioning 'Conversation on 2026-11-09': ['E-eid-1-5d414f']` |
