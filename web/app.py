import os, time
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

BASE = Path(__file__).parent
STATIC = BASE / "static"
BOOT_ID = str(time.time())

app = FastAPI(title="Jarvis")

@app.get("/api/version")
def version():
    # changes on every auto-reload -> browser reloads itself
    return {"boot": BOOT_ID}

@app.get("/")
def index():
    return FileResponse(STATIC / "index.html")

app.mount("/static", StaticFiles(directory=STATIC), name="static")
