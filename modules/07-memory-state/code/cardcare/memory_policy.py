"""The memory write path, as policy rather than prose: what may be stored, how it goes stale, what never goes in.

Both frameworks call these same functions, so the ADK and LangGraph agents differ
only in *where* a fact or episode lives, never in *what* is allowed to live there.
"""

import re

from cardcare.clock import add_days, parse_instant

# Semantic memory is a closed schema. A free-form key chosen by the model is how
# two facts that mean the same thing ("contact_pref", "preferred_channel") come
# to coexist and contradict each other.
CONTACT_CHANNELS = ("email", "sms", "secure_message")
FACT_KEYS = ("contact_channel", "travel_notice")
# Changing where the bank contacts a customer is a classic account-takeover step,
# so this key, unlike a travel notice, needs identity verified in the current session.
FACT_KEYS_NEEDING_VERIFICATION = ("contact_channel",)

# Episodes (reflections on past conversations) are personal data with a retention window.
EPISODE_RETENTION_DAYS = 180

_CARD_NUMBER = re.compile(r"(?<!\d)(?:\d[ -]?){12,18}\d(?!\d)")
_CVV = re.compile(r"\b(cvv|cvc|security code)\b\D{0,12}\d{3,4}\b", re.IGNORECASE)


def _passes_luhn(digits: str) -> bool:
    total = 0
    for position, char in enumerate(reversed(digits)):
        value = int(char)
        if position % 2:
            value = value * 2 - 9 if value > 4 else value * 2
        total += value
    return total % 10 == 0


def redact_card_secrets(text: str) -> str:
    """Mask full card numbers (13-19 digits passing Luhn) and CVV codes.

    The harness applies this to every customer message *before* it enters the
    session, so the event log, every memory store and the model itself only
    ever see the mask.
    """

    def mask_card(match: re.Match) -> str:
        digits = re.sub(r"\D", "", match.group())
        return "[REDACTED CARD NUMBER]" if _passes_luhn(digits) else match.group()

    return _CVV.sub("[REDACTED SECURITY CODE]", _CARD_NUMBER.sub(mask_card, text))


def build_fact(key: str, value: str, valid_until: str | None, now: str) -> dict:
    """Validate a customer-stated fact and stamp it. Raises ValueError with a reason the model can relay."""
    if key not in FACT_KEYS:
        raise ValueError(f"'{key}' is not a fact this assistant may store. Storable facts: {', '.join(FACT_KEYS)}.")
    value = value.strip()
    if not value or redact_card_secrets(value) != value or re.search(r"\d{9,}", value):
        raise ValueError("That value looks like an account or card number; it must never be stored.")
    if key == "contact_channel":
        if value not in CONTACT_CHANNELS:
            raise ValueError(f"contact_channel must be one of {', '.join(CONTACT_CHANNELS)}.")
        return {"value": value, "as_of": now, "expires_at": None}
    if not valid_until:
        raise ValueError("A travel notice needs the date the customer returns (valid_until, YYYY-MM-DD).")
    if parse_instant(valid_until) < parse_instant(now[:10]):
        raise ValueError("valid_until is in the past.")
    # A travel notice is useful only while the trip lasts; it expires the day after the return date.
    return {"value": value, "as_of": now, "valid_until": valid_until, "expires_at": add_days(valid_until, 1)}


def fact_is_expired(fact: dict, now: str) -> bool:
    return bool(fact.get("expires_at")) and parse_instant(fact["expires_at"]) <= parse_instant(now)


def render_profile(facts: dict[str, dict], now: str) -> str:
    """The preloaded slice of semantic memory: small, always relevant, re-sent every turn."""
    lines = []
    for key in FACT_KEYS:
        fact = facts.get(key)
        if not fact or fact_is_expired(fact, now):
            lines.append(f"- {key}: none on file")
        elif key == "travel_notice":
            lines.append(f"- travel_notice: {fact['value']} until {fact['valid_until']} (recorded {fact['as_of'][:10]})")
        else:
            lines.append(f"- {key}: {fact['value']} (recorded {fact['as_of'][:10]})")
    return "\n".join(lines)


def episode_expires_at(now: str) -> str:
    return add_days(now, EPISODE_RETENTION_DAYS)


def episode_is_expired(episode: dict, now: str) -> bool:
    return parse_instant(episode["expires_at"]) <= parse_instant(now)
