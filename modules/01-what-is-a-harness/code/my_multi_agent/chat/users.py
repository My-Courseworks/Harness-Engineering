"""
"""

from dataclasses import dataclass

import questionary

from commons.database_ops import list_chat_users

# TODO: decide proper place for this plus all other datamodels
# also check if they can be created directly from the sql or not
# also check if orm can be used.
@dataclass(frozen=True)
class User:
    user_id: str
    user_name: str
    role: str


async def choose_user() -> User | None:
    """
    Let the person at the terminal pick who they are.

    Returns the chosen User, or None if the prompt was cancelled (Ctrl+C).
    Raises if the users table is empty, since that means data_setup never ran.
    """
    users = [User(**user_dict) for user_dict in list_chat_users()]
    if not users:
        raise RuntimeError("No users found in ops.db; run data_setup first.")
    return await questionary.select(
        "Choose a user:",
        choices=[
            questionary.Choice(title=f"{user.user_name} ({user.role})", value=user)
            for user in users
        ]
    ).ask_async()
    