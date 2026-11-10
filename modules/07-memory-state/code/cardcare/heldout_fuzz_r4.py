"""Round-4 held-out fuzzer for the card-data masker, written by a separate agent before the round-4 fixes.

Its grammar is its own: it imports nothing from cardcare.masking or eval_redaction.py, only the standard library.
Like cardcare/heldout_r4.py it is run once, blind.

    from cardcare.heldout_fuzz_r4 import generate
    cases = generate(seed=4, size=600)

Every case has the REDACTION_HELDOUT_R4 format: {"messages": [...], "expect": "mask" | "keep", "pans": [...],
"codes": [...], "expiries": ["MM/YY", ...], "note": <family>}. About half are "mask" and half "keep".

Mask families are the ways card details reach a chat box: statement and PDF pastes (one group per line, blank lines,
Windows line ends), notes-app bullets and lettered lists, sentence breaks and semicolons, tables, tabs, read-outs
with long or varying joiners, number words, digits from other keyboards (full-width, Arabic-Indic, Devanagari,
mathematical bold, keycap emoji), a number split over several messages, details trickling in one per message,
corrections, Amex in its own groupings, and codes and expiries in many phrasings.

Keep families are the numbers a card desk needs intact: last fours and ZIPs next to security-sounding words, amounts
with and without a currency, dates and times, phone numbers, long order, tracking, ticket and acquirer reference
numbers (none of them Luhn-valid card numbers), case and transaction ids, labelled 3-digit numbers, cue words used in
their everyday sense, and several numbers typed over a few messages (including last-four guesses that happen to
complete a Luhn-valid number across messages).

A generated mask case is checked against its own oracle before it is returned: every declared item must be visible in
the raw messages, and nothing left once the card-data spans are removed may spell a declared item by accident.
"""

import random
import re
import unicodedata

PANS = ("5555555555554444", "4111111111111111", "4242424242424242", "378282246310005", "6011111111111117",
        "2223003122003222", "3530111333300000", "4000056655665556")
MONTH_NAMES = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
               "November", "December")
_WORDS = ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine")

# ------------------------------------------------------------------------------------------- the oracle

_UNITS = dict(zip(_WORDS, "0123456789")) | {"oh": "0"}
_TEENS = {"ten": "10", "eleven": "11", "twelve": "12", "thirteen": "13", "fourteen": "14", "fifteen": "15",
          "sixteen": "16", "seventeen": "17", "eighteen": "18", "nineteen": "19"}
_TENS = {"twenty": "2", "thirty": "3", "forty": "4", "fifty": "5", "sixty": "6", "seventy": "7", "eighty": "8", "ninety": "9"}


def _audit(text: str) -> str:
    """Text as a strict reader sees it: NFKC, every decimal digit as ASCII, number words as digits."""
    text = unicodedata.normalize("NFKC", text)
    text = "".join(str(unicodedata.digit(c)) if unicodedata.category(c) == "Nd" else c for c in text)
    units = "|".join(w for w in _WORDS if w != "zero")
    text = re.sub(rf"\b({'|'.join(_TENS)})[\s-]?({units})\b", lambda m: _TENS[m[1].lower()] + _UNITS[m[2].lower()], text, flags=re.I)
    text = re.sub(rf"\b({'|'.join(_TENS)})\b", lambda m: _TENS[m[1].lower()] + "0", text, flags=re.I)
    text = re.sub(rf"\b({'|'.join(_TEENS)})\b", lambda m: _TEENS[m[1].lower()], text, flags=re.I)
    return re.sub(rf"\b({'|'.join(_UNITS)})\b", lambda m: _UNITS[m[1].lower()], text, flags=re.I)


def _in_order(digits: str, text: str) -> bool:
    return bool(re.search(r"\D{0,20}".join(digits), text))


def _expiry_visible(mmyy: str, text: str) -> bool:
    mm, yy = mmyy.split("/")
    month = int(mm)
    return bool(_in_order(mm + yy, text) or re.search(rf"(?<!\d)0?{month}\D{{0,20}}(?:20)?{yy}(?!\d)", text)
                or re.search(rf"\b{MONTH_NAMES[month - 1][:3]}[a-z]*\.?\s*'?(?:20)?{yy}\b", text, re.I))


