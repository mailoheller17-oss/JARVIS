"""Macht Vorschaubilder der laufenden Jarvis-App (Desktop + iPhone, jede Kachel, jedes Design).

Aufruf:  python3 tools/screenshots.py            (App muss auf :8765 laufen, web/start.sh)
Ergebnis: docs/vorschau/*.png, ansehen unter http://localhost:8765/vorschau
Token kommt aus JARVIS_WEB_TOKEN oder web/.devtoken – wird nie ausgegeben.
"""
import os
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "vorschau"
URL = os.environ.get("JARVIS_URL", "http://localhost:8765")
GERAETE = {"desktop": dict(viewport={"width": 1440, "height": 900}),
           "handy": dict(viewport={"width": 390, "height": 844}, device_scale_factor=3, is_mobile=True, has_touch=True)}
KACHELN = ["chat", "edit", "learn", "money", "status", "konnektoren", "settings"]
NAMEN = {"chat": "start", "learn": "lernen", "money": "geld", "settings": "design"}
SKINS = ["ironman", "minimal", "neon"]

DEMO = {
    "jarvisMoney": {"name": "Neue Kamera", "goal": 650, "saved": 412.5},
    "jarvisHist": {
        "chat": [{"role": "user", "content": "yo wie wird das wetter morgn?"},
                 {"role": "assistant", "content": "Morgen 8–10 °C, ab Mittag Schauer. Jacke mit Kapuze, Mailo."}],
        "edit": [{"role": "user", "content": "Skate-Montage im Herbst"},
                 {"role": "assistant", "content": "1) Hook: Kickflip in Slow-Mo durch fallendes Laub (0–2 s)\n2) Clips: Push-Shots, Grinds, Fail-Moment, Crew-Lacher\n3) Musik: Lo-Fi Boom-Bap, 90 BPM\n4) Schnitte: auf jede Snare, Speed-Ramps bei Tricks\n5) Overlay: „Herbst-Session“\n6) Ende: Board fällt ins Laub, Abo-Hinweis"}],
        "learn": [{"role": "user", "content": "Erklär mir Zinseszins"},
                  {"role": "assistant", "content": "Zinseszins heißt: Deine Zinsen bringen selbst wieder Zinsen. 100 € mit 5 % → nach 1 Jahr 105 €, nach 2 Jahren 110,25 €.\n\nQuiz: Was wächst schneller?\nA) 5 % einfacher Zins\nB) 5 % Zinseszins\nC) beide gleich"}],
    },
}


def token() -> str:
    t = os.environ.get("JARVIS_WEB_TOKEN")
    if not t:
        f = ROOT / "data" / ".devtoken"
        t = f.read_text().strip() if f.exists() else ""
    if not t:
        sys.exit("Kein Token gefunden. Erst web/start.sh ausführen.")
    return t


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    tok = token()
    import json
    init = "".join(f"localStorage.setItem({json.dumps(k)}, {json.dumps(json.dumps(v))});" for k, v in DEMO.items())
    init += f"localStorage.setItem('jarvisToken', {json.dumps(json.dumps(tok))});localStorage.setItem('jarvisTts','false');"
    n = 0
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for geraet, opts in GERAETE.items():
            # Login-Seite (eigener Kontext ohne Token)
            lc = browser.new_context(**opts, locale="de-DE", service_workers="block")
            lp = lc.new_page()
            lp.goto(URL + "/")
            lp.wait_for_selector("#login:not([hidden])")
            lp.wait_for_timeout(800)
            lp.screenshot(path=OUT / f"login-{geraet}.png")
            lc.close()
            n += 1

            ctx = browser.new_context(**opts, locale="de-DE", service_workers="block")
            ctx.add_init_script(init)
            page = ctx.new_page()

            def shot(name, url):
                nonlocal n
                page.goto(url)
                page.wait_for_selector("#app:not([hidden])", timeout=10000)
                page.wait_for_timeout(1500)  # Animation + Daten
                page.screenshot(path=OUT / f"{name}-{geraet}.png")
                n += 1


            for k in KACHELN:
                shot(NAMEN.get(k, k), f"{URL}/?tile={k}&skin=ironman")
            for s in SKINS:
                shot(f"design-{s}", f"{URL}/?tile=chat&skin={s}")
            ctx.close()
        browser.close()
    print(f"{n} Screenshots in {OUT.relative_to(ROOT)}/  ->  {URL}/vorschau")


if __name__ == "__main__":
    main()
