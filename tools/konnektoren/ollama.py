from ._basis import GRATIS, KONTINGENT, BEZAHLT, env as _env, http_test, llm_test

name = "ollama"
titel = "Ollama (lokal)"
kategorie = "KI-Text"
beschreibung = "Läuft komplett auf deinem Rechner, gratis und privat."
kosten = GRATIS
env = []
key_url = "https://ollama.com/download"
llm = {
    "base_url": "http://localhost:11434/v1",
    "model": _env("OLLAMA_MODEL") or "llama3.2",
    "key_env": None,
    "prioritaet": 5,
}


def bereit():
    try:
        import httpx
        return httpx.get("http://localhost:11434/api/tags", timeout=0.5).status_code == 200
    except Exception:
        return False


def test():
    return llm_test(llm["base_url"], llm["key_env"])
