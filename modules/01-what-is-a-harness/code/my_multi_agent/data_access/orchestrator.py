"""Reads and writes for the orchestrator domain: notifications."""

from sqlalchemy import select

from commons.db import session_scope
from models import Employee, Notification


def record_notification(emp_id: int, message: str) -> bool:
    """Store a notification for an employee. Returns False, writing nothing, if no such employee exists."""
    with session_scope() as session:
        if session.get(Employee, emp_id) is None:
            return False
        session.add(Notification(emp_id=emp_id, message=message))
        return True


def list_notifications_for(emp_id: int) -> list[Notification]:
    """An employee's notifications, oldest first."""
    with session_scope() as session:
        query = (
            select(Notification)
            .where(Notification.emp_id == emp_id)
            .order_by(Notification.created_at, Notification.notification_id)
        )
        return list(session.scalars(query))
