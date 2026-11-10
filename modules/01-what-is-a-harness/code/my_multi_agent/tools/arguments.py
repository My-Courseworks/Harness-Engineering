"""Turning what the model sends into what the data layer expects."""


def as_int(value: object) -> int | None:
    """The model passes ids as text. Return the integer, or None if it is not one."""
    try:
        return int(str(value).strip())
    except ValueError:
        return None
