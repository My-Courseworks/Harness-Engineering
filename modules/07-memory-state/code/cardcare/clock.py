"""The harness clock.

The harness, not the model, owns time. Every turn is run with an explicit `now`
(an ISO-8601 UTC instant) so the scripted scenario can skip forward to the day a
follow-up is due or a travel notice expires, and the interactive chat
passes the real wall clock instead.
"""

from datetime import datetime, timedelta, timezone


def parse_instant(text: str) -> datetime:
    """Parse an ISO-8601 instant or date into an aware UTC datetime."""
    value = datetime.fromisoformat(text.replace("Z", "+00:00"))
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def format_instant(value: datetime) -> str:
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def add_days(instant: str, days: int) -> str:
    return format_instant(parse_instant(instant) + timedelta(days=days))


def wall_clock_now() -> str:
    return format_instant(datetime.now(timezone.utc))


def add_minutes(instant: str, minutes: int) -> str:
    return format_instant(parse_instant(instant) + timedelta(minutes=minutes))
