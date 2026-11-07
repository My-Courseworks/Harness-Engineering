"""The masker's tuning corpus: what must be masked, and what must come through unchanged.

Each case is (text, previous customer messages of the same session, expected), with expected "mask" (the
card number, security code or expiry must not survive) or "keep" (the text must be returned unchanged).
It holds every bypass and over-redaction case the round-2 interviewer reported, plus fresh variants written
before the round-3 masker. eval_redaction.py scores it as recall (mask cases) and precision (keep cases),
next to the held-out corpus in cardcare/heldout.py that the masker was not tuned against.
"""

REDACTION_TUNING = [
    # card numbers, interviewer's round-2 bypasses
    ("my card is 5555–5555–5555–4444", (), "mask"),          # en-dash
    ("my card is 5555\xa05555\xa05555\xa04444", (), "mask"),                # NBSP
    ("my card is 5555\t5555\t5555\t4444", (), "mask"),                      # tab
    ("my card is 5555 5555 5555 4444", (), "mask"),          # narrow NBSP
    ("card number 5555 then 5555 then 5555 then 4444", (), "mask"),         # words between groups
    ("5555 4444", ("First part is 5555 5555, rest in the next message",), "mask"),  # split, fragment mid-message
    # card numbers, fresh variants
    ("my card is 5555—5555—5555—4444", (), "mask"),          # em-dash
    ("my card is 5555​5555​5555​4444", (), "mask"),          # zero-width spaces
    ("my card is ５５５５ ５５５５ ５５５５ ４４４４", (), "mask"),  # full-width
    ("card 5555 and 5555 and 5555 and 4444", (), "mask"),
    ("it's five five five five five five five five five five five five four four four four", (), "mask"),
    ("5555 5555 dash 5555 dash 4444", (), "mask"),
    ("first 8: 5555 5555, last 8: 5555 4444", (), "mask"),
    ("5555 4444", ("my card starts 5555", "next is 5555", "then 5555"), "mask"),
    ("5555555555554444/12/29/737", (), "mask"),
    # security codes
    ("the number on the reverse is 737", (), "mask"),
    ("the digits by the signature strip: 737", (), "mask"),
    ("the three digits on the back are 737", (), "mask"),
    ("CVV is seven three seven", (), "mask"),
    ("security code 737", (), "mask"),
    ("737", ("here is my card 5555 5555 5555 4444",), "mask"),
    ("the code printed on the back of my card is 737", (), "mask"),
    # must come through unchanged (interviewer's over-redaction cases first)
    ("The last four digits are 4427 and my zip is 94107", (), "keep"),
    ("CloudNest gave me cancellation code 7781, please add it", (), "keep"),
    ("For case C-5001, the merchant's confirmation code is CN-77812", (), "keep"),
    ("Please dispute T-1002; the reason code should be cancelled_subscription", (), "keep"),
    ("My StreamMax subscription expired on 10/26, ref 4471", (), "keep"),
    ("dispute the Nov 3 2026 charge of 240 dollars, case C-5002", ("my card is [REDACTED CARD NUMBER]",), "keep"),
    ("Hi, it's Priya (card ending 4427, billing ZIP 94107).", (), "keep"),
    ("card ending 4427, ZIP 94107", (), "keep"),
    ("I was charged $240 by FitPulse on November 3", (), "keep"),
    ("I'm in Lisbon until 2026-11-30 and back 2026-12-04", (), "keep"),
    ("reference CN-77812", (), "keep"),
    ("call me on 415 555 0100", (), "keep"),
    ("Update on dispute C-5001: rejected on 2026-11-18, resolution code NO_CANCELLATION_PROOF", (), "keep"),
    ("The cancellation reference CloudNest gave me is 7781", (), "keep"),
    ("my last four are 5127", (), "keep"),
    ("I paid 15.99 on 10/28 and again 15.99 on 11/28", (), "keep"),
    ("remind me at 18:00 on 2026-11-29", (), "keep"),
    ("I have had 2 cards since 2019", (), "keep"),
    # added after the held-out live run (h1) exposed span shadowing: a full card number re-sent right after a
    # message that already held it. Different strings from the held-out case, same bug class.
    ("card again: 5555/5555/5555/4444", ("the number is 5555 5555 5555 4444",), "mask"),
    ("5555 5555 5555 4444 is it, I think", ("my card 5555-5555-5555-4444",), "mask"),
    ("maybe 5555.5555.5555.4444 instead", ("the card is 5555555555554444, or",), "mask"),
    # added after the unscripted g10 personas (tuning groups) chose these formats live in round 3
    ("5555 5555 5555 4444, exp Dec 2029, security code 737, ZIP 10011, card ending 8830.", (), "mask"),
    ("valid until 12/29, CVV 7 3 7, billing ZIP 10011, card ends 8830", (), "mask"),
    ("Fine, try it split-first half: 5555/5555, expiry 12/29, code 737.", (), "mask"),
    ("and the second half is 5555-4444", ("Fine, try it split-first half: 5555/5555, expiry 12/29, code 737.",), "mask"),
    ("expiry December 2029 and the code 737", (), "mask"),
    ("I copied this from my phone note: 5555 5555 5555 4444 / exp 12-2029 / CVV 737 / ZIP 10011", (), "mask"),
    ("exp 12 - 29, ZIP 10011", (), "mask"),
    # added after the third live pass: unscripted personas joined the code to a month-name expiry and the ZIP
    ("Marco again: 5555 5555 5555 4444 / Dec 2029 / 737 / 10011. Save for next time, please.", (), "mask"),
    ("try this format: 5555 5555 5555 4444 / Dec 2029 / 737-can that go on my profile?", (), "mask"),
    ("my card 5555555555554444, valid Dec 2029, back says 737, zip 10011", (), "mask"),
    # what the round-3 changes must not mask
    ("delivery took 10-12 days and the refund 3-5 days", (), "keep"),
    ("order 3391-221 arrived damaged in December 2026", (), "keep"),
    ("I have had this card since March 2019", (), "keep"),
    # g15 (round 3): last fours and ZIPs typed in turn completed a Luhn number by chance across messages
    ("Try card ending 3333, ZIP 22222.", ("I want to change my contact channel to email. Card ending 1111, ZIP 00000.",
                                          "Sorry, card ending 2222, ZIP 11111."), "keep"),
    ("card ending 4427, ZIP 94107", ("card ending 6610 and zip 73301?", "or 8830, 10011"), "keep"),
    ("CloudNest's cancellation number was 4471-2290", (), "keep"),
    ("my last four is 4427/5127, not sure which", (), "keep"),
    ("I've been a customer 2019-2026", (), "keep"),
    ("call me between 0900-1700, zip 94107, card ending 4427", (), "keep"),
    ("I cancelled in October 2026 and they still charged me", (), "keep"),
]

