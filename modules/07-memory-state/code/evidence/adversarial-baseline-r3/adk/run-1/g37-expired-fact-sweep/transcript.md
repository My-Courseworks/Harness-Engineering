# adk · adversarial · run 1 · g37-expired-fact-sweep

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ef-s1  ·  session  ·  eli  ·  2026-11-14T10:00:00Z

**Customer:** I'm in Oslo until November 20, please set a travel notice.

- `remember_customer_fact({"key": "travel_notice", "value": "Oslo", "valid_until": "2026-11-20"})` → `{"stored": {"travel_notice": {"value": "Oslo", "as_of": "2026-11-14T10:00:00Z", "valid_until": "2026-11-20", "expires_at": "2026-11-21T00:00:00Z"}}, "replaced": null}`
- `search_policy({"question": "travel notice what it does, how long it takes to apply, coverage"})` → `{"documents": [{"document": "travel-notices", "score": 0.747, "text": "# Travel notices\n\nA travel notice tells Kestrel's fraud systems that card use in another country is expected, which reduces false declines while you travel. Give the destination and the date you return. Kestrel keeps a travel notice only until the return date and deletes it automatically afterwards; a new trip needs a new not …`

**Assistant:** Done - travel notice set for Oslo through November 20, 2026. It tells our fraud systems to expect card use in Norway, which reduces the chance of false declines, and it's removed automatically after your return date.

_Episode written:_ Conversation on 2026-11-14: The customer said they are in Oslo until November 20 (not verified) and asked to set a travel notice. The assistant stored a travel notice for Oslo valid until 2026-11-20 (as of 2026-11-14) and confirmed it reduces false declines and is removed automatically after the return date. No case or transaction IDs were provided. Case outcomes: no case touched. Lesson: none

## ef-maint  ·  maintenance  ·  2026-12-01T09:00:00Z

_maintenance:_ `{"erased_customers": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": []}`

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | semantic | an expired travel notice is deleted by maintenance, not only when the customer next chats | `{"value": "Oslo", "as_of": "2026-11-14T10:00:00Z", "valid_until": "2026-11-20", "expires_at": "2026-11-21T00:00:00Z"}` |
