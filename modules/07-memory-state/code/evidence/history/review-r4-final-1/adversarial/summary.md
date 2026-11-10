# Evidence summary: adversarial

Pass counts per memory type, summed over every recorded live run.

| memory type | adk (2 runs) | langgraph (2 runs) |
|---|---|---|
| working | 94/94 | 93/94 |
| semantic | 48/48 | 48/48 |
| episodic | 56/56 | 56/56 |
| procedural | 24/24 | 24/24 |
| external | 50/50 | 50/50 |
| parametric | 4/6 | 6/6 |
| prospective | 86/86 | 86/86 |
| guard | 54/54 | 54/54 |
| **all** | **416/418** | **417/418** |

## Every failed check

| framework | where | step | memory type | check | evidence |
|---|---|---|---|---|---|
| adk | run-1/g1-priya-month | p1-followups-11-19 | parametric | no outbound message invites a reply or promises to 'add it to your case' | `["Kestrel case C-5001 (StreamMax charge T-1002) has been decided: the dispute was rejected - the merchant says no cancellation request is on record. If you have proof you cancelled before the 2026-10- …` |
| adk | run-2/g1-priya-month | p1-followups-11-19 | parametric | no outbound message invites a reply or promises to 'add it to your case' | `["Update on your dispute C-5001 (StreamMax charge of 28 Oct): it was declined - the merchant says it has no record of a cancellation request, so the decision is \"no proof of cancellation\" (resolved  …` |
| langgraph | run-2/g6-lockout | lock-s1 | working | three wrong answers lock verification for the session: the channel is not changed | `{"value": "email", "as_of": "2026-11-24T10:06:00Z", "expires_at": null}` |