def _visible(case: dict, text: str) -> list[str]:
    """Which declared items a reader can still recover from `text`."""
    audited = _audit(text)
    return ([p for p in case["pans"] if _in_order(p, audited)] + [c for c in case["codes"] if _in_order(c, audited)]
            + [e for e in case["expiries"] if _expiry_visible(e, audited)])


def _passes_luhn(digits: str) -> bool:
    total = 0
    for i, ch in enumerate(reversed(digits)):
        value = int(ch) * (2 if i % 2 else 1)
        total += value - 9 if value > 9 else value
    return total % 10 == 0


def _card_like(text: str) -> bool:
    """A separator-joined run of digit groups (no letters between) with a 13-19 digit Luhn-valid window."""
    for match in re.finditer(r"\d+(?:[^\w\n]{1,3}\d+)*", _audit(text)):
        groups = re.findall(r"\d+", match.group())
        for i in range(len(groups)):
            for j in range(i + 1, len(groups) + 1):
                run = "".join(groups[i:j])
                if 13 <= len(run) <= 19 and _passes_luhn(run):
                    return True
    return False


# ------------------------------------------------------------------------------------------- rendering card data

_SCRIPTS = ["ascii"] * 13 + ["words"] * 3 + ["spaced", "fullwidth", "arabic-indic", "devanagari", "bold", "keycap"]


def _render(digits: str, script: str, rng: random.Random) -> str:
    if script == "words":
        return " ".join(("oh" if d == "0" and rng.random() < 0.5 else _WORDS[int(d)]) for d in digits)
    if script == "spaced":
        return " ".join(digits)
    if script == "keycap":
        return "".join(d + "️⃣" for d in digits)
    base = {"ascii": ord("0"), "fullwidth": 0xFF10, "arabic-indic": 0x0660, "devanagari": 0x0966, "bold": 0x1D7CE}[script]
    return "".join(chr(base + int(d)) for d in digits)


def _groups(pan: str, rng: random.Random) -> list[str]:
    if len(pan) == 15:
        sizes = rng.choice([[4, 6, 5], [4, 6, 5], [4, 4, 4, 3], [15], [5, 5, 5]])
    else:
        sizes = rng.choice([[4, 4, 4, 4], [4, 4, 4, 4], [4, 4, 4, 4], [8, 8], [4, 8, 4], [4, 12], [16]])
    out, i = [], 0
    for size in sizes:
        out.append(pan[i:i + size])
        i += size
    return out


_READ_OUT = [", then ", ", and after that ", ", followed by ", " and next comes ", ", after which it's ", " and then ", ", next is "]
_LETTERS = "abcdefgh"


def _layout(parts: list[str], rng: random.Random) -> tuple[str, str]:
    """Join rendered groups the way a paste or a dictation lays them out; returns (text, family)."""
    family = rng.choice(["newline", "newline", "blank lines", "crlf", "bullets", "lettered", "sentence breaks", "semicolons",
                         "pipes", "tabs", "read-out", "labelled read-out", "commas", "plain"])
    if len(parts) == 1:
        family = "run together"
        return parts[0], family
    if family == "newline":
        return "\n".join(parts), family
    if family == "blank lines":
        return "\n\n".join(parts), family
    if family == "crlf":
        return "\r\n".join(parts), family
    if family == "bullets":
        marker = rng.choice(["-", "•", "*", "·"])
        return "\n".join(f"{marker} {p}" for p in parts), family
    if family == "lettered":
        return "\n".join(f"{_LETTERS[i]}) {p}" for i, p in enumerate(parts)), family
    if family == "sentence breaks":
        return ". ".join(parts) + ".", family
    if family == "semicolons":
        return rng.choice(["; ", ";", " ; "]).join(parts), family
    if family == "pipes":
        return " | ".join(parts), family
    if family == "tabs":
        return "\t".join(parts), family
    if family == "read-out":
        text = rng.choice(["it starts with ", "it goes ", "", "so it's "]) + parts[0]
        for p in parts[1:-1]:
            text += rng.choice(_READ_OUT) + p
        return text + rng.choice([", and it ends with ", " and finally ", ", and lastly ", " and the end is "]) + parts[-1], family
    if family == "labelled read-out":
        labels = ["the first group is ", "then ", "the third is ", "after that "]
        text = ", ".join(labels[min(i, 3)] + p for i, p in enumerate(parts[:-1]))
        return text + rng.choice([" and the last is ", ", last one ", " and it ends "]) + parts[-1], family
    if family == "commas":
        return ", ".join(parts), family
    return rng.choice([" ", "-", " - ", ".", "/", "  "]).join(parts), family


