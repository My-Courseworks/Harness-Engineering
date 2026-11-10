"""Card-data masking by normalisation, tokens and the card number's own structure, not by listing formats.

Round 4 rewrote the search. Round 3 chained digit groups and ended a chain at a newline, a sentence end or more
than two words, so a number pasted one group per line, or dictated ("the first four are 5555, the next four
are ..."), was never one candidate. Now nothing between two groups ends the search. A card number is found by what
it is, wherever its pieces sit in the message (or in the last three customer messages):

1. Normalise: NFKC (full-width digits, non-breaking and narrow spaces), every Unicode decimal digit to ASCII
   (Arabic-Indic, Devanagari ...), every dash to "-", zero-width characters and soft hyphens dropped.
2. Tokenise into digit runs, words and symbols. Spoken numbers become numeric tokens too: "five" 5, "oh" 0,
   "fifteen" 15, "fifty" 50, "fifty-five" 55, "double five" 55; spoken tokens next to each other merge into one
   group ("five five five five", "fifty-five fifty-five"). A lone number word that counts something ("the first
   FOUR are", "three digits") is a count, not a digit.
3. Give a role to every numeric token that is not card data: an identifier (touching letters: C-5001, CN-77812), an
   amount (a currency sign, a unit word, decimals), a clock time, a date (ISO, numeric with a year, a month name
   with a day), a phone number, a ZIP (after "zip" / "postal code"), a last four (after "ending", "ends in", "last
   four ..."), a year after "since" or "in". Role-less tokens are candidates.
4. Group candidates into runs: tokens joined only by separators on one line ("4111 1111 1111 1111", "4111-1111").
   A card number is a sequence of runs (one run, or several separated by anything at all: newlines, list markers,
   sentences, words) whose digits number 13-19, start with a card network's prefix (2221-2720, 3[0,4-9], 4, 5, 6),
   pass Luhn, and are grouped like a card when they span several runs (4s with a shorter last group, Amex 4-6-5,
   Diners 4-6-4, or spoken). The first run may be entered at any of its tokens (a code, PIN, expiry or order number
   typed just before the number: "CVV: 737 5555 5555 5555 4444", "order 12345, 5555 5555 5555 4444"), the last
   is used whole or cut after any token (a code may follow on the same line). One run with a card prefix and card
   grouping is masked even when Luhn fails: a mistyped card. A run after a reference label ("order", "tracking") is
   that reference, except a complete card number ending it (the round-4 review's "Order 12345 5555 5555 5555 4444").
5. Across messages: a sequence that ends in this message and starts in one of the last three customer messages is
   masked here, and the earlier stored message is rewritten too (`mask_customer_message` returns the rewrite), so
   the opening half of a number sent in two messages does not stay behind. One exemption, measured and listed: when
   every piece is a last-four- or ZIP-sized group (at most 5 digits per message), one message reads as a step-up
   answer and none says "card number", the pieces are taken for verification answers that pass Luhn by chance. The
   rest of a number whose last four was already given ("card ending 4444" ... "the first twelve: 5555 5555 5555") is
   masked when it completes that last four into a card number.
6. Codes and expiries. In a message that carries card data (a number found in it, or masked in one of the last
   two messages), every remaining bare candidate of 3-4 digits is the security code and every month/year pair or
   month name with a year is the expiry. Elsewhere a code is masked only after a cue phrase ("cvv", "security
   code", "code on the back", "3 digits on the reverse" ...), and an expiry only after "exp", "expiry",
   "valid thru"... A last four or a ZIP is never a code, whatever words surround it ("For verification: my last
   four are 6610" stays as typed).

`mask_customer_message` is the full rule set, for customer input (and the model's reasoning, which nobody reads).
`mask_card_numbers` is step 4 only, for text the model or the harness writes for people (replies, notes,
reflections), so case ids, dates and amounts in generated text are never touched.
"""

import re
import unicodedata
from collections import Counter

CARD_NUMBER_MASK = "[REDACTED CARD NUMBER]"
SECURITY_CODE_MASK = "[REDACTED SECURITY CODE]"
EXPIRY_MASK = "[REDACTED EXPIRY]"
CARD_DIGITS_MASK = "[REDACTED CARD DIGITS]"
MASK_TOKEN = re.compile(r"\[REDACTED [A-Z \-]+\]")
ONE_TIME_CODE_MASK = "[REDACTED ONE-TIME CODE]"

_DROP = dict.fromkeys(map(ord, "​‌‍⁠﻿­"), None)
_UNITS = {"zero": "0", "oh": "0", "one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7",
          "eight": "8", "nine": "9"}
_TEENS = {"ten": "10", "eleven": "11", "twelve": "12", "thirteen": "13", "fourteen": "14", "fifteen": "15", "sixteen": "16",
          "seventeen": "17", "eighteen": "18", "nineteen": "19"}
_TENS = {"twenty": "2", "thirty": "3", "forty": "4", "fourty": "4", "fifty": "5", "sixty": "6", "seventy": "7", "eighty": "8",
         "ninety": "9"}
_COUNTED = {"are", "is", "digits", "digit", "numbers", "number", "of", "more", "groups", "blocks"}
_COUNTERS = {"first", "next", "last", "final", "other", "the", "those", "these", "all"}
_UNIT_WORDS = {"dollar", "dollars", "usd", "euro", "euros", "eur", "cents", "bucks", "percent", "%", "days", "day", "months", "month",
               "years", "year", "minutes", "hours", "gb", "tb", "mb", "times", "items", "pounds", "gbp", "yen"}
_CURRENCY = set("$€£¥")
_MONTHS = r"(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*"
_MONTH = re.compile(_MONTHS + r"$", re.IGNORECASE)
_LAST_FOUR_CUE = re.compile(r"(ending|ends|ended)(\s+(in|with|on))?\W*$|last\s*(4|four)(\s+digits?)?(\s+of\s+(my|the)\s+card)?"
                            r"(\s+(are|is|were|was))?\W*$|last\s+digits(\s+(are|is))?\W*$", re.IGNORECASE)
# "ok just the last four then: 4689", "you only need the last four? It's 4427": the cue may sit a few words before the number
_LAST_FOUR_LOOSE = re.compile(r"\b(last\s*(4|four)(\s+digits?)?|ending(\s+(in|with))?|ends\s+(in|with))\b(?P<tail>[^\d\n]{0,25})$", re.IGNORECASE)
# a number after one of these labels is that kind of reference, unless it is itself a valid card number
_REFERENCE_CUE = re.compile(r"\b(tracking|order|booking|reference|ref|confirmation|invoice|ticket|receipt|claim|serial|parcel|shipment)"
                            r"(\s+(number|no\.?|num|id|code|#))?\s*[:#]?\s*$", re.IGNORECASE)
_CARD_CUE = re.compile(r"\b(card\s*(number|no\.?|num|#|:)|card\s+is|number\s+is|the\s+number|my\s+card\s+(number|is)|cc|visa|mastercard|"
                       r"amex|discover|digits\s+are)\b", re.IGNORECASE)
# an expiry cue about something other than the card ("exp. delivery 11/24", "travel notice expiration 12/10")
_NOT_CARD_EXPIRY = re.compile(r"\b(notice|subscription|delivery|deliver|membership|trial|offer|warranty|passport|licen[cs]e|plan|contract|"
                              r"lease|insurance|coupon|voucher|domain|prescription|visa\s+application|reservation|booking)\b", re.IGNORECASE)
# a message answering the step-up: a last four with its usual words, or a ZIP
_VERIFICATION_ANSWER = re.compile(r"\b(zip|zip\s*code|postal\s*code|postcode|card\s+ending|ending\s+in|last\s*(4|four))\b[^\d\n]{0,25}\d",
                                  re.IGNORECASE)
