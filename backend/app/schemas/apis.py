"""Schemas for external API management."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import Field

from .common import APIModel, BaseResource, HealthStatus


class AuthMode(str, Enum):
    NONE = "none"
    API_KEY = "api_key"
    BASIC = "basic"
    BEARER = "bearer"
    MTLS = "mtls"


class HTTPMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class APIAuthConfig(APIModel):
    mode: AuthMode
    header_name: Optional[str] = None
    api_key: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    token_url: Optional[str] = None
    scopes: List[str] = Field(default_factory=list)
    certificate_reference: Optional[str] = None


class APIEndpoint(APIModel):
    name: str
    method: HTTPMethod
    path: str
    description: Optional[str] = None
    sample_request: Optional[Dict[str, Any]] = None
    sample_response: Optional[Dict[str, Any]] = None
    timeout_seconds: float = 30.0
    retries: int = 0
    rate_limit_per_minute: Optional[int] = None


class APIEnvironment(APIModel):
    name: str
    base_url: str
    headers: Dict[str, str] = Field(default_factory=dict)
    verify_tls: bool = True


class APIMonitoring(APIModel):
    success_rate: float = 100.0
    last_checked_at: Optional[datetime] = None
    average_latency_ms: Optional[float] = None
    p95_latency_ms: Optional[float] = None
    error_rate: float = 0.0


class APIService(BaseResource):
    environments: List[APIEnvironment]
    default_environment: str
    auth: APIAuthConfig
    endpoints: List[APIEndpoint] = Field(default_factory=list)
    monitoring: APIMonitoring = Field(default_factory=APIMonitoring)
    health: HealthStatus = HealthStatus.UNKNOWN


class APIServiceCreate(APIModel):
    name: str
    description: Optional[str] = None
    environments: List[APIEnvironment]
    default_environment: str
    auth: APIAuthConfig
    endpoints: List[APIEndpoint] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)


class APIServiceUpdate(APIModel):
    name: Optional[str] = None
    description: Optional[str] = None
    environments: Optional[List[APIEnvironment]] = None
    default_environment: Optional[str] = None
    auth: Optional[APIAuthConfig] = None
    endpoints: Optional[List[APIEndpoint]] = None
    tags: Optional[List[str]] = None
    health: Optional[HealthStatus] = None
    monitoring: Optional[APIMonitoring] = None


__all__ = [
    "APIService",
    "APIServiceCreate",
    "APIServiceUpdate",
    "APIAuthConfig",
    "APIEndpoint",
    "APIEnvironment",
    "APIMonitoring",
    "AuthMode",
    "HTTPMethod",
]
