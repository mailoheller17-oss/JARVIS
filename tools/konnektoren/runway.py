from ._basis import GRATIS, KONTINGENT, BEZAHLT, env as _env, http_test, llm_test

name = "runway"
titel = "Runway"
kategorie = "Video-KI"
beschreibung = "KI-Videos Gen-3/Gen-4 (vorbereitet)."
kosten = BEZAHLT
env = ['RUNWAYML_API_SECRET']
key_url = "https://dev.runwayml.com/"
hinweis = "Kostenpflichtig. Nur vorbereitet."


def test():
    return (True, "Schlüssel vorhanden (vorbereitet)") if _env("RUNWAYML_API_SECRET") else (False, "Schlüssel fehlt")
