"""Which model both agents use, and where its key comes from.

The key is read, never written: from the environment, else a gitignored `.env`
next to this code, else module 01's gitignored `.env`. It is handed to the model
client at construction and never placed in state, memory, or a transcript.
"""

import os
from pathlib import Path

import litellm
from dotenv import dotenv_values

DEEPSEEK_MODEL = "deepseek-v4-flash"
# Transport-level retries only (a 5xx or a dropped connection is retried twice, with litellm's backoff). They do not
# change sampling: a reply that arrives is never re-asked for. Both agents' model clients and the judge use them.
TRANSPORT_RETRIES = 2
litellm.num_retries = TRANSPORT_RETRIES
# The eval judge is a different, larger model than the agent, so the agent is not graded by itself.
JUDGE_MODEL = "deepseek-v4-pro"
JUDGE_SAMPLES = 3

_CODE_DIR = Path(__file__).resolve().parent.parent
_KEY_FILES = (
    _CODE_DIR / ".env",
    _CODE_DIR.parent.parent / "01-what-is-a-harness" / "code" / "my_multi_agent" / ".env",
)


def deepseek_api_key() -> str:
    key = os.environ.get("DEEPSEEK_API_KEY")
    for path in _KEY_FILES:
        if key:
            break
        if path.exists():
            key = dotenv_values(path).get("DEEPSEEK_API_KEY")
    if not key:
        raise RuntimeError("Set DEEPSEEK_API_KEY in the environment or in modules/07-memory-state/code/.env")
    return key
