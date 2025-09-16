"""FastAPI lifecycle hooks."""

from __future__ import annotations

from fastapi import FastAPI

from .state import AppState


async def startup(app: FastAPI) -> None:
    state: AppState = app.state.app_state
    await state.bootstrap()
    await state.start_background_tasks()


async def shutdown(app: FastAPI) -> None:
    state: AppState = app.state.app_state
    await state.stop_background_tasks()


__all__ = ["startup", "shutdown"]
