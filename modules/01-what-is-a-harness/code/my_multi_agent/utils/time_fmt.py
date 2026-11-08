"""
Convert time to given format
"""

from datetime import datetime, tzinfo

def parse_utc(value: str) -> datetime:
    """
    """
    return datetime.fromisoformat(value)

def format_local(value: str, zone: tzinfo) -> str:
    """
    """
    return parse_utc(value=value).astimezone(zone).strftime("%Y-%m-%d %H:%M %Z")
