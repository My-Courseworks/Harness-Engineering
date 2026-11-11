"""Reads and writes for the people domain."""

from sqlalchemy import select

from commons.db import session_scope
from models import Employee


def list_employee_names(page: int, page_size: int) -> tuple[list[dict], int | None]:
    """
    One page of employees as {emp_id, emp_name}, ordered by id.

    Returns the page's rows and the next page number, or None when this was
    the last page. A page past the end returns no rows and None.
    """
    with session_scope() as session:
        # limit: retrieves all rows of this page + one extra row
        # offset: skip all rows till the offset argument value
        rows = session.execute(
            select(Employee.emp_id, Employee.emp_name)
            .order_by(Employee.emp_id)
            .limit(page_size + 1)
            .offset((page-1)*page_size)
        ).mappings().all()
        # the extra row is only a probe for "is there more": it is never returned
        next_page = page + 1 if len(rows) > page_size else None
        return [dict(emp) for emp in rows[:page_size]], next_page

def find_employee(name: str) -> list[dict[str, any]]:
    """
    Employees whose name contains `name`, ignoring case, ordered by id.

    Each match is a dict with emp_id, emp_name, profession and status.
    Returns an empty list when nothing matches. Terminated employees are
    included, so the caller decides whether status matters.
    `%` and `_` inside `name` are matched as literal characters.
    An empty `name` matches every employee.
    """
    with session_scope() as session:
        rows = session.execute(
            select(Employee.emp_id, Employee.emp_name, Employee.profession, Employee.status)
            .where(Employee.emp_name.icontains(name, autoescape=True))
            .order_by(Employee.emp_id)
        ).mappings()
        return [dict(r) for r in rows]

def get_employee_by_emp_id(emp_id: str) -> dict[str, any] | None:
    """
    The employee with this id, or None when there is no such employee.

    The result is a dict with emp_id, emp_name, profession and status,
    whether the employee is active or terminated.
    `emp_id` is compared as given: SQLite converts numeric text to a number,
    and text that is not a number matches nothing.
    """
    with session_scope() as session:
        row = session.execute(
            select(Employee.emp_id, Employee.emp_name, Employee.profession, Employee.status)
            .where(Employee.emp_id == emp_id)
        ).mappings().one_or_none()
        return dict(row) if row is not None else None
