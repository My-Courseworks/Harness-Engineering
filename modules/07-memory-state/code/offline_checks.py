"""Offline probes for the round-4 review's findings that a live conversation cannot reach, or reaches only by chance.

    python offline_checks.py [--out evidence/offline-checks.md]

No model call. Each check fails on the round-4 code (`d4bae63`) for the reason the review gave and passes after the
fix; the "before" table is in evidence/adversarial-baseline-r4/offline-checks-before.md. Exit status 1 if any fails.

What is covered, in the review's numbering:
- 2.1  the masker on the review's own leak list (a 3-4 digit token or an order label before the number in one run; a ZIP
       in the message that opens a split number; the rest of a number whose last four was already given), and the keep
       cases the same change must not touch;
- 2.2a an open second tab is not re-registered in the new generation after an erasure in another tab;
- nb 2 a reflection with an empty summary is not an episode;
- nb 3 three failures lock the account for every verified action, not only for new verifications;
- nb 1 the scheduler backs off between failed fires, keeps a record through a short outage, and tells someone when it gives up;
- nb 4 `review.py retract` with two `--by` names;
- nb 5 the reasoning masker leaves "card last4 8830" alone;
- nb 6 two comma-joined numbers in a reply are both masked;
- nb 8 the paired storage-claim check does not fail an honest agent over a store that leaked something else;
- 012  (the captain's question) a write tool called again after its result was lost to a crash is recognised as a repeat;
- fp1  (found by round 5's first declared-final pass, not by the review) a security code said twice in one message, in
       words and digits or typed twice: the two renderings joined into one six-digit run that was neither a code nor a
       card. These fail on `8051dbd`; that "before" is in evidence/adversarial-before-code-said-twice/;
- fp2  (found by twelve more unscripted runs before the second final pass) an expiry written as a month name and two
       digits ("July / 29"), and a bare last four beside a ZIP masked as a security code right after a card paste. These
       fail on `f0300c2`; that "before" is in evidence/adversarial-before-sweep-shapes/. And the check of the check: the
       store scanner must see a secret that begins or ends a string stored as msgpack (LangGraph's checkpoints), which
       the scanner of `f0300c2` did not (scanner-check-before.md in the same folder);
- fp3  (found by the tuning pass before the second final pass) the turn the harness returns carries no one-time code even
       when the model repeated one the customer typed. Fails on `1a31895` (evidence/adversarial-before-reply-echo/);
- fp4  (found by the second declared-final pass) the status of a decided case says what can still be done with it.
       Fails on `5140524` (evidence/adversarial-before-case-next-step/);
- r5   the round-5 review: the code entry as one definition applied at the door (2.1, 2.2, nb 5), the cap and the lock
       message (nb 4, nb 6), the masker when a date, a name or a unit word takes a group out of a number (2.4), splits with
       a token at the seam and labels (nb 11, nb 15), a numbered list in a reply (nb 1), the marker's own words (nb 12),
       what the masker removed as a record (nb 8), numbers in the scanner (nb 3), the wait as the reflection reads it
       (nb 7), a second reminder (nb 14). These fail on `3644feb` (evidence/adversarial-baseline-r5/offline-checks-before.md).
"""

import argparse
import asyncio
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from cardcare import episodes, masking, privacy, procedures, scenario, scheduler, store_audit, world
from cardcare.memory_policy import MAX_VERIFICATION_ATTEMPTS

CODE_DIR = Path(__file__).resolve().parent
NOW = "2026-11-20T09:00:00Z"
PANS = ["5555555555554444", "378282246310005", "2223003122003222", "4000056655665556", "4111111111111111"]

# the review's offline leak list (report 2.1), verbatim, plus one line per family of its seeded table
REVIEW_LEAKS = [
    ["CVV: 737 5555 5555 5555 4444"],
    ["Here's everything: CVV 737 5555 5555 5555 4444 exp 12/29"],
    ["1229 5555 5555 5555 4444"],
    ["PIN 1234 5555 5555 5555 4444"],
    ["Order 12345 5555 5555 5555 4444 was declined"],
    ["order 12345, 5555 5555 5555 4444"],
    ["5555 5555 5555 and my zip is 94107", "4444"],
    ["card ending 4444, zip 94107", "and the first twelve: 5555 5555 5555"],
    ["security code 7891; 3782 822463 10005"],
    ["exp 0827: 3782 822463 10005"],
    ["PIN 7293; 2223-0031-2200-3222"],
    ["order no. 2654861; 3782 822463 10005"],
    ["Order 1614993, 4000 0566 5566 5556"],
]
# what the same change must leave alone: references, tracking numbers and amounts that are not cards
REVIEW_KEEPS = [
    "order 2654861 arrived broken",
    "tracking 9400 1234 5678 9012 3456 78",
    "booking ref QX3-48213, and the invoice was 5678 9012",
    "my last four are 4427 and the order was 12345",
    "call me on +1 415 555 0100 about order 1614993",
    "the charge on 2026-11-01 for 1,299.00 and another for 15.99",
]

# the first round-5 final pass: its unscripted customer's own line, then the same code said twice in other ways
SAID_TWICE_LEAKS = [
    "old card: 6011 1111 1111 1117\nsecurity code: three eight six (386)\nexpiry: 07/29\nplease just file the CloudNest dispute",
    "security code 386 (three eight six)",
    "my cvv: 3 8 6 (386)",
    "security code is 386 [three eight six]",
    "cvv three eight six = 386",
    "cvv: three eight six/386",
    "security code: three, eight, six (386)",
    "security code - three eight six - 386",
    "the code on the back: seven three seven (737)",
    "card 6011 1111 1111 1117 cvv 386 386",
    "cvc 386-386",
    "sec code three eight six, in digits 386",
    # found while writing the lines above: a code dictated one digit at a time with commas, said once
    "security code: three, eight, six",
    "cvv 3, 8, 6",
    # found while checking the fix: an expiry typed with a space or a dot after its cue ("12.29" read as an amount, "12 29"
    # as two numbers); on `8051dbd` the first of these was hidden only because the card match ran on through "exp" by chance
    "5555 5555 5555 4444, exp 12 29, cvv 737",
    "card 6011 1111 1111 1117 expiry 07 29",
    "6011 1111 1111 1117 exp 07.29 cvv 386",
    "6011111111111117 expires 07 2029 cvv 386",
    "exp 07 29",
    "6011 1111 1111 1117 expires 07 29",
    "exp Jul 29",
    # ... and a card match that ran on through "cvv" into a spaced code, leaving its last digit beside the restatement
    "4111111111111111, cvv 1 8 1 = 181",
]
# a number restated in brackets that is not a code, and a last four said twice: unchanged before and after
SAID_TWICE_KEEPS = [
    "I was charged 386 (three payments) by CloudNest",
    "room 204 (two oh four) at the hotel in Lisbon",
    "flight 386 (three eight six) to Lisbon on November 30",
    "my last four are 4427 (four four two seven) and ZIP 94107",
    "order 5001 (2026) arrived late",
    "I disputed charges 1, 2, 3 and 4 on the list",
    "it was one, two, three weeks ago, I forget",
    "I paid 12.29 for parking and 7.29 for coffee",
    "my travel notice expiration should be 12 10",
    "exp. delivery 11 24, order 2654861",
    "my trial exp Jul 29, please cancel it before then",
    "the parcel arrives Jul 29",
]

