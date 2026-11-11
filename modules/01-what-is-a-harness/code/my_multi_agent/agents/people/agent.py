"""
Initialize the people agent with some initial state here.
"""

from google.adk.agents import Agent
from google.adk.models import BaseLlm

from commons import build_instructions, build_description_from_tools
from tools.pagination import listings_section
from tools.people import assemble_people_tools

def create_people_agent(model: BaseLlm) -> Agent:
    """
    create the people agent object and return it.
    Answer questions about employees and pay; create and terminate employee records.
    """
    people_tools = assemble_people_tools()
    return Agent(
        name="people_agent",
        model=model,
        description=build_description_from_tools(__file__, "description.md", people_tools),
        wait_for_output=True,
        instruction=build_instructions(__file__, "instructions.md",
                                       state_section=listings_section(people_tools),
                                       with_task_rules=True),
        tools = people_tools,
        mode="task"
    )