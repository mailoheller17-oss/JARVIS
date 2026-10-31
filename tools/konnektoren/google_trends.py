from ._basis import GRATIS, KONTINGENT, BEZAHLT, env as _env, http_test, llm_test

name = "google_trends"
titel = "Google Trends"
kategorie = "Wissen"
beschreibung = "Was gerade in Deutschland trendet (RSS) – Ideen für Edits."
kosten = GRATIS
env = []
key_url = "https://trends.google.com/trending?geo=DE"


def test():
    return http_test("https://trends.google.com/trending/rss?geo=DE")
