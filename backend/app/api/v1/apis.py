"""API management endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Response, status

from ...auth import require_roles
from ...schemas.apis import APIService, APIServiceCreate, APIServiceUpdate
from ...schemas.auth import User
from ...schemas.common import LogLevel, Role, Severity
from ...schemas.observability import LogEntry, NotificationCreate
from ...utils.datetime import utcnow
from ...utils.identifiers import generate_id
from ..deps import get_app_state

router = APIRouter()


@router.get("/", response_model=list[APIService])
async def list_api_services(state=Depends(get_app_state)) -> list[APIService]:
    return await state.list_api_services()


@router.post("/", response_model=APIService, status_code=status.HTTP_201_CREATED)
async def create_api_service(
    payload: APIServiceCreate,
    user: User = Depends(require_roles(Role.ADMINISTRATOR, Role.DEVELOPER)),
    state=Depends(get_app_state),
) -> APIService:
    return await state.create_api_service(payload, user)


@router.get("/{service_id}", response_model=APIService)
async def get_api_service(service_id: str, state=Depends(get_app_state)) -> APIService:
    return await state.get_api_service(service_id)


@router.put("/{service_id}", response_model=APIService)
async def update_api_service(
    service_id: str,
    payload: APIServiceUpdate,
    user: User = Depends(require_roles(Role.ADMINISTRATOR, Role.DEVELOPER)),
    state=Depends(get_app_state),
) -> APIService:
    return await state.update_api_service(service_id, payload, user)


@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_api_service(
    service_id: str,
    user: User = Depends(require_roles(Role.ADMINISTRATOR)),
    state=Depends(get_app_state),
) -> Response:
    await state.delete_api_service(service_id, actor=user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{service_id}/check", response_model=APIService)
async def check_api_service(
    service_id: str,
    user: User = Depends(require_roles(Role.ADMINISTRATOR, Role.DEVELOPER, Role.OPERATOR)),
    state=Depends(get_app_state),
) -> APIService:
    service = await state.get_api_service(service_id)
    await state.record_log(
        LogEntry(
            id=generate_id(),
            category="api",
            level=LogLevel.INFO,
            message=f"API {service.name} probed by {user.username}",
            timestamp=utcnow(),
            source="api",
        )
    )
    await state.create_notification(
        NotificationCreate(
            title="API geprüft",
            message=f"{service.name} wurde getestet.",
            severity=Severity.INFO,
            category="api",
        ),
        actor=user.username,
    )
    return service


__all__ = ["router"]
