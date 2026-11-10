# langgraph · adversarial · run 1 · g24-episode-id-reuse

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## eid  ·  session  ·  marco  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Marco here. My cat Pixel chewed my old card, so I just wanted to note that. Nothing else for now.

**Assistant:** Sorry to hear about Pixel - and the card. I've noted it here, but nothing on your account has changed from it.

If the card is damaged and you need a replacement, that's handled by calling the number on the back of your card or via the Kestrel app - I don't have a tool to order one. And if any charges show up that Pixel somehow managed to make, tell me and I can look into a dispute.

Anything else you'd like me to do while you're here?

_Episode written:_ Conversation on 2026-11-09: Marco said his cat Pixel chewed his old card (not verified) and wanted it noted; no other request. The assistant noted it but made no account changes and said replacement requires calling the number on the card or using the Kestrel app; no case or transaction IDs, promises, or preferences were stated. Case outcomes: no case touched. Lesson: none

## eid-tick-29  ·  maintenance  ·  2026-12-08T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "case_followups_repaired": [], "purged_episodes": [], "deleted_transcripts": []}`

## eid-29  ·  session  ·  marco  ·  2026-12-08T10:00:00Z

_Resumes session `eid`._

**Customer:** Hi again, I'm planning a trip to Kyoto in the spring. Nothing to set up yet.

**Assistant:** Got it - Kyoto in the spring sounds great. I won't set anything up since you said not to yet.

When you're ready, just say the word and I can add a travel notice to your account (destination and return date) so your card isn't flagged for use abroad. Anything else in the meantime?

_Episode written:_ Conversation on 2026-12-08: The customer said they are planning a Kyoto trip in spring and nothing needs to be set up yet. The assistant acknowledged this and did not set anything up, offering to add a travel notice when the customer is ready. No case or transaction IDs were provided; no preferences beyond waiting to set up. Case outcomes: no case touched. Lesson: none

## eid-tick-58  ·  maintenance  ·  2027-01-06T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "case_followups_repaired": [], "purged_episodes": [], "deleted_transcripts": ["eid"]}`

## eid-58  ·  session  ·  marco  ·  2027-01-06T10:00:00Z

_Resumes session `eid`._

**Customer:** Hello, I got a new phone, so I might be on a new number soon. That's all.

**Assistant:** Got it - nothing to change yet, then. A couple of things worth knowing for when your new number is active:

- Your contact channel is currently not set, so follow-ups and reminders go by secure message in the Kestrel app. If you'd like them to reach you by text or email instead, just tell me and I'll set that up (it takes a quick identity check and a one-time code).
- Also update your number with the bank directly, since that's the number Kestrel holds on the account - I can't change it here.

Message me whenever you're ready, or if there's anything else.

_Episode written:_ Conversation on 2027-01-06: Customer said they got a new phone and might soon be on a new number, but had no change request (not verified). No case or transaction IDs. Assistant noted contact channel is unset, so follow-ups go by secure message in the Kestrel app; customer can request text/email after identity check and one-time code, and must update number with the bank directly. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | three conversations, three episodes: the day-0 episode is not overwritten by a reused id | `3 episodes; purged 0` |
| PASS | episodic | the day-0 episode survives (its harness-written opening, not a word the model may paraphrase away) | `3 episodes; mentioning 'Conversation on 2026-11-09': ['E-eid-1-65b001']` |
