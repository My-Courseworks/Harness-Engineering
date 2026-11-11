"""

"""
import uuid

import questionary

from google.adk.events import Event, EventActions
from google.adk.sessions.session import Session
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

async def _top_up_state(session_service: DatabaseSessionService, session: Session, initial_state: dict):
    missing = {key: value for key,value in initial_state.items()
               if key not in session.state}
    if missing:
        await session_service.append_event(
            session, Event(author="user", actions=EventActions(state_delta = missing))
        )

def user_messages(session: Session) -> list[str]:
    """
    Every message the user typed in this session, oldest first.

    Used to seed the prompt's history, so the up and down arrows work right after
    a resume. It reads exactly what the replay prints as user lines.
    """
    return [
        part.text
        for event in session.events
        if event.content and event.content.role == "user"
        for part in event.content.parts or []
        if part.text
    ]


async def choose_session(
    session_service: DatabaseSessionService,
    app_name: str,
    user: User,
    initial_state: dict
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
    if choice == NEW_SESSION_CHOICE:
        session_id = f"session-{uuid.uuid4().hex}"
        await session_service.create_session(
            app_name=app_name,
            user_id=user.user_id,
            session_id=session_id,
            state=initial_state,
        )
        return session_id
    else:
        resumed_session: Session = await session_service.get_session(
            app_name=app_name,
            user_id=user.user_id,
            session_id=choice
        )
        await _top_up_state(session_service=session_service, session=resumed_session, initial_state=initial_state)
    return choice
    