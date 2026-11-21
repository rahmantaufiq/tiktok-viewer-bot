"""Round-robin proxy rotation with optional stickiness."""
from __future__ import annotations

import itertools
from pathlib import Path

from src.core.config_loader import ProxyCfg
from src.core.models.proxy_entry import ProxyEntry


def _parse_line(line: str) -> ProxyEntry | None:
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    if "@" in line:
        creds, hostport = line.split("@", 1)
        user, _, pw = creds.partition(":")
        host, _, port = hostport.partition(":")
        return ProxyEntry(host=host, port=int(port), user=user, password=pw)
    host, _, port = line.partition(":")
    return ProxyEntry(host=host, port=int(port))


class ProxyRotator:
    def __init__(self, cfg: ProxyCfg) -> None:
        self.cfg = cfg
        self._entries: list[ProxyEntry] = []
        self._cycle = None
        if cfg.enabled:
            self._load()

    def _load(self) -> None:
        path = Path(self.cfg.pool_file)
        if not path.exists():
            return
        for line in path.read_text(encoding="utf-8").splitlines():
            entry = _parse_line(line)
            if entry:
                self._entries.append(entry)
        if self._entries:
            self._cycle = itertools.cycle(self._entries)

    def next(self) -> ProxyEntry | None:
        if not self._cycle:
            return None
        return next(self._cycle)