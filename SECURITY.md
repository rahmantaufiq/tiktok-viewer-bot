# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.4.x   | Yes       |
| 0.3.x   | No        |

## Reporting a Vulnerability

This is an educational / research project for studying view-count manipulation
mechanics on short-form video platforms. Do **not** use it against accounts you
do not own. Do **not** deploy it at scale against production TikTok endpoints.

If you find a security issue (e.g. session leakage, proxy credential exposure,
or an unintended write to an account database), please email the maintainer
privately rather than opening a public issue.

We aim to respond within 72 hours.

## Scope

- Session cookie handling in `src/infrastructure/session_vault.py`
- Proxy rotation logic in `src/core/services/proxy_rotator.py`
- Playwright fingerprint spoofing in `src/infrastructure/browser_factory.py`

Out of scope: TikTok's own ToS violations arising from misuse of this tool.
Use at your own risk.