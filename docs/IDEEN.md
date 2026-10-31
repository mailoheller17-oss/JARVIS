# Jarvis – 10 Verbesserungen

| # | Idee | Nutzen | Aufwand | Stand |
|---|------|--------|---------|-------|
| 1 | **Natürliche Stimme**: ElevenLabs → Edge-TTS → Browser, automatisch | Jarvis klingt wie Jarvis statt wie ein Navi, auch ohne Schlüssel (Edge-TTS gratis) | klein | ✅ umgesetzt |
| 2 | **Live-Wissen im Chat**: Wetter (Open-Meteo), Wikipedia, Google-Trends werden automatisch mitgeliefert | Echte, aktuelle Antworten statt Raten; Trends = Ideen für Edits; klappt sogar im Demo-Modus | klein | ✅ umgesetzt |
| 3 | **Thumbnails per `/bild …`** (Pollinations, ohne Schlüssel) + Schnell-Knöpfe pro Kachel | Thumbnail-Entwürfe in Sekunden, weniger Tippen am Handy | klein | ✅ umgesetzt |
| 4 | **Material-Finder im Edit-Plan**: passende Clips von Pexels/Pixabay und SFX von Freesound direkt als Vorschau-Links | Vom Plan direkt zum fertigen Material | mittel | offen |
| 5 | **Auto-Rohschnitt mit ffmpeg**: Clips hochladen → Schnitte auf den Beat → Vorschau-MP4 | Spart die nervigste Arbeit am Edit | groß | offen |
| 6 | **Lern-Streak + Karteikarten**: falsche Quiz-Antworten werden zu Wiederholungskarten (Spaced Repetition) | Bleibt wirklich hängen, motiviert täglich | mittel | offen |
| 7 | **Geld-Coach**: Einnahmen/Ausgaben schnell eintragen, Jarvis sagt, wann das Sparziel erreicht ist und wo du sparen kannst | Sparziel schneller erreichen | mittel | offen |
| 8 | **Gaming-Modus**: Patch-Notes/News zu deinen Games, Build-/Loadout-Tipps, Session-Timer mit Pausen-Reminder | Besser spielen, nicht versumpfen | mittel | offen |
| 9 | **Morgen-Briefing per Telegram**: Wetter, Termine (ICS), Trends, Sparziel-Stand um 7 Uhr | Alltag im Griff ohne App zu öffnen | mittel | offen |
| 10 | **Gedächtnis**: Jarvis merkt sich Fakten über dich („mein Kanal heißt …“) und nutzt sie in jeder Antwort | Persönlichere, bessere Antworten | mittel | offen |

## Vorschaubilder neu machen

```bash
python3 tools/screenshots.py   # App muss laufen (web/start.sh)
```
Ansehen: `/vorschau` in der App oder direkt `docs/vorschau/`.
