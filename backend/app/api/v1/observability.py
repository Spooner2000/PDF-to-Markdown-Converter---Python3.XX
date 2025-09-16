"""Observability endpoints for logs, metrics and notifications."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status

from ...auth import get_current_user, require_roles
from ...schemas.auth import User
from ...schemas.common import LogLevel, Role
from ...schemas.observability import LogEntry, MetricSample, Notification, NotificationCreate
from ..deps import get_app_state

router = APIRouter()


@router.get("/logs", response_model=list[LogEntry])
async def list_logs(
    category: str | None = None,
    level: LogLevel | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=500),
    state=Depends(get_app_state),
) -> list[LogEntry]:
    level_value = level.value if isinstance(level, LogLevel) else level
    return await state.list_logs(category=category, level=level_value, limit=limit)


@router.get("/metrics", response_model=list[MetricSample])
async def list_metrics(
    name: str | None = None,
    limit: int = Query(default=100, ge=1, le=500),
    state=Depends(get_app_state),
) -> list[MetricSample]:
    return await state.list_metrics(name=name, limit=limit)


@router.get("/notifications", response_model=list[Notification])
async def list_notifications(state=Depends(get_app_state)) -> list[Notification]:
    return await state.list_notifications()


@router.post("/notifications", response_model=Notification, status_code=status.HTTP_201_CREATED)
async def create_notification(
    payload: NotificationCreate,
    user: User = Depends(require_roles(Role.ADMINISTRATOR, Role.OPERATOR)),
    state=Depends(get_app_state),
) -> Notification:
    return await state.create_notification(payload, actor=user.username)


@router.post("/notifications/{notification_id}/read", response_model=Notification)
async def mark_notification_read(
    notification_id: str,
    user: User = Depends(get_current_user),
    state=Depends(get_app_state),
) -> Notification:
    return await state.mark_notification_read(notification_id, actor=user)


__all__ = ["router"]
