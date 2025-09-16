"""HTTP server management endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Response, status

from ...auth import require_roles
from ...schemas.auth import User
from ...schemas.common import LogLevel, Role, Severity
from ...schemas.http_servers import HTTPServer, HTTPServerCreate, HTTPServerStatus, HTTPServerUpdate
from ...schemas.observability import LogEntry, NotificationCreate
from ...utils.datetime import utcnow
from ...utils.identifiers import generate_id
from ..deps import get_app_state

router = APIRouter()


@router.get("/", response_model=list[HTTPServer])
async def list_http_servers(state=Depends(get_app_state)) -> list[HTTPServer]:
    return await state.list_http_servers()


@router.post("/", response_model=HTTPServer, status_code=status.HTTP_201_CREATED)
async def create_http_server(
    payload: HTTPServerCreate,
    user: User = Depends(require_roles(Role.ADMINISTRATOR, Role.DEVELOPER)),
    state=Depends(get_app_state),
) -> HTTPServer:
    return await state.create_http_server(payload, user)


@router.get("/{server_id}", response_model=HTTPServer)
async def get_http_server(server_id: str, state=Depends(get_app_state)) -> HTTPServer:
    return await state.get_http_server(server_id)


@router.put("/{server_id}", response_model=HTTPServer)
async def update_http_server(
    server_id: str,
    payload: HTTPServerUpdate,
    user: User = Depends(require_roles(Role.ADMINISTRATOR, Role.DEVELOPER)),
    state=Depends(get_app_state),
) -> HTTPServer:
    return await state.update_http_server(server_id, payload, user)


@router.delete("/{server_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_http_server(
    server_id: str,
    user: User = Depends(require_roles(Role.ADMINISTRATOR)),
    state=Depends(get_app_state),
) -> Response:
    await state.delete_http_server(server_id, actor=user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{server_id}/start", response_model=HTTPServer)
async def start_http_server(
    server_id: str,
    user: User = Depends(require_roles(Role.ADMINISTRATOR, Role.DEVELOPER, Role.OPERATOR)),
    state=Depends(get_app_state),
) -> HTTPServer:
    server = await state.update_http_server(
        server_id,
        HTTPServerUpdate(status=HTTPServerStatus.RUNNING, last_started_at=utcnow()),
        user,
    )
    await state.record_log(
        LogEntry(
            id=generate_id(),
            category="http_server",
            level=LogLevel.INFO,
            message=f"Server {server.name} started by {user.username}",
            timestamp=utcnow(),
            source="api",
        )
    )
    return server


@router.post("/{server_id}/stop", response_model=HTTPServer)
async def stop_http_server(
    server_id: str,
    user: User = Depends(require_roles(Role.ADMINISTRATOR, Role.DEVELOPER, Role.OPERATOR)),
    state=Depends(get_app_state),
) -> HTTPServer:
    server = await state.update_http_server(
        server_id,
        HTTPServerUpdate(status=HTTPServerStatus.STOPPED, last_stopped_at=utcnow()),
        user,
    )
    await state.create_notification(
        NotificationCreate(
            title="Server gestoppt",
            message=f"{server.name} wurde gestoppt.",
            severity=Severity.WARNING,
            category="http_server",
        ),
        actor=user.username,
    )
    return server


__all__ = ["router"]