_CODE_PHRASES = ["CVV {}", "cvc: {}", "security code {}", "the 3 digits on the back are {}", "code on the back: {}", "CVV2 {}",
                 "sec code - {}", "{} is the code", "the number by the signature is {}", "verification number {}", "csc {}"]
_AMEX_CODE_PHRASES = ["CID {}", "the 4 digits on the front are {}", "Amex code {}", "security code {}", "front code: {}"]
_EXPIRY_PHRASES = [("exp ", "{mm}/{yy}"), ("exp. ", "{mm}/{yy}"), ("expires ", "{mm}/{yy}"), ("valid thru ", "{mm}/{yy}"),
                   ("good thru ", "{mm}-{yy}"), ("expiry ", "{mm}/20{yy}"), ("exp ", "{mm}{yy}"), ("expiration ", "{month} 20{yy}"),
                   ("expiry date: ", "{m}/{yy}"), ("exp ", "{mm} / {yy}"), ("valid until ", "{mon} 20{yy}"), ("expires end of ", "{month} '{yy}")]
_PREFIXES = ["", "", "my card number is ", "Card number:\n", "Here it is exactly as it shows on my statement:\n",
             "copied from my notes app:\n", "voice typing, sorry: ", "From the PDF:\n", "For the refund use this card: ",
             "ok so the number on the card is ", "Account Number\n", "the card the merchant has is "]
_SUFFIXES = ["", "", " thanks", "\nis that enough?", ". Can you check it?", " 🙏", "\n\nsent from my phone",
             " - please dispute the CloudNest charge on it"]


def _code(pan: str | None, rng: random.Random) -> str:
    return str(rng.randint(1000, 9999)) if pan and len(pan) == 15 else str(rng.randint(100, 999))


def _code_text(code: str, rng: random.Random) -> list[tuple[str, bool]]:
    phrase = rng.choice(_AMEX_CODE_PHRASES if len(code) == 4 else _CODE_PHRASES)
    script = rng.choice(["ascii"] * 6 + ["words", "spaced"])
    before, after = phrase.split("{}")
    return [(before, False), (_render(code, script, rng), True), (after, False)]


def _expiry(rng: random.Random) -> tuple[str, list[tuple[str, bool]]]:
    """An expiry as (MM/YY, [(label, not card data), (value, card data)])."""
    month, year = rng.randint(1, 12), rng.randint(27, 33)
    mm, name = f"{month:02d}", MONTH_NAMES[month - 1]
    label, value = rng.choice(_EXPIRY_PHRASES)
    return f"{mm}/{year}", [(label, False), (value.format(mm=mm, yy=year, m=month, month=name, mon=name[:3]), True)]


def _typo(pan: str, rng: random.Random) -> str:
    while True:
        i = rng.randrange(len(pan))
        wrong = pan[:i] + str((int(pan[i]) + rng.randint(1, 9)) % 10) + pan[i + 1:]
        if not _passes_luhn(wrong):
            return wrong


def _number(pan: str, rng: random.Random, script: str | None = None) -> tuple[list[tuple[str, bool]], str]:
    script = script or rng.choice(_SCRIPTS)
    text, family = _layout([_render(g, script, rng) for g in _groups(pan, rng)], rng)
    return [(text, True)], family + ("" if script == "ascii" else f", {script} digits")


def _join(segments: list[tuple[str, bool]], masked: bool) -> str:
    return "".join("[REDACTED]" if is_card and masked else text for text, is_card in segments)


