from ._basis import GRATIS, KONTINGENT, BEZAHLT, env as _env, http_test, llm_test

name = "pixabay"
titel = "Pixabay"
kategorie = "Material"
beschreibung = "Kostenlose Videos, Fotos und Musik."
kosten = GRATIS
env = ['PIXABAY_API_KEY']
key_url = "https://pixabay.com/api/docs/"


def test():
    return http_test("https://pixabay.com/api/", params={"key": _env("PIXABAY_API_KEY"), "q": "city", "per_page": 3})
