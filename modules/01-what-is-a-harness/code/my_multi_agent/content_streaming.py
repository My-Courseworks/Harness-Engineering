"""
This module handles the whole Markdown style printing with emulating the 
flush style printing.
"""

from rich.console import Group
from rich.markdown import Markdown

from enum import StrEnum

chat_transcript = Group()



class MessageType(StrEnum):
    THINKING = "thinking"
    TOOL_CALL = "tool_call"
    TOOL_RESPONSE = "tool_response"
    USER = "user"
    AGENT = "agent"


# message_type -> (style, render_as_markdown)
MESSAGE_STYLES = {
    "thinking":      "grey62 italic",
    "tool_call":     "#c98b8b",   # dull red
    "tool_response": "#8b9cc9",   # dull blue
    "user":          "#7ed957",   # green
    "agent":         "#f97316",    # Claude-Code orange
}

PREFIXES = {
    "thinking":      "[Thinking] ",
    "tool_call":     "⚙ ",
    "tool_response": "  ↪ ",
    "user":          "You: ",
    "agent":         "",                          # body is the markdown itself
}

def render():
    """
    Function that constantly keeps the chat wall updated with beautifully rendered 
    Markdown content
    """
    return chat_transcript

def update_content(
        message_type: MessageType,
        message_text: str,
        is_prefix_needed: bool = True
):
    """
    Function that writes to the chat wall.
    """
    style = MESSAGE_STYLES[message_type]
    prefix = PREFIXES[message_type]
    complete_msg = prefix + message_text if is_prefix_needed else message_text
    renderable_piece = Markdown(complete_msg, style=style)
    chat_transcript.renderables.append(renderable_piece)