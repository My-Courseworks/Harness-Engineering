# langgraph · adversarial · run 1 · g7-erasure

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## er-s1  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Priya (card ending 4427, ZIP 94107). I'm in Lisbon until November 30 and please email me from now on.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `remember_customer_fact({"key": "travel_notice", "value": "Lisbon", "valid_until": "2026-11-30"})` → `{"stored": {"travel_notice": {"value": "Lisbon", "as_of": "2026-11-09T10:00:00Z", "valid_until": "2026-11-30", "expires_at": "2026-12-01T00:00:00Z"}}, "replaced": null}`
- `search_policy({"question": "travel notice rules and what a travel notice does"})` → `{"documents": [{"document": "travel-notices", "score": 0.834, "text": "# Travel notices\n\nA travel notice tells Kestrel's fraud systems that card use in another country is expected, which reduces false declines while you travel. Give the destination and the date you return. Kestrel keeps a travel notice only until the return date and deletes it automatically afterwards; a new trip needs a new not …`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-09T10:00:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** I'll verify your identity and set up your travel notice.
You're verified, and both are set:

- **Travel notice:** Lisbon, valid until 2026-11-30 - it tells our fraud systems to expect card use abroad, which reduces false declines. It's deleted automatically after your return date.
- **Contact channel:** email - that's where reminders and case follow-ups will go from now on.

One thing worth knowing while traveling: purchases in a non-USD currency carry a 1.25% foreign transaction fee on the US-dollar amount, posted as a separate line the same day. A travel notice doesn't waive it.

Anything else - a transaction to look at or a reminder you'd like scheduled?

_Episode written:_ Conversation on 2026-11-09: Customer (Priya) asked to set a travel notice for Lisbon until 2026-11-30 and to use email for future contact. Identity was verified; travel notice and contact channel were stored. No case or transaction IDs were provided. Assistant explained the 1.25% foreign transaction fee and that travel notices do not waive it. No promise beyond automatic notice deletion after return date. Case outcomes: no case touched. Lesson: none

## er-s2  ·  session  ·  priya  ·  2026-11-10T10:00:00Z

**Customer:** Please delete everything you remember about me: my preferences and our past conversations.

- `request_memory_erasure({})` → `{"recorded": "the erasure request is recorded and will run when this conversation ends, or within the next maintenance run if the chat is simply closed", "erases": "every remembered fact, every past-conversation summary, every conversation transcript including this one, and every pending reminder with its note", "kept": "dispute cases, transactions and messages already sent are bank records with t …`

**Assistant:** Done - your erasure request is recorded. Here's what happens:

**Erased:** everything I remember about you - stored preferences (including your contact channel and travel notice), summaries of past conversations, conversation transcripts including this one, and any pending reminders along with their notes.

**Kept:** dispute cases, transactions, and messages already sent to you, since those are bank records with their own legal retention requirements.

**When:** it runs when this conversation ends - or, if you just close the chat, at the next maintenance run.

Is there anything else you'd like to do before you close the chat?

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | erasure: no fact remains | `{}` |
| PASS | episodic | erasure: no episode remains | `0 episodes; purged 0` |
| PASS | working | erasure: no transcript remains, including this conversation | `0 transcripts: []` |
| PASS | guard | erasure: 'Lisbon' is in no memory store (the bank's own ledger, which names a Lisbon bakery, is not memory) | `found nowhere` |
