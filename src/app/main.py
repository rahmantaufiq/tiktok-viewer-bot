"""CLI bootstrap for the TikTok Viewer Bot."""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

import click
from loguru import logger

from src.app.pipeline import build_pipeline
from src.core.config_loader import load_settings


@click.command()
@click.option("--config", default="config/settings.yaml", help="Path to settings YAML.")
@click.option("--dry-run", is_flag=True, help="Skip actual navigation, log only.")
@click.option("--version", is_flag=True, help="Print version and exit.")
def main(config: str, dry_run: bool, version: bool) -> None:
    if version:
        from src import __version__
        click.echo(f"tiktok-viewer-bot {__version__}")
        return

    cfg_path = Path(config)
    if not cfg_path.exists():
        logger.error(f"Config not found: {cfg_path}")
        sys.exit(1)

    settings = load_settings(cfg_path)
    if dry_run:
        settings.runtime.dry_run = True

    logger.info(f"Starting pipeline -> {settings.runtime.target_url}")
    asyncio.run(build_pipeline(settings).run())


if __name__ == "__main__":
    main()