# before the second final pass the unscripted "notes-app paste" persona was run twelve more times on the fixed code: one
# customer wrote her expiry as "July / 29" (kept raw, and invisible to the scanner until it learned the shape), and one
# answered the verification question right after her paste with "it's 5127 and ZIP 60614", which was masked as a security code
SWEEP_LEAKS = [
    ["expiry: July / 29"],
    ["exp Jul '29"],
    ["old card: 6011 1111 1111 1117\nsec code: 386\nexpiry: Jul/29"],
    ["the card expires July of 29"],
    ["exp Jul 33"],
    ["expiry: seven twenty-nine"],
    ["old card: 6011 1111 1111 1117", "cvv 1386 and ZIP 60614"],
    ["old card: 6011 1111 1111 1117", "386 and ZIP 60614"],
    # the scanner, once it could see a month name with an apostrophe year, found this in the independent fuzzer's corpus:
    # one of its twelve expiry phrasings had never been masked, and had never been counted as a miss
    ["starts 6011 1111 1111", "next 1117", "expires end of July '29"],
    ["oh, expires end of July '29"],
    ["old card 6011 1111 1111 1117, expiring Jul '29"],
]
SWEEP_KEEPS = [
    ["old card: 6011 1111 1111 1117\nsecurity code: 386\nexpiry: 07/29", "Fine, it's 5127 and ZIP 60614."],
    ["old card: 6011 1111 1111 1117\nsecurity code: 386\nexpiry: 07/29", "5127, ZIP 60614."],
    ["my trial exp Jul 29, cancel it before then"],
    ["the parcel arrives July / 29 at the latest"],
    ["my subscription expires end of July '29"],
    ["the dispute window expires December 2026, right?"],
    ["my travel notice expires July 2029"],
]


def _secrets_left(stored: list[str]) -> list[str]:
    return store_audit.secrets_left("\n".join(stored), {"pans": PANS, "codes": ["737", "7891", "7293", "1234"], "expiries": ["12/29", "08/27"]})


def check_masker_leaks() -> list[tuple[str, bool, str]]:
    rows = []
    for messages in REVIEW_LEAKS:
        stored = masking.mask_conversation(messages)
        left = _secrets_left(stored)
        rows.append((f"2.1 masked: {messages!r}", not left, json.dumps({"stored": stored, "left": left})))
    for message in REVIEW_KEEPS:
        stored = masking.mask_conversation([message])
        rows.append((f"2.1 kept: {message!r}", stored == [masking.normalize(message)], json.dumps(stored)))
    return rows


def check_code_said_twice() -> list[tuple[str, bool, str]]:
    secrets = {"pans": ["6011111111111117", "5555555555554444", "4111111111111111"], "codes": ["386", "737", "181"], "expiries": ["07/29", "12/29"]}
    rows = []
    for message in SAID_TWICE_LEAKS:
        stored = masking.mask_conversation([message])
        left = store_audit.secrets_left("\n".join(stored), secrets)
        rows.append((f"fp1 masked: {message!r}", not left, json.dumps({"stored": stored, "left": left})))
    for message in SAID_TWICE_KEEPS:
        stored = masking.mask_conversation([message])
        rows.append((f"fp1 kept: {message!r}", stored == [masking.normalize(message)], json.dumps(stored)))
    return rows


def check_sweep_shapes() -> list[tuple[str, bool, str]]:
    secrets = {"pans": ["6011111111111117"], "codes": ["386", "1386"], "expiries": ["07/29", "07/33"]}
    rows = []
    for messages in SWEEP_LEAKS:
        stored = masking.mask_conversation(messages)
        left = store_audit.secrets_left("\n".join(stored), secrets)
        rows.append((f"fp2 masked: {messages!r}", not left, json.dumps({"stored": stored, "left": left})))
    for messages in SWEEP_KEEPS:
        stored = masking.mask_conversation(messages)
        rows.append((f"fp2 last message kept as typed: {messages!r}", stored[-1] == masking.normalize(messages[-1]), json.dumps(stored)))
    return rows


def check_scanner_reads_msgpack_stores(tmp: Path) -> list[tuple[str, bool, str]]:
    """The check of the check. LangGraph's checkpoints are msgpack: a stored string is followed directly by the header byte
    of the next value. A scanner that reads the file as text and drops what is not text sees "expiry: 12/29additional_kwargs"
    and "entered737id", and its whole-token patterns match neither."""
    import sqlite3

    import ormsgpack
    path = tmp / "lg_like.db"
    with sqlite3.connect(path) as conn:
        conn.execute("CREATE TABLE writes (channel TEXT, value BLOB)")
        conn.execute("INSERT INTO writes VALUES ('messages', ?)", (ormsgpack.packb({"content": "old card, expiry: 12/29", "additional_kwargs": {}}),))
        conn.execute("INSERT INTO writes VALUES ('__pregel_tasks', ?)", (ormsgpack.packb({"name": "confirm", "args": {"entered": "737"}, "id": "call_1"}),))
    found = store_audit.card_data_locations([path], {"pans": [], "codes": ["737"], "expiries": ["12/29"]})
    return [("fp2 the scanner sees an expiry that ends a msgpack-stored message", "expiry 12/29" in found, json.dumps(found)),
            ("fp2 the scanner sees a code that is a whole msgpack-stored string (a tool-call argument)", "security code 737" in found, json.dumps(found))]


