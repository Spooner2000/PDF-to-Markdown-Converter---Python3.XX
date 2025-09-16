"""Authentication endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import HTTPAuthorizationCredentials

from ...auth import bearer_scheme, get_current_user, require_roles
from ...schemas.auth import LoginRequest, LoginResponse, Session, User, UserCreate, UserPublic
from ...schemas.common import Role
from ..deps import get_app_state

router = APIRouter()


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(payload: LoginRequest, state=Depends(get_app_state)) -> LoginResponse:
    return await state.auth.authenticate(payload)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    user: User = Depends(get_current_user),
    state=Depends(get_app_state),
) -> Response:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing credentials")
    await state.auth.logout(credentials.credentials, actor=user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/me", response_model=UserPublic)
async def me(user: User = Depends(get_current_user)) -> UserPublic:
    return UserPublic(id=user.id, username=user.username, full_name=user.full_name, roles=user.roles)


@router.get("/users", response_model=list[UserPublic])
async def list_users(
    _: User = Depends(require_roles(Role.ADMINISTRATOR)),
    state=Depends(get_app_state),
) -> list[UserPublic]:
    return await state.auth.list_users()


@router.post("/users", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreate,
    actor: User = Depends(require_roles(Role.ADMINISTRATOR)),
    state=Depends(get_app_state),
) -> UserPublic:
    return await state.auth.create_user(payload, actor=actor)


@router.get("/sessions", response_model=list[Session])
async def list_sessions(
    _: User = Depends(require_roles(Role.ADMINISTRATOR)),
    state=Depends(get_app_state),
):
    return await state.auth.list_sessions()


__all__ = ["router"]
