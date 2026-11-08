"""
Contains all tools needed for the orchestrator agent
"""

from google.adk.agents.llm_agent import ToolUnion

from commons.database_ops import notify_db

def _notify(emp_id: str, message: str) -> dict:
    """
    Send message to emp_id employee.
    """

    # an exception will be carried upstream and trigger the "reflect and retry plugin"
    # configured with the ADK App
    notify_db(emp_id=emp_id, message=message)
    return {
        "status": "ok",
        "emp_id": emp_id,
        "detail": "Notification recorded for this employee."
    }

def assemble_orchestrator_tools() -> list[ToolUnion]:
    return [_notify]