import hmac
import os
import shutil
import time
from pathlib import Path

import httpx
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

BASE = Path(__file__).parent
STATIC = BASE / "static"
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
    "Kein Gelaber, keine Floskeln."
)

MODES = {
    "chat": "",
    "edit": (
        "Mailo will ein Video schneiden. Plane den Edit zum genannten Thema als knappe Liste: "
        "1) Hook (erste 2 Sekunden, konkret), 2) Clips/Szenen in Reihenfolge mit Dauer, "
        "3) Musik (Stimmung, BPM, Beispiel-Genre), 4) Schnitte & Übergänge (auf Beat, Jump-Cuts usw.), "
        "5) Text-Overlays, 6) Ende/Call-to-Action. Kurz und umsetzbar."
    ),
    "learn": (
        "Mailo will etwas lernen. Erklär das Thema einfach und kurz (max. 6 Sätze, mit Beispiel). "
        "Stell danach genau EINE Quiz-Frage mit Antwortmöglichkeiten A/B/C, Lösung NICHT verraten. "
        "Wenn Mailo eine Quiz-Antwort gibt, sag ob richtig und warum."
    ),
}

PROVIDERS = [
    {
        "name": "Gemini",
        "env": "GEMINI_API_KEY",
        "url": "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
        "model": os.environ.get("GEMINI_MODEL", "gemini-2.5-flash"),
    },
    {
        "name": "Groq",
        "env": "GROQ_API_KEY",
        "url": "https://api.groq.com/openai/v1/chat/completions",
        "model": os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile"),
    },
]


class Msg(BaseModel):
    role: str
    content: str


class ChatIn(BaseModel):
    messages: list[Msg]
    mode: str = "chat"


async def ask(messages: list[dict]) -> tuple[str, str]:
    errors = []
    available = [p for p in PROVIDERS if os.environ.get(p["env"])]
    if not available:
        missing = " oder ".join(p["env"] for p in PROVIDERS)
        last = messages[-1]["content"] if messages else ""
        return (
            f"Demo-Modus, Mailo 😉 Mir fehlt ein Schlüssel: setz {missing} als Umgebungsvariable "
            f"und starte web/start.sh neu. Du hast gesagt: „{last[:120]}“",
            "demo",
        )
    async with httpx.AsyncClient(timeout=40) as client:
        for p in available:
            try:
                r = await client.post(
                    p["url"],
                    headers={"Authorization": f"Bearer {os.environ[p['env']]}"},
                    json={"model": p["model"], "messages": messages, "temperature": 0.7},
                )
                r.raise_for_status()
                return r.json()["choices"][0]["message"]["content"].strip(), p["name"]
            except Exception as e:  # automatic fallback to next provider
                code = getattr(getattr(e, "response", None), "status_code", type(e).__name__)
                errors.append(f"{p['name']}: {code}")
    return "Gerade erreiche ich kein Gehirn (" + ", ".join(errors) + "). Versuch's gleich nochmal.", "error"


@app.post("/api/chat", dependencies=[Depends(require_auth)])
async def chat(body: ChatIn):
    system = PERSONA + ("\n\n" + MODES[body.mode] if MODES.get(body.mode) else "")
    msgs = [{"role": "system", "content": system}] + [
        {"role": m.role if m.role in ("user", "assistant") else "user", "content": m.content}
        for m in body.messages[-20:]
    ]
    reply, provider = await ask(msgs)
    return {"reply": reply, "provider": provider}


@app.get("/api/status", dependencies=[Depends(require_auth)])
def status():
    keys = {p["env"]: bool(os.environ.get(p["env"])) for p in PROVIDERS}
    keys["JARVIS_WEB_TOKEN"] = bool(os.environ.get("JARVIS_WEB_TOKEN"))
    tools = {t: bool(shutil.which(t)) for t in ("ffmpeg", "yt-dlp", "git", "node")}
    return {"keys": keys, "tools": tools, "models": {p["name"]: p["model"] for p in PROVIDERS}}


@app.post("/api/login")
def login(authorization: str = Header(default="")):
    require_auth(authorization)
    return {"ok": True}


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
