"""Score the card-data masker: recall on what must be masked, precision on what must come through unchanged.

    python eval_redaction.py tuning            # the cases the masker was developed against (rounds 2-4)
    python eval_redaction.py heldout           # round 3's held-out corpus (spent: run blind once in round 3)
    python eval_redaction.py heldout-r4        # round 4's held-out corpus, written by a separate agent before the fixes
    python eval_redaction.py fuzz              # round 3's seeded fuzzer (one card number, single-line separators)
    python eval_redaction.py fuzz-v2           # round 4's seeded fuzzer: every family the round-3 review found, many cards
    python eval_redaction.py fuzz-v2-fresh     # the same grammar, three seeds fixed before the final pass and run only then
    python eval_redaction.py fuzz-independent  # a fuzzer written by a separate agent from its own grammar (round 4)

No model calls. A case is one customer's consecutive messages, scored as the conversation would be STORED: each
message is masked with the session's earlier stored messages as context, and a later message may rewrite an earlier
stored one (a number completed across messages is removed from both). A "mask" case passes if none of its declared
secrets (card numbers, security codes, expiries) can be recovered from the stored conversation by the auditor's
scanner (cardcare/store_audit.py, written independently of the masker; it reads digits in order across any gaps,
newlines and words, with number words read both as digits and as words). A "keep" case passes only if every stored
message equals its normalised input exactly, so any over-redaction fails it.
Writes evidence/redaction/<corpus>.md.
"""

import random
import sys
from pathlib import Path

from cardcare import masking
from cardcare.heldout import REDACTION_HELDOUT
from cardcare.redaction_cases import REDACTION_TUNING, REDACTION_TUNING_R4
from cardcare.store_audit import DEFAULT_SECRETS, secrets_left

CODE_DIR = Path(__file__).resolve().parent


def _as_case(entry, note: str) -> dict:
    """Round-2/3 cases are (text, previous messages, expected): the same conversation, with the default secrets."""
    if isinstance(entry, dict):
        return entry
    text, previous, expected = entry
    secrets = DEFAULT_SECRETS if expected == "mask" else {"pans": [], "codes": [], "expiries": []}
    return {"messages": [*previous, text], "expect": expected, "note": note, **{k: list(v) for k, v in secrets.items()}}


def stored_conversation(messages: list[str]) -> list[str]:
    """What the session store would hold after these customer messages, oldest first."""
    if hasattr(masking, "mask_conversation"):
        return masking.mask_conversation(messages)
    stored: list[str] = []  # round-3 masker: each message masked against the stored earlier ones, nothing rewritten
    for message in messages:
        stored.append(masking.mask_customer_text(message, tuple(stored[-3:])))
    return stored


def score(case: dict) -> tuple[bool, list[str], str]:
    stored = stored_conversation(case["messages"])
    if case["expect"] == "mask":
        left = secrets_left("\n".join(stored), {k: case.get(k, []) for k in ("pans", "codes", "expiries")})
        return not left, stored, ("left: " + ", ".join(left)) if left else ""
    changed = [i for i, (a, b) in enumerate(zip(case["messages"], stored)) if masking.normalize(a) != b]
    return not changed, stored, f"changed message(s) {changed}" if changed else ""


# --------------------------------------------------------------------------- round 3's fuzzer (kept, unchanged)
_DIGIT_WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
_SEPARATORS = [" ", "-", "–", "—", "−", " ", " ", " ", "\t", ".", "/", "_", "·", "|", ",", " - ",
               "  ", "​", "－", " / "]
_GAP_WORDS = [" then ", " and ", " dash ", " space ", " , then ", " next ", " followed by "]
_SPLITS = [[4, 4, 4, 4], [8, 8], [4, 8, 4], [4, 4, 8], [16], [2, 2, 4, 4, 4], [4, 4, 4, 2, 2], [6, 6, 4], [4, 12]]
_FRAMES = ["my card is {}", "{} is the card", "card: {} thanks", "number {} please", "it says {} on the front",
           "use {}", "the full number is {}, is that right?", "{}"]


