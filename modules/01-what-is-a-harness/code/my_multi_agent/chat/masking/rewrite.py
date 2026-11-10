"""
"""

import re

from google.adk.models import BaseLlm
from google.adk.models.llm_request import LlmRequest

from google.genai import types

from chat.masking.internal_names import has_internal_name
from chat.masking.units import clean_table
from chat.masking.utils import CleanUnit, Kind, response_text


UNIT_REWRITE_INSTRUCTION = """You are given one line from an assistant's reply to an end user.
Rewrite it so it does not mention or allude to internal tools, functions, agents,
sub-agents, delegation or routing.
- Keep every fact, number, date, person's name and decision exactly as given. Add nothing.
- Keep any markdown marker at the start of the line (bullet, number, heading).
- If the line is only about internals and nothing would remain, reply with exactly: DROP
Output only the rewritten line."""

def build_unit_cleaner(patterns: dict[Kind, re.Pattern[str]], rewriter: BaseLlm) -> CleanUnit:
    """Return clean_unit(unit) -> text to show, or None to withhold the unit.

    Clean units pass through untouched. A prose unit that names internals is
    rewritten by the model and rechecked; if that fails it is withheld. Tables
    lose their offending rows; code blocks that name internals are withheld.
    Results are cached, so the live stream and the after-model callback pay for
    one model call per offending unit between them.
    """
    cache: dict[str, str | None] = {}

    async def rewrite(unit: str) -> str | None:
        request = LlmRequest(
            contents=[types.Content(role="user", parts=[types.Part(text=unit.strip())])],
            config=types.GenerateContentConfig(system_instruction=UNIT_REWRITE_INSTRUCTION),
        )
        try:
            # stream=False yields exactly one complete response.
            async for response in rewriter.generate_content_async(request, stream=False):
                if response.error_code:
                    return None
                rewritten = response_text(response).strip()
                if not rewritten or rewritten == "DROP" or has_internal_name(rewritten, patterns):
                    return None
                return rewritten + "\n"
        except Exception:
            return None
        return None

    async def clean_unit(unit: str) -> str | None:
        if not has_internal_name(unit, patterns):
            return unit
        if unit not in cache:
            stripped = unit.lstrip()
            if stripped.startswith("|"):
                cache[unit] = clean_table(unit, patterns)
            elif stripped.startswith("```"):
                cache[unit] = None
            else:
                cache[unit] = await rewrite(unit)
        return cache[unit]

    return clean_unit