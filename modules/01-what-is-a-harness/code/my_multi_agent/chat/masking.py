"""
"""

import re
from typing import Awaitable, Callable, Literal

from google.adk.agents import BaseAgent, LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.agents.llm_agent import AfterModelCallback
from google.adk.models import BaseLlm
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai import types

# The kinds of internal name the model can see. A Literal, not a free string,
# so a typo in a key is a type error rather than a KeyError at the first hit.
Kind = Literal["agent", "tool"]

# Key under which the callback stores the rewritten, name-free answer in
# event.custom_metadata. Readers (turn.py, replay.py) prefer it when present.
DISPLAY_TEXT_KEY = "harness:display_text"

# Tools ADK injects into requests at call time. canonical_tools() never returns
# them, so the tree walk cannot find them; the model can still name them.
ADK_INJECTED_TOOL_NAMES = {"transfer_to_agent"}

# Shown when every unit of an answer had to be withheld.
NOTHING_TO_SHOW = "I can't go into how I work internally, but I'm glad to help with a request."

# Runner-wide instruction for masked roles: prevention, so the holdback rarely has to act.
MASKED_ROLE_INSTRUCTION = """The person you are talking to is an end user of this service.
Speak in first person about outcomes and results only.
Never mention or describe tools, functions, agents, sub-agents, delegation, routing,
or how you work internally, even when asked directly.
If asked what you can do, list the kinds of requests you can help with, nothing more."""

UNIT_REWRITE_INSTRUCTION = """You are given one line from an assistant's reply to an end user.
Rewrite it so it does not mention or allude to internal tools, functions, agents,
sub-agents, delegation or routing.
- Keep every fact, number, date, person's name and decision exactly as given. Add nothing.
- Keep any markdown marker at the start of the line (bullet, number, heading).
- If the line is only about internals and nothing would remain, reply with exactly: DROP
Output only the rewritten line."""


async def collect_internal_names(agent: BaseAgent) -> dict[Kind, set[str]]:
    """
    """
    names: dict[Kind, set[str]] = {"agent": set(), "tool": set()}

    # add itself
    names["agent"].add(agent.name)

    # add its tools available directly.
    # Note: the subagents due to task mode association
    # also get counted as root-agent's tools,
    # hence the usage of a set.
    # Only LlmAgents carry tools; a workflow agent in the tree has none.
    if isinstance(agent, LlmAgent):
        for tool in await agent.canonical_tools():
            # A tool that wraps an agent (AgentTool / task-mode sub-agent) is an
            # agent for substitution purposes; the recursion below collects its tree.
            if getattr(tool, "agent", None) is not None:
                names["agent"].add(tool.name)
            else:
                names["tool"].add(tool.name)

    for sub_agent in agent.sub_agents:
        sub_names = await collect_internal_names(sub_agent)
        names["agent"] |= sub_names["agent"]
        names["tool"] |= sub_names["tool"]

    names["tool"] |= ADK_INJECTED_TOOL_NAMES

    # guarantee the two sets are disjoint, whatever the wrappers looked like.
    names["tool"] -= names["agent"]
    return names


def _compile_pattern(internal_names: set[str]) -> re.Pattern[str]:
    """One regex that matches any of the given names as a whole word, plus the
    decoration models wrap it in: an article before, backticks, call syntax,
    and a trailing 'tool' or 'agent' after."""
    # longest first, so a name that is a prefix of another cannot win early;
    # drop empties, since an empty alternative would match everywhere.
    names = sorted((n for n in internal_names if n), key=len, reverse=True)
    if not names:
        return re.compile(r"(?!x)x")     # matches nothing, ever
    alternation = "|".join(re.escape(n) for n in names)
    return re.compile(
        r"(?:\b(?:the|a|an|our|my)\s+)?"       # optional article, swallowed
        r"`?\b(?:" + alternation + r")\b"       # the name itself
        r"(?:\([^)]*\))?`?"                     # optional (args) and closing backtick
        r"(?:\s+(?:tool|agent|sub-?agent))?",   # optional trailing noun, swallowed
        re.IGNORECASE,
    )


def compile_name_patterns(internal_names: dict[Kind, set[str]]) -> dict[Kind, re.Pattern[str]]:
    """One compiled pattern per kind, so each kind can get its own substitute."""
    return {kind: _compile_pattern(names) for kind, names in internal_names.items()}


def has_internal_name(text: str, patterns: dict[Kind, re.Pattern[str]]) -> bool:
    """True if any kind of internal name appears in text."""
    return any(pattern.search(text) for pattern in patterns.values())


def response_text(llm_response: LlmResponse) -> str:
    """Concatenate the non-thought text parts of a model response; empty if none."""
    content = llm_response.content
    if content is None or not content.parts:
        return ""
    return "".join(part.text for part in content.parts if part.text and not part.thought)


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


def _clean_table(unit: str, patterns: dict[Kind, re.Pattern[str]]) -> str | None:
    """Drop the rows that name internals. A table left with no data rows is dropped."""
    rows = unit.splitlines(keepends=True)
    kept = [row for row in rows if not has_internal_name(row, patterns)]
    data_rows = [row for row in kept[2:] if row.strip()]
    return "".join(kept) if data_rows else None


CleanUnit = Callable[[str], Awaitable[str | None]]


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
                cache[unit] = _clean_table(unit, patterns)
            elif stripped.startswith("```"):
                cache[unit] = None
            else:
                cache[unit] = await rewrite(unit)
        return cache[unit]

    return clean_unit


async def clean_text(text: str, clean_unit: CleanUnit) -> str:
    """Whole-text form: every unit cleaned or withheld, rejoined."""
    cleaned = [await clean_unit(unit) for unit in split_units(text, final=True)]
    return "".join(unit for unit in cleaned if unit is not None).strip() or NOTHING_TO_SHOW


def build_mask_callback(patterns: dict[Kind, re.Pattern[str]], clean_unit: CleanUnit) -> AfterModelCallback:
    """
    """

    async def mask_internals(callback_context: CallbackContext, llm_response: LlmResponse) -> LlmResponse | None:
        """
        """
        llm_resp_text = response_text(llm_response=llm_response)

        # ignore partial events
        if llm_response.partial or not llm_resp_text:
            return None
        if not has_internal_name(llm_resp_text, patterns):
            # no internal names found in llm response text, so ignore
            return None

        # same units, same cleaner (and cache) as the live stream, so what is
        # persisted for replay is what the user saw.
        display = await clean_text(llm_resp_text, clean_unit)

        # retain all other fields of llm_response.custom_metadata if it exists, or initalize it to an empty dict
        # and then add the harness display text to store it so that it can be displayed during replay.
        llm_response.custom_metadata = {**(llm_response.custom_metadata or {}), DISPLAY_TEXT_KEY: display}

        return llm_response

    return mask_internals
