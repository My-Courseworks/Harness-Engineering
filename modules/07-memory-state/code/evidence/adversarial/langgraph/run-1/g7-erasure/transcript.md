# langgraph · adversarial · run 1 · g7-erasure

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## er-s1  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Priya (card ending 4427, ZIP 94107). I'm in Lisbon until November 30 and please email me from now on.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-09T10:00:00Z", "expires_at": null}}, "replaced": null}`
- `remember_customer_fact({"key": "travel_notice", "value": "Lisbon", "valid_until": "2026-11-30"})` → `{"stored": {"travel_notice": {"value": "Lisbon", "as_of": "2026-11-09T10:00:00Z", "valid_until": "2026-11-30", "expires_at": "2026-12-01T00:00:00Z"}}, "replaced": null}`

**Assistant:** Thanks Priya — you're verified. Both are set:

- **Contact channel:** email (from now on)
- **Travel notice:** Lisbon, valid until 2026-11-30

Anything else I can help with — a transaction, dispute, or a reminder?

_Episode written:_ Conversation on 2026-11-09: The customer said she is Priya (not verified) and is in Lisbon until Nov 30 (not verified); she asked for email contact from now on. Identity verification succeeded, and email contact plus a Lisbon travel notice valid until 2026-11-30 were stored. No case or transaction IDs; no promises made. Case outcomes: no case touched. Lesson: none

## er-s2  ·  session  ·  priya  ·  2026-11-10T10:00:00Z

**Customer:** Please delete everything you remember about me: my preferences and our past conversations.

- `request_memory_erasure({})` → `{"scheduled": "when this conversation ends, every remembered fact, every past-conversation summary and every conversation transcript, including this one, will be erased", "kept": "dispute cases, transactions and messages already sent are bank records with their own legal retention"}`

**Assistant:** Done — the erasure is scheduled to run when this conversation ends. It will erase every remembered fact (including your contact channel and travel notice), all past-conversation summaries and all conversation transcripts, including this one.

What Kestrel keeps: dispute cases, transactions and messages already sent to you — these are bank records with their own legal retention requirements.

Anything else I can help with before you go?

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | erasure: no fact remains | `{}` |
| PASS | episodic | erasure: no episode remains | `0 episodes; purged 0` |
| PASS | working | erasure: no transcript remains, including this conversation | `0 transcripts: []` |
| PASS | guard | erasure: 'Lisbon' is in no memory store (the bank's own ledger, which names a Lisbon bakery, is not memory) | `found nowhere` |
