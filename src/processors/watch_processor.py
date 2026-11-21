"""Core watch-cycle processor: navigate, dwell, mark attempt."""
from __future__ import annotations

import asyncio
from typing import Iterable

from loguru import logger

from src.core.models.view_job import ViewJob, ViewResult
from src.core.services.proxy_rotator import ProxyRotator
from src.core.services.session_manager import SessionManager
from src.infrastructure.browser_factory import BrowserFactory


class WatchProcessor:
    def __init__(
        self,
        browser: BrowserFactory,
        proxies: ProxyRotator,
        sessions: SessionManager,
    ) -> None:
        self.browser = browser
        self.proxies = proxies
        self.sessions = sessions

    async def run_batch(self, jobs: Iterable[ViewJob]) -> list[ViewResult]:
        tasks = [self._run_one(job) for job in jobs]
        return await asyncio.gather(*tasks)

    async def _run_one(self, job: ViewJob) -> ViewResult:
        proxy = self.proxies.next()
        session = self.sessions.acquire()
        try:
            page = await self.browser.new_page(proxy=proxy, session=session)
            await page.goto(job.target_url, wait_until="domcontentloaded", timeout=30000)
            await asyncio.sleep(job.watch_seconds)
            logger.info(f"[{job.job_id}] watch complete (proxy={proxy.label})")
            job.attempts += 1
            return ViewResult(job_id=job.job_id, success=True, proxy=proxy.label)
        except Exception as exc:  # noqa: BLE001
            logger.warning(f"[{job.job_id}] failed: {exc}")
            return ViewResult(job_id=job.job_id, success=False, error=str(exc))
        finally:
            await self.browser.close_page()