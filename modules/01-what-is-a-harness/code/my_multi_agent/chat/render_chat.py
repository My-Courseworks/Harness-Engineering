"""
Printers for the chat transcript. Everything is printed once and left alone,
except the agent answer, which streams inside one Live region per message.
"""

from typing import Callable
from dataclasses import dataclass

from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.text import Text

from commons.config import Styles, Display, Labels


@dataclass
class AnswerStream:
    live: Live | None          # None: a hidden segment; appends and close draw nothing
    buffer: str = ""

def passthrough(text: str) -> str:
    """Identity render: what the model wrote is what gets drawn."""
    return text


@dataclass(frozen=True)
class View:
    styles: Styles
    labels: Labels
    display: Display
    root_agent_name: str                         # only this author answers the user
    render: Callable[[str], str] = passthrough   # admin view: draw text as-is


def shows_answer(view: View, author: str) -> bool:
    """Sub-agent answer text is process narration, and it never passes through the
    masking callback (which sits on the root agent only). Show it only to roles
    configured for it."""
    return author == view.root_agent_name or view.display.show_subagent_answers


def print_user(console: Console, view: View, text: str) -> None:
    console.print(Text(f"\n{view.labels.user} {text}", style=view.styles.user))


def print_tool_call(console: Console, view: View, author: str, name: str, args: dict | None) -> None:
    if view.display.show_tool_call:
        console.print(Text(f"\n\n{view.labels.tool_call_glyph} {author} → {name}({args or {}})", style=view.styles.tool_call))


def print_tool_response(console: Console, view: View,name: str, response: dict | None) -> None:
    if view.display.show_tool_response:
        console.print(Text(f"  {view.labels.tool_response_glyph} {name}: {response}", style=view.styles.tool_response))


def print_thinking_header(console: Console, view: View,author: str) -> None:
    if view.display.show_thinking:
        console.print(Text(f"\n[{author} {view.labels.thinking_prefix}]", style=view.styles.thinking))


def print_thinking_delta(console: Console, view: View, delta: str) -> None:
    if view.display.show_thinking:
        # soft_wrap=True: let the terminal wrap, since rich cannot track the cursor across end="" calls.
        console.print(delta, end="", style=view.styles.thinking, markup=False, highlight=False, soft_wrap=True)


def print_answer_header(console: Console, view: View,author: str) -> None:
    if view.display.show_agent_name:
        console.print(Text(f"\n[{author}]:", style=view.styles.agent))
    else:
        console.print(Text(f"\n[agent]:", style=view.styles.agent))


def print_answer(console: Console, view: View, author: str, text: str) -> None:
    """Non-streaming form, used for history replay."""
    if not shows_answer(view, author):
        return
    print_answer_header(console, view, author)
    console.print(Markdown(view.render(text)))



def open_answer(console: Console, view: View, author: str) -> AnswerStream:
    if not shows_answer(view, author):
        return AnswerStream(live=None)     # hidden segment: the caller's state machine is unchanged
    print_answer_header(console, view, author)
    live = Live(Markdown(""), console=console, refresh_per_second=10, transient=False)
    live.start()
    return AnswerStream(live=live)


def append_answer(stream: AnswerStream, view: View, delta: str) -> None:
    stream.buffer += delta
    if stream.live is None:
        return
    stream.live.update(Markdown(view.render(stream.buffer)))   # tail-commit for tall answers plugs in here later


def close_answer(stream: AnswerStream, view: View, final_text: str | None = None) -> None:
    if stream.live is None:
        return
    stream.live.update(Markdown(view.render(final_text or stream.buffer)))
    stream.live.stop()
