"""Common schema components used by multiple domains."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class APIModel(BaseModel):
    """Base model with sane defaults for API responses."""

    model_config = ConfigDict(use_enum_values=True, populate_by_name=True)


class Role(str, Enum):
    ADMINISTRATOR = "administrator"
    OPERATOR = "operator"
    DEVELOPER = "developer"
    VIEWER = "viewer"


class Severity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class LogLevel(str, Enum):
    TRACE = "trace"
    DEBUG = "debug"
    INFO = "info"
    WARN = "warn"
    ERROR = "error"
    FATAL = "fatal"


class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


class AuditTrail(APIModel):
    """Metadata about who created or modified an entity."""

    created_at: datetime
    updated_at: datetime
    created_by: str
    updated_by: str


class TaggedEntity(APIModel):
    """Mixin for objects that support tagging."""

    tags: List[str] = Field(default_factory=list)


class BaseResource(TaggedEntity):
    """Base resource model with identifier and audit fields."""

    id: str
    name: str
    description: Optional[str] = None
    audit: AuditTrail


class Pagination(APIModel):
    """Generic pagination metadata."""

    total: int
    limit: int
    offset: int


class PaginatedResult(APIModel):
    """Wrap paginated responses together with metadata."""

    data: List[Dict[str, object]]
    pagination: Pagination


__all__ = [
    "APIModel",
    "Role",
    "Severity",
    "LogLevel",
    "HealthStatus",
    "AuditTrail",
    "TaggedEntity",
    "BaseResource",
    "Pagination",
    "PaginatedResult",
]
