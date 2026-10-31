from ._basis import GRATIS, KONTINGENT, BEZAHLT, env as _env, http_test, llm_test

name = "freesound"
titel = "Freesound"
kategorie = "Material"
beschreibung = "Soundeffekte (Whooshes, Hits, Risers) für Edits."
kosten = GRATIS
env = ['FREESOUND_API_KEY']
key_url = "https://freesound.org/apiv2/apply/"


def test():
    return http_test("https://freesound.org/apiv2/search/text/", params={"query": "whoosh", "token": _env("FREESOUND_API_KEY")})
