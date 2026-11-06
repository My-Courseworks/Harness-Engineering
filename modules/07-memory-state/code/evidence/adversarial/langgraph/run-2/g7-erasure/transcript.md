# langgraph · adversarial · run 2 · g7-erasure

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## er-s1  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Priya (card ending 4427, ZIP 94107). I'm in Lisbon until November 30 and please email me from now on.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-09T10:00:00Z", "expires_at": null}}, "replaced": null}`
- `remember_customer_fact({"key": "travel_notice", "value": "Lisbon", "valid_until": "2026-11-30"})` → `{"stored": {"travel_notice": {"value": "Lisbon", "as_of": "2026-11-09T10:00:00Z", "valid_until": "2026-11-30", "expires_at": "2026-12-01T00:00:00Z"}}, "replaced": null}`

**Assistant:** Thanks, Priya — you're verified. I've saved both:

- **Contact channel:** email
- **Travel notice:** Lisbon, through 2026-11-30

Anything else I can help with?

_Episode written:_ Conversation on 2026-11-09: Customer wanted email contact and a travel notice for Lisbon until November 30, [REDACTED SECURITY CODE]. Identity verification succeeded, and the assistant saved contact channel as email and travel notice as Lisbon through [REDACTED SECURITY CODE]-[REDACTED EXPIRY] (expires [REDACTED SECURITY CODE]-[REDACTED EXPIRY]). No case or transaction IDs were provided, and no further commitments were made. Case outcomes: no case touched. Lesson: none

## er-s2  ·  session  ·  priya  ·  2026-11-10T10:00:00Z

**Customer:** Please delete everything you remember about me: my preferences and our past conversations.

- `request_memory_erasure({})` → `{"scheduled": "when this conversation ends, every remembered fact, every past-conversation summary and every conversation transcript, including this one, will be erased", "kept": "dispute cases, transactions and messages already sent are bank records with their own legal retention"}`
- `search_policy({"question": "memory erasure: what is deleted and what does Kestrel keep?"})` → `{"documents": [{"document": "card-replacement", "score": 0.633, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "contact-preferences", "score": 0.587, "text": "# Contact pre …`

**Assistant:** Done — the erasure is scheduled to run when this conversation ends.

What gets erased:
- Every remembered fact about you (including your contact channel and travel notice)
- Every past-conversation summary
- Every conversation transcript, including this one

What Kestrel keeps: dispute cases, transactions, and messages already sent — these are bank records with their own legal retention requirements.

Note: if you have a scheduled reminder or case follow-up, its delivery may still go out; tell me if you'd like me to check or cancel anything before the conversation ends.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | erasure: no fact remains | `{}` |
| PASS | episodic | erasure: no episode remains | `0 episodes; purged 0` |
| PASS | working | erasure: no transcript remains, including this conversation | `0 transcripts: []` |
| PASS | guard | erasure: 'Lisbon' is in no memory store (the bank's own ledger, which names a Lisbon bakery, is not memory) | `found nowhere` |
