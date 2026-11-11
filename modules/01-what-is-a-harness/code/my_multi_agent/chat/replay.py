"""
"""

from rich.console import Console

from google.adk.sessions.session import Session

from chat.masking.masking_policy import DISPLAY_TEXT_KEY
from chat.render_chat import (
    View,
    print_user, 
    print_answer,
    print_thinking_header, print_thinking_delta,
    print_tool_call, print_tool_response
)

async def replay_session(session: Session | None, console: Console, view: View):
    """
    Print the last five turns of a stored session. The caller fetches the session,
    so it can be read once and shared with whatever else needs it.
    """
    try:
        if session:
            invocations = {}
            for event in getattr(session, 'events'):
                # skip empty-invocation events like the missing-key additions to state of resumed sessions.
                if not event.invocation_id:
                    continue
                if event.invocation_id not in invocations:
                    invocations[event.invocation_id] = event.timestamp
                else:
                    invocations[event.invocation_id] = max(event.timestamp, invocations[event.invocation_id])

            last_5_invocations = [x[0] for x in sorted(invocations.items(), key=lambda x: x[1], reverse=True)][:5][::-1]

            for event in getattr(session, 'events'):
                if event.invocation_id not in last_5_invocations:
                    continue
                if not event.content or not event.content.parts:
                    continue

                author = event.author or "agent"

                for part in getattr(event.content, 'parts') or []:
                    if event.content.role == "user" and part.text:
                        print_user(console=console, view=view, text=part.text)
                    elif part.function_call:
                        print_tool_call(console=console, view=view, author=author, name = part.function_call.name, args = part.function_call.args)
                    elif part.function_response:
                        print_tool_response(console=console, view=view, name = part.function_response.name, response = part.function_response.response)
                    elif part.text and part.thought:
                        print_thinking_header(console=console, view=view, author=author)
                        print_thinking_delta(console=console, view=view, delta=part.text)
                        console.print()
                    elif part.text:
                        # If the masking callback rewrote this answer for a non-admin, the
                        # name-free version was persisted with the event; prefer it.
                        # Admin events never carry the key, so they fall through to raw text.
                        masked_text: str | None = (event.custom_metadata or {}).get(DISPLAY_TEXT_KEY)
                        print_answer(console=console, view=view, author=author, text=masked_text or part.text)
                    
    except Exception:
        # Tracebacks name modules and tools; only roles configured for it see them.
        if view.display.show_error_details:
            console.print_exception()
        else:
            console.print("\nCould not load earlier messages of this session.", style=view.styles.agent)