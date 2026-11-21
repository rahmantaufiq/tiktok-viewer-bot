"""Loads and validates YAML settings into typed dataclasses."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class RuntimeCfg:
    headless: bool = True
    concurrency: int = 4
    target_url: str = ""
    watch_seconds: int = 18
    dry_run: bool = True


@dataclass
class ProxyCfg:
    enabled: bool = False
    pool_file: str = "config/proxies.txt"
    rotate_every: int = 3


@dataclass
class FingerprintCfg:
    user_agents_file: str = "config/user_agents.txt"
    viewport_randomize: bool = True
    locale_pool: list[str] = field(default_factory=lambda: ["en-US"])


@dataclass
class OutputCfg:
    log_dir: str = "logs"
    state_file: str = "viewer_state.json"
    report_format: str = "json"


@dataclass
class Settings:
    runtime: RuntimeCfg
    proxy: ProxyCfg
    fingerprint: FingerprintCfg
    output: OutputCfg


def load_settings(path: Path) -> Settings:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    return Settings(
        runtime=RuntimeCfg(**raw.get("runtime", {})),
        proxy=ProxyCfg(**raw.get("proxy", {})),
        fingerprint=FingerprintCfg(**raw.get("fingerprint", {})),
        output=OutputCfg(**raw.get("output", {})),
    )