def _mask_case(pan: str, rng: random.Random) -> tuple[list[list[tuple[str, bool]]], dict]:
    """Returns the messages as segments, and the declared items with the family."""
    shape = rng.choice(["single"] * 6 + ["split", "split", "trickle", "trickle", "correction", "detail only"])
    case = {"pans": [pan], "codes": [], "expiries": []}
    extras: list[list[tuple[str, bool]]] = []
    if shape != "correction" and rng.random() < 0.5:
        code = _code(pan, rng)
        case["codes"].append(code)
        extras.append(_code_text(code, rng))
    if shape != "correction" and rng.random() < 0.5:
        mmyy, segments = _expiry(rng)
        case["expiries"].append(mmyy)
        extras.append(segments)
    rng.shuffle(extras)
    if shape == "detail only":
        case["pans"] = []
        if not extras:
            code = _code(None, rng)
            case["codes"].append(code)
            extras.append(_code_text(code, rng))
        message = [(rng.choice(["", "and ", "oh, ", "if you need it, ", "for the card I sent: "]), False)]
        for extra in extras:
            message += extra + [(rng.choice(["\n", ", ", " / "]), False)]
        return [message[:-1]], {**case, "note": "code or expiry alone"}
    if shape == "single":
        number, family = _number(pan, rng)
        message = [(rng.choice(_PREFIXES), False)] + number
        for extra in extras:
            message += [(rng.choice(["\n", ", ", " / ", ". ", " - ", "\t", "\n\n"]), False)] + extra
        message.append((rng.choice(_SUFFIXES), False))
        return [message], {**case, "note": family}
    if shape == "split":
        groups = _groups(pan, rng)
        while len(groups) < 2:
            groups = _groups(pan, rng)
        script = rng.choice(["ascii"] * 4 + ["words"])
        pieces = max(2, min(len(groups), rng.choice([2, 2, 3, 4])))
        cuts = sorted(rng.sample(range(1, len(groups)), pieces - 1))
        chunks = [groups[a:b] for a, b in zip([0] + cuts, cuts + [len(groups)])]
        messages = [[(rng.choice(["my card number is", "ok here goes", "typing it in parts, the app keeps sending",
                                  "number coming in bits"]), False)]] if rng.random() < 0.5 else []
        for i, chunk in enumerate(chunks):
            lead = rng.choice(["", "", "then ", "next ", "and "]) if i else rng.choice(["", "it's ", "starts "])
            messages.append([(lead, False), (" ".join(_render(g, script, rng) for g in chunk), True)])
        messages += [extra for extra in extras]
        return messages, {**case, "note": "split over messages" + ("" if script == "ascii" else ", words")}
    if shape == "trickle":
        number, family = _number(pan, rng, rng.choice(["ascii"] * 5 + ["words"]))
        messages = [[(rng.choice(_PREFIXES), False)] + number]
        if not extras:
            mmyy, segments = _expiry(rng)
            case["expiries"].append(mmyy)
            extras.append(segments)
        for extra in extras:
            bare = [segment for segment in extra if segment[1]]
            messages.append(bare if rng.random() < 0.4 else extra)
        return messages, {**case, "note": "details one per message"}
    wrong = _typo(pan, rng)
    first, _ = _number(wrong, rng, "ascii")
    second, _ = _number(pan, rng, "ascii")
    return [[(rng.choice(["card ", "", "it's "]), False)] + first,
            [(rng.choice(["sorry, typo: ", "no wait, it's ", "correction: ", "ugh, I mean "]), False)] + second], \
        {**case, "note": "correction over messages"}


# ------------------------------------------------------------------------------------------- what must be kept

_CUES = ["For verification", "For security purposes", "Security check", "Verification details", "For the security question",
         "Card verification", "To verify me", "Security"]
_CUE_SENTENCES = ["I want my money back.", "Please reverse the charge.", "The front of my card is scratched.",
                  "My verification text never came.", "Do you need my security code?", "The back of the card is peeling."]


def _l4(rng):
    return f"{rng.randint(0, 9999):04d}"


def _zip(rng):
    return f"{rng.randint(1001, 99950):05d}"


def _not_card(make, rng):
    while True:
        value = make(rng)
        if not _card_like(value):
            return value


