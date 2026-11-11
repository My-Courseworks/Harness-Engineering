"""
Contains all tools needed for the people agent
"""


from google.adk.agents.llm_agent import ToolUnion
from google.adk.tools import ToolContext

from data_access.orchestrator import list_notifications_for
from data_access.people import list_employee_names, find_employee, get_employee_by_emp_id

from tools.arguments import as_int
from tools.pagination import pagination_decorator, Page


@pagination_decorator
def _list_employee_names(page: int, page_size: int) -> Page:
    """
    List all employees in the database, one page per call, ordered by emp_id.

    Use this only when the user asks for the whole staff list. It is not suited
    to finding one person: it returns many rows and no details about anyone.

    Arguments:
    page: the page number to read, starting at 1.

    Returns `entries`, one per employee with emp_id and emp_name, and
    `next_page`: the page number to ask for when more is wanted, or a sentence
    saying this was the final page.
    """

    emp_names_w_ids, next_page = list_employee_names(page=page, page_size=page_size)

    return Page(
        entries = emp_names_w_ids,
        filters={},
        next_page=next_page,
        status="ok",
        detail="Employees listed." if emp_names_w_ids else "There are no employees on this page."
    )

def _find_employee(name: str) -> dict[str, any]:
    """
    Find employee(s) by name, returns a list of employees with their details 
    like name, id, employment status, profession
    when multiple employees share the name.
    """
    status = "fail"
    detail = "Employee retrieval errored out"
    employees = []
    try:
        employees = find_employee(name=name)
        if len(employees) == 0:
            status = "missing"
            detail = "No employee with the given name was found"
        elif len(employees) == 1:
            # exactly one, this must be it
            status = "found"
            detail = "Exactly one employee found, this must be it"
        else:
            # more filtering exists, agent-user couldn't provide us
            status = "found_multiple"
            detail = "Multiple employees found with the same name, please select which one do you mean exactly."
    except Exception as _:
        pass

    return {
        "status": status, 
        "detail": detail,
        "employees": employees
    }

def _get_employee(emp_id: str) -> dict:
    """
    Look up one employee by employee id.
    emp_id: the employee's numeric id, as text, for example "24".
    Returns the employee with these fields: id, name, employment_status, profession.
    """
    status = "fail"
    detail = "Employee retrieval errored out"
    employee = None

    try:
        employee = get_employee_by_emp_id(emp_id=emp_id)
        if employee:
            status = "found"
            detail = "Employee with the given emp_id exists."
        else:
            status = "Not found"
            detail = "Employee with the given emp_id does not exist."
    except Exception as _:
        pass

    return {
        "status": status, 
        "detail": detail,
        "employee": employee
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
    return [_list_employee_names, _list_notifications, _find_employee, _get_employee]
