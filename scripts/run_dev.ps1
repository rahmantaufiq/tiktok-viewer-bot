# Developer launcher for tiktok-viewer-bot (Windows PowerShell)
$ErrorActionPreference = "Stop"
if (-not (Test-Path ".venv")) {
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    playwright install chromium
} else {
    .\.venv\Scripts\Activate.ps1
}
python -m src.app.main --config config/settings.yaml --dry-run