"""Async event bus used for real-time updates and WebSocket streaming."""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Any, Dict, List
from uuid import uuid4

from pydantic import BaseModel, Field


class EventEnvelope(BaseModel):
    """Serializable payload for WebSocket and audit streaming."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    type: str
    payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class EventBus:
    """Simple publish/subscribe bus backed by asyncio queues."""

    def __init__(self) -> None:
        self._subscribers: List[asyncio.Queue[EventEnvelope]] = []
        self._lock = asyncio.Lock()

    async def subscribe(self) -> asyncio.Queue[EventEnvelope]:
        queue: asyncio.Queue[EventEnvelope] = asyncio.Queue()
        async with self._lock:
            self._subscribers.append(queue)
        return queue

    async def unsubscribe(self, queue: asyncio.Queue[EventEnvelope]) -> None:
        async with self._lock:
            if queue in self._subscribers:
                self._subscribers.remove(queue)

    async def publish(self, event_type: str, payload: Dict[str, Any]) -> EventEnvelope:
        event = EventEnvelope(type=event_type, payload=payload)
        async with self._lock:
            subscribers = list(self._subscribers)
        for queue in subscribers:
            await queue.put(event)
        return event


__all__ = ["EventBus", "EventEnvelope"]
