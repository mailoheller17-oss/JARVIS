from ._basis import GRATIS, KONTINGENT, BEZAHLT, env as _env, http_test, llm_test

name = "pexels"
titel = "Pexels"
kategorie = "Material"
beschreibung = "Kostenlose Stock-Videos und Fotos für Edits."
kosten = GRATIS
env = ['PEXELS_API_KEY']
key_url = "https://www.pexels.com/api/new/"


def test():
    return http_test("https://api.pexels.com/v1/search?query=city&per_page=1", headers={"Authorization": _env("PEXELS_API_KEY")})