def check_reply_that_repeats_a_code() -> list[tuple[str, bool, str]]:
    """The tuning pass before the second final pass, ADK: asked "did it go through? here's the code once more", the model
    answered "... so I don't need 018899". It reads what the customer types, so it can repeat it; the turn the harness
    returns (what the customer reads, what the evidence records) must not carry the code whatever the model wrote."""
    record = {"customer": "Did it go through? Here's the code once more in case: 018899",
              "tool_calls": [{"name": "get_case_status", "args": {"case_id": "the one I confirmed with 018899"}, "result": {}}],
              "reply": "Yes, it went through - the code was accepted on the first try, so I don't need 018899."}
    returned = masking.turn_without_codes(record, record["customer"], {"018899"})
    return [("fp3 a reply that repeats a one-time code the customer typed is returned without it", "018899" not in json.dumps(returned),
             json.dumps(returned))]


def check_decided_case_says_what_can_be_done(tmp: Path) -> list[tuple[str, bool, str]]:
    """The second final pass, LangGraph, both runs: the follow-up for a rejected case told the customer to message the chat
    "and we can add it to your case". Nothing can be added to a decided case (add_case_evidence refuses and says to file a
    new dispute), but the status the model read did not say so. The record must."""
    bank = tmp / "bank_next_step.db"
    world.seed_bank(bank)
    opened, _ = world.open_case(bank, "priya", "T-1002", "cancelled_subscription", "says she cancelled", NOW)
    open_view = world.with_next_step(world.list_cases(bank, "priya", opened["case_id"])[0])
    world.resolve_case(bank, opened["case_id"], "rejected", "NO_CANCELLATION_PROOF", "Merchant states no cancellation request is on record.", NOW, "D-1")
    decided = world.with_next_step(world.list_cases(bank, "priya", opened["case_id"])[0])
    said = json.dumps(decided).lower()
    return [("fp4 a decided case's status says nothing can be added to it and that new proof means a new dispute",
             "next_step" in decided and "new dispute" in said and "nothing can be added" in said, json.dumps(decided)),
            ("fp4 an open case's status makes no such statement", "next_step" not in open_view, json.dumps(open_view))]


# ----------------------------------------------------------------------------------------------- the round-5 review
def _row(label: str, property_holds) -> tuple[str, bool, str]:
    """One check row from a thunk returning (passed, evidence). On older code the thunk may meet a function that does not
    exist yet: that is this row failing, not the whole group."""
    try:
        passed, evidence = property_holds()
        return label, bool(passed), evidence
    except Exception as exc:
        return label, False, f"{type(exc).__name__}: {exc}".replace(str(CODE_DIR), ".")


# its own lines (2.4, nb 11, nb 15), which the masker of `3644feb` stores with the number raw
R5_CARD_LEAKS = [
    ["For the CloudNest dispute, here is the card it was on: exp Dec 29 5555 5555 5555 4444."],
    ["My Visa-4111 1111 1111 1111 keeps getting declined at CloudNest."],
    ["Card5555 5555 5555 4444"],
    ["Visa4111-1111-1111-1111"],
    ["on 1 Feb 3530 1113 3330 0000"],
    ["charged December 14: 4000-0566-5566-5556"],
    ["valid thru Oct 27 - 3530-1113-3330-0000"],
    ["I used 5555 5555 5555 4444 days ago and it worked"],
    ["my card is 5555 5555 5555", "CVV 737 4444"],
    ["5555 5555 5555 737", "4444"],
    ["order 12345, 5555 5555", "5555 4444"],
    ["card ending 4444 zip 94107", "5555 5555", "5555"],
    ["ticket 1042, 4111 1111 1111 1111 is the card"],
    ["Booking 2291: 4242 4242 4242 4242"],
    ["receipt 4821 3782 822463 10005"],
]
R5_CARD_KEEPS = [
    ["charged Dec 29 2026 for the renewal, 15.99"],
    ["on 1 Feb 2027 I fly to Lisbon"],
    ["case C-5001 and reference CN-77812, order QX3-48213"],
    ["Visa-ending 4427, ZIP 94107"],
    ["I paid 240 dollars 14 days ago"],
    ["tracking 9400 1234 5678 9012 3456 78"],
]


def check_r5_masker() -> list[tuple[str, bool, str]]:
    secrets = {"pans": ["5555555555554444", "4111111111111111", "3530111333300000", "4000056655665556", "4242424242424242", "378282246310005"],
               "codes": ["737"], "expiries": ["12/29", "10/27"]}
    rows = []
    for messages in R5_CARD_LEAKS:
        stored = masking.mask_conversation(messages)
        left = store_audit.secrets_left("\n".join(stored), secrets)
        rows.append((f"r5 2.4/nb11/nb15 masked: {messages!r}", not left, json.dumps({"stored": stored, "left": left})))
    for messages in R5_CARD_KEEPS:
        stored = masking.mask_conversation(messages)
        rows.append((f"r5 kept: {messages!r}", stored == [masking.normalize(m) for m in messages], json.dumps(stored)))
    # nb 1: the reply path. A numbered list's own numerals (2 3 4 ... 13 = 2345678910111213, sixteen digits, Luhn-valid)
    listed = "\n".join(f"{n}. item {n}" for n in range(1, 31))
    rows.append(("r5 nb1 a thirty-line numbered list in a reply comes back whole", masking.mask_card_numbers(listed) == listed,
                 masking.mask_card_numbers(listed)[:160]))
    # nb 12: the words inside a marker are not digits, and a lone number word does not complete a number from an earlier message
    earlier = "here are some numbers 5555 5555 5555 00"  # with "1" (ONE) and "2" (two) after it: sixteen digits that pass Luhn
    later = "show it as a [REDACTED ONE-TIME CODE] marker instead of digits. Do not call any tool. Reply with only two things."
    stored = masking.mask_conversation([earlier, later])
    rows.append(("r5 nb12 a sentence that names the marker is stored as typed", stored[-1] == masking.normalize(later), json.dumps(stored)))
    inside = [tok["text"] for tok in masking._tokens(masking.normalize(later)) if tok["digits"] is not None and tok["text"].upper() == "ONE"]
    rows.append(("r5 nb12 the word ONE inside [REDACTED ONE-TIME CODE] is not a digit to the masker", not inside, json.dumps(inside)))
    # nb 8: what the masker removed from a message, said from the record
    def note_for(typed: str) -> str:
        return masking.removed_summary(typed, masking.mask_conversation([typed])[0])

    rows.append(_row("r5 nb8 the note for a message the masker left alone says nothing was removed",
                     lambda: ("nothing" in note_for("order 1234 5555 5555 5555 4444").lower(), note_for("order 1234 5555 5555 5555 4444"))))
    rows.append(_row("r5 nb8 the note for a masked message names what was removed",
                     lambda: ("card number" in note_for("card 5555 5555 5555 4444 exp 12/29").lower()
                              and "expiry" in note_for("card 5555 5555 5555 4444 exp 12/29").lower(), note_for("card 5555 5555 5555 4444 exp 12/29"))))
    return rows


