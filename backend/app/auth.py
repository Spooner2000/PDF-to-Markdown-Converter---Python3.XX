"""Authentication helpers and RBAC enforcement."""

from __future__ import annotations

import asyncio
import hashlib
import secrets
from datetime import timedelta
from typing import List, Optional, Sequence

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .config import settings
from .events import EventBus
from .schemas.auth import LoginRequest, LoginResponse, Session, User, UserCreate, UserPublic
from .schemas.common import Role
from .utils.datetime import utcnow
from .utils.identifiers import generate_id


class AuthService:
    """Very small in-memory auth subsystem for the prototype."""

    def __init__(self, event_bus: EventBus) -> None:
        self._event_bus = event_bus
        self._users: dict[str, tuple[User, str]] = {}
        self._usernames: dict[str, str] = {}
        self._sessions: dict[str, Session] = {}
        self._lock = asyncio.Lock()
        self._seed_default_users()

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def _seed_default_users(self) -> None:
        defaults = [
            ("admin", "Administrator", "admin123", [Role.ADMINISTRATOR, Role.OPERATOR, Role.DEVELOPER, Role.VIEWER]),
            ("operator", "Operations", "operator123", [Role.OPERATOR, Role.VIEWER]),
            ("developer", "Developer", "dev123", [Role.DEVELOPER, Role.VIEWER]),
            ("viewer", "Read Only", "viewer123", [Role.VIEWER]),
        ]
        for username, full_name, password, roles in defaults:
            user = User(id=generate_id(), username=username, full_name=full_name, roles=roles)
            password_hash = self._hash_password(password)
            self._users[user.id] = (user, password_hash)
            self._usernames[username] = user.id

    async def list_users(self) -> List[UserPublic]:
        async with self._lock:
            return [self._to_public(user) for user, _ in self._users.values()]

    async def create_user(self, payload: UserCreate, actor: User) -> UserPublic:
        async with self._lock:
            if payload.username in self._usernames:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
            user = User(id=generate_id(), username=payload.username, full_name=payload.full_name, roles=payload.roles)
            self._users[user.id] = (user, self._hash_password(payload.password))
            self._usernames[user.username] = user.id
        await self._event_bus.publish(
            "user.created",
            {"id": user.id, "username": user.username, "roles": [role.value for role in user.roles], "actor": actor.username},
        )
        return self._to_public(user)

    async def authenticate(self, payload: LoginRequest) -> LoginResponse:
        async with self._lock:
            user_id = self._usernames.get(payload.username)
            if not user_id:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
            user, password_hash = self._users[user_id]
            if self._hash_password(payload.password) != password_hash:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
            if not user.active:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User disabled")
            now = utcnow()
            expires = now + timedelta(minutes=settings.access_token_ttl_minutes)
            token = secrets.token_urlsafe(32)
            session = Session(token=token, user_id=user.id, issued_at=now, expires_at=expires, last_seen_at=now)
            self._sessions[token] = session
        await self._event_bus.publish("auth.login", {"user": user.username, "session": token})
        return LoginResponse(token=token, user=self._to_public(user), expires_at=session.expires_at)

    async def logout(self, token: str, actor: Optional[User] = None) -> None:
        async with self._lock:
            session = self._sessions.pop(token, None)
        if session:
            username = None
            async with self._lock:
                user_entry = self._users.get(session.user_id)
                if user_entry:
                    username = user_entry[0].username
            await self._event_bus.publish("auth.logout", {"session": token, "user": username, "actor": actor.username if actor else None})

    async def get_user_for_token(self, token: str) -> Optional[User]:
        async with self._lock:
            session = self._sessions.get(token)
            if not session:
                return None
            now = utcnow()
            if session.expires_at < now:
                self._sessions.pop(token, None)
                return None
            session = session.model_copy(update={"last_seen_at": now})
            self._sessions[token] = session
            user_entry = self._users.get(session.user_id)
            if not user_entry:
                return None
            return user_entry[0]

    async def require_roles(self, user: User, allowed_roles: Sequence[Role]) -> None:
        if not allowed_roles:
            return
        if not any(role in user.roles for role in allowed_roles):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient privileges")

    async def list_sessions(self) -> List[Session]:
        async with self._lock:
            return list(self._sessions.values())

    def _to_public(self, user: User) -> UserPublic:
        return UserPublic(id=user.id, username=user.username, full_name=user.full_name, roles=user.roles)


bearer_scheme = HTTPBearer(auto_error=False)


def get_auth_service(request: Request) -> AuthService:
    return request.app.state.app_state.auth


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    auth: AuthService = Depends(get_auth_service),
) -> User:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing credentials")
    user = await auth.get_user_for_token(credentials.credentials)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired credentials")
    return user


def require_roles(*roles: Role):
    async def dependency(user: User = Depends(get_current_user), auth: AuthService = Depends(get_auth_service)) -> User:
        await auth.require_roles(user, roles)
        return user

    return dependency


__all__ = [
    "AuthService",
    "get_auth_service",
    "get_current_user",
    "require_roles",
]
