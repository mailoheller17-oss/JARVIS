import asyncio
import hmac
import re
import os
import shutil
import sys
import time
import urllib.parse
from pathlib import Path

import httpx
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

BASE = Path(__file__).parent
ROOT = BASE.parent
sys.path.insert(0, str(ROOT))
from tools import konnektoren as K  # noqa: E402
from tools import wissen  # noqa: E402

STATIC = BASE / "static"
VORSCHAU = ROOT / "docs" / "vorschau"
VORSCHAU.mkdir(parents=True, exist_ok=True)
BOOT_ID = str(time.time())

app = FastAPI(title="Jarvis")


# ---------- Auth ----------
def _token() -> str:
    return os.environ.get("JARVIS_WEB_TOKEN") or os.environ.get("JARVIS_DEV_TOKEN") or ""


def require_auth(authorization: str = Header(default="")):
    expected = _token()
    given = authorization.removeprefix("Bearer ").strip()
    if not expected or not hmac.compare_digest(given, expected):
        raise HTTPException(401, "Falscher Token")


# ---------- Brain ----------
PERSONA = (
    "Du bist Jarvis, der persönliche Assistent von Mailo. Du duzt Mailo, bist locker, "
    "direkt und antwortest kurz (meist 1-4 Sätze), auf Deutsch, außer Mailo schreibt anders. "
    "Mailo tippt oft schnell: Tippfehler und Umgangssprache verstehst du einfach, ohne darauf hinzuweisen. "
    "Kein Gelaber, keine Floskeln. Wenn Live-Daten mitgeliefert werden, nutze sie und erfinde nichts dazu."
)

MODES = {
    "chat": "",
    "edit": (
        "Mailo will ein Video schneiden. Plane den Edit zum genannten Thema als knappe Liste: "
        "1) Hook (erste 2 Sekunden, konkret), 2) Clips/Szenen in Reihenfolge mit Dauer, "
        "3) Musik (Stimmung, BPM, Beispiel-Genre), 4) Schnitte & Übergänge (auf Beat, Jump-Cuts usw.), "
        "5) Text-Overlays, 6) Ende/Call-to-Action. Kurz und umsetzbar. "
        "Gratis-Material: Pexels/Pixabay (Clips), Mixkit/Freesound (Musik, SFX)."
    ),
    "learn": (
        "Mailo will etwas lernen. Erklär das Thema einfach und kurz (max. 6 Sätze, mit Beispiel). "
        "Stell danach genau EINE Quiz-Frage mit Antwortmöglichkeiten A/B/C, Lösung NICHT verraten. "
        "Wenn Mailo eine Quiz-Antwort gibt, sag ob richtig und warum."
    ),
}


class Msg(BaseModel):
    role: str
    content: str


class ChatIn(BaseModel):
    messages: list[Msg]
    mode: str = "chat"


async def _ask_cli(messages: list[dict]) -> str:
    prompt = "\n\n".join(f"[{m['role']}]\n{m['content']}" for m in messages) + "\n\n[assistant]\n"
    p = await asyncio.create_subprocess_exec("claude", "-p", prompt, stdout=asyncio.subprocess.PIPE,
                                             stderr=asyncio.subprocess.DEVNULL)
    out, _ = await asyncio.wait_for(p.communicate(), 90)
    if p.returncode:
        raise RuntimeError(f"exit {p.returncode}")
    return out.decode().strip()


async def ask(messages: list[dict], live: list[str]) -> tuple[str, str]:
    brains = K.gehirne()
    if not brains:
        last = messages[-1]["content"] if messages else ""
        if live:  # Live-Daten gibt's auch ohne KI – direkt ausgeben
            return ("\n\n".join(live) + "\n\n(Demo-Modus: Mit GEMINI_API_KEY fasse ich dir das locker zusammen.)", "demo")
        return (
            "Demo-Modus, Mailo 😉 Mir fehlt ein KI-Schlüssel – am einfachsten GEMINI_API_KEY "
            "(gratis: aistudio.google.com/apikey) oder GROQ_API_KEY. Danach web/start.sh neu starten. "
            f"Du hast gesagt: „{last[:120]}“",
            "demo",
        )
    errors = []
    async with httpx.AsyncClient(timeout=40) as client:
        for m in brains:
            try:
                if m.llm.get("cli"):
                    return await _ask_cli(messages), m.titel
                key = os.environ.get(m.llm["key_env"]) if m.llm.get("key_env") else None
                r = await client.post(
                    m.llm["base_url"].rstrip("/") + "/chat/completions",
                    headers={"Authorization": f"Bearer {key}"} if key else {},
                    json={"model": m.llm["model"], "messages": messages, "temperature": 0.7},
                )
                r.raise_for_status()
                return r.json()["choices"][0]["message"]["content"].strip(), m.titel
            except Exception as e:  # automatischer Wechsel zum nächsten Gehirn
                code = getattr(getattr(e, "response", None), "status_code", type(e).__name__)
                errors.append(f"{m.titel}: {code}")
    return "Gerade erreiche ich kein Gehirn (" + ", ".join(errors) + "). Versuch's gleich nochmal.", "fehler"


