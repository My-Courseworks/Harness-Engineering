"""

"""
import uuid

import questionary
from questionary.prompts.common import InquirerControl

from google.adk.events import Event, EventActions
from google.adk.sessions.session import Session
from google.adk.sessions import DatabaseSessionService


from commons.db import sessions_path
from models import User

NEW_SESSION_CHOICE = "Create a new Session ➕"
DELETE_KEY = "d"    # pressed on a highlighted session in the list, asks to delete it


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


async def _ask_which_session(greeting: str, session_ids: list[str]) -> tuple[str, bool] | None:
    """
    Show the session list once.

    Returns the highlighted row and whether it was picked for deletion: enter picks it
    to open, DELETE_KEY picks it to delete. Returns None if the prompt was cancelled (Ctrl+C).

    questionary has no option for an extra key, so the key is added to the prompt it
    built. This relies on two of its internals: the prompt's own key bindings, and the
    InquirerControl that knows which row is highlighted.
    """
    question = questionary.select(
        greeting,
        choices=[*session_ids, NEW_SESSION_CHOICE],
        instruction=f"(enter opens, {DELETE_KEY} deletes)" if session_ids else None,
    )
    list_control = next(
        control for control in question.application.layout.find_all_controls()
        if isinstance(control, InquirerControl)
    )
    wants_delete = False

    @question.application.key_bindings.add(DELETE_KEY, eager=True)
    def pick_for_deletion(event):
        nonlocal wants_delete
        highlighted = list_control.get_pointed_at().value
        if highlighted == NEW_SESSION_CHOICE:
            return      # nothing to delete on this row
        wants_delete = True
        # answered: the list collapses to "<question> <session id>", as it does on enter
        list_control.is_answered = True
        event.app.exit(result=highlighted)

    row = await question.ask_async()
    return None if row is None else (row, wants_delete)


async def choose_session(
    session_service: DatabaseSessionService,
    app_name: str,
    user: User,
    initial_state: dict
) -> str | None:
    """
    Choose and return the session id chosen.

    A session can also be deleted from the list. After a deletion, or a declined one,
    the list is shown again, so this returns only once a session is opened or created,
    or None if the list was cancelled (Ctrl+C).
    """

    greeting = f"\n\nHi {user.user_name}, please choose a session or start a new one:"

    while True:
        sessions_list = await list_sessions_for_user(session_service=session_service, app_name=app_name, user_id = user.user_id)
        session_ids = [session.id for session in sessions_list]

        picked = await _ask_which_session(greeting=greeting, session_ids=session_ids)
        if picked is None:
            return None
        choice, wants_delete = picked
        if not wants_delete:
            break

        # Ctrl+C here answers None: treated as "no", back to the list.
        is_sure = await questionary.confirm(f"Delete {choice} for good?", default=False).ask_async()
        if is_sure:
            await session_service.delete_session(app_name=app_name, user_id=user.user_id, session_id=choice)

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
    