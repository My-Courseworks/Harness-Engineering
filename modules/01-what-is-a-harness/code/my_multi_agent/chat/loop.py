"""
The conversation itself: show how full the context is, ask the user, run the turn,
repeat until the user leaves.
"""

import questionary
from prompt_toolkit.history import InMemoryHistory

from google.adk.sessions.session import Session

from rich.console import Console

from chat.context_usage import tokens_in_context
from chat.render_chat import View, print_context_usage
from chat.runtime import Runtime
from chat.sessions import user_messages
from chat.turn import get_async_agent_response

LEAVE_WORDS = ("exit", "quit")


async def _prompt_user(view: View, history: InMemoryHistory) -> str | None:
    """
    Ask for the next message. Returns it, or None when the user wants to leave:
    Ctrl+C, or one of LEAVE_WORDS. An empty line asks again.
    """
    style = questionary.Style([
        ("qmark", ""),
        ("question", view.styles.user),
        ("answer", view.styles.user)
    ])
    while True:
        query = await questionary.text(
            message = f"\n{view.labels.user} ",
            qmark="",
            style = style,
            history = history
        ).ask_async()
        if query is None or query in LEAVE_WORDS:
            return None
        if query.strip():
            return query


async def run_chat_loop(runtime: Runtime, session: Session, console: Console, view: View,
                        context_window: int | None) -> None:
    """
    Converse in this session until the user leaves.

    session: the stored session as read at startup. It names the conversation, and
        seeds the prompt history and the first context usage line. The turns
        themselves go through runtime.runner, which keeps the store up to date.
    context_window: input tokens the model accepts, or None when unknown.
    """
    # up and down arrows walk through what the user typed in this session. One history
    # object for the whole loop: the prompt appends every new input to it by itself.
    history = InMemoryHistory(user_messages(session))

    # None until the root agent has made a model call in this session.
    used = tokens_in_context(session.events, view.root_agent_name)

    while True:
        print_context_usage(console=console, view=view, used=used, window=context_window)

        query = await _prompt_user(view=view, history=history)
        if query is None:
            return

        try:
            turn_events = await get_async_agent_response(query=query, runner=runtime.runner,
                run_config=runtime.run_config, user_id=session.user_id, session_id=session.id,
                console=console, view=view)
        except Exception:
            # One failed turn must not end the session. Tracebacks name modules
            # and tools, so only roles configured to see error details get them.
            if view.display.show_error_details:
                console.print_exception()
            else:
                console.print("\nSomething went wrong on my side. Please try again.", style=view.styles.agent)
            continue

        # a turn answered entirely by a sub-agent holds no root agent call: keep the last figure
        used = tokens_in_context(turn_events, view.root_agent_name) or used