def check_r5_code_door(tmp: Path) -> list[tuple[str, bool, str]]:
    """2.1, 2.2, nb 5: one definition of a typed code, applied at the door. Nothing the customer can read distinguishes the
    real code from another six-digit number, and only a single entry in the conversation that asked for it is compared."""
    bank = tmp / "bank_door.db"
    world.seed_bank(bank)
    world.issue_code(bank, "dana", "s", NOW, MAX_VERIFICATION_ATTEMPTS)
    code = re.search(r"\b(\d{6})\b", world.outbound_messages(bank)[-1]["body"]).group(1)
    wrong = "".join(str((int(d) + 1) % 10) for d in code)
    failures = lambda: world.failed_verifications(bank, "dana", NOW)
    open_codes = lambda: sum(c["user_id"] == "dana" and c["status"] == "open" for c in world.list_challenges(bank))
    door = lambda session, text: world.take_code_entry(bank, "dana", session, text, NOW, MAX_VERIFICATION_ATTEMPTS)
    numbers = [f"{(int(code) * 7919 + i * 104729) % 10 ** 6:06d}" for i in range(1, 300)]
    pasted = "\n".join(f"PL-{n}" for n in numbers[:150] + [code] + numbers[150:])
    chatter = "It hasn't arrived. Is it going to the number ending 0100? I'm in 94"

    def pasted_elsewhere():
        taken = door("notes", pasted)
        shown = set(re.findall(r"PL-(\S+)", taken["text"]))
        return len(shown) == 1 and code not in taken["text"] and failures() == 0 and open_codes() == 1, json.dumps(
            {"distinct renderings of the 300 references": len(shown), "failures": failures(), "open codes": open_codes()})

    def pasted_in_the_waiting_chat():
        taken = door("s", pasted)
        return (taken["entry"] or {}).get("outcome") == "several_numbers" and failures() == 0 and open_codes() == 1, json.dumps(taken["entry"])

    def not_an_entry():
        taken = door("s", chatter)
        return taken["text"] == chatter and (taken["entry"] or {}).get("outcome") == "no_code_entered" and failures() == 0, json.dumps(taken)

    def one_wrong_entry():
        taken = door("s", f"{wrong[:3]} {wrong[3:]}")
        return failures() == 1 and wrong[:3] not in taken["text"], json.dumps(taken)

    def as_the_phone_shows_it():
        taken = door("s", f"ok it says {code[:3]}-{code[3:]}")
        return (taken["entry"] or {}).get("outcome") == "matched" and not re.search(r"\d", taken["text"]), json.dumps(taken)

    def typed_again_when_dead():
        taken = door("s", f"here it is once more: {code}")
        return code not in taken["text"], taken["text"]

    def no_code_open():
        taken = world.take_code_entry(bank, "marco", "m", "my order number is 482913", NOW, MAX_VERIFICATION_ATTEMPTS)
        return taken["text"] == "my order number is 482913" and taken["entry"] is None, json.dumps(taken)

    def after_the_code_expired():
        # eli's code was sent and never typed: ten minutes later it is still marked open, and cannot be entered
        from cardcare.clock import add_minutes
        world.issue_code(bank, "eli", "e1", NOW, MAX_VERIFICATION_ATTEMPTS)
        expired = re.search(r"\b(\d{6})\b", world.outbound_messages(bank)[-1]["body"]).group(1)
        other = "482913" if expired != "482913" else "482914"
        later = add_minutes(NOW, 10)
        taken = world.take_code_entry(bank, "eli", "e2", f"my order number is {other}, and that old code was {expired}", later, MAX_VERIFICATION_ATTEMPTS)
        return other in taken["text"] and expired not in taken["text"] and taken["entry"] is None, json.dumps(taken).replace(expired, "<the expired code>")

    def a_form_the_bank_does_not_take():
        # marco's code written with a comma, then a new one as four digits and two in another chat: neither is an entry,
        # neither is kept, each costs that code and no attempt
        from cardcare.clock import add_minutes
        results = []
        for minute, session, form in ((0, "m1", lambda c: f"{c[:3]},{c[3:]}"), (2, "m-notes", lambda c: f"it says {c[:4]} {c[4:]}")):
            world.issue_code(bank, "marco", "m1", add_minutes(NOW, minute), MAX_VERIFICATION_ATTEMPTS)
            sent = re.search(r"\b(\d{6})\b", world.outbound_messages(bank)[-1]["body"]).group(1)
            taken = world.take_code_entry(bank, "marco", session, form(sent), add_minutes(NOW, minute + 1), MAX_VERIFICATION_ATTEMPTS)
            results.append(not re.search(r"\d", taken["text"]) and (taken["entry"] or {}).get("outcome") == "written_unusably")
        statuses = [c["status"] for c in world.list_challenges(bank) if c["user_id"] == "marco"]
        return all(results) and statuses == ["cancelled", "cancelled"] and world.failed_verifications(bank, "marco", NOW) == 0, json.dumps(
            {"removed and reported": results, "codes": statuses, "failures": world.failed_verifications(bank, "marco", NOW)})

    def other_numbers_are_not_codes():
        text = "I paid $1,234.56 on 2026-11-13 at 10:02:00 and I have 123,456 points"
        world.issue_code(bank, "priya", "p1", NOW, MAX_VERIFICATION_ATTEMPTS)
        taken = world.take_code_entry(bank, "priya", "p1", text, NOW, MAX_VERIFICATION_ATTEMPTS)
        still_open = sum(c["user_id"] == "priya" and c["status"] == "open" for c in world.list_challenges(bank))
        return taken["text"] == text and (taken["entry"] or {}).get("outcome") == "no_code_entered" and still_open == 1, json.dumps(taken)

    def no_code_starts_with_zero():
        from cardcare.clock import add_days
        firsts = set()
        for day in range(40):  # five a day is the cap: forty days of sends for one account
            for send in range(5):
                at = add_days(NOW, day + 2)[:11] + f"{10 + send}:00:00Z"
                world.issue_code(bank, "eli", f"z{day}", at, MAX_VERIFICATION_ATTEMPTS)
                firsts.add(re.search(r"\b(\d{6})\b", world.outbound_messages(bank)[-1]["body"]).group(1)[0])
        return "0" not in firsts and len(firsts) > 5, json.dumps(sorted(firsts))

    def waits_only_for_a_code_not_yet_answered():
        from cardcare.clock import add_minutes
        world.issue_code(bank, "dana", "w1", add_minutes(NOW, 30), MAX_VERIFICATION_ATTEMPTS)
        waits = lambda entry, at: world.waits_for_an_entry(bank, "dana", "w1", entry, at)
        facts = {"sent this turn, the message was read before it": waits({"outcome": "mismatch"}, add_minutes(NOW, 30)),
                 "sent earlier, the message held no code": waits({"outcome": "no_code_entered"}, add_minutes(NOW, 31)),
                 "sent earlier, the message was a wrong entry": waits({"outcome": "mismatch"}, add_minutes(NOW, 31)),
                 "another conversation": world.waits_for_an_entry(bank, "dana", "w2", None, add_minutes(NOW, 31))}
        return list(facts.values()) == [True, True, False, False], json.dumps(facts)

    rows = [_row("r5 2.1 300 references pasted in another chat all read the same afterwards; no attempt is counted; the code stays open", pasted_elsewhere),
            _row("r5 2.1 many numbers in the chat that waits: nothing is compared, nothing counted", pasted_in_the_waiting_chat),
            _row("r5 nb5 a message whose digits total six is not a guess", not_an_entry),
            _row("r5 a single wrong entry is one failed attempt, and its digits are not kept", one_wrong_entry),
            _row("r5 2.2 the code typed as a phone shows it ('ok it says NNN-NNN') is accepted and nothing of it is kept", as_the_phone_shows_it),
            _row("r5 a code typed again after it was used is removed too (the customer's own dead code)", typed_again_when_dead),
            _row("r5 with no code open, six digits are just six digits", no_code_open),
            _row("r5 ten minutes after a code was sent and never typed, an order number in another chat is kept; the expired code itself is not",
                 after_the_code_expired),
            _row("r6 a code written with a comma, or as four digits and two, is not an entry and not kept: it is removed and that code cancelled",
                 a_form_the_bank_does_not_take),
            _row("r6 an amount, a date, a clock time and a points balance are not codes: kept as typed, the code stays open", other_numbers_are_not_codes),
            _row("r6 the wait is for a code this turn's message did not answer", waits_only_for_a_code_not_yet_answered),
            _row("r6 no code starts with a zero (200 sends)", no_code_starts_with_zero)]
    for form in ("123456", "123 456", "123-456", "123.456", "12 34 56", "1 2 3 4 5 6", "one two three four five six"):
        rows.append(_row(f"r5 2.2 the entry grammar reads {form!r} as one code",
                         lambda form=form: ([d for _, _, d in world.code_spans(f"ok it says {form} now")] == ["123456"], json.dumps(world.code_spans(f"ok it says {form} now")))))
    for text in ("ending 0100? I'm in 94", "card 5555 5555 5555 4444", "call +1 415 555 0100", "it was 1,234,567"):
        rows.append(_row(f"r5 nb5 the entry grammar finds no code in {text!r}", lambda text=text: (world.code_spans(text) == [], json.dumps(world.code_spans(text)))))
    return rows