def _reference(rng: random.Random) -> str:
    digits = lambda n: "".join(str(rng.randint(0, 9)) for _ in range(n))
    kind = rng.randrange(10)
    if kind == 0:
        return f"Amazon order {rng.randint(111, 114)}-{digits(7)}-{digits(7)}"
    if kind == 1:
        rest = digits(18)
        return "USPS tracking 9400 " + " ".join([rest[i:i + 4] for i in range(0, 16, 4)] + [rest[16:]])
    if kind == 2:
        return f"FedEx tracking {digits(4)} {digits(4)} {digits(4)}"
    if kind == 3:
        return "UPS tracking 1Z" + "".join(rng.choice("0123456789ABCDEFGHJKLMNPRSTUVWXYZ") for _ in range(16))
    if kind == 4:
        return f"ticket number 0{digits(2)} {digits(10)}"
    if kind == 5:
        return f"the ARN is {digits(23)}"
    if kind == 6:
        return f"booking confirmation {digits(4)}.{digits(3)}.{digits(3)}"
    if kind == 7:
        return f"order {digits(10)}"
    if kind == 8:
        return f"cancellation number {digits(4)}-{digits(4)}"
    return f"cancellation ref 2026-{rng.randint(1, 12):02d}{rng.randint(1, 28):02d}-{digits(4)}"


def _amount(rng: random.Random) -> str:
    whole, cents = rng.randint(1, 2400), rng.randint(0, 99)
    return rng.choice([f"${whole}.{cents:02d}", f"€{whole},{cents:02d}", f"£{whole}", f"USD {whole}.{cents:02d}",
                       f"{whole}.{cents:02d} EUR", f"charged {rng.randint(100, 999)} for the renewal", f"paid {whole}.{cents:02d} at the hotel",
                       f"{whole:,}.{cents:02d} instead of {whole // 10}.{cents:02d}", f"{whole} dollars"])


def _date(rng: random.Random) -> str:
    m, d = rng.randint(1, 12), rng.randint(1, 28)
    return rng.choice([f"on {m:02d}/{d:02d}/2026", f"on 2026-{m:02d}-{d:02d}", f"on {MONTH_NAMES[m - 1][:3]} {d}",
                       f"on {d} {MONTH_NAMES[m - 1]}", f"on {d:02d}.{m:02d}.2026", f"at {rng.randint(1, 12)}:{rng.randint(0, 59):02d} pm",
                       f"at {rng.randint(0, 23):02d}:{rng.randint(0, 59):02d}", f"between {m}/{d} and {m}/{d + 1}",
                       f"posted {m:02d}/{d:02d}/26"])


def _phone(rng: random.Random) -> str:
    n = lambda k: "".join(str(rng.randint(0, 9)) for _ in range(k))
    return rng.choice([f"call me on ({rng.randint(201, 989)}) 555-{n(4)}", f"text me at {rng.randint(201, 989)}-555-{n(4)}",
                       f"my number is +1 {rng.randint(201, 989)} 555 {n(4)}", f"the merchant's line is 1-800-555-{n(4)}",
                       f"my UK mobile is +44 7700 {n(6)}", f"landline 020 7946 {n(4)}", f"reach me on +91 9{n(4)} {n(5)}"])


def _ident(rng: random.Random) -> str:
    return rng.choice([f"case C-{rng.randint(5001, 5999)}", f"transaction T-{rng.randint(1001, 4999)}",
                       f"ref CN-{rng.randint(10000, 99999)}", f"Re: C{rng.randint(5001, 5999)}"])


def _labelled(rng: random.Random) -> str:
    return rng.choice([f"room {rng.randint(101, 989)}", f"ext {rng.randint(200, 899)}", f"store #{rng.randint(100, 999)}",
                       f"gate {rng.randint(1, 60)}", f"flight TP {rng.randint(1000, 1999)}"])


def _everyday_cue(rng: random.Random) -> str:
    m, d = rng.randint(1, 12), rng.randint(1, 28)
    return rng.choice([f"Amazon says exp. delivery {m}/{d} for the replacement", f"my travel notice expiration should be {m}/{d}",
                       f"the hotel took a security deposit of ${rng.randint(100, 900)}", f"I got ${rng.randint(5, 90)} back on {m:02d}/{d:02d}",
                       f"the front desk said to call {rng.randint(201, 989)}-555-{rng.randint(1000, 9999)}"])


