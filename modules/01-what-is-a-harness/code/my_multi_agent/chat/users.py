"""
Picking who is sitting at the terminal.
"""

import questionary

from data_access.users import list_users
from models import User


async def choose_user() -> User | None:
    """
    Let the person at the terminal pick who they are.

    Returns the chosen User, or None if the prompt was cancelled (Ctrl+C).
    Raises if the users table is empty, since that means the database was never seeded.
    """
    users = list_users()
    if not users:
        raise RuntimeError("No users found in the database. Run: python -m data_setup seed")
    return await questionary.select(
        "Choose a user:",
        choices=[
            questionary.Choice(title=f"{user.user_name} ({user.role})", value=user)
            for user in users
        ]
    ).ask_async()
