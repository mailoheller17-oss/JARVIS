"""Zeigt den Handy-Link mit Auto-Login (Token im Link). Nur dir selbst schicken!"""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
tok = os.environ.get("JARVIS_WEB_TOKEN") or (ROOT / "data" / ".devtoken").read_text().strip()
cs = os.environ.get("CODESPACE_NAME")
base = (f"https://{cs}-8765.{os.environ.get('GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN', 'app.github.dev')}"
        if cs else "http://localhost:8765")
print(f"{base}/?t={tok}")
