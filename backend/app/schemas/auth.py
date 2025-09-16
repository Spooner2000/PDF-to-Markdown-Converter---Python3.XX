"""Authentication and RBAC schemas."""

from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import Field

from .common import APIModel, Role


class User(APIModel):
    id: str
    username: str
    full_name: str
    roles: List[Role]
    active: bool = True


class UserCreate(APIModel):
    username: str
    password: str
    full_name: str
    roles: List[Role]


class UserPublic(APIModel):
    id: str
    username: str
    full_name: str
    roles: List[Role]


class Session(APIModel):
    token: str
    user_id: str
    issued_at: datetime
    expires_at: datetime
    last_seen_at: datetime


class LoginRequest(APIModel):
    username: str
    password: str


class LoginResponse(APIModel):
    token: str
    user: UserPublic
    expires_at: datetime


class RefreshResponse(APIModel):
    token: str
    expires_at: datetime


class TokenPayload(APIModel):
    sub: str
    exp: datetime
    roles: List[Role]
    session_id: str = Field(..., alias="sid")


__all__ = [
    "User",
    "UserCreate",
    "UserPublic",
    "Session",
    "LoginRequest",
    "LoginResponse",
    "RefreshResponse",
    "TokenPayload",
]
