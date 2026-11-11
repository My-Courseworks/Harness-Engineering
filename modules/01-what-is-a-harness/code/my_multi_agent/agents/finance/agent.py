"""
Initialize the finance agent with some initial state here.
Handle employee expense claims and report spending.
"""

from google.adk.agents import Agent
from google.adk.models import BaseLlm

from commons import build_instructions
from tools.finance import assemble_finance_tools

def create_finance_agent(model: BaseLlm) -> Agent:
    """
    create the finance agent object and return it.
    Handle employee expense claims and report spending.
    """
    return Agent(
        name="finance_agent",
        model=model,
        description="The finance agent that handles employee expense claims and reports spending.",
        wait_for_output=True,
        instruction=build_instructions(__file__, "instructions.md", with_task_rules=True),
        tools = assemble_finance_tools(),
        mode="task"
    )