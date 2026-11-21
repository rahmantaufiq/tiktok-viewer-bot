"""Writes pipeline results to disk in json/csv."""
from __future__ import annotations

import csv
import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from src.core.config_loader import OutputCfg
from src.core.models.view_job import ViewResult


class ReportWriter:
    def __init__(self, cfg: OutputCfg) -> None:
        self.cfg = cfg
        Path(cfg.log_dir).mkdir(parents=True, exist_ok=True)

    def write(self, results: list[ViewResult]) -> Path:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        if self.cfg.report_format == "csv":
            path = Path(self.cfg.log_dir) / f"run_{stamp}.csv"
            with path.open("w", newline="", encoding="utf-8") as fh:
                writer = csv.DictWriter(fh, fieldnames=list(asdict(results[0]).keys()))
                writer.writeheader()
                for r in results:
                    writer.writerow(asdict(r))
        else:
            path = Path(self.cfg.log_dir) / f"run_{stamp}.json"
            path.write_text(
                json.dumps([asdict(r) for r in results], indent=2),
                encoding="utf-8",
            )
        return path