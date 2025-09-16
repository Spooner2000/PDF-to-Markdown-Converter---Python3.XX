"""Schemas for Python virtual environment management."""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

from pydantic import Field

from .common import APIModel, BaseResource, HealthStatus


class PackageInfo(APIModel):
    name: str
    version: str
    summary: Optional[str] = None
    homepage: Optional[str] = None


class VirtualEnvironment(BaseResource):
    python_version: str
    location: str
    status: HealthStatus = HealthStatus.UNKNOWN
    packages: List[PackageInfo] = Field(default_factory=list)
    last_check_at: Optional[datetime] = None
    size_bytes: Optional[int] = None


class VirtualEnvironmentCreate(APIModel):
    name: str
    description: Optional[str] = None
    python_version: str = "3.12"
    packages: List[PackageInfo] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)


class VirtualEnvironmentUpdate(APIModel):
    description: Optional[str] = None
    packages: Optional[List[PackageInfo]] = None
    status: Optional[HealthStatus] = None
    tags: Optional[List[str]] = None
    size_bytes: Optional[int] = None
    last_check_at: Optional[datetime] = None


__all__ = [
    "VirtualEnvironment",
    "VirtualEnvironmentCreate",
    "VirtualEnvironmentUpdate",
    "PackageInfo",
]
