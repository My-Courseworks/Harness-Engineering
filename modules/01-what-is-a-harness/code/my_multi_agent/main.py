"""

"""

import os
import asyncio
from pathlib import Path

import uuid

from dotenv import load_dotenv
load_dotenv()



import async_to_sync

import questionary

from google.genai import types

from google.adk.apps import App
from google.adk.agents.llm_agent import Agent
from google.adk.agents import RunConfig
from google.adk.agents._streaming_mode import StreamingMode
from google.adk.plugins import ReflectAndRetryToolPlugin
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService



# sadly google search tool is unavailable with anything but Gemini models
from google.adk.tools import google_search

from rich.console import Console
from rich.text import Text
from rich.markdown import Markdown
from rich.live import Live


from agents.orchestrator import create_orchestrator_agent

from content_streaming import render, update_content, MessageType
from reloader import start_reloader


USER_ID = "akshay"
APP_NAME = "multi-agent-team"
NEW_SESSION_CHOICE = "Create a new Session ➕"

LAST_SESSION_FILE = Path(".last_session")

session_service = DatabaseSessionService(db_url = "sqlite+aiosqlite:///./session.db")

root_agent = create_orchestrator_agent()
console = Console()
print("console width =", console.width)      # temporary


def remember_session(session_id: str) -> None:
    LAST_SESSION_FILE.write_text(session_id)

def last_session() -> str | None:
    return LAST_SESSION_FILE.read_text().strip() if LAST_SESSION_FILE.is_file() else None

async def get_async_agent_response(query: str, runner: Runner, run_config: RunConfig, 
                             user_id, session_id):
    """
    """

    new_msg = types.Content(role = 'user', parts = [types.Part(text=query)])
    
    thinking_just_started, main_resp_just_started = True, True

    # reset()
    with Live(render(), console=console, refresh_per_second=10, transient=False) as live:
        async for event in runner.run_async(user_id=user_id, session_id=session_id, 
                                            new_message=new_msg,
                                            run_config=run_config):
            
            if not event.content or not event.content.parts:
                continue
            for part in getattr(event.content, 'parts') or []:
                
                text_to_print = ""

                # tool call
                if part.function_call and not event.partial:
                    # non partial even whose part is a function call
                    fc = part.function_call
                    # simple print function call for now
                    # # TODO: convert this to rich text later on, once flow is verified.
                    # text_to_print += f"\n\n\t⚙ {fc.name} ({fc.args})\n"
                    # console.print(Text(f"⚙  {fc.name}", style="#c98b8b"))            # dull red
                    update_content(
                        MessageType.TOOL_CALL, 
                        f"\n\n\t⚙ {fc.name} ({fc.args})\n"
                    )

                # tool response
                if part.function_response:
                    fr = part.function_response
                    # text_to_print += f"\n\n\t↪ {fr.response}\n"
                    # console.print(Text(f"      ↳  {fr.response}", style="#8b9cc9"))   # dull blue
                    update_content(
                        MessageType.TOOL_RESPONSE, 
                        f"      ↳  {fr.response}"
                    )

                if not text_to_print and (not part.text or not event.partial):
                    continue
                text_to_print += (part.text or "")
                if part.thought:
                    # text_to_print = ("\n  [Thinking]: " if thinking_just_started else "") + text_to_print
                    update_content(MessageType.THINKING, text_to_print, thinking_just_started)
                    thinking_just_started = False
                    main_resp_just_started = True

                    # # grey and italicised thinking blocks.
                    # text_to_print = f"\033[2;3m{text_to_print}\033[0m"
                else:
                    # text_to_print = ("\n\n[Agent]: " if main_resp_just_started else "") + text_to_print
                    update_content(MessageType.AGENT, text_to_print, main_resp_just_started)
                    main_resp_just_started = False
                    thinking_just_started = True

                # print(text_to_print, end="", flush=True)
                live.refresh()


