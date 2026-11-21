"""Proxy pool entry model."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ProxyEntry:
    host: str
    port: int
    user: str | None = None
    password: str | None = None

    @property
    def label(self) -> str:
        return f"{self.host}:{self.port}"

    def to_playwright(self) -> dict:
        cfg = {"server": f"http://{self.host}:{self.port}"}
        if self.user:
            cfg["username"] = self.user
            cfg["password"] = self.password or ""
        return cfg