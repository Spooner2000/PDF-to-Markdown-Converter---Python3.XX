"""Application state container with CRUD helpers."""

from __future__ import annotations

import asyncio
from typing import Any, Dict, List, Optional

from fastapi import HTTPException, status

from .auth import AuthService
from .config import settings
from .events import EventBus
from .schemas.apis import (
    APIAuthConfig,
    APIEnvironment,
    APIEndpoint,
    APIMonitoring,
    APIService,
    APIServiceCreate,
    APIServiceUpdate,
    AuthMode,
    HTTPMethod,
)
from .schemas.common import AuditTrail, HealthStatus, LogLevel, Severity
from .schemas.devices import (
    Device,
    DeviceCapability,
    DeviceConnection,
    DeviceCreate,
    DeviceCredential,
    CredentialType,
    DeviceStatus,
    DeviceUpdate,
)
from .schemas.http_servers import (
    HTTPRoute,
    HTTPServer,
    HTTPServerCreate,
    HTTPServerStatus,
    HTTPServerUpdate,
    TLSConfig,
)
from .schemas.observability import LogEntry, MetricSample, MetricUnit, Notification, NotificationCreate
from .schemas.routines import (
    RetryPolicy,
    Routine,
    RoutineAction,
    RoutineCreate,
    RoutineStatus,
    RoutineStep,
    TriggerType,
    RoutineTrigger,
    RoutineUpdate,
)
from .schemas.scripts import Script, ScriptCreate, ScriptLanguage, ScriptUpdate
from .schemas.venv import PackageInfo, VirtualEnvironment, VirtualEnvironmentCreate, VirtualEnvironmentUpdate
from .schemas.auth import User
from .services.telemetry import TelemetryService
from .storage import ResourceStore, TemporalStore
from .utils.datetime import utcnow
from .utils.identifiers import generate_id


def _audit(actor: str, previous: Optional[AuditTrail] = None) -> AuditTrail:
    now = utcnow()
    if previous is None:
        return AuditTrail(created_at=now, updated_at=now, created_by=actor, updated_by=actor)
    return AuditTrail(
        created_at=previous.created_at,
        updated_at=now,
        created_by=previous.created_by,
        updated_by=actor,
    )


