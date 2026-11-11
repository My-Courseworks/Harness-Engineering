"""

"""

from dataclasses import asdict

import asyncio

from google.adk.sessions import DatabaseSessionService

# # sadly google search tool is unavailable with anything but Gemini models
# from google.adk.tools import google_search

from rich.console import Console

from agents.orchestrator import create_orchestrator_agent

from chat.masking.masking_policy import apply_masking, MASKED_ROLE_INSTRUCTION
from chat.masking.utils import CleanUnit

from chat.loop import run_chat_loop
from chat.model_choice import choose_model
from chat.render_chat import View
from chat.replay import replay_session
from chat.runtime import build_runtime
from chat.sessions import get_session_service, choose_session
from chat.users import choose_user

from commons import create_model, context_window
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

    # the stored session, read once: the replay prints its last turns, and the chat loop
    # seeds its prompt history and its first context usage line from it.
    session = await session_service.get_session(app_name=chat_runtime.app.name, user_id=user.user_id,
                                                session_id=session_id)

    await replay_session(session=session, console=console, view=view)

    # ask, answer, repeat: returns when the user leaves (Ctrl+C, exit or quit).
    await run_chat_loop(runtime=chat_runtime, session=session, console=console, view=view,
                        context_window=context_window(model_str))

    print("\nBye. 👋🏽👋🏽👋🏽")


if __name__ == '__main__':

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, EOFError):
        print("\nBye. 👋🏽👋🏽👋🏽")
    except Exception as e:
        print(f"\n-- Exception = {e}\n")