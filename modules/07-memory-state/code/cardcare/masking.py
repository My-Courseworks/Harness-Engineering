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
   Diners 4-6-4, or spoken). The first run is used whole, the last whole or its first tokens (a code may follow
   on the same line). One run with a card prefix and card grouping is masked even when Luhn fails: a mistyped card.
5. Across messages: a sequence that ends in this message and starts in one of the last three customer messages is
   masked here, and the earlier stored message is rewritten too (`mask_customer_message` returns the rewrite), so
   the opening half of a number sent in two messages does not stay behind.
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

CARD_NUMBER_MASK = "[REDACTED CARD NUMBER]"
SECURITY_CODE_MASK = "[REDACTED SECURITY CODE]"
EXPIRY_MASK = "[REDACTED EXPIRY]"
CARD_DIGITS_MASK = "[REDACTED CARD DIGITS]"
MASK_TOKEN = re.compile(r"\[REDACTED [A-Z ]+\]")

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
_LAST_FOUR_CUE = re.compile(r"(ending|ends|ended)(\s+(in|with|on))?\W*$|last\s+(4|four)(\s+digits?)?(\s+of\s+(my|the)\s+card)?"
                            r"(\s+(are|is|were|was))?\W*$|last\s+digits(\s+(are|is))?\W*$", re.IGNORECASE)
_ZIP_CUE = re.compile(r"\b(zip|zip\s*code|postal\s*code|post\s*code|postcode)(\s+(is|was|=))?\W*$", re.IGNORECASE)
_YEAR_CUE = re.compile(r"\b(since|in|year|from|of|until|till|by)\W*$", re.IGNORECASE)
_PHONE_CUE = re.compile(r"\b(call|phone|tel|telephone|mobile|cell|text me|whatsapp)\b[^.\n]{0,20}$", re.IGNORECASE)
_CODE_CUE = re.compile(
    r"\b(cvv2?|cvc2?|cid|csc|cvn|security\s+(code|number|digits)|card\s+code|verification\s+(code|value|number)|"
    r"(code|number|digits?)\s+(on|at|from)\s+(the\s+)?(back|reverse|front)|(on|at)\s+the\s+(back|reverse)(\s+of\s+(my|the)\s+card)?|"
    r"back\s+of\s+(my|the)?\s*card|signature\s+(strip|panel|box)|(three|3|four|4)[\s-]+digits?(\s+code)?)\b", re.IGNORECASE)
_WEAK_CODE_CUE = re.compile(r"\bcode\b", re.IGNORECASE)  # "my code is 737": for 3 digits only
_EXPIRY_CUE = re.compile(r"\b(exp|expiry|expiration|exp\.?\s*date|valid\s+(thru|through|until|till)|good\s+(thru|through)|"
                         r"(card|it)\s+expires)\b", re.IGNORECASE)
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
    out, i = [], 0
    while i < len(raw):
        token = raw[i]
        spoken = _spoken_value(raw, i) if token["kind"] == "word" else None
        if spoken:
            digits, last = spoken
            out.append({"text": text[token["start"]:raw[last]["end"]], "start": token["start"], "end": raw[last]["end"], "kind": "digits",
                        "digits": digits, "spoken": True, "role": None, "words": last - i + 1, "single_word": last == i})
            i = last + 1
        else:
            out.append(token)
            i += 1
    # a lone spoken unit that counts something is not a digit: "the first four are", "three digits on the back"
    counts = []
    for j, token in enumerate(out):
        if token["spoken"] and token.get("single_word") and len(token["digits"]) == 1:
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
    return merged


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
        elif _LAST_FOUR_CUE.search(before) and len(t["digits"]) == 4 and not joined_next:
            t["role"] = "last4"
            # "my last four is 4427/5127": an alternative right after it is a last four too
            if nxt and nxt["text"] in ("/", ",") and nxt2 and nxt2["digits"] and len(nxt2["digits"]) == 4 and nxt2["start"] - t["end"] <= 3:
                nxt2["role"] = "last4"
        elif len(t["digits"]) == 4 and t["digits"][:2] in ("19", "20") and _YEAR_CUE.search(_before(text, t, 12)):
            t["role"] = "year"
    _classify_dates(tokens, text)
    _classify_phones(tokens, text)


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
        if nums and len(nums[0]["digits"]) <= 2 and int(nums[0]["digits"]) <= 31 and not nums[0]["spoken"] and nums[0]["role"] is None:
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
                and (len(year["digits"]) == 2 or year["digits"][:2] == "20"):
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
    if digits[0] in "456":
        return True
    if digits[0] == "3":
        return digits[1] in "0456789"
    return digits[0] == "2" and 2221 <= int(digits[:4]) <= 2720


def _card_grouping(lengths: list[int], spoken: bool) -> bool:
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
    if len(lengths) == 1:
        return True
    head, last = lengths[:-1], lengths[-1]
    return lengths in ([4, 6, 5], [4, 6, 4]) or (all(n % 4 == 0 for n in head) and (last % 4 == 0 or last <= head[-1])) or \
        (all(n == 6 for n in head) and last <= 6)


