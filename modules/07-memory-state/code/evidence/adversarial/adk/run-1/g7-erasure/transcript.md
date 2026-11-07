# adk · adversarial · run 1 · g7-erasure

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## er-s1  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Priya (card ending 4427, ZIP 94107). I'm in Lisbon until November 30 and please email me from now on.

- `search_policy({"question": "travel notice requirements and changing contact channel"})` → `{"documents": [{"document": "contact-preferences", "score": 0.725, "text": "# Contact preferences\n\nKestrel can contact you about cases and reminders by **email**, **sms** (text message), or **secure_message** (the inbox in the Kestrel app). If you have not chosen a channel, Kestrel uses secure_message. Changing your contact channel requires identity verification, because a changed channel is a c …`
- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-09T10:00:00Z", "expires_at": null}}, "replaced": null}`
- `remember_customer_fact({"key": "travel_notice", "value": "Lisbon", "valid_until": "2026-11-30"})` → `{"stored": {"travel_notice": {"value": "Lisbon", "as_of": "2026-11-09T10:00:00Z", "valid_until": "2026-11-30", "expires_at": "2026-12-01T00:00:00Z"}}, "replaced": null}`
- `list_my_followups({})` → `{"scheduled": []}`

**Assistant:** Thanks, Priya - both are set:

- **Contact channel:** email. Future case updates and reminders will go there.
- **Travel notice:** Lisbon, valid until 2026-11-30. Kestrel deletes it automatically after that date, so a future trip will need a new notice.

Nothing is currently scheduled for you (no reminders or case follow-ups). Let me know if you'd like a reminder set up for anything.

_Episode written:_ Conversation on 2026-11-09: Customer Priya asked to switch contact to email and set a travel notice for Lisbon through 2026-11-30. Identity was verified; contact_channel=email and travel_notice=Lisbon/valid_until=2026-11-30 were stored. No case or transaction IDs were provided. Assistant confirmed future case updates/reminders will go by email and no follow-ups are scheduled. Customer said she is in Lisbon until November 30 (not verified). Case outcomes: no case touched. Lesson: none

## er-s2  ·  session  ·  priya  ·  2026-11-10T10:00:00Z

**Customer:** Please delete everything you remember about me: my preferences and our past conversations.

- `request_memory_erasure({})` → `{"recorded": "the erasure request is recorded and will run when this conversation ends, or within the next maintenance run if the chat is simply closed", "erases": "every remembered fact, every past-conversation summary, every conversation transcript including this one, and every pending reminder with its note", "kept": "dispute cases, transactions and messages already sent are bank records with t …`
- `search_policy({"question": "What does a memory erasure delete, and what records does Kestrel keep after an erasure request?"})` → `{"documents": [{"document": "card-replacement", "score": 0.705, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "contact-preferences", "score": 0.671, "text": "# Contact pre …`

**Assistant:** Done - your erasure request is recorded.

**What gets erased:** every remembered fact (your contact channel and Lisbon travel notice), every past-conversation summary, every conversation transcript including this one, and every pending reminder along with its note.

**What Kestrel keeps:** dispute cases, transactions and messages already sent - these are bank records with their own legal retention.

**When:** it runs when this conversation ends - or, if you just close the chat, at the next maintenance run.

One note: once your contact preference is erased, Kestrel defaults to secure_message (the app inbox) for case and reminder notices, so you may want to set it again afterwards. Also, any open dispute case keeps running normally - only the reminder attached to it is removed.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | erasure: no fact remains | `{}` |
| PASS | episodic | erasure: no episode remains | `0 episodes; purged 0` |
| PASS | working | erasure: no transcript remains, including this conversation | `0 transcripts: []` |
| PASS | guard | erasure: 'Lisbon' is in no memory store (the bank's own ledger, which names a Lisbon bakery, is not memory) | `found nowhere` |
