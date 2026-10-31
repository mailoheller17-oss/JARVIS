# JARVIS
#
# Beispiel für die zentrale Check-Logik.
# Diese Datei soll kurz und robust sein und nur eine verlässliche Qualitätsprüfung liefern.

from __future__ import annotations

import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

CRITICAL = [
    "kern",
    "tools",
    "web",
    "scripts",
    "docs",
]

OPTIONAL = [
    "requirements.txt",
    ".env.example",
    ".gitignore",
    "README.md",
    "CLAUDE.md",
]


def check_paths() -> list[str]:
    issues: list[str] = []
    for path in CRITICAL + OPTIONAL:
        full = ROOT / path
        if not full.exists():
            issues.append(f"Fehlt: {path}")
    return issues


def check_imports() -> list[str]:
    issues: list[str] = []
    targets = [
        "kern.gehirn",
        "web.app",
        "tools.telegram.bot",
        "tools.pipeline.edit_auftrag",
    ]
    for name in targets:
        try:
            importlib.import_module(name)
        except Exception as exc:
            issues.append(f"Importfehler: {name}: {exc}")
    return issues


def main() -> int:
    problems = []
    problems.extend(check_paths())
    problems.extend(check_imports())

    if problems:
        print("Jarvis CHECK: FEHLER")
        for item in problems:
            print(f"- {item}")
        return 1

    print("Jarvis CHECK: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())

