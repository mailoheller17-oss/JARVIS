from ._basis import GRATIS, KONTINGENT, BEZAHLT, env as _env, http_test, llm_test

name = "higgsfield"
titel = "Higgsfield"
kategorie = "Video-KI"
beschreibung = "KI-Videos und Kamerafahrten. Verbraucht Credits!"
kosten = BEZAHLT
env = ['HIGGSFIELD_API_KEY']
key_url = "https://cloud.higgsfield.ai/"
hinweis = "Kostet Credits pro Video. Nur einschalten, wenn du das willst."


def test():
    return (True, "Schlüssel vorhanden (kein Test, um keine Credits zu verbrauchen)") if _env("HIGGSFIELD_API_KEY") else (False, "Schlüssel fehlt")
