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
