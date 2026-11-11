"""
Picking the model the agents will run on: first the provider, then one of its models.
"""

import asyncio
from typing import Sequence

import questionary

from commons.config import Provider
from commons.llm import account_note, list_chat_models, providers_with_keys


async def choose_model(providers: Sequence[Provider]) -> tuple[str, str] | None:
    """
    Let the person at the terminal pick a provider and then a model.

    Returns (model_str, api_key_name), ready for create_model, or None if either
    prompt was cancelled (Ctrl+C).
    Raises if no configured provider has its API key set.
    """
    usable = providers_with_keys(providers)
    if not usable:
        raise RuntimeError("No model provider has its API key set. Check `providers` in config.yml and the .env file.")

    # one lookup per provider, all at once and off the event loop; a failed one just shows no note
    notes = await asyncio.gather(*(asyncio.to_thread(account_note, p) for p in usable))

    provider: Provider | None = await questionary.select(
        "Choose a model provider:",
        choices=[
            questionary.Choice(title=f"{p.label} ({note})" if note else p.label, value=p)
            for p, note in zip(usable, notes)
        ],
    ).ask_async()
    if provider is None:
        return None

    # one network call; kept off the event loop
    listed = await asyncio.to_thread(list_chat_models, provider)
    if not listed:
        questionary.print(f"Could not fetch {provider.label}'s model list. Offering its default model only.")
    # the default is the known-good choice: always offered, and listed first
    model_names = [provider.default_model, *(name for name in listed if name != provider.default_model)]

    model_name: str | None = await questionary.select(
        f"Choose a model from {provider.label} (type to filter):",
        choices=model_names,
        default=provider.default_model,
        use_search_filter=True,
        use_jk_keys=False,          # j and k have to be typeable for the filter
    ).ask_async()
    if model_name is None:
        return None

    return f"{provider.litellm_provider}/{model_name}", provider.api_key_env