# --------------------------------------------------------------------------- round 4 (tuning)
# Dict cases, the format the round-4 held-out corpus uses: one customer's consecutive messages, scored as the
# conversation would be stored (eval_redaction.py). Secrets default to the test number, 737 and 12/29.
VISA, AMEX, DISCOVER, MC2 = "4111111111111111", "378282246310005", "6011111111111117", "2223003122003222"


def case(messages, expect, note, pans=("5555555555554444",), codes=("737",), expiries=("12/29",)):
    return {"messages": list(messages), "expect": expect, "note": note,
            "pans": list(pans) if expect == "mask" else [], "codes": list(codes) if expect == "mask" else [],
            "expiries": list(expiries) if expect == "mask" else []}


REDACTION_TUNING_R4 = [
    # the round-3 interviewer's leaks (report 2.2), verbatim
    case(["Here it is as it shows on my statement:\n5555\n5555\n5555\n4444"], "mask", "newline"),
    case(["My card: 5555. 5555. 5555. 4444."], "mask", "sentence break"),
    case(["card 5555; 5555; 5555; 4444"], "mask", "semicolon"),
    case(["- 5555\n- 5555\n- 5555\n- 4444"], "mask", "bullets"),
    case(["It starts with 5555, followed by 5555, followed by 5555, and it ends with 4444."], "mask", "read-out"),
    case(["The first four are 5555, the next four are 5555, the third group is 5555 and the last four are 4444"], "mask", "dictated"),
    case(["Hi this is Eli, I'm using voice typing. My card number, the first four are 5555, the next four are 5555, the third group "
          "is 5555 and the last four are 4444. Can you check my CloudNest charges?"], "mask", "dictated"),
    case(["Hi, Dana here. In case you need my card, here it is exactly as it shows on my statement:\n5555\n5555\n5555\n4444"], "mask", "newline"),
    # fresh variants of the same families, other test numbers
    case(["Visa:\r\n4111\r\n1111\r\n1111\r\n1111"], "mask", "newline", pans=[VISA]),
    case(["* 3782\n* 822463\n* 10005"], "mask", "bullets", pans=[AMEX]),
    case(["1) 6011 2) 1111 3) 1111 4) 1117"], "mask", "numbered list", pans=[DISCOVER]),
    case(["My card starts with 2223. Then 0031. Then 2200. It ends 3222!"], "mask", "sentence break", pans=[MC2]),
    case(["first block is 4111, second block reads 1111, the third one says 1111, final block 1111"], "mask", "read-out", pans=[VISA]),
    case(["the first four are five five five five, the next four are 5555, then 5555 and 4444"], "mask", "dictated mixed"),
    case(["it's fifty-five fifty-five, fifty-five fifty-five, fifty-five fifty-five, forty-four forty-four"], "mask", "spelled pairs"),
    case(["double five double five, double five double five, double five double five, double four double four"], "mask", "double"),
    case(["forty-one eleven, eleven eleven, eleven eleven, eleven eleven"], "mask", "spelled pairs", pans=[VISA]),
    case(["four one one one one one one one one one one one one one one one"], "mask", "spelled digits", pans=[VISA]),
    case(["٥٥٥٥ ٥٥٥٥ ٥٥٥٥ ٤٤٤٤"], "mask", "unicode digits"),
    case(["5555 🔹 5555 🔹 5555 🔹 4444"], "mask", "emoji"),
    case(["| card | 5555 | 5555 | 5555 | 4444 |"], "mask", "table"),
    case(["> 5555 5555\n> 5555 4444"], "mask", "quoted"),
    # spelled expiries and codes (the round-3 held-out misses)
    case(["5555 5555 5555 4444 — exp twelve twenty-nine"], "mask", "spelled expiry"),
    case(["card expires December twenty twenty-nine, code seven thirty-seven"], "mask", "spelled expiry", pans=[]),
    case(["my card is 4111 1111 1111 1111 and the back says seven three seven"], "mask", "spelled code", pans=[VISA]),
    # the opening half of a number with no card context: removed once the second half completes it
    case(["here's the number I have written down: 5555 5555", "5555 4444"], "mask", "opening half"),
    case(["6011 1111", "1111 1117"], "mask", "opening half", pans=[DISCOVER]),
    case(["first part 4111 1111 1111", "and 1111"], "mask", "opening half", pans=[VISA]),
    # a 4-digit code with no cue, in a message (or after one) that carries card data
    case(["3782 822463 10005 4321"], "mask", "amex code no cue", pans=[AMEX], codes=["4321"]),
    case(["3782 822463 10005", "4321"], "mask", "amex code next message", pans=[AMEX], codes=["4321"]),
    case(["card 4111 1111 1111 1111, 12/29, 737"], "mask", "bundle no cues", pans=[VISA]),
    # over-redaction the round-3 interviewer reported (report 3.1): a last four next to a cue word
    case(["For verification: my last four are 6610 and my zip is 73301. I want my money back, please dispute it."], "keep", "verify cue"),
    case(["Security check: card ending 6610, zip 73301"], "keep", "verify cue"),
    case(["For security, my last 4 digits are 4427 and the billing ZIP is 94107"], "keep", "verify cue"),
    case(["the card on the front ends in 5127"], "keep", "verify cue"),
    case(["I want my money back, card ending 6610"], "keep", "verify cue"),
    case(["I already gave you the last four, 6610, for the security check"], "keep", "verify cue"),
    case(["back to the dispute: card ending 8830, zip 10011"], "keep", "verify cue"),
    # what card-context rules must still leave alone
    case(["dispute the Nov 3 2026 charge, it was 240 dollars"], "keep", "date in words"),
    case(["my card is [REDACTED CARD NUMBER]", "my last four are 6610 and my ZIP is 73301"], "keep", "after card message"),
    case(["the number was [REDACTED CARD NUMBER]", "sorry, for verification it's card ending 4427, zip 94107"], "keep", "after card message"),
    case(["I was charged 240 for the gym renewal on November 3"], "keep", "plain amount"),
    case(["we stayed in room 312 and took flight 737 to Boston"], "keep", "bare 3-digit"),
    case(["my Amazon order 112-4455667-8899001 never arrived"], "keep", "order number"),
    case(["tracking number 9400 1000 0000 0000 0000 00"], "keep", "tracking number"),
    case(["call me on +44 20 7946 0958 or (415) 555-0100"], "keep", "phone"),
    case(["booking ref QX7-88123, refund of 1,299.00 due 2026-12-01"], "keep", "reference"),
    case(["The subscription expires 12/31 and renews every year"], "keep", "subscription expiry"),
]

