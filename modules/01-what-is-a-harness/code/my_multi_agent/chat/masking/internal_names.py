"""
Finding the internal names, and asking whether a piece of text contains one.

The names are collected by walking the agent tree: every agent, every tool an
agent carries, plus the tool names ADK injects at call time. They are compiled
into one regular expression per kind. Detection is by identifier only: text
that describes the design without naming anything is not caught here.
"""

import re

from google.adk.agents import BaseAgent, LlmAgent

from chat.masking.utils import Kind


# Tools ADK injects into requests at call time. canonical_tools() never returns
# them, so the tree walk cannot find them; the model can still name them.
ADK_INJECTED_TOOL_NAMES = {"transfer_to_agent"}

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

def has_internal_name(text: str, patterns: dict[Kind, re.Pattern[str]]) -> bool:
    """True if any kind of internal name appears in text."""
    return any(pattern.search(text) for pattern in patterns.values())


def compile_name_patterns(internal_names: dict[Kind, set[str]]) -> dict[Kind, re.Pattern[str]]:
    """One compiled pattern per kind, so each kind can get its own substitute."""
    return {kind: _compile_pattern(names) for kind, names in internal_names.items()}