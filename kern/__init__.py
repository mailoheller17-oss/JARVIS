"""Zentrale Hilfsfunktionen für Jarvis."""

from __future__ import annotations

import os
from pathlib import Path

JARVIS_HOME = Path(os.getenv("JARVIS_HOME", ".")).resolve()


def get_jarvis_home() -> Path:
    return JARVIS_HOME


def ensure_dir(path: str | Path) -> Path:
    target = Path(path)
    target.mkdir(parents=True, exist_ok=True)
    return target
