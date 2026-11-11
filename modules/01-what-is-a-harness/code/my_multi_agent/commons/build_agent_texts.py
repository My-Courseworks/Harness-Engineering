"""
enable each agent to use their instructions.md as their instruction argument
while creating their instance.
"""

from pathlib import Path

from utils.time_fmt import now_local
from utils.file_ops import read_file_if_exists



def build_instructions(module_file, filename, state_section=None):
    # Return an InstructionProvider (ADK calls it every turn) so the date stays fresh.
    # The static body is read once; only now_local() is re-evaluated per turn.
    #
    # state_section, when given, is a function of the session state that returns text to
    # append (or "" for nothing). ADK does not fill {key} placeholders in an instruction
    # that comes from a function, so anything from state has to be added here.
    base = read_file_if_exists(module_file, filename)

    def provide(readonly_context=None):
        text = f"Today is {now_local(date=True)}\n\n{base}"
        if state_section is not None and readonly_context is not None:
            section = state_section(readonly_context.state)
            if section:
                text += f"\n\n{section}"
        return text

    return provide

def build_description_from_tools(module_file, filename, tools = []) -> str:
    """
    filename contains description of agent in addition to its tools.
    Recommended: scope/intent/boundaries should be covered in description.md
    """
    parts = []
    
    # agent description from description.md
    base = read_file_if_exists(module_file=module_file, filename=filename)
    if base:
        parts.append(base)


    # tools' docstrings into the agent's description
    tools_w_descs = "\n".join(
        [
            f"- {t.__name__}: {(t.__doc__ or '').strip()}"
            for t in tools
        ]
    )
    if tools_w_descs:
        parts.append(tools_w_descs)

    return "\n\n".join(parts)