class AppState:
    """Aggregates repositories and convenience operations."""

    def __init__(self) -> None:
        self.events = EventBus()
        self.auth = AuthService(self.events)
        self.routines: ResourceStore[Routine] = ResourceStore()
        self.scripts: ResourceStore[Script] = ResourceStore()
        self.devices: ResourceStore[Device] = ResourceStore()
        self.apis: ResourceStore[APIService] = ResourceStore()
        self.http_servers: ResourceStore[HTTPServer] = ResourceStore()
        self.venvs: ResourceStore[VirtualEnvironment] = ResourceStore()
        self.logs: TemporalStore[LogEntry] = TemporalStore(maxlen=settings.logs_retention)
        self.metrics: TemporalStore[MetricSample] = TemporalStore(maxlen=settings.metrics_retention)
        self.notifications: ResourceStore[Notification] = ResourceStore()
        self.telemetry = TelemetryService(self)
        self._bootstrap_lock = asyncio.Lock()
        self._bootstrapped = False

    async def bootstrap(self) -> None:
        if self._bootstrapped:
            return
        async with self._bootstrap_lock:
            if self._bootstrapped:
                return
            await self._seed_demo_content()
            self._bootstrapped = True

    async def start_background_tasks(self) -> None:
        await self.telemetry.start()

    async def stop_background_tasks(self) -> None:
        await self.telemetry.stop()

    async def _seed_demo_content(self) -> None:
        system_user = "system"
        script = Script(
            id=generate_id(),
            name="Sample Health Check",
            description="Checks the availability of a device",
            language=ScriptLanguage.PYTHON,
            entrypoint="main.py",
            code="""import time\nprint('health ok')\ntime.sleep(0.2)""",
            parameters=[],
            version="1.0.0",
            audit=_audit(system_user),
        )
        await self.scripts.set(script)

        routine = Routine(
            id=generate_id(),
            name="Nightly Backup",
            description="Backs up configuration every night",
            trigger=RoutineTrigger(type=TriggerType.CRON, expression="0 2 * * *", timezone="UTC"),
            steps=[
                RoutineStep(
                    name="Export configuration",
                    action=RoutineAction(
                        action_type="script",
                        target=script.id,
                        parameters={"mode": "backup"},
                    ),
                )
            ],
            owner="admin",
            tags=["backup", "nightly"],
            status=RoutineStatus.PAUSED,
            version=1,
            concurrency_limit=1,
            retry_policy=RetryPolicy(max_attempts=3, delay_seconds=60, backoff_factor=2.0, jitter_seconds=5.0),
            audit=_audit(system_user),
        )
        await self.routines.set(routine)

        device = Device(
            id=generate_id(),
            name="Edge Router",
            description="Main branch office router",
            device_type="router",
            status=DeviceStatus.WARNING,
            health=HealthStatus.WARNING,
            connection=DeviceConnection(
                host="192.168.10.1",
                protocol="ssh",
                port=22,
                credential=DeviceCredential(
                    type=CredentialType.SSH_KEY,
                    username="admin",
                    secret_reference="secret://ssh/router",
                ),
            ),
            capabilities=[DeviceCapability(name="backup", metadata={"supports": ["config", "firmware"]})],
            metadata={"vendor": "Acme"},
            tags=["network"],
            audit=_audit(system_user),
        )
        await self.devices.set(device)

        api = APIService(
            id=generate_id(),
            name="Inventory API",
            description="Corporate CMDB",
            environments=[APIEnvironment(name="prod", base_url="https://api.example.com")],
            default_environment="prod",
            auth=APIAuthConfig(mode=AuthMode.BEARER, token_url="https://auth.example.com/token"),
            endpoints=[
                APIEndpoint(name="List assets", method=HTTPMethod.GET, path="/assets", timeout_seconds=10.0, retries=1),
            ],
            tags=["cmdb"],
            monitoring=APIMonitoring(
                success_rate=99.9,
                last_checked_at=utcnow(),
                average_latency_ms=120.0,
                p95_latency_ms=320.0,
                error_rate=0.1,
            ),
            health=HealthStatus.HEALTHY,
            audit=_audit(system_user),
        )
        await self.apis.set(api)

        server = HTTPServer(
            id=generate_id(),
            name="Webhook Relay",
            description="Receives device alerts",
            host="0.0.0.0",
            port=8080,
            status=HTTPServerStatus.STOPPED,
            tls=TLSConfig(enabled=False),
            routes=[HTTPRoute(path="/hooks/alerts", methods=["POST"], script_id=script.id)],
            middlewares=[],
            tags=["alerts"],
            health=HealthStatus.UNKNOWN,
            audit=_audit(system_user),
        )
        await self.http_servers.set(server)

        venv = VirtualEnvironment(
            id=generate_id(),
            name="automation-core",
            description="Base environment for automation scripts",
            python_version="3.12",
            location="/opt/aadp/venvs/automation-core",
            packages=[
                PackageInfo(name="fastapi", version="0.111.0"),
                PackageInfo(name="httpx", version="0.27.0"),
            ],
            status=HealthStatus.HEALTHY,
            audit=_audit(system_user),
        )
        await self.venvs.set(venv)

        await self.record_metric(
            MetricSample(
                id=generate_id(),
                name="cpu_usage",
                value=24.5,
                unit=MetricUnit.PERCENT,
                timestamp=utcnow(),
                tags={"host": "controller"},
            )
        )
        await self.record_log(
            LogEntry(
                id=generate_id(),
                category="system",
                level=LogLevel.INFO,
                message="Demo content initialised",
                timestamp=utcnow(),
                source="bootstrap",
            )
        )
        notification = Notification(
            id=generate_id(),
            title="Willkommen",
            message="Demo-Daten wurden geladen.",
            severity=Severity.INFO,
            created_at=utcnow(),
            category="system",
            metadata={},
        )
        await self.notifications.set(notification)

    # Routine management -------------------------------------------------
    async def list_routines(self) -> List[Routine]:
        return await self.routines.list()

    async def get_routine(self, routine_id: str) -> Routine:
        routine = await self.routines.get(routine_id)
        if not routine:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Routine not found")
        return routine

    async def create_routine(self, payload: RoutineCreate, user: User) -> Routine:
        routine = Routine(
            id=generate_id(),
            name=payload.name,
            description=payload.description,
            trigger=payload.trigger,
            steps=payload.steps,
            owner=user.username,
            tags=payload.tags,
            status=RoutineStatus.DRAFT,
            version=1,
            concurrency_limit=payload.concurrency_limit,
            retry_policy=payload.retry_policy,
            audit=_audit(user.username),
        )
        await self.routines.set(routine)
        await self.events.publish("routine.created", {"id": routine.id, "name": routine.name})
        return routine

    async def update_routine(self, routine_id: str, payload: RoutineUpdate, user: User) -> Routine:
        routine = await self.get_routine(routine_id)
        update_data = payload.model_dump(exclude_unset=True)
        if "status" in update_data and update_data["status"] is None:
            update_data.pop("status")
        updated = routine.model_copy(
            update={**update_data, "version": routine.version + 1, "audit": _audit(user.username, routine.audit)},
        )
        await self.routines.set(updated)
        await self.events.publish("routine.updated", {"id": routine.id, "name": routine.name})
        return updated

    async def delete_routine(self, routine_id: str, actor: User) -> None:
        routine = await self.routines.delete(routine_id)
        if not routine:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Routine not found")
        await self.events.publish("routine.deleted", {"id": routine.id, "name": routine.name, "actor": actor.username})

    # Script management --------------------------------------------------
    async def list_scripts(self) -> List[Script]:
        return await self.scripts.list()

    async def get_script(self, script_id: str) -> Script:
        script = await self.scripts.get(script_id)
        if not script:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Script not found")
        return script

    async def create_script(self, payload: ScriptCreate, user: User) -> Script:
        script = Script(
            id=generate_id(),
            name=payload.name,
            description=payload.description,
            language=payload.language,
            entrypoint=payload.entrypoint,
            code=payload.code,
            parameters=payload.parameters,
            tags=payload.tags,
            version="1.0.0",
            audit=_audit(user.username),
        )
        await self.scripts.set(script)
        await self.events.publish("script.created", {"id": script.id, "name": script.name})
        return script

    async def update_script(self, script_id: str, payload: ScriptUpdate, user: User) -> Script:
        script = await self.get_script(script_id)
        update_data = payload.model_dump(exclude_unset=True)
        if "version" not in update_data:
            update_data["version"] = self._increment_version(script.version)
        updated = script.model_copy(update={**update_data, "audit": _audit(user.username, script.audit)})
        await self.scripts.set(updated)
        await self.events.publish("script.updated", {"id": script.id, "name": script.name})
        return updated

    async def delete_script(self, script_id: str, actor: User) -> None:
        script = await self.scripts.delete(script_id)
        if not script:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Script not found")
        await self.events.publish("script.deleted", {"id": script.id, "name": script.name, "actor": actor.username})

    # Device management --------------------------------------------------
    async def list_devices(self) -> List[Device]:
        return await self.devices.list()

    async def get_device(self, device_id: str) -> Device:
        device = await self.devices.get(device_id)
        if not device:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
        return device

    async def create_device(self, payload: DeviceCreate, user: User) -> Device:
        device = Device(
            id=generate_id(),
            name=payload.name,
            description=payload.description,
            device_type=payload.device_type,
            status=DeviceStatus.UNKNOWN,
            health="unknown",  # type: ignore[arg-type]
            connection=payload.connection,
            capabilities=payload.capabilities,
            tags=payload.tags,
            audit=_audit(user.username),
        )
        await self.devices.set(device)
        await self.events.publish("device.created", {"id": device.id, "name": device.name})
        return device

    async def update_device(self, device_id: str, payload: DeviceUpdate, user: User) -> Device:
        device = await self.get_device(device_id)
        update_data = payload.model_dump(exclude_unset=True)
        updated = device.model_copy(update={**update_data, "audit": _audit(user.username, device.audit)})
        await self.devices.set(updated)
        await self.events.publish("device.updated", {"id": device.id, "name": device.name})
        return updated

    async def delete_device(self, device_id: str, actor: User) -> None:
        device = await self.devices.delete(device_id)
        if not device:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
        await self.events.publish("device.deleted", {"id": device.id, "name": device.name, "actor": actor.username})

    # API management -----------------------------------------------------
    async def list_api_services(self) -> List[APIService]:
        return await self.apis.list()

    async def get_api_service(self, service_id: str) -> APIService:
        service = await self.apis.get(service_id)
        if not service:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="API not found")
        return service

    async def create_api_service(self, payload: APIServiceCreate, user: User) -> APIService:
        service = APIService(
            id=generate_id(),
            name=payload.name,
            description=payload.description,
            environments=payload.environments,
            default_environment=payload.default_environment,
            auth=payload.auth,
            endpoints=payload.endpoints,
            tags=payload.tags,
            monitoring={},  # type: ignore[arg-type]
            health="unknown",  # type: ignore[arg-type]
            audit=_audit(user.username),
        )
        await self.apis.set(service)
        await self.events.publish("api.created", {"id": service.id, "name": service.name})
        return service

    async def update_api_service(self, service_id: str, payload: APIServiceUpdate, user: User) -> APIService:
        service = await self.get_api_service(service_id)
        update_data = payload.model_dump(exclude_unset=True)
        updated = service.model_copy(update={**update_data, "audit": _audit(user.username, service.audit)})
        await self.apis.set(updated)
        await self.events.publish("api.updated", {"id": service.id, "name": service.name})
        return updated

    async def delete_api_service(self, service_id: str, actor: User) -> None:
        service = await self.apis.delete(service_id)
        if not service:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="API not found")
        await self.events.publish("api.deleted", {"id": service.id, "name": service.name, "actor": actor.username})

    # HTTP server management --------------------------------------------
    async def list_http_servers(self) -> List[HTTPServer]:
        return await self.http_servers.list()

    async def get_http_server(self, server_id: str) -> HTTPServer:
        server = await self.http_servers.get(server_id)
        if not server:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Server not found")
        return server

    async def create_http_server(self, payload: HTTPServerCreate, user: User) -> HTTPServer:
        server = HTTPServer(
            id=generate_id(),
            name=payload.name,
            description=payload.description,
            host=payload.host,
            port=payload.port,
            tls=payload.tls,
            routes=payload.routes,
            middlewares=payload.middlewares,
            tags=payload.tags,
            status=HTTPServerStatus.STOPPED,
            health="unknown",  # type: ignore[arg-type]
            audit=_audit(user.username),
        )
        await self.http_servers.set(server)
        await self.events.publish("http_server.created", {"id": server.id, "name": server.name})
        return server

    async def update_http_server(self, server_id: str, payload: HTTPServerUpdate, user: User) -> HTTPServer:
        server = await self.get_http_server(server_id)
        update_data = payload.model_dump(exclude_unset=True)
        updated = server.model_copy(update={**update_data, "audit": _audit(user.username, server.audit)})
        await self.http_servers.set(updated)
        await self.events.publish("http_server.updated", {"id": server.id, "name": server.name})
        return updated

    async def delete_http_server(self, server_id: str, actor: User) -> None:
        server = await self.http_servers.delete(server_id)
        if not server:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Server not found")
        await self.events.publish("http_server.deleted", {"id": server.id, "name": server.name, "actor": actor.username})

    # Virtual environment management ------------------------------------
    async def list_virtual_environments(self) -> List[VirtualEnvironment]:
        return await self.venvs.list()

    async def get_virtual_environment(self, venv_id: str) -> VirtualEnvironment:
        venv = await self.venvs.get(venv_id)
        if not venv:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Virtual environment not found")
        return venv

    async def create_virtual_environment(
        self, payload: VirtualEnvironmentCreate, user: User
    ) -> VirtualEnvironment:
        venv = VirtualEnvironment(
            id=generate_id(),
            name=payload.name,
            description=payload.description,
            python_version=payload.python_version,
            location=f"/opt/aadp/venvs/{payload.name}",
            packages=payload.packages,
            tags=payload.tags,
            status=HealthStatus.UNKNOWN,
            audit=_audit(user.username),
        )
        await self.venvs.set(venv)
        await self.events.publish("venv.created", {"id": venv.id, "name": venv.name})
        return venv

    async def update_virtual_environment(
        self, venv_id: str, payload: VirtualEnvironmentUpdate, user: User
    ) -> VirtualEnvironment:
        venv = await self.get_virtual_environment(venv_id)
        update_data = payload.model_dump(exclude_unset=True)
        updated = venv.model_copy(update={**update_data, "audit": _audit(user.username, venv.audit)})
        await self.venvs.set(updated)
        await self.events.publish("venv.updated", {"id": venv.id, "name": venv.name})
        return updated

    async def delete_virtual_environment(self, venv_id: str, actor: User) -> None:
        venv = await self.venvs.delete(venv_id)
        if not venv:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Virtual environment not found")
        await self.events.publish("venv.deleted", {"id": venv.id, "name": venv.name, "actor": actor.username})

    # Observability ------------------------------------------------------
    async def record_log(self, entry: LogEntry) -> None:
        await self.logs.append(entry)
        await self.events.publish(
            "log.created",
            {
                "id": entry.id,
                "category": entry.category,
                "level": entry.level,
                "message": entry.message,
                "timestamp": entry.timestamp.isoformat(),
            },
        )

    async def list_logs(self, category: Optional[str] = None, level: Optional[str] = None, limit: int = 100) -> List[LogEntry]:
        entries = await self.logs.list(limit=limit)
        filtered = []
        for entry in entries:
            if category and entry.category != category:
                continue
            if level and entry.level != level:
                continue
            filtered.append(entry)
        return filtered[-limit:]

    async def record_metric(self, sample: MetricSample) -> None:
        await self.metrics.append(sample)
        await self.events.publish(
            "metric.created",
            {
                "id": sample.id,
                "name": sample.name,
                "value": sample.value,
                "unit": sample.unit,
                "timestamp": sample.timestamp.isoformat(),
            },
        )

    async def list_metrics(self, name: Optional[str] = None, limit: int = 100) -> List[MetricSample]:
        samples = await self.metrics.list(limit=limit)
        if name:
            samples = [sample for sample in samples if sample.name == name]
        return samples[-limit:]

    async def create_notification(self, payload: NotificationCreate, actor: str) -> Notification:
        notification = Notification(
            id=generate_id(),
            title=payload.title,
            message=payload.message,
            severity=payload.severity,
            created_at=utcnow(),
            category=payload.category,
            metadata=payload.metadata,
        )
        await self.notifications.set(notification)
        await self.events.publish("notification.created", {"id": notification.id, "title": notification.title, "actor": actor})
        return notification

    async def list_notifications(self) -> List[Notification]:
        return await self.notifications.list()

    async def mark_notification_read(self, notification_id: str, actor: User) -> Notification:
        notification = await self.notifications.get(notification_id)
        if not notification:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
        if notification.read_at:
            return notification
        updated = notification.model_copy(update={"read_at": utcnow()})
        await self.notifications.set(updated)
        await self.events.publish("notification.read", {"id": notification.id, "actor": actor.username})
        return updated

    async def dashboard_snapshot(self) -> Dict[str, Any]:
        routines, scripts, devices, apis, servers, venvs = await asyncio.gather(
            self.routines.list(),
            self.scripts.list(),
            self.devices.list(),
            self.apis.list(),
            self.http_servers.list(),
            self.venvs.list(),
        )
        logs = await self.list_logs(limit=10)
        metrics = await self.list_metrics(limit=10)
        notifications = await self.list_notifications()
        return {
            "counts": {
                "routines": len(routines),
                "scripts": len(scripts),
                "devices": len(devices),
                "apis": len(apis),
                "http_servers": len(servers),
                "venvs": len(venvs),
            },
            "recent_logs": logs,
            "recent_metrics": metrics,
            "notifications": [n for n in notifications if not n.read_at][-5:],
            "system_health": {
                "devices": self._health_score(devices, attr="health"),
                "apis": self._health_score(apis, attr="health"),
                "http_servers": self._health_score(servers, attr="health"),
            },
            "scripts": scripts,
            "api_services": apis,
            "http_servers": servers,
        }

    def _health_score(self, resources: List[Any], attr: str) -> str:
        if not resources:
            return "unknown"
        statuses = [getattr(res, attr, "unknown") for res in resources]
        if any(status == "critical" for status in statuses):
            return "critical"
        if any(status == "warning" for status in statuses):
            return "warning"
        if all(status == "healthy" for status in statuses):
            return "healthy"
        return "unknown"

    def _increment_version(self, version: str) -> str:
        try:
            major, minor, patch = [int(part) for part in version.split(".")]
        except ValueError:
            return version
        patch += 1
        return f"{major}.{minor}.{patch}"


__all__ = ["AppState"]