_ZIP_CUE = re.compile(r"\b(zip|zip\s*code|postal\s*code|post\s*code|postcode)(\s+(is|was|=))?\W*$", re.IGNORECASE)
_YEAR_CUE = re.compile(r"\b(since|in|year|from|of|until|till|by)\W*$", re.IGNORECASE)
_PHONE_CUE = re.compile(r"\b(call|phone|tel|telephone|mobile|cell|text me|whatsapp)\b[^.\n]{0,20}$", re.IGNORECASE)
_CODE_CUE = re.compile(
    r"\b(cvv2?|cvc2?|cid|csc|cvn|security\s+(code|number|digits)|card\s+code|verification\s+(code|value|number)|"
    r"(code|number|digits?)\s+(on|at|from)\s+(the\s+)?(back|reverse|front)|(on|at)\s+the\s+(back|reverse)(\s+of\s+(my|the)\s+card)?|"
    r"back\s+of\s+(my|the)?\s*card|signature\s+(strip|panel|box|line)|(by|next\s+to|beside|near|on|at)\s+the\s+signature|"
    r"(three|3|four|4)[\s-]+(digits?|numbers?)(\s+code)?)\b", re.IGNORECASE)
_DATE_WORD_BEFORE = re.compile(r"\b(on|charged|since|dated|posted|from|until|billed|bought|paid|lost|stolen|missing|around|before|after|by)\W+(the\W+)?$",
                               re.IGNORECASE)
_WEAK_CODE_CUE = re.compile(r"\bcode\b", re.IGNORECASE)  # "my code is 737": for 3 digits only
_EXPIRY_CUE = re.compile(r"\b(exp|expiry|expiration|exp\.?\s*date|valid\s+(thru|through|until|till)|good\s+(thru|through)|"
                         r"(card|it)\s+expires)\b", re.IGNORECASE)
# after a card number, these words introduce its code or its expiry, never more of the number ("…1111, cvv 1 8 1")
_AFTER_NUMBER_CUE = re.compile(r"\b(cvv2?|cvc2?|cid|csc|cvn|security\s+(code|number|digits)|verification\s+(code|value|number)|"
                               r"exp|expiry|expiration|expires)\b", re.IGNORECASE)
_BARE_EXPIRY_CUE = re.compile(r"\b(expires|expiring|expired)\b", re.IGNORECASE)
_CARD_SUBJECTS = {"card", "it", "that", "which", "this", "one", "and", "but", "also", "visa", "mastercard", "amex"}
_TOKEN = re.compile(r"\d+|[^\W\d_]+|\S")


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).translate(_DROP)
    chars = []
    for ch in text:
        if ch in "\n\r":
            chars.append(ch)
        elif ch.isspace():
            chars.append(" ")
        elif ch.isdecimal() and not ch.isascii():
            chars.append(str(unicodedata.decimal(ch)))
        elif unicodedata.category(ch) == "Pd" or ch == "−":
            chars.append("-")
        else:
            chars.append(ch)
    return "".join(chars)


# --------------------------------------------------------------------------- tokens


def _raw_tokens(text: str) -> list[dict]:
    out = []
    for match in _TOKEN.finditer(text):
        value = match.group()
        kind = "digits" if value.isdigit() else "word" if value[0].isalpha() else "symbol"
        out.append({"text": value, "start": match.start(), "end": match.end(), "kind": kind,
                    "digits": value if kind == "digits" else None, "spoken": False, "role": None})
    return out


def _spoken_value(tokens: list[dict], i: int) -> tuple[str, int] | None:
    """(digits, index of the last token used) if a spoken number starts at tokens[i]."""
    word = tokens[i]["text"].lower()
    nxt = tokens[i + 1] if i + 1 < len(tokens) else None
    nxt2 = tokens[i + 2] if i + 2 < len(tokens) else None
    if word in _TENS:
        if nxt and nxt["kind"] == "word" and nxt["text"].lower() in _UNITS and nxt["text"].lower() not in ("zero", "oh") \
                and nxt["start"] - tokens[i]["end"] <= 1:
            return _TENS[word] + _UNITS[nxt["text"].lower()], i + 1
        if nxt and nxt["text"] == "-" and nxt2 and nxt2["kind"] == "word" and nxt2["text"].lower() in _UNITS \
                and nxt2["text"].lower() not in ("zero", "oh") and nxt2["start"] - tokens[i]["end"] <= 2:
            return _TENS[word] + _UNITS[nxt2["text"].lower()], i + 2
        return _TENS[word] + "0", i
    if word in _TEENS:
        return _TEENS[word], i
    if word in _UNITS:
        return _UNITS[word], i
    if word in ("double", "triple") and nxt and (nxt["kind"] == "digits" and len(nxt["text"]) == 1
                                                 or nxt["kind"] == "word" and nxt["text"].lower() in _UNITS):
        digit = nxt["text"] if nxt["kind"] == "digits" else _UNITS[nxt["text"].lower()]
        return digit * (2 if word == "double" else 3), i + 1
    return None


def _tokens(text: str) -> list[dict]:
    """Digit tokens, plus spoken numbers merged into groups; every other token keeps its kind."""
    raw = _raw_tokens(text)
    markers = [m.span() for m in MASK_TOKEN.finditer(text)]  # "ONE" in [REDACTED ONE-TIME CODE] is not the digit one
    in_marker = lambda token: any(start <= token["start"] and token["end"] <= end for start, end in markers)
    out, i = [], 0
    while i < len(raw):
        token = raw[i]
        spoken = _spoken_value(raw, i) if token["kind"] == "word" and not in_marker(token) else None
        if spoken:
            digits, last = spoken
            out.append({"text": text[token["start"]:raw[last]["end"]], "start": token["start"], "end": raw[last]["end"], "kind": "digits",
                        "digits": digits, "spoken": True, "role": None, "words": last - i + 1, "single_word": last == i})
            i = last + 1
        else:
            out.append(token)
            i += 1
    # a lone spoken number that counts something is not a digit: "the first four are", "three digits on the back", "the
    # first twelve:" (one word: a unit, a teen or a ten; "fifty-five" and "double five" are never counts)
    counts = []
    for j, token in enumerate(out):
        if token["spoken"] and token.get("single_word") and (len(token["digits"]) == 1 or token["text"].lower() in _TEENS
                                                               or token["text"].lower() in _TENS):
            prev = out[j - 1]["text"].lower() if j else ""
            nxt = out[j + 1]["text"].lower() if j + 1 < len(out) else ""
            in_sequence = (j and out[j - 1]["spoken"]) or (j + 1 < len(out) and out[j + 1]["spoken"])
            if not in_sequence and (prev in _COUNTERS or nxt in _COUNTED
                                    or (nxt == "-" and j + 2 < len(out) and out[j + 2]["text"].lower() in _COUNTED)):
                counts.append(token)
    for token in counts:
        token.update(kind="word", digits=None, spoken=False)
    # merge spoken tokens that follow each other with only spaces, commas or hyphens between
    merged: list[dict] = []
    for token in out:
        if token["spoken"] and merged and merged[-1]["spoken"] and re.fullmatch(r"[ ,\-]*", text[merged[-1]["end"]:token["start"]]):
            merged[-1].update(end=token["end"], digits=merged[-1]["digits"] + token["digits"], text=text[merged[-1]["start"]:token["end"]])
        else:
            merged.append(dict(token))
    # "oh" alone is an interjection, not a zero
    for token in merged:
        if token["spoken"] and token["digits"] == "0" and token["text"].lower() == "oh":
            token.update(kind="word", digits=None, spoken=False)
    _classify(merged, text)
    _classify_list_markers(merged, text)
    _release_card_groups(merged, text)
    return merged


