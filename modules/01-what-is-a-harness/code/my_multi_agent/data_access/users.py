"""Reads for the chat users: the people who sit at the terminal."""

from sqlalchemy import select

from commons.db import session_scope
from models import User


def list_users() -> list[User]:
    """Every chat user, admins first, then by name."""
    with session_scope() as session:
        return list(session.scalars(select(User).order_by(User.role, User.user_name)))
