"""
Initialize the it agent with some initial state here.
"""

from google.adk.agents import Agent
from google.adk.models import BaseLlm

from commons import build_instructions, build_description_from_tools
from tools.it import assemble_it_tools

def create_it_agent(model: BaseLlm) -> Agent:
    """
    create the IT agent object and return it.
    Purpose: Manage equipment assignment and employee-facing IT requests.
    """
    it_tools = assemble_it_tools()
    return Agent(
        name="it_agent",
        model=model,
        description=build_description_from_tools(__file__, "description.md", it_tools),
        wait_for_output=True,
        instruction=build_instructions(__file__, "instructions.md"),
        tools = it_tools,
        mode="task"
    )