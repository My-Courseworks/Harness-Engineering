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
    context: str = "grey62"             # the context usage line above the prompt
    context_warn: str = "yellow"        # same line, from Display.context_warn_percent
    context_critical: str = "red"       # same line, from Display.context_critical_percent

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
    show_context_usage: bool = False     # a line above the prompt: how full the model's context window is
    context_warn_percent: int = 70       # at or above this, the line is drawn in styles.context_warn
    context_critical_percent: int = 90   # at or above this, in styles.context_critical
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
class InitialState:
    read_page_size: int = 20

@dataclass(frozen=True)
class Provider:
    label: str                      # shown in the provider menu
    litellm_provider: str           # the prefix LiteLLM expects in a model string, e.g. "openai"
    api_key_env: str                # name of the environment variable that holds the key
    default_model: str              # known-good model: preselected, and offered even if the listing fails
    api_base: str | None = None     # only for providers that must be asked for their model list at their own address
    admin_key_env: str | None = None  # optional: env var of a key allowed to read spend, for the provider menu

@dataclass(frozen=True)
class Config:
    styles: Styles
    labels: Labels
    displays: dict[str, Display]       # keyed by role == "user" or "admin"
    providers: tuple[Provider, ...] = ()
    initial_state: InitialState = InitialState()
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
        initial_state=InitialState(**raw.get("initial_state", {})),
        providers=tuple(Provider(**p) for p in raw.get("providers", [])),
    )