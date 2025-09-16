"""Shared dependencies for API routes."""

from fastapi import Request

from ..state import AppState


def get_app_state(request: Request) -> AppState:
    return request.app.state.app_state


__all__ = ["get_app_state"]
