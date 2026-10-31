"""Gemeinsame Helfer für Konnektoren. Schlüssel werden nur aus der Umgebung gelesen und nie ausgegeben."""
import os

import httpx

GRATIS, KONTINGENT, BEZAHLT = "gratis", "gratis-kontingent", "kostenpflichtig"


def env(name: str) -> str:
    return os.environ.get(name, "")


def http_test(url: str, method: str = "GET", ok: str = "verbunden", timeout: float = 15, **kw) -> tuple[bool, str]:
    try:
        r = httpx.request(method, url, timeout=timeout, follow_redirects=True, **kw)
    except Exception as e:  # nur Fehlertyp, nie Header/URL mit Schlüssel
        return False, f"nicht erreichbar ({type(e).__name__})"
    if r.status_code in (401, 403):
        return False, f"Schlüssel abgelehnt (HTTP {r.status_code})"
    return (True, ok) if r.status_code < 400 else (False, f"HTTP {r.status_code}")


def llm_test(base_url: str, key_env: str | None) -> tuple[bool, str]:
    """Prüft einen OpenAI-kompatiblen Dienst über /models (kostet keine Tokens)."""
    headers = {"Authorization": f"Bearer {env(key_env)}"} if key_env else {}
    return http_test(base_url.rstrip("/") + "/models", headers=headers, ok="verbunden (Modelle abrufbar)")
