"""

"""
import uuid

import questionary

from google.adk.sessions import DatabaseSessionService

from commons.db import sessions_path
from models import User

NEW_SESSION_CHOICE = "Create a new Session ➕"


def get_session_service() -> DatabaseSessionService:
    """
    ADK's own session store. Its location comes from config, never from the working directory.
    """
    path = sessions_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    return DatabaseSessionService(db_url=f"sqlite+aiosqlite:///{path}")

async def list_sessions_for_user(
    session_service: DatabaseSessionService,
    app_name: str,
    user_id: str
):
    response = await session_service.list_sessions(app_name=app_name, user_id=user_id)
    return response.sessions

async def choose_session(
    session_service: DatabaseSessionService,
    app_name: str,
    user: User
) -> str | None:
    """
    Choose and return the session id chosen
    """

    sessions_list = await list_sessions_for_user(session_service=session_service, app_name=app_name, user_id = user.user_id)
    session_ids = [session.id for session in sessions_list]

    greeting = f"\n\nHi {user.user_name}, please choose a session or start a new one:"

    choice = await questionary.select(
        greeting,
        choices=[*session_ids, NEW_SESSION_CHOICE],
    ).ask_async()
    if choice is None:
        return None
    session_id = f"session-{uuid.uuid4().hex}" if choice == NEW_SESSION_CHOICE else choice
    return session_id
    