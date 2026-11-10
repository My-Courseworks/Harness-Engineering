"""
Time helpers: stored timestamps are UTC text; people read local time.
"""

from datetime import datetime, tzinfo

LOCAL_TZ = datetime.now().astimezone().tzinfo

def parse_utc(value: str) -> datetime:
    """
    """
    return datetime.fromisoformat(value)

def format_local(value: str, zone: tzinfo) -> str:
    """
    """
    return parse_utc(value=value).astimezone(zone).strftime("%Y-%m-%d %H:%M %Z")

def to_local(value: str) -> str:
    """
    Convert all times to local timezone
    """
    return format_local(value, LOCAL_TZ)

def now_local(date: bool = False) -> str:
    """Current wall-clock time in the local zone."""
    if date:
        return datetime.now().astimezone(LOCAL_TZ).strftime("%Y-%m-%d")
    return datetime.now().astimezone(LOCAL_TZ).strftime("%Y-%m-%d %H:%M %Z")
