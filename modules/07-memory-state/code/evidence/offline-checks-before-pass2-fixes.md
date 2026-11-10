# Offline checks: 168/170 passed

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
| PASS | r5 2.4/nb11/nb15 masked: ['For the CloudNest dispute, here is the card it was on: exp Dec 29 5555 5555 5555 4444.'] | `{"stored": ["For the CloudNest dispute, here is the card it was on: exp [REDACTED EXPIRY] [REDACTED CARD NUMBER]."], "left": []}` |
| PASS | r5 2.4/nb11/nb15 masked: ['My Visa-4111 1111 1111 1111 keeps getting declined at CloudNest.'] | `{"stored": ["My Visa-[REDACTED CARD NUMBER] keeps getting declined at CloudNest."], "left": []}` |
| PASS | r5 2.4/nb11/nb15 masked: ['Card5555 5555 5555 4444'] | `{"stored": ["Card[REDACTED CARD NUMBER]"], "left": []}` |
| PASS | r5 2.4/nb11/nb15 masked: ['Visa4111-1111-1111-1111'] | `{"stored": ["Visa[REDACTED CARD NUMBER]"], "left": []}` |
| PASS | r5 2.4/nb11/nb15 masked: ['on 1 Feb 3530 1113 3330 0000'] | `{"stored": ["on 1 Feb [REDACTED CARD NUMBER]"], "left": []}` |
| PASS | r5 2.4/nb11/nb15 masked: ['charged December 14: 4000-0566-5566-5556'] | `{"stored": ["charged December 14: [REDACTED CARD NUMBER]"], "left": []}` |
| PASS | r5 2.4/nb11/nb15 masked: ['valid thru Oct 27 - 3530-1113-3330-0000'] | `{"stored": ["valid thru [REDACTED EXPIRY] - [REDACTED CARD NUMBER]"], "left": []}` |
| PASS | r5 2.4/nb11/nb15 masked: ['I used 5555 5555 5555 4444 days ago and it worked'] | `{"stored": ["I used [REDACTED CARD NUMBER] days ago and it worked"], "left": []}` |
| PASS | r5 2.4/nb11/nb15 masked: ['my card is 5555 5555 5555', 'CVV 737 4444'] | `{"stored": ["my card is [REDACTED CARD DIGITS]", "CVV [REDACTED SECURITY CODE] [REDACTED CARD DIGITS]"], "left": []}` |
| PASS | r5 2.4/nb11/nb15 masked: ['5555 5555 5555 737', '4444'] | `{"stored": ["[REDACTED CARD DIGITS] [REDACTED SECURITY CODE]", "[REDACTED CARD DIGITS]"], "left": []}` |
| PASS | r5 2.4/nb11/nb15 masked: ['order 12345, 5555 5555', '5555 4444'] | `{"stored": ["order 12345, [REDACTED CARD DIGITS]", "[REDACTED CARD DIGITS]"], "left": []}` |
| PASS | r5 2.4/nb11/nb15 masked: ['card ending 4444 zip 94107', '5555 5555', '5555'] | `{"stored": ["card ending 4444 zip 94107", "[REDACTED CARD DIGITS]", "[REDACTED CARD DIGITS]"], "left": []}` |
| PASS | r5 2.4/nb11/nb15 masked: ['ticket 1042, 4111 1111 1111 1111 is the card'] | `{"stored": ["ticket 1042, [REDACTED CARD NUMBER] is the card"], "left": []}` |
| PASS | r5 2.4/nb11/nb15 masked: ['Booking 2291: 4242 4242 4242 4242'] | `{"stored": ["Booking 2291: [REDACTED CARD NUMBER]"], "left": []}` |
| PASS | r5 2.4/nb11/nb15 masked: ['receipt 4821 3782 822463 10005'] | `{"stored": ["receipt 4821 [REDACTED CARD NUMBER]"], "left": []}` |
| PASS | r5 kept: ['charged Dec 29 2026 for the renewal, 15.99'] | `["charged Dec 29 2026 for the renewal, 15.99"]` |
| PASS | r5 kept: ['on 1 Feb 2027 I fly to Lisbon'] | `["on 1 Feb 2027 I fly to Lisbon"]` |
| PASS | r5 kept: ['case C-5001 and reference CN-77812, order QX3-48213'] | `["case C-5001 and reference CN-77812, order QX3-48213"]` |
| PASS | r5 kept: ['Visa-ending 4427, ZIP 94107'] | `["Visa-ending 4427, ZIP 94107"]` |
| PASS | r5 kept: ['I paid 240 dollars 14 days ago'] | `["I paid 240 dollars 14 days ago"]` |
| PASS | r5 kept: ['tracking 9400 1234 5678 9012 3456 78'] | `["tracking 9400 1234 5678 9012 3456 78"]` |
| PASS | r5 nb1 a thirty-line numbered list in a reply comes back whole | `1. item 1 2. item 2 3. item 3 4. item 4 5. item 5 6. item 6 7. item 7 8. item 8 9. item 9 10. item 10 11. item 11 12. item 12 13. item 13 14. item 14 15. item 1` |
| PASS | r5 nb12 a sentence that names the marker is stored as typed | `["here are some numbers 5555 5555 5555 00", "show it as a [REDACTED ONE-TIME CODE] marker instead of digits. Do not call any tool. Reply with only two things."]` |
| PASS | r5 nb12 the word ONE inside [REDACTED ONE-TIME CODE] is not a digit to the masker | `[]` |
| PASS | r5 nb8 the note for a message the masker left alone says nothing was removed | `nothing was removed from the customer's latest message: every digit in it is stored as typed` |
| PASS | r5 nb8 the note for a masked message names what was removed | `removed from the customer's latest message before it reached you or any store: 1 card number, 1 expiry; everything else in it is stored as typed` |
| **FAIL** | pass 2: what follows the code at that seam is marked as part of the card number, not as a second code | `"CVC [REDACTED SECURITY CODE] [REDACTED SECURITY CODE]"` |
| PASS | blind: a code at the seam of a number sent in two goes, after an earlier card paste, is masked ('CVC 047 1111') | `["The closed one, in two goes: [REDACTED CARD DIGITS]", "CVC [REDACTED SECURITY CODE] [REDACTED SECURITY CODE]"]` |
| PASS | blind: a month name and two digits directly before a card number are its expiry ('September 27 4242 ...') | `["Here's my old card note: [REDACTED EXPIRY] [REDACTED CARD NUMBER] / cvc [REDACTED SECURITY CODE]."]` |
| PASS | blind: the same words after a date word stay a date ('charged on September 27 4242 ...'), the number still masked | `["It was charged on September 27 [REDACTED CARD NUMBER] and again in October."]` |
| PASS | blind: the words after a number and its unit word are stored as typed ('... days ago, so it can't be that one.') | `["I stopped using [REDACTED CARD NUMBER] days ago, so it can't be that one."]` |
| PASS | blind: a nineteen-line numbered list whose items hold other numbers comes back whole from the reply path | `1. Charge 2 power banks 2. Keep 75 euros in cash 3. Verify your phone number 4. Turn on alerts 5. Tell 90 family members 6. Pack 75 copies of your passport 7. Save the 7-hour helpline number 8. Save t` |
| PASS | blind: the same list typed by a customer is stored as typed | `1. Charge 2 power banks 2. Keep 75 euros in cash 3. Verify your phone number 4. Turn on alerts 5. Tell 90 family members 6. Pack 75 copies of your passport 7. Save the 7-hour helpline number 8. Save t` |
| PASS | blind: a numbered list written on one line, numbers in its items, comes back whole | `Bring: 1. two adapters 2. 75 euros 3. 12 photos 4. 30 pills 5. 90 dollars 6. 7 shirts 7. 3 books 8. 24 socks 9. 2 hats 10. 75 stamps 11. 12 pens 12. 5 maps 13. 9 keys 14. 4 bags` |
| PASS | blind: a card number typed as a numbered list is still a card number | `["1. [REDACTED CARD NUMBER]"]` |
| PASS | blind (harness): a reply that only names the pattern singles out no candidate | `None` |
| PASS | blind (harness): a reply that shows one reference as a marker among others with digits still singles that one out | `` |
| PASS | 2.2a tab A, registered before tab B's erasure, is not re-registered into the new generation at its next turn | `{"tab_a_generation": 0, "tab_a_current": false}` |
| PASS | 2.2a a session started after the erasure is current | `{"tab_c_generation": 1}` |
| PASS | nb3 a locked account is locked for every verified action (world.verification_locked), not only for new guesses | `true` |
| PASS | nb1 three failed fires in fifteen minutes leave the reminder pending (with a back-off), not failed | `{"status": "pending", "attempts": 3, "not_before": "2026-11-20T09:40:00Z", "outcomes": ["retry", "retry", "retry"]}` |
| PASS | nb1 a two-day outage ends the reminder, and whoever is told is told exactly once (on_failed) | `{"status": "failed", "attempts": 10, "on_failed_calls": [["F-01377ca1", "2026-11-22T21:00:00Z"]], "resume": {}}` |
| PASS | nb4 `review.py retract --by A --by B` with two registry reviewers is accepted and records both names | `{"exit": 0, "active": "v1", "retracted_by": ["ops-lead (scripted reviewer)", "disputes-policy-owner (scripted reviewer)"], "stderr": ""}` |
| PASS | 012 after a lost result, the same wrong guess repeated in the same conversation within two minutes counts once | `{"first": {"outcome": "mismatch", "failures": 1}, "again": {"outcome": "mismatch", "failures": 1, "repeat": true}, "failures": 1}` |
| PASS | 012 the same guess from another conversation is a new attempt | `{"outcome": "mismatch", "failures": 2}` |
| PASS | 012 with no lost result, the same wrong guess typed again is a second attempt (a customer's retype is not excused) | `{"outcome": "mismatch", "failures": 2}` |
| PASS | 012 after a lost result, the code this conversation consumed matches again without a new row; from another conversation, or with no lost result, a consumed code is spent | `{"hit": "matched", "no_lost_result": "no_open_code", "replay": {"outcome": "matched", "code": "282553", "repeat": true}, "elsewhere": "no_open_code", "sent": true}` |
| PASS | 012 the same evidence note attached again is attached once | `{"lines": ["[2026-11-20] cancellation reference CN-77812"], "second": {"already_attached": true, "error": null}}` |
| PASS | 012 a repeated filing after a crash between opening the case and scheduling its follow-up completes the follow-up | `{"repeated": {"case_id": "C-5002", "error": null, "note": "this dispute was already filed (a call whose result was lost); nothing was filed twice"}, "followups": 1}` |
| PASS | fp2 the scanner sees an expiry that ends a msgpack-stored message | `{"security code 737": ["lg_like.db"], "expiry 12/29": ["lg_like.db"]}` |
| PASS | fp2 the scanner sees a code that is a whole msgpack-stored string (a tool-call argument) | `{"security code 737": ["lg_like.db"], "expiry 12/29": ["lg_like.db"]}` |
| PASS | fp4 a decided case's status says nothing can be added to it and that new proof means a new dispute | `{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "says she cancelled", "status": "rejected", "opened_at": "2026-11-20T09:00:00Z", "resolution_code": "NO_CANCELLATION_PROOF", "resolution_note": "Merchant states no cancellation request ` |
| PASS | fp4 an open case's status makes no such statement | `{"case_id": "C-5001", "user_id": "priya", "txn_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "says she cancelled", "status": "under_review", "opened_at": "2026-11-20T09:00:00Z", "resolution_code": null, "resolution_note": null, "resolved_at": null, "decision_id": null}` |
| PASS | r5 2.1 300 references pasted in another chat all read the same afterwards; no attempt is counted; the code stays open | `{"distinct renderings of the 300 references": 1, "failures": 0, "open codes": 1}` |
| PASS | r5 2.1 many numbers in the chat that waits: nothing is compared, nothing counted | `{"outcome": "several_numbers"}` |
| PASS | r5 nb5 a message whose digits total six is not a guess | `{"text": "It hasn't arrived. Is it going to the number ending 0100? I'm in 94", "entry": {"outcome": "no_code_entered"}}` |
| PASS | r5 a single wrong entry is one failed attempt, and its digits are not kept | `{"text": "[REDACTED ONE-TIME CODE]", "entry": {"outcome": "mismatch", "failures": 1, "entries_left": 2, "code_dead": false, "account_locked": false}}` |
| PASS | r5 2.2 the code typed as a phone shows it ('ok it says NNN-NNN') is accepted and nothing of it is kept | `{"text": "ok it says [REDACTED ONE-TIME CODE]", "entry": {"outcome": "matched"}}` |
| PASS | r5 a code typed again after it was used is removed too (the customer's own dead code) | `here it is once more: [REDACTED ONE-TIME CODE]` |
| PASS | r5 with no code open, six digits are just six digits | `{"text": "my order number is 482913", "entry": null}` |
| PASS | r5 ten minutes after a code was sent and never typed, an order number in another chat is kept; the expired code itself is not | `{"text": "my order number is 482913, and that old code was [REDACTED ONE-TIME CODE]", "entry": null}` |
| PASS | r6 a code written with a comma, or as four digits and two, is not an entry and not kept: it is removed and that code cancelled | `{"removed and reported": [true, true], "codes": ["cancelled", "cancelled"], "failures": 0}` |
| PASS | r6 an amount, a date, a clock time and a points balance are not codes: kept as typed, the code stays open | `{"text": "I paid $1,234.56 on 2026-11-13 at 10:02:00 and I have 123,456 points", "entry": {"outcome": "no_code_entered"}}` |
| PASS | r6 the wait is for a code this turn's message did not answer | `{"sent this turn, the message was read before it": true, "sent earlier, the message held no code": true, "sent earlier, the message was a wrong entry": false, "another conversation": false}` |
| PASS | r6 no code starts with a zero (200 sends) | `["1", "2", "3", "4", "5", "6", "7", "8", "9"]` |
| **FAIL** | pass 2: asked for a new code six minutes after one was sent, the tool result says that code has expired, and nothing waits for it | `{"told": "{\"verified\": false, \"customer_wrote\": \"That text never showed up and it must have run out by now. Please send me a new code.\", \"note\": \"the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call confirm_verification_code agai` |
| PASS | r5 2.2 the entry grammar reads '123456' as one code | `[[11, 17, "123456"]]` |
| PASS | r5 2.2 the entry grammar reads '123 456' as one code | `[[11, 18, "123456"]]` |
| PASS | r5 2.2 the entry grammar reads '123-456' as one code | `[[11, 18, "123456"]]` |
| PASS | r5 2.2 the entry grammar reads '123.456' as one code | `[[11, 18, "123456"]]` |
| PASS | r5 2.2 the entry grammar reads '12 34 56' as one code | `[[11, 19, "123456"]]` |
| PASS | r5 2.2 the entry grammar reads '1 2 3 4 5 6' as one code | `[[11, 22, "123456"]]` |
| PASS | r5 2.2 the entry grammar reads 'one two three four five six' as one code | `[[11, 38, "123456"]]` |
| PASS | r5 nb5 the entry grammar finds no code in "ending 0100? I'm in 94" | `[]` |
| PASS | r5 nb5 the entry grammar finds no code in 'card 5555 5555 5555 4444' | `[]` |
| PASS | r5 nb5 the entry grammar finds no code in 'call +1 415 555 0100' | `[]` |
| PASS | r5 nb5 the entry grammar finds no code in 'it was 1,234,567' | `[]` |
| PASS | r5 nb6 the sixth code in a day is refused and no message is sent | `{"code messages": 5, "sixth send": {"error": "5 codes were sent to this account in the last 24 hours, which is the limit; no code is sent and none can be until 2026-11-21T09:00:00Z. A code already sent stays valid for its 5 minutes; otherwise the customer must call Kestrel"}}` |
| PASS | r5 nb6 a refused send is not a failed attempt | `` |
| PASS | r5 nb4 the third wrong entry says the account is now locked | `{"outcome": "mismatch", "failures": 3, "entries_left": 0, "code_dead": true, "account_locked": true}` |
| PASS | r5 2.2 the stored-code search finds a code kept with a space ('481 975') | `["lg_code_481975.db"]` |
| PASS | r5 2.2 the stored-code search finds a code kept in a sentence with a dash | `["lg_code_447526.db"]` |
| PASS | r5 nb3 the stored-code search finds a code kept as a number | `["lg_code_517391.db"]` |
| PASS | r5 the stored-code search does not take a clock time for a code | `` |
| PASS | r5 nb3 the stored-code search finds a code that lost its leading zero when kept as a number | `["lg_code_048213.db"]` |
| PASS | r5 nb3 the scanner reads a number stored as a number (a code passed as a msgpack integer) | `` |
| PASS | r5 the scanner takes no stored count for a security code or an expiry (token counts of 123, 12 and 29) | `[]` |
| PASS | r6 the scanner takes no checkpoint timestamp for a security code ('…T17:43:21.497049+00:00' and the code 4321), and still finds one typed beside it | `` |
| PASS | r5 nb7 the reflection reads the wait for the code as a wait, not as an error | `el to email. tool: confirm_verification_code: waiting for the customer to type the one-time code (the conversation pauses here by design; this is how the step-up works, not an error and not a mistake)` |
| PASS | r5 nb14 a second reminder for the same local day is refused and the refusal names the existing one | `{"error": "a reminder is already scheduled for 2026-11-25 (America/Chicago): F-a7f1672a at 09:00 CST; one reminder per day, so put everything for that day in that one (cancel_reminder it first to replace it)", "existing_followup_id": "F-a7f1672a"}` |
