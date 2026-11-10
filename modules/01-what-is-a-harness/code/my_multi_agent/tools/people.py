"""
Contains all tools needed for the people agent
"""


from google.adk.agents.llm_agent import ToolUnion

from data_access.orchestrator import list_notifications_for
from data_access.people import list_employee_names
from tools.arguments import as_int

def _list_employees() -> dict:
    """
    List all user names and emp ids
    """

    emps_w_ids = [{"emp_id": emp_id, "emp_name": emp_name} for emp_id, emp_name in list_employee_names()]
    return {
        "status": "ok",
        "users_w_emp_ids": emps_w_ids,
        "detail": "Employees with their emp ids and names were fetched successfully."
    }

def _list_notifications(emp_id: str) -> dict:
    """
    List notifications of a particular employee
    """

    # an exception will be carried upstream and trigger the "reflect and retry plugin"
    # configured with the ADK App
    employee_id = as_int(emp_id)
    notifications = [] if employee_id is None else [
        {
            "notification_id": n.notification_id,
            "emp_id": n.emp_id,
            "message": n.message,
            "created_at": n.created_at,
        }
        for n in list_notifications_for(emp_id=employee_id)
    ]
    return {
        "status": "ok",
        "notifications": notifications,
        "detail": "Notifications listed for this employee."
    }

def assemble_people_tools() -> list[ToolUnion]:
    return [_list_employees, _list_notifications]
