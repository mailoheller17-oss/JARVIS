from ._basis import GRATIS, KONTINGENT, BEZAHLT, env as _env, http_test, llm_test

name = "deepl"
titel = "DeepL Free"
kategorie = "Übersetzen"
beschreibung = "Top-Übersetzungen, 500.000 Zeichen/Monat gratis."
kosten = KONTINGENT
env = ['DEEPL_API_KEY']
key_url = "https://www.deepl.com/de/pro-api"


def test():
    return http_test("https://api-free.deepl.com/v2/usage", headers={"Authorization": f"DeepL-Auth-Key {_env('DEEPL_API_KEY')}"})