def _fuzz_pan(rng: random.Random) -> str:
    pan, groups, i = "5555555555554444", [], 0
    for size in rng.choice(_SPLITS):
        group = pan[i:i + size]
        i += size
        if rng.random() < 0.15:
            group = " ".join(_DIGIT_WORDS[int(d)] for d in group)
        elif rng.random() < 0.15:
            group = "".join(chr(0xFF10 + int(d)) for d in group)  # full-width digits
        groups.append(group)
    gap = rng.choice(_GAP_WORDS) if rng.random() < 0.25 else None
    text = groups[0]
    for group in groups[1:]:
        text += (gap or rng.choice(_SEPARATORS)) + group
    return rng.choice(_FRAMES).format(text)


def _fuzz_keep(rng: random.Random) -> str:
    parts = [f"case C-{rng.randint(5000, 5999)}", f"transaction T-{rng.randint(1000, 2999)}", f"${rng.randint(1, 999)}.{rng.randint(10, 99)}",
             f"{rng.randint(2, 90)} dollars", f"on 2026-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d}", f"at {rng.randint(0, 23):02d}:{rng.randint(0, 59):02d}",
             f"card ending {rng.randint(1000, 9999)}", f"ZIP {rng.randint(10000, 99999)}", f"reference {rng.randint(10000, 99999)}",
             f"call {rng.randint(200, 999)} {rng.randint(200, 999)} {rng.randint(1000, 9999)}", f"confirmation CN-{rng.randint(10000, 99999)}",
             f"since {rng.randint(1990, 2026)}", f"{rng.randint(2, 30)} days ago", f"cancellation number {rng.randint(1000, 9999)}-{rng.randint(1000, 9999)}"]
    return ", ".join(rng.sample(parts, rng.randint(2, 4)))


def _fuzz_split_pan(rng: random.Random) -> tuple[str, tuple, str]:
    cut = sorted(rng.sample([4, 8, 12], rng.choice([1, 2])))
    pan, pieces = "5555555555554444", []
    for a, b in zip([0] + cut, cut + [16]):
        pieces.append(" ".join(pan[i:i + 4] for i in range(a, b, 4)))
    lead = ["first part: {}", "it starts {}", "{}", "then {}", "next {}"]
    previous = tuple(rng.choice(lead).format(piece) for piece in pieces[:-1])
    return rng.choice(["and the rest {}", "last bit {}", "{}", "ends {}"]).format(pieces[-1]), previous, "mask"


def _fuzz_typed_in_turn(rng: random.Random) -> tuple[str, tuple, str]:
    line = lambda: rng.choice(["card ending {a}, ZIP {z}", "try {a} and {z}", "sorry, {a} / {z}", "last four {a}, zip {z}",
                               "case C-{c}, card ending {a}", "reference {r}, ZIP {z}"]).format(
        a=rng.randint(1000, 9999), z=rng.randint(10000, 99999), c=rng.randint(5000, 5999), r=rng.randint(10000, 99999))
    return line(), tuple(line() for _ in range(rng.randint(1, 3))), "keep"


