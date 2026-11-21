"""Playwright browser lifecycle + fingerprint injection."""
from __future__ import annotations

import random
from pathlib import Path

from playwright.async_api import Browser, BrowserContext, Page, async_playwright

from src.core.config_loader import FingerprintCfg
from src.core.models.proxy_entry import ProxyEntry


class BrowserFactory:
    def __init__(self, fp: FingerprintCfg, headless: bool) -> None:
        self.fp = fp
        self.headless = headless
        self._pw = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None
        self._page: Page | None = None

    async def _ensure(self) -> Browser:
        if self._browser is None:
            self._pw = await async_playwright().start()
            self._browser = await self._pw.chromium.launch(headless=self.headless)
        return self._browser

    def _pick_ua(self) -> str:
        path = Path(self.fp.user_agents_file)
        if path.exists():
            pool = [l.strip() for l in path.read_text().splitlines() if l.strip()]
            if pool:
                return random.choice(pool)
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

    async def new_page(self, proxy: ProxyEntry | None = None, session: dict | None = None) -> Page:
        browser = await self._ensure()
        kwargs: dict = {"user_agent": self._pick_ua()}
        if proxy:
            kwargs["proxy"] = proxy.to_playwright()
        if self.fp.viewport_randomize:
            kwargs["viewport"] = {
                "width": random.choice([1280, 1366, 1440, 1920]),
                "height": random.choice([720, 768, 900, 1080]),
            }
        if self.fp.locale_pool:
            kwargs["locale"] = random.choice(self.fp.locale_pool)
        self._context = await browser.new_context(**kwargs)
        self._page = await self._context.new_page()
        return self._page

    async def close_page(self) -> None:
        if self._context:
            await self._context.close()
            self._context = None
            self._page = None

    async def shutdown(self) -> None:
        if self._browser:
            await self._browser.close()
        if self._pw:
            await self._pw.stop()