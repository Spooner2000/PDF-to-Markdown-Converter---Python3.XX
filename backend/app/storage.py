"""Thread-safe in-memory data stores for the prototype backend."""

from __future__ import annotations

import asyncio
from collections import deque
from typing import Deque, Dict, Generic, Iterable, List, Optional, TypeVar


T = TypeVar("T")


class ResourceStore(Generic[T]):
    """Generic store for CRUD style resources keyed by ``id``."""

    def __init__(self) -> None:
        self._items: Dict[str, T] = {}
        self._lock = asyncio.Lock()

    async def list(self) -> List[T]:
        async with self._lock:
            return list(self._items.values())

    async def get(self, item_id: str) -> Optional[T]:
        async with self._lock:
            return self._items.get(item_id)

    async def set(self, item: T) -> T:
        key = getattr(item, "id")
        async with self._lock:
            self._items[key] = item
        return item

    async def bulk_set(self, items: Iterable[T]) -> None:
        async with self._lock:
            for item in items:
                key = getattr(item, "id")
                self._items[key] = item

    async def delete(self, item_id: str) -> Optional[T]:
        async with self._lock:
            return self._items.pop(item_id, None)


class TemporalStore(Generic[T]):
    """FIFO store with a configurable maximum length."""

    def __init__(self, maxlen: int = 500) -> None:
        self._items: Deque[T] = deque(maxlen=maxlen)
        self._lock = asyncio.Lock()

    async def append(self, item: T) -> None:
        async with self._lock:
            self._items.append(item)

    async def extend(self, items: Iterable[T]) -> None:
        async with self._lock:
            for item in items:
                self._items.append(item)

    async def list(self, limit: Optional[int] = None) -> List[T]:
        async with self._lock:
            snapshot = list(self._items)
        if limit is None:
            return snapshot
        return snapshot[-limit:]

    async def clear(self) -> None:
        async with self._lock:
            self._items.clear()

    async def __len__(self) -> int:  # pragma: no cover - convenience method
        async with self._lock:
            return len(self._items)


__all__ = ["ResourceStore", "TemporalStore"]
