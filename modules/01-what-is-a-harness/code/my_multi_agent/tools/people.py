"""
Contains all tools needed for the people agent
"""


from google.adk.agents.llm_agent import ToolUnion

from commons.database_ops import (
    list_employees_from_db, list_notifications_db
)

def _list_employees() -> dict:
    """
    List all user names and emp ids
    """

    emps_w_ids = list_employees_from_db()
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
    notifications = list_notifications_db(emp_id=emp_id)
    return {
        "status": "ok",
        "notifications": notifications,
        "detail": "Notifications listed for this employee."
    }

def assemble_people_tools() -> list[ToolUnion]:
    return [_list_employees, _list_notifications]