def bild_url(prompt: str) -> str:
    q = urllib.parse.quote(prompt[:400])
    return f"https://image.pollinations.ai/prompt/{q}?width=1280&height=720&nologo=true&seed={int(time.time()) % 99999}"


JARVIS_PREFIX = re.compile(r"^\s*(hey |hi |ok |okay )?(jarvis|javis|jarvi|jervis)[\s,.:!]*", re.I)


@app.post("/api/chat", dependencies=[Depends(require_auth)])
async def chat(body: ChatIn):
    if body.messages:
        body.messages[-1].content = JARVIS_PREFIX.sub("", body.messages[-1].content).strip() or body.messages[-1].content
    last = body.messages[-1].content.strip() if body.messages else ""
    # /bild <beschreibung> -> Thumbnail über Pollinations (gratis, ohne Schlüssel)
    if last.lower().startswith(("/bild", "/thumbnail")):
        prompt = last.split(" ", 1)[1] if " " in last else "cinematic youtube thumbnail"
        if K.status(K.get("pollinations")) != "verbunden":
            return {"reply": "Pollinations ist in den Konnektoren ausgeschaltet.", "provider": "-"}
        return {"reply": f"Hier dein Bild zu „{prompt}“:", "image": bild_url(prompt), "provider": "Pollinations"}

    live = await wissen.kontext(last) if last else []
    system = PERSONA + ("\n\n" + MODES[body.mode] if MODES.get(body.mode) else "")
    if live:
        system += "\n\nLive-Daten:\n" + "\n".join(live)
        if any(x.startswith("Aktuelle Top-Meldungen") for x in live):
            system += ("\n\nFasse die Nachrichten als lockeres Briefing zusammen: 5-7 kurze Punkte mit passendem Emoji, "
                       "Wichtigstes zuerst, je 1 Satz. Am Ende ein kurzer Satz, was davon für Mailo interessant sein könnte.")
    msgs = [{"role": "system", "content": system}] + [
        {"role": m.role if m.role in ("user", "assistant") else "user", "content": m.content}
        for m in body.messages[-20:]
    ]
    reply, provider = await ask(msgs, live)
    return {"reply": reply, "provider": provider, "live": bool(live)}


# ---------- Stimme: ElevenLabs -> edge-tts -> (Browser) ----------
class TtsIn(BaseModel):
    text: str


@app.post("/api/tts", dependencies=[Depends(require_auth)])
async def tts(body: TtsIn):
    text = body.text.replace("*", "").replace("#", "")[:1500]
    el = K.get("elevenlabs")
    if el and K.status(el) == "verbunden":
        try:
            async with httpx.AsyncClient(timeout=30) as c:
                r = await c.post(
                    f"https://api.elevenlabs.io/v1/text-to-speech/{el.voice_id}",
                    headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"]},
                    json={"text": text, "model_id": "eleven_multilingual_v2"},
                )
                r.raise_for_status()
                return Response(r.content, media_type="audio/mpeg", headers={"X-Stimme": "ElevenLabs"})
        except Exception:
            pass
    et = K.get("edge_tts")
    if et and K.status(et) == "verbunden":
        try:
            import edge_tts
            audio = bytearray()
            async for chunk in edge_tts.Communicate(text, et.stimme, rate="+8%").stream():
                if chunk["type"] == "audio":
                    audio += chunk["data"]
            if audio:
                return Response(bytes(audio), media_type="audio/mpeg", headers={"X-Stimme": "Edge-TTS"})
        except Exception:
            pass
    raise HTTPException(503, "Keine Server-Stimme, Browser übernimmt")