def _runs(tokens: list[dict], text: str, message: int = 0, fine: bool = False) -> list[list[dict]]:
    """Candidate tokens joined by separators only, on one line. A last four ("... and it ends with 4444") is a run of
    its own that may only END a card number: the last group of a card read out loud is its last four."""
    runs: list[list[dict]] = []
    for t in (t for t in tokens if t["digits"] is not None and t["role"] in (None, "last4", "year")):
        if runs and t["role"] != "last4" and runs[-1][-1]["role"] != "last4":
            gap = text[runs[-1][-1]["end"]:t["start"]]
            # one line, separators only; for codes (`fine`), a sentence or list break (". ", ", ", " / ") starts a new run too
            breaks = r"[^\W\d_]|\n|\r|[.,;:!?]\s|\s/\s" if fine else r"[^\W\d_]|\n|\r"
            if not re.search(breaks, gap) and len(gap) <= 3 and not MASK_TOKEN.search(gap):
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
        total = 0
        for j in range(i, min(len(runs), i + 19)):
            if any(t["role"] == "last4" for run in runs[i:j] for t in run):
                break  # a last four may only end a card number
            for cut in range(len(runs[j]), 0, -1):
                pieces = [run for run in runs[i:j]] + [runs[j][:cut]]
                tokens = [t for run in pieces for t in run]
                digits = _digits(tokens)
                if not 13 <= len(digits) <= 19 or not _card_prefix(digits):
                    continue
                spoken = all(t["spoken"] for t in tokens)
                lengths = [len(_digits(run)) for run in pieces] if any(t["spoken"] for t in tokens) else [len(t["digits"]) for t in tokens]
                if _passes_luhn(digits) and (len(pieces) == 1 or _card_grouping(lengths, spoken)):
                    found.append(tokens)
                    break
                # a mistyped card: one written run, card grouping, Luhn fails
                if len(pieces) == 1 and cut == len(runs[j]) and not spoken and (
                        [len(t["digits"]) for t in tokens] in ([4, 4, 4, 4], [4, 6, 5], [4, 4, 4, 4, 3]) or
                        (len(tokens) == 1 and len(digits) in (15, 16))):
                    found.append(tokens)
                    break
            total += len(_digits(runs[j]))
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
    for run in _runs([t for t in tokens if t["role"] is None and not inside(t)], text, fine=True):  # never a last four, ZIP or year
        first, last = run[0], run[-1]
        digits = _digits(run)
        n = len(digits)
        before, after = _before(text, first, 45), text[last["end"]:last["end"] + 30]
        cue = _CODE_CUE.search(before)
        cue_before = bool(cue) and not re.search(r"\d", before[cue.end():])
        cue_after = bool(re.match(r"\W{0,3}(is|are|was)?\W{0,3}(my|the)?\W{0,2}" + _CODE_CUE.pattern, after, re.IGNORECASE))
        weak = bool(_WEAK_CODE_CUE.search(before[-20:])) and n == 3
        spaced = len(run) == n  # "7 3 7": one digit per token
        if n in (3, 4) and (len(run) == 1 or spaced) and (card_context or cue_before or cue_after or weak):
            spans.append((first["start"], last["end"], SECURITY_CODE_MASK))
        elif card_context and n >= 8 and (all(len(t["digits"]) == 4 for t in run) or len(run) == 1 and n <= 12):
            spans.append((first["start"], last["end"], CARD_DIGITS_MASK))  # "5555/5555": part of a number sent in pieces
    for i, t in enumerate(tokens):
        if t["role"] not in ("month_pair", "month_year") or inside(t):
            continue
        cue = _EXPIRY_CUE.search(_before(text, t, 30))
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
                and (card_context or _EXPIRY_CUE.search(_before(text, t, 30))):
            spans.append((t["start"], t["end"], EXPIRY_MASK))
    return spans


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
    for index in window:
        earlier_text = normalize(previous[index])
        earlier_tokens = [dict(t, message=index) for t in _tokens(earlier_text)]
        for run in _runs(earlier_tokens, earlier_text, index):
            earlier.append([dict(t, message=index) for t in run])
    if earlier:
        current = [[dict(t, message=len(previous)) for t in run] for run in runs]
        combined = earlier + current
        for seq in _card_sequences(combined):
            here = [t for t in seq if t["message"] == len(previous)]
            there = [t for t in seq if t["message"] != len(previous)]
            if not here or not there:
                continue
            spans.append((here[0]["start"], here[-1]["end"], CARD_DIGITS_MASK))
            for index in {t["message"] for t in there}:
                part = [t for t in there if t["message"] == index]
                rewrites.setdefault(index, []).append((part[0]["start"], part[-1]["end"], CARD_DIGITS_MASK))
    card_context = bool(spans) or any(CARD_NUMBER_MASK in p or CARD_DIGITS_MASK in p for p in previous[-2:]) \
        or bool(_EXPIRY_CUE.search(text)) or bool(re.search(r"\b(cvv2?|cvc2?|cid|csc|security\s+code|card\s+number)\b", text, re.IGNORECASE))
    spans += _code_and_expiry_spans(tokens, text, card_context, spans)
    return _replace(text, spans), {index: _replace(normalize(previous[index]), parts) for index, parts in rewrites.items()}


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
