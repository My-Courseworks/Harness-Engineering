# adk · adversarial · run 1 · g37-expired-fact-sweep

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ef-s1  ·  session  ·  eli  ·  2026-11-14T10:00:00Z

**Customer:** I'm in Oslo until November 20, please set a travel notice.

- `remember_customer_fact({"key": "travel_notice", "value": "Oslo", "valid_until": "2026-11-20"})` → `{"stored": {"travel_notice": {"value": "Oslo", "as_of": "2026-11-14T10:00:00Z", "valid_until": "2026-11-20", "expires_at": "2026-11-21T00:00:00Z"}}, "replaced": null}`

**Assistant:** Your travel notice for Oslo is set, valid through November 20 (expires at the end of that day). Anything else I can help with?

_Episode written:_ Conversation on 2026-11-14: Customer wanted a travel notice for Oslo through Nov 20. Assistant stored travel notice for Oslo valid until 2026-11-20 (expires end of that day; recorded Nov 14, 2026). No case or transaction ID was provided. No further preference stated. Case outcomes: no case touched. Lesson: none

## ef-maint  ·  maintenance  ·  2026-12-01T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": ["eli:travel_notice"], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": [], "case_followups_repaired": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | an expired travel notice is deleted by maintenance, not only when the customer next chats | `null` |
