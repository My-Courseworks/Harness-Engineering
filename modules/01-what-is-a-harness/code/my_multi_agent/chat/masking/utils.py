"""
"""

from typing import Awaitable, Callable, Literal

from google.adk.models.llm_response import LlmResponse


# The kinds of internal name the model can see. A Literal, not a free string,
# so a typo in a key is a type error rather than a KeyError at the first hit.
Kind = Literal["agent", "tool"]

CleanUnit = Callable[[str], Awaitable[str | None]]

def response_text(llm_response: LlmResponse) -> str:
    """Concatenate the non-thought text parts of a model response; empty if none."""
    content = llm_response.content
    if content is None or not content.parts:
        return ""
    return "".join(part.text for part in content.parts if part.text and not part.thought)
