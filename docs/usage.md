# Usage

## Quickstart

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
copy config\settings.example.yaml config\settings.yaml
python -m src.app.main --dry-run
```

## Dry-run vs live

`--dry-run` will skip actual navigation and only emit results to
`logs/run_*.json`. Use it to validate config and proxy pools before
pointing the bot at a real video URL.

## Proxy pool format

`config/proxies.txt` supports:

```
1.2.3.4:8080
user:pass@10.0.0.1:3128
```

Leave `proxy.enabled: false` to disable rotation entirely.

## Reporting

Reports are written per-run to `logs/` in either JSON or CSV
(controlled by `output.report_format`).

## ⚠️ Legal notice

This repository is a **research / educational** tool for studying
engagement mechanics on short-form video platforms. Using it to
inflate view counts on videos you do not own violates TikTok's Terms
of Service and may be illegal in your jurisdiction. Use at your own
risk; the maintainers accept no liability.