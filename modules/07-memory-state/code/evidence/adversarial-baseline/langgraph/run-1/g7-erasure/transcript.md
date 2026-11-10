# langgraph · adversarial · run 1 · g7-erasure

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## er-s1  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Priya (card ending 4427, ZIP 94107). I'm in Lisbon until November 30 and please email me from now on.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-09T10:00:00Z", "expires_at": null}}, "replaced": null}`
- `remember_customer_fact({"key": "travel_notice", "value": "Lisbon", "valid_until": "2026-11-30"})` → `{"stored": {"travel_notice": {"value": "Lisbon", "as_of": "2026-11-09T10:00:00Z", "valid_until": "2026-11-30", "expires_at": "2026-12-01T00:00:00Z"}}, "replaced": null}`

**Assistant:** Thanks, Priya — you're verified. Both are set:

- **Contact channel:** email from now on
- **Travel notice:** Lisbon through November 30, 2026

Anything else I can help with while you're traveling?

_Episode written:_ Conversation on 2026-11-09: Priya asked to switch contact to email and register a travel notice for Lisbon through November 30, 2026. After identity verification, the assistant stored both preferences and confirmed them. No case or transaction IDs were provided. Case outcomes: no case touched. Lesson: none

## er-s2  ·  session  ·  priya  ·  2026-11-10T10:00:00Z

**Customer:** Please delete everything you remember about me: my preferences and our past conversations.

- `forget_customer_fact({"key": "contact_channel"})` → `{"forgotten": "contact_channel", "had_value": true}`
- `forget_customer_fact({"key": "travel_notice"})` → `{"forgotten": "travel_notice", "had_value": true}`

**Assistant:** Done — I've deleted the stored facts about you. Nothing is on file for contact channel or travel notice now.

One thing I can't do: I have no tool to delete the notes from our past conversations themselves (I can only search them). If you want those erased, please contact Kestrel support and ask for a conversation-history deletion.

_Episode written:_ Conversation on 2026-11-10: Customer asked to delete everything remembered about them: preferences and past conversations. The assistant deleted stored contact-channel and travel-notice facts (both had values) and said nothing remains for those. It explained it cannot delete past conversation notes, only search them, and advised contacting Kestrel support for conversation-history deletion. No case/transaction IDs or timing were given. Case outcomes: no case touched. Lesson: Next time, state the limit on deleting conversation history before performing the fact deletions, then direct the customer to Kestrel support.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | erasure: no fact remains | `{}` |
| **FAIL** | episodic | erasure: no episode remains | `2 episodes; purged 0` |
| **FAIL** | working | erasure: no transcript remains, including this conversation | `2 transcripts: ['er-s1', 'er-s2']` |
| **FAIL** | guard | erasure: 'Lisbon' is in no store | `{"Lisbon": ["lg_store.db", "bank.db", "lg_checkpoints.db-wal"]}` |