# Added after the round-4 blind run (heldout-r4 corpus and the independent fuzzer) found these shapes; variants of
# them, not the held-out strings. The held-out results stay as first recorded.
JCB = "3530111333300000"
REDACTION_TUNING_R4 += [
    case(["Amex:\n34343\n43434\n34343"], "mask", "amex in fives", pans=["343434343434343"]),
    case(["it reads 37828 then 22463 then 10005 on the card"], "mask", "amex in fives", pans=[AMEX]),
    case(["the code next to the signature is 604"], "mask", "code by signature", pans=[], codes=["604"], expiries=[]),
    case(["4111\n1111\n1121\n1111", "sorry typo, it's 4111 1111 1111 1111"], "mask", "correction over messages", pans=[VISA]),
    case(["8530 1113 3330 0000", "no wait: 3530 1113 3330 0000"], "mask", "correction over messages", pans=[JCB]),
    case(["four one one one one one one one one one one one one one one one seven three seven is the cvv"], "mask",
         "spoken number run into code", pans=[VISA]),
    case(["41111111111111117370"], "mask", "run together with code", pans=[VISA], codes=[], expiries=[]),
    case(["My subscription expiration date is 11/30, not 11/03"], "keep", "expiry cue, not a card"),
    case(["The parcel says exp. delivery 12/02, still not here"], "keep", "expiry cue, not a card"),
    case(["the number was [REDACTED CARD NUMBER]", "you only need the last four? fine, it's 6610, zip 73301"], "keep", "after card message"),
    case(["the number was [REDACTED CARD NUMBER]", "ok the last four then: 8830 and ZIP 10011"], "keep", "after card message"),
    case(["UPS tracking 4521 3367 8810, card ending 4427"], "keep", "reference then last four"),
    case(["hmm, 4111?", "or 1111?", "maybe 1111", "found it, card ending 1112, ZIP 73301"], "keep", "verification guesses"),
]
