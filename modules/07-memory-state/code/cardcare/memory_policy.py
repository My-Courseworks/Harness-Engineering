"""The memory write path, as policy rather than prose: what may be stored, how long it lives, what never goes in.

Both frameworks call these same functions, so the ADK and LangGraph agents differ
only in *where* a fact, an episode or a transcript lives, never in *what* is allowed
to live there or for how long.
"""

import re

from cardcare.clock import add_days, add_minutes, parse_instant
from cardcare.masking import ONE_TIME_CODE_MASK, mask_customer_text

# Semantic memory is a closed schema. A free-form key chosen by the model is how
# two facts that mean the same thing ("contact_pref", "preferred_channel") come
# to coexist and contradict each other.
CONTACT_CHANNELS = ("email", "sms", "secure_message")
DEFAULT_CHANNEL = "secure_message"
FACT_KEYS = ("contact_channel", "travel_notice")
# Changing where the bank contacts a customer is a classic account-takeover step, and so is removing the channel
# (messages would then go to the app, which whoever holds the phone reads): writing or deleting this key, unlike a
# travel notice, needs a fresh step-up verification. Erasing everything does not: the login is enough to exercise the
# right to erasure, and an erasure gives whoever holds the phone nothing (round 4 tried a gate and reverted it).
FACT_KEYS_NEEDING_VERIFICATION = ("contact_channel",)

# A fact is preloaded into every later system prompt, so its value is data with a grammar, never free text: a
# travel notice is a place name (letters, spaces and light punctuation, at most 60 characters and 8 words) and
# holds nothing that reads as an instruction. Its horizon is bounded, like every other class of memory.
TRAVEL_NOTICE_MAX_DAYS = 365
_PLACE = re.compile(r"[^\W\d_](?:[^\W\d_]|[ .,'\u2019&()\-])*")
_INSTRUCTION_WORDS = re.compile(r"\b(assistant|system|ignore|instructions?|prompt|verif\w*|note|skip|policy|rule|always|never|must|"
                                r"admin|override|vip|exempt|waiver|bypass|pretend|act as)\b", re.IGNORECASE)

# Working memory is bounded in size as well as in turns: one customer message is kept up to this many characters.
MAX_CUSTOMER_MESSAGE_CHARS = 4000
# A reminder holds the customer's own words until it fires, so how far ahead it may be set is a retention limit.
REMINDER_HORIZON_DAYS = 90

# Step-up verification proves possession *now*. It expires, and guessing is capped on the account (not the
# conversation): 3 failures lock verification for 24 hours, and opening a new chat does not reset it.
VERIFICATION_TTL_MINUTES = 15
MAX_VERIFICATION_ATTEMPTS = 3
VERIFICATION_LOCK_HOURS = 24
# The step-up is tiered (round 4): filing a dispute needs the last four and ZIP (something the customer knows); changing
# or removing the contact channel, the account-takeover actions, also needs a one-time code sent to the mobile number
# or email the bank holds on the account (something the customer has). The code is 6 digits, lives CODE_TTL_MINUTES,
# is single-use, dies after CODE_MAX_ENTRIES wrong entries, and a new one can be sent CODE_RESEND_SECONDS after the last.
# A correct code is good for the same VERIFICATION_TTL_MINUTES as the digits; every wrong code is a failed attempt on
# the same account lock as a wrong last four.
CODE_TTL_MINUTES = 5
CODE_MAX_ENTRIES = 3
CODE_RESEND_SECONDS = 60
MAX_CODES_PER_DAY = 5  # codes sent to one account in any 24 hours: without a cap, 60 fit in an hour (round-5 review)

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
    if len(value) > 60 or len(value.split()) > 8 or not _PLACE.fullmatch(value) or _INSTRUCTION_WORDS.search(value):
        raise ValueError("A travel notice's destination is a place name only (for example 'Lisbon' or 'Porto, Portugal'), at most "
                         "60 characters, with no instructions or other text. Store just the place.")
    if not valid_until:
        raise ValueError("A travel notice needs the date the customer returns (valid_until, YYYY-MM-DD).")
    if parse_instant(valid_until) < parse_instant(now[:10]):
        raise ValueError("valid_until is in the past.")
    if parse_instant(valid_until) > parse_instant(add_days(now, TRAVEL_NOTICE_MAX_DAYS)):
        raise ValueError(f"A travel notice can cover at most {TRAVEL_NOTICE_MAX_DAYS} days from today.")
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


