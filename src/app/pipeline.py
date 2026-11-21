"""Wires ingest -> processor -> output stages together."""
from __future__ import annotations

from src.core.config_loader import Settings
from src.core.models.view_job import ViewJob
from src.core.services.proxy_rotator import ProxyRotator
from src.core.services.session_manager import SessionManager
from src.infrastructure.browser_factory import BrowserFactory
from src.infrastructure.report_writer import ReportWriter
from src.ingest.job_dispatcher import JobDispatcher
from src.processors.watch_processor import WatchProcessor


class Pipeline:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.dispatcher = JobDispatcher(settings.runtime.concurrency)
        self.sessions = SessionManager(settings)
        self.proxies = ProxyRotator(settings.proxy)
        self.browser = BrowserFactory(settings.fingerprint, settings.runtime.headless)
        self.processor = WatchProcessor(self.browser, self.proxies, self.sessions)
        self.reporter = ReportWriter(settings.output)

    async def run(self) -> None:
        jobs = list(self.dispatcher.spawn(self.settings.runtime.concurrency))
        results = await self.processor.run_batch(jobs)
        self.reporter.write(results)
        await self.browser.shutdown()


def build_pipeline(settings: Settings) -> Pipeline:
    return Pipeline(settings)