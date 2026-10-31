from ._basis import GRATIS, KONTINGENT, BEZAHLT, env as _env, http_test, llm_test

name = "pollinations"
titel = "Pollinations"
kategorie = "Bilder"
beschreibung = "Bilder per Text, ganz ohne Schlüssel. Perfekt für Thumbnails."
kosten = GRATIS
env = []
key_url = "https://pollinations.ai"


def test():
    return http_test("https://image.pollinations.ai/prompt/test?width=64&height=64&nologo=true", ok="verbunden", timeout=40)
