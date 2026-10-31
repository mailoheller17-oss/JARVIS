# JARVIS

Jarvis ist ein persönlicher KI-Assistent für einen älteren Windows-PC als Server, mit Handy-Zugriff über Telegram und private Web-App, lokalem Fallback, Werkzeugen für Video, Audio, Recherche, Lernen, Geld und PC-Steuerung.

## Ziele
- Intelligente Modellwahl: kostenloser Fallback, lokale Modelle, Claude Code CLI bei schwereren Aufgaben
- Persönlicher Stil: locker, ehrlich, kurz, duzt den Nutzer, verständigt sich mit Umgangssprache
- Web-App als private lokale Oberfläche über Tailscale
- Telegram-Workflow mit Sprachnachricht, Befehlen und Bestätigungsfragen
- Edit-Workflow per Handy: Thema, Stil, Länge, Material, Auto-Edit, Freigabe

## Struktur
- `kern/` – Gehirn, Einstellungen, Routing, zentrale Logik
- `web/` – FastAPI-Backend + UI-Assets
- `tools/` – KI, Telegram, Schnitt, Recherche, Sehen, Hören, PC, Lernen, Geld, Pipeline
- `scripts/` – Installation, Hilfsbefehle, Updates
- `docs/` – Dokumentation und Übergabe an Claude Code

## Regeln
- Keine .env-Dateien lesen oder auslesen. Werte nur über Umgebungsvariablen oder `.env.example`.
- Keine Schlüssel, Tokens oder persönlichen Daten im Code.
- Alles, was löscht, sendet, postet, kauft oder hochlädt, braucht Freigabe.
- Fallbacks und lokale Tools haben Vorrang vor Cloud-Features.
- Alles kurz, deutsch, verständlich, ohne Standardfloskeln.
- Windows- und Handy-Features müssen immer sicher und leicht nachvollziehbar sein.

## Befehle
- `python check.py`
- `scripts/install.ps1`
- `jcheck`
- `jhelp`
- `jedit "BMW bei Nacht"`
- `jweb`

## Sicherheit
- `.env` ist niemals im Repo.
- Keine öffentlichen Uploads ohne explizite Freigabe.
- Keine Downloads von YouTube/TikTok/Instagram.
- Nur lizenzfreie Medienquellen nutzen.

## TODO-CLAUDE
- Windows-spezifische Funktionen mit echten Tests nur auf dem Ziel-PC prüfen.
- Mikrofon, Telegram, Tailscale, ffmpeg und OCR sind hier ungetestet und müssen sauber abgesichert werden.
