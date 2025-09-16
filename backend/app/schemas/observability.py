"""Schemas for logs, metrics and notifications."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import Field

from .common import APIModel, LogLevel, Severity


class MetricUnit(str, Enum):
    PERCENT = "%"
    BYTES = "bytes"
    MEGABYTES = "MB"
    MILLISECONDS = "ms"
    SECONDS = "s"
    COUNT = "count"


class MetricSample(APIModel):
    id: str
    name: str
    value: float
    unit: MetricUnit
    timestamp: datetime
    tags: Dict[str, str] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class LogEntry(APIModel):
    id: str
    category: str
    level: LogLevel
    message: str
    timestamp: datetime
    correlation_id: Optional[str] = None
    source: Optional[str] = None
    context: Dict[str, Any] = Field(default_factory=dict)


class Notification(APIModel):
    id: str
    title: str
    message: str
    severity: Severity
    created_at: datetime
    read_at: Optional[datetime] = None
    category: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class NotificationCreate(APIModel):
    title: str
    message: str
    severity: Severity = Severity.INFO
    category: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


__all__ = [
    "MetricSample",
    "MetricUnit",
    "LogEntry",
    "Notification",
    "NotificationCreate",
]
