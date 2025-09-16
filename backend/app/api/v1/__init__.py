"""Versioned API router composition."""

from fastapi import APIRouter

from . import apis, auth, dashboard, devices, http_servers, observability, routines, scripts, venvs

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(routines.router, prefix="/routines", tags=["routines"])
api_router.include_router(scripts.router, prefix="/scripts", tags=["scripts"])
api_router.include_router(devices.router, prefix="/devices", tags=["devices"])
api_router.include_router(apis.router, prefix="/apis", tags=["apis"])
api_router.include_router(http_servers.router, prefix="/http-servers", tags=["http-servers"])
api_router.include_router(venvs.router, prefix="/venvs", tags=["venvs"])
api_router.include_router(observability.router, prefix="/observability", tags=["observability"])

__all__ = ["api_router"]