def _classify_list_markers(tokens: list[dict], text: str) -> None:
    """The numerals that number a list are not digits of anything: "3. …", "4) …", "(5) …", "6: …", three or more of them
    counting up by one. Read with the numbers inside the items, the numerals of a checklist made card numbers by chance:
    a reply lost its lines 3 to 14 in round 6's blind held-out run, and 74 of 150 generated lists were damaged
    (`fuzz-v2`, "a numbered list whose items hold other numbers"). A card number typed as a numbered list ("1. 5555 /
    2. 5555 / …") keeps its groups: only the numerals and the items' own small numbers go (_mark_list)."""
    shaped = [t for t in tokens if t["digits"] is not None and not t["spoken"] and t["role"] is None and len(t["digits"]) <= 2
              and (t["start"] == 0 or text[t["start"] - 1] in " \t\n\r(*-")
              and re.match(r"[.):]\s|\)\s", text[t["end"]:t["end"] + 2])]
    chain: list[dict] = []
    for t in [*shaped, None]:
        if t is not None and chain and int(t["digits"]) == int(chain[-1]["digits"]) + 1:
            chain.append(t)
            continue
        if len(chain) >= 3:
            _mark_list(chain, tokens, text)
        chain = [t] if t is not None else []


def _mark_list(chain: list[dict], tokens: list[dict], text: str) -> None:
    """The numerals of one list, and the small numbers inside its items. In an item that has words, a one- or two-digit
    number is that item's own ("7. Carry 3 adapters", "12. Book 30 nights"): with the numerals gone, the quantities of
    a long checklist still chained into a card number in 5 of 150 generated lists. A card number dictated as a list
    keeps its groups, which are three digits or more."""
    one_per_line = "\n" in text[chain[0]["end"]:chain[1]["start"]]
    for k, marker in enumerate(chain):
        marker["role"] = "list_marker"
        if k + 1 < len(chain):
            end = chain[k + 1]["start"]
        else:
            line_end = text.find("\n", marker["end"])
            end = line_end if one_per_line and line_end != -1 else len(text)
        if re.search(r"[^\W\d_]", text[marker["end"]:end]):
            for t in tokens:
                if marker["end"] <= t["start"] < end and t["digits"] is not None and not t["spoken"] and t["role"] is None and len(t["digits"]) <= 2:
                    t["role"] = "list_item_number"


# roles that are a reading of one token by its neighbours ("a year after a month and a day", "an identifier glued to a
# word", "an amount before 'days'"): a complete card number is a stronger reading of the same digits and wins
_SOFT_ROLES = {"identifier", "amount", "time", "date", "year", "phone", "month_year"}


def _release_card_groups(tokens: list[dict], text: str) -> None:
    """A complete card number wins over a role. "exp Dec 29 5555 5555 5555 4444" gave the first 5555 the role of a year,
    "Visa-4111 1111 1111 1111" made 4111 an identifier, "... 4444 days ago" made 4444 an amount; each took a group out
    of the number and left twelve digits that are no card (the round-5 review's 2.4). Here, written tokens joined by
    separators only are read once more without their roles: a window of them that is 13-19 digits, starts with a card
    network's prefix, passes Luhn and is grouped like a card is a card, and any soft role inside it is dropped. A
    reference after a label keeps its own rule (_classify_references), a last four and a ZIP are never soft."""
    written = [t for t in tokens if t["digits"] is not None and not t["spoken"]]
    run: list[dict] = []
    for t in [*written, None]:
        joined = t is not None and run and t["start"] - run[-1]["end"] <= 3 and not re.search(r"[^\W\d_]|\n|\r", text[run[-1]["end"]:t["start"]])
        if joined:
            run.append(t)
            continue
        for i in range(len(run)):
            for j in range(len(run), i, -1):
                window = run[i:j]
                if not any(x["role"] in _SOFT_ROLES for x in window) or any(x["role"] not in _SOFT_ROLES and x["role"] is not None for x in window):
                    continue
                digits = _digits(window)
                if 13 <= len(digits) <= 19 and _card_prefix(digits) and _passes_luhn(digits) \
                        and _card_grouping([len(x["digits"]) for x in window], False, digits):
                    for x in window:
                        x["role"] = None
                    break
        run = [t] if t is not None else []


def _before(text: str, token: dict, width: int = 40) -> str:
    return text[max(0, token["start"] - width):token["start"]]


def _classify(tokens: list[dict], text: str) -> None:
    """Roles for numeric tokens that are never card data."""
    numeric = [t for t in tokens if t["digits"] is not None]
    for i, t in enumerate(tokens):
        if t["digits"] is None or t["role"]:
            continue
        prev = tokens[i - 1] if i else None
        nxt = tokens[i + 1] if i + 1 < len(tokens) else None
        nxt2 = tokens[i + 2] if i + 2 < len(tokens) else None
        letters = lambda tok: tok is not None and tok["kind"] == "word"
        touching = lambda a, b: a is not None and b is not None and a["end"] == b["start"]
        before = _before(text, t)
        joined_next = nxt is not None and ((nxt["digits"] is not None and nxt["start"] - t["end"] <= 3)
                                           or (nxt["text"] in "-/.|;:" and nxt2 is not None and nxt2["digits"] is not None
                                               and nxt2["start"] - t["end"] <= 3))
        if not t["spoken"] and (touching(prev, t) and letters(prev) or touching(t, nxt) and letters(nxt)
                                or (prev and prev["text"] == "-" and touching(prev, t) and i > 1 and letters(tokens[i - 2])
                                    and touching(tokens[i - 2], prev))):
            t["role"] = "identifier"  # C-5001, CN-77812, A1B2, 5001A
        elif prev and prev["text"] in _CURRENCY and t["start"] - prev["end"] <= 1:
            t["role"] = "amount"
        elif nxt and nxt["text"].lower() in _UNIT_WORDS:
            t["role"] = "amount"
        elif not t["spoken"] and nxt and nxt["text"] in ".," and touching(t, nxt) and nxt2 and nxt2["kind"] == "digits" \
                and touching(nxt, nxt2) and (nxt["text"] == "." and len(nxt2["text"]) == 2 or nxt["text"] == "," and len(nxt2["text"]) == 3) \
                and not re.search(r"\d[^\w\n]{0,3}$", text[max(0, t["start"] - 4):t["start"]]) \
                and not re.match(r"[^\w\n]{0,3}(\d|(zero|oh|one|two|three|four|five|six|seven|eight|nine)\b)", text[nxt2["end"]:nxt2["end"] + 12],
                                 re.IGNORECASE):  # "5555,5555,44.44" and "55.55 five five five five" are no amounts
            t["role"] = "amount"  # 15.99, 1,299
            j = i + 2
            while j < len(tokens) and tokens[j]["kind"] == "digits" and touching(tokens[j - 1], tokens[j]):
                tokens[j]["role"] = "amount"
                if j + 2 < len(tokens) and tokens[j + 1]["text"] in ".," and touching(tokens[j], tokens[j + 1]) \
                        and tokens[j + 2]["kind"] == "digits" and touching(tokens[j + 1], tokens[j + 2]):
                    j += 2
                else:
                    break
        elif not t["spoken"] and nxt and nxt["text"] == ":" and touching(t, nxt) and nxt2 and nxt2["kind"] == "digits" and touching(nxt, nxt2) \
                and len(t["text"]) <= 2 and len(nxt2["text"]) == 2:
            t["role"] = nxt2["role"] = "time"
        elif nxt and nxt["text"].lower() in ("am", "pm", "a.m", "p.m") and len(t["digits"]) <= 4:
            t["role"] = "time"
        elif _ZIP_CUE.search(before) and len(t["digits"]) in (5, 9) and not joined_next:
            t["role"] = "zip"
        elif len(t["digits"]) == 4 and not joined_next and (_LAST_FOUR_CUE.search(before) or _last_four_loose(before)):
            t["role"] = "last4"
            # "my last four is 4427/5127": an alternative right after it is a last four too
            if nxt and nxt["text"] in ("/", ",") and nxt2 and nxt2["digits"] and len(nxt2["digits"]) == 4 and nxt2["start"] - t["end"] <= 3:
                nxt2["role"] = "last4"
        elif len(t["digits"]) == 4 and t["digits"][:2] in ("19", "20") and _YEAR_CUE.search(_before(text, t, 12)):
            t["role"] = "year"
    _classify_dates(tokens, text)
    _classify_phones(tokens, text)
    _classify_references(tokens, text)


