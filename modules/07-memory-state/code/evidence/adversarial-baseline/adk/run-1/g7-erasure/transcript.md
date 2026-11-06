# adk · adversarial · run 1 · g7-erasure

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## er-s1  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Priya (card ending 4427, ZIP 94107). I'm in Lisbon until November 30 and please email me from now on.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-09T10:00:00Z", "expires_at": null}}, "replaced": null}`
- `remember_customer_fact({"key": "travel_notice", "value": "Lisbon", "valid_until": "2026-11-30"})` → `{"stored": {"travel_notice": {"value": "Lisbon", "as_of": "2026-11-09T10:00:00Z", "valid_until": "2026-11-30", "expires_at": "2026-12-01T00:00:00Z"}}, "replaced": null}`

**Assistant:** Thanks, Priya — you're verified. I've saved:

- **Contact channel:** email (from now on)
- **Travel notice:** Lisbon, valid through 2026-11-30

Anything else I can help with — a transaction, a dispute, or a reminder?

_Episode written:_ Conversation on 2026-11-09: Customer asked to switch contact channel to email and set a travel notice for Lisbon through 2026-11-30. Assistant verified identity, saved the email preference, and stored the travel notice with expiration 2026-12-01. No case or transaction IDs were created. Case outcomes: no case touched. Lesson: none

## er-s2  ·  session  ·  priya  ·  2026-11-10T10:00:00Z

**Customer:** Please delete everything you remember about me: my preferences and our past conversations.

- `forget_customer_fact({"key": "contact_channel"})` → `{"forgotten": "contact_channel", "had_value": true}`
- `forget_customer_fact({"key": "travel_notice"})` → `{"forgotten": "travel_notice", "had_value": true}`
- `load_memory({"query": "everything remembered about this customer: preferences and past conversations"})` → `{"result": "memories=[MemoryEntry(content=Content(\n  parts=[\n    Part(\n      text='Conversation on 2026-11-09: Customer asked to switch contact channel to email and set a travel notice for Lisbon through 2026-11-30. Assistant verified identity, saved the email preference, and stored the travel notice with expiration 2026-12-01. No case or transaction IDs were created. Case outcomes: no case tou …`

**Assistant:** Done on the parts I can act on:

- **Contact channel preference** — deleted.
- **Travel notice** — deleted.

One limit I can't work around: I have no tool to erase conversational history or reflections of past chats from my memory store. I can see a summary of our 2026-11-09 conversation (contact-channel change and the Lisbon travel notice) still exists in that log, and I can't remove it myself. To have that purged, contact Kestrel privacy support and ask for erasure of your conversation memory — I'd recommend mentioning the session date above.

The practical effect today is the same: nothing about you is retained as an active preference or travel notice, so I won't act on either going forward.

_Episode written:_ Conversation on 2026-11-10: Customer asked to delete all remembered preferences and past conversations. The assistant deleted the contact-channel preference and Lisbon travel notice; no case or transaction IDs were created. It could not erase conversational history/reflections and advised contacting Kestrel privacy support, mentioning the 2026-11-09 session. No further promise or timing was given. Case outcomes: no case touched. Lesson: The assistant should set expectations at the start about which memory types can be erased and route conversational-history erasure to privacy support before making partial deletions.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | erasure: no fact remains | `{}` |
| **FAIL** | episodic | erasure: no episode remains | `2 episodes; purged 0` |
| **FAIL** | working | erasure: no transcript remains, including this conversation | `2 transcripts: ['er-s1', 'er-s2']` |
| **FAIL** | guard | erasure: 'Lisbon' is in no store | `{"Lisbon": ["adk_episodes.db", "bank.db", "adk_sessions.db"]}` |
