"""Device management endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Response, status

from ...auth import require_roles
from ...schemas.auth import User
from ...schemas.common import LogLevel, Role, Severity
from ...schemas.devices import Device, DeviceCreate, DeviceStatus, DeviceUpdate
from ...schemas.observability import LogEntry, NotificationCreate
from ...utils.datetime import utcnow
from ...utils.identifiers import generate_id
from ..deps import get_app_state

router = APIRouter()


@router.get("/", response_model=list[Device])
async def list_devices(state=Depends(get_app_state)) -> list[Device]:
    return await state.list_devices()


@router.post("/", response_model=Device, status_code=status.HTTP_201_CREATED)
async def create_device(
    payload: DeviceCreate,
    user: User = Depends(require_roles(Role.ADMINISTRATOR, Role.OPERATOR)),
    state=Depends(get_app_state),
) -> Device:
    return await state.create_device(payload, user)


@router.get("/{device_id}", response_model=Device)
async def get_device(device_id: str, state=Depends(get_app_state)) -> Device:
    return await state.get_device(device_id)


@router.put("/{device_id}", response_model=Device)
async def update_device(
    device_id: str,
    payload: DeviceUpdate,
    user: User = Depends(require_roles(Role.ADMINISTRATOR, Role.OPERATOR)),
    state=Depends(get_app_state),
) -> Device:
    return await state.update_device(device_id, payload, user)


@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device(
    device_id: str,
    user: User = Depends(require_roles(Role.ADMINISTRATOR)),
    state=Depends(get_app_state),
) -> Response:
    await state.delete_device(device_id, actor=user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{device_id}/check", response_model=Device)
async def check_device(
    device_id: str,
    user: User = Depends(require_roles(Role.ADMINISTRATOR, Role.OPERATOR)),
    state=Depends(get_app_state),
) -> Device:
    device = await state.get_device(device_id)
    await state.record_log(
        LogEntry(
            id=generate_id(),
            category="device",
            level=LogLevel.INFO,
            message=f"Device {device.name} health check triggered by {user.username}",
            timestamp=utcnow(),
            source="api",
        )
    )
    await state.create_notification(
        NotificationCreate(
            title="Geräteprüfung",
            message=f"{device.name} wurde überprüft.",
            severity=Severity.INFO,
            category="device",
        ),
        actor=user.username,
    )
    return device


@router.post("/{device_id}/status", response_model=Device)
async def set_device_status(
    device_id: str,
    status_value: DeviceStatus,
    user: User = Depends(require_roles(Role.ADMINISTRATOR, Role.OPERATOR)),
    state=Depends(get_app_state),
) -> Device:
    update = DeviceUpdate(status=status_value)
    return await state.update_device(device_id, update, user)


__all__ = ["router"]