def _last_four_loose(before: str) -> bool:
    match = _LAST_FOUR_LOOSE.search(before)
    return bool(match) and len(re.findall(r"[^\W\d_]+", match.group("tail"))) <= 3


def _classify_references(tokens: list[dict], text: str) -> None:
    """A run of digits right after "tracking", "order #", "booking ref" ... is that reference, unless the run is itself a
    valid card number, or a complete card number ends it ("Order 12345 5555 5555 5555 4444": the order number is the
    reference, the card is a card). A label never hides a card. A long reference whose tail happens to pass Luhn
    ("tracking 9400 1234 5678 9012 3456 78") is one number: its tail is not grouped like a whole card."""
    for i, t in enumerate(tokens):
        if t["digits"] is None or t["role"] or t["spoken"] or not _REFERENCE_CUE.search(_before(text, t, 30)):
            continue
        run = [t]
        for nxt in tokens[i + 1:]:
            if nxt["digits"] is not None and not nxt["spoken"] and nxt["role"] is None and nxt["start"] - run[-1]["end"] <= 3 \
                    and not re.search(r"[^\W\d_]|\n|[,;:]\s", text[run[-1]["end"]:nxt["start"]]):
                run.append(nxt)  # "ticket 1042, 4111 ...", "Booking 2291: 4242 ...": the label ends at the punctuation
            elif nxt["digits"] is None and nxt["kind"] == "symbol" and nxt["start"] - run[-1]["end"] <= 1:
                continue
            else:
                break
        card_from = next((k for k in range(len(run)) if _card_after_label(run, k)), None)
        for x in run[:card_from]:
            x["role"] = "reference"


def _classify_dates(tokens: list[dict], text: str) -> None:
    for i, t in enumerate(tokens):
        if t["digits"] is None or t["spoken"]:
            continue
        window = tokens[i:i + 5]
        # ISO dates
        if len(window) == 5 and len(t["text"]) == 4 and t["text"][:2] in ("19", "20") and window[1]["text"] == "-" and window[3]["text"] == "-" \
                and window[2]["kind"] == window[4]["kind"] == "digits" and window[4]["end"] - t["start"] == 10 \
                and 1 <= int(window[2]["text"]) <= 12 and 1 <= int(window[4]["text"]) <= 31:
            for w in (t, window[2], window[4]):
                w["role"] = "date"
        # D/M/YYYY, M/D/YYYY, D.M.YYYY: a numeric date with a four-digit year
        if len(window) == 5 and len(t["text"]) <= 2 and window[1]["text"] in "/." and window[3]["text"] == window[1]["text"] \
                and window[2]["kind"] == window[4]["kind"] == "digits" and len(window[2]["text"]) <= 2 and len(window[4]["text"]) == 4 \
                and window[4]["end"] - t["start"] <= 10:
            for w in (t, window[2], window[4]):
                w["role"] = "date"
    for i, t in enumerate(tokens):
        if t["kind"] != "word" or not _MONTH.match(t["text"]):
            continue
        # a month name with a day and/or a year: "Nov 3", "November 3rd 2026", "3 Nov", "Dec 2029" (a month/year pair)
        nums = [x for x in tokens[i + 1:i + 4] if x["digits"] is not None and x["start"] - t["end"] <= 12
                and "\n" not in text[t["end"]:x["start"]]]
        if nums and len(nums[0]["digits"]) == 2 and not nums[0]["spoken"] and nums[0]["role"] is None \
                and re.fullmatch(r"\s*['’]", text[t["end"]:nums[0]["start"]]):
            nums[0]["role"] = "month_year"  # "January '27": an apostrophe marks a year, never a day of the month
        elif nums and len(nums[0]["digits"]) <= 2 and int(nums[0]["digits"]) <= 31 and not nums[0]["spoken"] and nums[0]["role"] is None:
            nums[0]["role"] = "date"
            if len(nums) > 1 and len(nums[1]["digits"]) == 4 and nums[1]["role"] is None and nums[1]["start"] - nums[0]["end"] <= 3:
                nums[1]["role"] = "date"
        elif nums and len(nums[0]["digits"]) in (2, 4) and nums[0]["role"] is None and (nums[0]["digits"][:2] in ("19", "20") or nums[0]["spoken"]):
            nums[0]["role"] = "month_year"
        if i and tokens[i - 1]["digits"] and not tokens[i - 1]["spoken"] and len(tokens[i - 1]["digits"]) <= 2 and tokens[i - 1]["role"] is None \
                and text[tokens[i - 1]["end"]:t["start"]] == " ":
            tokens[i - 1]["role"] = "date"  # "3 Nov"
            if nums and len(nums[0]["digits"]) == 4 and nums[0]["role"] in (None, "month_year"):
                nums[0]["role"] = "date"
    # month/year pairs: 12/29, 12-29, 12/2029, 12 / 29 (dates unless the message carries card data or says "exp")
    for i, t in enumerate(tokens):
        if t["digits"] is None or t["role"] or i + 2 >= len(tokens):
            continue
        sep, year = tokens[i + 1], tokens[i + 2]
        if sep["text"] in ("/", "-", ".") and year["digits"] and year["role"] is None and len(t["digits"]) <= 2 \
                and 1 <= int(t["digits"]) <= 12 and len(year["digits"]) in (2, 4) and sep["start"] - t["end"] <= 1 and year["start"] - sep["end"] <= 1 \
                and (len(year["digits"]) == 2 or year["digits"][:2] == "20") \
                and not (i + 4 < len(tokens) and tokens[i + 3]["text"] in ("/", "-") and tokens[i + 3]["start"] == year["end"]
                         and tokens[i + 4]["digits"] and tokens[i + 4]["start"] == tokens[i + 3]["end"]):
            t["role"] = year["role"] = "month_pair"


def _classify_phones(tokens: list[dict], text: str) -> None:
    """+1 415 555 0100, (415) 555-0100, 415.555.0100, +44 20 7946 0958, or a number after "call me on"."""
    for match in re.finditer(r"(\+\d{1,3}[ .\-]?)?(\(\d{2,4}\)|\d{2,4})([ .\-]\d{2,4}){1,3}", text):
        digits = re.sub(r"\D", "", match.group())
        plus = match.group().startswith("+")
        paren = "(" in match.group()
        cue = _PHONE_CUE.search(text[max(0, match.start() - 40):match.start()])
        shaped = re.fullmatch(r"(\(\d{3}\)|\d{3})[ .\-]\d{3}[ .\-]\d{4}", match.group().strip())
        if (plus or paren or cue or shaped) and 9 <= len(digits) <= 13:
            for t in tokens:
                if t["digits"] and t["start"] >= match.start() and t["end"] <= match.end() and t["role"] is None:
                    t["role"] = "phone"


# --------------------------------------------------------------------------- card numbers


def _passes_luhn(digits: str) -> bool:
    total = 0
    for position, char in enumerate(reversed(digits)):
        value = int(char)
        if position % 2:
            value = value * 2 - 9 if value > 4 else value * 2
        total += value
    return total % 10 == 0


def _card_prefix(digits: str) -> bool:
    if len(digits) < 4:
        return False
    if digits[0] in "456":
        return True
    if digits[0] == "3":
        return digits[1] in "0456789"
    return digits[0] == "2" and 2221 <= int(digits[:4]) <= 2720


