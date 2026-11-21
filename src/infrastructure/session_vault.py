"""Encrypted-at-rest storage for session cookies (local dev only)."""
from __future__ import annotations

import json
from pathlib import Path


class SessionVault:
    """Very light wrapper — do not commit the vault file to git."""

    def __init__(self, path: str = "sessions/vault.json") -> None:
        self.path = Path(path)

    def save(self, key: str, cookie_blob: dict) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        data = self._read()
        data[key] = cookie_blob
        self.path.write_text(json.dumps(data), encoding="utf-8")

    def load(self, key: str) -> dict | None:
        return self._read().get(key)

    def _read(self) -> dict:
        if not self.path.exists():
            return {}
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}