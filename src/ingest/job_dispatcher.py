"""Fan-out dispatcher producing ViewJob instances for the processor."""
from __future__ import annotations

import uuid
from typing import Iterator

from src.core.models.view_job import ViewJob


class JobDispatcher:
    def __init__(self, concurrency: int) -> None:
        self.concurrency = concurrency

    def spawn(self, count: int) -> Iterator[ViewJob]:
        for i in range(count):
            yield ViewJob(
                job_id=str(uuid.uuid4()),
                worker_index=i,
                attempts=0,
            )