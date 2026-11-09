"""
Printers for the chat transcript. Everything is printed once and left alone,
except the agent answer, which streams inside one Live region per message.
"""

from dataclasses import dataclass

from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.text import Text

from commons.config import Styles, Display, Labels


@dataclass
class AnswerStream:
    live: Live
    buffer: str = ""

@dataclass(frozen=True)
class View:
    styles: Styles
    labels: Labels
    displays: dict[str, Display]


def print_user(console: Console, view: View, text: str) -> None:
    console.print(Text(f"\n{view.labels.user} {text}", style=view.styles.user))


def print_tool_call(console: Console, view: View, author: str, name: str, args: dict | None) -> None:
    console.print(Text(f"\n{view.labels.tool_call_glyph} {author} → {name}({args or {}})", style=view.styles.tool_call))


def print_tool_response(console: Console, view: View,name: str, response: dict | None) -> None:
    console.print(Text(f"  {view.labels.tool_response_glyph} {name}: {response}", style=view.styles.tool_response))


def print_thinking_header(console: Console, view: View,author: str) -> None:
    console.print(Text(f"\n[{author} {view.labels.thinking_prefix}]", style=view.styles.thinking))


def print_thinking_delta(console: Console, view: View, delta: str) -> None:
    # soft_wrap=True: let the terminal wrap, since rich cannot track the cursor across end="" calls.
    console.print(delta, end="", style=view.styles.thinking, markup=False, highlight=False, soft_wrap=True)


def print_answer_header(console: Console, view: View,author: str) -> None:
    console.print(Text(f"\n[{author}]:", style=view.styles.agent))


def print_answer(console: Console, view: View, author: str, text: str) -> None:
    """Non-streaming form, used for history replay."""
    print_answer_header(console, view, author)
    console.print(Markdown(text))



def open_answer(console: Console, view: View, author: str) -> AnswerStream:
    print_answer_header(console, view, author)
    live = Live(Markdown(""), console=console, refresh_per_second=10, transient=False)
    live.start()
    return AnswerStream(live=live)


def append_answer(stream: AnswerStream, delta: str) -> None:
    stream.buffer += delta
    stream.live.update(Markdown(stream.buffer))   # tail-commit for tall answers plugs in here later


def close_answer(stream: AnswerStream, final_text: str | None = None) -> None:
    stream.live.update(Markdown(final_text or stream.buffer))
    stream.live.stop()
