"""
Contains all tools needed for the orchestrator agent
"""

from google.adk.agents.llm_agent import ToolUnion

from data_access.orchestrator import record_notification
from tools.arguments import as_int

def _notify(emp_id: str, message: str) -> dict:
    """
    Send message to emp_id employee.
    emp_id: the exact employee id to send the notification to. is validated from the employees table.
    message: notification sent to the employee, should be composed
        from the user's intent. Plain, crisp text, no greeting or recipient name.
    """

    # an exception will be carried upstream and trigger the "reflect and retry plugin"
    # configured with the ADK App
    employee_id = as_int(emp_id)
    is_emp_found = employee_id is not None and record_notification(emp_id=employee_id, message=message)
    return {
        "status": "ok" if is_emp_found else "fail",
        "emp_id": emp_id,
        "detail": "Notification recorded for this employee." if is_emp_found else "Employee not found, use another employee id."
    }

def assemble_orchestrator_tools() -> list[ToolUnion]:
    return [_notify]
