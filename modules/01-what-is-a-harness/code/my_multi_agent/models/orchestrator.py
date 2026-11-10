"""Orchestrator cluster: the cross-cutting notify tool writes here. Starts empty."""

from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import UTC_NOW_SQL, Base, utc_now


class Notification(Base):
    __tablename__ = "notifications"

    notification_id: Mapped[int] = mapped_column(Integer, primary_key=True, default=None)
    emp_id: Mapped[int] = mapped_column(ForeignKey("employees.emp_id"))
    message: Mapped[str] = mapped_column(Text)
    created_at: Mapped[str] = mapped_column(Text, default_factory=utc_now, server_default=UTC_NOW_SQL)
