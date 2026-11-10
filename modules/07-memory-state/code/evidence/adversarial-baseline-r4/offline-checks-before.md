# Offline checks: 11/39 passed

`python offline_checks.py`, run from the code directory; no model call.

| | check | evidence |
|---|---|---|
| **FAIL** | 2.1 masked: ['CVV: 737 5555 5555 5555 4444'] | `{"stored": ["CVV: 737 5555 5555 5555 4444"], "left": ["card number 5555\u20264444", "security code 737"]}` |
| **FAIL** | 2.1 masked: ["Here's everything: CVV 737 5555 5555 5555 4444 exp 12/29"] | `{"stored": ["Here's everything: CVV 737 5555 5555 5555 4444 exp [REDACTED EXPIRY]"], "left": ["card number 5555\u20264444", "security code 737"]}` |
| **FAIL** | 2.1 masked: ['1229 5555 5555 5555 4444'] | `{"stored": ["1229 5555 5555 5555 4444"], "left": ["card number 5555\u20264444"]}` |
| **FAIL** | 2.1 masked: ['PIN 1234 5555 5555 5555 4444'] | `{"stored": ["PIN 1234 5555 5555 5555 4444"], "left": ["card number 5555\u20264444", "security code 1234"]}` |
| **FAIL** | 2.1 masked: ['Order 12345 5555 5555 5555 4444 was declined'] | `{"stored": ["Order 12345 5555 5555 5555 4444 was declined"], "left": ["card number 5555\u20264444"]}` |
| **FAIL** | 2.1 masked: ['order 12345, 5555 5555 5555 4444'] | `{"stored": ["order 12345, 5555 5555 5555 4444"], "left": ["card number 5555\u20264444"]}` |
| **FAIL** | 2.1 masked: ['5555 5555 5555 and my zip is 94107', '4444'] | `{"stored": ["5555 5555 5555 and my zip is 94107", "4444"], "left": ["card number fragment 5555\u20264444"]}` |
| **FAIL** | 2.1 masked: ['card ending 4444, zip 94107', 'and the first twelve: 5555 5555 5555'] | `{"stored": ["card ending 4444, zip 94107", "and the first twelve: 5555 5555 5555"], "left": ["card number fragment 5555\u20264444"]}` |
| **FAIL** | 2.1 masked: ['security code 7891; 3782 822463 10005'] | `{"stored": ["security code [REDACTED SECURITY CODE]; 3782 822463 10005"], "left": ["card number 3782\u20260005"]}` |
| **FAIL** | 2.1 masked: ['exp 0827: 3782 822463 10005'] | `{"stored": ["exp 0827: 3782 822463 10005"], "left": ["card number 3782\u20260005"]}` |
| **FAIL** | 2.1 masked: ['PIN 7293; 2223-0031-2200-3222'] | `{"stored": ["PIN 7293; 2223-0031-2200-3222"], "left": ["card number 2223\u20263222", "security code 7293"]}` |
| **FAIL** | 2.1 masked: ['order no. 2654861; 3782 822463 10005'] | `{"stored": ["order no. 2654861; 3782 822463 10005"], "left": ["card number 3782\u20260005"]}` |
| **FAIL** | 2.1 masked: ['Order 1614993, 4000 0566 5566 5556'] | `{"stored": ["Order 1614993, 4000 0566 5566 5556"], "left": ["card number 4000\u20265556"]}` |
| PASS | 2.1 kept: 'order 2654861 arrived broken' | `["order 2654861 arrived broken"]` |
| PASS | 2.1 kept: 'tracking 9400 1234 5678 9012 3456 78' | `["tracking 9400 1234 5678 9012 3456 78"]` |
| PASS | 2.1 kept: 'booking ref QX3-48213, and the invoice was 5678 9012' | `["booking ref QX3-48213, and the invoice was 5678 9012"]` |
| PASS | 2.1 kept: 'my last four are 4427 and the order was 12345' | `["my last four are 4427 and the order was 12345"]` |
| PASS | 2.1 kept: 'call me on +1 415 555 0100 about order 1614993' | `["call me on +1 415 555 0100 about order 1614993"]` |
| PASS | 2.1 kept: 'the charge on 2026-11-01 for 1,299.00 and another for 15.99' | `["the charge on 2026-11-01 for 1,299.00 and another for 15.99"]` |
| **FAIL** | nb5 the reasoning masker leaves 'card last4 8830' alone next to card data | `The customer gave card last4 [REDACTED SECURITY CODE] and ZIP 10011; the card number in their message was masked. I will verify.` |
| **FAIL** | nb6 two comma-joined numbers in a reply are both masked | `You gave [REDACTED CARD NUMBER], 4111 1111 1111 1111.` |
| **FAIL** | nb2 an empty reflection '{"summary": "", "lesson": ""}' is not an episode | `{"summary": "{\"summary\": \"\", \"lesson\": \"\"}", "lesson": "none"}` |
| **FAIL** | nb2 an empty reflection '' is not an episode | `{"summary": "", "lesson": "none"}` |
| **FAIL** | nb2 an empty reflection '{"summary": "   "}' is not an episode | `{"summary": "   ", "lesson": "none"}` |
| PASS | nb2 a real reflection still parses | `{"summary": "Customer asked about a CloudNest charge; no case filed.", "lesson": "none"}` |
| PASS | nb8 a true 'the expiry was removed' over a store that leaked the card number is consistent | `{"agent_claimed_not_stored": ["expiry"], "card_data_in_stores": {"card number 5555\u20264444": ["adk_sessions.db"]}, "false_claims": []}` |
| PASS | nb8 a false 'the card number was not stored' over that store is still caught | `{"agent_claimed_not_stored": ["card number"], "card_data_in_stores": {"card number 5555\u20264444": ["adk_sessions.db"]}, "false_claims": ["card number"]}` |
| **FAIL** | 2.2a tab A, registered before tab B's erasure, is not re-registered into the new generation at its next turn | `{"tab_a_generation": 1, "tab_a_current": true}` |
| PASS | 2.2a a session started after the erasure is current | `{"tab_c_generation": 1}` |
| **FAIL** | nb3 a locked account is locked for every verified action (world.verification_locked), not only for new guesses | `"world.verification_locked does not exist"` |
| **FAIL** | nb1 three failed fires in fifteen minutes leave the reminder pending (with a back-off), not failed | `fire_due_followups() got an unexpected keyword argument 'on_failed'` |
| **FAIL** | nb1 a two-day outage ends the reminder, and whoever is told is told exactly once (on_failed) | `fire_due_followups() got an unexpected keyword argument 'on_failed'` |
| **FAIL** | nb4 `review.py retract --by A --by B` with two registry reviewers is accepted and records both names | `{"exit": 1, "active": "v2", "retracted_by": null, "stderr": "CY_OWNER_ROLE}\")\nValueError: 'ops-lead (scripted reviewer), disputes-policy-owner (scripted reviewer)' holds no reviewer role in the registry; a retraction needs an ops_lead or a disputes_policy_owner"}` |
| **FAIL** | 012 after a lost result, the same wrong guess repeated in the same conversation within two minutes counts once | `attempt_verification() got an unexpected keyword argument 'session_id'` |
| **FAIL** | 012 the same guess from another conversation is a new attempt | `attempt_verification() got an unexpected keyword argument 'session_id'` |
| PASS | 012 with no lost result, the same wrong guess typed again is a second attempt (a customer's retype is not excused) | `{"outcome": "mismatch", "failures": 2}` |
| **FAIL** | 012 after a lost result, the code this conversation consumed matches again without a new row; from another conversation, or with no lost result, a consumed code is spent | `AttributeError: module 'cardcare.world' has no attribute 'issue_code'` |
| **FAIL** | 012 the same evidence note attached again is attached once | `{"lines": ["[2026-11-20] cancellation reference CN-77812", "[2026-11-20] cancellation reference CN-77812"], "second": {"already_attached": null, "error": null}}` |
| **FAIL** | 012 a repeated filing after a crash between opening the case and scheduling its follow-up completes the follow-up | `{"repeated": {"case_id": null, "error": "case C-5002 is already open for T-2002", "note": null}, "followups": 0}` |
