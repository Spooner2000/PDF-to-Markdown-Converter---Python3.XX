"""Schemas for script lifecycle management."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import Field

from .common import APIModel, BaseResource


class ScriptLanguage(str, Enum):
    PYTHON = "python"
    BASH = "bash"
    POWERSHELL = "powershell"
    JAVASCRIPT = "javascript"


class ScriptParameter(APIModel):
    name: str
    type: str = "string"
    required: bool = False
    default: Optional[Any] = None
    description: Optional[str] = None


class ScriptExecutionResult(APIModel):
    exit_code: int
    stdout: str
    stderr: str
    duration_ms: int
    started_at: datetime
    finished_at: datetime


class Script(BaseResource):
    language: ScriptLanguage
    version: str
    entrypoint: str
    code: str
    parameters: List[ScriptParameter] = Field(default_factory=list)
    last_run_at: Optional[datetime] = None
    last_result: Optional[ScriptExecutionResult] = None
    validated: bool = False
    repository_path: Optional[str] = None


class ScriptCreate(APIModel):
    name: str
    description: Optional[str] = None
    language: ScriptLanguage
    entrypoint: str
    code: str
    parameters: List[ScriptParameter] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)


class ScriptUpdate(APIModel):
    name: Optional[str] = None
    description: Optional[str] = None
    language: Optional[ScriptLanguage] = None
    entrypoint: Optional[str] = None
    code: Optional[str] = None
    parameters: Optional[List[ScriptParameter]] = None
    tags: Optional[List[str]] = None
    validated: Optional[bool] = None
    version: Optional[str] = None


__all__ = [
    "Script",
    "ScriptCreate",
    "ScriptUpdate",
    "ScriptParameter",
    "ScriptExecutionResult",
    "ScriptLanguage",
]
