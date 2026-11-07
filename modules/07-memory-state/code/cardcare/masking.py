"""Card-data masking by normalisation and tokens, not by enumerating formats.

1. Normalise: NFKC (full-width digits, non-breaking and narrow spaces), every Unicode dash to "-", every
   other space-like character to " ", zero-width characters and soft hyphens dropped.
2. Tokenise into digit runs, words and single symbols, each with its span. A token's digit value is its
   digits, or the digit a number word names ("zero" ... "nine", "oh").
3. Classify digit tokens that are never card data: identifiers (attached to letters, not to number words:
   "C-5001", "T-1002", "CN-77812"), amounts (a currency sign before, or a unit word after), clock times
   ("14:30") and ISO dates that are real dates.
   Month/year pairs ("10/26", "12-2029") are dates unless the message is about a card, where they are expiries.
4. Chain the remaining digit tokens across short gaps: separators of any kind, and up to two ordinary words
   ("5555 then 5555"); a sentence end breaks a chain. In a chain:
     - 12 or more digits joined by separators only are masked (a card number, mistyped or not);
     - any contiguous run of 13-19 digits that passes Luhn is masked, words between groups or not (also
       searched with 1-2 digit labels such as "first 8:" left out); where words split it, it must look read
       out in sequence (one repeated joiner, or card-shaped groups), so unrelated numbers in one sentence that
       pass Luhn by chance do not combine;
     - a run that completes a Luhn-valid, card-shaped number together with digit tokens from the previous
       one to three customer messages is masked, wherever the earlier fragment sat in its message.
5. Inside a chain, digit tokens joined by separators only (no word between them) form a run. Security
   codes: a run of exactly 3 digits is masked ("737", "7 3 7", "seven three seven"), wherever it sits in
   the chain (nothing this agent needs is a bare 3-digit number; amounts carry a currency or unit). A
   4-digit run is masked only next to a security cue ("cvv", "cid", "back", "reverse", "signature"...),
   because 4-digit numbers the agent needs (last four, years, cancellation codes) look the same. A run of
   two or more 4-digit groups that are not all years ("5555/5555") is masked as part of a card number sent
   in pieces when the same message carries other card data (a code, an expiry, a card number) or follows a
   masked one; on its own it could be an order or cancellation number the dispute needs. In such a message,
   any bare 3-digit number left is masked as the security code, wherever it sits.
6. Expiry: a month/year pair ("12/29") or a month name with a year ("Dec 2029") is masked only when the
   message, or the one before it, carries card data, or the message says "expiry".

`mask_customer_text` is the full rule set, for customer input and for the model's reasoning, which nobody
reads, so over-masking there costs nothing. `mask_card_numbers` is step 4's first two rules only, for text
the model or the harness writes for people (replies, notes, reflections), so case ids, dates and amounts in
generated text are never touched.
"""

import re
import unicodedata

CARD_NUMBER_MASK = "[REDACTED CARD NUMBER]"
SECURITY_CODE_MASK = "[REDACTED SECURITY CODE]"
EXPIRY_MASK = "[REDACTED EXPIRY]"
CARD_DIGITS_MASK = "[REDACTED CARD DIGITS]"

_DROP = dict.fromkeys(map(ord, "​‌‍⁠﻿­"), None)
_NUMBER_WORDS = {"zero": "0", "oh": "0", "one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6",
                 "seven": "7", "eight": "8", "nine": "9"}
_UNITS = {"dollar", "dollars", "usd", "euro", "euros", "eur", "cents", "bucks", "percent", "%", "days", "day", "months",
          "month", "years", "year", "minutes", "hours", "gb", "tb", "mb"}
