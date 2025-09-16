"""Endpoints for routine orchestration."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Response, status

from ...auth import require_roles
from ...schemas.common import LogLevel, Role, Severity
from ...schemas.observability import LogEntry, NotificationCreate
from ...schemas.routines import Routine, RoutineCreate, RoutineStatus, RoutineUpdate
from ...schemas.auth import User
from ...utils.datetime import utcnow
from ...utils.identifiers import generate_id
from ..deps import get_app_state

router = APIRouter()


@router.get("/", response_model=list[Routine])
async def list_routines(state=Depends(get_app_state)) -> list[Routine]:
    return await state.list_routines()


@router.post("/", response_model=Routine, status_code=status.HTTP_201_CREATED)
async def create_routine(
    payload: RoutineCreate,
    user: User = Depends(require_roles(Role.ADMINISTRATOR, Role.OPERATOR)),
    state=Depends(get_app_state),
) -> Routine:
    return await state.create_routine(payload, user)


@router.get("/{routine_id}", response_model=Routine)
async def get_routine(routine_id: str, state=Depends(get_app_state)) -> Routine:
    return await state.get_routine(routine_id)


@router.put("/{routine_id}", response_model=Routine)
async def update_routine(
    routine_id: str,
    payload: RoutineUpdate,
    user: User = Depends(require_roles(Role.ADMINISTRATOR, Role.OPERATOR)),
    state=Depends(get_app_state),
) -> Routine:
    return await state.update_routine(routine_id, payload, user)


@router.delete("/{routine_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_routine(
    routine_id: str,
    user: User = Depends(require_roles(Role.ADMINISTRATOR)),
    state=Depends(get_app_state),
) -> Response:
    await state.delete_routine(routine_id, actor=user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{routine_id}/run", response_model=Routine)
async def run_routine(
    routine_id: str,
    user: User = Depends(require_roles(Role.ADMINISTRATOR, Role.OPERATOR)),
    state=Depends(get_app_state),
) -> Routine:
    routine = await state.get_routine(routine_id)
    await state.record_log(
        LogEntry(
            id=generate_id(),
            category="routine",
            level=LogLevel.INFO,
            message=f"Routine {routine.name} triggered by {user.username}",
            timestamp=utcnow(),
            source="api",
        )
    )
    await state.create_notification(
        NotificationCreate(
            title="Routine gestartet",
            message=f"{routine.name} wurde durch {user.username} gestartet.",
            severity=Severity.INFO,
            category="routine",
        ),
        actor=user.username,
    )
    return routine


@router.post("/{routine_id}/status", response_model=Routine)
async def set_routine_status(
    routine_id: str,
    status_value: RoutineStatus,
    user: User = Depends(require_roles(Role.ADMINISTRATOR, Role.OPERATOR)),
    state=Depends(get_app_state),
) -> Routine:
    update = RoutineUpdate(status=status_value)
    return await state.update_routine(routine_id, update, user)


__all__ = ["router"]
