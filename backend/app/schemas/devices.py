"""Schemas for device onboarding and management."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import Field

from .common import APIModel, BaseResource, HealthStatus


class DeviceStatus(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    WARNING = "warning"
    MAINTENANCE = "maintenance"
    UNKNOWN = "unknown"


class CredentialType(str, Enum):
    PASSWORD = "password"
    SSH_KEY = "ssh_key"
    API_KEY = "api_key"
    CERTIFICATE = "certificate"


class DeviceCredential(APIModel):
    type: CredentialType
    username: Optional[str] = None
    secret_reference: str
    expires_at: Optional[datetime] = None


class DeviceConnection(APIModel):
    host: str
    port: Optional[int] = None
    protocol: str = "ssh"
    credential: Optional[DeviceCredential] = None


class DeviceCapability(APIModel):
    name: str
    enabled: bool = True
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Device(BaseResource):
    device_type: str
    status: DeviceStatus
    health: HealthStatus = HealthStatus.UNKNOWN
    connection: DeviceConnection
    capabilities: List[DeviceCapability] = Field(default_factory=list)
    last_seen_at: Optional[datetime] = None
    notes: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class DeviceCreate(APIModel):
    name: str
    description: Optional[str] = None
    device_type: str
    connection: DeviceConnection
    capabilities: List[DeviceCapability] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)


class DeviceUpdate(APIModel):
    name: Optional[str] = None
    description: Optional[str] = None
    device_type: Optional[str] = None
    status: Optional[DeviceStatus] = None
    health: Optional[HealthStatus] = None
    connection: Optional[DeviceConnection] = None
    capabilities: Optional[List[DeviceCapability]] = None
    tags: Optional[List[str]] = None
    notes: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


__all__ = [
    "Device",
    "DeviceCreate",
    "DeviceUpdate",
    "DeviceConnection",
    "DeviceCredential",
    "DeviceCapability",
    "DeviceStatus",
    "CredentialType",
]
