"""Background telemetry generator for demo purposes."""

from __future__ import annotations

import asyncio
import random
from contextlib import suppress

from ..config import settings
from ..schemas.common import LogLevel, Severity
from ..schemas.observability import LogEntry, MetricSample, MetricUnit, NotificationCreate
from ..utils.datetime import utcnow
from ..utils.identifiers import generate_id


class TelemetryService:
    """Produces synthetic metrics, logs and occasional notifications."""

    def __init__(self, state) -> None:
        from ..state import AppState  # local import to avoid circular dependency

        self.state: "AppState" = state
        self._task: asyncio.Task | None = None
        self._running = False
        self._random = random.Random()

    async def start(self) -> None:
        if self._task and not self._task.done():
            return
        self._running = True
        self._task = asyncio.create_task(self._run(), name="telemetry-worker")

    async def stop(self) -> None:
        self._running = False
        if self._task:
            self._task.cancel()
            with suppress(asyncio.CancelledError):
                await self._task
            self._task = None

    async def _run(self) -> None:
        try:
            while self._running:
                await asyncio.sleep(settings.telemetry_interval_seconds)
                await self._emit_metrics()
                await self._maybe_emit_log()
        finally:
            self._task = None

    async def _emit_metrics(self) -> None:
        timestamp = utcnow()
        cpu = MetricSample(
            id=generate_id(),
            name="cpu_usage",
            value=round(self._random.uniform(15, 75), 2),
            unit=MetricUnit.PERCENT,
            timestamp=timestamp,
            tags={"host": "controller"},
        )
        mem = MetricSample(
            id=generate_id(),
            name="memory_usage",
            value=round(self._random.uniform(1024, 8192), 2),
            unit=MetricUnit.MEGABYTES,
            timestamp=timestamp,
            tags={"host": "controller"},
        )
        net = MetricSample(
            id=generate_id(),
            name="network_latency",
            value=round(self._random.uniform(5, 80), 2),
            unit=MetricUnit.MILLISECONDS,
            timestamp=timestamp,
            tags={"host": "controller"},
        )
        await self.state.record_metric(cpu)
        await self.state.record_metric(mem)
        await self.state.record_metric(net)

    async def _maybe_emit_log(self) -> None:
        chance = self._random.random()
        level = LogLevel.INFO
        severity = None
        message = "Routine heartbeat"
        if chance > 0.8:
            level = LogLevel.WARN
            severity = Severity.WARNING
            message = "Routine backlog exceeds expected threshold"
        elif chance < 0.1:
            level = LogLevel.ERROR
            severity = Severity.ERROR
            message = "Gerätekommunikation kurzzeitig fehlgeschlagen"
        entry = LogEntry(
            id=generate_id(),
            category="telemetry",
            level=level,
            message=message,
            timestamp=utcnow(),
            source="telemetry",
        )
        await self.state.record_log(entry)
        if severity:
            await self.state.create_notification(
                NotificationCreate(
                    title="Systemhinweis",
                    message=message,
                    severity=severity,
                    category="telemetry",
                ),
                actor="telemetry",
            )


__all__ = ["TelemetryService"]
