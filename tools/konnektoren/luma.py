from ._basis import GRATIS, KONTINGENT, BEZAHLT, env as _env, http_test, llm_test

name = "luma"
titel = "Luma Dream Machine"
kategorie = "Video-KI"
beschreibung = "KI-Videos (vorbereitet)."
kosten = BEZAHLT
env = ['LUMAAI_API_KEY']
key_url = "https://lumalabs.ai/dream-machine/api/keys"
hinweis = "Kostenpflichtig. Nur vorbereitet."


def test():
    return (True, "Schlüssel vorhanden (vorbereitet)") if _env("LUMAAI_API_KEY") else (False, "Schlüssel fehlt")
