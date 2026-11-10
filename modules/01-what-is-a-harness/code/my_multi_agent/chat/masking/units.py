"""
"""

import re

from chat.masking.internal_names import has_internal_name
from chat.masking.utils import Kind, CleanUnit


# Shown when every unit of an answer had to be withheld.
NOTHING_TO_SHOW = "I can't go into how I work internally, but I'm glad to help with a request."

# ----------------------------- units ---------------------------------------
# A unit is the smallest piece of an answer that is checked, and then either
# shown, shown rewritten, or not shown. Nothing is drawn before its unit closes,
# so nothing ever has to be taken back.

def split_units(text: str, final: bool = False) -> list[str]:
    """Split text into closed units. The returned units concatenate to a prefix
    of text; whatever is left over is still open and must not be drawn yet.

    - a complete line is a unit (covers paragraphs, bullets, headings),
    - consecutive table lines form one unit, closed by the first non-table line,
    - a fenced code block is one unit, closed by its closing fence.
    With final=True the remainder is returned as a last unit as well.
    """
    lines = text.split("\n")
    complete = [line + "\n" for line in lines[:-1]]
    rest = lines[-1]

    units: list[str] = []
    i = 0
    while i < len(complete):
        stripped = complete[i].strip()
        if stripped.startswith("```"):
            j = i + 1
            while j < len(complete) and not complete[j].strip().startswith("```"):
                j += 1
            if j == len(complete):
                break                                  # fence still open
            units.append("".join(complete[i:j + 1]))
            i = j + 1
        elif stripped.startswith("|"):
            j = i
            while j < len(complete) and complete[j].strip().startswith("|"):
                j += 1
            if j == len(complete):
                break                                  # table may still grow
            units.append("".join(complete[i:j]))
            i = j
        else:
            units.append(complete[i])
            i += 1

    if final:
        remainder = "".join(complete[i:]) + rest
        if remainder:
            units.append(remainder)
    return units


def clean_table(unit: str, patterns: dict[Kind, re.Pattern[str]]) -> str | None:
    """Drop the rows that name internals. A table left with no data rows is dropped."""
    rows = unit.splitlines(keepends=True)
    kept = [row for row in rows if not has_internal_name(row, patterns)]
    data_rows = [row for row in kept[2:] if row.strip()]
    return "".join(kept) if data_rows else None





async def clean_text(text: str, clean_unit: CleanUnit) -> str:
    """Whole-text form: every unit cleaned or withheld, rejoined."""
    cleaned = [await clean_unit(unit) for unit in split_units(text, final=True)]
    return "".join(unit for unit in cleaned if unit is not None).strip() or NOTHING_TO_SHOW
