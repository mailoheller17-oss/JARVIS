"""Zentrale Einstellungen für server/client-Mode."""

from __future__ import annotations

import json
import os
from pathlib import Path


def load_settings(path: str | None = None) -> dict:
    target = Path(path or os.getenv("JARVIS_HOME", ".")) / "einstellungen.json"
    if not target.exists():
        return {
            "rolle": "server",
            "home": str(Path(os.getenv("JARVIS_HOME", ".")).resolve()),
            "telegram_enabled": True,
            "web_enabled": True,
            "debug": False,
        }

    with open(target, "r", encoding="utf-8") as fh:
        return json.load(fh)