async def main(session_id: str):
    """
    Run the main agentic loop in an asynchronous manner
    Args:
        session_id: str
        session id of the session a user wants to either continue or start from scratch.
    """

    app = App(
        name=APP_NAME,
        root_agent = root_agent,
        plugins=[ReflectAndRetryToolPlugin(max_retries=3)]
    )

    runner = Runner(
        app=app,
        session_service=session_service,
        auto_create_session=True
    )
    run_config = RunConfig(streaming_mode=StreamingMode.SSE)

    # check if session exists, and retrieve last 5 messages to be displayed.
    try:
        session = await session_service.get_session(
            app_name=APP_NAME, user_id=USER_ID, session_id = session_id
        )
        if session:
            invocations = {}
            for event in getattr(session, 'events'):
                if event.invocation_id not in invocations:
                    invocations[event.invocation_id] = event.timestamp
                else:
                    invocations[event.invocation_id] = max(event.timestamp, invocations[event.invocation_id])

            last_5_invocations = [x[0] for x in sorted(invocations.items(), key=lambda x: x[1], reverse=True)][:5][::-1]

            thinking_just_started, main_resp_just_started = True, True

            for event in getattr(session, 'events'):
                if event.invocation_id not in last_5_invocations:
                    continue
                if not event.content or not event.content.parts:
                    continue

                for part in getattr(event.content, 'parts') or []:
                    if not part.text:
                        continue
                    text_to_print = part.text
                    if event.content.role == "user":
                        text_to_print = ("\n[user]: ") + text_to_print
                    else:
                        if part.thought:
                            text_to_print = ("\n  [Thinking]: " if thinking_just_started else "") + text_to_print
                            thinking_just_started = False
                            main_resp_just_started = True
        
                            # grey and italicised thinking blocks.
                            text_to_print = f"\033[2;3m{text_to_print}\033[0m"
                        else:
                            text_to_print = ("\n\n[Agent]: " if main_resp_just_started else "") + text_to_print
                            main_resp_just_started = False
                            thinking_just_started = True
    
                    print(text_to_print, end="", flush=True)
    except Exception as excp:
        print(excp)



    try:
        while True:
            # asyncio.to_thread(func, *args) runs func(*args) in a separate worker thread, 
            #   and returns an awaitable that completes when the function returns.
            # await suspends main() until that thread finishes, then gives you 
            #   the returned string in query.
            query = await asyncio.to_thread(input, "\n[user]: ")
            query = query.strip()
            if not query:
                continue
            if query in ('exit', 'quit'):
                print("\nBye. 👋🏽👋🏽👋🏽")
                break
            await get_async_agent_response(query=query, runner=runner, 
                run_config=run_config, user_id=USER_ID, session_id = session_id)
    except (KeyboardInterrupt, EOFError):
        print("\nBye. 👋🏽👋🏽👋🏽")
    except Exception as e:
        print(f"\n-- Exception = {e}\n")


if __name__ == '__main__':
    reloader = start_reloader()
    sessions_list = async_to_sync.function(session_service.list_sessions)(app_name=APP_NAME)
    session_ids = [session.id for session in sessions_list.sessions]

    # Auto-resume the same session after a file-save reload; otherwise ask.
    prior = last_session()
    session_id = None
    if os.environ.get("ADK_RELOADED") and prior in session_ids:
        session_id = prior
        print(f"[reloader] restarted (pid={os.getpid()}) — resumed session {session_id}", flush=True)
    else:
        choice = questionary.select(
            "Choose a session:",
            choices=[*session_ids, NEW_SESSION_CHOICE],
            default=prior,
        ).ask()
        session_id = f"session-{uuid.uuid4().hex}" if choice == NEW_SESSION_CHOICE else choice

    if session_id:
        remember_session(session_id)

    try:
        if session_id:
            asyncio.run(main(session_id))
        else:
            raise Exception("Session id cannot be null, please select a session.")
    except (KeyboardInterrupt, EOFError):
        print("\nBye. 👋🏽👋🏽👋🏽")
    except Exception as e:
        print(f"\n-- Exception = {e}\n")