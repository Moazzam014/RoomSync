
from datetime import UTC, datetime


def utcnow_naive() -> datetime:
    """
    Return the current UTC time as a naive datetime.

    Use this only for existing database columns configured
    with timezone=False.
    """
    return datetime.now(UTC).replace(tzinfo=None)
