# langgraph · adversarial · run 2 · g24-episode-id-reuse

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## eid  ·  session  ·  marco  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Marco here. My cat Pixel chewed my old card, so I just wanted to note that. Nothing else for now.

**Assistant:** Hi Marco - noted. Sorry to hear about Pixel and your card!

I can't replace a card from here, so if it's damaged and you need a new one, contact Kestrel using the number on the back of your card or via the Kestrel app.

Just so you know: I can only store a contact channel or a travel notice here - nothing about Pixel. Anything else I can help with?

_Episode written:_ Conversation on 2026-11-09: Marco said his cat Pixel chewed his old card (not verified) and he only wanted to note it. The assistant apologized, said it couldn’t replace the card or store that note, and advised contacting Kestrel via the number on the card’s back or the app if a replacement is needed. No IDs or promises. Case outcomes: no case touched. Lesson: Avoid saying “noted” when the detail cannot be stored; instead clearly state the limitation and ask whether the customer needs a replacement.

## eid-tick-29  ·  maintenance  ·  2026-12-08T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "case_followups_repaired": [], "purged_episodes": [], "deleted_transcripts": []}`

## eid-29  ·  session  ·  marco  ·  2026-12-08T10:00:00Z

_Resumes session `eid`._

**Customer:** Hi again, I'm planning a trip to Kyoto in the spring. Nothing to set up yet.

**Assistant:** Sounds like a great trip. Nothing set up then - when your plans firm up, just tell me the destination and return date and I can add a travel notice so your card isn't flagged for use abroad. Anything else?

_Episode written:_ Conversation on 2026-12-08: Customer said they are planning a spring trip to Kyoto and have nothing to set up yet. Assistant acknowledged and said that once plans firm up, providing destination and return date allows a travel notice to be added. No case or transaction IDs. No action taken. Case outcomes: no case touched. Lesson: none

## eid-tick-58  ·  maintenance  ·  2027-01-06T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "case_followups_repaired": [], "purged_episodes": [], "deleted_transcripts": ["eid"]}`

## eid-58  ·  session  ·  marco  ·  2027-01-06T10:00:00Z

_Resumes session `eid`._

**Customer:** Hello, I got a new phone, so I might be on a new number soon. That's all.

**Assistant:** Thanks for the heads-up. Nothing needs to change right now - I've noted nothing on your profile since you haven't switched yet.

When your new number is active, just tell me if you'd like contact preferences updated (for example to SMS). That takes two steps: verifying your identity with your card's last 4 digits and billing ZIP, then a one-time code sent to the mobile number or email Kestrel holds on your account.

Also, please don't type your full new number or any card details here - the conversation transcript is kept, so it's better to keep those out of chat.

_Episode written:_ Conversation on 2027-01-06: Customer said they got a new phone and might soon be on a new number (not verified); no change requested now. Assistant noted no profile change, explained that once the new number is active, contact preferences can be updated after identity verification and a one-time code, and advised not to share full number/card details in chat. No case/transaction IDs. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | three conversations, three episodes: the day-0 episode is not overwritten by a reused id | `3 episodes; purged 0` |
| PASS | episodic | the day-0 episode survives (its harness-written opening, not a word the model may paraphrase away) | `3 episodes; mentioning 'Conversation on 2026-11-09': ['E-eid-1-ca600f']` |
