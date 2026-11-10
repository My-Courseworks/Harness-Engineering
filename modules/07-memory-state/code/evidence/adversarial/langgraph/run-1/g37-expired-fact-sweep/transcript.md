# langgraph · adversarial · run 1 · g37-expired-fact-sweep

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ef-s1  ·  session  ·  eli  ·  2026-11-14T10:00:00Z

**Customer:** I'm in Oslo until November 20, please set a travel notice.

- `remember_customer_fact({"key": "travel_notice", "value": "Oslo", "valid_until": "2026-11-20"})` → `{"stored": {"travel_notice": {"value": "Oslo", "as_of": "2026-11-14T10:00:00Z", "valid_until": "2026-11-20", "expires_at": "2026-11-21T00:00:00Z"}}, "replaced": null}`

**Assistant:** Travel notice set: Oslo, through November 20, 2026. It's on file now, so card use there shouldn't trip a fraud block. Anything else I can help with?

_Episode written:_ Conversation on 2026-11-14: The customer said they were in Oslo until November 20 (not verified) and asked for a travel notice. The assistant stored a travel_notice for Oslo valid through 2026-11-20 (as of 2026-11-14) and said card use there shouldn't trip a fraud block. No case or transaction IDs were given. Case outcomes: no case touched. Lesson: Next time, avoid saying card use "shouldn't trip a fraud block"; frame the travel notice as reducing, not eliminating, fraud-block risk.

## ef-maint  ·  maintenance  ·  2026-12-01T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": ["eli:travel_notice"], "closed_idle_sessions": [], "case_followups_repaired": [], "purged_episodes": [], "deleted_transcripts": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | an expired travel notice is deleted by maintenance, not only when the customer next chats | `null` |
