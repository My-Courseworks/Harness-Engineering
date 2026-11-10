"""
Load config for the ops desk chat agent
"""

from pathlib import Path
import yaml


from dataclasses import dataclass

CONFIG_FILE = Path(__file__).resolve().parent.parent / "config.yml"


@dataclass(frozen=True)
class Styles:
    user: str
    thinking: str
    agent: str
    tool_call: str
    tool_response: str

@dataclass(frozen=True)
class Labels:
    user: str
    thinking_prefix: str
    tool_call_glyph: str
    tool_response_glyph: str

@dataclass(frozen=True)
class Display:
    show_thinking: bool = False
    show_tool_call: bool = False
    show_tool_response: bool = False
    show_agent_name: bool = False
    show_error_details: bool = False     # tracebacks carry module and tool names
    show_subagent_answers: bool = False  # sub-agents narrate process; only the root agent answers the user
    tool_response_max_chars: int = 300
    code_theme: str = "monokai"
    width: int = 0                      # use default terminal width

@dataclass(frozen=True)
class Database:
    path: str = "data/ops.db"
    sessions_path: str = "data/session.db"

@dataclass(frozen=True)
class Features:
    masking: bool = True                    # security feature: a missing key means on
    masked_role_instruction: bool = True

@dataclass(frozen=True)
class Config:
    styles: Styles
    labels: Labels
    displays: dict[str, Display]       # keyed by role == "user" or "admin"
    features: Features = Features()
    database: Database = Database()

def load_config(path: Path = CONFIG_FILE) -> Config:
    """
    Use the config file provided or the default config file
    to load up config required.
    """
    raw = yaml.safe_load(path.read_text())
    return Config(
        styles=Styles(**raw.get("styles", {})),
        labels=Labels(**raw.get("labels", {})),
        displays={role: Display(**d)
                  for role, d in raw.get("display", {}).items()},
        features=Features(**raw.get("features", {})),
        database=Database(**raw.get("database", {})),
    )