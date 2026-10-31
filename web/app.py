"""Web-App-Basis für Jarvis."""

from __future__ import annotations

from fastapi import FastAPI

app = FastAPI(title="Jarvis Web App")


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": "jarvis"}