_CURRENCY = set("$€£¥")
_SECURITY_CUES = re.compile(r"\b(cvv2?|cvc2?|cid|csc|security|verification|back|reverse|signature|front)\b", re.IGNORECASE)
_EXPIRY_CUES = re.compile(r"\b(expiry|expiration|exp|valid thru|valid through|good thru)\b", re.IGNORECASE)
_MONTH_YEAR = re.compile(r"\b(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.?\s+(19|20)\d{2}\b", re.IGNORECASE)
_MONTH_NAME = re.compile(r"(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*", re.IGNORECASE)
_TOKEN = re.compile(r"\d+|[^\W\d_]+|\S")
_SENTENCE_END = set(".!?;")


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).translate(_DROP)
    chars = []
    for ch in text:
        if ch in "\n\r":
            chars.append(ch)
        elif ch.isspace():
            chars.append(" ")
        elif unicodedata.category(ch) == "Pd" or ch in "−":
            chars.append("-")
        else:
            chars.append(ch)
    return "".join(chars)


def _tokens(text: str) -> list[dict]:
    tokens = []
    for match in _TOKEN.finditer(text):
        value = match.group()
        kind = "digits" if value.isdigit() else "word" if value[0].isalpha() else "symbol"
        digits = value if kind == "digits" else _NUMBER_WORDS.get(value.lower()) if kind == "word" else None
        tokens.append({"text": value, "start": match.start(), "end": match.end(), "kind": kind, "digits": digits, "role": None})
    _classify(tokens, text)
    return tokens


def _classify(tokens: list[dict], text: str) -> None:
    """Mark digit tokens that are identifiers, amounts, times or dates; they never join a card chain."""
    for i, t in enumerate(tokens):
        if t["kind"] != "digits" or t["role"]:
            continue
        prev, nxt = (tokens[i - 1] if i else None), (tokens[i + 1] if i + 1 < len(tokens) else None)
        touching_prev = prev and prev["end"] == t["start"]
        letters = lambda token: token["kind"] == "word" and token["digits"] is None  # a number word is not a prefix
        if touching_prev and (letters(prev) or (prev["text"] == "-" and i > 1 and letters(tokens[i - 2])
                                                and tokens[i - 2]["end"] == prev["start"])):
            t["role"] = "identifier"
        elif (touching_prev and prev["text"] in _CURRENCY) or (prev and prev["text"] in _CURRENCY and t["start"] - prev["end"] <= 1):
            t["role"] = "amount"
        elif nxt and nxt["text"].lower() in _UNITS:
            t["role"] = "amount"
        elif prev and letters(prev) and _MONTH_NAME.fullmatch(prev["text"]) and len(t["text"]) == 4 and t["text"][:2] in ("19", "20"):
            t["role"] = "month_year"  # "Dec 2029": a date, never part of a card chain
        elif nxt and nxt["text"] == ":" and i + 2 < len(tokens) and tokens[i + 2]["kind"] == "digits" and nxt["end"] == tokens[i + 2]["start"]:
            t["role"] = tokens[i + 2]["role"] = "time"
        elif i + 4 < len(tokens) and len(t["text"]) == 4 and tokens[i + 1]["text"] == "-" and tokens[i + 3]["text"] == "-" \
                and tokens[i + 2]["kind"] == tokens[i + 4]["kind"] == "digits" and tokens[i + 4]["end"] - t["start"] == 10 \
                and t["text"][:2] in ("19", "20") and 1 <= int(tokens[i + 2]["text"]) <= 12 and 1 <= int(tokens[i + 4]["text"]) <= 31:
            t["role"] = tokens[i + 2]["role"] = tokens[i + 4]["role"] = "date"
        elif nxt and nxt["text"] in ("/", "-") and i + 2 < len(tokens) and tokens[i + 2]["kind"] == "digits" and len(t["text"]) <= 2 \
                and len(tokens[i + 2]["text"]) in (2, 4) and nxt["start"] - t["end"] <= 1 and tokens[i + 2]["start"] - nxt["end"] <= 1 \
                and 1 <= int(t["text"]) <= 12:
            t["role"] = tokens[i + 2]["role"] = "month_pair"
    # an amount's decimal part ("$15.99") is part of the amount
    for i, t in enumerate(tokens):
        if t["role"] == "amount" and i + 2 < len(tokens) and tokens[i + 1]["text"] == "." and tokens[i + 2]["kind"] == "digits":
            tokens[i + 2]["role"] = "amount"