def render_stepup_status(verified_at: str | None, code_verified_at: str | None, now: str, open_code: dict | None = None) -> str:
    """One line for the system prompt: what this conversation has proved so far, and until when it counts. `open_code` is
    the bank's record of the latest code sent to this customer (world.open_code_status), so a code sent and not yet
    entered is stated from the record: the model neither forgets it nor invents one."""
    def status(label: str, at: str | None) -> str:
        if not at:
            return f"{label}: not done"
        if verification_is_fresh(at, now):
            until = add_minutes(at, VERIFICATION_TTL_MINUTES)
            return f"{label}: done at {at[11:16]} UTC, valid until {until[11:16]} UTC"
        return f"{label}: done at {at[11:16]} UTC but expired (15 minutes); needed again"
    code = status("one-time code", code_verified_at)
    if not code_verified_at and open_code and open_code["status"] == "open":
        code = (f"one-time code: sent at {open_code['sent_at'][11:16]} UTC by {open_code['sent_to']}, not yet entered, usable until "
                f"{open_code['expires_at'][11:16]} UTC; a six-digit number the customer types is taken by the harness before you "
                "see the message (you see [REDACTED ONE-TIME CODE]); call confirm_verification_code() to wait for it or to read the result")
    elif not code_verified_at and open_code and open_code["status"] == "expired":
        code = (f"one-time code: the code sent at {open_code['sent_at'][11:16]} UTC expired at {open_code['expires_at'][11:16]} UTC unused; "
                "send a new one if the customer still needs the change")
    elif not code_verified_at and open_code and open_code["status"] == "failed":
        code = "one-time code: the last code was entered wrongly three times and is dead; send a new one if the account is not locked"
    elif not code_verified_at and open_code and open_code["status"] == "consumed":
        code = (f"one-time code: the code sent at {open_code['sent_at'][11:16]} UTC was entered correctly at {(open_code.get('closed_at') or '')[11:16]} "
                "UTC in another conversation; this one needs its own")
    return status("last four + ZIP", verified_at) + "; " + code


def possession_gate_error(verified_at: str | None, code_verified_at: str | None, now: str, action: str) -> str | None:
    """The second factor for the account-takeover actions: a fresh last-four-plus-ZIP step-up AND a fresh one-time code."""
    error = verification_gate_error(verified_at, now, action)
    if error:
        return error
    if not code_verified_at:
        return (f"{action} also requires a one-time code: call send_verification_code, then confirm_verification_code when the "
                "customer has entered it")
    if not verification_is_fresh(code_verified_at, now):
        return f"the one-time code verification expired ({VERIFICATION_TTL_MINUTES} minutes); send a new code before {action}"
    return None


def render_profile(facts: dict[str, dict], now: str) -> str:
    """The preloaded slice of semantic memory: small, always relevant, re-sent every turn. Values are quoted data.
    The channel line says where follow-ups go when none is set, so the agent never has to guess (it guessed
    "nowhere" in round 3)."""
    lines = []
    for key in FACT_KEYS:
        fact = facts.get(key)
        if not fact or fact_is_expired(fact, now):
            lines.append("- contact_channel: none set, so follow-ups and reminders go by secure message in the Kestrel app (the default)"
                         if key == "contact_channel" else f"- {key}: none on file")
        elif key == "travel_notice":
            lines.append(f"- travel_notice: \"{fact['value']}\" until {fact['valid_until']} (recorded {fact['as_of'][:10]})")
        else:
            lines.append(f"- {key}: {fact['value']} (recorded {fact['as_of'][:10]})")
    return "\n".join(lines)


def typed_in_session(customer_texts: list[str], *values: str, turn_times: list[str] | None = None, now: str | None = None) -> bool:
    """Did the customer type each of these values in this conversation, in the last VERIFICATION_TTL_MINUTES (as a whole
    number, not inside a longer one)? verify_identity accepts only such values: digits remembered from an earlier
    conversation, guessed or filled in never verify anyone, and digits typed longer ago than a step-up lasts do not
    renew it (a step-up proves possession now; the chat's scrollback is visible to whoever holds the phone).
    `turn_times` are the harness instants of the customer's messages, oldest first, aligned from the end."""
    if turn_times and now:
        recent = []
        for text, at in zip(reversed(customer_texts), reversed(turn_times)):
            if (parse_instant(now) - parse_instant(at)).total_seconds() <= VERIFICATION_TTL_MINUTES * 60:
                recent.append(text)
        customer_texts = recent
    said = "\n".join(customer_texts)
    return all(str(v).strip() and re.search(rf"(?<!\d){re.escape(str(v).strip())}(?!\d)", said) for v in values)


