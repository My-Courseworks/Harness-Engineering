"""

"""

from dataclasses import dataclass

from google.adk.agents import RunConfig, Agent
from google.adk.agents._streaming_mode import StreamingMode
from google.adk.apps import App
from google.adk.plugins import ReflectAndRetryToolPlugin
from google.adk.plugins.global_instruction_plugin import GlobalInstructionPlugin
from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner


APP_NAME = "multi-agent-team"

@dataclass(frozen=True)
class Runtime:
    app: App
    runner: Runner
    run_config: RunConfig

def build_runtime(root_agent: Agent, session_service: DatabaseSessionService,
                  global_instruction: str | None = None) -> Runtime:
    """
    global_instruction, when given, is prepended to the system instruction of
    every model call on this runner, sub-agents included.
    """
    plugins = [ReflectAndRetryToolPlugin(max_retries=3)]
    if global_instruction:
        plugins.append(GlobalInstructionPlugin(global_instruction=global_instruction))

    app = App(
        name=APP_NAME,
        root_agent = root_agent,
        plugins=plugins
    )

    runner = Runner(
        app=app,
        session_service=session_service
    )
    run_config = RunConfig(streaming_mode=StreamingMode.SSE)

    return Runtime(app = app, runner = runner, run_config = run_config)