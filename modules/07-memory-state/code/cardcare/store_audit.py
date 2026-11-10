"""The auditor's scanner: does a store file (or a masked conversation) still hold a known card number, code or expiry?

It is written independently of cardcare/masking.py and shares no code with it, so a blind spot in the masker is not
also a blind spot here. It reads bytes the way an auditor would:
  - decode UTF-8, undo JSON \\uXXXX escapes, apply NFKC, and map every Unicode decimal digit to ASCII;
  - read number words two ways: as digits ("five" -> 5, "fifty-five" -> 55, "double five" -> 55, "oh" -> 0, the
    teens and tens), and not at all; a digit that came from a word is marked as such;
  - look for each secret's digits in order. Anything that is not a digit may sit between two of them (separators,
    newlines, list markers, sentences, words), up to MAX_GAP characters; a digit that came from a word may be
    skipped (a dictated "the first FOUR are 5555, the next FOUR are 5555..." still matches); a written digit that
    does not match ends the attempt. A match must also fit in MAX_SPAN characters.
A secret is a card number (13-19 digits), a security code (3-4 digits, matched as a whole token: never inside a
longer number, an id or a hex string) or an expiry ("MM/YY", matched as MM and YY or 20YY with a separator, as a
month name and year, or spelled).
"""

import json
import re
import sqlite3
import unicodedata
from contextlib import closing
from pathlib import Path

DEFAULT_SECRETS = {"pans": ["5555555555554444"], "codes": ["737"], "expiries": ["12/29"]}
# Published test numbers only; no real card.
TEST_PANS = ["5555555555554444", "4111111111111111", "4242424242424242", "378282246310005", "6011111111111117",
             "2223003122003222", "3530111333300000", "4000056655665556"]
MAX_GAP = 60
MAX_SPAN = 600

_UNITS = {"zero": 0, "oh": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}
_TEENS = {"ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16,
          "seventeen": 17, "eighteen": 18, "nineteen": 19}
_TENS = {"twenty": 2, "thirty": 3, "forty": 4, "fourty": 4, "fifty": 5, "sixty": 6, "seventy": 7, "eighty": 8, "ninety": 9}
_MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
_WORD = re.compile(r"[A-Za-z]+")


def store_text(path: Path) -> str:
    """A store file as the text the scanner reads: its raw bytes, and every string it holds as a string.

    Round 5 found the raw bytes alone misleading for LangGraph's checkpoints. They are msgpack: a string is followed
    directly by the header byte of the next value, which is not text. Dropping such bytes glued a stored string to its
    neighbours ("...expiry: July / 29additional_kwargs", "entered325096id"), so a secret that began or ended a stored
    string had no boundary and matched nothing. Undecodable bytes are now separators, and an SQLite file is also read as
    a database: every text value, and every string inside a blob decoded as msgpack (nested extension payloads too), on
    a line of its own. The raw bytes stay in the text because they also cover the write-ahead log and freed pages."""
    raw = Path(path).read_bytes()
    return raw.decode("utf-8", errors="replace").replace("\ufffd", " ") + "\n" + "\n".join(_sqlite_strings(Path(path), raw))


def _sqlite_strings(path: Path, raw: bytes) -> list[str]:
    if not raw.startswith(b"SQLite format 3\x00"):
        return []
    found: list[str] = []
    try:
        with closing(sqlite3.connect(f"file:{path}?mode=ro", uri=True, timeout=30)) as conn:
            for (table,) in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall():
                for row in conn.execute(f'SELECT * FROM "{table}"'):
                    for value in row:
                        if isinstance(value, str):
                            found.append(value)
                        elif isinstance(value, (bytes, bytearray, memoryview)):
                            found += _blob_strings(bytes(value))
    except sqlite3.Error:
        pass  # a file that cannot be opened as a database is still scanned as bytes
    return found


def _blob_strings(blob: bytes) -> list[str]:
    """Every string inside a msgpack value; a blob that is not msgpack is read as text."""
    try:
        import ormsgpack
    except ImportError:
        return [blob.decode("utf-8", errors="replace").replace("\ufffd", " ")]

    def unpack(data: bytes):
        return ormsgpack.unpackb(data, ext_hook=lambda _code, payload: unpack(payload), option=ormsgpack.OPT_NON_STR_KEYS)

    def strings(value) -> list[str]:
        if isinstance(value, str):
            return [value]
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            # A code or a card number a model passed as a number is stored as one (round-5 review, nb 3). It is written
            # the way JSON writes a number value, so that the two frameworks read alike: a token count of 123 is not a
            # security code in either (code_present), and two counts on neighbouring lines are not an expiry.
            return [f'"number": {value}']
        if isinstance(value, (bytes, bytearray)):
            return _blob_strings(bytes(value)) if value else []
        if isinstance(value, dict):
            return [s for pair in value.items() for item in pair for s in strings(item)]
        if isinstance(value, (list, tuple)):
            return [s for item in value for s in strings(item)]
        return []

    try:
        return strings(unpack(blob))
    except Exception:  # not msgpack (JSON metadata, plain bytes)
        return [blob.decode("utf-8", errors="replace").replace("\ufffd", " ")]