def check_r5_code_limits(tmp: Path) -> list[tuple[str, bool, str]]:
    """nb 4 and nb 6: the third wrong entry says the account is locked; at most MAX_CODES_PER_DAY codes per account per day."""
    from cardcare import memory_policy
    from cardcare.clock import add_minutes
    bank = tmp / "bank_limits.db"
    world.seed_bank(bank)
    cap = getattr(memory_policy, "MAX_CODES_PER_DAY", 5)  # the contract's number, also where the constant does not exist yet
    sent = [world.issue_code(bank, "eli", "s", add_minutes(NOW, 2 * i), MAX_VERIFICATION_ATTEMPTS) for i in range(cap + 1)]
    messages = sum(m["user_id"] == "eli" and m.get("purpose") == "one_time_code" for m in world.outbound_messages(bank))
    rows = [("r5 nb6 the sixth code in a day is refused and no message is sent", messages == cap and "24 hours" in str(sent[-1].get("error")),
             json.dumps({"code messages": messages, "sixth send": sent[-1]})),
            ("r5 nb6 a refused send is not a failed attempt", world.failed_verifications(bank, "eli", add_minutes(NOW, 20)) == 0, "")]
    world.issue_code(bank, "priya", "p", NOW, MAX_VERIFICATION_ATTEMPTS)
    results = [world.attempt_code(bank, "priya", "000001", NOW, MAX_VERIFICATION_ATTEMPTS, session_id="p") for _ in range(3)]
    rows.append(("r5 nb4 the third wrong entry says the account is now locked", results[-1].get("account_locked") is True
                 and not results[0].get("account_locked"), json.dumps(results[-1])))
    return rows


