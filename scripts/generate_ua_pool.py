"""Utility: scrape a small set of realistic UA strings into config/user_agents.txt."""
from __future__ import annotations

from pathlib import Path

BASE = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
]


def main(out: str = "config/user_agents.txt") -> None:
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text("\n".join(BASE) + "\n", encoding="utf-8")
    print(f"wrote {len(BASE)} user agents -> {out}")


if __name__ == "__main__":
    main()