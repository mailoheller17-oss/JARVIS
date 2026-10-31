from ._basis import GRATIS, KONTINGENT, BEZAHLT, env as _env, http_test, llm_test

name = "duckduckgo"
titel = "DuckDuckGo"
kategorie = "Wissen"
beschreibung = "Schnelle Sofort-Antworten aus dem Web."
kosten = GRATIS
env = []
key_url = "https://duckduckgo.com"


def test():
    return http_test("https://api.duckduckgo.com/", params={"q": "Berlin", "format": "json"})
