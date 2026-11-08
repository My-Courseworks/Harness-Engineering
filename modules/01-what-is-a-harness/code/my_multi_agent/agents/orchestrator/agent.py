"""
Initialize the orchestrator agent with some initial state here.
"""

from google.adk.agents import Agent

from commons import create_model, build_instructions, build_description_from_tools

from agents.finance import create_finance_agent
from agents.it import create_it_agent
from agents.people import create_people_agent
from agents.scheduling import create_scheduling_agent

from tools.orchestrator import assemble_orchestrator_tools

def create_orchestrator_agent() -> Agent:
    """
    create the orchestrator agent object and return it.
    """
    orchestrator_tools = assemble_orchestrator_tools()
    return Agent(
        name="orchestrator_agent",
        model=create_model(),
        description=build_description_from_tools(__file__, "description.md", orchestrator_tools),
        wait_for_output=True,
        instruction=build_instructions(__file__, "instructions.md"),
        sub_agents=[
            create_finance_agent(),
            create_it_agent(),
            create_people_agent(),
            create_scheduling_agent()
        ],
        tools = orchestrator_tools
    )