"""
enable each agent to use their instructions.md as their instruction argument
while creating their instance.
"""

from pathlib import Path

from commons.database_ops import now_local
from utils.file_ops import read_file_if_exists



def build_instructions(module_file, filename):
    # Return an InstructionProvider (ADK calls it every turn) so the date stays fresh.
    # The static body is read once; only now_local() is re-evaluated per turn.
    base = read_file_if_exists(module_file, filename)

    def provide(readonly_context=None):
        return f"Today is {now_local(date=True)}\n\n{base}"

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

