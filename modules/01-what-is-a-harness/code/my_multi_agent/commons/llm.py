"""
Everything about the language model the agents run on: which providers have a
key, which models a provider offers, and creating the model object.

- the .env contains the API keys, and is located inside the project root,
   hence create the path accordingly.
- no terminal code lives here; the prompts are in chat/model_choice.py.
"""

import json
import os
import pathlib
import urllib.request
import warnings
from datetime import datetime, timezone
from typing import Callable, Sequence

import litellm
from dotenv import load_dotenv

from google.adk.models import LiteLlm

from commons.config import Provider

PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(ENV_FILE)

# Without this LiteLLM prints a "Provider List" notice to the terminal for every
# model name it cannot place while we look up what a model can do.
litellm.suppress_debug_info = True

# A LiteLLM defect, still present in 1.109.0. For OpenAI models it routes through the
# Responses API (gpt-5.4 and later with tools), its own logging stores chat-format usage
# in a field typed ResponseAPIUsage and then serializes it, so Pydantic warns on every
# model call. This happens after the reply is delivered and changes nothing in the run.
# Only that one warning is hidden; any other serializer warning still shows.
# Remove once LiteLLM fixes _transform_usage_objects in litellm_logging.py.
warnings.filterwarnings(
    "ignore",
    message=r"Pydantic serializer warnings:\s+PydanticSerializationUnexpectedValue\(Expected `ResponseAPIUsage`",
    category=UserWarning,
)


def providers_with_keys(providers: Sequence[Provider]) -> list[Provider]:
    """The configured providers whose API key is set in the environment."""
    return [provider for provider in providers if os.getenv(provider.api_key_env)]


def _is_tool_calling_chat_model(model_str: str) -> bool:
    """True for a chat model that can call tools, according to LiteLLM's bundled registry.
    A model the registry does not know is treated as unusable."""
    try:
        info = litellm.get_model_info(model_str)
    except Exception:
        return False
    return info.get("mode") == "chat" and bool(info.get("supports_function_calling"))


def context_window(model_str: str) -> int | None:
    """How many input tokens the model accepts, according to LiteLLM's bundled registry.
    None when the registry does not know the model, or knows it without this figure."""
    try:
        return litellm.get_model_info(model_str).get("max_input_tokens")
    except Exception:
        return None


def list_chat_models(provider: Provider) -> list[str]:
    """
    The model names this provider offers for the configured key, limited to chat
    models that can call tools, since every agent here uses tools.

    Names come back without the provider prefix, sorted. Returns an empty list
    when the provider cannot be asked. This makes one network call.
    """
    try:
        names = litellm.get_valid_models(
            check_provider_endpoint=True,
            # a provider with its own address is asked through the OpenAI-compatible route;
            # under its own name LiteLLM would answer from a bundled list instead.
            custom_llm_provider="openai" if provider.api_base else provider.litellm_provider,
            api_base=provider.api_base,
            api_key=os.getenv(provider.api_key_env),
        )
    except Exception:
        return []
    bare_names = {name.split("/", 1)[-1] for name in names}
    return sorted(
        name for name in bare_names
        if _is_tool_calling_chat_model(f"{provider.litellm_provider}/{name}")
    )


# ----------------------------- account notes -----------------------------
# A short money note per provider for the provider menu. The two providers expose
# different things, so the notes say different things: DeepSeek reports what is left,
# OpenAI has no balance API and can only report what was spent.

ACCOUNT_LOOKUP_TIMEOUT_SECONDS = 5


def _get_json(url: str, api_key: str) -> dict:
    request = urllib.request.Request(url, headers={"Authorization": f"Bearer {api_key}", "Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=ACCOUNT_LOOKUP_TIMEOUT_SECONDS) as response:
        return json.loads(response.read().decode())


def _deepseek_balance(provider: Provider) -> str | None:
    """What is left on the DeepSeek account, e.g. '1.09 USD left'."""
    body = _get_json(f"{provider.api_base}/user/balance", os.getenv(provider.api_key_env))
    balances = [f"{info['total_balance']} {info['currency']}" for info in body.get("balance_infos", [])]
    return f"{', '.join(balances)} left" if balances else None


def _openai_spend_this_month(provider: Provider) -> str | None:
    """What the OpenAI organization has spent since the 1st (UTC), e.g. '0.42 USD spent this month'.
    Needs a key with usage-read permission; without one there is nothing to show."""
    admin_key = os.getenv(provider.admin_key_env) if provider.admin_key_env else None
    if not admin_key:
        return None
    now = datetime.now(timezone.utc)
    month_start = int(datetime(now.year, now.month, 1, tzinfo=timezone.utc).timestamp())
    # daily buckets: a month always fits in one page of 31
    body = _get_json(f"https://api.openai.com/v1/organization/costs?start_time={month_start}&bucket_width=1d&limit=31", admin_key)
    spent = sum(float(result["amount"]["value"]) for bucket in body.get("data", []) for result in bucket.get("results", []))
    amount = "under 0.01" if 0 < spent < 0.01 else f"{spent:.2f}"
    return f"{amount} USD spent this month"


_ACCOUNT_NOTES: dict[str, Callable[[Provider], str | None]] = {
    "deepseek": _deepseek_balance,
    "openai": _openai_spend_this_month,
}


def account_note(provider: Provider) -> str | None:
    """
    A short note about the provider's account for the provider menu, or None when
    there is nothing to show. It never raises: a slow or failed lookup must not
    get in the way of starting the chat. This makes one network call.
    """
    lookup = _ACCOUNT_NOTES.get(provider.litellm_provider)
    if lookup is None:
        return None
    try:
        return lookup(provider)
    except Exception:
        return None


def create_model(model_str: str, api_key_name: str) -> LiteLlm:
    """
    model_str: the full LiteLLM model string, for example "deepseek/deepseek-v4-flash".
    api_key_name: the name of the environment variable that holds the key.
    """
    api_key = os.getenv(api_key_name)
    if not api_key:
        raise RuntimeError(f"{api_key_name} is not set. Add it to {ENV_FILE}.")
    return LiteLlm(model=model_str, api_key=api_key)
