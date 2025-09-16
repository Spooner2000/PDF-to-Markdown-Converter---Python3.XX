"""FastAPI application factory for the Admin Automation Dashboard Pro backend."""

from __future__ import annotations

from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from .api.v1 import api_router
from .config import settings
from .events import EventEnvelope
from .lifecycle import shutdown, startup
from .state import AppState


def create_app() -> FastAPI:
    app = FastAPI(title=settings.project_name, version="0.1.0")
    app.state.app_state = AppState()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=settings.api_v1_prefix)

    @app.get("/healthz")
    async def health_check(state: AppState = Depends(lambda: app.state.app_state)) -> dict:
        await state.bootstrap()
        return {
            "status": "ok",
            "counts": (await state.dashboard_snapshot())["counts"],
        }

    @app.on_event("startup")
    async def _startup() -> None:  # pragma: no cover - startup hook
        await startup(app)

    @app.on_event("shutdown")
    async def _shutdown() -> None:  # pragma: no cover - shutdown hook
        await shutdown(app)

    @app.websocket("/ws/events")
    async def events_websocket(websocket: WebSocket) -> None:
        await websocket.accept()
        state: AppState = app.state.app_state
        queue = await state.events.subscribe()
        try:
            while True:
                event: EventEnvelope = await queue.get()
                await websocket.send_json(event.model_dump(mode="json"))
        except WebSocketDisconnect:
            pass
        finally:
            await state.events.unsubscribe(queue)

    return app


app = create_app()

__all__ = ["create_app", "app"]
