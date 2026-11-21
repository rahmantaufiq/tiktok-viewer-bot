"""Normalizes and validates TikTok video URLs from config or CLI."""
from __future__ import annotations

import re
from urllib.parse import urlparse

TIKTOK_HOSTS = {"www.tiktok.com", "tiktok.com", "vm.tiktok.com", "vt.tiktok.com"}
VIDEO_PATH_RE = re.compile(r"/@[^/]+/video/\d+")


def resolve_target(url: str) -> str:
    parsed = urlparse(url.strip())
    if parsed.netloc not in TIKTOK_HOSTS:
        raise ValueError(f"Not a TikTok host: {parsed.netloc}")
    if not VIDEO_PATH_RE.search(parsed.path) and "vm.tiktok.com" not in parsed.netloc:
        raise ValueError(f"Unrecognized TikTok URL shape: {url}")
    return url.strip()