"""Schemas for automation routines and flows."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import Field

from .common import APIModel, BaseResource


class RoutineStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    DISABLED = "disabled"
    ERROR = "error"


class TriggerType(str, Enum):
    CRON = "cron"
    INTERVAL = "interval"
    FIXED_TIME = "fixed_time"
    EVENT = "event"
    MANUAL = "manual"


class RoutineTrigger(APIModel):
    type: TriggerType
    expression: str
    timezone: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class RetryPolicy(APIModel):
    max_attempts: int = 1
    delay_seconds: float = 0.0
    backoff_factor: float = 1.0
    jitter_seconds: float = 0.0


class RoutineAction(APIModel):
    action_type: str
    target: str
    parameters: Dict[str, Any] = Field(default_factory=dict)


class RoutineStep(APIModel):
    name: str
    description: Optional[str] = None
    action: RoutineAction
    timeout_seconds: Optional[float] = None


class Routine(BaseResource):
    status: RoutineStatus
    trigger: RoutineTrigger
    steps: List[RoutineStep]
    owner: str
    version: int
    concurrency_limit: int = 1
    retry_policy: RetryPolicy = Field(default_factory=RetryPolicy)
    last_run_at: Optional[datetime] = None
    next_run_at: Optional[datetime] = None


class RoutineCreate(APIModel):
    name: str
    description: Optional[str] = None
    trigger: RoutineTrigger
    steps: List[RoutineStep]
    tags: List[str] = Field(default_factory=list)
    concurrency_limit: int = 1
    retry_policy: RetryPolicy = Field(default_factory=RetryPolicy)


class RoutineUpdate(APIModel):
    name: Optional[str] = None
    description: Optional[str] = None
    trigger: Optional[RoutineTrigger] = None
    steps: Optional[List[RoutineStep]] = None
    tags: Optional[List[str]] = None
    concurrency_limit: Optional[int] = None
    retry_policy: Optional[RetryPolicy] = None
    status: Optional[RoutineStatus] = None


class RoutineExecution(APIModel):
    routine_id: str
    started_at: datetime
    finished_at: Optional[datetime] = None
    status: RoutineStatus
    logs: List[str] = Field(default_factory=list)
    result: Dict[str, Any] = Field(default_factory=dict)


__all__ = [
    "Routine",
    "RoutineStatus",
    "RoutineTrigger",
    "TriggerType",
    "RoutineAction",
    "RoutineStep",
    "RoutineCreate",
    "RoutineUpdate",
    "RoutineExecution",
    "RetryPolicy",
]
