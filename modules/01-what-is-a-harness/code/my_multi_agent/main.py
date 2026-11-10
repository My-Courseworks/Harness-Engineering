"""

"""

import functools


import asyncio

import questionary

from google.adk.sessions import DatabaseSessionService



# # sadly google search tool is unavailable with anything but Gemini models
# from google.adk.tools import google_search

from rich.console import Console


from agents.orchestrator import create_orchestrator_agent
from chat.masking import (
    build_mask_callback, collect_internal_names, 
    substitute_internals, compile_name_patterns
)
from chat.render_chat import View, passthrough
from chat.replay import replay_session
from chat.runtime import build_runtime
from chat.sessions import get_session_service, choose_session
from chat.turn import get_async_agent_response
from chat.users import choose_user, User
from commons.config import load_config
from commons.create_model import create_model


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

    # Masking: non-admins must never see internal agent or tool names.
    # The role is resolved exactly once, here; everything downstream receives
    # functions (a callback on the agent, a render transform on the View) and
    # never asks who the user is. Patterns are compiled once and shared so the
    # callback and the renderer provably match against the same regexes.
    # TODO: change the role check to an Enum once this starts working
    render = passthrough
    if user.role != "admin":
        internal_names = await collect_internal_names(root_agent)
        patterns = compile_name_patterns(internal_names)
        root_agent.after_model_callback = build_mask_callback(patterns, create_model())
        render = functools.partial(substitute_internals, patterns=patterns)

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
    view = View(styles=config.styles, labels=config.labels, display=config.displays[user.role],
                root_agent_name=root_agent.name, render=render)

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
        try:
            await get_async_agent_response(query=query, runner=chat_runtime.runner,
                run_config=chat_runtime.run_config, user_id=user.user_id, session_id=session_id,
                console=console, view=view)
        except Exception:
            # One failed turn must not end the session. Tracebacks name modules
            # and tools, so only roles configured to see error details get them.
            if view.display.show_error_details:
                console.print_exception()
            else:
                console.print("\nSomething went wrong on my side. Please try again.", style=view.styles.agent)


if __name__ == '__main__':

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, EOFError):
        print("\nBye. 👋🏽👋🏽👋🏽")
    except Exception as e:
        print(f"\n-- Exception = {e}\n")