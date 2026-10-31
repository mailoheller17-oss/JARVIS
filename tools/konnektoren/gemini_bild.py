from ._basis import GRATIS, KONTINGENT, BEZAHLT, env as _env, http_test, llm_test

name = "gemini_bild"
titel = "Gemini-Bild"
kategorie = "Bilder"
beschreibung = "Bilder mit Gemini (Gratis-Kontingent, abhängig vom Modell)."
kosten = KONTINGENT
env = ['GEMINI_API_KEY']
key_url = "https://aistudio.google.com/apikey"


def test():
    return http_test("https://generativelanguage.googleapis.com/v1beta/models", headers={"x-goog-api-key": _env("GEMINI_API_KEY")})
