# JARVIS

Jarvis ist ein persönlicher KI-Assistent für einen alten Windows-PC als Server. Er arbeitet mit Telegram, einer privaten Web-App, lokaler KI-Auswahl, Video-/Audio-Analyse, Recherche, Lernen, Geld, PC-Steuerung und Edit-Workflow. Grundidee: kurze, ehrliche, natürliche Gespräche, privat ausgeliefert, keine Standardfloskeln.

## Schnellstart
1. Python 3.11+ installieren.
2. In einem leeren Ordner `git clone` dieses Repo klonen.
3. `pip install -r requirements.txt`
4. `cp .env.example .env` und nur die Werte manuell ergänzen.
5. `python check.py`
6. `scripts/install.ps1` ausführen.

## Wichtige Befehle
- `jcheck` – Schnellprüfung
- `jhelp` – Hilfe
- `jedit "BMW bei Nacht"` – Edit-Auftrag starten
- `jweb` – Web-App starten
- `jupdate` – pull + Pakete installieren

## Verhalten
- Berlin-/deutsche Umgangssprache, kurze Antworten
- Fallback bei 429/Quota/Fehlern
- Umfeld: Windows-PC Server, iPhone/iPad per Telegram + Tailscale private Web-App
- keine öffentlichen Uploads ohne Bestätigung

## Struktur
- `kern/` – Gehirn, Einstellungen, Auswahl der KI
- `tools/` – Telegram, Schnitt, Recherche, Sehen, Hören, PC, Lernen, Geld
- `web/` – FastAPI + UI
- `scripts/` – Installations- und Update-Logik
- `docs/` – Hinweise und Übergabe
