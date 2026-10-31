# Übergabe an Claude Code

## Ziel
Jarvis auf einem älteren Windows-PC als persönlicher KI-Assistent vollständig aufbauen. Die Umsetzung muss sauber, lokal nutzbar und privat bleiben.

## Reihenfolge der Arbeit
1. Basisprojekt aufbauen, Pfade, Pakete, Struktur, `.gitignore`, `.env.example`, `requirements.txt`
2. `kern/gehirn.py` bauen: Modell-Auswahl, Fallbacks, Tageszähler, Fehler- und Limit-Behandlung
3. Telegram-Bot mit Sprachanbindung und Befehlen implementieren
4. Web-App mit Token-Login, Chat, Mikrofon, Kacheln und Handy-Design bauen
5. Edit-Workflow (`tools/pipeline/edit_auftrag.py`) mit Materialrecherche und Auto-Edit
6. Video-/Audio-/Material-Analyse (`sehen`, `hoeren`, `recherche`) ergänzen
7. PC-Steuerung, Lernen, Geld und Werkzeug-Register ergänzen
8. Installationsskript, Dokumentation und README finalisieren
9. Test- und Fehlerpflege, Releasenotes und PR

## Jede Aufgabe
- klein, testbar, sauber isoliert
- nur genau eine Logik in einem Modul
- kein Feature ohne kurzen Testbefehl
- wenn ein Teil nicht auf dem aktuellen PC getestet werden kann, `TODO-CLAUDE` setzen

## Datei-Checks je Aufgabe
- prüfe zuerst nur die betroffenen Dateien
- nutze lokale Fallbacks statt externer Abhängigkeiten
- nur minimale Änderungen, keine komplette Neu-Architektur

## Testbefehle (PowerShell)
- `python -m py_compile kern/gehirn.py`
- `python -m py_compile tools/telegram/bot.py`
- `python -m py_compile web/app.py`
- `python check.py`
- `python tools/pipeline/edit_auftrag.py --thema "BMW bei Nacht" --stil aggressive --laenge 15`
- `scripts/install.ps1`

## Regeln
- `.env` nie lesen
- keine Schlüssel im Code
- keine öffentlichen Uploads ohne Bestätigung
- keine YouTube/TikTok/Instagram-Downloads
- alles mit Freigabe
- `TODO-CLAUDE` nur dort, wo Hardware-Features oder externe Dienste nicht getestet werden konnten

## Wichtige Dateien
- `kern/gehirn.py` – Modellwahl und Fallbacks
- `tools/telegram/bot.py` – Telegram-Logik
- `web/app.py` – FastAPI-App
- `tools/pipeline/edit_auftrag.py` – Auftrags-Workflow
- `scripts/install.ps1` – Installation und Aliase
- `check.py` – kurze Qualitätsprüfung
