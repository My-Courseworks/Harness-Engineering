"""
The entry point of the masking feature, and the callback that serves replay.

apply_masking is the only place that looks at the user's role. For a masked
role it builds the unit cleaner, attaches a callback to the root agent, and
returns the cleaner for the live stream; for an admin, or with the feature
off, it does nothing and returns None. The callback stores the cleaned answer
beside the raw one in custom_metadata, so a resumed session shows what the
user originally saw. The model's own content is never modified.
"""

import re

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.agents.llm_agent import AfterModelCallback
from google.adk.models import BaseLlm
from google.adk.models.llm_response import LlmResponse

# ------------------------------- LOCAL IMPORTS -------------------------------
from chat.masking.internal_names import collect_internal_names, compile_name_patterns, has_internal_name
from chat.masking.rewrite import build_unit_cleaner
from chat.masking.utils import Kind, CleanUnit, response_text
from chat.masking.units import clean_text


# Key under which the callback stores the rewritten, name-free answer in
# event.custom_metadata. Readers (turn.py, replay.py) prefer it when present.
DISPLAY_TEXT_KEY = "harness:display_text"

# Runner-wide instruction for masked roles: prevention, so the holdback rarely has to act.
MASKED_ROLE_INSTRUCTION = """The person you are talking to is an end user of this service.
Speak in first person about outcomes and results only.
Never mention or describe tools, functions, agents, sub-agents, delegation, routing,
or how you work internally, even when asked directly.
If asked what you can do, list the kinds of requests you can help with, nothing more."""

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


async def apply_masking(root_agent: LlmAgent, user_role: str, rewriter: BaseLlm,
                        is_masking_enabled: bool = True) -> CleanUnit | None:
    # Masking: non-admins must never see internal agent or tool names.
    # The role is resolved exactly once, here; everything downstream receives
    # functions and never asks who the user is. Three layers, same patterns:
    #   - a runner-wide instruction, so the model rarely narrates internals;
    #   - clean_unit on the View: the live stream prints a unit only after it
    #     has been checked, rewritten if needed, or withheld;
    #   - a callback on the root agent that persists the same clean text for replay.
    # rewriter is the model that rewrites a line naming an internal: the same one the agents run on.
    # TODO: change the role check to an Enum once this starts working
    clean_unit = None
    if is_masking_enabled and user_role != "admin":
        patterns = compile_name_patterns(await collect_internal_names(root_agent))
        clean_unit = build_unit_cleaner(patterns, rewriter)
        root_agent.after_model_callback = build_mask_callback(patterns, clean_unit)
    return clean_unit
