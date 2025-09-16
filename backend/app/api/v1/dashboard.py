"""High-level dashboard view endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from ...auth import get_current_user
from ...schemas.auth import User
from ..deps import get_app_state

router = APIRouter()


@router.get("/summary")
async def dashboard_summary(
    _: User = Depends(get_current_user),
    state=Depends(get_app_state),
) -> dict:
    return await state.dashboard_snapshot()


__all__ = ["router"]
