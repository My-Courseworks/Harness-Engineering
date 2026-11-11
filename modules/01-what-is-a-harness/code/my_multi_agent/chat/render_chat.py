"""
Printers for the chat transcript. Everything is printed once and left alone,
except the agent answer. Unmasked roles stream it inside one Live region.
Masked roles get it unit by unit: a unit is printed only after it has been
checked, and is never redrawn.
"""

from dataclasses import dataclass

from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.text import Text

from chat.masking.utils import CleanUnit
from chat.masking.units import NOTHING_TO_SHOW, split_units

from commons.config import Styles, Display, Labels

CONTEXT_BAR_CELLS = 20      # width of the bar in the context usage line


@dataclass
class AnswerStream:
    live: Live | None          # None: nothing is redrawn (hidden segment, or masked unit stream)
    buffer: str = ""
    hidden: bool = False       # sub-agent answer this role does not see: draw nothing at all
    released: int = 0          # masked stream: how much of buffer has been checked and consumed
    printed: bool = False      # masked stream: whether any unit reached the screen
    last_blank: bool = True    # masked stream: collapse blank lines left behind by withheld units


@dataclass(frozen=True)
class View:
    styles: Styles
    labels: Labels
    display: Display
    root_agent_name: str                         # only this author answers the user
    clean_unit: CleanUnit | None = None          # None: unmasked role, live streaming


def shows_answer(view: View, author: str) -> bool:
    """Sub-agent answer text is process narration, and it never passes through the
    masking callback (which sits on the root agent only). Show it only to roles
    configured for it."""
    return author == view.root_agent_name or view.display.show_subagent_answers


def print_user(console: Console, view: View, text: str) -> None:
    console.print(Text(f"\n{view.labels.user} {text}", style=view.styles.user))


def _short_count(tokens: int) -> str:
    """864 -> '864', 12400 -> '12.4k', 128000 -> '128k', 1047576 -> '1.05M'."""
    if tokens >= 999_950:
        return f"{tokens / 1_000_000:.2f}".rstrip("0").rstrip(".") + "M"
    if tokens >= 1_000:
        return f"{tokens / 1_000:.1f}".rstrip("0").rstrip(".") + "k"
    return str(tokens)


def _context_usage_line(used: int, window: int | None) -> str:
    """'context ██░░░░░░░░░░░░░░░░░░ 9.7% · 12.4k / 128k', or the count alone when the
    window is unknown: a bar and a percentage would then be a guess."""
    if window is None:
        return f"context {_short_count(used)} tokens"
    filled = min(CONTEXT_BAR_CELLS, round(CONTEXT_BAR_CELLS * used / window))
    bar = "█" * filled + "░" * (CONTEXT_BAR_CELLS - filled)
    return f"context {bar} {100 * used / window:.1f}% · {_short_count(used)} / {_short_count(window)}"


def print_context_usage(console: Console, view: View, used: int | None, window: int | None) -> None:
    """
    One line saying how full the model's context window is, meant to sit just above
    the prompt.

    used: tokens the conversation occupies, or None before the first model call,
        in which case nothing is printed.
    window: input tokens the model accepts, or None when that is unknown.
    """
    if not view.display.show_context_usage or used is None:
        return
    percent = 100 * used / window if window else 0
    if percent >= view.display.context_critical_percent:
        style = view.styles.context_critical
    elif percent >= view.display.context_warn_percent:
        style = view.styles.context_warn
    else:
        style = view.styles.context
    console.print(Text(f"\n{_context_usage_line(used, window)}", style=style))


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
    """Non-streaming form, used for history replay. For masked roles the caller
    passes the persisted clean text."""
    if not shows_answer(view, author):
        return
    print_answer_header(console, view, author)
    console.print(Markdown(text))


def _print_unit(console: Console, unit: str) -> None:
    if unit.strip():
        console.print(Markdown(unit))
    else:
        console.print()            # a blank line in the answer stays a blank line


async def _release_units(console: Console, view: View, stream: AnswerStream, final: bool) -> None:
    """Check every closed unit not yet consumed; print the ones that may be shown."""
    for unit in split_units(stream.buffer[stream.released:], final=final):
        stream.released += len(unit)
        cleaned = await view.clean_unit(unit)
        if cleaned is None:
            continue
        blank = not cleaned.strip()
        if blank and stream.last_blank:
            continue
        _print_unit(console, cleaned)
        stream.last_blank = blank
        stream.printed = stream.printed or not blank


def open_answer(console: Console, view: View, author: str) -> AnswerStream:
    if not shows_answer(view, author):
        return AnswerStream(live=None, hidden=True)   # the caller's state machine is unchanged
    print_answer_header(console, view, author)
    if view.clean_unit is not None:
        return AnswerStream(live=None)                 # masked: units are printed, never redrawn
    live = Live(Markdown(""), console=console, refresh_per_second=10, transient=False)
    live.start()
    return AnswerStream(live=live)


async def append_answer(console: Console, stream: AnswerStream, view: View, delta: str) -> None:
    stream.buffer += delta
    if stream.hidden:
        return
    if stream.live is None:
        await _release_units(console, view, stream, final=False)
        return
    stream.live.update(Markdown(stream.buffer))   # tail-commit for tall answers plugs in here later


async def close_answer(console: Console, stream: AnswerStream, view: View, final_text: str | None = None) -> None:
    if stream.hidden:
        return
    if stream.live is None:
        if not stream.buffer and final_text:
            stream.buffer = final_text             # answer arrived without partials
        await _release_units(console, view, stream, final=True)
        if stream.buffer.strip() and not stream.printed:
            console.print(Markdown(NOTHING_TO_SHOW))
        return
    stream.live.update(Markdown(final_text or stream.buffer))
    stream.live.stop()
