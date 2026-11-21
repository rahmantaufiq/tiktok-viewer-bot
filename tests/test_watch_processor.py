import asyncio

import pytest

from src.core.models.view_job import ViewJob


class _FakePage:
    async def goto(self, *a, **kw):
        return None


class _FakeBrowser:
    async def new_page(self, proxy=None, session=None):
        return _FakePage()

    async def close_page(self):
        return None


class _FakeProxy:
    def next(self):
        return None


class _FakeSessions:
    def acquire(self):
        return {}


def test_single_job_success(monkeypatch):
    from src.processors.watch_processor import WatchProcessor

    proc = WatchProcessor(_FakeBrowser(), _FakeProxy(), _FakeSessions())
    job = ViewJob(job_id="t1", worker_index=0, target_url="https://www.tiktok.com/@x/video/1", watch_seconds=0)
    result = asyncio.run(proc._run_one(job))
    assert result.success is True
    assert job.attempts == 1