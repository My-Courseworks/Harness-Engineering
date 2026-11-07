"""Score the card-data masker: recall on what must be masked, precision on what must come through unchanged.

    python eval_redaction.py tuning     # the corpus the masker was developed against
    python eval_redaction.py heldout    # the corpus written before the masker and run once, afterwards
    python eval_redaction.py fuzz       # seeded random renderings of the test card (also split across messages),
                                        # and random text to keep (also last fours and ZIPs typed over several messages)

No model calls. A "mask" case passes if the masked output no longer contains the test card number (digits in
order, any gaps, number words up to "ninety-nine" included), two adjacent groups of it, its last group, the test
security code as a whole token, or the test expiry (12/29, twelve twenty-nine, Dec 2029). The scanner is the
suites' store scanner (cardcare/scenario.py). A "keep" case passes only if the output equals the normalised input
exactly, so any over-redaction fails it.
Writes evidence/redaction/<corpus>.md.
"""

import random
import re
import sys
from pathlib import Path

from cardcare.heldout import REDACTION_HELDOUT
from cardcare.masking import mask_customer_text, normalize
from cardcare.redaction_cases import REDACTION_TUNING
from cardcare.scenario import _TEST_CVV_SCAN, _TEST_EXPIRY_SCAN, _TEST_PAN_FRAGMENT_SCAN, _TEST_PAN_SCAN, _auditor_text

CODE_DIR = Path(__file__).resolve().parent
_DIGIT_WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
_SEPARATORS = [" ", "-", "\u2013", "\u2014", "\u2212", "\u00a0", "\u202f", "\u2009", "\t", ".", "/", "_", "\u00b7", "|", ",", " - ",
               "  ", "\u200b", "\uff0d", " / "]
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
    """The test card sent over 2 or 3 messages; the last piece (the current message) must be masked."""
    cut = sorted(rng.sample([4, 8, 12], rng.choice([1, 2])))
    pan, pieces = "5555555555554444", []
    for a, b in zip([0] + cut, cut + [16]):
        pieces.append(" ".join(pan[i:i + 4] for i in range(a, b, 4)))
    lead = ["first part: {}", "it starts {}", "{}", "then {}", "next {}"]
    previous = tuple(rng.choice(lead).format(piece) for piece in pieces[:-1])
    return rng.choice(["and the rest {}", "last bit {}", "{}", "ends {}"]).format(pieces[-1]), previous, "mask"


def _fuzz_typed_in_turn(rng: random.Random) -> tuple[str, tuple, str]:
    """Last fours, ZIPs and ids typed over several messages (wrong attempts, corrections): all of it must be kept."""
    line = lambda: rng.choice(["card ending {a}, ZIP {z}", "try {a} and {z}", "sorry, {a} / {z}", "last four {a}, zip {z}",
                               "case C-{c}, card ending {a}", "reference {r}, ZIP {z}"]).format(
        a=rng.randint(1000, 9999), z=rng.randint(10000, 99999), c=rng.randint(5000, 5999), r=rng.randint(10000, 99999))
    return line(), tuple(line() for _ in range(rng.randint(1, 3))), "keep"


def fuzz_corpus(seed: int = 7, size: int = 1000) -> list[tuple[str, tuple, str]]:
    rng = random.Random(seed)
    return ([(_fuzz_pan(rng), (), "mask") for _ in range(size)] + [_fuzz_split_pan(rng) for _ in range(size // 4)]
            + [(_fuzz_keep(rng), (), "keep") for _ in range(size)] + [_fuzz_typed_in_turn(rng) for _ in range(size // 4)])


CORPORA = {"tuning": REDACTION_TUNING, "heldout": REDACTION_HELDOUT, "fuzz": fuzz_corpus()}


def card_data_left(text: str) -> bool:
    audited = _auditor_text(text.encode())
    return bool(_TEST_PAN_SCAN.search(audited) or _TEST_PAN_FRAGMENT_SCAN.search(audited) or _TEST_CVV_SCAN.search(audited)
                or _TEST_EXPIRY_SCAN.search(audited) or re.search(r"(?<!\d)4444(?!\d)", audited))


def main() -> None:
    name = sys.argv[1] if len(sys.argv) > 1 else "tuning"
    rows, mask_ok, keep_ok, masks, keeps = [], 0, 0, 0, 0
    for text, previous, expected in CORPORA[name]:
        out = mask_customer_text(text, previous)
        if expected == "mask":
            masks += 1
            ok = not card_data_left(out)
            mask_ok += ok
        else:
            keeps += 1
            ok = out == normalize(text)
            keep_ok += ok
        rows.append((ok, expected, text, previous, out))
    lines = [f"# Masker evaluation: {name} corpus", "", f"Generated by `python eval_redaction.py {name}`. No model calls.", "",
             f"- **recall** (card data removed where it must be): {mask_ok}/{masks}",
             f"- **precision** (text kept unchanged where it must be): {keep_ok}/{keeps}", "",
             ("Every failure, then the first 40 cases (the corpus is generated: `fuzz_corpus()` with seed 7)." if name == "fuzz" else ""), "",
             "| result | expected | input (previous messages) | output |", "|---|---|---|---|"]
    shown = [r for r in rows if not r[0]] + rows[:40] if name == "fuzz" else rows
    for ok, expected, text, previous, out in shown:
        prev = f" (after: {' / '.join(previous)})" if previous else ""
        cell = lambda v: repr(v).replace("|", "\\|")
        lines.append(f"| {'pass' if ok else '**FAIL**'} | {expected} | {cell(text)}{cell(prev) if prev else ''} | {cell(out)} |")
    out_path = CODE_DIR / "evidence" / "redaction" / f"{name}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:6]))
    for ok, expected, text, previous, out in rows:
        if not ok:
            print("FAIL", expected, repr(text)[:90], "->", repr(out)[:120])


if __name__ == "__main__":
    main()
