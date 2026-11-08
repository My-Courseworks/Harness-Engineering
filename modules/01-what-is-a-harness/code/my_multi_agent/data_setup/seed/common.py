"""Small, pure helpers shared by the seeders (no database access, no randomness)."""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone


def iso_date(value: date) -> str:
    return value.isoformat()


def iso_datetime(value: datetime) -> str:
    """UTC, minute precision, so string comparison matches chronological order."""
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)      # naive seed values are UTC by definition
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M") + "Z"


def at_hour(day: date, hour: int, minute: int = 0) -> datetime:
    return datetime(day.year, day.month, day.day, hour, minute)


def next_workdays(start: date, count: int) -> list[date]:
    """The first ``count`` Monday-to-Friday days strictly after ``start``."""
    days: list[date] = []
    current = start
    while len(days) < count:
        current += timedelta(days=1)
        if current.weekday() < 5:
            days.append(current)
    return days


def round_to(value: float, step: float) -> float:
    return round(value / step) * step
