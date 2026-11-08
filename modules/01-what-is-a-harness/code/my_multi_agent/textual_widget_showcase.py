"""A standalone taste of Textual's collapsible + interactive widgets.

Run:  pip install textual && python textual_showcase.py

No agent, no ADK, no project imports — just the primitives, so you can feel
what Textual gives you before tuning any of it into the chat app.
"""

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import (
    Collapsible,
    Footer,
    Header,
    Input,
    Label,
    LoadingIndicator,
    Markdown,
    Static,
    Tree,
)


class WidgetShowcase(App):
    """Four capabilities on one screen:

    1. Collapsible Tree      — click ▸/▾ or press Enter on a node to fold/unfold.
    2. Collapsible section   — click the title bar to hide/show its body.
    3. Spinner               — LoadingIndicator (Claude-Code style, no \\r tricks).
    4. Live prompt           — type + Enter to append a node to the tree.
    """

    CSS = """
    #demo { height: 1fr; padding: 1 2; }
    #tree-column { width: 55%; border: round $accent; padding: 0 1; }
    #right { width: 45%; border: round $primary; padding: 0 1; }
    #prompt { dock: bottom; }
    Collapsible { border: solid $panel-lighten-2; margin: 1 0; }
    """

    def compose(self) -> ComposeResult:
        yield Header()

        with Horizontal(id="demo"):
            # LEFT: the star — a collapsible Tree.
            with Vertical(id="tree-column"):
                yield Label(
                    "[b]Collapsible Tree[/b] — click a ▸/▾ or press Enter on a node",
                    id="caption",
                )
                yield Tree("tools", id="tree")

            # RIGHT: the other primitives you asked about.
            with VerticalScroll(id="right"):
                yield Markdown("## Foldable sections\nClick a title bar to fold/unfold.")

                with Collapsible(title="Thinking", collapsed=False):
                    yield LoadingIndicator()
                    yield Static("The model is reasoning… (hidden when folded)")


                with Collapsible(title="Tool call", collapsed=False):
                    yield Static('args    {"emp_id": 1, "message": "hi"}')
                    yield Static("→       Notification recorded for this employee.")

                yield Markdown("## Spinner\n`LoadingIndicator` is the spinner, free.")
                yield Label("Type below and press Enter to add a node →")

        yield Input(placeholder="Add a tool-call node: type a name…", id="prompt")
        yield Footer()

    def on_mount(self) -> None:
        tree = self.query_one("#tree", Tree)

        # Seed two nodes: one expanded, one collapsed.
        notify = tree.root.add("notify", expand=True)
        notify.add_leaf("args   {'emp_id': 1, 'message': 'hi'}")
        notify.add_leaf("→      Notification recorded")

        people = tree.root.add("list_employees", expand=False)
        people.add_leaf("→      200 employees")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if not event.value.strip():
            return
        tree = self.query_one("#tree", Tree)
        node = tree.root.add(event.value.strip(), expand=True)
        node.add_leaf("args   (streaming…)")
        event.input.value = ""


if __name__ == "__main__":
    WidgetShowcase().run()