# Contributing to tiktok-viewer-bot

Thanks for your interest in improving the TikTok Viewer Bot.

## Development Setup

1. Clone the repo and create a virtualenv:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   playwright install chromium
   ```
2. Copy `config/settings.example.yaml` to `config/settings.yaml` and edit.
3. Run the bot: `python -m src.app.main --dry-run`

## Pull Request Guidelines

- Keep PRs scoped to a single pipeline stage (ingest, process, or output).
- Add a test under `tests/` for any new worker or handler.
- Do not commit live session cookies, proxy lists, or account databases.
- Follow the existing loguru-based logging style; no `print()` in library code.

## Code Style

- Python 3.11+, type hints preferred.
- Format with `black` (line length 100).
- Ruff for linting.

## Reporting Bugs

Open an issue with:
- Bot version (`python -m src.app.main --version`)
- Config excerpt (redact proxies/sessions)
- Relevant log tail from `logs/`