def _keep_case(rng: random.Random) -> tuple[list[str], str]:
    family = rng.choice(["cue words", "cue words", "amounts", "dates and times", "phone numbers", "references", "references",
                         "ids", "several numbers", "labelled numbers", "everyday cue words", "typed in turn", "typed in turn",
                         "after card talk"])
    if family == "cue words":
        l4, z = _l4(rng), _zip(rng)
        return [rng.choice([f"{rng.choice(_CUES)}: last four {l4}, ZIP {z}.", f"{rng.choice(_CUES)} - card ending {l4}, billing zip {z}",
                            f"My last 4 are {l4} and my ZIP is {z}. {rng.choice(_CUE_SENTENCES)}",
                            f"{rng.choice(_CUE_SENTENCES)} Card ending {l4}, ZIP {z}."])], family
    if family == "several numbers":
        makers = [_amount, _date, _phone, _ident, _reference, lambda r: f"card ending {_l4(r)}", lambda r: f"ZIP {_zip(r)}"]
        join = lambda r: r.choice([", ", "; ", " and "]).join(r.choice(makers)(r) for _ in range(r.randint(2, 4)))
        return [_not_card(join, rng)], family
    if family == "typed in turn":
        if rng.random() < 0.5:
            guesses = [_l4(rng) for _ in range(4)]
        else:  # three wrong guesses and the real last four that complete a Luhn-valid 16-digit number across messages
            stem = "".join(_l4(rng) for _ in range(3)) + f"{rng.randint(0, 999):03d}"
            full = stem + next(str(d) for d in range(10) if _passes_luhn(stem + str(d)))
            guesses = [full[i:i + 4] for i in range(0, 16, 4)]
            family = "typed in turn, Luhn by chance"
        lines = [rng.choice(["is it card ending {}?", "try {}", "or maybe {}", "hmm, {}?", "sorry, {} then"]).format(g) for g in guesses[:3]]
        last = rng.choice(["found it: card ending {}, ZIP {}", "it's {} and ZIP {}", "ok, last four {}, zip {}"])
        return lines + [last.format(guesses[3], _zip(rng))], family
    if family == "after card talk":
        l4, z = _l4(rng), _zip(rng)
        first = rng.choice(["I almost pasted my whole card number, sorry!", "here's my card: [REDACTED CARD NUMBER]",
                            "do you need the full card number?", "I won't type my card number in here."])
        return [first, rng.choice([f"Last four is {l4} and ZIP {z}, that's enough right?", f"ok just the last four then: {l4}, ZIP {z}",
                                   f"card ending {l4}, billing ZIP {z}"])], family
    make = {"amounts": _amount, "dates and times": _date, "phone numbers": _phone, "references": _reference, "ids": _ident,
            "labelled numbers": _labelled, "everyday cue words": _everyday_cue}[family]
    lead = rng.choice(["", "Hi, ", "Quick question: ", "For the dispute, "])
    tail = rng.choice(["", ", can you check?", " - please help", ", thanks"])
    return [_not_card(lambda r: lead + make(r) + tail, rng)], family


# ------------------------------------------------------------------------------------------- the corpus


def generate(seed: int = 4, size: int = 600) -> list[dict]:
    """`size` cases, half "mask" (the eight test numbers in turn) and half "keep", deterministic for `seed`."""
    rng = random.Random(seed)
    cases = []
    while len(cases) < size // 2:
        pan = PANS[len(cases) % len(PANS)]
        segments, case = _mask_case(pan, rng)
        messages = [_join(m, masked=False) for m in segments]
        ideal = "\n".join(_join(m, masked=True) for m in segments)
        declared = len(case["pans"]) + len(case["codes"]) + len(case["expiries"])
        if len(_visible(case, "\n".join(messages))) != declared or _visible(case, ideal):
            continue  # the oracle cannot see it, or the context spells a declared item by accident: draw again
        cases.append({"messages": messages, "expect": "mask", "pans": case["pans"], "codes": case["codes"],
                      "expiries": case["expiries"], "note": case["note"]})
    while len(cases) < size:
        messages, family = _keep_case(rng)
        if any(_card_like(m) for m in messages):
            continue
        cases.append({"messages": messages, "expect": "keep", "pans": [], "codes": [], "expiries": [], "note": family})
    return cases
