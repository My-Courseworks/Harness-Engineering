"""

"""

import asyncio

import questionary

from google.adk.sessions import DatabaseSessionService



# # sadly google search tool is unavailable with anything but Gemini models
# from google.adk.tools import google_search

from rich.console import Console


from agents.orchestrator import create_orchestrator_agent
from chat.masking import (
    MASKED_ROLE_INSTRUCTION,
    build_mask_callback, build_unit_cleaner,
    collect_internal_names, compile_name_patterns
)
from chat.render_chat import View
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
    # functions and never asks who the user is. Three layers, same patterns:
    #   - a runner-wide instruction, so the model rarely narrates internals;
    #   - clean_unit on the View: the live stream prints a unit only after it
    #     has been checked, rewritten if needed, or withheld;
    #   - a callback on the root agent that persists the same clean text for replay.
    # TODO: change the role check to an Enum once this starts working
    clean_unit = None
    global_instruction = None
    if config.features.masking and user.role != "admin":
        patterns = compile_name_patterns(await collect_internal_names(root_agent))
        clean_unit = build_unit_cleaner(patterns, create_model())
        root_agent.after_model_callback = build_mask_callback(patterns, clean_unit)
        if config.features.masked_role_instruction:
            global_instruction = MASKED_ROLE_INSTRUCTION

    chat_runtime = build_runtime(root_agent=root_agent, session_service=session_service,
                                 global_instruction=global_instruction)

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
                root_agent_name=root_agent.name, clean_unit=clean_unit)

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