from ._basis import GRATIS, KONTINGENT, BEZAHLT, env as _env, http_test, llm_test

name = "wikipedia"
titel = "Wikipedia"
kategorie = "Wissen"
beschreibung = "Zusammenfassungen für Erklärungen und Lernen."
kosten = GRATIS
env = []
key_url = "https://de.wikipedia.org"


def test():
    return http_test("https://de.wikipedia.org/api/rest_v1/page/summary/Jarvis", headers={"User-Agent": "JarvisApp/1.0"})
