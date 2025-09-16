"""Virtual environment management endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Response, status

from ...auth import require_roles
from ...schemas.auth import User
from ...schemas.common import LogLevel, Role
from ...schemas.observability import LogEntry
from ...schemas.venv import VirtualEnvironment, VirtualEnvironmentCreate, VirtualEnvironmentUpdate
from ...utils.datetime import utcnow
from ...utils.identifiers import generate_id
from ..deps import get_app_state

router = APIRouter()


@router.get("/", response_model=list[VirtualEnvironment])
async def list_virtual_envs(state=Depends(get_app_state)) -> list[VirtualEnvironment]:
    return await state.list_virtual_environments()


@router.post("/", response_model=VirtualEnvironment, status_code=status.HTTP_201_CREATED)
async def create_virtual_env(
    payload: VirtualEnvironmentCreate,
    user: User = Depends(require_roles(Role.ADMINISTRATOR, Role.DEVELOPER)),
    state=Depends(get_app_state),
) -> VirtualEnvironment:
    return await state.create_virtual_environment(payload, user)


@router.get("/{venv_id}", response_model=VirtualEnvironment)
async def get_virtual_env(venv_id: str, state=Depends(get_app_state)) -> VirtualEnvironment:
    return await state.get_virtual_environment(venv_id)


@router.put("/{venv_id}", response_model=VirtualEnvironment)
async def update_virtual_env(
    venv_id: str,
    payload: VirtualEnvironmentUpdate,
    user: User = Depends(require_roles(Role.ADMINISTRATOR, Role.DEVELOPER)),
    state=Depends(get_app_state),
) -> VirtualEnvironment:
    return await state.update_virtual_environment(venv_id, payload, user)


@router.delete("/{venv_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_virtual_env(
    venv_id: str,
    user: User = Depends(require_roles(Role.ADMINISTRATOR)),
    state=Depends(get_app_state),
) -> Response:
    await state.delete_virtual_environment(venv_id, actor=user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{venv_id}/refresh", response_model=VirtualEnvironment)
async def refresh_virtual_env(
    venv_id: str,
    user: User = Depends(require_roles(Role.ADMINISTRATOR, Role.DEVELOPER)),
    state=Depends(get_app_state),
) -> VirtualEnvironment:
    venv = await state.update_virtual_environment(
        venv_id,
        VirtualEnvironmentUpdate(last_check_at=utcnow()),
        user,
    )
    await state.record_log(
        LogEntry(
            id=generate_id(),
            category="venv",
            level=LogLevel.INFO,
            message=f"Virtuelle Umgebung {venv.name} aktualisiert",
            timestamp=utcnow(),
            source="api",
        )
    )
    return venv


__all__ = ["router"]