def check_r5_small(tmp: Path) -> list[tuple[str, bool, str]]:
    """nb 3 (the scanner reads numbers), nb 7 (the wait as the reflection reads it), nb 14 (a second reminder names the first)."""
    import sqlite3

    import ormsgpack
    from cardcare import desk, episodes
    path = tmp / "lg_numbers.db"
    with sqlite3.connect(path) as conn:
        conn.execute("CREATE TABLE writes (channel TEXT, value BLOB)")
        conn.execute("INSERT INTO writes VALUES ('messages', ?)", (ormsgpack.packb({"name": "confirm_verification_code", "args": {"entered": 517391}, "id": "call_1"}),))
    waiting = [{"role": "customer", "text": "Change my contact channel to email."},
               {"role": "tool", "text": "called confirm_verification_code({})"},
               {"role": "tool", "text": 'confirm_verification_code -> {"error": "This tool call requires confirmation, please approve or reject."}'}]
    sched = tmp / "sched_names.db"
    scheduler.create_scheduler(sched)
    first = desk.schedule_customer_reminder(sched, "eli", "call FitPulse", "2026-11-25", "09:00", "America/Chicago", NOW)
    second = desk.schedule_customer_reminder(sched, "eli", "call CloudNest", "2026-11-25", "18:00", "America/Chicago", NOW)
    rendered = episodes.format_transcript(waiting)
    def code_search(stored_value, code: str):
        import run_scenario
        store = tmp / f"lg_code_{code}.db"
        with sqlite3.connect(store) as conn:
            conn.execute("CREATE TABLE writes (channel TEXT, value BLOB)")
            conn.execute("INSERT INTO writes VALUES ('__resume__', ?)", (ormsgpack.packb(stored_value),))
        held = run_scenario.stores_holding_a_code([store], [code])
        return bool(held), json.dumps(held)

    def counts_are_not_card_data():
        store = tmp / "lg_counts.db"
        with sqlite3.connect(store) as conn:
            conn.execute("CREATE TABLE writes (channel TEXT, value BLOB)")
            conn.execute("INSERT INTO writes VALUES ('messages', ?)", (ormsgpack.packb({"usage_metadata": {"output_tokens": 123, "cached": 12, "reasoning": 29}}),))
        left = store_audit.secrets_left(store_audit.store_text(store), {"pans": [], "codes": ["123"], "expiries": ["12/29"]})
        return left == [], json.dumps(left)

    return [_row("r5 2.2 the stored-code search finds a code kept with a space ('481 975')", lambda: code_search("481 975", "481975")),
            _row("r5 2.2 the stored-code search finds a code kept in a sentence with a dash", lambda: code_search("ok it says 447-526", "447526")),
            _row("r5 nb3 the stored-code search finds a code kept as a number", lambda: code_search({"args": {"entered": 517391}}, "517391")),
            _row("r5 the stored-code search does not take a clock time for a code", lambda: (not code_search("sent at 2026-11-13T10:02:00Z", "100200")[0], "")),
            _row("r5 nb3 the stored-code search finds a code that lost its leading zero when kept as a number",
                 lambda: code_search({"args": {"entered": 48213}}, "048213")),
            ("r5 nb3 the scanner reads a number stored as a number (a code passed as a msgpack integer)",
             '"number": 517391' in store_audit.store_text(path).split("\n"), ""),
            _row("r5 the scanner takes no stored count for a security code or an expiry (token counts of 123, 12 and 29)", counts_are_not_card_data),
            ("r5 nb7 the reflection reads the wait for the code as a wait, not as an error", "requires confirmation" not in rendered
             and "waiting for the customer" in rendered, rendered[-200:]),
            ("r5 nb14 a second reminder for the same local day is refused and the refusal names the existing one",
             "error" in second and first.get("followup_id", "?") in json.dumps(second) and "09:00" in json.dumps(second), json.dumps(second))]


def check_reasoning_last4() -> list[tuple[str, bool, str]]:
    # the review's case sat in the reasoning of a turn whose message carried card data, so the code rule was armed
    text = "The customer gave card last4 8830 and ZIP 10011; the card number in their message was masked. I will verify."
    masked = masking.mask_customer_text(text, ("Marco here, card ending 8830, ZIP 10011. CVV: 737 [REDACTED CARD NUMBER], exp 12/29.",))
    return [("nb5 the reasoning masker leaves 'card last4 8830' alone next to card data", masked == text, masked)]


def check_reply_two_numbers() -> list[tuple[str, bool, str]]:
    reply = "You gave 5555 5555 5555 4444, 4111 1111 1111 1111."
    masked = masking.mask_card_numbers(reply)
    left = store_audit.secrets_left(masked, {"pans": PANS, "codes": [], "expiries": []})
    return [("nb6 two comma-joined numbers in a reply are both masked", not left, masked)]


def check_empty_reflection() -> list[tuple[str, bool, str]]:
    rows = []
    for raw in ['{"summary": "", "lesson": ""}', "", '{"summary": "   "}']:
        parsed = episodes.parse_reflection(raw, "priya", set())
        rows.append((f"nb2 an empty reflection {raw!r} is not an episode", parsed is None, json.dumps(parsed)))
    good = episodes.parse_reflection('{"summary": "Customer asked about a CloudNest charge; no case filed.", "lesson": "none"}', "priya", set())
    rows.append(("nb2 a real reflection still parses", bool(good) and good["summary"].startswith("Customer asked"), json.dumps(good)))
    return rows


def check_stale_tab(tmp: Path) -> list[tuple[str, bool, str]]:
    db = tmp / "privacy.db"
    privacy.create_ledger(db)
    privacy.register_session(db, "priya", "tab-a", "live", "2026-11-09T10:00:00Z")
    privacy.register_session(db, "priya", "tab-b", "live", "2026-11-09T10:02:00Z")
    privacy.begin_erasure(db, "priya", "tab-b", "2026-11-09T10:02:30Z")
    # tab A's next turn registers again, as every turn does
    generation = privacy.register_session(db, "priya", "tab-a", "live", "2026-11-09T10:05:00Z")
    current = privacy.session_is_current(db, "priya", "tab-a")
    fresh = privacy.register_session(db, "priya", "tab-c", "live", "2026-11-09T10:06:00Z")
    return [("2.2a tab A, registered before tab B's erasure, is not re-registered into the new generation at its next turn",
             generation == 0 and not current, json.dumps({"tab_a_generation": generation, "tab_a_current": current})),
            ("2.2a a session started after the erasure is current", fresh == 1 and privacy.session_is_current(db, "priya", "tab-c"),
             json.dumps({"tab_c_generation": fresh}))]


def check_lock_applies_to_actions(tmp: Path) -> list[tuple[str, bool, str]]:
    bank = tmp / "bank.db"
    world.seed_bank(bank)
    for _ in range(MAX_VERIFICATION_ATTEMPTS):
        world.record_verification(bank, "eli", False, NOW)
    locked = getattr(world, "verification_locked", None)
    state = locked(bank, "eli", NOW) if locked else "world.verification_locked does not exist"
    return [("nb3 a locked account is locked for every verified action (world.verification_locked), not only for new guesses",
             state is True, json.dumps(state))]


