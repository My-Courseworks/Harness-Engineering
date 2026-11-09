"""

"""

import asyncio

import uuid

from dataclasses import dataclass

import async_to_sync

import questionary

from google.adk.sessions import DatabaseSessionService



# # sadly google search tool is unavailable with anything but Gemini models
# from google.adk.tools import google_search

from rich.console import Console


from agents.orchestrator import create_orchestrator_agent
from chat.render_chat import View
from chat.replay import replay_session
from chat.runtime import build_runtime
from chat.sessions import get_session_service, choose_session
from chat.turn import get_async_agent_response
from chat.users import choose_user, User
from commons.config import load_config


async def main():
    """
    Run the main agentic loop in an asynchronous manner
    """

    # bad YAML fails main agentic loop.
    config = load_config()

    session_service: DatabaseSessionService = get_session_service()
    
    user: User | None = await choose_user()
    if user is None:
        print("\nBye. 👋🏽👋🏽👋🏽")
        return

    root_agent = create_orchestrator_agent()
    chat_runtime = build_runtime(root_agent=root_agent, session_service=session_service)

    session_id = await choose_session(
        session_service = session_service,
        user = user,
        app_name=chat_runtime.app.name
    )

    if session_id is None:
        print("\nBye. 👋🏽👋🏽👋🏽")
        return

    console = Console()
    view = View(styles=config.styles, labels=config.labels, displays=config.displays)

    await replay_session(app_name=chat_runtime.app.name, session_id=session_id,  user_id = user.user_id,
        session_service=session_service, console=console, view=view)

    user_prompt_style = questionary.Style([
        ("qmark", ""),
        ("question", view.styles.user),
        ("answer", view.styles.user)
    ])

    while True:
        # asyncio.to_thread(func, *args) runs func(*args) in a separate worker thread, 
        #   and returns an awaitable that completes when the function returns.
        # await suspends main() until that thread finishes, then gives you 
        #   the returned string in query.
        # query = await asyncio.to_thread(input, "\n[user]: ")
        query = await questionary.text(
            message = f"\n{view.labels.user} ",
            qmark="",
            style = user_prompt_style
        ).ask_async()

        if query is None:
            # Ctrl+C
            break
        if not query.strip():
            # Accidental empy enter-key
            continue
        if query in ('exit', 'quit'):
            print("\nBye. 👋🏽👋🏽👋🏽")
            break
        await get_async_agent_response(query=query, runner=chat_runtime.runner, 
            run_config=chat_runtime.run_config, user_id=user.user_id, session_id = session_id)


if __name__ == '__main__':

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, EOFError):
        print("\nBye. 👋🏽👋🏽👋🏽")
    except Exception as e:
        print(f"\n-- Exception = {e}\n")