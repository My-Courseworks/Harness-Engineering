"""Reads and writes for the people domain."""

from sqlalchemy import select

from commons.db import session_scope
from models import Employee


def list_employee_names() -> list[tuple[int, str]]:
    """Every employee as (emp_id, emp_name), ordered by id."""
    with session_scope() as session:
        rows = session.execute(select(Employee.emp_id, Employee.emp_name).order_by(Employee.emp_id))
        return [(emp_id, emp_name) for emp_id, emp_name in rows]
