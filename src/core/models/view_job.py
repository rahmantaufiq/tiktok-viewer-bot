"""Job/result dataclasses shared across pipeline stages."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ViewJob:
    job_id: str
    worker_index: int
    attempts: int = 0
    target_url: str = ""
    watch_seconds: int = 18
    tags: dict[str, str] = field(default_factory=dict)


@dataclass
class ViewResult:
    job_id: str
    success: bool
    proxy: str | None = None
    error: str | None = None
    duration_ms: int = 0