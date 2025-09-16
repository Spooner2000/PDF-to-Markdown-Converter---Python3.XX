"""Datetime helpers used across the backend."""

from datetime import datetime, timezone


def utcnow() -> datetime:
    """Return a timezone aware timestamp in UTC."""

    return datetime.now(timezone.utc)


__all__ = ["utcnow"]
