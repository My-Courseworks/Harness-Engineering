"""Chat users: the people who sit at the ops desk terminal.

Deliberately separate from employees, who are the subjects of the data, not its
operators. ``role`` decides what the terminal shows them; the allowed values
must match the ``display`` keys in config.yml.
"""

from sqlalchemy import CheckConstraint, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (CheckConstraint("role IN ('admin', 'user')", name="role_allowed"),)

    user_id: Mapped[str] = mapped_column(Text, primary_key=True)   # what ADK stores sessions under
    user_name: Mapped[str] = mapped_column(Text, unique=True)      # shown in the picker and the greeting
    role: Mapped[str] = mapped_column(Text)
