"""Gehirn von Jarvis.

Ziel: passende KI automatisch wählen, Fallbacks nutzen, Fehler/Quota erkennen,
Tageszähler für Claude-Aufrufe führen.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any


@dataclass
class ModelDecision:
    provider: str
    model: str
    mode: str
    reason: str


def choose_model(task: str, offline: bool = False, fallback_on_error: bool = True) -> ModelDecision:
    """Ermittle das passende Modell je nach Aufgabe und Verfügbarkeit."""
    task_text = (task or "").lower()

    if offline:
        return ModelDecision("ollama", "llama3", "local", "Offline-Modus aktiv")

    if "schwer" in task_text or "komplex" in task_text or "code" in task_text:
        return ModelDecision("claude_cli", "claude -p", "heavy", "Komplexe Aufgabe, Claude Code CLI bevorzugt")

    if "bild" in task_text or "video" in task_text or "vision" in task_text:
        return ModelDecision("gemini", "gemini-2.5-flash", "vision", "Vision- oder Video-Aufgabe")

    if "kurz" in task_text or "simple" in task_text:
        return ModelDecision("groq", "llama-3.1-8b", "cheap", "Einfache Aufgabe, günstiger Fallback")

    return ModelDecision("openrouter", "openrouter/default", "general", "Allgemeiner Lauf")


def record_claude_call(day_key: str | None = None) -> int:
    """Zählt Claude-Aufrufe pro Tag. Wird im späteren Projekt in einer Datei/DB persistiert."""
    base = os.getenv("JARVIS_HOME", ".")
    path = os.path.join(base, "Gedaechtnis", "claude_calls.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)

    import json
    data: dict[str, Any] = {}
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except Exception:
            data = {}

    key = day_key or "today"
    value = int(data.get(key, 0)) + 1
    data[key] = value
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)
    return value