def auditor_text(data: bytes | str) -> str:
    text = data.decode("utf-8", errors="replace").replace("\ufffd", " ") if isinstance(data, bytes) else data
    text = re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), text)
    text = unicodedata.normalize("NFKC", text)
    # a UUID (a LangGraph message or checkpoint id) is never card data; its digit groups ("…-a296-4321-…") are not codes
    # (also back to back), replaced by filler of the same length so the distance between other digits does not shrink
    text = re.sub(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}", lambda m: "#" * len(m.group()), text)
    # nor is an ISO date-time: LangGraph stamps every checkpoint with the wall clock, and "2026-11-10T17:43:21.497049+00:00"
    # holds "43:21", which read as the security code 4321 in a round-6 tuning run that happened to cross that second
    text = re.sub(r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?", lambda m: "#" * len(m.group()), text)
    return "".join(str(unicodedata.decimal(ch)) if ch.isdecimal() and not ch.isascii() else ch for ch in text)


def _spoken_units(text: str) -> list[tuple[int, int, str]]:
    """(start, end, digits) for every spoken number: "five", "fifteen", "fifty", "fifty-five", "double five"."""
    units = []
    for match in _WORD.finditer(text):
        if units and match.start() < units[-1][1]:
            continue  # already consumed by a compound
        word, end = match.group().lower(), match.end()
        digits = None
        if word in _TENS:
            tail = re.match(r"[\s-]*([A-Za-z]+)", text[end:end + 12])
            if tail and tail.group(1).lower() in _UNITS and tail.group(1).lower() not in ("zero", "oh"):
                digits, end = f"{_TENS[word]}{_UNITS[tail.group(1).lower()]}", end + tail.end()
            else:
                digits = f"{_TENS[word]}0"
        elif word in _TEENS:
            digits = str(_TEENS[word])
        elif word in _UNITS:
            digits = str(_UNITS[word])
        elif word in ("double", "triple"):
            tail = re.match(r"\s+([A-Za-z]+|\d)", text[end:end + 10])
            unit = None
            if tail:
                unit = tail.group(1) if tail.group(1).isdigit() else _UNITS.get(tail.group(1).lower())
            if unit is not None:
                digits, end = str(unit) * (2 if word == "double" else 3), end + tail.end()
        if digits:
            units.append((match.start(), end, digits))
    return units


def _stream(text: str, words_as_digits: bool) -> list[tuple[str, int, bool]]:
    """(digit, position, came_from_a_word) for every digit, written or (optionally) spoken, in order."""
    out = [(ch, i, False) for i, ch in enumerate(text) if ch.isdigit()]
    if words_as_digits:
        out += [(d, start, True) for start, _, digits in _spoken_units(text) for d in digits]
        out.sort(key=lambda item: item[1])
    return out


def _find_in_order(stream, secret: str, text: str) -> bool:
    """Is `secret` spelled out by `stream` in order (gaps, skippable spoken digits) within MAX_SPAN characters?"""
    n = len(stream)

    def walk(start: int) -> bool:
        # depth-first with backtracking: at each needed digit, try every candidate position reachable without
        # crossing a written digit that does not match and without a gap over MAX_GAP characters
        stack = [(start, 1)]
        while stack:
            index, matched = stack.pop()
            if matched == len(secret):
                return True
            position = stream[index][1]
            for j in range(index + 1, n):
                digit, pos, spoken = stream[j]
                if pos - position > MAX_GAP or pos - stream[start][1] > MAX_SPAN:
                    break
                if digit == secret[matched]:
                    stack.append((j, matched + 1))
                if not spoken:
                    break  # a written digit is never skipped
        return False

    return any(stream[i][0] == secret[0] and walk(i) for i in range(n))


def _views(text: str) -> list[list[tuple[str, int, bool]]]:
    return [_stream(text, words_as_digits=False), _stream(text, words_as_digits=True)]


def pan_present(text: str, pan: str) -> bool:
    return any(_find_in_order(view, pan, text) for view in _views(text))


def _fragments(pan: str) -> list[str]:
    """Two adjacent groups of the number as printed (4-6-5 for Amex, 4s otherwise), unless the fragment is one digit
    repeated (a "1111 1111" also comes from guessed last fours)."""
    groups = [pan[:4], pan[4:10], pan[10:]] if len(pan) == 15 else [pan[i:i + 4] for i in range(0, len(pan), 4)]
    pieces = [a + b for a, b in zip(groups, groups[1:])]
    return [p for p in pieces if len(set(p)) > 1 or pan == "5555555555554444"]


def fragment_present(text: str, pan: str) -> bool:
    """A partial leak: two adjacent groups of a known number, written as digits with at most 6 characters between."""
    for piece in _fragments(pan):
        half = len(piece) // 2 if len(pan) != 15 else 4
        first, second = piece[:half], piece[half:]
        pattern = r"(?<!\d)" + r"\D{0,2}".join(first) + r"\D{1,6}" + r"\D{0,2}".join(second) + r"(?!\d)"
        if re.search(pattern, text):
            return True
    return False


def code_present(text: str, code: str) -> bool:
    """A whole-token match, never a JSON number value: ADK stores usage metadata such as "total_token_count": 4321 in
    its events, while anything a customer or the model says is inside a JSON string."""
    for view_text in (text, _spoken_to_digits(text)):
        pattern = r"(?<![0-9A-Za-z.])" + r"[^0-9A-Za-z]{0,2}".join(code) + r"(?![0-9A-Za-z])"
        for match in re.finditer(pattern, view_text):
            if not re.search(r'":\s*$', view_text[max(0, match.start() - 4):match.start()]):
                return True
    return False


def expiry_present(text: str, expiry: str) -> bool:
    month, year = expiry.split("/")
    month_number = int(month)
    month_name = _MONTHS[month_number - 1]
    yy = year[-2:]
    sep = r"\s*[/\-.]\s*|\s+"
    patterns = [
        rf"(?<![0-9A-Za-z\-:/.$]){month_number:02d}(?:{sep})(?:20)?{yy}(?![0-9A-Za-z])(?![:.]\d)",
        rf"(?<![0-9A-Za-z\-:/.$]){month_number}(?:{sep})(?:20)?{yy}(?![0-9A-Za-z])(?![:.]\d)" if month_number < 10 else None,
        # "July 29", "Jul. 2029", and (round 5: an unscripted customer wrote "expiry: July / 29", which this pattern did not
        # see) "July / 29", "Jul/29", "Jul '29", "July of 29"
        rf"\b{month_name}[a-z]*[\s.,/'’\-]{{0,4}}(?:of\s+)?['’]?(?:20\s?)?{yy}\b",
    ]
    for view_text in (text, _spoken_to_digits(text)):
        for pattern in filter(None, patterns):
            if re.search(pattern, view_text, re.IGNORECASE):
                return True
    return False


def spoken_to_digits(text: str) -> str:
    """The text with every spoken number replaced by its digits: the view in which a secret typed in words is found."""
    return _spoken_to_digits(text)


def _spoken_to_digits(text: str) -> str:
    """The text with every spoken number replaced by its digits (for the code and expiry patterns)."""
    pieces, last = [], 0
    for start, end, digits in _spoken_units(text):
        pieces += [text[last:start], digits]
        last = end
    return "".join(pieces + [text[last:]])


def secrets_left(text: str, secrets: dict) -> list[str]:
    """Which of the secrets (pans, codes, expiries) are still recoverable from `text`."""
    text = auditor_text(text)
    found = []
    for pan in secrets.get("pans", []):
        if pan_present(text, pan):
            found.append(f"card number {pan[:4]}…{pan[-4:]}")
        elif fragment_present(text, pan):
            found.append(f"card number fragment {pan[:4]}…{pan[-4:]}")
    found += [f"security code {c}" for c in secrets.get("codes", []) if code_present(text, c)]
    found += [f"expiry {e}" for e in secrets.get("expiries", []) if expiry_present(text, e)]
    return found


def merged_secrets(*extra: dict | None) -> dict:
    merged = {key: list(values) for key, values in DEFAULT_SECRETS.items()}
    for secrets in extra:
        for key, values in (secrets or {}).items():
            merged.setdefault(key, [])
            merged[key] += [v for v in values if v not in merged[key]]
    return merged


def card_data_locations(paths: list, secrets: dict | None = None) -> dict[str, list[str]]:
    """Which store files hold any of the secrets (defaults plus `secrets`), in any formatting or encoding."""
    secrets = merged_secrets(secrets)
    hits: dict[str, list[str]] = {}
    for path in paths:
        for finding in secrets_left(store_text(path), secrets):
            hits.setdefault(finding, []).append(path.name)
    return hits


def describe(secrets: dict) -> str:
    return json.dumps({k: [v[:4] + "…" if len(v) > 8 else v for v in vs] for k, vs in secrets.items()})