def _chains(tokens: list[dict], text: str) -> list[dict]:
    """Groups of card-candidate digit tokens joined by short gaps (separators, at most two ordinary words)."""
    chains, current, gap_words, gap_has_words = [], [], 0, False
    last_end = None
    for t in tokens:
        candidate = t["digits"] is not None and t["role"] is None
        if candidate:
            if current:
                gap = text[last_end:t["start"]]
                sentence_break = any(ch in _SENTENCE_END for ch in gap) and not (len(gap) == 1 and gap in ".")
                if sentence_break or gap_words > 2 or len(gap) > 24 or "\n" in gap:
                    chains.append({"tokens": current, "words": gap_has_words})
                    current, gap_has_words = [], False
                else:
                    gap_has_words = gap_has_words or gap_words > 0
            current.append(t)
            gap_words, last_end = 0, t["end"]
        elif current and t["kind"] == "word":
            gap_words += 1
    if current:
        chains.append({"tokens": current, "words": gap_has_words})
    return chains


def _separator_runs(chain: dict, text: str) -> list[list[dict]]:
    """Split a chain where a word sits between two digit tokens; what is left is joined by separators only."""
    runs: list[list[dict]] = []
    for token in chain["tokens"]:
        if runs and not re.search(r"[^\W\d_]", text[runs[-1][-1]["end"]:token["start"]]):
            runs[-1].append(token)
        else:
            runs.append([token])
    return runs


def _is_year(token: dict) -> bool:
    return len(token["digits"]) == 4 and token["digits"][:2] in ("19", "20")


def _passes_luhn(digits: str) -> bool:
    total = 0
    for position, char in enumerate(reversed(digits)):
        value = int(char)
        if position % 2:
            value = value * 2 - 9 if value > 4 else value * 2
        total += value
    return total % 10 == 0


def _card_group_lengths(lengths: list[int]) -> bool:
    """A card's groups: 4-digit groups (the last may be shorter), or Amex 4-6-5."""
    return lengths == [4, 6, 5] or (all(n % 4 == 0 for n in lengths[:-1]) and (lengths[-1] % 4 == 0 or lengths[-1] <= 4))


def _card_shaped(tokens: list[dict], text: str) -> bool:
    """Digit groups that words split apart are read as one number only if they look read out in sequence: three or
    more groups with the same joiner every time ("5555 then 5555 then ..."), or the groups are a card's (4s, or
    Amex 4-6-5). Two numbers with one word between them ("4477-4545, ZIP 73466") and a clock range, a ZIP and a
    last four in one sentence ("0900-1700, zip 94107, card ending 4427") never combine."""
    runs = _separator_runs({"tokens": tokens}, text)
    if len(runs) == 1:
        return True
    joiners = {text[a[-1]["end"]:b[0]["start"]].strip(" ,").lower() for a, b in zip(runs, runs[1:])}
    lengths = [len("".join(t["digits"] for t in run)) for run in runs]
    return (len(runs) >= 3 and len(joiners) == 1) or _card_group_lengths(lengths)


def _card_spans(chain: dict, text: str) -> list[tuple[int, int]]:
    tokens = chain["tokens"]
    digits = "".join(t["digits"] for t in tokens)
    if len(digits) >= 12 and not chain["words"]:
        return [(tokens[0]["start"], tokens[-1]["end"])]
    spans = []
    # Search the chain as written, and again without short numbers (labels such as "first 8:" or "2)").
    for view in (tokens, [t for t in tokens if len(t["digits"]) >= 3]):
        for i in range(len(view)):
            for j in range(len(view), i, -1):
                run = "".join(t["digits"] for t in view[i:j])
                if 13 <= len(run) <= 19 and _passes_luhn(run) and _card_shaped(view[i:j], text):
                    spans.append((view[i]["start"], view[j - 1]["end"]))
                    break
    return spans