def _card_after_label(run: list[dict], k: int) -> bool:
    """Whether `run[k:]` is a card number that follows a reference in the same run: 13-19 digits, a card prefix, Luhn,
    card grouping, and (unless it is the whole run) a label token before it that is not grouped like the card's first
    group. "Order 12345 5555 5555 5555 4444" and "order no. 2654861; 3782 822463 10005" are a label and a card; a
    tracking number whose tail happens to pass Luhn ("9400 1234 5678 9012 3456 78") is one number, and so is "order
    1234 5555 5555 5555 4444", which reads as twenty digits in fours: that shape is a listed miss."""
    tokens = run[k:]
    digits = _digits(tokens)
    if not (13 <= len(digits) <= 19 and _card_prefix(digits) and _passes_luhn(digits)):
        return False
    lengths = [len(t["digits"]) for t in tokens]
    if not _card_grouping(lengths, spoken=False, digits=digits):
        return False
    # a four-digit label before a number in fours reads as twenty digits in fours and stays one reference (a listed miss);
    # a 4-6-5 or 4-6-4 grouping is a card's own shape whatever stands before it ("receipt 4821 3782 822463 10005")
    return k == 0 or len(run[k - 1]["digits"]) != lengths[0] or lengths in ([4, 6, 5], [4, 6, 4])


def _card_grouping(lengths: list[int], spoken: bool, digits: str = "") -> bool:
    """How a card is written in groups: 4s (or 8s, 12s) with a last group no longer than the one before it, equal
    groups with a shorter last one (6-6-4), Amex 4-6-5, Diners 4-6-4; spoken groups and a single group are free."""
    if spoken or len(lengths) == 1:
        return True
    merged: list[int] = []
    for n in lengths:  # short pieces read out in pairs ("55 then 55") count as one group
        if merged and n < 4 and merged[-1] < 4:
            merged[-1] += n
        else:
            merged.append(n)
    lengths = merged
    if len(lengths) == 1 or (lengths == [5, 5, 5] and digits[:2] in ("34", "37")):  # an Amex read in fives
        return True
    head, last = lengths[:-1], lengths[-1]
    return lengths in ([4, 6, 5], [4, 6, 4]) or (all(n % 4 == 0 for n in head) and (last % 4 == 0 or last <= head[-1])) or \
        (all(n == 6 for n in head) and last <= 6)


def _runs(tokens: list[dict], text: str, message: int = 0, fine: bool = False) -> list[list[dict]]:
    """Candidate tokens joined by separators only, on one line. A last four ("... and it ends with 4444") is a run of
    its own that may only END a card number: the last group of a card read out loud is its last four."""
    runs: list[list[dict]] = []
    for t in (t for t in tokens if t["digits"] is not None and t["role"] in (None, "last4", "year")):
        if runs:
            between = text[runs[-1][-1]["end"]:t["start"]]
            t["words_before"] = bool(re.search(r"[^\W\d_]", between.replace("REDACTED", "")))
            t["after_number_cue"] = bool(_AFTER_NUMBER_CUE.search(between))
        if runs and t["role"] != "last4" and runs[-1][-1]["role"] != "last4":
            gap = text[runs[-1][-1]["end"]:t["start"]]
            # one line, separators only; for codes (`fine`), a sentence or list break (". ", ", ", " / ") starts a new run too
            breaks = r"[^\W\d_]|\n|\r|[.,;:!?]\s|\s/\s" if fine else r"[^\W\d_]|\n|\r"
            # except a code dictated one digit at a time: "three, eight, six", "3, 8, 6" is one code, not a list of three
            dictated = fine and len(t["digits"]) == 1 and len(runs[-1][-1]["digits"]) == 1 and bool(re.fullmatch(r", ?", gap))
            if (dictated or not re.search(breaks, gap)) and len(gap) <= 3 and not MASK_TOKEN.search(gap):
                runs[-1].append(t)
                continue
        runs.append([t])
    return runs


def _digits(tokens: list[dict]) -> str:
    return "".join(t["digits"] for t in tokens)


def _card_sequences(runs: list[list[dict]]) -> list[list[dict]]:
    """Token sequences that are card numbers: whole runs, the last one whole or cut after any of its tokens. Searched
    twice: as written, and with 1-2 digit written tokens left out (list labels: "1) 6011 2) 1111", "first 8: ...")."""
    found = _card_sequences_in(runs)
    unlabelled = [[t for t in run if (t["spoken"] and not t.get("single_word")) or (not t["spoken"] and len(t["digits"]) > 2)
                   or (t["spoken"] and len(t["digits"]) > 1)] for run in runs]
    return found + _card_sequences_in([run for run in unlabelled if run])


def _card_sequences_in(runs: list[list[dict]]) -> list[list[dict]]:
    found = []
    for i in range(len(runs)):
        for start in range(len(runs[i])):
            found += _card_sequences_from(runs, i, runs[i][start:])
    return found


def _counts_up(tokens: list[dict]) -> bool:
    """Six or more tokens that count upwards past nine are a count, not a card: the numerals of a numbered list ("2. ...
    3. ... 13. ...") read together as 2345678910111213, sixteen digits with a Mastercard prefix that pass Luhn, and the
    reply masker removed lines 2 to 13 of every such list (the round-5 review's non-blocking 1). Each token is the one
    before it or one more ("5. item 5 / 6. item 6" repeats each numeral), and the count reaches ten: thirteen digits
    cannot be had from one-digit numerals that only count up."""
    values = [int(t["digits"]) for t in tokens]
    return len(values) >= 6 and values[-1] >= 10 and all(b - a in (0, 1) for a, b in zip(values, values[1:]))


def _card_sequences_from(runs: list[list[dict]], i: int, first: list[dict]) -> list[list[dict]]:
    """Card numbers that begin with `first` (the first run, or a suffix of it: a code, PIN, expiry or order number typed
    just before the number in the same run is not part of it) and end in a later run or in `first` itself."""
    found = []
    total = 0
    for j in range(i, min(len(runs), i + 19)):
        if j > i and runs[j][0].get("after_number_cue"):
            break  # the digits after "cvv" or "exp" are the code or the expiry: a number never continues through them
        head = [first] + runs[i + 1:j]
        if any(t["role"] == "last4" for run in head for t in run):
            break  # a last four may only end a card number
        last_run = first if j == i else runs[j]
        for cut in range(len(last_run), 0, -1):
            pieces = head + [runs[j][:cut]] if j > i else [first[:cut]]
            tokens = [t for run in pieces for t in run]
            digits = _digits(tokens)
            last = tokens[-1]
            # a number run into its code: one spoken group, or one long written token, with 3-4 code digits on the end
            if cut == len(last_run) and (last["spoken"] or len(last["digits"]) >= 16) and len(digits) <= 23 and _card_prefix(digits):
                tails = [k for k in ((1, 2, 3, 4) if last["spoken"] else (3, 4)) if k < len(last["digits"])]
                if any(13 <= len(digits) - k <= 19 and _passes_luhn(digits[:-k]) for k in tails):
                    found.append(tokens)
                    break
            if not 13 <= len(digits) <= 19 or not _card_prefix(digits) or _counts_up(tokens):
                continue
            spoken = all(t["spoken"] for t in tokens)
            lengths = [len(_digits(run)) for run in pieces] if any(t["spoken"] for t in tokens) else [len(t["digits"]) for t in tokens]
            if _passes_luhn(digits) and (len(pieces) == 1 or _card_grouping(lengths, spoken, digits)):
                found.append(tokens)
                break
            # a mistyped card: one written run, card grouping, Luhn fails
            # ... or pasted one group per line, nothing but line breaks and list markers between the groups
            shape = [len(t["digits"]) for t in tokens]
            one_message = len({t.get("message", 0) for t in tokens}) == 1
            no_words = not any(t.get("words_before") for run in pieces[1:] for t in run[:1])
            if cut == len(last_run) and not spoken and one_message and (len(pieces) == 1 or no_words) and (
                    shape in ([4, 4, 4, 4], [4, 6, 5], [4, 4, 4, 4, 3], [5, 5, 5]) or (len(tokens) == 1 and len(digits) in (15, 16))):
                found.append(tokens)
                break
        if found:
            # the first complete number from this start is the number: what a later run adds is something else. "… 3530 1113
            # 3330 0000 days ago, so it can't be that one" read the last word as a seventeenth digit, which passed Luhn
            # by chance, and the words between went with the number (seen in round 6's blind held-out run)
            break
        total += len(_digits(last_run))
        if total > 19:
            break
    return found


