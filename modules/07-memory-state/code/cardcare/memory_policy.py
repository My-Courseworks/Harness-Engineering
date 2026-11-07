"""The memory write path, as policy rather than prose: what may be stored, how long it lives, what never goes in.

Both frameworks call these same functions, so the ADK and LangGraph agents differ
only in *where* a fact, an episode or a transcript lives, never in *what* is allowed
to live there or for how long.
"""

import re

from cardcare.clock import add_days, parse_instant
from cardcare.masking import mask_customer_text

# Semantic memory is a closed schema. A free-form key chosen by the model is how
# two facts that mean the same thing ("contact_pref", "preferred_channel") come
# to coexist and contradict each other.
CONTACT_CHANNELS = ("email", "sms", "secure_message")
FACT_KEYS = ("contact_channel", "travel_notice")
# Changing where the bank contacts a customer is a classic account-takeover step,
# so this key, unlike a travel notice, needs a fresh step-up verification.
FACT_KEYS_NEEDING_VERIFICATION = ("contact_channel",)

# Step-up verification proves possession *now*. It expires, and guessing is capped on the account (not the
# conversation): 3 failures lock verification for 24 hours, and opening a new chat does not reset it.
VERIFICATION_TTL_MINUTES = 15
MAX_VERIFICATION_ATTEMPTS = 3
VERIFICATION_LOCK_HOURS = 24

# Retention, per data class. Transcripts are the raw record of everything said, so they live shortest:
# a session is deleted 30 days after its *first* turn, however recently it was used, so no line of any
# transcript outlives 30 days (plus one maintenance interval). The distilled episode lives 180 days. Bank
# records (cases, ledger) are not memory and keep their own legal retention in the system of record.
TRANSCRIPT_RETENTION_DAYS = 30
EPISODE_RETENTION_DAYS = 180
IDLE_SESSION_MINUTES = 30  # a chat with no turn for this long has ended, even if nobody typed 'exit'

# Working memory is bounded: the model is re-sent at most this many customer turns. When a
# turn would exceed it, the oldest turns are reflected into an episode (and so stay
# recallable with load_memory) and only the most recent WORKING_KEEP_TURNS stay in context.
WORKING_WINDOW_TURNS = 8
WORKING_KEEP_TURNS = 4

def build_fact(key: str, value: str, valid_until: str | None, now: str) -> dict:
    """Validate a customer-stated fact and stamp it. Raises ValueError with a reason the model can relay."""
    if key not in FACT_KEYS:
        raise ValueError(f"'{key}' is not a fact this assistant may store. Storable facts: {', '.join(FACT_KEYS)}.")
    value = value.strip()
    if not value or mask_customer_text(value) != value or len(re.sub(r"\D", "", value)) >= 6:
        raise ValueError("That value contains digits that look like card or account data; it must never be stored.")
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


def verification_is_fresh(verified_at: str | None, now: str) -> bool:
    if not verified_at:
        return False
    age_minutes = (parse_instant(now) - parse_instant(verified_at)).total_seconds() / 60
    return 0 <= age_minutes <= VERIFICATION_TTL_MINUTES


def verification_gate_error(verified_at: str | None, now: str, action: str) -> str | None:
    """None if the step-up is fresh; otherwise the reason the model must relay."""
    if not verified_at:
        return f"{action} requires verify_identity in this conversation"
    if not verification_is_fresh(verified_at, now):
        return f"identity verification expired ({VERIFICATION_TTL_MINUTES} minutes); call verify_identity again before {action}"
    return None


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


def transcript_is_expired(first_active_at: str | None, now: str) -> bool:
    """A session expires 30 days after its first turn. One that cannot be dated cannot be kept."""
    return not first_active_at or parse_instant(add_days(first_active_at, TRANSCRIPT_RETENTION_DAYS)) <= parse_instant(now)


def session_is_idle(last_active_at: str | None, now: str) -> bool:
    return bool(last_active_at) and (parse_instant(now) - parse_instant(last_active_at)).total_seconds() >= IDLE_SESSION_MINUTES * 60