def episode_expires_at(now: str) -> str:
    return add_days(now, EPISODE_RETENTION_DAYS)


def episode_is_expired(episode: dict, now: str) -> bool:
    return parse_instant(episode["expires_at"]) <= parse_instant(now)


def transcript_is_expired(first_active_at: str | None, now: str) -> bool:
    """A session expires 30 days after its first turn. One that cannot be dated cannot be kept."""
    return not first_active_at or parse_instant(add_days(first_active_at, TRANSCRIPT_RETENTION_DAYS)) <= parse_instant(now)


def session_is_idle(last_active_at: str | None, now: str) -> bool:
    return bool(last_active_at) and (parse_instant(now) - parse_instant(last_active_at)).total_seconds() >= IDLE_SESSION_MINUTES * 60


def describe_code_entry(entry: dict | None, message: str, proved_at: str | None = None) -> dict:
    """What confirm_verification_code tells the model about the customer's latest message, from what the door made of it
    (world.take_code_entry) and the bank's record of the proof. The typed digits are never in it: the door took them.
    `message` is the customer's message as stored, shown when it was more than an entry so the model can answer it."""
    outcome = (entry or {}).get("outcome")
    wrote = {"customer_wrote": message} if message.strip() else {}  # set when the message resumed a wait: it is not in the history otherwise
    if outcome == "matched" or (proved_at and outcome in (None, "no_code_entered", "no_open_code")):
        return {"verified": True, "valid_for_minutes": VERIFICATION_TTL_MINUTES, **wrote,
                "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, "
                        "without asking them to repeat it"}
    if outcome == "locked":
        return {"verified": False, **wrote, "error": f"verification is locked on this account for {VERIFICATION_LOCK_HOURS} hours after "
                f"{MAX_VERIFICATION_ATTEMPTS} failed attempts: no code can be sent and nothing that needs verification can be done; "
                "the customer must call Kestrel. Do not offer to send a new code"}
    if outcome == "mismatch":
        if entry.get("account_locked"):
            return {"verified": False, **wrote, "error": f"that code is not right, and it was failed attempt {MAX_VERIFICATION_ATTEMPTS} of "
                    f"{MAX_VERIFICATION_ATTEMPTS}: verification is now locked on this account for {VERIFICATION_LOCK_HOURS} hours. No new code "
                    "can be sent and nothing that needs verification can be done; the customer must call Kestrel. Do not offer to send a new code"}
        return {"verified": False, **wrote, "error": "that code is not right", "entries_left_for_this_code": entry["entries_left"]}
    if outcome == "expired":
        return {"verified": False, **wrote, "error": f"the code expired ({CODE_TTL_MINUTES} minutes) and no new code has been sent; tell the "
                "customer and send a new one only if they ask (send_verification_code)"}
    if outcome == "written_unusably":
        return {"verified": False, **wrote, "error": "the customer wrote the code in a form the bank does not take (for example with a comma, "
                "or grouped four and two). It was removed from their message, and that code is now cancelled because it was written into "
                "the conversation. Send a new code (send_verification_code) and ask them to type only its six digits"}
    if outcome == "several_numbers":
        return {"verified": False, **wrote, "note": "the message held more than one six-digit number: none was checked and nothing was "
                "counted. Ask the customer to type only the code, as their whole message"}
    if outcome == "other_conversation":
        return {"verified": False, **wrote, "note": "a code is open for this customer, but it was sent from another conversation: a six-digit "
                "number typed here is removed and not checked. To verify in this conversation, send a new code (send_verification_code)"}
    if outcome == "no_open_code" or entry is None:
        return {"verified": False, **wrote, "error": "no code is open for this customer in this conversation; call send_verification_code first"}
    return {"verified": False, **wrote, "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid "
            f"for its {CODE_TTL_MINUTES} minutes, so call confirm_verification_code again when they are ready, without sending a new one"}