def _replace(text: str, spans: list[tuple[int, int, str]]) -> str:
    """Overlapping spans are merged into one mask covering all of them (the label of the earliest, longest span)."""
    merged: list[list] = []
    for start, end, mask in sorted(set(spans), key=lambda span: (span[0], -span[1])):
        if merged and start < merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end, mask])
    out, last = [], 0
    for start, end, mask in merged:
        out += [text[last:start], mask]
        last = end
    return "".join(out + [text[last:]])


def mask_card_numbers(text: str) -> str:
    """Card numbers only (step 4), for text the model or the harness writes."""
    text = normalize(text)
    tokens = _tokens(text)
    spans = [(seq[0]["start"], seq[-1]["end"], CARD_NUMBER_MASK) for seq in _card_sequences(_runs(tokens, text))]
    return _replace(text, spans)


# --------------------------------------------------------------------------- customer messages


def _code_and_expiry_spans(tokens: list[dict], text: str, card_context: bool, taken: list[tuple[int, int, str]]) -> list[tuple[int, int, str]]:
    spans = []
    inside = lambda t: any(t["start"] >= a and t["end"] <= b for a, b, _ in taken + spans)
    # an expiry typed as four digits after its cue ("exp 0827"): an expiry, before the code rule can take it for a code
    for t in tokens:
        if t["digits"] is not None and not t["spoken"] and t["role"] is None and len(t["digits"]) == 4 and 1 <= int(t["digits"][:2]) <= 12 \
                and not inside(t) \
                and _card_expiry_cue(_before(text, t, 30), text, t):
            spans.append((t["start"], t["end"], EXPIRY_MASK))
    # an expiry typed as two numbers with a space or a dot between: "exp 12 29", "exp 12.29" (which reads as an amount),
    # "expiry 12 2029" after its cue; "12 2029" without one when the message carries card data, as "12/2029" already is
    numeric = [t for t in tokens if t["digits"] is not None]
    for month, year in zip(numeric, numeric[1:]):
        if month["spoken"] or year["spoken"] or month["role"] not in (None, "amount") or year["role"] not in (None, "amount") \
                or inside(month) or not (len(month["digits"]) <= 2 and 1 <= int(month["digits"]) <= 12):
            continue
        gap = text[month["end"]:year["start"]]
        full_year = len(year["digits"]) == 4 and year["digits"][:2] == "20"
        before = _before(text, month, 30)
        cued = _card_expiry_cue(before, text, month) or card_context and bool(re.search(r"\bexpir\w*\W*$", before))  # "…4444 expires 12 29"
        if cued and (len(year["digits"]) == 2 or full_year) and re.fullmatch(r"[ ./\-]{1,3}", gap) or card_context and full_year and gap == " ":
            spans.append((month["start"], year["end"], EXPIRY_MASK))
    # "exp Dec 29", "expiry: July / 29", "exp Jul 33": after an expiry cue, a month name and two digits are a month and a
    # year, not a day of the month, whatever separates them
    for i, t in enumerate(tokens):
        if t["digits"] is None or t["spoken"] or len(t["digits"]) != 2 or t["role"] not in (None, "date", "identifier") or inside(t):
            continue  # ("Oct-30" reads as an identifier, like "CN-77812")
        month = next((x for x in reversed(tokens[max(0, i - 4):i]) if x["kind"] == "word" and x["text"].lower() != "of"), None)
        # ... and with no cue at all when they stand directly before the card number, as in a pasted card note ("September
        # 27 4242 4242 4242 4242 / cvc 123": round 6's blind held-out run), unless a date word leads up to them ("charged
        # on September 27 4242 …" is a day)
        beside_the_number = month is not None and any(mask == CARD_NUMBER_MASK and re.fullmatch(r"[ \t]+", text[t["end"]:a]) for a, _, mask in taken) \
            and not _DATE_WORD_BEFORE.search(text[max(0, month["start"] - 24):month["start"]])
        if month is not None and _MONTH.match(month["text"]) and re.fullmatch(r"(\s+of)?[\s/.,\-]{1,4}", text[month["end"]:t["start"]]) \
                and (_card_expiry_cue(_before(text, t, 30), text, t) or beside_the_number):
            spans.append((month["start"], t["end"], EXPIRY_MASK))
    # "Fine, it's 5127 and ZIP 60614", typed right after a card paste: four bare digits beside a ZIP given after its cue, in
    # a message with no card number of its own, are the other half of a verification answer, not the security code
    answers_verification = not taken and any(t["role"] == "zip" for t in tokens)
    codes: set[str] = set()  # every code found in this message: the same digits again are the same secret
    unclaimed: list[list[dict]] = []
    queue = _runs([t for t in tokens if t["role"] is None and not inside(t)], text, fine=True)  # never a last four, ZIP or year
    after_a_cued_code: list[dict] = []  # the rest of a run that began with a cue and its code
    while queue:
        run = queue.pop(0)
        first = run[0]
        if run is after_a_cued_code and card_context:
            # in a card conversation, what follows the code in the same run is the rest of the number, not a second code
            spans.append((first["start"], run[-1]["end"], CARD_DIGITS_MASK))
            continue
        before = _before(text, first, 45)
        cue = _CODE_CUE.search(before)
        cue_before = bool(cue) and not re.search(r"\d", before[cue.end():])
        if cue_before and len(run) > 1 and len(first["digits"]) in (3, 4) and not _code_said_more_than_once(run):
            # the cue names the token after it; what follows in the run is something else, read on its own. "CVC 047 1111"
            # (the code, then the last group of a number whose first twelve digits came in the message before) was a
            # seven-digit run that no rule took, and the code was stored (round 6's blind held-out run)
            after_a_cued_code = run[1:]
            queue.insert(0, after_a_cued_code)
            run = run[:1]
        last = run[-1]
        digits = _digits(run)
        n = len(digits)
        after = text[last["end"]:last["end"] + 30]
        cue_after = bool(re.match(r"\W{0,3}(is|are|was)?\W{0,3}(my|the)?\W{0,2}" + _CODE_CUE.pattern, after, re.IGNORECASE))
        weak_cue = bool(_WEAK_CODE_CUE.search(before[-20:]))
        spaced = len(run) == n  # "7 3 7": one digit per token
        said_twice = _code_said_more_than_once(run)
        last_four = answers_verification and n == 4 and len(run) == 1 and not first["spoken"]
        if n in (3, 4) and (len(run) == 1 or spaced) and (card_context and not last_four or cue_before or cue_after or weak_cue and n == 3):
            spans.append((first["start"], last["end"], SECURITY_CODE_MASK))
            codes.add(digits)
        elif card_context and n >= 8 and (all(len(t["digits"]) == 4 for t in run) or len(run) == 1 and n <= 12):
            spans.append((first["start"], last["end"], CARD_DIGITS_MASK))  # "5555/5555": part of a number sent in pieces
        elif said_twice and (card_context or cue_before or cue_after or weak_cue and len(said_twice) == 3):
            # "three eight six (386)", "386 386": one code in two renderings reads as one six-digit run
            closes = text[last["end"]:last["end"] + 1] in (")", "]", "}") and bool(re.search(r"[(\[{]", text[first["end"]:last["start"]]))
            spans.append((first["start"], last["end"] + closes, SECURITY_CODE_MASK))
            codes.add(said_twice)
        else:
            unclaimed.append(run)
    for run in unclaimed:  # "sec code three eight six, in digits 386": no cue of its own, the digits of a code just found
        if _digits(run) in codes and (len(run) == 1 or len(run) == len(_digits(run))):
            spans.append((run[0]["start"], run[-1]["end"], SECURITY_CODE_MASK))
    for i, t in enumerate(tokens):
        if t["role"] not in ("month_pair", "month_year") or inside(t):
            continue
        cue = _card_expiry_cue(_before(text, t, 30), text, t) or t["role"] == "month_year" and _card_expiry_cue(_before(text, t, 40), text, t, bare=True)
        if card_context or cue:
            if t["role"] == "month_pair":
                partner = next((x for x in tokens[i + 1:i + 3] if x["role"] == "month_pair"), None)
                if partner:
                    spans.append((t["start"], partner["end"], EXPIRY_MASK))
                continue
            month = next((x for x in reversed(tokens[max(0, i - 3):i]) if x["kind"] == "word" and _MONTH.match(x["text"])), None)
            spans.append(((month or t)["start"], t["end"], EXPIRY_MASK))
    # a spoken expiry after a cue: "exp twelve twenty-nine" (one spoken group "1229")
    for t in tokens:
        if t["spoken"] and not inside(t) and t["role"] is None and len(t["digits"]) == 4 and 1 <= int(t["digits"][:2]) <= 12 \
                and (card_context or _card_expiry_cue(_before(text, t, 30), text, t)):
            spans.append((t["start"], t["end"], EXPIRY_MASK))
        # ... and with a one-digit month, "expiry: seven twenty-nine" (three digits: only after its cue)
        elif t["spoken"] and not inside(t) and t["role"] is None and len(t["digits"]) == 3 and t["digits"][0] != "0" \
                and _card_expiry_cue(_before(text, t, 30), text, t):
            spans.append((t["start"], t["end"], EXPIRY_MASK))
    return spans


