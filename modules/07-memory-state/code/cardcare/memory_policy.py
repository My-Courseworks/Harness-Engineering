"""The memory write path, as policy rather than prose: what may be stored, how long it lives, what never goes in.

Both frameworks call these same functions, so the ADK and LangGraph agents differ
only in *where* a fact, an episode or a transcript lives, never in *what* is allowed
to live there or for how long.
"""

import re

from cardcare.clock import add_days, parse_instant

# Semantic memory is a closed schema. A free-form key chosen by the model is how
# two facts that mean the same thing ("contact_pref", "preferred_channel") come
# to coexist and contradict each other.
CONTACT_CHANNELS = ("email", "sms", "secure_message")
FACT_KEYS = ("contact_channel", "travel_notice")
# Changing where the bank contacts a customer is a classic account-takeover step,
# so this key, unlike a travel notice, needs a fresh step-up verification.
FACT_KEYS_NEEDING_VERIFICATION = ("contact_channel",)

# Step-up verification proves possession *now*. It expires, and guessing is capped.
VERIFICATION_TTL_MINUTES = 15
MAX_VERIFICATION_ATTEMPTS = 3

# Retention, per data class. Transcripts are the raw record of everything said, so they
# live shortest; the distilled episode outlives them; bank records (cases, ledger) are
# not memory and keep their own legal retention in the system of record.
TRANSCRIPT_RETENTION_DAYS = 30
EPISODE_RETENTION_DAYS = 180
IDLE_SESSION_MINUTES = 30  # a chat with no turn for this long has ended, even if nobody typed 'exit'

# Working memory is bounded: the model is re-sent at most this many customer turns. When a
# turn would exceed it, the oldest turns are reflected into an episode (and so stay
# recallable with load_memory) and only the most recent WORKING_KEEP_TURNS stay in context.
WORKING_WINDOW_TURNS = 8
WORKING_KEEP_TURNS = 4

CARD_NUMBER_MASK = "[REDACTED CARD NUMBER]"
SECURITY_CODE_MASK = "[REDACTED SECURITY CODE]"
CARD_DIGITS_MASK = "[REDACTED CARD DIGITS]"
EXPIRY_MASK = "[REDACTED EXPIRY]"

# Digits joined by up to three separator characters: "5555 5555", "5555.5555", "5555//5555", "5555  5555".
_DIGIT_RUN = re.compile(r"(?<![0-9A-Za-z])\d(?:[ .\-/_,]{0,3}\d)*(?![0-9A-Za-z])")
_ISO_DATES = re.compile(r"(\d{4}-\d{2}-\d{2}[ ,;]*)+")
_CARD_CONTEXT = re.compile(
    r"\b(cvv2?|cvc2?|csc|cid|security code|card code|verification code|code|on the back|back of (the|my) card|"
    r"three digits|3 digits|four digits|expir\w*|exp\.?|valid (thru|through))\b", re.IGNORECASE)
_EXPIRY = re.compile(r"(?<![\d/])(0?[1-9]|1[0-2])\s?[/\-]\s?(\d{4}|\d{2})(?![\d/])")
_SHORT_CODE = re.compile(r"(?<![\d$€£.,/])\d{3,4}(?![\d/%]|[.,]\d)")
_NOT_A_CODE = re.compile(r"(ending|ends in|ending in|last 4|last four|zip|postal code)\s*(is\s*)?$", re.IGNORECASE)


def _digits(text: str) -> str:
    return re.sub(r"\D", "", text)


def _passes_luhn(digits: str) -> bool:
    total = 0
    for position, char in enumerate(reversed(digits)):
        value = int(char)
        if position % 2:
            value = value * 2 - 9 if value > 4 else value * 2
        total += value
    return total % 10 == 0


def _trailing_digits(text: str) -> str:
    """The digit run a message ends with, if it ends with one (a fragment a next message might complete)."""
    match = re.search(r"\d(?:[ .\-/_,]{0,3}\d)*\W*$", text)
    return _digits(match.group()) if match else ""


def redact_card_secrets(text: str, previous_customer_texts: tuple[str, ...] = ()) -> str:
    """Mask card numbers, security codes and expiry dates before the message is stored anywhere.

    - Any run of 12 or more digits, whatever separates them (spaces, dots, slashes, hyphens, doubles), is
      masked: a card number, or a card number run together with its expiry and code ("5555555555554444 / 12/29
      / 737"). Twelve is below every card length on purpose: the agent never needs a number that long. ISO
      dates written back to back are the one exception.
    - A shorter run that *completes* a Luhn-valid 13-19 digit number together with the digit runs the
      previous one to three customer messages ended with is the second half of a split number, and is
      masked. (The earlier fragments were stored before the number was complete; they never include the
      last four digits, and they leave with the transcript at retention.)
    - In a message about card security (CVV, "the digits on the back", expiry...), or one that follows a
      message in which anything was masked, a standalone 3-4 digit group is masked (a security code, or a
      fragment of a number being typed in pieces) and mm/yy is an expiry.

    The harness applies this to every customer message before it enters the session, so the event log,
    every checkpoint, every memory store and the model itself only see the masks.
    `previous_customer_texts` are the earlier customer messages of this session, oldest first, already masked.
    """
    tails = [t for t in (_trailing_digits(p) for p in previous_customer_texts[-3:]) if t]
    completed_split = False

    def mask_run(match: re.Match) -> str:
        nonlocal completed_split
        run, digits = match.group(), _digits(match.group())
        if len(digits) >= 12 and not _ISO_DATES.fullmatch(run.strip()):
            return CARD_NUMBER_MASK
        for start in range(len(tails)):
            combined = "".join(tails[start:]) + digits
            if 13 <= len(combined) <= 19 and _passes_luhn(combined):
                completed_split = True
                return CARD_NUMBER_MASK
        return run

    masked = _DIGIT_RUN.sub(mask_run, text)
    in_card_context = bool(
        _CARD_CONTEXT.search(masked) or CARD_NUMBER_MASK in masked or completed_split
        or any("[REDACTED" in p for p in previous_customer_texts[-1:])
    )
    if not in_card_context:
        return masked
    masked = _EXPIRY.sub(EXPIRY_MASK, masked)

    token = SECURITY_CODE_MASK if _CARD_CONTEXT.search(masked) else CARD_DIGITS_MASK

    def mask_code(match: re.Match) -> str:
        return match.group() if _NOT_A_CODE.search(masked[:match.start()]) else token

    return _SHORT_CODE.sub(mask_code, masked)


def build_fact(key: str, value: str, valid_until: str | None, now: str) -> dict:
    """Validate a customer-stated fact and stamp it. Raises ValueError with a reason the model can relay."""
    if key not in FACT_KEYS:
        raise ValueError(f"'{key}' is not a fact this assistant may store. Storable facts: {', '.join(FACT_KEYS)}.")
    value = value.strip()
    if not value or redact_card_secrets(value) != value or re.search(r"\d{6,}", _digits(value)):
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


def transcript_is_expired(last_active_at: str | None, now: str) -> bool:
    """A transcript with no recorded activity is treated as expired: it cannot be dated, so it cannot be kept."""
    return not last_active_at or parse_instant(add_days(last_active_at, TRANSCRIPT_RETENTION_DAYS)) <= parse_instant(now)


def session_is_idle(last_active_at: str | None, now: str) -> bool:
    return bool(last_active_at) and (parse_instant(now) - parse_instant(last_active_at)).total_seconds() >= IDLE_SESSION_MINUTES * 60
