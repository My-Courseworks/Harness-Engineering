# Offline checks: 105/145 passed

`python offline_checks.py`, run from the code directory; no model call.

| | check | evidence |
|---|---|---|
| PASS | 2.1 masked: ['CVV: 737 5555 5555 5555 4444'] | `{"stored": ["CVV: [REDACTED SECURITY CODE] [REDACTED CARD NUMBER]"], "left": []}` |
| PASS | 2.1 masked: ["Here's everything: CVV 737 5555 5555 5555 4444 exp 12/29"] | `{"stored": ["Here's everything: CVV [REDACTED SECURITY CODE] [REDACTED CARD NUMBER] exp [REDACTED EXPIRY]"], "left": []}` |
| PASS | 2.1 masked: ['1229 5555 5555 5555 4444'] | `{"stored": ["[REDACTED SECURITY CODE] [REDACTED CARD NUMBER]"], "left": []}` |
| PASS | 2.1 masked: ['PIN 1234 5555 5555 5555 4444'] | `{"stored": ["PIN [REDACTED SECURITY CODE] [REDACTED CARD NUMBER]"], "left": []}` |
| PASS | 2.1 masked: ['Order 12345 5555 5555 5555 4444 was declined'] | `{"stored": ["Order 12345 [REDACTED CARD NUMBER] was declined"], "left": []}` |
| PASS | 2.1 masked: ['order 12345, 5555 5555 5555 4444'] | `{"stored": ["order 12345, [REDACTED CARD NUMBER]"], "left": []}` |
| PASS | 2.1 masked: ['5555 5555 5555 and my zip is 94107', '4444'] | `{"stored": ["[REDACTED CARD DIGITS] and my zip is 94107", "[REDACTED CARD DIGITS]"], "left": []}` |
| PASS | 2.1 masked: ['card ending 4444, zip 94107', 'and the first twelve: 5555 5555 5555'] | `{"stored": ["card ending 4444, zip 94107", "and the first twelve: [REDACTED CARD DIGITS]"], "left": []}` |
| PASS | 2.1 masked: ['security code 7891; 3782 822463 10005'] | `{"stored": ["security code [REDACTED SECURITY CODE]; [REDACTED CARD NUMBER]"], "left": []}` |
| PASS | 2.1 masked: ['exp 0827: 3782 822463 10005'] | `{"stored": ["exp [REDACTED EXPIRY]: [REDACTED CARD NUMBER]"], "left": []}` |
| PASS | 2.1 masked: ['PIN 7293; 2223-0031-2200-3222'] | `{"stored": ["PIN [REDACTED SECURITY CODE]; [REDACTED CARD NUMBER]"], "left": []}` |
| PASS | 2.1 masked: ['order no. 2654861; 3782 822463 10005'] | `{"stored": ["order no. 2654861; [REDACTED CARD NUMBER]"], "left": []}` |
| PASS | 2.1 masked: ['Order 1614993, 4000 0566 5566 5556'] | `{"stored": ["Order 1614993, [REDACTED CARD NUMBER]"], "left": []}` |
| PASS | 2.1 kept: 'order 2654861 arrived broken' | `["order 2654861 arrived broken"]` |
| PASS | 2.1 kept: 'tracking 9400 1234 5678 9012 3456 78' | `["tracking 9400 1234 5678 9012 3456 78"]` |
| PASS | 2.1 kept: 'booking ref QX3-48213, and the invoice was 5678 9012' | `["booking ref QX3-48213, and the invoice was 5678 9012"]` |
| PASS | 2.1 kept: 'my last four are 4427 and the order was 12345' | `["my last four are 4427 and the order was 12345"]` |
| PASS | 2.1 kept: 'call me on +1 415 555 0100 about order 1614993' | `["call me on +1 415 555 0100 about order 1614993"]` |
| PASS | 2.1 kept: 'the charge on 2026-11-01 for 1,299.00 and another for 15.99' | `["the charge on 2026-11-01 for 1,299.00 and another for 15.99"]` |
| PASS | nb5 the reasoning masker leaves 'card last4 8830' alone next to card data | `The customer gave card last4 8830 and ZIP 10011; the card number in their message was masked. I will verify.` |
| PASS | nb6 two comma-joined numbers in a reply are both masked | `You gave [REDACTED CARD NUMBER].` |
| PASS | nb2 an empty reflection '{"summary": "", "lesson": ""}' is not an episode | `null` |
| PASS | nb2 an empty reflection '' is not an episode | `null` |
| PASS | nb2 an empty reflection '{"summary": "   "}' is not an episode | `null` |
| PASS | nb2 a real reflection still parses | `{"summary": "Customer asked about a CloudNest charge; no case filed.", "lesson": "none"}` |
| PASS | nb8 a true 'the expiry was removed' over a store that leaked the card number is consistent | `{"agent_claimed_not_stored": ["expiry"], "card_data_in_stores": {"card number 5555\u20264444": ["adk_sessions.db"]}, "false_claims": []}` |
| PASS | nb8 a false 'the card number was not stored' over that store is still caught | `{"agent_claimed_not_stored": ["card number"], "card_data_in_stores": {"card number 5555\u20264444": ["adk_sessions.db"]}, "false_claims": ["card number"]}` |
| PASS | fp1 masked: 'old card: 6011 1111 1111 1117\nsecurity code: three eight six (386)\nexpiry: 07/29\nplease just file the CloudNest dispute' | `{"stored": ["old card: [REDACTED CARD NUMBER]\nsecurity code: [REDACTED SECURITY CODE]\nexpiry: [REDACTED EXPIRY]\nplease just file the CloudNest dispute"], "left": []}` |
| PASS | fp1 masked: 'security code 386 (three eight six)' | `{"stored": ["security code [REDACTED SECURITY CODE]"], "left": []}` |
| PASS | fp1 masked: 'my cvv: 3 8 6 (386)' | `{"stored": ["my cvv: [REDACTED SECURITY CODE]"], "left": []}` |
| PASS | fp1 masked: 'security code is 386 [three eight six]' | `{"stored": ["security code is [REDACTED SECURITY CODE]"], "left": []}` |
| PASS | fp1 masked: 'cvv three eight six = 386' | `{"stored": ["cvv [REDACTED SECURITY CODE]"], "left": []}` |
| PASS | fp1 masked: 'cvv: three eight six/386' | `{"stored": ["cvv: [REDACTED SECURITY CODE]"], "left": []}` |
| PASS | fp1 masked: 'security code: three, eight, six (386)' | `{"stored": ["security code: [REDACTED SECURITY CODE]"], "left": []}` |
| PASS | fp1 masked: 'security code - three eight six - 386' | `{"stored": ["security code - [REDACTED SECURITY CODE]"], "left": []}` |
| PASS | fp1 masked: 'the code on the back: seven three seven (737)' | `{"stored": ["the code on the back: [REDACTED SECURITY CODE]"], "left": []}` |
| PASS | fp1 masked: 'card 6011 1111 1111 1117 cvv 386 386' | `{"stored": ["card [REDACTED CARD NUMBER] cvv [REDACTED SECURITY CODE]"], "left": []}` |
| PASS | fp1 masked: 'cvc 386-386' | `{"stored": ["cvc [REDACTED SECURITY CODE]"], "left": []}` |
| PASS | fp1 masked: 'sec code three eight six, in digits 386' | `{"stored": ["sec code [REDACTED SECURITY CODE], in digits [REDACTED SECURITY CODE]"], "left": []}` |
| PASS | fp1 masked: 'security code: three, eight, six' | `{"stored": ["security code: [REDACTED SECURITY CODE]"], "left": []}` |
| PASS | fp1 masked: 'cvv 3, 8, 6' | `{"stored": ["cvv [REDACTED SECURITY CODE]"], "left": []}` |
| PASS | fp1 masked: '5555 5555 5555 4444, exp 12 29, cvv 737' | `{"stored": ["[REDACTED CARD NUMBER], exp [REDACTED EXPIRY], cvv [REDACTED SECURITY CODE]"], "left": []}` |
| PASS | fp1 masked: 'card 6011 1111 1111 1117 expiry 07 29' | `{"stored": ["card [REDACTED CARD NUMBER] expiry [REDACTED EXPIRY]"], "left": []}` |
| PASS | fp1 masked: '6011 1111 1111 1117 exp 07.29 cvv 386' | `{"stored": ["[REDACTED CARD NUMBER] exp [REDACTED EXPIRY] cvv [REDACTED SECURITY CODE]"], "left": []}` |
| PASS | fp1 masked: '6011111111111117 expires 07 2029 cvv 386' | `{"stored": ["[REDACTED CARD NUMBER] expires [REDACTED EXPIRY] cvv [REDACTED SECURITY CODE]"], "left": []}` |
| PASS | fp1 masked: 'exp 07 29' | `{"stored": ["exp [REDACTED EXPIRY]"], "left": []}` |
| PASS | fp1 masked: '6011 1111 1111 1117 expires 07 29' | `{"stored": ["[REDACTED CARD NUMBER] expires [REDACTED EXPIRY]"], "left": []}` |
| PASS | fp1 masked: 'exp Jul 29' | `{"stored": ["exp [REDACTED EXPIRY]"], "left": []}` |
| PASS | fp1 masked: '4111111111111111, cvv 1 8 1 = 181' | `{"stored": ["[REDACTED CARD NUMBER], cvv [REDACTED SECURITY CODE]"], "left": []}` |
| PASS | fp1 kept: 'I was charged 386 (three payments) by CloudNest' | `["I was charged 386 (three payments) by CloudNest"]` |
| PASS | fp1 kept: 'room 204 (two oh four) at the hotel in Lisbon' | `["room 204 (two oh four) at the hotel in Lisbon"]` |
| PASS | fp1 kept: 'flight 386 (three eight six) to Lisbon on November 30' | `["flight 386 (three eight six) to Lisbon on November 30"]` |
| PASS | fp1 kept: 'my last four are 4427 (four four two seven) and ZIP 94107' | `["my last four are 4427 (four four two seven) and ZIP 94107"]` |
| PASS | fp1 kept: 'order 5001 (2026) arrived late' | `["order 5001 (2026) arrived late"]` |
| PASS | fp1 kept: 'I disputed charges 1, 2, 3 and 4 on the list' | `["I disputed charges 1, 2, 3 and 4 on the list"]` |
| PASS | fp1 kept: 'it was one, two, three weeks ago, I forget' | `["it was one, two, three weeks ago, I forget"]` |
| PASS | fp1 kept: 'I paid 12.29 for parking and 7.29 for coffee' | `["I paid 12.29 for parking and 7.29 for coffee"]` |
| PASS | fp1 kept: 'my travel notice expiration should be 12 10' | `["my travel notice expiration should be 12 10"]` |
| PASS | fp1 kept: 'exp. delivery 11 24, order 2654861' | `["exp. delivery 11 24, order 2654861"]` |
| PASS | fp1 kept: 'my trial exp Jul 29, please cancel it before then' | `["my trial exp Jul 29, please cancel it before then"]` |
| PASS | fp1 kept: 'the parcel arrives Jul 29' | `["the parcel arrives Jul 29"]` |
| PASS | fp2 masked: ['expiry: July / 29'] | `{"stored": ["expiry: [REDACTED EXPIRY]"], "left": []}` |
| PASS | fp2 masked: ["exp Jul '29"] | `{"stored": ["exp [REDACTED EXPIRY]"], "left": []}` |
| PASS | fp2 masked: ['old card: 6011 1111 1111 1117\nsec code: 386\nexpiry: Jul/29'] | `{"stored": ["old card: [REDACTED CARD NUMBER]\nsec code: [REDACTED SECURITY CODE]\nexpiry: [REDACTED EXPIRY]"], "left": []}` |
| PASS | fp2 masked: ['the card expires July of 29'] | `{"stored": ["the card expires [REDACTED EXPIRY]"], "left": []}` |
| PASS | fp2 masked: ['exp Jul 33'] | `{"stored": ["exp [REDACTED EXPIRY]"], "left": []}` |
| PASS | fp2 masked: ['expiry: seven twenty-nine'] | `{"stored": ["expiry: [REDACTED EXPIRY]"], "left": []}` |
| PASS | fp2 masked: ['old card: 6011 1111 1111 1117', 'cvv 1386 and ZIP 60614'] | `{"stored": ["old card: [REDACTED CARD NUMBER]", "cvv [REDACTED SECURITY CODE] and ZIP 60614"], "left": []}` |
| PASS | fp2 masked: ['old card: 6011 1111 1111 1117', '386 and ZIP 60614'] | `{"stored": ["old card: [REDACTED CARD NUMBER]", "[REDACTED SECURITY CODE] and ZIP 60614"], "left": []}` |
| PASS | fp2 masked: ['starts 6011 1111 1111', 'next 1117', "expires end of July '29"] | `{"stored": ["starts [REDACTED CARD DIGITS]", "next [REDACTED CARD DIGITS]", "expires end of [REDACTED EXPIRY]"], "left": []}` |
| PASS | fp2 masked: ["oh, expires end of July '29"] | `{"stored": ["oh, expires end of [REDACTED EXPIRY]"], "left": []}` |
| PASS | fp2 masked: ["old card 6011 1111 1111 1117, expiring Jul '29"] | `{"stored": ["old card [REDACTED CARD NUMBER], expiring [REDACTED EXPIRY]"], "left": []}` |
| PASS | fp2 last message kept as typed: ['old card: 6011 1111 1111 1117\nsecurity code: 386\nexpiry: 07/29', "Fine, it's 5127 and ZIP 60614."] | `["old card: [REDACTED CARD NUMBER]\nsecurity code: [REDACTED SECURITY CODE]\nexpiry: [REDACTED EXPIRY]", "Fine, it's 5127 and ZIP 60614."]` |
| PASS | fp2 last message kept as typed: ['old card: 6011 1111 1111 1117\nsecurity code: 386\nexpiry: 07/29', '5127, ZIP 60614.'] | `["old card: [REDACTED CARD NUMBER]\nsecurity code: [REDACTED SECURITY CODE]\nexpiry: [REDACTED EXPIRY]", "5127, ZIP 60614."]` |
| PASS | fp2 last message kept as typed: ['my trial exp Jul 29, cancel it before then'] | `["my trial exp Jul 29, cancel it before then"]` |
| PASS | fp2 last message kept as typed: ['the parcel arrives July / 29 at the latest'] | `["the parcel arrives July / 29 at the latest"]` |
| PASS | fp2 last message kept as typed: ["my subscription expires end of July '29"] | `["my subscription expires end of July '29"]` |
| PASS | fp2 last message kept as typed: ['the dispute window expires December 2026, right?'] | `["the dispute window expires December 2026, right?"]` |
| PASS | fp2 last message kept as typed: ['my travel notice expires July 2029'] | `["my travel notice expires July 2029"]` |
| PASS | fp3 a reply that repeats a one-time code the customer typed is returned without it | `{"customer": "Did it go through? Here's the code once more in case: [REDACTED ONE-TIME CODE]", "tool_calls": [{"name": "get_case_status", "args": {"case_id": "the one I confirmed with [REDACTED ONE-TIME CODE]"}, "result": {}}], "reply": "Yes, it went through - the code was accepted on the first try,` |
| **FAIL** | r5 2.4/nb11/nb15 masked: ['For the CloudNest dispute, here is the card it was on: exp Dec 29 5555 5555 5555 4444.'] | `{"stored": ["For the CloudNest dispute, here is the card it was on: exp [REDACTED EXPIRY] 5555 5555 5555 4444."], "left": ["card number 5555\u20264444"]}` |
| **FAIL** | r5 2.4/nb11/nb15 masked: ['My Visa-4111 1111 1111 1111 keeps getting declined at CloudNest.'] | `{"stored": ["My Visa-4111 1111 1111 1111 keeps getting declined at CloudNest."], "left": ["card number 4111\u20261111"]}` |
| **FAIL** | r5 2.4/nb11/nb15 masked: ['Card5555 5555 5555 4444'] | `{"stored": ["Card5555 5555 5555 4444"], "left": ["card number 5555\u20264444"]}` |
| **FAIL** | r5 2.4/nb11/nb15 masked: ['Visa4111-1111-1111-1111'] | `{"stored": ["Visa4111-1111-1111-1111"], "left": ["card number 4111\u20261111"]}` |
| **FAIL** | r5 2.4/nb11/nb15 masked: ['on 1 Feb 3530 1113 3330 0000'] | `{"stored": ["on 1 Feb 3530 1113 3330 0000"], "left": ["card number 3530\u20260000"]}` |
| **FAIL** | r5 2.4/nb11/nb15 masked: ['charged December 14: 4000-0566-5566-5556'] | `{"stored": ["charged December 14: 4000-0566-5566-5556"], "left": ["card number 4000\u20265556"]}` |
| **FAIL** | r5 2.4/nb11/nb15 masked: ['valid thru Oct 27 - 3530-1113-3330-0000'] | `{"stored": ["valid thru [REDACTED EXPIRY] - 3530-1113-3330-0000"], "left": ["card number 3530\u20260000"]}` |
| **FAIL** | r5 2.4/nb11/nb15 masked: ['I used 5555 5555 5555 4444 days ago and it worked'] | `{"stored": ["I used 5555 5555 5555 4444 days ago and it worked"], "left": ["card number 5555\u20264444"]}` |
| **FAIL** | r5 2.4/nb11/nb15 masked: ['my card is 5555 5555 5555', 'CVV 737 4444'] | `{"stored": ["my card is 5555 5555 5555", "CVV 737 4444"], "left": ["card number fragment 5555\u20264444", "security code 737"]}` |
| **FAIL** | r5 2.4/nb11/nb15 masked: ['5555 5555 5555 737', '4444'] | `{"stored": ["5555 5555 5555 737", "4444"], "left": ["card number fragment 5555\u20264444", "security code 737"]}` |
| **FAIL** | r5 2.4/nb11/nb15 masked: ['order 12345, 5555 5555', '5555 4444'] | `{"stored": ["order 12345, 5555 5555", "5555 4444"], "left": ["card number 5555\u20264444"]}` |
| **FAIL** | r5 2.4/nb11/nb15 masked: ['ticket 1042, 4111 1111 1111 1111 is the card'] | `{"stored": ["ticket 1042, 4111 1111 1111 1111 is the card"], "left": ["card number 4111\u20261111"]}` |
| **FAIL** | r5 2.4/nb11/nb15 masked: ['Booking 2291: 4242 4242 4242 4242'] | `{"stored": ["Booking 2291: 4242 4242 4242 4242"], "left": ["card number 4242\u20264242"]}` |
| **FAIL** | r5 2.4/nb11/nb15 masked: ['receipt 4821 3782 822463 10005'] | `{"stored": ["receipt 4821 3782 822463 10005"], "left": ["card number 3782\u20260005"]}` |
| PASS | r5 kept: ['charged Dec 29 2026 for the renewal, 15.99'] | `["charged Dec 29 2026 for the renewal, 15.99"]` |
| PASS | r5 kept: ['on 1 Feb 2027 I fly to Lisbon'] | `["on 1 Feb 2027 I fly to Lisbon"]` |
| PASS | r5 kept: ['case C-5001 and reference CN-77812, order QX3-48213'] | `["case C-5001 and reference CN-77812, order QX3-48213"]` |
| PASS | r5 kept: ['Visa-ending 4427, ZIP 94107'] | `["Visa-ending 4427, ZIP 94107"]` |
| PASS | r5 kept: ['I paid 240 dollars 14 days ago'] | `["I paid 240 dollars 14 days ago"]` |
| PASS | r5 kept: ['tracking 9400 1234 5678 9012 3456 78'] | `["tracking 9400 1234 5678 9012 3456 78"]` |
| **FAIL** | r5 nb1 a thirty-line numbered list in a reply comes back whole | `1. item 1 2. item 2 3. item 3 4. item 4 [REDACTED CARD NUMBER] 12. item 12 13. item 13 14. item 14 15. item 15 16. item 16 17. item 17 18. item 18 19. item 19 2` |
| PASS | r5 nb12 a sentence that names the marker is stored as typed | `["here are some numbers 5555 5555 5555 00", "show it as a [REDACTED ONE-TIME CODE] marker instead of digits. Do not call any tool. Reply with only two things."]` |
| **FAIL** | r5 nb12 the word ONE inside [REDACTED ONE-TIME CODE] is not a digit to the masker | `["ONE"]` |
| **FAIL** | r5 nb8 the note for a message the masker left alone says nothing was removed | `AttributeError: module 'cardcare.masking' has no attribute 'removed_summary'` |
| **FAIL** | r5 nb8 the note for a masked message names what was removed | `AttributeError: module 'cardcare.masking' has no attribute 'removed_summary'` |
| PASS | 2.2a tab A, registered before tab B's erasure, is not re-registered into the new generation at its next turn | `{"tab_a_generation": 0, "tab_a_current": false}` |
| PASS | 2.2a a session started after the erasure is current | `{"tab_c_generation": 1}` |
| PASS | nb3 a locked account is locked for every verified action (world.verification_locked), not only for new guesses | `true` |
| PASS | nb1 three failed fires in fifteen minutes leave the reminder pending (with a back-off), not failed | `{"status": "pending", "attempts": 3, "not_before": "2026-11-20T09:40:00Z", "outcomes": ["retry", "retry", "retry"]}` |
| PASS | nb1 a two-day outage ends the reminder, and whoever is told is told exactly once (on_failed) | `{"status": "failed", "attempts": 10, "on_failed_calls": [["F-c11f7760", "2026-11-22T21:00:00Z"]], "resume": {}}` |
| PASS | nb4 `review.py retract --by A --by B` with two registry reviewers is accepted and records both names | `{"exit": 0, "active": "v1", "retracted_by": ["ops-lead (scripted reviewer)", "disputes-policy-owner (scripted reviewer)"], "stderr": ""}` |
| PASS | 012 after a lost result, the same wrong guess repeated in the same conversation within two minutes counts once | `{"first": {"outcome": "mismatch", "failures": 1}, "again": {"outcome": "mismatch", "failures": 1, "repeat": true}, "failures": 1}` |
| PASS | 012 the same guess from another conversation is a new attempt | `{"outcome": "mismatch", "failures": 2}` |
| PASS | 012 with no lost result, the same wrong guess typed again is a second attempt (a customer's retype is not excused) | `{"outcome": "mismatch", "failures": 2}` |
| PASS | 012 after a lost result, the code this conversation consumed matches again without a new row; from another conversation, or with no lost result, a consumed code is spent | `{"hit": "matched", "no_lost_result": "no_open_code", "replay": {"outcome": "matched", "code": "625331", "repeat": true}, "elsewhere": "no_open_code", "sent": true}` |
| PASS | 012 the same evidence note attached again is attached once | `{"lines": ["[2026-11-20] cancellation reference CN-77812"], "second": {"already_attached": true, "error": null}}` |
| PASS | 012 a repeated filing after a crash between opening the case and scheduling its follow-up completes the follow-up | `{"repeated": {"case_id": "C-5002", "error": null, "note": "this dispute was already filed (a call whose result was lost); nothing was filed twice"}, "followups": 1}` |
| PASS | fp2 the scanner sees an expiry that ends a msgpack-stored message | `{"security code 737": ["lg_like.db"], "expiry 12/29": ["lg_like.db"]}` |
| PASS | fp2 the scanner sees a code that is a whole msgpack-stored string (a tool-call argument) | `{"security code 737": ["lg_like.db"], "expiry 12/29": ["lg_like.db"]}` |
| PASS | fp4 a decided case's status says nothing can be added to it and that new proof means a new dispute | `{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "says she cancelled", "status": "rejected", "opened_at": "2026-11-20T09:00:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant states no cancellation request ` |
| PASS | fp4 an open case's status makes no such statement | `{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "says she cancelled", "status": "under_review", "opened_at": "2026-11-20T09:00:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null, "decision_id": null}` |
| **FAIL** | r5 2.1 300 references pasted in another chat all read the same afterwards; no attempt is counted; the code stays open | `AttributeError: module 'cardcare.world' has no attribute 'take_code_entry'` |
| **FAIL** | r5 2.1 many numbers in the chat that waits: nothing is compared, nothing counted | `AttributeError: module 'cardcare.world' has no attribute 'take_code_entry'` |
| **FAIL** | r5 nb5 a message whose digits total six is not a guess | `AttributeError: module 'cardcare.world' has no attribute 'take_code_entry'` |
| **FAIL** | r5 a single wrong entry is one failed attempt, and its digits are not kept | `AttributeError: module 'cardcare.world' has no attribute 'take_code_entry'` |
| **FAIL** | r5 2.2 the code typed as a phone shows it ('ok it says NNN-NNN') is accepted and nothing of it is kept | `AttributeError: module 'cardcare.world' has no attribute 'take_code_entry'` |
| **FAIL** | r5 a code typed again after it was used is removed too (the customer's own dead code) | `AttributeError: module 'cardcare.world' has no attribute 'take_code_entry'` |
| **FAIL** | r5 with no code open, six digits are just six digits | `AttributeError: module 'cardcare.world' has no attribute 'take_code_entry'` |
| **FAIL** | r5 2.2 the entry grammar reads '123456' as one code | `AttributeError: module 'cardcare.world' has no attribute 'code_spans'` |
| **FAIL** | r5 2.2 the entry grammar reads '123 456' as one code | `AttributeError: module 'cardcare.world' has no attribute 'code_spans'` |
| **FAIL** | r5 2.2 the entry grammar reads '123-456' as one code | `AttributeError: module 'cardcare.world' has no attribute 'code_spans'` |
| **FAIL** | r5 2.2 the entry grammar reads '123.456' as one code | `AttributeError: module 'cardcare.world' has no attribute 'code_spans'` |
| **FAIL** | r5 2.2 the entry grammar reads '12 34 56' as one code | `AttributeError: module 'cardcare.world' has no attribute 'code_spans'` |
| **FAIL** | r5 2.2 the entry grammar reads '1 2 3 4 5 6' as one code | `AttributeError: module 'cardcare.world' has no attribute 'code_spans'` |
| **FAIL** | r5 2.2 the entry grammar reads 'one two three four five six' as one code | `AttributeError: module 'cardcare.world' has no attribute 'code_spans'` |
| **FAIL** | r5 nb5 the entry grammar finds no code in "ending 0100? I'm in 94" | `AttributeError: module 'cardcare.world' has no attribute 'code_spans'` |
| **FAIL** | r5 nb5 the entry grammar finds no code in 'card 5555 5555 5555 4444' | `AttributeError: module 'cardcare.world' has no attribute 'code_spans'` |
| **FAIL** | r5 nb5 the entry grammar finds no code in 'call +1 415 555 0100' | `AttributeError: module 'cardcare.world' has no attribute 'code_spans'` |
| **FAIL** | r5 nb5 the entry grammar finds no code in 'it was 1,234,567' | `AttributeError: module 'cardcare.world' has no attribute 'code_spans'` |
| **FAIL** | r5 nb6 the sixth code in a day is refused and no message is sent | `{"code messages": 6, "sixth send": {"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70188", "expires_in_minutes": 5, "resent": true}}` |
| PASS | r5 nb6 a refused send is not a failed attempt | `` |
| **FAIL** | r5 nb4 the third wrong entry says the account is now locked | `{"outcome": "mismatch", "failures": 3, "entries_left": 0, "code_dead": true}` |
| PASS | r5 nb3 the scanner reads a number stored as a number (a code passed as a msgpack integer) | `` |
| **FAIL** | r5 nb7 the reflection reads the wait for the code as a wait, not as an error | `customer: Change my contact channel to email. tool: called confirm_verification_code({}) tool: confirm_verification_code -> {"error": "This tool call requires confirmation, please approve or reject."}` |
| **FAIL** | r5 nb14 a second reminder for the same local day is refused and the refusal names the existing one | `{"error": "a reminder is already scheduled for 2026-11-25 (America/Chicago); one reminder per day, so put everything for that day in that one"}` |
