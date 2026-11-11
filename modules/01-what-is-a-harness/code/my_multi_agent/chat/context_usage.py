"""
How much of the model's context window a conversation occupies, read from the
token counts ADK attaches to every model-call event.
"""

from typing import Sequence

from google.adk.events import Event


def tokens_in_context(events: Sequence[Event], agent_name: str) -> int | None:
    """
    The size of this agent's most recent model call among the events: the tokens it
    was sent plus the tokens it answered with. That is about what its next call
    starts from.

    Returns None when the events hold no model call by this agent.

    Each agent has its own context. Pass the root agent's name: its context is the
    one that grows across a session, while a task sub-agent's starts nearly empty
    on every delegation.
    """
    for event in reversed(events):
        usage = event.usage_metadata
        if event.author == agent_name and usage and usage.total_token_count:
            return usage.total_token_count
    return None