def check_scheduler_backoff(tmp: Path) -> list[tuple[str, bool, str]]:
    sched, bank = tmp / "scheduler.db", tmp / "bank2.db"
    world.seed_bank(bank)
    scheduler.create_scheduler(sched)
    record = scheduler.schedule_followup(sched, "priya", "customer_reminder", "2026-11-20T09:00:00Z", {"note": "book the transfer"}, "none",
                                         "2026-11-09T10:00:00Z")
    failed_calls = []

    def provider_down(_record, _now):
        raise RuntimeError("InternalServerError: simulated outage")

    def on_failed(rec, now):
        failed_calls.append((rec["followup_id"], now))

    rows = []
    try:
        outcomes = [asyncio.run(scheduler.fire_due_followups(sched, bank, at, provider_down, on_failed=on_failed))
                    for at in ("2026-11-20T09:05:00Z", "2026-11-20T09:10:00Z", "2026-11-20T09:20:00Z")]
        after_three = scheduler.get_followup(sched, record["followup_id"])
        rows.append(("nb1 three failed fires in fifteen minutes leave the reminder pending (with a back-off), not failed",
                     after_three["status"] == "pending" and bool(after_three.get("not_before")),
                     json.dumps({"status": after_three["status"], "attempts": after_three["attempts"], "not_before": after_three.get("not_before"),
                                 "outcomes": [o[0]["outcome"] if o else "nothing due" for o in outcomes]})))
        ticks = ["2026-11-20T10:30:00Z", "2026-11-20T12:00:00Z", "2026-11-20T15:00:00Z", "2026-11-20T21:00:00Z", "2026-11-21T09:00:00Z",
                 "2026-11-21T21:00:00Z", "2026-11-22T09:00:00Z", "2026-11-22T21:00:00Z"]
        for at in ticks:
            asyncio.run(scheduler.fire_due_followups(sched, bank, at, provider_down, on_failed=on_failed))
        final = scheduler.get_followup(sched, record["followup_id"])
        rows.append(("nb1 a two-day outage ends the reminder, and whoever is told is told exactly once (on_failed)",
                     final["status"] == "failed" and len(failed_calls) == 1 and final["resume"] == {},
                     json.dumps({"status": final["status"], "attempts": final["attempts"], "on_failed_calls": failed_calls, "resume": final["resume"]})))
    except TypeError as exc:  # the round-4 scheduler has no on_failed and no back-off
        rows.append(("nb1 three failed fires in fifteen minutes leave the reminder pending (with a back-off), not failed", False, f"{exc}"))
        rows.append(("nb1 a two-day outage ends the reminder, and whoever is told is told exactly once (on_failed)", False, f"{exc}"))
    return rows


def check_retract_two_names(tmp: Path) -> list[tuple[str, bool, str]]:
    var = tmp / "var"
    var.mkdir()
    candidate = {"resolution_code": "NO_CANCELLATION_PROOF", "users": ["marco", "priya"], "decisions": ["D-1", "D-2"],
                 "episodes": ["E-a", "E-b"], "lessons": [], "notes": []}
    rule = "Ask whether the customer has the merchant's cancellation confirmation, and file either way."
    procedures.promote(var, candidate, rule, rule, scenario.APPROVERS, NOW)
    command = [sys.executable, str(CODE_DIR / "review.py"), "retract", "--framework", "adk", "--var-dir", str(var), "--to", "v1",
               "--by", scenario.APPROVERS[0], "--by", scenario.APPROVERS[1], "--reason", "drill", "--now", NOW]
    run = subprocess.run(command, capture_output=True, text=True, cwd=CODE_DIR)
    registry = procedures.load_registry(var)
    retracted = registry["versions"].get("v2", {}).get("retracted") or {}
    by = retracted.get("by")
    names_kept = by == scenario.APPROVERS or (isinstance(by, str) and all(n in by for n in scenario.APPROVERS))
    return [("nb4 `review.py retract --by A --by B` with two registry reviewers is accepted and records both names",
             run.returncode == 0 and registry["active"] == "v1" and names_kept,
             json.dumps({"exit": run.returncode, "active": registry["active"], "retracted_by": by, "stderr": run.stderr.strip()[-200:]}))]


