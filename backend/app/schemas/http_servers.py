"""Schemas for managed Flask/HTTP servers."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import Field

from .common import APIModel, BaseResource, HealthStatus


class HTTPServerStatus(str, Enum):
    STOPPED = "stopped"
    RUNNING = "running"
    STARTING = "starting"
    ERROR = "error"


class RouteAuthType(str, Enum):
    INHERIT = "inherit"
    NONE = "none"
    API_KEY = "api_key"
    BASIC = "basic"
    BEARER = "bearer"


class HTTPRoute(APIModel):
    path: str
    methods: List[str] = Field(default_factory=lambda: ["GET"])
    script_id: Optional[str] = None
    description: Optional[str] = None
    auth_type: RouteAuthType = RouteAuthType.INHERIT
    cors_enabled: bool = False


class TLSConfig(APIModel):
    enabled: bool = False
    certificate_reference: Optional[str] = None
    key_reference: Optional[str] = None
    auto_renew: bool = False


class MiddlewareConfig(APIModel):
    name: str
    enabled: bool = True
    settings: Dict[str, str] = Field(default_factory=dict)


class HTTPServer(BaseResource):
    host: str = "0.0.0.0"
    port: int = 5000
    status: HTTPServerStatus = HTTPServerStatus.STOPPED
    tls: TLSConfig = Field(default_factory=TLSConfig)
    routes: List[HTTPRoute] = Field(default_factory=list)
    middlewares: List[MiddlewareConfig] = Field(default_factory=list)
    health: HealthStatus = HealthStatus.UNKNOWN
    last_started_at: Optional[datetime] = None
    last_stopped_at: Optional[datetime] = None


class HTTPServerCreate(APIModel):
    name: str
    description: Optional[str] = None
    host: str = "0.0.0.0"
    port: int = 5000
    tls: TLSConfig = Field(default_factory=TLSConfig)
    routes: List[HTTPRoute] = Field(default_factory=list)
    middlewares: List[MiddlewareConfig] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)


class HTTPServerUpdate(APIModel):
    name: Optional[str] = None
    description: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    tls: Optional[TLSConfig] = None
    routes: Optional[List[HTTPRoute]] = None
    middlewares: Optional[List[MiddlewareConfig]] = None
    tags: Optional[List[str]] = None
    status: Optional[HTTPServerStatus] = None
    health: Optional[HealthStatus] = None
    last_started_at: Optional[datetime] = None
    last_stopped_at: Optional[datetime] = None


__all__ = [
    "HTTPServer",
    "HTTPServerCreate",
    "HTTPServerUpdate",
    "HTTPServerStatus",
    "HTTPRoute",
    "RouteAuthType",
    "MiddlewareConfig",
    "TLSConfig",
]