def fuzz_corpus(seed: int = 7, size: int = 1000) -> list[dict]:
    rng = random.Random(seed)
    cases = ([((_fuzz_pan(rng), (), "mask"), "r3 single line") for _ in range(size)]
             + [(_fuzz_split_pan(rng), "r3 split") for _ in range(size // 4)]
             + [((_fuzz_keep(rng), (), "keep"), "r3 keep") for _ in range(size)]
             + [(_fuzz_typed_in_turn(rng), "r3 typed in turn") for _ in range(size // 4)])
    return [_as_case(entry, note) for entry, note in cases]


# --------------------------------------------------------------------------- round 4's fuzzer: the families round 3 missed
_TEST_PANS = ["5555555555554444", "4111111111111111", "4242424242424242", "378282246310005", "6011111111111117",
              "2223003122003222", "3530111333300000", "4000056655665556"]
_PREFIXES = [("4", 16), ("4", 13), ("4", 19), ("51", 16), ("55", 16), ("2221", 16), ("2720", 16), ("34", 15), ("37", 15),
             ("6011", 16), ("65", 16), ("3528", 16), ("36", 14), ("62", 19)]
_TENS = {2: "twenty", 3: "thirty", 4: "forty", 5: "fifty", 6: "sixty", 7: "seventy", 8: "eighty", 9: "ninety"}
_TEENS = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
_MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def _luhn_complete(body: str) -> str:
    for check in "0123456789":
        digits, total = body + check, 0
        for position, char in enumerate(reversed(digits)):
            value = int(char) * (2 if position % 2 else 1)
            total += value - 9 if value > 9 else value
        if total % 10 == 0:
            return digits
    raise AssertionError


def _random_pan(rng: random.Random) -> str:
    if rng.random() < 0.4:
        return rng.choice(_TEST_PANS)
    prefix, length = rng.choice(_PREFIXES)
    return _luhn_complete(prefix + "".join(rng.choice("0123456789") for _ in range(length - len(prefix) - 1)))


def _groups(pan: str, rng: random.Random) -> list[str]:
    if len(pan) == 15 and rng.random() < 0.8:
        return [pan[:4], pan[4:10], pan[10:]]
    if len(pan) == 14 and rng.random() < 0.7:
        return [pan[:4], pan[4:10], pan[10:]]
    size = rng.choice([4, 4, 4, 4, 8, len(pan)])
    return [pan[i:i + size] for i in range(0, len(pan), size)]


def _pair_words(group: str) -> str:
    words = []
    for i in range(0, len(group), 2):
        pair = group[i:i + 2]
        if len(pair) == 1 or pair[0] == "0":
            words += [("oh" if d == "0" else _DIGIT_WORDS[int(d)]) for d in pair]
        elif pair[0] == "1":
            words.append(_TEENS[int(pair[1])])
        else:
            words.append(_TENS[int(pair[0])] + ("" if pair[1] == "0" else "-" + _DIGIT_WORDS[int(pair[1])]))
    return " ".join(words)


def _spell(group: str, rng: random.Random) -> str:
    style = rng.choice(["digits", "pairs", "double"])
    if style == "pairs":
        return _pair_words(group)
    if style == "double":
        out, i = [], 0
        while i < len(group):
            if i + 1 < len(group) and group[i] == group[i + 1]:
                out.append("double " + _DIGIT_WORDS[int(group[i])])
                i += 2
            else:
                out.append(_DIGIT_WORDS[int(group[i])])
                i += 1
        return " ".join(out)
    return " ".join(_DIGIT_WORDS[int(d)] for d in group)


_UNICODE_ZEROS = [0xFF10, 0x0660, 0x0966, 0x06F0]


def _unicode_digits(group: str, rng: random.Random) -> str:
    zero = rng.choice(_UNICODE_ZEROS)
    return "".join(chr(zero + int(d)) for d in group)


_JOINERS = {
    "newline": ["\n", "\r\n", "\n\n"],
    "bullets": ["\n- ", "\n* ", "\n• ", "\n> "],
    "sentence break": [". ", "! ", "? ", ".\n"],
    "semicolon/colon": ["; ", ": ", ";", " ; "],
    "read-out": [", followed by ", ", then the next block is ", ". After that it's ", " and then comes ", ", next group: ",
                 " — then — "],
}
_DICTATION = [("the first four are {0}, the next four are {1}, the third group is {2} and the last four are {3}", 4),
              ("starting with {0}, then {1}, then {2}, ending in {3}", 4),
              ("ok so it's {0}... {1}... {2}... and {3}", 4),
              ("first block {0}, middle block {1}, last block {2}", 3)]
_LEADS = ["", "my card is ", "here's my card number: ", "Card number below\n", "I'm reading it off the card: ", "Copied from my statement: "]


def _render_pan(pan: str, family: str, rng: random.Random) -> str:
    groups = _groups(pan, rng)
    if family == "dictation":
        template, n = rng.choice([d for d in _DICTATION if d[1] == len(groups)] or [("{}".join([""] * 1), 1)])
        if n != len(groups):
            return rng.choice(_LEADS) + " ".join(groups)
        groups = [g if rng.random() < 0.7 else _spell(g, rng) for g in groups]
        return template.format(*groups)
    if family == "spelled":
        joiner = rng.choice([", ", " ", "; ", "\n"])
        return rng.choice(_LEADS) + joiner.join(_spell(g, rng) for g in groups)
    if family == "unicode digits":
        return rng.choice(_LEADS) + rng.choice([" ", "-", "\n"]).join(_unicode_digits(g, rng) for g in groups)
    if family == "spaced digits":
        return rng.choice(_LEADS) + " ".join(pan)
    joiner = rng.choice(_JOINERS[family])
    text = joiner.join(groups)
    if family == "bullets":
        text = joiner.strip(" \n") + " " + text if rng.random() < 0.8 else text
    return rng.choice(_LEADS) + text


def _expiry(rng: random.Random) -> tuple[str, str]:
    month, year = rng.randint(1, 12), rng.randint(26, 33)
    rendering = rng.choice([f"{month:02d}/{year}", f"{month:02d}-20{year}", f"{month}/{year}", f"{_MONTHS[month - 1][:3]} 20{year}",
                            f"{_MONTHS[month - 1]} 20{year}", f"{_pair_words(f'{month:02d}') if month >= 10 else _DIGIT_WORDS[month]} "
                            f"{_pair_words(str(year))}"])
    return f"{month:02d}/{year}", rendering


def _code(rng: random.Random, amex: bool) -> tuple[str, str]:
    code = "".join(rng.choice("0123456789") for _ in range(4 if amex else 3))
    while code[0] == "0" or len(set(code)) == 1:
        code = "".join(rng.choice("0123456789") for _ in range(4 if amex else 3))
    return code, rng.choice([code, " ".join(code), _spell(code, rng)])


def fuzz_v2(seed: int = 11, per_family: int = 150) -> list[dict]:
    rng = random.Random(seed)
    cases = []
    for family in ["newline", "bullets", "sentence break", "semicolon/colon", "read-out", "dictation", "spelled", "unicode digits",
                   "spaced digits"]:
        for _ in range(per_family):
            pan = _random_pan(rng)
            cases.append({"messages": [_render_pan(pan, family, rng)], "expect": "mask", "note": family, "pans": [pan], "codes": [],
                          "expiries": []})
    for _ in range(per_family):  # split over 2-4 messages, with chatter around the pieces
        pan = _random_pan(rng)
        groups = _groups(pan, rng)
        cut = sorted(rng.sample(range(1, len(groups)), min(len(groups) - 1, rng.randint(1, 3)))) if len(groups) > 1 else []
        pieces = [" ".join(groups[a:b]) for a, b in zip([0] + cut, cut + [len(groups)])]
        lead = ["{}", "it starts {}", "next part {}", "{} (continued)", "then {}", "ok: {}", "the rest is {}"]
        cases.append({"messages": [rng.choice(lead).format(p) for p in pieces], "expect": "mask", "note": "split messages",
                      "pans": [pan], "codes": [], "expiries": []})
    for _ in range(per_family):  # number, expiry and code together, with or without cue words
        pan = _random_pan(rng)
        expiry, expiry_text = _expiry(rng)
        code, code_text = _code(rng, amex=len(pan) == 15)
        cue = rng.random() < 0.5
        parts = [_render_pan(pan, rng.choice(["newline", "semicolon/colon", "sentence break"]), rng),
                 ("exp " if cue else "") + expiry_text, ("cvv " if cue else "") + code_text]
        cases.append({"messages": [rng.choice([" / ", "\n", ", ", ". "]).join(parts)], "expect": "mask",
                      "note": "bundle with cues" if cue else "bundle without cues", "pans": [pan], "codes": [code], "expiries": [expiry]})
    for _ in range(per_family):  # a code with a cue phrase, no number
        code, code_text = _code(rng, amex=rng.random() < 0.2)
        cue = rng.choice(["the cvv is {}", "security code: {}", "the code on the back is {}", "the 3 digits on the reverse are {}",
                          "CVC {}", "card verification value {}", "the number by the signature strip is {}", "CID on the front: {}"])
        cases.append({"messages": [cue.format(code_text)], "expect": "mask", "note": "code with cue", "pans": [], "codes": [code], "expiries": []})
    # keep side
    for _ in range(per_family):
        last4, zip_code = f"{rng.randint(1000, 9999)}", f"{rng.randint(10000, 99999)}"
        template = rng.choice(["For verification: my last four are {a} and my zip is {z}.", "Security check: card ending {a}, zip {z}",
                               "For security, my last 4 digits are {a} and the billing ZIP is {z}", "the card on the front ends in {a}",
                               "I want my money back, card ending {a}", "I already gave you the last four, {a}, for the security check",
                               "verification details: ends with {a}, ZIP {z}", "back on the dispute: card ending {a}, zip {z}",
                               "my card's last 4 are {a}, front says so, and the postcode is {z}"])
        cases.append({"messages": [template.format(a=last4, z=zip_code)], "expect": "keep", "note": "verify cue", "pans": [], "codes": [],
                      "expiries": []})
    for _ in range(per_family):
        template = rng.choice(["I was charged {n} for the renewal", "they took {n} twice", "paid {n} on {d}", "the refund of {n} never came",
                               "we were in room {r} and the flight was {r}", "order {o} arrived broken", "tracking {t}",
                               "call me on {p}", "booking ref {b}", "I've had the card since {y}, about {k} purchases a year",
                               "the charge on {d} for {n} and another on {d2}", "my Amazon order {amz} never arrived",
                               "subscription renews {d} every year, {n} each time"])
        cases.append({"messages": [template.format(
            n=rng.choice([f"{rng.randint(10, 999)}", f"{rng.randint(1, 99)}.{rng.randint(10, 99)}", f"${rng.randint(1, 2000):,}",
                          f"{rng.randint(2, 500)} dollars", f"€{rng.randint(1, 300)}"]),
            d=rng.choice([f"2026-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d}", f"{rng.randint(1, 12)}/{rng.randint(1, 28)}",
                          f"{_MONTHS[rng.randint(0, 11)][:3]} {rng.randint(1, 28)}", f"{rng.randint(1, 28)} {_MONTHS[rng.randint(0, 11)]} 2026"]),
            d2=f"{_MONTHS[rng.randint(0, 11)]} {rng.randint(1, 28)}", r=rng.randint(100, 999),
            o=f"{rng.randint(100, 999)}-{rng.randint(1000, 9999)}", t=f"9400 {rng.randint(1000, 9999)} {rng.randint(1000, 9999)} "
                                                                       f"{rng.randint(1000, 9999)} {rng.randint(1000, 9999)} {rng.randint(10, 99)}",
            p=rng.choice([f"+1 {rng.randint(200, 999)} {rng.randint(200, 999)} {rng.randint(1000, 9999)}",
                          f"({rng.randint(200, 999)}) {rng.randint(200, 999)}-{rng.randint(1000, 9999)}",
                          f"+44 20 {rng.randint(1000, 9999)} {rng.randint(1000, 9999)}"]),
            b=f"QX{rng.randint(1, 9)}-{rng.randint(10000, 99999)}", y=rng.randint(1995, 2026), k=rng.randint(10, 300),
            amz=f"1{rng.randint(10, 99)}-{rng.randint(1000000, 9999999)}-{rng.randint(1000000, 9999999)}")],
            "expect": "keep", "note": "numbers a dispute needs", "pans": [], "codes": [], "expiries": []})
    for _ in range(per_family // 2):  # verification typed after a message that carried card data (stored masked)
        last4, zip_code = f"{rng.randint(1000, 9999)}", f"{rng.randint(10000, 99999)}"
        cases.append({"messages": [rng.choice(["my card is [REDACTED CARD NUMBER]", "[REDACTED CARD NUMBER] exp [REDACTED EXPIRY]"]),
                                   rng.choice([f"for verification, card ending {last4} and zip {zip_code}", f"my last four are {last4}, ZIP {zip_code}"])],
                      "expect": "keep", "note": "after card message", "pans": [], "codes": [], "expiries": []})
    # ---- round 5: the families the round-4 review found (appended, so every earlier case of a seed is unchanged)
    for _ in range(per_family):  # a 3-4 digit token before the number, joined to it by separators only
        pan = _random_pan(rng)
        code, code_text = _code(rng, amex=len(pan) == 15)
        expiry, _ = _expiry(rng)
        lead = rng.choice([f"CVV: {code}", f"cvv {code}", f"security code {code};", f"PIN {rng.randint(1000, 9999)};",
                           f"PIN {rng.randint(1000, 9999)}", f"exp {expiry.replace('/', '')}:", f"{expiry.replace('/', '')}"])
        number = rng.choice([" ", "-"]).join(_groups(pan, rng))
        codes = [code] if lead.lower().startswith(("cvv", "security")) else []
        cases.append({"messages": [f"{rng.choice(['', 'here: ', 'In case you need it, '])}{lead} {number}{rng.choice(['', ', exp 12/29', '.'])}"],
                      "expect": "mask", "note": "leading token in the run", "pans": [pan], "codes": codes, "expiries": []})
    for _ in range(per_family):  # an order or booking label before the number, in the same run
        pan = _random_pan(rng)
        label = rng.choice(["order no. {o};", "Order {o},", "order {o}", "booking {o};", "Order #{o}", "reference {o}:", "ticket {o},"])
        order = rng.choice([f"{rng.randint(10000, 99999)}", f"{rng.randint(1000000, 9999999)}", f"{rng.randint(100000, 999999)}"])
        number = rng.choice([" ", "-"]).join(_groups(pan, rng))
        cases.append({"messages": [f"{label.format(o=order)} {number}{rng.choice([' was declined', ' is the card I used', ''])}"],
                      "expect": "mask", "note": "order label before the number", "pans": [pan], "codes": [], "expiries": []})
    for _ in range(per_family):  # a ZIP phrase in the message that opens a split number
        pan = _random_pan(rng)
        groups = _groups(pan, rng)
        if len(groups) < 2:
            groups = [pan[:-4], pan[-4:]]
        zip_code = f"{rng.randint(10000, 99999)}"
        opening = " ".join(groups[:-1]) + rng.choice([f" and my zip is {zip_code}", f", zip {zip_code}", f" (ZIP {zip_code})"])
        cases.append({"messages": [opening, groups[-1]], "expect": "mask", "note": "zip in the opening message of a split", "pans": [pan],
                      "codes": [], "expiries": []})
    for _ in range(per_family):  # the last four first, then the rest of the number
        pan = _random_pan(rng)
        if len(pan) != 16:
            pan = rng.choice([p for p in _TEST_PANS if len(p) == 16])
        rest = " ".join(pan[i:i + 4] for i in range(0, 12, 4))
        first = rng.choice([f"card ending {pan[-4:]}, zip {rng.randint(10000, 99999)}", f"the last four are {pan[-4:]}", f"ending in {pan[-4:]}"])
        second = rng.choice([f"and the first twelve: {rest}", f"the rest is {rest}", f"the first 12 are {rest}"])
        cases.append({"messages": [first, second] if rng.random() < 0.7 else [f"{first}, {second}"], "expect": "mask",
                      "note": "last four given, then the rest", "pans": [pan], "codes": [], "expiries": []})
    for _ in range(per_family):  # the exemption's cost, measured: answer-sized pieces (<= 5 digits per message), one message a step-up answer
        pan = rng.choice([p for p in _TEST_PANS if len(p) == 16])
        pieces = [pan[i:i + 4] for i in range(0, 16, 4)]
        at = rng.randrange(4)
        zip_code = f"{rng.randint(10000, 99999)}"
        messages = [f"{p} and my zip is {zip_code}" if i == at else rng.choice(["{}", "then {}", "next {}", "{} ..."]).format(p) for i, p in enumerate(pieces)]
        cases.append({"messages": messages, "expect": "mask", "note": "answer-sized pieces with a zip phrase (the exemption; listed miss)",
                      "pans": [pan], "codes": [], "expiries": []})
    for _ in range(per_family):  # keep: references and tracking numbers after a label, not cards
        tracking = f"9400 {rng.randint(1000, 9999)} {rng.randint(1000, 9999)} {rng.randint(1000, 9999)} {rng.randint(1000, 9999)} {rng.randint(10, 99)}"
        text = rng.choice([f"order {rng.randint(1000000, 9999999)} arrived broken", f"tracking {tracking}", f"booking ref QX{rng.randint(1, 9)}-{rng.randint(10000, 99999)}",
                           f"order no. {rng.randint(10000, 99999)}; the invoice was {rng.randint(1000, 9999)} {rng.randint(1000, 9999)}",
                           f"ticket {rng.randint(100000, 999999)}, paid {rng.randint(10, 999)}.{rng.randint(10, 99)}",
                           f"my Amazon order 1{rng.randint(10, 99)}-{rng.randint(1000000, 9999999)}-{rng.randint(1000000, 9999999)}"])
        cases.append({"messages": [text], "expect": "keep", "note": "reference after a label", "pans": [], "codes": [], "expiries": []})
    # ---- round 5, after its first final pass: a security code said twice in one message (appended, as above)
    for _ in range(per_family):
        code, _ = _code(rng, amex=False)
        first, second = rng.sample([code, " ".join(code), " ".join(_DIGIT_WORDS[int(d)] for d in code)], 2)
        if rng.random() < 0.25:  # or the same digits typed twice
            first = second = code
        said = first + rng.choice([" ({})", " [{}]", " = {}", "/{}", " - {}", "-{}", " {}", ", i.e. {}", " (that is {})"]).format(second)
        cue = rng.choice(["the cvv is {}", "security code: {}", "the code on the back is {}", "CVC {}", "cvv {}", "card verification value {}"])
        pan = _random_pan(rng) if rng.random() < 0.5 else None
        text = cue.format(said) if pan is None else rng.choice(["{n}, {c}", "{n}\n{c}\nexp 12/29", "{c}, card {n}"]).format(
            n=" ".join(_groups(pan, rng)), c=cue.format(said))
        cases.append({"messages": [text], "expect": "mask", "note": "code said twice", "pans": [pan] if pan else [], "codes": [code],
                      "expiries": []})
    for _ in range(per_family):  # keep: a number restated in brackets or in words that is not a code
        n = rng.randint(100, 999)
        words = " ".join(_DIGIT_WORDS[int(d)] for d in str(n))
        text = rng.choice([f"I was charged {n} ({rng.choice(['two', 'three', 'four'])} payments) by CloudNest", f"room {n} ({words}) at the hotel",
                           f"flight {n} ({words}) on November 30", f"order {rng.randint(1000, 9999)} ({rng.randint(2024, 2026)}) arrived late",
                           f"my last four are {n}7 ({words} seven) and ZIP {rng.randint(10000, 99999)}",
                           f"gate {n} - {words} - is where I paid", f"bus {n}/{n} to the airport"])
        cases.append({"messages": [text], "expect": "keep", "note": "a number restated, not a code", "pans": [], "codes": [], "expiries": []})
    for _ in range(per_family):  # an expiry typed with a space or a dot after its cue, with or without the number beside it
        month, year = rng.randint(1, 12), rng.randint(26, 33)
        written = rng.choice([f"{month:02d} {year}", f"{month:02d}.{year}", f"{month:02d} 20{year}", f"{month} {year}", f"{month:02d} / {year}"])
        cue = rng.choice(["exp {}", "expiry {}", "exp. date {}", "expiration: {}", "valid thru {}", "the card expires {}"])
        pan = _random_pan(rng) if rng.random() < 0.6 else None
        code, _ = _code(rng, amex=False)
        text = cue.format(written) if pan is None else rng.choice(["{n}, {e}, cvv {c}", "{n} {e}", "card {n} {e} cvv {c}", "{e} on {n}"]).format(
            n=" ".join(_groups(pan, rng)), e=cue.format(written), c=code)
        cases.append({"messages": [text], "expect": "mask", "note": "expiry with a space or a dot after its cue", "pans": [pan] if pan else [],
                      "codes": [code] if pan and "cvv" in text else [], "expiries": [f"{month:02d}/{year}"]})
    for _ in range(per_family):  # keep: an amount or a date written the same way, about something else
        a, b = rng.randint(1, 12), rng.randint(10, 33)
        text = rng.choice([f"I paid {a}.{b} for parking", f"the fee was {a}.{b} and the tip {rng.randint(1, 9)}.{rng.randint(10, 99)}",
                           f"my travel notice expiration should be {a} {b}", f"exp. delivery {a} {b}, still nothing",
                           f"the subscription exp {a:02d} {b} is the one I cancelled", f"seats {a} {b} on the flight to Lisbon",
                           f"my passport expires {a:02d} 20{b}"])
        cases.append({"messages": [text], "expect": "keep", "note": "an amount or a date, not an expiry", "pans": [], "codes": [], "expiries": []})
    return cases


def _independent() -> list[dict]:
    from cardcare.heldout_fuzz_r4 import generate
    return generate()


def _heldout_r4() -> list[dict]:
    from cardcare.heldout_r4 import REDACTION_HELDOUT_R4
    return REDACTION_HELDOUT_R4


CORPORA = {
    "tuning": lambda: [_as_case(c, "r2-r3 tuning") for c in REDACTION_TUNING] + REDACTION_TUNING_R4,
    "heldout": lambda: [_as_case(c, "r3 held-out") for c in REDACTION_HELDOUT],
    "heldout-r4": _heldout_r4,
    "fuzz": fuzz_corpus,
    "fuzz-v2": fuzz_v2,
    # seeds fixed before the round-4 final pass and never run before it: the round-4 grammar on inputs not tuned against
    "fuzz-v2-fresh": lambda: [case for seed in (7001, 7002, 7003) for case in fuzz_v2(seed=seed, per_family=100)],
    # declared after the first final pass spent the seeds above and the independent fuzzer's default seed; run only in the second
    "fuzz-v2-fresh2": lambda: [case for seed in (8001, 8002, 8003) for case in fuzz_v2(seed=seed, per_family=100)],
    "fuzz-independent-fresh": lambda: [case for seed in (41, 42, 43) for case in __import__("cardcare.heldout_fuzz_r4", fromlist=["generate"]).generate(seed=seed)],
    "fuzz-independent": _independent,
}


def evaluate_corpus(name: str) -> tuple[list[tuple], dict]:
    rows, families = [], {}
    for case in CORPORA[name]():
        ok, stored, why = score(case)
        rows.append((ok, case, stored, why))
        family = families.setdefault((case["expect"], case.get("note", "")), [0, 0])
        family[0] += ok
        family[1] += 1
    return rows, families


def main() -> None:
    name = sys.argv[1] if len(sys.argv) > 1 else "tuning"
    out_name = sys.argv[2] if len(sys.argv) > 2 else name
    rows, families = evaluate_corpus(name)
    masks = [r for r in rows if r[1]["expect"] == "mask"]
    keeps = [r for r in rows if r[1]["expect"] == "keep"]
    lines = [f"# Masker evaluation: {name} corpus", "", f"Generated by `python eval_redaction.py {name}`. No model calls.", "",
             f"- **recall** (no declared card number, code or expiry recoverable from the stored conversation): "
             f"{sum(r[0] for r in masks)}/{len(masks)}",
             f"- **precision** (every message stored exactly as typed): {sum(r[0] for r in keeps)}/{len(keeps)}", "",
             "| expected | family | passed |", "|---|---|---|"]
    lines += [f"| {expect} | {note} | {ok}/{total} |" for (expect, note), (ok, total) in sorted(families.items())]
    generated = name.startswith("fuzz")
    lines += ["", "Every failure" + (", then the first 30 cases." if generated else ", then every case."), "",
              "| result | expected | family | messages | stored | why |", "|---|---|---|---|---|---|"]
    cell = lambda v: repr(v).replace("|", "\\|")
    shown = [r for r in rows if not r[0]] + (rows[:30] if generated else rows)
    for ok, case, stored, why in shown:
        # a randomly generated number could be someone's real card (A20): such a case is described, never printed
        if any(pan not in _TEST_PANS for pan in case.get("pans", [])):
            messages = stored_cell = "(uses a randomly generated card number, not printed; regenerate it locally from the seed)"
        else:
            messages, stored_cell = cell(case["messages"]), cell(stored)
        lines.append(f"| {'pass' if ok else '**FAIL**'} | {case['expect']} | {case.get('note', '')} | {messages} | {stored_cell} | {why} |")
    out_path = CODE_DIR / "evidence" / "redaction" / f"{out_name}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n")
    print("\n".join(lines[4:6]))
    for (expect, note), (ok, total) in sorted(families.items()):
        if ok < total:
            print(f"  {expect:4} {note:28} {ok}/{total}")


if __name__ == "__main__":
    main()