def _replace(text: str, spans: list[tuple[int, int, str]]) -> str:
    """Overlapping spans are merged into one mask covering all of them (the label of the earliest, longest span),
    so a short span can never shadow a longer one that starts at the same place."""
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
    """Card numbers only (rules 4a and 4b), for text the model or the harness writes."""
    text = normalize(text)
    tokens = _tokens(text)
    spans = [(s, e, CARD_NUMBER_MASK) for chain in _chains(tokens, text) for s, e in _card_spans(chain, text)]
    return _replace(text, spans)


def mask_customer_text(text: str, previous_customer_texts: tuple[str, ...] = ()) -> str:
    """Every rule, for a customer message, given the session's earlier customer messages (oldest first)."""
    text = normalize(text)
    tokens = _tokens(text)
    chains = _chains(tokens, text)
    spans = [(s, e, CARD_NUMBER_MASK) for chain in chains for s, e in _card_spans(chain, text)]
    earlier = [t for p in previous_customer_texts[-3:] for t in _tokens(normalize(p)) if t["digits"] is not None and t["role"] is None]
    for chain in chains:
        for k in range(1, len(chain["tokens"]) + 1):
            for start, stop in ((a, b) for a in range(len(earlier)) for b in range(a + 1, len(earlier) + 1)):
                pieces = earlier[start:stop] + chain["tokens"][:k]
                combined = "".join(t["digits"] for t in pieces)
                # every fragment counts as its own group, so last fours and ZIPs typed in turn (4-5-4-5...) never combine
                if 13 <= len(combined) <= 19 and _passes_luhn(combined) and _card_group_lengths([len(t["digits"]) for t in pieces]):
                    spans.append((chain["tokens"][0]["start"], chain["tokens"][k - 1]["end"], CARD_DIGITS_MASK))
    masked_card = bool(spans) or any("[REDACTED" in p for p in previous_customer_texts[-1:])
    card_groups = []  # "5555/5555": masked only in a message that carries other card data
    for chain in chains:
        for run in _separator_runs(chain, text):
            start, end = run[0]["start"], run[-1]["end"]
            if any(start >= s and end <= e for s, e, _ in spans):
                continue
            digits = "".join(t["digits"] for t in run)
            sentence = text[max(0, text.rfind(".", 0, start) + 1):end + 40]
            if len(digits) == 3 or (len(digits) == 4 and _SECURITY_CUES.search(sentence)):
                spans.append((start, end, SECURITY_CODE_MASK))
            elif len(run) >= 2 and all(len(t["digits"]) == 4 for t in run) and not all(_is_year(t) for t in run):
                card_groups.append((start, end, CARD_DIGITS_MASK))
    has_card_data = masked_card or bool(spans) or bool(_EXPIRY_CUES.search(text))
    if has_card_data:
        spans += card_groups
        # in a message that carries card data, a bare 3-digit number is the security code wherever it sits
        # ("... / Dec 2029 / 737 / 10011"); amounts, times and identifiers have roles and are never candidates
        spans += [(t["start"], t["end"], SECURITY_CODE_MASK) for chain in chains for t in chain["tokens"]
                  if len(t["digits"]) == 3 and not any(t["start"] >= a and t["end"] <= b for a, b, _ in spans)]
        for i, t in enumerate(tokens):
            if t["role"] == "month_pair" and i + 2 < len(tokens) and tokens[i + 2]["role"] == "month_pair":
                spans.append((t["start"], tokens[i + 2]["end"], EXPIRY_MASK))
        spans += [(m.start(), m.end(), EXPIRY_MASK) for m in _MONTH_YEAR.finditer(text)]
    return _replace(text, spans)
