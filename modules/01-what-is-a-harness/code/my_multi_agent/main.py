"""

"""

from dataclasses import asdict

import asyncio

import questionary
from prompt_toolkit.history import InMemoryHistory

from google.adk.sessions import DatabaseSessionService

# # sadly google search tool is unavailable with anything but Gemini models
# from google.adk.tools import google_search

from rich.console import Console

from agents.orchestrator import create_orchestrator_agent

from chat.masking.masking_policy import apply_masking, MASKED_ROLE_INSTRUCTION
from chat.masking.utils import CleanUnit

from chat.model_choice import choose_model
from chat.render_chat import View
from chat.replay import replay_session
from chat.runtime import build_runtime
from chat.sessions import get_session_service, choose_session, user_messages
from chat.turn import get_async_agent_response
from chat.users import choose_user

from commons import create_model
from commons.config import load_config
from commons.db import require_current_schema

from models import User


async def main():
    """
    Run the main agentic loop in an asynchronous manner
    """

    # bad YAML fails main agentic loop.
    config = load_config()

    # refuse to run against a database whose schema is not the one this code expects.
    require_current_schema()

    session_service: DatabaseSessionService = get_session_service()
    
    user: User | None = await choose_user()
    if user is None:
        print("\nBye. 👋🏽👋🏽👋🏽")
        return

    # pick the provider, then one of its models. Returns the model string and the name of
    # the key variable, or None on Ctrl+C. Must come before the agents are built.
    model_choice = await choose_model(config.providers)
    if model_choice is None:
        print("\nBye. 👋🏽👋🏽👋🏽")
        return
    model_str, api_key_name = model_choice

    # one model object for the whole run: every agent and the masking rewriter share it
    model = create_model(model_str=model_str, api_key_name=api_key_name)

    root_agent = create_orchestrator_agent(model)

    clean_unit: CleanUnit | None = await apply_masking(root_agent=root_agent, user_role=user.role, rewriter=model,
                                                       is_masking_enabled=config.features.masking)

    global_instruction = None    
    if config.features.masking and config.features.masked_role_instruction and user.role != "admin":
        global_instruction = MASKED_ROLE_INSTRUCTION

    chat_runtime = build_runtime(root_agent=root_agent, session_service=session_service,
                                 global_instruction=global_instruction)

    session_id = await choose_session(
        session_service = session_service,
        user = user,
        app_name=chat_runtime.app.name,
        initial_state=asdict(config.initial_state)
    )

    if session_id is None:
        print("\nBye. 👋🏽👋🏽👋🏽")
        return

    console = Console()
    view = View(styles=config.styles, labels=config.labels, display=config.displays[user.role],
                root_agent_name=root_agent.name, clean_unit=clean_unit)

    # the stored session, read once: the replay prints its last turns, and the prompt
    # history below is seeded from it.
    session = await session_service.get_session(app_name=chat_runtime.app.name, user_id=user.user_id,
                                                session_id=session_id)

    await replay_session(session=session, console=console, view=view)

    user_prompt_style = questionary.Style([
        ("qmark", ""),
        ("question", view.styles.user),
        ("answer", view.styles.user)
    ])

    # up and down arrows walk through what the user typed in this session. One history
    # object for the whole loop: the prompt appends every new input to it by itself.
    history = InMemoryHistory(user_messages(session) if session else [])

    while True:
        # asyncio.to_thread(func, *args) runs func(*args) in a separate worker thread, 
        #   and returns an awaitable that completes when the function returns.
        # await suspends main() until that thread finishes, then gives you 
        #   the returned string in query.
        # query = await asyncio.to_thread(input, "\n[user]: ")
        query = await questionary.text(
            message = f"\n{view.labels.user} ",
            qmark="",
            style = user_prompt_style,
            history = history
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