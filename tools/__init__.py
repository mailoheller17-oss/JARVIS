"""FastAPI-App, die als private Web-App läuft."""

from __future__ import annotations

from fastapi import FastAPI

from web import app as web_app

app = FastAPI(title="Jarvis")


@app.get("/")
async def index() -> dict:
    return {"message": "Jarvis läuft", "status": "ok"}


@app.get("/status")
async def status() -> dict:
    return {"status": "online", "mode": "server"}


app.mount("/api", web_app)
