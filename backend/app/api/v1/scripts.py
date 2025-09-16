"""Script lifecycle endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Response, status

from ...auth import require_roles
from ...schemas.auth import User
from ...schemas.common import LogLevel, Role, Severity
from ...schemas.observability import LogEntry, NotificationCreate
from ...schemas.scripts import Script, ScriptCreate, ScriptUpdate
from ...utils.datetime import utcnow
from ...utils.identifiers import generate_id
from ..deps import get_app_state

router = APIRouter()


@router.get("/", response_model=list[Script])
async def list_scripts(state=Depends(get_app_state)) -> list[Script]:
    return await state.list_scripts()


@router.post("/", response_model=Script, status_code=status.HTTP_201_CREATED)
async def create_script(
    payload: ScriptCreate,
    user: User = Depends(require_roles(Role.ADMINISTRATOR, Role.DEVELOPER)),
    state=Depends(get_app_state),
) -> Script:
    return await state.create_script(payload, user)


@router.get("/{script_id}", response_model=Script)
async def get_script(script_id: str, state=Depends(get_app_state)) -> Script:
    return await state.get_script(script_id)


@router.put("/{script_id}", response_model=Script)
async def update_script(
    script_id: str,
    payload: ScriptUpdate,
    user: User = Depends(require_roles(Role.ADMINISTRATOR, Role.DEVELOPER)),
    state=Depends(get_app_state),
) -> Script:
    return await state.update_script(script_id, payload, user)


@router.delete("/{script_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_script(
    script_id: str,
    user: User = Depends(require_roles(Role.ADMINISTRATOR)),
    state=Depends(get_app_state),
) -> Response:
    await state.delete_script(script_id, actor=user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{script_id}/validate", response_model=Script)
async def validate_script(
    script_id: str,
    user: User = Depends(require_roles(Role.ADMINISTRATOR, Role.DEVELOPER)),
    state=Depends(get_app_state),
) -> Script:
    script = await state.get_script(script_id)
    update = ScriptUpdate(validated=True)
    validated = await state.update_script(script_id, update, user)
    await state.create_notification(
        NotificationCreate(
            title="Script validiert",
            message=f"{script.name} wurde von {user.username} geprüft.",
            severity=Severity.INFO,
            category="scripts",
        ),
        actor=user.username,
    )
    return validated


@router.post("/{script_id}/run", response_model=Script)
async def run_script(
    script_id: str,
    user: User = Depends(require_roles(Role.ADMINISTRATOR, Role.DEVELOPER, Role.OPERATOR)),
    state=Depends(get_app_state),
) -> Script:
    script = await state.get_script(script_id)
    await state.record_log(
        LogEntry(
            id=generate_id(),
            category="script",
            level=LogLevel.INFO,
            message=f"Script {script.name} executed by {user.username}",
            timestamp=utcnow(),
            source="api",
        )
    )
    return script


__all__ = ["router"]