def _code_said_more_than_once(run: list[dict]) -> str | None:
    """The 3- or 4-digit code a run repeats ("three eight six (386)", "386 386", "3 8 6/386"), or None. Every repetition
    must end where a token ends; a spoken group may end at any of its digits ("three eight six three eight six")."""
    digits = _digits(run)
    ends, at = set(), 0
    for t in run:
        ends |= set(range(at + 1, at + len(t["digits"]) + 1)) if t["spoken"] else {at + len(t["digits"])}
        at += len(t["digits"])
    for size in (3, 4):
        if len(digits) >= 2 * size and digits == digits[:size] * (len(digits) // size) \
                and all(end in ends for end in range(size, len(digits) + 1, size)):
            return digits[:size]
    return None


def _card_expiry_cue(before: str, text: str, token: dict, bare: bool = False) -> bool:
    """An expiry cue right before the date ("exp 12/29", "expiry date: 12/29"), and not about something else
    ("exp. delivery 11/24", "my travel notice expiration should be 12/10"). With `bare`, for a month and a year that
    cannot be a day ("expires end of January '27"): a plain "expires" too, when it has no subject of its own or its
    subject is the card ("my subscription expires July 2029" is the subscription's)."""
    cues = list(_EXPIRY_CUE.finditer(before))
    if bare:
        cues += [cue for cue in _BARE_EXPIRY_CUE.finditer(before)
                 if (re.search(r"([^\W\d_]+)[ \t]+$", before[:cue.start()]) or [None, "it"])[1].lower() in _CARD_SUBJECTS]
    for cue in cues:
        between = before[cue.end():]
        context = text[max(0, token["start"] - len(before) - 30):token["start"] - len(before) + cue.start()]
        between = re.sub(_MONTHS + r"\.?[\W_]*(of[\W_]+)?$", "", between, flags=re.IGNORECASE)  # "expiry December 2029": the month is the expiry's
        if re.fullmatch(r"[\W_]*((date|is|was|on|of|at|the|end|should\s+be|reads?|says?)[\W_]+)*", between, re.IGNORECASE) \
                and not _NOT_CARD_EXPIRY.search(context + " " + between):
            return True
    return False


def mask_customer_message(text: str, previous: tuple[str, ...] = ()) -> tuple[str, dict[int, str]]:
    """Every rule, for one customer message, given the session's earlier stored customer messages (oldest first).

    Returns the masked message and {index into `previous`: rewritten text} for earlier messages that held the
    opening part of a card number this message completes; the caller writes those rewrites back to the store.
    """
    text = normalize(text)
    tokens = _tokens(text)
    runs = _runs(tokens, text)
    spans = [(seq[0]["start"], seq[-1]["end"], CARD_NUMBER_MASK) for seq in _card_sequences(runs)]
    rewrites: dict[int, list[tuple[int, int, str]]] = {}
    window = list(range(max(0, len(previous) - 3), len(previous)))
    earlier = []
    last_fours = [t["digits"] for t in tokens if t["role"] == "last4"]
    for index in window:
        earlier_text = normalize(previous[index])
        earlier_tokens = [dict(t, message=index) for t in _tokens(earlier_text)]
        last_fours += [t["digits"] for t in earlier_tokens if t["role"] == "last4"]
        for run in _runs(earlier_tokens, earlier_text, index):
            earlier.append([dict(t, message=index) for t in run])
    answers = {index for index in window if _VERIFICATION_ANSWER.search(previous[index])}
    if _VERIFICATION_ANSWER.search(text):
        answers.add(len(previous))
    if earlier:
        current = [[dict(t, message=len(previous)) for t in run] for run in runs]
        # A security code typed at the seam is not part of the number: "my card is 5555 5555 5555" / "CVV 737 4444",
        # "5555 5555 5555 737" / "4444" (the round-5 review's non-blocking 11). The number is also looked for with one
        # code-sized token dropped from the end of an earlier message, or from the start of this one.
        seams = [earlier + current]
        if current and len(current[0]) > 1 and len(current[0][0]["digits"]) in (3, 4):
            seams.append(earlier + [current[0][1:]] + current[1:])
        ends = {run[0]["message"]: k for k, run in enumerate(earlier)}  # the last run of each earlier message
        trimmed = [run[:-1] if k in ends.values() and len(run) > 1 and len(run[-1]["digits"]) in (3, 4) else run for k, run in enumerate(earlier)]
        if trimmed != earlier:
            seams.append(trimmed + current)
        found, seen = [], set()
        for combined in seams:
            for seq in _card_sequences(combined):
                key = tuple((t["message"], t["start"]) for t in seq)
                if key not in seen:
                    seen.add(key)
                    found.append(seq)
        for seq in found:
            here = [t for t in seq if t["message"] == len(previous)]
            there = [t for t in seq if t["message"] != len(previous)]
            if not here or not there:
                continue
            involved = {t["message"] for t in seq}
            # verification answers typed in turn ("hmm, 2425?", "try 0634", "card ending 8230, ZIP 81775") can pass Luhn
            # together by chance: short pieces (a last-four or ZIP-sized group per message) complete a card number only if
            # the customer said they were giving one. A message that holds eight or more digits of the number is never
            # an answer, whatever else it says ("5555 5555 5555 and my zip is 94107" / "4444": the round-4 review)
            texts = [normalize(previous[i]) if i < len(previous) else text for i in involved]
            short = all(len(_digits([t for t in seq if t["message"] == m])) <= 5 for m in involved)
            if involved & answers and short and not any(_CARD_CUE.search(x) for x in texts):
                continue
            spans.append((here[0]["start"], here[-1]["end"], CARD_DIGITS_MASK))
            for index in {t["message"] for t in there}:
                part = [t for t in there if t["message"] == index]
                rewrites.setdefault(index, []).append((part[0]["start"], part[-1]["end"], CARD_DIGITS_MASK))
    # a card number here corrects a mistyped one sent just before ("4000 0566 5562 5556" ... "no wait, 4000 0566 5566 5556"):
    # the earlier, nearly identical number is card data too
    for seq in _card_sequences(runs):
        digits = _digits(seq)
        for index in window:
            earlier_text = normalize(previous[index])
            earlier_runs = _runs(_tokens(earlier_text), earlier_text)
            for a in range(len(earlier_runs)):
                for b in range(a + 1, min(len(earlier_runs), a + 8) + 1):
                    piece = [t for run in earlier_runs[a:b] for t in run]
                    if len(_digits(piece)) >= 12 and abs(len(_digits(piece)) - len(digits)) <= 2 and _edit_distance(_digits(piece), digits) <= 2:
                        rewrites.setdefault(index, []).append((piece[0]["start"], piece[-1]["end"], CARD_DIGITS_MASK))
    # the rest of a number whose last four was already given, here or in the window ("card ending 4444, zip 94107" then "and
    # the first twelve: 5555 5555 5555"): card-prefixed digits in card groups that complete a last four into a Luhn number
    taken = lambda run: any(run[0]["start"] >= a and run[-1]["end"] <= b for a, b, _ in spans)
    for run in runs:
        digits = _digits(run)
        if 8 <= len(digits) <= 15 and _card_prefix(digits) and not taken(run) and all(t["role"] is None for t in run) \
                and (len(run) == 1 or all(len(t["digits"]) == 4 for t in run)) \
                and any(13 <= len(digits + lf) <= 19 and _passes_luhn(digits + lf) for lf in last_fours):
            spans.append((run[0]["start"], run[-1]["end"], CARD_DIGITS_MASK))
    # ... and the same when those digits came in two or three messages ("card ending 4444 zip 94107" / "5555 5555" / "5555":
    # the round-5 review's non-blocking 11): plain groups that end the earlier messages and open this one. One message
    # must hold eight or more of them, as above: guessed last fours typed in turn are not the rest of a card number.
    plain = lambda run: all(t["role"] is None for t in run) and (len(run) == 1 or all(len(t["digits"]) == 4 for t in run))
    chain = [runs[0]] if runs and plain(runs[0]) and not taken(runs[0]) else []
    for index in reversed(window if chain else []):
        last_run = next((run for run in reversed(earlier) if run[0]["message"] == index), None)
        if not last_run or not plain(last_run):
            break
        chain.insert(0, last_run)
        digits = "".join(_digits(run) for run in chain)
        if 8 <= len(digits) <= 15 and _card_prefix(digits) and any(len(_digits(run)) >= 8 for run in chain) \
                and any(13 <= len(digits + lf) <= 19 and _passes_luhn(digits + lf) for lf in last_fours):
            spans.append((chain[-1][0]["start"], chain[-1][-1]["end"], CARD_DIGITS_MASK))
            for run in chain[:-1]:
                rewrites.setdefault(run[0]["message"], []).append((run[0]["start"], run[-1]["end"], CARD_DIGITS_MASK))
            break
    card_context = bool(spans) or any(CARD_NUMBER_MASK in p or CARD_DIGITS_MASK in p for p in previous[-2:]) \
        or any(_card_expiry_cue(text[:t["start"]][-30:], text, t) for t in tokens if t["role"] in ("month_pair", "month_year")) \
        or bool(re.search(r"\b(cvv2?|cvc2?|cid|csc|security\s+code|card\s+number)\b", text, re.IGNORECASE))
    spans += _code_and_expiry_spans(tokens, text, card_context, spans)
    for index, parts in rewrites.items():  # the code typed beside the opening groups ("5555 5555 5555 737") is card data as well
        earlier_text = normalize(previous[index])
        parts += _code_and_expiry_spans(_tokens(earlier_text), earlier_text, True, parts)
    return _replace(text, spans), {index: _replace(normalize(previous[index]), parts) for index, parts in rewrites.items()}


_MASK_NAMES = {CARD_NUMBER_MASK: ("card number", "card numbers"), CARD_DIGITS_MASK: ("part of a card number", "parts of a card number"),
               SECURITY_CODE_MASK: ("security code", "security codes"), EXPIRY_MASK: ("expiry", "expiries"),
               ONE_TIME_CODE_MASK: ("six-digit number typed while a one-time code was open", "six-digit numbers typed while a one-time code was open")}


def removed_summary(typed: str, stored: str) -> str:
    """What the harness removed from a customer message, for the model to read as a fact about that message. The model
    sees the stored text; without this line it has to infer from the absence of digits whether masking ran, and a
    round-5 review session had it say a number "was removed before it reached me" while the number sat in the store."""
    added = Counter(m.group() for m in MASK_TOKEN.finditer(stored)) - Counter(m.group() for m in MASK_TOKEN.finditer(typed))
    if not added:
        return "nothing was removed from the customer's latest message: every digit in it is stored as typed"
    return "removed from the customer's latest message before it reached you or any store: " + ", ".join(
        f"{added[mask]} {one if added[mask] == 1 else many}" for mask, (one, many) in _MASK_NAMES.items() if added[mask]) + \
        "; everything else in it is stored as typed"


def turn_without_codes(record: dict, sent: str, codes: set[str]) -> dict:
    """A turn record with every one of `codes` (one-time codes) replaced: in the customer's message, in every tool-call
    argument, and in the reply. The model reads what the customer typed, so it can repeat a code typed there ("... so I
    don't need 018899"); the procedure forbids that, and what the customer reads and the evidence records does not
    depend on the procedure being followed."""
    def without(text: str) -> str:
        for code in codes:
            text = text.replace(code, ONE_TIME_CODE_MASK)
        return text

    calls = [{**call, "args": {key: without(value) if isinstance(value, str) else value for key, value in call["args"].items()}}
             for call in record["tool_calls"]]
    return {**record, "customer": without(sent), "tool_calls": calls, "reply": without(record.get("reply") or "")}


def _edit_distance(a: str, b: str) -> int:
    row = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        prev, row[0] = row[0], i
        for j, cb in enumerate(b, 1):
            prev, row[j] = row[j], min(row[j] + 1, row[j - 1] + 1, prev + (ca != cb))
    return row[-1]


def mask_customer_text(text: str, previous_customer_texts: tuple[str, ...] = ()) -> str:
    """The masked message only (for text with no store to rewrite: the model's reasoning, tool arguments)."""
    return mask_customer_message(text, previous_customer_texts)[0]


def mask_conversation(messages: list[str]) -> list[str]:
    """What a session store holds after these customer messages, with every rewrite applied (for evaluation)."""
    stored: list[str] = []
    for message in messages:
        masked, rewrites = mask_customer_message(message, tuple(stored))
        for index, rewritten in rewrites.items():
            stored[index] = rewritten
        stored.append(masked)
    return stored


def removed_fragments(original: str, rewritten: str) -> list[str]:
    """The digit strings a rewrite removed from an earlier message (at least 4 digits each): what to scrub elsewhere."""
    original = normalize(original)
    kept = re.sub(r"\D", " ", MASK_TOKEN.sub(" ", rewritten)).split()
    pieces = []
    for match in re.finditer(r"\d(?:[^\w\n]{0,3}\d)+", original):
        digits = re.sub(r"\D", "", match.group())
        if len(digits) >= 4 and digits not in kept:
            pieces.append(digits)
    return pieces


def scrub_fragments(text: str, fragments: list[str]) -> str:
    """Replace every written occurrence of these digit strings (any separators of up to 3 characters between digits)."""
    for digits in sorted(set(fragments), key=len, reverse=True):
        pattern = r"(?<!\d)" + r"[^\w\n]{0,3}".join(digits) + r"(?!\d)"
        text = re.sub(pattern, CARD_DIGITS_MASK, text)
    return text
