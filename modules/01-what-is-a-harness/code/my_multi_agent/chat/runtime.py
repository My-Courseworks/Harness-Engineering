"""

"""

from dataclasses import dataclass

from google.adk.agents import RunConfig, Agent
from google.adk.agents._streaming_mode import StreamingMode
from google.adk.apps import App
from google.adk.plugins import ReflectAndRetryToolPlugin
from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner


APP_NAME = "multi-agent-team"

@dataclass(frozen=True)
class Runtime:
    app: App
    runner: Runner
    run_config: RunConfig

def build_runtime(root_agent: Agent, session_service: DatabaseSessionService) -> Runtime:
    """
    """

    app = App(
        name=APP_NAME,
        root_agent = root_agent,
        plugins=[ReflectAndRetryToolPlugin(max_retries=3)]
    )

    runner = Runner(
        app=app,
        session_service=session_service,
        auto_create_session=True
    )
    run_config = RunConfig(streaming_mode=StreamingMode.SSE)

    return Runtime(app = app, runner = runner, run_config = run_config)