def check_repeats_after_lost_result(tmp: Path) -> list[tuple[str, bool, str]]:
    """The captain's question (012): a write tool called again after its result was lost to a crash. Each repeat must
    be recognised: the same wrong guess counts once; the consumed code re-entered by the same conversation is the
    same proof; a note is attached once; a filing whose follow-up the crash skipped is completed, not refused."""
    from cardcare import desk
    bank, sched = tmp / "bank3.db", tmp / "scheduler3.db"
    world.seed_bank(bank)
    scheduler.create_scheduler(sched)
    rows = []
    try:
        first = world.attempt_verification(bank, "priya", "1234", "94107", NOW, MAX_VERIFICATION_ATTEMPTS, session_id="s1")
        again = world.attempt_verification(bank, "priya", "1234", "94107", "2026-11-20T09:01:00Z", MAX_VERIFICATION_ATTEMPTS, session_id="s1",
                                           repeat_of_lost_call=True)
        failures = world.failed_verifications(bank, "priya", "2026-11-20T09:01:00Z")
        rows.append(("012 after a lost result, the same wrong guess repeated in the same conversation within two minutes counts once",
                     first["outcome"] == "mismatch" and again["outcome"] == "mismatch" and again.get("repeat") is True and failures == 1,
                     json.dumps({"first": first, "again": again, "failures": failures})))
        other = world.attempt_verification(bank, "priya", "1234", "94107", "2026-11-20T09:01:30Z", MAX_VERIFICATION_ATTEMPTS, session_id="s2",
                                           repeat_of_lost_call=True)
        rows.append(("012 the same guess from another conversation is a new attempt", other.get("repeat") is None and other["failures"] == 2,
                     json.dumps(other)))
    except TypeError as exc:
        rows += [("012 after a lost result, the same wrong guess repeated in the same conversation within two minutes counts once", False, str(exc)),
                 ("012 the same guess from another conversation is a new attempt", False, str(exc))]

    def retype(at: str) -> dict:  # the round-4 signature has no session_id: the property is asked of whichever code is under test
        try:
            return world.attempt_verification(bank, "marco", "1234", "10011", at, MAX_VERIFICATION_ATTEMPTS, session_id="s5")
        except TypeError:
            return world.attempt_verification(bank, "marco", "1234", "10011", at, MAX_VERIFICATION_ATTEMPTS)

    retype(NOW)
    retyped = retype("2026-11-20T09:00:30Z")
    rows.append(("012 with no lost result, the same wrong guess typed again is a second attempt (a customer's retype is not excused)",
                 retyped.get("repeat") is None and retyped["failures"] == 2, json.dumps(retyped)))
    try:
        sent = world.issue_code(bank, "eli", "s3", NOW, MAX_VERIFICATION_ATTEMPTS)
        code = next(m for m in reversed(world.outbound_messages(bank)) if m["user_id"] == "eli")["body"].split("is ")[1][:6]
        hit = world.attempt_code(bank, "eli", code, "2026-11-20T09:00:30Z", MAX_VERIFICATION_ATTEMPTS, session_id="s3")
        plain = world.attempt_code(bank, "eli", code, "2026-11-20T09:00:45Z", MAX_VERIFICATION_ATTEMPTS, session_id="s3")
        replay = world.attempt_code(bank, "eli", code, "2026-11-20T09:01:00Z", MAX_VERIFICATION_ATTEMPTS, session_id="s3", repeat_of_lost_call=True)
        elsewhere = world.attempt_code(bank, "eli", code, "2026-11-20T09:01:30Z", MAX_VERIFICATION_ATTEMPTS, session_id="s4", repeat_of_lost_call=True)
        rows.append(("012 after a lost result, the code this conversation consumed matches again without a new row; from another "
                     "conversation, or with no lost result, a consumed code is spent",
                     hit["outcome"] == "matched" and replay.get("repeat") is True and replay["outcome"] == "matched"
                     and elsewhere["outcome"] != "matched" and plain["outcome"] != "matched",
                     json.dumps({"hit": hit["outcome"], "no_lost_result": plain["outcome"], "replay": replay, "elsewhere": elsewhere["outcome"],
                                 "sent": sent.get("sent")})))
    except (TypeError, AttributeError) as exc:
        rows.append(("012 after a lost result, the code this conversation consumed matches again without a new row; from another "
                     "conversation, or with no lost result, a consumed code is spent", False, f"{type(exc).__name__}: {exc}"))
    filed = desk.file_dispute_with_followup(bank, sched, "priya", "T-1002", "cancelled_subscription", None, NOW, 10, 20000)
    case_id = filed.get("case_id")
    once = world.add_case_evidence(bank, "priya", case_id, "cancellation reference CN-77812", NOW)
    twice = world.add_case_evidence(bank, "priya", case_id, "cancellation reference CN-77812", NOW)
    lines = [line for line in (twice.get("evidence_note") or "").split("\n") if "CN-77812" in line]
    rows.append(("012 the same evidence note attached again is attached once", len(lines) == 1 and twice.get("already_attached") is True,
                 json.dumps({"lines": lines, "second": {k: twice.get(k) for k in ("already_attached", "error")}})))
    # a filing whose follow-up the crash skipped: the case exists, no follow-up record; the repeated filing completes it
    case, created = world.open_case(bank, "marco", "T-2002", "cancelled_subscription", None, NOW)
    repeated = desk.file_dispute_with_followup(bank, sched, "marco", "T-2002", "cancelled_subscription", None, NOW, 10, 20000)
    followups = [f for f in scheduler.user_followups(sched, "marco") if f["action"] == "case_status_followup"]
    rows.append(("012 a repeated filing after a crash between opening the case and scheduling its follow-up completes the follow-up",
                 created and "error" not in repeated and len(followups) == 1 and repeated.get("case_id") == case["case_id"],
                 json.dumps({"repeated": {k: repeated.get(k) for k in ("case_id", "error", "note")}, "followups": len(followups)})))
    return rows


def check_claim_pairing() -> list[tuple[str, bool, str]]:
    """An honest agent over a store that leaked the card number: it said the expiry (a [REDACTED EXPIRY] token) was removed,
    which is true, and said the card number is kept in the transcript. The paired check must not fail it."""
    spec = {"kind": "storage_claim_consistent", "id": "claim", "turn": None}
    honest = {"judgements": {"claim": {"verdict": "pass", "reason": "it said the expiry was removed", "items": ["expiry"]}},
              "card_data_hits": {"card number 5555…4444": ["adk_sessions.db"]}}
    passed, evidence = scenario.evaluate(spec, honest, {})
    dishonest = {"judgements": {"claim": {"verdict": "pass", "reason": "it said the card number was not stored", "items": ["card number"]}},
                 "card_data_hits": {"card number 5555…4444": ["adk_sessions.db"]}}
    caught, evidence2 = scenario.evaluate(spec, dishonest, {})
    return [("nb8 a true 'the expiry was removed' over a store that leaked the card number is consistent", passed, evidence),
            ("nb8 a false 'the card number was not stored' over that store is still caught", not caught, evidence2)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=CODE_DIR / "evidence" / "offline-checks.md")
    args = parser.parse_args()
    rows: list[tuple[str, bool, str]] = []
    with tempfile.TemporaryDirectory() as tmp_name:
        tmp = Path(tmp_name)
        without_files = (check_masker_leaks, check_reasoning_last4, check_reply_two_numbers, check_empty_reflection, check_claim_pairing,
                         check_code_said_twice, check_sweep_shapes, check_reply_that_repeats_a_code, check_r5_masker)
        with_files = (check_stale_tab, check_lock_applies_to_actions, check_scheduler_backoff, check_retract_two_names,
                      check_repeats_after_lost_result, check_scanner_reads_msgpack_stores, check_decided_case_says_what_can_be_done,
                      check_r5_code_door, check_r5_code_limits, check_r5_small)
        for fn in (*without_files, *with_files):
            try:
                rows += fn(tmp) if fn in with_files else fn()
            except Exception as exc:  # a missing function on old code is a failed check, not a crash
                rows.append((fn.__name__, False, f"{type(exc).__name__}: {exc}"))
    passed = sum(ok for _, ok, _ in rows)
    lines = [f"# Offline checks: {passed}/{len(rows)} passed", "", "`python offline_checks.py`, run from the code directory; no model call.", "",
             "| | check | evidence |", "|---|---|---|"]
    lines += [f"| {'PASS' if ok else '**FAIL**'} | {label.replace('|', '\\|')} | `{evidence[:300].replace('|', '\\|').replace(chr(10), ' ')}` |"
              for label, ok, evidence in rows]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0 if passed == len(rows) else 1


if __name__ == "__main__":
    sys.exit(main())
