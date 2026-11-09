"""
Contains all tools needed for the orchestrator agent
"""

from google.adk.agents.llm_agent import ToolUnion

from commons.database_ops import notify_db

def _notify(emp_id: str, message: str) -> dict:
    """
    Send message to emp_id employee.
    emp_id: the exact employee id to send the notification to. is validated from the employees table.
    message: notification sent to the employee, should be composed
        from the user's intent. Plain, crisp text, no greeting or recipient name.
    """

    # an exception will be carried upstream and trigger the "reflect and retry plugin"
    # configured with the ADK App
    is_emp_found = notify_db(emp_id=emp_id, message=message)
    return {
        "status": "ok" if is_emp_found else "fail",
        "emp_id": emp_id,
        "detail": "Notification recorded for this employee." if is_emp_found else "Employee not found, use another employee id."
    }

def assemble_orchestrator_tools() -> list[ToolUnion]:
    return [_notify]