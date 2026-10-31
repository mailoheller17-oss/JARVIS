from ._basis import GRATIS, KONTINGENT, BEZAHLT, env as _env, http_test, llm_test

name = "whisper"
titel = "Whisper (lokal)"
kategorie = "Sprache"
beschreibung = "Spracherkennung offline auf deinem Rechner (faster-whisper)."
kosten = GRATIS
env = []
key_url = "https://github.com/SYSTRAN/faster-whisper"
def bereit():
    import importlib.util
    return bool(importlib.util.find_spec("faster_whisper") or importlib.util.find_spec("whisper"))


def test():
    import importlib.util
    if importlib.util.find_spec("faster_whisper") or importlib.util.find_spec("whisper"):
        return True, "installiert"
    return False, "nicht installiert: pip install faster-whisper"