# ---------- Konnektoren ----------
@app.get("/api/konnektoren", dependencies=[Depends(require_auth)])
def konnektoren_liste():
    return {"kategorien": K.KATEGORIEN, "konnektoren": [K.info(m) for m in K.alle()],
            "gehirn": [m.titel for m in K.gehirne()]}


@app.post("/api/konnektoren/{name}/test", dependencies=[Depends(require_auth)])
async def konnektor_test(name: str):
    m = K.get(name)
    if not m:
        raise HTTPException(404)
    if not K.konfiguriert(m):
        return {"ok": False, "meldung": "Schlüssel fehlt: " + ", ".join(m.env)}
    ok, msg = await asyncio.to_thread(m.test)
    return {"ok": ok, "meldung": msg}


class AktivIn(BaseModel):
    aktiv: bool


@app.post("/api/konnektoren/{name}/aktiv", dependencies=[Depends(require_auth)])
def konnektor_aktiv(name: str, body: AktivIn):
    m = K.get(name)
    if not m:
        raise HTTPException(404)
    K.setze_aktiv(name, body.aktiv)
    return K.info(m)


@app.get("/api/status", dependencies=[Depends(require_auth)])
def status():
    alle = K.alle()
    keys = {}
    for m in alle:
        for v in m.env:
            keys[v] = bool(os.environ.get(v))
    keys["JARVIS_WEB_TOKEN"] = bool(os.environ.get("JARVIS_WEB_TOKEN"))
    tools = {t: bool(shutil.which(t)) for t in ("ffmpeg", "yt-dlp", "git", "node", "claude")}
    verbunden = [m.titel for m in alle if K.status(m) == "verbunden"]
    return {"keys": keys, "tools": tools, "gehirn": [m.titel for m in K.gehirne()], "verbunden": verbunden}


@app.post("/api/login")
def login(authorization: str = Header(default="")):
    require_auth(authorization)
    return {"ok": True}


# ---------- Vorschau ----------
@app.get("/vorschau", response_class=HTMLResponse)
def vorschau():
    bilder = sorted(p.name for p in VORSCHAU.glob("*.png"))
    gruppen: dict[str, list[str]] = {}
    for b in bilder:
        gruppen.setdefault(b.rsplit("-", 1)[0], []).append(b)
    v = int(time.time())
    rows = "".join(
        f"<section><h2>{g}</h2><div class='row'>"
        + "".join(f"<figure><a href='/vorschau-bilder/{b}' target='_blank'><img loading='lazy' src='/vorschau-bilder/{b}?v={v}'></a>"
                  f"<figcaption>{b}</figcaption></figure>" for b in bs)
        + "</div></section>"
        for g, bs in gruppen.items()
    ) or "<p>Noch keine Screenshots. Starte <code>python3 tools/screenshots.py</code>.</p>"
    return f"""<!doctype html><html lang="de"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Jarvis Vorschau</title>
<style>body{{margin:0;padding:16px;background:#05070d;color:#d8f3ff;font:15px system-ui,sans-serif}}
h1{{color:#2fd6ff;font-weight:300;letter-spacing:.3em}}h2{{font-size:15px;color:#7fe6ff;margin:22px 0 8px}}
.row{{display:flex;gap:14px;align-items:flex-start;overflow-x:auto;padding-bottom:6px}}
figure{{margin:0;flex:none}}img{{display:block;height:340px;width:auto;border:1px solid #17304a;border-radius:10px}}
figcaption{{font-size:12px;color:#6f8aa3;margin-top:4px}}a{{color:#2fd6ff}}
@media(max-width:600px){{img{{height:220px}}}}</style></head><body>
<h1>JARVIS · VORSCHAU</h1><p><a href="/">← zur App</a> · {len(bilder)} Screenshots</p>{rows}</body></html>"""


app.mount("/vorschau-bilder", StaticFiles(directory=VORSCHAU), name="vorschau-bilder")


# ---------- Dev auto-reload + static ----------
@app.get("/api/version")
def version():
    return {"boot": BOOT_ID}


@app.get("/")
def index():
    return FileResponse(STATIC / "index.html", headers={"Cache-Control": "no-cache"})


@app.get("/sw.js")
def sw():
    return FileResponse(STATIC / "sw.js", media_type="application/javascript",
                        headers={"Cache-Control": "no-cache"})


@app.get("/manifest.json")
def manifest():
    return FileResponse(STATIC / "manifest.json", media_type="application/manifest+json")


app.mount("/static", StaticFiles(directory=STATIC), name="static")
