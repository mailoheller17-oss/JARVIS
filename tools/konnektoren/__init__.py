"""Konnektor-Register: lädt alle Module in diesem Ordner.

Jedes Modul definiert: name, titel, kategorie, beschreibung, kosten, env (Pflicht-Variablen),
key_url (wo es den Schlüssel gibt) und test() -> (ok, meldung).
Text-KI-Module definieren zusätzlich `llm = {"base_url", "model", "key_env", "prioritaet"}`.
"""
import importlib
import json
import os
import pkgutil
from pathlib import Path

from ._basis import BEZAHLT

SETTINGS = Path(__file__).resolve().parents[2] / "data" / "einstellungen.json"
KATEGORIEN = ["Sprache", "KI-Text", "Bilder", "Video-KI", "Material", "Wissen", "Übersetzen",
              "Alltag", "Messenger", "Entwickler"]


def alle():
    mods = []
    for info in pkgutil.iter_modules(__path__):
        if not info.name.startswith("_"):
            mods.append(importlib.import_module(f"{__name__}.{info.name}"))
    order = {k: i for i, k in enumerate(KATEGORIEN)}
    return sorted(mods, key=lambda m: (order.get(m.kategorie, 99), getattr(m, "llm", {}).get("prioritaet", 50), m.titel))


def get(name):
    return next((m for m in alle() if m.name == name), None)


def _load():
    try:
        return json.loads(SETTINGS.read_text())
    except Exception:
        return {}


def einstellungen():
    return _load()


def speichern(data):
    SETTINGS.parent.mkdir(parents=True, exist_ok=True)
    SETTINGS.write_text(json.dumps(data, indent=2, ensure_ascii=False))


def aktiv(m) -> bool:
    saved = _load().get("aktiv", {})
    return saved.get(m.name, m.kosten != BEZAHLT)  # kostenpflichtig = standardmäßig AUS


def setze_aktiv(name, wert: bool):
    data = _load()
    data.setdefault("aktiv", {})[name] = bool(wert)
    speichern(data)


def konfiguriert(m) -> bool:
    return all(os.environ.get(v) for v in m.env)


def status(m) -> str:
    if not aktiv(m):
        return "aus"
    if not konfiguriert(m):
        return "schluessel_fehlt"
    extra = getattr(m, "bereit", None)
    if extra and not extra():
        return "schluessel_fehlt"
    return "verbunden"


def info(m) -> dict:
    return {
        "name": m.name, "titel": m.titel, "kategorie": m.kategorie, "beschreibung": m.beschreibung,
        "kosten": m.kosten, "env": m.env, "key_url": m.key_url, "status": status(m), "aktiv": aktiv(m),
        "hinweis": getattr(m, "hinweis", ""),
    }


def gehirne():
    """Text-KIs in Nutzungsreihenfolge: erst gratis/gratis-kontingent nach Priorität, dann aktivierte kostenpflichtige."""
    ready = [m for m in alle() if hasattr(m, "llm") and status(m) == "verbunden"]
    return sorted(ready, key=lambda m: (m.kosten == BEZAHLT, m.llm.get("prioritaet", 50)))
