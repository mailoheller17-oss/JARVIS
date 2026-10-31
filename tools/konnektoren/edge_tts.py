from ._basis import GRATIS, KONTINGENT, BEZAHLT, env as _env, http_test, llm_test

name = "edge_tts"
titel = "Edge-TTS"
kategorie = "Sprache"
beschreibung = "Microsoft-Neural-Stimmen ohne Schlüssel (Fallback für Jarvis' Stimme)."
kosten = GRATIS
env = []
key_url = "https://github.com/rany2/edge-tts"
stimme = _env("EDGE_TTS_VOICE") or "de-DE-ConradNeural"


def test():
    try:
        import edge_tts  # noqa: F401
    except ImportError:
        return False, "pip install edge-tts"
    return True, f"bereit, Stimme {stimme}"
