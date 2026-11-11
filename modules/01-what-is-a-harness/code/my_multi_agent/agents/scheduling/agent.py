"""
Initialize the scheduling agent with some initial state here.
"""

from google.adk.agents import Agent
from google.adk.models import BaseLlm

from commons import build_instructions, build_description_from_tools
from tools.scheduling import assemble_scheduling_tools

def create_scheduling_agent(model: BaseLlm) -> Agent:
    """
    create the scheduling agent object and return it.
    Check availability and reserve a resource over a time range — a person's time (leave) 
        or a room's time (booking).
    """
    scheduling_tools = assemble_scheduling_tools()
    return Agent(
        name="scheduling_agent",
        model=model,
        description=build_description_from_tools(__file__, "description.md", scheduling_tools),
        wait_for_output=True,
        instruction=build_instructions(__file__, "instructions.md"),
        tools = scheduling_tools,
        mode="task"
    )