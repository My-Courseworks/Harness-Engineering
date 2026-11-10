"""
"""

import re
from typing import Literal

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

# What each kind of internal name is replaced with when the deterministic floor runs.
SUBSTITUTES: dict[Kind, str] = {
    "agent": "a colleague",
    "tool": "an internal tool",
}

REWRITE_INSTRUCTION = """You rewrite an assistant's reply so it never mentions how the assistant works internally.
Rules:
- Write in first person about outcomes, never about process or delegation.
- Remove every reference to tools, functions, agents, sub-agents, or internal components.
- Keep every fact, number, date, person's name and decision exactly as given. Add nothing.
- Keep the original language, tone, and markdown formatting.
- Output only the rewritten reply."""


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


def substitute_internals(text: str, patterns: dict[Kind, re.Pattern[str]]) -> str:
    """Deterministic floor: swap every internal name for the neutral phrase of its kind."""
    for kind, pattern in patterns.items():
        text = pattern.sub(SUBSTITUTES[kind], text)
    return text


def response_text(llm_response: LlmResponse) -> str:
    """Concatenate the non-thought text parts of a model response; empty if none."""
    content = llm_response.content
    if content is None or not content.parts:
        return ""
    return "".join(part.text for part in content.parts if part.text and not part.thought)


async def rewrite_without_internals(rewriter: BaseLlm, text_to_rewrite: str,
                                    patterns: dict[Kind, re.Pattern[str]]) -> str:
    """Return a version of text_to_rewrite with no internal names in it.

    Prefers a one-shot model rewrite so the sentence still reads naturally.
    Falls back to plain substitution if the model errors, returns nothing,
    or still leaks a name. Never raises and never returns empty text, so the
    caller can store the result without inspecting it.
    """
    fallback = substitute_internals(text_to_rewrite, patterns)
    request = LlmRequest(
        contents=[types.Content(role="user", parts=[types.Part(text=text_to_rewrite)])],
        config=types.GenerateContentConfig(system_instruction=REWRITE_INSTRUCTION),
    )
    try:
        # stream=False yields exactly one complete response.
        async for response in rewriter.generate_content_async(request, stream=False):
            if response.error_code:
                return fallback
            rewritten = response_text(response).strip()
            if not rewritten or has_internal_name(rewritten, patterns):
                return fallback
            return rewritten
    except Exception:
        return fallback
    return fallback


def build_mask_callback(patterns: dict[Kind, re.Pattern[str]], masking_model: BaseLlm) -> AfterModelCallback:
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

        display = await rewrite_without_internals(rewriter=masking_model, text_to_rewrite=llm_resp_text, patterns=patterns)

        # retain all other fields of llm_response.custom_metadata if it exists, or initalize it to an empty dict
        # and then add the harness display text to store it so that it can be displayed during replay.
        llm_response.custom_metadata = {**(llm_response.custom_metadata or {}), DISPLAY_TEXT_KEY: display}

        return llm_response

    return mask_internals
